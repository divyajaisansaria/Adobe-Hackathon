import os
import json
import pdfplumber
import numpy as np
from pathlib import Path

def extract_lines(pdf_path):
    """Extract lines from the PDF with attributes for heading detection."""
    with pdfplumber.open(pdf_path) as pdf:
        all_lines = []
        for page in pdf.pages:
            words = page.extract_words(extra_attrs=["size", "fontname", "bottom"])
            # Group words into lines
            lines = []
            current_line = []
            current_top = None
            for word in sorted(words, key=lambda w: (w["top"], w["x0"])):
                if current_top is None or abs(word["top"] - current_top) > 2:
                    if current_line:
                        line_bottom = max(w["bottom"] for w in current_line)
                        lines.append({
                            "page": page.page_number - 1,
                            "top": current_top,
                            "bottom": line_bottom,
                            "text": " ".join(w["text"] for w in current_line),
                            "font_size": current_line[0]["size"],
                            "is_bold": any("bold" in w["fontname"].lower() for w in current_line),
                            "x0": min(w["x0"] for w in current_line),
                            "x1": max(w["x1"] for w in current_line),
                            "is_uniform": all(w["size"] == current_line[0]["size"] and w["fontname"] == current_line[0]["fontname"] for w in current_line)
                        })
                    current_line = [word]
                    current_top = word["top"]
                else:
                    current_line.append(word)
            if current_line:
                line_bottom = max(w["bottom"] for w in current_line)
                lines.append({
                    "page": page.page_number - 1,
                    "top": current_top,
                    "bottom": line_bottom,
                    "text": " ".join(w["text"] for w in current_line),
                    "font_size": current_line[0]["size"],
                    "is_bold": any("bold" in w["fontname"].lower() for w in current_line),
                    "x0": min(w["x0"] for w in current_line),
                    "x1": max(w["x1"] for w in current_line),
                    "is_uniform": all(w["size"] == current_line[0]["size"] and w["fontname"] == current_line[0]["fontname"] for w in current_line)
                })
            
            # Sort lines by top and compute gaps
            lines.sort(key=lambda l: l["top"])
            for i, line in enumerate(lines):
                if i == 0:
                    line["gap"] = line["top"]
                else:
                    line["gap"] = line["top"] - lines[i-1]["bottom"]
            
            all_lines.extend(lines)
        
        # Compute global statistics
        all_font_sizes = [line["font_size"] for line in all_lines]
        median_font_size = np.median(all_font_sizes) if all_font_sizes else 0
        
        # Count frequency of each font size
        font_size_counts = {}
        for fs in all_font_sizes:
            font_size_counts[fs] = font_size_counts.get(fs, 0) + 1
        
        total_lines = len(all_lines)
        
        # Add attributes to each line
        for i, line in enumerate(all_lines):
            page = pdf.pages[line["page"]]
            line["word_count"] = len(line["text"].split())
            line["is_near_top"] = line["top"] < page.height * 0.2
            center = page.width / 2
            line_center = (line["x0"] + line["x1"]) / 2
            line["is_centered"] = abs(line_center - center) < page.width * 0.1
            fs = line["font_size"]
            line["fs_frequency"] = font_size_counts[fs] / total_lines if total_lines > 0 else 0
            # Check if next line continues the text (indicating content)
            line["is_followed_closely"] = (i + 1 < len(all_lines) and 
                                          all_lines[i+1]["page"] == line["page"] and 
                                          all_lines[i+1]["top"] - line["bottom"] < 10 and 
                                          abs(all_lines[i+1]["font_size"] - line["font_size"]) < 1)
        
        first_page_height = pdf.pages[0].height if pdf.pages else 0
        return all_lines, median_font_size, first_page_height

def merge_title_lines(candidates):
    """Merge consecutive title lines with similar properties, allowing 2-3 lines."""
    if not candidates:
        return "", []
    candidates.sort(key=lambda l: l["top"])
    title_lines = [candidates[0]]
    prev_line = candidates[0]
    max_lines = 3  # Limit title to 3 lines max
    for line in candidates[1:]:
        if (len(title_lines) < max_lines and
            abs(line["font_size"] - prev_line["font_size"]) < 1 and 
            line["top"] - prev_line["bottom"] < 20 and 
            not line["is_followed_closely"]):
            title_lines.append(line)
            prev_line = line
        else:
            break
    title_text = " ".join(line["text"] for line in title_lines)
    return title_text, title_lines

def classify_headings(lines, median_font_size, first_page_height):
    """Classify lines into Title, H1, H2, H3 with improved hierarchy and limits."""
    # Identify content-like font sizes (used in >20% of lines)
    total_lines = len(lines)
    font_size_freq = {}
    for line in lines:
        fs = line["font_size"]
        font_size_freq[fs] = font_size_freq.get(fs, 0) + 1
    content_font_sizes = {fs for fs, count in font_size_freq.items() if count / total_lines > 0.2}

    # Filter potential headings with stricter criteria
    potential_headings = []
    for line in lines:
        if (line["is_uniform"] and 
            line["font_size"] not in content_font_sizes and
            line["word_count"] < 10 and
            (line["font_size"] > median_font_size * 1.2 or line["is_bold"] or line["is_centered"]) and
            (line["gap"] > 20 or line["is_near_top"]) and
            line["fs_frequency"] < 0.1 and
            not line["is_followed_closely"]):
            potential_headings.append(line)
    
    # Detect title on first page (up to 3 lines)
    title_candidates = [line for line in potential_headings if line["page"] == 0 and line["is_near_top"]]
    title_text, title_lines = merge_title_lines(title_candidates)
    
    # Remove title lines from potential headings
    potential_headings = [h for h in potential_headings if h not in title_lines]
    
    # Fallback: if no title, use first line of first page
    if not title_text and lines and lines[0]["page"] == 0:
        title_text = lines[0]["text"]
    
    # Group headings by page and enforce 4-5 headings per page
    headings_by_page = {}
    for h in potential_headings:
        page = h["page"]
        if page not in headings_by_page:
            headings_by_page[page] = []
        headings_by_page[page].append(h)
    
    outline = []
    for page, page_headings in headings_by_page.items():
        # Sort by position (top) to maintain H1 > H2 > H3 order
        page_headings.sort(key=lambda h: h["top"])
        
        # Limit to 5 headings per page
        page_headings = page_headings[:5]
        
        # Get unique font sizes in descending order
        heading_font_sizes = sorted(set(h["font_size"] for h in page_headings), reverse=True)
        
        # Map font sizes to levels: H1 (largest), H2 (next), H3 (others)
        level_map = {}
        if heading_font_sizes:
            level_map[heading_font_sizes[0]] = "H1"
            if len(heading_font_sizes) > 1:
                level_map[heading_font_sizes[1]] = "H2"
            for fs in heading_font_sizes[2:]:
                level_map[fs] = "H3"
        
        # Assign levels, adjusting with gaps and position
        for i, h in enumerate(page_headings):
            fs = h["font_size"]
            level = level_map.get(fs, "H3")
            # Promote based on gap or position
            if h["gap"] > 30 and level != "H1" and i < 2:  # First two can be H1/H2
                level = "H1" if i == 0 else "H2"
            outline.append({
                "level": level,
                "text": h["text"],
                "page": h["page"]
            })
    
    # Sort outline by page and position
    outline.sort(key=lambda x: (x["page"], x["text"]))
    
    return outline, title_text

def process_pdfs(input_dir, output_dir):
    """Process PDFs and save heading outlines as JSON."""
    os.makedirs(output_dir, exist_ok=True)
    
    for pdf_file in Path(input_dir).glob("*.pdf"):
        print(f"Processing {pdf_file}")
        lines, median_font_size, first_page_height = extract_lines(pdf_file)
        outline, title = classify_headings(lines, median_font_size, first_page_height)
        
        output = {
            "title": title,
            "outline": outline
        }
        
        output_path = os.path.join(output_dir, f"{pdf_file.stem}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)
        print(f"Saved output to {output_path}")

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    process_pdfs(input_dir, output_dir)

if __name__ == "__main__":
    main()
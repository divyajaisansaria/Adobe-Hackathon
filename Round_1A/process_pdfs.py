import os
import json
import fitz  # PyMuPDF
from collections import defaultdict
from statistics import median

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def extract_title(doc):
    # Try metadata first
    title = doc.metadata.get("title", "") or ""
    if title and title.lower() != "untitled":
        return title.strip()
    
    # Else, get first page and extract largest, centered font text
    page = doc[0]
    blocks = page.get_text("dict")["blocks"]
    candidates = []

    for b in blocks:
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                text = s["text"].strip()
                if len(text.split()) >= 3 and s["size"] > 10:
                    candidates.append((s["size"], text, s))  # store text + font size

    if candidates:
        # Pick the largest font size text
        candidates.sort(reverse=True)
        return candidates[0][1].strip()
    
    return ""

def extract_outline(doc):
    headings = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        
        for b in blocks:
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    text = s["text"].strip()
                    if not text or len(text.split()) < 2:
                        continue
                    
                    size = round(s["size"], 1)
                    is_bold = "bold" in s.get("font", "").lower()
                    
                    # Heuristic: Consider as heading candidates
                    if size >= 10 and is_bold:
                        headings.append({
                            "text": text,
                            "size": size,
                            "font": s.get("font"),
                            "page": page_num
                        })

    if not headings:
        return []

    # Get unique sizes and rank from largest to smallest
    sizes = sorted(set(h["size"] for h in headings), reverse=True)
    size_to_level = {}

    for i, sz in enumerate(sizes[:3]):  # Up to H3
        size_to_level[sz] = f"H{i+1}"

    structured = []
    for h in headings:
        level = size_to_level.get(h["size"])
        if level:
            structured.append({
                "level": level,
                "text": h["text"],
                "page": h["page"]
            })

    return structured

def process_pdf_file(file_path):
    with fitz.open(file_path) as doc:
        title = extract_title(doc)
        outline = extract_outline(doc)
        
        return {
            "title": title,
            "outline": outline
        }

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            base_name = os.path.splitext(filename)[0]
            json_path = os.path.join(OUTPUT_DIR, base_name + ".json")

            result = process_pdf_file(pdf_path)

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"Processed {filename} -> {base_name}.json")

if __name__ == "__main__":
    main()

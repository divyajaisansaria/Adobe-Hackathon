📄 Adobe PDF Content Extractor (Hackathon-1A)
This project provides a containerized solution using Docker to automatically extract structured data from PDF documents and convert them into corresponding JSON files.

🚀 How to Run
Follow these steps to set up and run the project on your local machine.

✅ Prerequisites
Ensure Docker Desktop is installed and running on your system.

📥 Step 1: Clone the Repository
bash
Copy
Edit
git clone https://github.com/divyajaisansaria/Adobe-Hackathon-1a && cd Adobe-Hackathon-1a
📂 Step 2: Add Input Files
Place all your PDF files into the input/ folder.

🛠️ Step 3: Build & Run the Docker Container
🔷 For Windows (PowerShell)
powershell
Copy
Edit
docker build --platform linux/amd64 -t adobe-round-1a .
powershell
Copy
Edit
docker run --rm -v ${PWD}/input:/app/input:ro -v ${PWD}/output/adobe-round-1a/:/app/output --network none adobe-round-1a
🔶 For macOS / Linux (Bash)
bash
Copy
Edit
docker build --platform linux/amd64 -t adobe-round-1a .
bash
Copy
Edit
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/adobe-round-1a/:/app/output --network none adobe-round-1a
📁 Step 4: Access the Output
After execution, the extracted .json files will be available in the output/adobe-round-1a/ directory.

🧠 Project Explanation
📁 File Structure
graphql
Copy
Edit
ADOBE-HACKATHON-1A/
├── input/                  # Place source PDF files here
├── output/
│   └── adobe-round-1a/     # JSON output files appear here
├── packages/
├── Dockerfile              # Docker build configuration
├── process_pdf.py          # Core processing script
├── README.md
└── requirements.txt        # Python dependencies
📄 File Descriptions
Dockerfile: Instructions to build the Docker image with required dependencies.

process_pdf.py: Reads PDFs, extracts structured data, and saves it as JSON.

requirements.txt: Lists all required Python libraries.

input/: Directory to store source PDF files (read-only in container).

output/: Directory to save generated JSON files (write-enabled in container).

🔄 How It Works
When you run the Docker container:

It mounts the local input/ and output/ directories.

Executes process_pdf.py inside the isolated Docker environment.

Extracts textual and structural data from PDFs.

Saves results as .json files in the output/adobe-round-1a/ folder.

This ensures consistent and environment-independent execution across any system.
# Adobe PDF Content Extractor (Hackathon-1A)

This project provides a containerized solution using Docker to automatically extract structured data from PDF documents and output it into corresponding JSON files.

---

## 🚀 How to Run

Follow these steps to set up and run the project on your local machine.

### Prerequisites

* Ensure you have **Docker Desktop** installed and running on your system. You can download it from the [official Docker website](https://www.docker.com/products/docker-desktop/).

### Step 1: Clone the Repository

Open your terminal or command prompt and run the following command to clone the project:

```bash
git clone [https://github.com/divyajaisansaria/Adobe-Hackathon-1a](https://github.com/divyajaisansaria/Adobe-Hackathon-1a)
cd Adobe-Hackathon-1a
Step 2: Add Input Files
Place all the PDF files you want to process inside the input folder.

Step 3: Build & Run the Docker Container
The following commands will build the Docker image and run the container. The script will process the PDFs from the input folder and place the resulting JSON files in the output/adobe-round-1a directory.

For Windows (using PowerShell)
PowerShell

# Build the Docker image
docker build --platform linux/amd64 -t adobe-round-1a .

# Run the container
docker run --rm -v ${PWD}/input:/app/input:ro -v ${PWD}/output/adobe-round-1a/:/app/output --network none adobe-round-1a
For macOS / Linux
Bash

# Build the Docker image
docker build --platform linux/amd64 -t adobe-round-1a .

# Run the container
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/adobe-round-1a/:/app/output --network none adobe-round-1a
Step 4: Access the Output
Once the container finishes running, you can find the extracted .json files in the output/adobe-round-1a directory.

🛠️ Project Explanation
File Structure
ADOBE-HACKATHON-1A/
├── input/
│   └── (Your source PDF files go here)
├── output/
│   └── adobe-round-1a/
│       └── (Generated JSON files appear here)
├── packages/
├── Dockerfile
├── process_pdf.py
├── README.md
└── requirements.txt
File Descriptions
Dockerfile: Contains the instructions to build the Docker image, setting up the environment and dependencies needed to run the Python script.

process_pdf.py: The core Python script that reads each PDF from the input directory, processes it to extract data, and saves the result as a JSON file.

requirements.txt: Lists the Python libraries required for the project (e.g., PDF processing libraries), which are installed by the Dockerfile.

input/: The directory where you must place your source PDFs. This folder is mounted as a read-only volume in the container.

output/: The directory where the final JSON files are stored. This folder is mounted as a writeable volume.

How It Works
The entire workflow is automated using Docker. When you run the docker run command, it starts a new container based on the adobe-round-1a image. Inside this isolated environment, the process_pdf.py script executes automatically. It accesses the PDF files you placed in the local input folder, processes each one to extract key textual and structural information, and then writes the output to a new JSON file in the output/adobe-round-1a directory on your machine. Using Docker ensures that the processing script runs consistently across different machines without any need for manual dependency installation.
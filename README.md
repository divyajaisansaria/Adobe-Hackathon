# 📄 Adobe PDF Content Extractor (Hackathon-1A)

This project provides a containerized solution using **Docker** to automatically extract structured data from PDF documents and convert them into corresponding **JSON** files.

## 🚀 How to Run

### ✅ Prerequisites

Ensure **Docker Desktop** is installed and running on your system.  
👉 [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 📥 Step 1: Clone the Repository

Run:  
```bash
git clone https://github.com/divyajaisansaria/Adobe-Hackathon-1a
cd Adobe-Hackathon-1a
```
### 📂 Step 2: Add Input Files

Place all your PDF files inside the `input/` folder.

### 🛠️ Step 3: Build & Run the Docker Container

#### 🔷 For Windows (PowerShell)
```bash
docker build --platform linux/amd64 -t adobe-round-1a .

```
```bash
docker run --rm -v ${PWD}/input:/app/input:ro -v ${PWD}/output/adobe-round-1a/:/app/output --network none adobe-round-1a

```

#### 🔶 For macOS / Linux (Bash)
```bash
docker build --platform linux/amd64 -t adobe-round-1a .

```
```bash
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/adobe-round-1a/:/app/output --network none adobe-round-1a

```
### 📁 Step 4: Access the Output

After execution, the extracted `.json` files will be available in the `output/adobe-round-1a/` directory.

### ⚙️ Performance & Constraints
This model meets the following requirements:

- 🚀 Performance: Processes 50 PDFs in under 10 seconds.
- 🔒 Offline: Operates without internet access for enhanced security.
- 📦 Size: The optimized Docker image is under 450MB.

### 📄 File Descriptions

- `Dockerfile`: Contains instructions to build the Docker image with all required dependencies.
- `process_pdf.py`: Core Python script that extracts structured data from each PDF and saves it to a JSON file.
- `requirements.txt`: Lists all the Python libraries required by the script.
- `input/`: Folder to place the input PDF files. It is mounted as read-only in the container.
- `output/`: Folder where the extracted JSON files will be saved. It is mounted as a write-enabled volume.

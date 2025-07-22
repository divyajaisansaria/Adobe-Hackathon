# Add --platform=linux/amd64 to force the build for x86_64 architecture
FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# IMPORTANT: This assumes the base image already contains 'poppler-utils'.
# You MUST confirm this with the hackathon organizers.

# Copy your local files into the Docker image
COPY requirements.txt .
COPY process_pdf.py .
COPY ./packages /app/packages

# Install python packages from the local folder, NOT the internet
RUN pip install --no-cache-dir --no-index --find-links=/app/packages -r requirements.txt

# Create input and output directories as required by the hackathon run command
# Note: The run command mounts volumes here, so these folders must exist.
RUN mkdir -p /app/input /app/output

# Set the entrypoint to run your script
CMD ["python", "process_pdf.py"]
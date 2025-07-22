# Use the base image (assuming it has poppler-utils)
FROM python:3.10-slim

WORKDIR /app

# IMPORTANT: This assumes the base image already contains 'poppler-utils'.
# Confirm this with the hackathon organizers.

# Copy local files into the Docker image
COPY requirements.txt .
COPY process_pdf.py .
COPY ./packages /app/packages

# Install python packages from the local folder, NOT the internet
# --no-index prevents network access
# --find-links points to our local packages
RUN pip install --no-cache-dir --no-index --find-links=/app/packages -r requirements.txt

# Create required input/output directories
RUN mkdir -p /app/input /app/output

# Set the entrypoint to run your script
CMD ["python", "process_pdf.py"]
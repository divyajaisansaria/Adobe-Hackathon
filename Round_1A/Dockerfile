# Use the base image provided by the hackathon (or python:3.10-slim if they confirm it has poppler-utils)
FROM python:3.10-slim

WORKDIR /app

# IMPORTANT: The 'apt-get' command has been removed.
# This assumes the base image already contains the 'poppler-utils' system dependency.
# You MUST confirm this with the hackathon organizers.

# Copy your local files into the Docker image
COPY requirements.txt .
COPY process_pdf.py .
COPY ./packages /packages

# Install python packages from the local folder, NOT the internet
RUN pip install --no-cache-dir --no-index --find-links=/packages -r requirements.txt

# Create input and output directories as required by the hackathon run command
# Note: The run command mounts volumes here, so these folders must exist.
RUN mkdir -p /app/input /app/output

# Set the entrypoint to run your script
CMD ["python", "process_pdf.py"]
FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
COPY requirements.txt .
COPY process_pdf.py .
COPY ./packages /app/packages
RUN pip install --no-cache-dir --no-index --find-links=/app/packages -r requirements.txt
RUN mkdir -p /app/input /app/output
CMD ["python", "process_pdf.py"]
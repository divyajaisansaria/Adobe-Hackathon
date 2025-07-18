FROM python:3.10-slim

RUN pip install PyMuPDF

WORKDIR /app

COPY process_pdfs.py .

CMD ["python", "process_pdfs.py"]

FROM python:3.11
WORKDIR /app

# Системные зависимости для OCR чеков (pytesseract + opencv-python-headless).
# tesseract-ocr-rus/eng — языковые пакеты; libglib2.0-0 нужен OpenCV.
RUN apt-get update && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-rus \
        tesseract-ocr-eng \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY bot/. .
COPY backend ./backend
RUN pip install --upgrade pip && pip install -r requirements.txt
ENV PYTHONPATH=/app:/app/backend
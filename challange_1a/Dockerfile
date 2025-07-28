# Use Alpine-based Python 3.9
FROM --platform=linux/amd64 python:3.9-alpine

WORKDIR /app

# Install minimal dependencies for PyMuPDF and spacy
RUN apk add --no-cache \
    libstdc++ \
    && apk add --no-cache --virtual .build-deps \
    build-base \
    python3-dev \
    && pip install --no-cache-dir PyMuPDF \
    && pip install --no-cache-dir spacy \
    && python -m spacy download en_core_web_sm \
    && apk del .build-deps \
    && rm -rf /root/.cache/pip

# Copy application
COPY pdf_process.py .

# Run the script
CMD ["python", "pdf_process.py"]
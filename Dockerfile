FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip pip install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY data/DIBaS_Dataset_png /app/data/DIBaS_Dataset_png

COPY models /app/models

COPY logo.png /app/logo.png
COPY qr_image.png /app/qr_image.png

COPY app.py /app/app.py

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
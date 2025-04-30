FROM python:3.12.10-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libsm6 \
    libxext6 \
    libxrender1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY camVideo.py .
COPY page.html .

CMD ["python", "camVideo.py"]

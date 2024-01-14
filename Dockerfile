FROM python:3.11-alpine

RUN apk update && apk add --no-cache \
    python3-dev \
    py3-pip

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python3", "tg_bot.py"]

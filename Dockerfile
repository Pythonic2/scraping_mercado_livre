FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install
RUN apt-get update && apt-get install -y chromium
COPY . .

CMD ["chromium-browser"]

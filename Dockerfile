FROM playw-bot-app:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install
RUN playwright install-deps
RUN apt-get update && apt-get install -y
COPY . .
CMD ["python","main.py"]

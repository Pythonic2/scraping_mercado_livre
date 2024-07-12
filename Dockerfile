FROM ultrafunk/undetected-chromedriver

# Instale o Chrome
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copie seu código para o contêiner
COPY . /app

WORKDIR /app

CMD ["python","main.py"]

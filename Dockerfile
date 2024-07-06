# Use a imagem oficial do Python
FROM balenalib/raspberry-pi-python
# Instale o Playwright e dependências do navegador (Chromium, Firefox, WebKit)
RUN apt-get update && apt-get install -y \
    wget \
    xvfb \
    libnss3 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Instale o Playwright via pip
RUN pip install playwright

# Configuração do Playwright para uso com Python
RUN playwright install
RUN playwright install-deps
RUN apt-get install libgbm1

# Diretório de trabalho para a aplicação
WORKDIR /app

# Copie os arquivos de aplicação para o contêiner
COPY . .

CMD ["python", "main.py"]

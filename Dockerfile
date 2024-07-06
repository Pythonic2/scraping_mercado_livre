# Use a imagem oficial do Python
FROM python:3.11

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

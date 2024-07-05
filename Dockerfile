# Use uma imagem base oficial do Python
FROM python:3.11

# Instale o Selenium
RUN pip install selenium

# Copie o código da aplicação para o contêiner
COPY . /app

# Defina o diretório de trabalho
WORKDIR /app

# Comando para executar a aplicação
CMD ["python", "your_script.py"]

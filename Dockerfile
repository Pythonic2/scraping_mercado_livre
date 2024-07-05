# Use a imagem base do Python 3.11
FROM python:3.11

# Defina o diretório de trabalho
WORKDIR /app

# Copie os requisitos para o contêiner
COPY requirements.txt requirements.txt

# Instale os pacotes necessários
RUN pip install -r requirements.txt

# Copie o restante do código do aplicativo
COPY . .

# Comando para executar os testes
CMD ["python","main.py"]

# Use a imagem oficial do Python
FROM python:3.11

# Diretório de trabalho para a aplicação
WORKDIR /app

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instale os pacotes necessários
RUN pip install --no-cache-dir -r requirements.txt

# Copie os arquivos de aplicação para o contêiner
COPY . .

# Comando para iniciar a aplicação
CMD ["python", "main.py"]

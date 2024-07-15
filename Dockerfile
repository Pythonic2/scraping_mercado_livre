# Use a imagem oficial do Python
FROM python:3.10

# Configura o diretório de trabalho
WORKDIR /app

# Copia o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install
RUN playwright install-deps 
# Copia o restante da aplicação para o contêiner
COPY . .

# Executa a aplicação
CMD ["python", "main.py"]

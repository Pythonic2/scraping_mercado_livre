# Usar uma imagem base oficial do Python
FROM python:3.11

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação para o diretório /app no contêiner
COPY . /app
WORKDIR /app

# Comando para rodar a aplicação
CMD ["python", "main.py"]

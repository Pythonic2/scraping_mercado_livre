FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy
# Use a imagem base do Playwright com Python

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

COPY . .

RUN ["python","main.py"]
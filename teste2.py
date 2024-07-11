# 2 — Palavra mais longa

# Desafio:

# O desafio consiste em criar uma função que irá receber um texto (string) e retornará a palavra mais longa.

# Segue exemplo de texto:


lista_palavras = ["O Louco do Python","e em cada linha de código", "eu encontre a sabedoria."]
tamanhos = []
for item in lista_palavras:
    tamanhos.append(len(item))

maior = max(tamanhos)
print(maior)
#!/bin/bash

# Navega um diretório acima para a raiz do projeto
cd ..

# Copia todos os arquivos e diretórios de 'prod' para a raiz, sobrescrevendo os existentes
cp -r prod/* .

# Executa o docker-compose up
docker-compose up -d --build
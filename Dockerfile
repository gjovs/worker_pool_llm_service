FROM python:3.15-slim

WORKDIR /app

# Configura variáveis de ambiente para o Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copia e instala as dependências primeiro para otimizar o cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação, que está dentro de um módulo 'app'
COPY ./app /app/src

# O comando para iniciar o worker de IA. 
# `python -m src` executa o arquivo __main__.py dentro do diretório 'src'.
CMD ["python", "-m", "src"]
# Use uma imagem base do Python (escolha a versão que você precisa)
FROM python:3.9-slim-buster

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo requirements.txt para o container
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do seu aplicativo para o container
COPY . .

# Defina a variável de ambiente FLASK_APP (se necessário)
ENV FLASK_APP=app.py

# Defina a variável de ambiente FLASK_DEBUG (opcional)
ENV FLASK_DEBUG=0

# Exponha a porta que o seu aplicativo Flask usa (geralmente 5000)
EXPOSE 5000

# Defina o comando para iniciar o seu aplicativo
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
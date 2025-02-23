# Usar una imagen base con Python 3.11+
FROM python:3.13-slim

# Definir el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY requirements.txt ./
COPY gemini/ /app/
COPY .env .env

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puertos (si se usa webhook en lugar de polling)
# EXPOSE 8443

# Comando por defecto para ejecutar el bot
CMD ["python", "bot.py"]

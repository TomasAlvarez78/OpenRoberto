# Usa una imagen base de Python
FROM python:3.13

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requisitos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto en el que corre tu aplicación
EXPOSE 8000

# Comando para ejecutar el servidor con uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
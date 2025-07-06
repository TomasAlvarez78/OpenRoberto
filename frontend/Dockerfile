# Usa una imagen base de Node.js
FROM node:24-alpine

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo package.json y package-lock.json
COPY package*.json ./

# Instala las dependencias
RUN npm install

# Copia el resto del código de la aplicación
COPY . .

# Construye la aplicación para producción (ajústalo según tu framework)
RUN npm run build

# Expone el puerto en el que corre tu aplicación (ajústalo según tu configuración)
EXPOSE 3000

# Comando para ejecutar la aplicación
CMD ["npm", "start"]
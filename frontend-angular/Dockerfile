# Estágio de build
FROM node:20-alpine as build

WORKDIR /app

# Copiar arquivos de dependências
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar o código fonte
COPY . .

# Build da aplicação
RUN npm run build

# Estágio de produção
FROM nginx:alpine

# Copiar os arquivos de build do estágio anterior
COPY --from=build /app/dist/angular-model/browser /usr/share/nginx/html

# Copiar o favicon da pasta public
COPY public/favicon.ico /usr/share/nginx/html/

# Copiar configuração do nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor porta 80
EXPOSE 80

# Iniciar nginx
CMD ["nginx", "-g", "daemon off;"] 
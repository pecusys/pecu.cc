FROM nginx:alpine
COPY ./client/build /var/www
COPY nginx.conf /etc/nginx/nginx.conf
ENTRYPOINT ["nginx","-g","daemon off;"]

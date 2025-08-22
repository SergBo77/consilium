#!/usr/bin/env sh

main () {
   echo "
   server {
       listen 80;

       gzip on;
       gzip_disable "msie6";
       gzip_vary on;
       gzip_proxied any;
       gzip_comp_level 6;
       gzip_buffers 16 8k;
       gzip_http_version 1.1;
       gzip_min_length 0;
       gzip_types text/plain application/javascript text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript application/vnd.ms-fontobject application/x-font-ttf font/opentype image/svg+xml;

       root /usr/share/nginx/html;
       try_files \$uri \$uri/ /index.html;
       index index.html;

   } " > /etc/nginx/conf.d/default.conf;

   nginx "$@"
}

main "$@"

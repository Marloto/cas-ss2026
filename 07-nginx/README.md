docker run -d \
  --mount type=bind,source=/Users/seb/Entwicklung/THI/Repositories/thi-snippets/cas/cas-ss2026/07-nginx,target=/usr/share/nginx/html \
  -p 8080:80 nginx


docker run -d \
  --mount source=mydata,target=/usr/share/nginx/html \
   -p 8080:80 nginx

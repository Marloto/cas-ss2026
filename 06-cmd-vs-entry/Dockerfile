FROM alpine:3.12

RUN echo 'hello' > test.txt

ENTRYPOINT ["ls", "-la"]
# docker run test cat test.txt führt zu "ls -la; cat test.txt" als Gesamtbefehl
FROM rasa/rasa:3.6.2

WORKDIR /app

COPY . /app

EXPOSE 10000

CMD ["run", "--enable-api", "--cors", "*", "--port", "10000"]

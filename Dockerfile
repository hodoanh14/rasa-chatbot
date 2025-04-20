FROM rasa/rasa:3.6.2

WORKDIR /app

COPY . /app

EXPOSE 10000

RUN rasa train

CMD ["run", "--enable-api", "--cors", "*", "--port", "10000"]

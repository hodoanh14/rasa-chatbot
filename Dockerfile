FROM rasa/rasa:3.6.2

WORKDIR /app

COPY . /app

COPY models/ /app/models/

EXPOSE 10000


CMD ["run", "--enable-api", "--model", "models", "--cors", "*", "--port", "10000"]

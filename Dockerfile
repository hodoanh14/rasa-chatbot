FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug"]

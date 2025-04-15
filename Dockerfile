FROM rasa/rasa:3.6.10

# Copy toàn bộ mã nguồn vào container
COPY . /app
WORKDIR /app

# Train mô hình
RUN rasa train

# Chạy server Rasa khi container khởi động
CMD ["run", "--enable-api", "--port", "8000", "--cors", "*"]

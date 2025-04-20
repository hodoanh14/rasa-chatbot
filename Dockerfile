FROM rasa/rasa:3.6.2

WORKDIR /app

# Copy toàn bộ project
COPY . /app

# Đảm bảo models được copy đúng
COPY models/ /app/models/

# Mở cổng (bạn đang dùng 10000)
EXPOSE 10000

# Lệnh khởi động Rasa
CMD ["rasa", "run", "--enable-api", "--model", "models", "--cors", "*", "--port", "10000", "--debug"]

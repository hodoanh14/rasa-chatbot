FROM rasa/rasa:3.6.2

WORKDIR /app

# Copy toàn bộ project
COPY . /app
# Đảm bảo models được copy đúng
COPY models/ /app/models/

# Mở cổng (bạn đang dùng 10000)
EXPOSE 10000

# Lệnh khởi động Rasa
CMD ["run", "--enable-api", "--model", "models/20250420-225707-brass-lyrics.tar.gz", "--cors", "*", "--port", "10000", "--debug"]

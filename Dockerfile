FROM rasa/rasa:3.6.10

# Copy toàn bộ mã nguồn vào container
COPY . /app
WORKDIR /app

# Cài đặt các thư viện bổ sung nếu có
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Train mô hình
RUN rasa train

# Chạy server Rasa khi container khởi động
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "8000"]

# Sử dụng image Python 3.10 làm base image
FROM python:3.10

# Cài đặt netcat-openbsd để kiểm tra kết nối mạng
RUN apt-get update && apt-get install -y netcat-openbsd

# Chỉ định thư mục làm việc
WORKDIR /app

# Copy file yêu cầu
COPY requirements.txt .

# Cài đặt các yêu cầu
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Chắc chắn rằng entrypoint.sh có quyền thực thi
RUN chmod +x entrypoint.sh

# Chỉ định entrypoint cho container, giúp tự động chạy các lệnh trước khi chạy server
ENTRYPOINT ["bash", "/app/entrypoint.sh"]

# Lệnh CMD để chạy Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

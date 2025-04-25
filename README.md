# 📝 Interview BuyNgon – Backend System

Project demo cho vòng 2 vị trí backend developer tại BN. 

Dự án được xây dựng bằng Django + PostgreSQL + Docker

Created by : gsnake1102

Phone : 093.797.4444

Email : ntdung2508@gmail.com

---

## 📚 Table of Contents

- [📌 Technical Stack](#-technical-stack)
- [🐳 Docker Usage](#-docker-usage)
- [📂 Folder Structure](#-folder-structure)
- [🔐 Environment Variables](#-environment-variables)

---

## 📌 Technical Stack

- **Python**: 3.10  
- **Database**: PostgreSQL
- **Docker**   

---



## 🐳 Docker Usage
### Build and run containers
```
docker compose up --build
```
### Useful
```
# clean docker

    docker compose down                    # Dừng và xóa container, network (giữ volumes)
    docker compose down -v                # Dừng và xóa container + network + volume
    docker volume ls                      # Liệt kê tất cả volume
    docker volume rm <volume_name>        # Xóa volume cụ thể
-
# manage docker
    docker ps                             # Xem các container đang chạy
    docker ps -a                          # Xem tất cả container (kể cả đã dừng)
    docker stop <container_id_or_name>   # Dừng container
    docker rm <container_id_or_name>     # Xóa container đã dừng
    docker restart <container_name>      # Khởi động lại container
-
# manage image
    docker images                         # Liệt kê tất cả Docker images
    docker rmi <image_name>:<tag>         # Xóa image cụ thể (ví dụ: microservices-user-service:latest)
-
# check port 
    netstat -aon | findstr 5432           # Kiểm tra xem cổng 5432 (PostgreSQL) có đang bị chiếm không
-
# other useful
    docker exec -it <container_name> bash      # Truy cập terminal bên trong container (nếu có bash)
    docker logs <container_name>               # Xem log của container
    docker compose logs                        # Xem log toàn bộ các service trong docker-compose
    docker compose build                       # Build lại image (nếu Dockerfile thay đổi)
    docker compose up -d                       # Chạy docker ở chế độ detached (nền)
    docker network ls                          # Liệt kê các network Docker đang quản lý
    docker network inspect <network_name>     # Xem chi tiết network, giúp debug kết nối giữa các container



```

## 📂 Folder Structure
```
bn_interview_round_2/
├── backend/        
│   ├── backend/
│   ├── user/                
│   ├── accounting/          
│   ├── Dockerfile
│   ├── staticfiles/
│   ├── entrypoint.sh
│   ├── manage.py
│   ├── requirements.txt
├── postgres/       # customize config db
│   ├── pg_hba.conf
│   ├── postgresql.conf  
├── .env                     
├── docker-compose.yml
├── .gitattributes
├── .gitignore
└── README.md
```

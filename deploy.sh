#!/bin/bash
# Deploy Django project script
# Author: bạn 😁

# Thư mục dự án trên VPS
PROJECT_DIR="/var/www/sieutocndc"
VENV_DIR="$PROJECT_DIR/venv"
BRANCH="main"
SERVICE_NAME="gunicorn"

echo "🔄 Bắt đầu deploy dự án..."

# 1. Vào thư mục dự án
cd $PROJECT_DIR || { echo "❌ Không tìm thấy thư mục dự án"; exit 1; }

# 2. Lấy code mới nhất
echo "📥 Đang pull code từ Git..."
git reset --hard
git pull origin $BRANCH || { echo "❌ Lỗi khi pull code"; exit 1; }

# 3. Kích hoạt virtualenv
echo "🐍 Kích hoạt môi trường Python..."
source $VENV_DIR/bin/activate || { echo "❌ Không thể kích hoạt venv"; exit 1; }

# 4. Cài đặt requirements mới
echo "📦 Cài đặt package mới..."
pip install -r requirements.txt

# 5. Chạy migrate
echo "🛠 Đang migrate database..."
python manage.py migrate

# 6. Collect static files
echo "🎨 Thu thập static files..."
python manage.py collectstatic --noinput

# 7. Restart service
echo "🚀 Khởi động lại dịch vụ..."
sudo systemctl restart $SERVICE_NAME

echo "✅ Deploy thành công!"

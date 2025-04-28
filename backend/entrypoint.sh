#!/bin/bash

echo "==== [🚀 ENTRYPOINT STARTED] ===="

# ================================
# STEP 1: Wait for PostgreSQL
# ================================
echo "🔄 Waiting for PostgreSQL at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done
echo "✅ PostgreSQL is up"

# ================================
# STEP 2: Run Migrations
# ================================
echo "🔄 Running makemigrations..."
python manage.py makemigrations --noinput

echo "🔄 Running migrate..."
python manage.py migrate --noinput

echo "🔄 Running script add data to Role model "
python manage.py seed_roles

# ================================
# STEP 3: Create superuser
# ================================
echo "👤 Creating superuser if not exists..."

python manage.py shell << END
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "gsnake")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "gsnake1102@gmail.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "abcd@1234")

if not User.objects.filter(username=username).exists():
    print("➡️ Creating superuser:", username)
    User.objects.create_superuser(username, email, password)
else:
    print("✅ Superuser already exists:", username)
END

# ================================
# STEP 4: Collect static files (optional)
# ================================
echo "🧹 Collecting static files..."
python manage.py collectstatic --noinput

# ================================
# STEP 5: Start server
# ================================
echo "🚀 Starting Django server..."
exec "$@"

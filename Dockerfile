# Base image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run database migrations
RUN python manage.py migrate

# Expose port
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "--timeout", "120", "--workers", "3", "optixpay_backend.wsgi:application", "--bind", "0.0.0.0:8000"]

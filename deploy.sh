#!/bin/bash

# Daily News Flow Deployment Script
# This script automates the deployment process

set -e  # Exit on any error

echo "🚀 Starting Daily News Flow Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements-prod.txt
print_success "Dependencies installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp .env.example .env
    print_warning "Please edit .env file with your production values before continuing"
    exit 1
fi

# Create logs directory
print_status "Creating logs directory..."
mkdir -p logs
print_success "Logs directory created"

# Run Django checks
print_status "Running Django security checks..."
python manage.py check --deploy
print_success "Django checks passed"

# Run migrations
print_status "Running database migrations..."
python manage.py migrate
print_success "Database migrations completed"

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput
print_success "Static files collected"

# Create superuser if it doesn't exist
print_status "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    print('No superuser found. Please create one:')
    exit(1)
else:
    print('Superuser exists')
"

# Test the application
print_status "Running tests..."
python manage.py test
print_success "All tests passed"

print_success "🎉 Deployment completed successfully!"
print_status "To start the server, run: gunicorn daily_news_flow.wsgi:application --bind 0.0.0.0:8000"

echo ""
print_status "📋 Post-deployment checklist:"
echo "   1. Verify .env file has correct production values"
echo "   2. Create superuser if needed: python manage.py createsuperuser"
echo "   3. Configure Nginx reverse proxy"
echo "   4. Set up SSL certificates"
echo "   5. Configure firewall rules"
echo "   6. Set up monitoring and backups"

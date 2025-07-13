# Daily News Flow

A Django web application that aggregates news from multiple sources across different countries and categories.

## Features

- **Multi-source News Aggregation**: Collects news from various reliable news providers
- **Global Coverage**: News from multiple countries and regions
- **Category Organization**: Technology, Business, Sports, Health, Science, Politics, Entertainment, World
- **Responsive Design**: Modern, mobile-friendly interface
- **Search Functionality**: Advanced search with filtering options
- **Admin Interface**: Django admin for content management
- **Real-time Updates**: Continuous news monitoring and updates

## Technology Stack

- **Backend**: Django 5.2.4 (Python web framework)
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **APIs**: Integration with NewsAPI, Guardian API, and other news sources

## Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "Daily News Flow"
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL database**
   ```sql
   CREATE DATABASE daily_news_flow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. **Configure database settings**
   - Update `daily_news_flow/settings.py` with your MySQL credentials
   - Default configuration uses:
     - Database: `daily_news_flow`
     - User: `root`
     - Password: `Clyde@23`
     - Host: `localhost`
     - Port: `3306`

6. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Load sample data (optional)**
   ```bash
   python manage.py load_sample_data
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Website: http://127.0.0.1:8000/
    - Admin: http://127.0.0.1:8000/admin/

## Project Structure

```
Daily News Flow/
├── daily_news_flow/        # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Main configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py
├── news/                   # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── admin.py           # Admin configuration
│   ├── urls.py            # App URL routing
│   └── management/        # Custom management commands
│       └── commands/
│           ├── collect_news.py      # News collection script
│           └── load_sample_data.py  # Sample data loader
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   └── news/              # News app templates
├── static/                # Static files
│   ├── css/               # Stylesheets
│   └── js/                # JavaScript files
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## Models

### Country
- Stores country information with ISO codes
- Fields: name, code, flag_url, is_active

### Category
- News categories with color coding
- Fields: name, slug, description, color, is_active

### NewsProvider
- News source configuration
- Fields: name, website, api_url, api_key, rate_limit, priority

### NewsArticle
- Individual news articles
- Fields: title, slug, description, content, url, image_url, author, published_at, views, is_featured

### NewsCollectionLog
- Tracks news collection activities
- Fields: provider, country, category, articles_collected, status, errors

## Management Commands

### Collect News
```bash
python manage.py collect_news [--provider PROVIDER] [--country COUNTRY] [--category CATEGORY] [--limit LIMIT]
```

### Load Sample Data
```bash
python manage.py load_sample_data
```

## API Integration

The application supports integration with various news APIs:

### NewsAPI.org
- Add your API key to the NewsProvider model
- Supports country and category filtering
- Rate limited to API provider limits

### The Guardian API
- Configure API key in NewsProvider
- Rich content with images and metadata
- Category-based content retrieval

### Custom APIs
- Extend the `collect_news` management command
- Add custom API handlers in `news/management/commands/collect_news.py`

## Configuration

### Environment Variables
Set these in your environment or create a `.env` file:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=daily_news_flow
DB_USER=root
DB_PASSWORD=Clyde@23
DB_HOST=localhost
DB_PORT=3306
NEWS_API_KEY=your-newsapi-key
GUARDIAN_API_KEY=your-guardian-api-key
```

### News Collection
- Configure providers in Django admin
- Set API keys and rate limits
- Schedule regular collection using cron or task schedulers

## Admin Interface

Access the Django admin at `/admin/` to:

- Manage countries, categories, and news providers
- View and moderate articles
- Monitor collection logs
- Configure system settings

## Customization

### Adding New News Sources
1. Create a NewsProvider in admin
2. Add API integration in `collect_news.py`
3. Configure countries and categories
4. Test collection with management command

### Styling
- Modify `static/css/style.css` for custom styling
- Templates are in `templates/` directory
- Uses Bootstrap 5 for responsive design

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure web server (nginx/Apache)
- [ ] Set up SSL certificate
- [ ] Configure logging
- [ ] Set up monitoring

### Docker Support
Docker configuration can be added for containerized deployment.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions, issues, or suggestions:
- Use the contact form in the application
- Check the FAQ section
- Review the documentation

## Roadmap

- [ ] Mobile application (iOS/Android)
- [ ] Real-time notifications
- [ ] User accounts and preferences
- [ ] Social media integration
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Advanced search filters
- [ ] Bookmarking system
- [ ] RSS feed generation
- [ ] API endpoints for third-party access

---

**Daily News Flow** - Your trusted source for global news coverage.

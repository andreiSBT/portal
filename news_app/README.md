# News App - Flask Multi-Tab Web Application

A full-featured news management system built with Flask, featuring user authentication, role-based access control, and a comprehensive content management system.

## Features

### User Authentication
- User registration and login system
- Password hashing with Werkzeug (pbkdf2:sha256)
- Session management with Flask-Login
- Remember-me functionality
- Admin and regular user roles

### News Management (Admin Only)
- **Create, Edit, Delete** news articles
- Rich text content support
- Image upload with validation and resizing
- Article categories with color coding
- Featured articles system
- Draft/publish workflow
- SEO-friendly URL slugs

### Public Features
- Browse all published articles
- Category filtering
- Search functionality (by title, content, summary)
- Article detail view with related articles
- View counter for articles
- Paginated article listings
- Responsive Bootstrap 5 design

### Category Management (Admin Only)
- Create, edit, delete categories
- Color-coded categories
- Category descriptions
- Prevention of deleting categories with articles

## Technology Stack

### Backend
- **Flask 3.0** - Web framework
- **Flask-SQLAlchemy 3.1.1** - ORM
- **Flask-Migrate 4.0.5** - Database migrations
- **Flask-Login 0.6.3** - User session management
- **Flask-WTF 1.2.1** - Form handling with CSRF protection
- **Pillow** - Image processing
- **SQLite** - Database (development)

### Frontend
- **Bootstrap 5.3.0** - CSS framework
- **Bootstrap Icons 1.11.0** - Icon library
- **Custom CSS** - Additional styling
- **Vanilla JavaScript** - Client-side interactivity

## Project Structure

```
news_app/
├── app/
│   ├── __init__.py                 # Application factory
│   ├── models.py                   # Database models
│   ├── extensions.py               # Flask extension instances
│   ├── decorators.py               # Custom decorators
│   ├── blueprints/
│   │   ├── auth/                   # Authentication routes
│   │   ├── main/                   # Home page routes
│   │   └── news/                   # News management routes
│   ├── templates/                  # Jinja2 templates
│   ├── static/                     # CSS, JS, images
│   └── utils/                      # Utility functions
├── migrations/                     # Database migrations
├── config.py                       # Configuration
├── run.py                          # Application entry point
├── seed.py                         # Database seeding script
└── requirements.txt                # Python dependencies
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd news_app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Initialize the database**
   ```bash
   set FLASK_APP=run.py
   flask db upgrade
   ```

7. **Seed the database with sample data** (optional but recommended)
   ```bash
   python seed.py
   ```

## Running the Application

1. **Start the development server**
   ```bash
   python run.py
   ```

2. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`

3. **Login with default credentials**
   - Admin User:
     - Username: `admin`
     - Password: `admin123`
   - Regular User:
     - Username: `john`
     - Password: `password123`

   **Note:** Change these passwords in production!

## Usage

### For Regular Users
1. **Browse News**: Visit the News tab to see all published articles
2. **Read Articles**: Click on any article to read the full content
3. **Search**: Use the search bar to find articles by keyword
4. **Filter by Category**: Click on category buttons to filter articles
5. **Register**: Create an account to access personalized features

### For Admin Users
1. **Create Articles**: Click "New Article" in the navbar
2. **Manage Categories**: Access category management from the Categories link
3. **Edit/Delete**: Use the edit and delete buttons on articles
4. **Feature Articles**: Mark articles as featured to display them on the home page
5. **Draft Mode**: Save articles as drafts before publishing

## Database Models

### User
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `is_admin`: Admin flag
- `is_active`: Active status
- `created_at`: Registration date
- `last_login`: Last login timestamp

### NewsCategory
- `id`: Primary key
- `name`: Category name (unique)
- `slug`: URL-friendly slug
- `description`: Category description
- `color`: Hex color code
- `created_at`: Creation date

### NewsArticle
- `id`: Primary key
- `title`: Article title
- `slug`: URL-friendly slug
- `summary`: Short description
- `content`: Full article content
- `image_filename`: Featured image
- `is_published`: Publication status
- `is_featured`: Featured flag
- `publish_date`: Publication date
- `views`: View counter
- `author_id`: Foreign key to User
- `category_id`: Foreign key to NewsCategory

## Configuration

Edit `config.py` to customize:
- Database URI
- Upload folder location
- File size limits
- Pagination settings
- Session protection
- And more...

## Security Features

- CSRF protection enabled globally
- Password hashing with pbkdf2:sha256
- Admin-only routes protected with custom decorator
- File upload validation (type and size)
- Unique filename generation to prevent path traversal
- SQLAlchemy ORM to prevent SQL injection
- Jinja2 auto-escaping to prevent XSS

## Production Deployment

### Before deploying to production:

1. **Change secret key**
   ```python
   SECRET_KEY='your-strong-random-key-here'
   ```

2. **Use a production database**
   - PostgreSQL (recommended)
   - MySQL/MariaDB

3. **Update configuration**
   ```python
   FLASK_ENV=production
   DEBUG=False
   ```

4. **Set up proper file storage**
   - Consider using cloud storage (AWS S3, Cloudflare R2)

5. **Configure a production server**
   - Gunicorn/uWSGI
   - Nginx as reverse proxy

6. **Enable HTTPS**
   - Use Let's Encrypt or commercial SSL certificate

7. **Set up logging and monitoring**

## Future Enhancements

- Rich text editor (TinyMCE, CKEditor) for article content
- Comment system for articles
- Article tagging beyond categories
- Email notifications for new articles
- User profile pages with avatars
- Analytics dashboard for admins
- REST API endpoints
- Social sharing buttons
- RSS feed generation
- Multilingual support
- Dark mode theme

## Troubleshooting

### Database Issues
- If you encounter database errors, try:
  ```bash
  flask db downgrade
  flask db upgrade
  ```

### Port Already in Use
- Change the port in `run.py` or `config.py`

### Image Upload Failures
- Check upload folder permissions
- Verify file size limits
- Ensure Pillow is installed correctly

### CSRF Token Errors
- Clear browser cookies
- Check that CSRF protection is enabled

## Contributing

This is a personal project, but suggestions and improvements are welcome!

## License

This project is open source and available for educational purposes.

## Contact

For questions or support, please refer to the project documentation.

---

Built with Flask and Bootstrap 5 | 2026

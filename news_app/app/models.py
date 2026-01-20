from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db
import re


class User(db.Model, UserMixin):
    """User model for authentication - Fiascha Citizens"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    # Fiascha Citizen Information
    citizen_id = db.Column(db.String(20), unique=True, nullable=True, index=True)  # e.g., "FSC-2026-001"
    full_name = db.Column(db.String(100), nullable=True)
    citizen_rank = db.Column(db.String(20), default='Citizen')  # Citizen, Official, Minister, President
    desired_jobs = db.Column(db.Text, nullable=True)  # JSON array of up to 3 desired professions

    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships
    news_articles = db.relationship('NewsArticle', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'citizen_id': self.citizen_id,
            'full_name': self.full_name,
            'citizen_rank': self.citizen_rank,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    def generate_citizen_id(self):
        """Generate a unique citizen ID for Fiascha"""
        import random
        year = datetime.utcnow().year
        # Generate ID like FSC-2026-001
        count = User.query.count() + 1
        self.citizen_id = f"FSC-{year}-{count:03d}"

    @property
    def display_name(self):
        """Get display name (full_name if available, otherwise username)"""
        return self.full_name if self.full_name else self.username

    def get_desired_jobs(self):
        """Get list of desired jobs"""
        import json
        if self.desired_jobs:
            try:
                return json.loads(self.desired_jobs)
            except:
                return []
        return []

    def set_desired_jobs(self, jobs_list):
        """Set desired jobs (max 3)"""
        import json
        if len(jobs_list) > 3:
            jobs_list = jobs_list[:3]
        self.desired_jobs = json.dumps(jobs_list)

    def add_desired_job(self, job):
        """Add a desired job (max 3)"""
        jobs = self.get_desired_jobs()
        if job not in jobs and len(jobs) < 3:
            jobs.append(job)
            self.set_desired_jobs(jobs)
            return True
        return False

    def remove_desired_job(self, job):
        """Remove a desired job"""
        jobs = self.get_desired_jobs()
        if job in jobs:
            jobs.remove(job)
            self.set_desired_jobs(jobs)
            return True
        return False

    def toggle_desired_job(self, job):
        """Toggle a desired job selection"""
        jobs = self.get_desired_jobs()
        if job in jobs:
            jobs.remove(job)
            self.set_desired_jobs(jobs)
            return False
        elif len(jobs) < 3:
            jobs.append(job)
            self.set_desired_jobs(jobs)
            return True
        return None  # Max limit reached


class JobApplication(db.Model):
    """Job application requests from citizens"""
    __tablename__ = 'job_applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_title = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, denied
    message = db.Column(db.Text, nullable=True)  # Optional message from citizen
    admin_response = db.Column(db.Text, nullable=True)  # Admin's response/reason
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relationships
    applicant = db.relationship('User', foreign_keys=[user_id], backref='job_applications')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])

    def __repr__(self):
        return f'<JobApplication {self.applicant.username} - {self.job_title}>'

    def approve(self, admin_user, response=None):
        """Approve the job application"""
        self.status = 'approved'
        self.reviewed_by = admin_user.id
        self.reviewed_at = datetime.utcnow()
        self.admin_response = response
        # Add job to user's desired jobs if not already there
        self.applicant.add_desired_job(self.job_title)

    def deny(self, admin_user, response=None):
        """Deny the job application"""
        self.status = 'denied'
        self.reviewed_by = admin_user.id
        self.reviewed_at = datetime.utcnow()
        self.admin_response = response


class Message(db.Model):
    """Messages between Fiascha citizens"""
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')

    def __repr__(self):
        return f'<Message from {self.sender.username} to {self.recipient.username}>'

    def mark_as_read(self):
        """Mark message as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()


class NewsCategory(db.Model):
    """Category model for organizing news articles"""
    __tablename__ = 'news_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    slug = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#3498db')  # Hex color
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    articles = db.relationship('NewsArticle', backref='category', lazy='dynamic')

    def generate_slug(self):
        """Generate slug from name"""
        slug = re.sub(r'[^\w\s-]', '', self.name.lower())
        slug = re.sub(r'[\s_-]+', '-', slug)
        slug = re.sub(r'^-+|-+$', '', slug)
        self.slug = slug

    def __repr__(self):
        return f'<NewsCategory {self.name}>'

    def to_dict(self):
        """Convert category to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'article_count': self.articles.count()
        }


class NewsArticle(db.Model):
    """News article model"""
    __tablename__ = 'news_articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    summary = db.Column(db.String(500))  # Short description
    content = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255))  # Stored image filename

    # Publishing
    is_published = db.Column(db.Boolean, default=False, index=True)
    is_featured = db.Column(db.Boolean, default=False, index=True)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Metadata
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign keys
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('news_categories.id'), nullable=False)

    def generate_slug(self):
        """Generate slug from title"""
        slug = re.sub(r'[^\w\s-]', '', self.title.lower())
        slug = re.sub(r'[\s_-]+', '-', slug)
        slug = re.sub(r'^-+|-+$', '', slug)

        # Ensure uniqueness
        base_slug = slug
        counter = 1
        while NewsArticle.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug

    def increment_views(self):
        """Increment article view count"""
        self.views += 1
        db.session.commit()

    @property
    def image_url(self):
        """Generate full image path"""
        if self.image_filename:
            return f'/static/uploads/news/{self.image_filename}'
        return None

    @property
    def formatted_publish_date(self):
        """Format publish date for display"""
        if self.publish_date:
            return self.publish_date.strftime('%B %d, %Y')
        return None

    def __repr__(self):
        return f'<NewsArticle {self.title}>'

    def to_dict(self):
        """Convert article to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'summary': self.summary,
            'content': self.content,
            'image_filename': self.image_filename,
            'image_url': self.image_url,
            'is_published': self.is_published,
            'is_featured': self.is_featured,
            'publish_date': self.publish_date.isoformat() if self.publish_date else None,
            'formatted_publish_date': self.formatted_publish_date,
            'views': self.views,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author_id': self.author_id,
            'author_username': self.author.username if self.author else None,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None
        }

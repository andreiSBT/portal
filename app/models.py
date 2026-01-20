from datetime import datetime
from app import db

class Category(db.Model):
    """Category model for organizing tasks"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(7), default='#3498db')  # Hex color code
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with Task model
    tasks = db.relationship('Task', backref='category', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name}>'

    def to_dict(self):
        """Convert category to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'task_count': self.tasks.count()
        }


class Task(db.Model):
    """Task model for to-do items"""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=2)  # 1=High, 2=Medium, 3=Low
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key to Category
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    def __repr__(self):
        return f'<Task {self.title}>'

    def to_dict(self):
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None
        }

    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and not self.completed:
            return datetime.utcnow() > self.due_date
        return False

    @property
    def priority_label(self):
        """Get priority label"""
        priority_map = {1: 'High', 2: 'Medium', 3: 'Low'}
        return priority_map.get(self.priority, 'Medium')

# To-Do List Web Application

A feature-rich, web-based to-do list application built with Python Flask. Organize your tasks efficiently with categories, priorities, and due dates.

## Features

- **Task Management**: Create, edit, delete, and mark tasks as complete
- **Categories**: Organize tasks with color-coded categories
- **Priority Levels**: Set task priorities (High, Medium, Low)
- **Due Dates**: Set deadlines for your tasks
- **Filtering**: Filter tasks by status (All, Active, Completed) or by category
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Clean UI**: Modern interface built with Bootstrap 5

## Technology Stack

- **Backend**: Flask 3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Forms**: Flask-WTF with CSRF protection
- **Migrations**: Flask-Migrate (Alembic)
- **Frontend**: Bootstrap 5, Jinja2 templates
- **Icons**: Bootstrap Icons

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or navigate to the project directory**:
   ```bash
   cd a:\Development\project1
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment file** (optional):
   ```bash
   copy .env.example .env
   ```
   Edit `.env` to customize your configuration.

6. **Initialize the database**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Run the application**:
   ```bash
   python run.py
   ```

8. **Access the application**:
   Open your browser and navigate to: `http://localhost:5000`

## Usage Guide

### Creating Tasks

1. Click the "Add New Task" button or navigate to "New Task" in the navbar
2. Fill in the task details:
   - **Title** (required): Brief description of the task
   - **Description** (optional): Additional details
   - **Priority**: Choose High, Medium, or Low
   - **Due Date** (optional): Set a deadline
   - **Category** (optional): Assign to a category
3. Click "Save Task"

### Managing Categories

1. Navigate to "Categories" in the navbar
2. Enter a category name and choose a color
3. Click "Save Category" to create
4. Edit or delete categories using the buttons next to each category

### Filtering Tasks

- Use the filter buttons to view:
  - **All**: All tasks
  - **Active**: Incomplete tasks only
  - **Completed**: Completed tasks only
- Click category badges to filter by category

### Completing Tasks

- Click the "Complete" button on any task card
- Completed tasks will show with a strikethrough
- Click "Reopen" to mark a completed task as active again

## Project Structure

```
project1/
├── app/
│   ├── __init__.py           # Application factory
│   ├── models.py             # Database models
│   ├── forms.py              # WTForms forms
│   ├── routes.py             # Application routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Custom styles
│   │   └── js/
│   │       └── main.js      # Custom JavaScript
│   └── templates/
│       ├── base.html        # Base template
│       ├── index.html       # Task list view
│       ├── task_form.html   # Task form
│       ├── categories.html  # Categories page
│       ├── 404.html         # 404 error page
│       └── 500.html         # 500 error page
├── migrations/              # Database migrations
├── config.py                # Configuration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore file
└── README.md                # This file
```

## Database Schema

### Task Model
- `id`: Primary key
- `title`: Task title (required)
- `description`: Detailed description
- `completed`: Boolean status
- `priority`: Integer (1=High, 2=Medium, 3=Low)
- `due_date`: Optional deadline
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `category_id`: Foreign key to Category

### Category Model
- `id`: Primary key
- `name`: Category name (unique)
- `color`: Hex color code
- `created_at`: Creation timestamp
- `tasks`: One-to-many relationship with Task

## Configuration

The application uses environment variables for configuration. Create a `.env` file based on `.env.example`:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URI=sqlite:///todo_dev.db
```

## Development

### Database Migrations

When you make changes to the models:

```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply the migration
flask db upgrade

# Rollback if needed
flask db downgrade
```

### Viewing Database Contents

```bash
# Open SQLite database
sqlite3 todo_dev.db

# View tables
.tables

# Query data
SELECT * FROM tasks;
SELECT * FROM categories;

# Exit
.exit
```

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, edit `run.py` and change the port number:

```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Database Errors

If you encounter database errors, try resetting the database:

```bash
# Delete the database file
del todo_dev.db

# Delete migrations folder
rmdir /s migrations

# Reinitialize
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Module Not Found Errors

Ensure your virtual environment is activated and all dependencies are installed:

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

## Future Enhancements

Potential features to add:

- User authentication and multi-user support
- Search functionality
- Task notes and comments
- File attachments
- Email reminders
- Multiple tags per task
- Drag-and-drop task reordering
- Dark mode
- Export/import tasks (CSV, JSON)
- Task analytics and statistics

## Contributing

Feel free to fork this project and submit pull requests for improvements!

## License

This project is open source and available for personal and educational use.

## Support

For issues, questions, or suggestions, please create an issue in the project repository.

---

Built with Flask | 2026

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Task, Category
from app.forms import TaskForm, CategoryForm
from datetime import datetime
import os

bp = Blueprint('main', __name__)

# ===== Health Check Route =====

@bp.route('/health')
def health():
    """Health check endpoint for debugging"""
    db_url = os.environ.get('POSTGRES_URL', 'Not set')
    db_configured = db_url != 'Not set'
    # Hide credentials in display
    if db_url and '@' in db_url:
        db_url = db_url.split('@')[0][:20] + '...(hidden)'

    # Test actual database connectivity
    db_connected = False
    db_error = None
    try:
        db.session.execute(db.text('SELECT 1'))
        db_connected = True
    except Exception as e:
        db_error = str(e)

    status = 'healthy' if db_connected else 'unhealthy'
    parts = [
        f"Status: {status}",
        f"DB URL configured: {db_configured}",
        f"DB connected: {db_connected}",
    ]
    if db_error:
        parts.append(f"DB error: {db_error}")

    code = 200 if db_connected else 503
    return '\n'.join(parts), code

# ===== Task Routes =====

@bp.route('/')
@login_required
def index():
    """Homepage - display all tasks with optional filtering"""
    try:
        filter_status = request.args.get('filter', 'all')
        category_id = request.args.get('category', type=int)

        # Base query - filter by current user
        query = Task.query.filter_by(user_id=current_user.id)

        # Apply category filter
        if category_id:
            query = query.filter_by(category_id=category_id)

        # Apply status filter
        if filter_status == 'active':
            query = query.filter_by(completed=False)
        elif filter_status == 'completed':
            query = query.filter_by(completed=True)

        # Order by priority and due date
        tasks = query.order_by(Task.completed, Task.priority, Task.due_date).all()

        # Get all categories for the sidebar/filter (user's categories only)
        categories = Category.query.filter_by(user_id=current_user.id).all()

        # Get counts for filters (user's tasks only)
        total_count = Task.query.filter_by(user_id=current_user.id).count()
        active_count = Task.query.filter_by(user_id=current_user.id, completed=False).count()
        completed_count = Task.query.filter_by(user_id=current_user.id, completed=True).count()

        return render_template('index.html',
                             tasks=tasks,
                             categories=categories,
                             current_filter=filter_status,
                             current_category=category_id,
                             total_count=total_count,
                             active_count=active_count,
                             completed_count=completed_count)
    except Exception as e:
        return f"Database Error: {str(e)}. Please make sure POSTGRES_URL is configured in Vercel.", 500

@bp.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def create_task():
    """Create a new task"""
    form = TaskForm()

    # Populate category choices (user's categories only)
    form.category.choices = [(0, '-- No Category --')] + [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]

    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            category_id=form.category.data if form.category.data != 0 else None,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('task_form.html', form=form, title='New Task', action='Create')

@bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    """Edit an existing task"""
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = TaskForm(obj=task)

    # Populate category choices (user's categories only)
    form.category.choices = [(0, '-- No Category --')] + [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]

    if request.method == 'GET':
        # Pre-populate form with task data
        form.category.data = task.category_id if task.category_id else 0

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        task.category_id = form.category.data if form.category.data != 0 else None
        task.updated_at = datetime.utcnow()

        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('task_form.html', form=form, title='Edit Task', action='Update', task=task)

@bp.route('/tasks/<int:id>/delete', methods=['POST'])
@login_required
def delete_task(id):
    """Delete a task"""
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'info')
    return redirect(url_for('main.index'))

@bp.route('/tasks/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_task(id):
    """Toggle task completion status"""
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    db.session.commit()

    status = 'completed' if task.completed else 'reopened'
    flash(f'Task {status}!', 'success')
    return redirect(url_for('main.index'))

# ===== Category Routes =====

@bp.route('/categories')
@login_required
def categories():
    """Display all categories"""
    categories_list = Category.query.filter_by(user_id=current_user.id).all()
    form = CategoryForm()
    return render_template('categories.html', categories=categories_list, form=form)

@bp.route('/categories/new', methods=['POST'])
@login_required
def create_category():
    """Create a new category"""
    form = CategoryForm()

    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            color=form.color.data,
            user_id=current_user.id
        )
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')

    return redirect(url_for('main.categories'))

@bp.route('/categories/<int:id>/edit', methods=['POST'])
@login_required
def edit_category(id):
    """Edit an existing category"""
    category = Category.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    name = request.form.get('name')
    color = request.form.get('color')

    if name and color:
        category.name = name
        category.color = color
        db.session.commit()
        flash('Category updated successfully!', 'success')
    else:
        flash('Category name and color are required!', 'danger')

    return redirect(url_for('main.categories'))

@bp.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    """Delete a category"""
    category = Category.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    # Check if category has tasks
    task_count = category.tasks.count()
    if task_count > 0:
        flash(f'Cannot delete category with {task_count} task(s). Please reassign or delete tasks first.', 'warning')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'info')

    return redirect(url_for('main.categories'))

# ===== Error Handlers =====

@bp.app_errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500

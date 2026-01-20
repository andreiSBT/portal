from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

class TaskForm(FlaskForm):
    """Form for creating and editing tasks"""
    title = StringField('Title', validators=[
        DataRequired(message='Title is required'),
        Length(min=1, max=200, message='Title must be between 1 and 200 characters')
    ])

    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=1000, message='Description must be less than 1000 characters')
    ])

    priority = SelectField('Priority', choices=[
        ('1', 'High'),
        ('2', 'Medium'),
        ('3', 'Low')
    ], default='2', coerce=int)

    due_date = DateTimeLocalField('Due Date', validators=[Optional()], format='%Y-%m-%dT%H:%M')

    category = SelectField('Category', coerce=int, validators=[Optional()])

    submit = SubmitField('Save Task')

class CategoryForm(FlaskForm):
    """Form for creating and editing categories"""
    name = StringField('Category Name', validators=[
        DataRequired(message='Category name is required'),
        Length(min=1, max=50, message='Category name must be between 1 and 50 characters')
    ])

    color = StringField('Color', validators=[
        DataRequired(message='Color is required'),
        Regexp(r'^#[0-9A-Fa-f]{6}$', message='Color must be a valid hex code (e.g., #3498db)')
    ], default='#3498db')

    submit = SubmitField('Save Category')

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class NewsForm(FlaskForm):
    """Form for creating and editing news articles"""
    title = StringField('Title', validators=[
        DataRequired(message='Title is required'),
        Length(min=1, max=200, message='Title must be between 1 and 200 characters')
    ])

    summary = StringField('Summary', validators=[
        Optional(),
        Length(max=500, message='Summary must be less than 500 characters')
    ])

    content = TextAreaField('Content', validators=[
        DataRequired(message='Content is required'),
        Length(min=10, message='Content must be at least 10 characters long')
    ])

    image = FileField('Featured Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files are allowed (jpg, jpeg, png, gif)')
    ])

    category = SelectField('Category', coerce=int, validators=[
        DataRequired(message='Please select a category')
    ])

    is_published = BooleanField('Publish Article')
    is_featured = BooleanField('Feature on Home Page')

    submit = SubmitField('Save Article')


class CategoryForm(FlaskForm):
    """Form for creating and editing news categories"""
    name = StringField('Category Name', validators=[
        DataRequired(message='Category name is required'),
        Length(min=1, max=50, message='Category name must be between 1 and 50 characters')
    ])

    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=500, message='Description must be less than 500 characters')
    ])

    color = StringField('Color', validators=[
        DataRequired(message='Color is required'),
        Regexp(r'^#[0-9A-Fa-f]{6}$', message='Color must be a valid hex code (e.g., #3498db)')
    ], default='#3498db')

    submit = SubmitField('Save Category')


class SearchForm(FlaskForm):
    """Form for searching news articles"""
    query = StringField('Search', validators=[
        Optional(),
        Length(max=100, message='Search query must be less than 100 characters')
    ])

    category = SelectField('Category', coerce=int, validators=[Optional()])

    submit = SubmitField('Search')

import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app


def allowed_file(filename):
    """Check if the file extension is allowed"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']


def generate_unique_filename(original_filename):
    """Generate a unique filename using UUID and timestamp"""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}.{ext}"


def validate_image(file_stream):
    """Validate that the file is actually an image"""
    try:
        img = Image.open(file_stream)
        img.verify()
        return True
    except Exception:
        return False


def save_news_image(file, max_width=1200, max_height=800):
    """
    Save and resize news article image

    Args:
        file: FileStorage object from request.files
        max_width: Maximum width for the image
        max_height: Maximum height for the image

    Returns:
        str: Filename of the saved image, or None if save failed
    """
    if not file or file.filename == '':
        return None

    if not allowed_file(file.filename):
        return None

    # Validate it's actually an image
    if not validate_image(file.stream):
        return None

    # Reset stream position after validation
    file.stream.seek(0)

    # Generate unique filename
    filename = generate_unique_filename(file.filename)

    # Determine save path
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'news')
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)

    try:
        # Open and resize image
        img = Image.open(file.stream)

        # Convert RGBA to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background

        # Resize while maintaining aspect ratio
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

        # Save the image
        img.save(filepath, quality=85, optimize=True)

        return filename
    except Exception as e:
        print(f"Error saving image: {e}")
        return None


def delete_news_image(filename):
    """
    Delete a news article image

    Args:
        filename: Name of the file to delete

    Returns:
        bool: True if deleted successfully, False otherwise
    """
    if not filename:
        return False

    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'news')
    filepath = os.path.join(upload_folder, filename)

    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except Exception as e:
        print(f"Error deleting image: {e}")

    return False

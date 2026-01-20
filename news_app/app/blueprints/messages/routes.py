from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.blueprints.messages import messages_bp
from app.models import Message, User
from app.extensions import db
from sqlalchemy import or_


@messages_bp.route('/')
@login_required
def inbox():
    """View inbox - received messages"""
    messages = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.created_at.desc()).all()
    unread_count = Message.query.filter_by(recipient_id=current_user.id, is_read=False).count()

    return render_template('messages/inbox.html',
                         messages=messages,
                         unread_count=unread_count,
                         active_tab='inbox')


@messages_bp.route('/sent')
@login_required
def sent():
    """View sent messages"""
    messages = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()

    return render_template('messages/sent.html',
                         messages=messages,
                         active_tab='sent')


@messages_bp.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
    """Compose a new message"""
    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        subject = request.form.get('subject')
        content = request.form.get('content')

        # Validation
        if not recipient_id or not subject or not content:
            flash('All fields are required.', 'warning')
            return redirect(url_for('messages.compose'))

        recipient = User.query.get(recipient_id)
        if not recipient:
            flash('Recipient not found.', 'danger')
            return redirect(url_for('messages.compose'))

        if recipient.id == current_user.id:
            flash('You cannot send a message to yourself.', 'warning')
            return redirect(url_for('messages.compose'))

        # Create message
        message = Message(
            sender_id=current_user.id,
            recipient_id=recipient_id,
            subject=subject,
            content=content
        )
        db.session.add(message)
        db.session.commit()

        flash(f'Message sent to {recipient.display_name}!', 'success')
        return redirect(url_for('messages.sent'))

    # Get all active users except current user
    users = User.query.filter(User.id != current_user.id, User.is_active == True).order_by(User.username).all()

    # Check if replying to a message
    reply_to_id = request.args.get('reply_to')
    reply_to_message = None
    if reply_to_id:
        reply_to_message = Message.query.get(reply_to_id)

    return render_template('messages/compose.html',
                         users=users,
                         reply_to=reply_to_message,
                         active_tab='compose')


@messages_bp.route('/<int:message_id>')
@login_required
def view(message_id):
    """View a specific message"""
    message = Message.query.get_or_404(message_id)

    # Check if user is sender or recipient
    if message.sender_id != current_user.id and message.recipient_id != current_user.id:
        flash('You do not have permission to view this message.', 'danger')
        return redirect(url_for('messages.inbox'))

    # Mark as read if recipient is viewing
    if message.recipient_id == current_user.id and not message.is_read:
        message.mark_as_read()
        db.session.commit()

    return render_template('messages/view.html',
                         message=message)


@messages_bp.route('/<int:message_id>/delete', methods=['POST'])
@login_required
def delete(message_id):
    """Delete a message"""
    message = Message.query.get_or_404(message_id)

    # Check if user is sender or recipient
    if message.sender_id != current_user.id and message.recipient_id != current_user.id:
        flash('You do not have permission to delete this message.', 'danger')
        return redirect(url_for('messages.inbox'))

    db.session.delete(message)
    db.session.commit()

    flash('Message deleted successfully.', 'info')

    # Redirect based on where the user came from
    if message.sender_id == current_user.id:
        return redirect(url_for('messages.sent'))
    else:
        return redirect(url_for('messages.inbox'))


@messages_bp.route('/mark-all-read', methods=['POST'])
@login_required
def mark_all_read():
    """Mark all messages as read"""
    Message.query.filter_by(recipient_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()

    flash('All messages marked as read.', 'success')
    return redirect(url_for('messages.inbox'))

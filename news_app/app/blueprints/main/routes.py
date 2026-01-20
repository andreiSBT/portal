from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.blueprints.main import main_bp
from app.models import NewsArticle, User, JobApplication
from app.extensions import db
from sqlalchemy import func


@main_bp.route('/')
def index():
    """Landing page - redirects to welcome if logged in"""
    if current_user.is_authenticated:
        return redirect(url_for('main.welcome'))
    return render_template('main/landing.html')


@main_bp.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    """Welcome screen with job selection poll"""

    # Available jobs in Fiascha
    available_jobs = [
        'Policeman', 'Soldier', 'Judge', 'Lawyer', 'Journalist', 'Coach'
    ]

    # Handle job application submission
    if request.method == 'POST':
        selected_job = request.form.get('job')
        message = request.form.get('message', '')

        if selected_job and selected_job in available_jobs:
            # Check if already has 3 approved jobs
            approved_jobs = current_user.get_desired_jobs()
            if len(approved_jobs) >= 3:
                flash('You already have 3 approved jobs. You cannot apply for more.', 'warning')
                return redirect(url_for('main.welcome'))

            # Check if already applied for this job (pending)
            existing_application = JobApplication.query.filter_by(
                user_id=current_user.id,
                job_title=selected_job,
                status='pending'
            ).first()

            if existing_application:
                flash(f'You already have a pending application for {selected_job}.', 'info')
                return redirect(url_for('main.welcome'))

            # Check if already has this job
            if selected_job in approved_jobs:
                flash(f'You already have {selected_job} as an approved job.', 'info')
                return redirect(url_for('main.welcome'))

            # Create new job application
            application = JobApplication(
                user_id=current_user.id,
                job_title=selected_job,
                message=message,
                status='pending'
            )
            db.session.add(application)
            db.session.commit()

            flash(f'Your application for {selected_job} has been submitted to the President for review!', 'success')
            return redirect(url_for('main.welcome'))

    # Get job statistics for poll display
    # Count how many users selected each job
    import json
    all_users = User.query.filter(User.desired_jobs.isnot(None)).all()
    job_counts = {job: 0 for job in available_jobs}

    for user in all_users:
        user_jobs = user.get_desired_jobs()
        for job in user_jobs:
            if job in job_counts:
                job_counts[job] += 1

    total_selections = sum(job_counts.values())
    user_jobs = current_user.get_desired_jobs()

    # Get user's pending applications
    pending_applications = JobApplication.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).all()

    # Get user's recent application history
    recent_applications = JobApplication.query.filter_by(
        user_id=current_user.id
    ).order_by(JobApplication.created_at.desc()).limit(5).all()

    return render_template('main/welcome.html',
                         available_jobs=available_jobs,
                         job_counts=job_counts,
                         total_selections=total_selections,
                         user_jobs=user_jobs,
                         pending_applications=pending_applications,
                         recent_applications=recent_applications)


@main_bp.route('/job-applications')
@login_required
def job_applications():
    """View all job applications (Admin only)"""
    if not current_user.is_admin:
        flash('Only administrators can view job applications.', 'danger')
        return redirect(url_for('main.welcome'))

    # Get pending applications
    pending = JobApplication.query.filter_by(status='pending').order_by(JobApplication.created_at.desc()).all()

    # Get recent reviewed applications
    reviewed = JobApplication.query.filter(
        JobApplication.status.in_(['approved', 'denied'])
    ).order_by(JobApplication.reviewed_at.desc()).limit(20).all()

    pending_count = len(pending)

    return render_template('main/job_applications.html',
                         pending=pending,
                         reviewed=reviewed,
                         pending_count=pending_count)


@main_bp.route('/job-applications/<int:application_id>/approve', methods=['POST'])
@login_required
def approve_application(application_id):
    """Approve a job application (Admin only)"""
    if not current_user.is_admin:
        flash('Only administrators can approve applications.', 'danger')
        return redirect(url_for('main.welcome'))

    application = JobApplication.query.get_or_404(application_id)
    response = request.form.get('response', '')

    application.approve(current_user, response)
    db.session.commit()

    flash(f'Application for {application.job_title} by {application.applicant.display_name} has been approved!', 'success')
    return redirect(url_for('main.job_applications'))


@main_bp.route('/job-applications/<int:application_id>/deny', methods=['POST'])
@login_required
def deny_application(application_id):
    """Deny a job application (Admin only)"""
    if not current_user.is_admin:
        flash('Only administrators can deny applications.', 'danger')
        return redirect(url_for('main.welcome'))

    application = JobApplication.query.get_or_404(application_id)
    response = request.form.get('response', '')

    if not response:
        flash('Please provide a reason for denying the application.', 'warning')
        return redirect(url_for('main.job_applications'))

    application.deny(current_user, response)
    db.session.commit()

    flash(f'Application for {application.job_title} by {application.applicant.display_name} has been denied.', 'info')
    return redirect(url_for('main.job_applications'))

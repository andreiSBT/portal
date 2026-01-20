from flask import render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from app.blueprints.news import news_bp
from app.blueprints.news.forms import NewsForm, CategoryForm, SearchForm
from app.models import NewsArticle, NewsCategory
from app.extensions import db
from app.decorators import admin_required, journalist_required
from app.utils.image_handler import save_news_image, delete_news_image


@news_bp.route('/')
def index():
    """News listing page with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    show_featured = request.args.get('featured', type=int)

    # Base query: only published articles
    query = NewsArticle.query.filter_by(is_published=True)

    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)
    if show_featured:
        query = query.filter_by(is_featured=True)

    # Sort by publish date (newest first)
    query = query.order_by(NewsArticle.publish_date.desc())

    # Paginate
    per_page = current_app.config.get('ARTICLES_PER_PAGE', 12)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    articles = pagination.items
    categories = NewsCategory.query.all()

    return render_template('news/index.html',
                           articles=articles,
                           pagination=pagination,
                           categories=categories,
                           selected_category=category_id,
                           show_featured=show_featured)


@news_bp.route('/article/<slug>')
def article(slug):
    """Single article view"""
    article = NewsArticle.query.filter_by(slug=slug).first_or_404()

    # Only show published articles to non-admin users
    if not article.is_published and (not current_user.is_authenticated or not current_user.is_admin):
        abort(404)

    # Increment view count
    article.increment_views()

    # Get related articles (same category, excluding current)
    related_articles = NewsArticle.query.filter(
        NewsArticle.category_id == article.category_id,
        NewsArticle.id != article.id,
        NewsArticle.is_published == True
    ).order_by(NewsArticle.publish_date.desc()).limit(3).all()

    return render_template('news/article.html',
                           article=article,
                           related_articles=related_articles)


@news_bp.route('/search')
def search():
    """Search news articles"""
    form = SearchForm(request.args)
    query_text = request.args.get('query', '')
    category_id = request.args.get('category', type=int)
    page = request.args.get('page', 1, type=int)

    # Base query
    query = NewsArticle.query.filter_by(is_published=True)

    # Apply search filter
    if query_text:
        search_filter = db.or_(
            NewsArticle.title.ilike(f'%{query_text}%'),
            NewsArticle.content.ilike(f'%{query_text}%'),
            NewsArticle.summary.ilike(f'%{query_text}%')
        )
        query = query.filter(search_filter)

    # Apply category filter
    if category_id:
        query = query.filter_by(category_id=category_id)

    # Sort by relevance (publish date for now)
    query = query.order_by(NewsArticle.publish_date.desc())

    # Paginate
    per_page = current_app.config.get('SEARCH_RESULTS_PER_PAGE', 20)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    articles = pagination.items
    categories = NewsCategory.query.all()

    # Populate form choices
    form.category.choices = [(0, 'All Categories')] + [(c.id, c.name) for c in categories]

    return render_template('news/search.html',
                           form=form,
                           articles=articles,
                           pagination=pagination,
                           query_text=query_text,
                           category_id=category_id)


@news_bp.route('/new', methods=['GET', 'POST'])
@journalist_required
def create():
    """Create new article (journalists and officials only)"""
    form = NewsForm()

    # Populate category choices
    categories = NewsCategory.query.all()
    form.category.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        article = NewsArticle(
            title=form.title.data,
            summary=form.summary.data,
            content=form.content.data,
            is_published=form.is_published.data,
            is_featured=form.is_featured.data,
            category_id=form.category.data,
            author_id=current_user.id
        )

        # Generate slug
        article.generate_slug()

        # Handle image upload
        if form.image.data:
            filename = save_news_image(form.image.data)
            if filename:
                article.image_filename = filename
            else:
                flash('Failed to upload image. Please try again with a different image.', 'warning')

        db.session.add(article)
        db.session.commit()

        flash('Article created successfully!', 'success')
        return redirect(url_for('news.article', slug=article.slug))

    return render_template('news/form.html', form=form, title='Create Article')


@news_bp.route('/edit/<int:article_id>', methods=['GET', 'POST'])
@journalist_required
def edit(article_id):
    """Edit article (journalists and officials only)"""
    article = NewsArticle.query.get_or_404(article_id)
    form = NewsForm()

    # Populate category choices
    categories = NewsCategory.query.all()
    form.category.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        article.title = form.title.data
        article.summary = form.summary.data
        article.content = form.content.data
        article.is_published = form.is_published.data
        article.is_featured = form.is_featured.data
        article.category_id = form.category.data

        # Regenerate slug if title changed
        article.generate_slug()

        # Handle image upload (replace existing)
        if form.image.data:
            # Delete old image if it exists
            if article.image_filename:
                delete_news_image(article.image_filename)

            # Save new image
            filename = save_news_image(form.image.data)
            if filename:
                article.image_filename = filename
            else:
                flash('Failed to upload new image. Keeping the existing image.', 'warning')

        db.session.commit()

        flash('Article updated successfully!', 'success')
        return redirect(url_for('news.article', slug=article.slug))

    elif request.method == 'GET':
        # Pre-populate form with existing data
        form.title.data = article.title
        form.summary.data = article.summary
        form.content.data = article.content
        form.is_published.data = article.is_published
        form.is_featured.data = article.is_featured
        form.category.data = article.category_id

    return render_template('news/form.html', form=form, article=article, title='Edit Article')


@news_bp.route('/delete/<int:article_id>', methods=['POST'])
@journalist_required
def delete(article_id):
    """Delete article (journalists and officials only)"""
    article = NewsArticle.query.get_or_404(article_id)

    # Delete associated image
    if article.image_filename:
        delete_news_image(article.image_filename)

    db.session.delete(article)
    db.session.commit()

    flash('Article deleted successfully.', 'success')
    return redirect(url_for('news.index'))


@news_bp.route('/categories')
@admin_required
def categories():
    """Category management page (admin only)"""
    categories = NewsCategory.query.all()
    return render_template('news/categories.html', categories=categories)


@news_bp.route('/categories/new', methods=['POST'])
@admin_required
def create_category():
    """Create new category (admin only)"""
    form = CategoryForm()

    if form.validate_on_submit():
        category = NewsCategory(
            name=form.name.data,
            description=form.description.data,
            color=form.color.data
        )
        category.generate_slug()

        db.session.add(category)
        db.session.commit()

        flash('Category created successfully!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')

    return redirect(url_for('news.categories'))


@news_bp.route('/categories/edit/<int:category_id>', methods=['POST'])
@admin_required
def edit_category(category_id):
    """Edit category (admin only)"""
    category = NewsCategory.query.get_or_404(category_id)
    form = CategoryForm()

    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        category.color = form.color.data
        category.generate_slug()

        db.session.commit()

        flash('Category updated successfully!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')

    return redirect(url_for('news.categories'))


@news_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@admin_required
def delete_category(category_id):
    """Delete category (admin only)"""
    category = NewsCategory.query.get_or_404(category_id)

    # Check if category has articles
    if category.articles.count() > 0:
        flash('Cannot delete category with existing articles. Please reassign or delete the articles first.', 'danger')
        return redirect(url_for('news.categories'))

    db.session.delete(category)
    db.session.commit()

    flash('Category deleted successfully.', 'success')
    return redirect(url_for('news.categories'))

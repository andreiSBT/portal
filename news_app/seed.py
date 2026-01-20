"""
Database seeding script for News App
Creates sample data including admin user, categories, and news articles
"""
from app import create_app
from app.extensions import db
from app.models import User, NewsCategory, NewsArticle
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    print("Starting database seeding...")

    # Clear existing data
    print("Clearing existing data...")
    NewsArticle.query.delete()
    NewsCategory.query.delete()
    User.query.delete()
    db.session.commit()

    # Create admin user (President of Fiascha)
    print("Creating admin user...")
    admin = User(
        username='admin',
        email='admin@fiascha.com',
        full_name='President Administrator',
        citizen_rank='President',
        is_admin=True,
        is_active=True
    )
    admin.set_password('admin123')  # Change this in production!
    admin.generate_citizen_id()
    db.session.add(admin)
    db.session.commit()
    print(f"[OK] President created (username: admin, password: admin123, ID: {admin.citizen_id})")

    # Create journalist user
    print("Creating journalist user...")
    journalist = User(
        username='journalist',
        email='journalist@fiascha.com',
        full_name='Maria Chen',
        citizen_rank='Journalist',
        is_admin=False,
        is_active=True
    )
    journalist.set_password('journalist123')
    journalist.generate_citizen_id()
    db.session.add(journalist)
    db.session.commit()
    print(f"[OK] Journalist created (username: journalist, password: journalist123, ID: {journalist.citizen_id})")

    # Create regular citizen
    print("Creating regular citizen...")
    citizen = User(
        username='john',
        email='john@fiascha.com',
        full_name='John Smith',
        citizen_rank='Citizen',
        is_admin=False,
        is_active=True
    )
    citizen.set_password('password123')
    citizen.generate_citizen_id()
    db.session.add(citizen)
    db.session.commit()
    print(f"[OK] Citizen created (username: john, password: password123, ID: {citizen.citizen_id})")

    # Create categories
    print("Creating categories...")
    categories = [
        {
            'name': 'Government',
            'description': 'Official government announcements and updates',
            'color': '#3498db'
        },
        {
            'name': 'Culture',
            'description': 'Cultural events and Fiaschan traditions',
            'color': '#9b59b6'
        },
        {
            'name': 'Citizens',
            'description': 'Citizen achievements and community news',
            'color': '#2ecc71'
        },
        {
            'name': 'Development',
            'description': 'Infrastructure and territorial development',
            'color': '#e67e22'
        },
        {
            'name': 'International',
            'description': 'International relations and diplomacy',
            'color': '#1abc9c'
        }
    ]

    category_objects = []
    for cat_data in categories:
        category = NewsCategory(**cat_data)
        category.generate_slug()
        db.session.add(category)
        category_objects.append(category)

    db.session.commit()
    print(f"[OK] Created {len(categories)} categories")

    # Create sample articles
    print("Creating sample articles...")
    articles = [
        {
            'title': 'The Future of Artificial Intelligence in 2026',
            'summary': 'Exploring the latest developments in AI technology and its impact on society.',
            'content': '''
                <p>Artificial Intelligence continues to reshape our world in unprecedented ways. In 2026, we're seeing breakthroughs that were once thought impossible.</p>
                <p>From advanced natural language processing to revolutionary computer vision systems, AI is becoming more integrated into our daily lives than ever before.</p>
                <p>This article explores the key trends and innovations that are defining the AI landscape this year.</p>
            ''',
            'category': category_objects[0],  # Technology
            'is_published': True,
            'is_featured': True
        },
        {
            'title': 'Global Markets Show Strong Recovery',
            'summary': 'Stock markets around the world demonstrate robust growth in the first quarter.',
            'content': '''
                <p>Financial markets are showing remarkable resilience and growth as we move through 2026.</p>
                <p>Major indices have posted significant gains, with technology and green energy sectors leading the charge.</p>
                <p>Analysts are optimistic about continued growth throughout the year.</p>
            ''',
            'category': category_objects[1],  # Business
            'is_published': True,
            'is_featured': True
        },
        {
            'title': 'Championship Finals: A Historic Match',
            'summary': 'The most exciting championship game in decades keeps fans on the edge of their seats.',
            'content': '''
                <p>Last night's championship game will go down in history as one of the most thrilling matches ever played.</p>
                <p>Both teams displayed extraordinary skill and determination, making for an unforgettable sporting event.</p>
                <p>Fans around the world celebrated what many are calling the game of the century.</p>
            ''',
            'category': category_objects[2],  # Sports
            'is_published': True,
            'is_featured': True
        },
        {
            'title': 'New Blockbuster Breaks Box Office Records',
            'summary': 'Latest superhero film surpasses all expectations in opening weekend.',
            'content': '''
                <p>The entertainment industry is buzzing about the latest blockbuster release that shattered box office records.</p>
                <p>With stunning visual effects and a compelling storyline, the film has captivated audiences worldwide.</p>
                <p>Critics and fans alike are praising this cinematic achievement.</p>
            ''',
            'category': category_objects[3],  # Entertainment
            'is_published': True,
            'is_featured': False
        },
        {
            'title': 'Breakthrough in Renewable Energy Storage',
            'summary': 'Scientists develop new battery technology that could revolutionize green energy.',
            'content': '''
                <p>A team of researchers has announced a major breakthrough in energy storage technology.</p>
                <p>The new battery design promises to make renewable energy more viable and cost-effective than ever before.</p>
                <p>This development could be a game-changer in the fight against climate change.</p>
            ''',
            'category': category_objects[4],  # Science
            'is_published': True,
            'is_featured': False
        },
        {
            'title': 'Cybersecurity in the Modern Age',
            'summary': 'Understanding the importance of digital security in our interconnected world.',
            'content': '''
                <p>As our lives become increasingly digital, cybersecurity has never been more critical.</p>
                <p>This comprehensive guide covers the essential practices everyone should follow to stay safe online.</p>
                <p>From password management to recognizing phishing attempts, learn how to protect your digital life.</p>
            ''',
            'category': category_objects[0],  # Technology
            'is_published': True,
            'is_featured': False
        },
        {
            'title': 'Startup Culture: Innovation and Growth',
            'summary': 'Inside the world of tech startups and entrepreneurial success stories.',
            'content': '''
                <p>The startup ecosystem continues to thrive, with innovative companies emerging across various sectors.</p>
                <p>We explore what makes successful startups tick and the challenges entrepreneurs face.</p>
                <p>From funding rounds to scaling operations, learn about the startup journey.</p>
            ''',
            'category': category_objects[1],  # Business
            'is_published': True,
            'is_featured': False
        },
        {
            'title': 'Draft Article: Upcoming Tech Conference',
            'summary': 'Preview of the biggest tech conference of the year (Coming Soon).',
            'content': '''
                <p>This is a draft article about an upcoming technology conference.</p>
                <p>More details will be added as the event approaches.</p>
            ''',
            'category': category_objects[0],  # Technology
            'is_published': False,  # Draft
            'is_featured': False
        }
    ]

    for i, article_data in enumerate(articles):
        article = NewsArticle(
            title=article_data['title'],
            summary=article_data['summary'],
            content=article_data['content'],
            category_id=article_data['category'].id,
            author_id=journalist.id,  # Articles written by journalist
            is_published=article_data['is_published'],
            is_featured=article_data['is_featured'],
            publish_date=datetime.utcnow() - timedelta(days=len(articles) - i),
            views=(i + 1) * 15  # Give some initial views
        )
        article.generate_slug()
        db.session.add(article)

    db.session.commit()
    print(f"[OK] Created {len(articles)} sample articles")

    print("\n" + "="*50)
    print("Database seeding completed successfully!")
    print("="*50)
    print("\nFiascha Citizen Login Credentials:")
    print("-" * 50)
    print("President (Admin):")
    print("  Username: admin")
    print("  Password: admin123")
    print(f"  Citizen ID: {admin.citizen_id}")
    print("\nJournalist:")
    print("  Username: journalist")
    print("  Password: journalist123")
    print(f"  Citizen ID: {journalist.citizen_id}")
    print("\nRegular Citizen:")
    print("  Username: john")
    print("  Password: password123")
    print(f"  Citizen ID: {citizen.citizen_id}")
    print("-" * 50)
    print("\nYou can now run the application with: python run.py")
    print("="*50)

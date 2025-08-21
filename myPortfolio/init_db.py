#!/usr/bin/env python3
"""
Database Initialization Script
This script sets up the database and adds sample data
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.extensions import db
from backend.models import Project, Skill, Contact, Blog, BlogCategory

def init_database():
    """Initialize the database with tables and sample data"""
    print("🚀 Initializing Portfolio Database...")
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            print("📊 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if data already exists
            if Project.query.first() is not None:
                print("ℹ️  Database already contains data. Skipping sample data creation.")
                return
            
            # Create sample data
            print("📝 Adding sample data...")
            
            # Create blog categories
            web_dev = BlogCategory(name="Web Development")
            mobile_dev = BlogCategory(name="Mobile Development")
            data_science = BlogCategory(name="Data Science")
            
            db.session.add_all([web_dev, mobile_dev, data_science])
            db.session.commit()
            
            # Create sample skills
            skills = [
                Skill(name="Python", level="Advanced"),
                Skill(name="JavaScript", level="Intermediate"),
                Skill(name="React", level="Intermediate"),
                Skill(name="Flask", level="Advanced"),
                Skill(name="SQL", level="Intermediate"),
                Skill(name="Git", level="Intermediate"),
            ]
            
            db.session.add_all(skills)
            db.session.commit()
            
            # Create sample projects
            projects = [
                Project(
                    title="Portfolio Website",
                    description="A full-stack portfolio website built with Flask and Bootstrap",
                    tech_stack="Python, Flask, SQLAlchemy, Bootstrap, JavaScript",
                    github_link="https://github.com/Zarifwebme/portfolio",
                    demo_link="https://your-portfolio.railway.app"
                ),
                Project(
                    title="Task Manager App",
                    description="A simple task management application with user authentication",
                    tech_stack="Python, Flask, SQLite, HTML, CSS",
                    github_link="https://github.com/Zarifwebme/task-manager",
                    demo_link="https://task-manager-demo.railway.app"
                ),
                Project(
                    title="Weather Dashboard",
                    description="Real-time weather information dashboard using external APIs",
                    tech_stack="JavaScript, HTML, CSS, Weather API",
                    github_link="https://github.com/Zarifwebme/weather-dashboard",
                    demo_link="https://weather-dashboard.railway.app"
                )
            ]
            
            db.session.add_all(projects)
            db.session.commit()
            
            # Create sample blog posts
            blog_posts = [
                Blog(
                    title="Getting Started with Flask",
                    content="Flask is a lightweight web framework for Python that makes it easy to build web applications...",
                    category=web_dev,
                ),
                Blog(
                    title="Building Responsive UIs with Bootstrap",
                    content="Bootstrap is a powerful CSS framework that helps you create responsive and mobile-first websites...",
                    category=web_dev,
                ),
                Blog(
                    title="Introduction to Data Science",
                    content="Data science is an interdisciplinary field that uses scientific methods to extract insights from data...",
                    category=data_science,
                )
            ]
            
            db.session.add_all(blog_posts)
            db.session.commit()
            
            # Create sample contact
            contact = Contact(
                email="zarif@example.com",
                phone="+998 90 123 45 67",
                linkedin="https://linkedin.com/in/zarifwebme",
                github="https://github.com/Zarifwebme"
            )
            
            db.session.add(contact)
            db.session.commit()
            
            print("✅ Sample data added successfully!")
            print(f"📊 Database contains:")
            print(f"   - {Project.query.count()} projects")
            print(f"   - {Skill.query.count()} skills")
            print(f"   - {Blog.query.count()} blog posts")
            print(f"   - {BlogCategory.query.count()} blog categories")
            print(f"   - {Contact.query.count()} contact entries")
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            db.session.rollback()
            raise
        finally:
            db.session.close()

def check_database():
    """Check database status"""
    print("\n🔍 Checking Database Status...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📋 Found tables: {', '.join(tables)}")
            
            # Check data counts
            if 'project' in tables:
                project_count = Project.query.count()
                print(f"📊 Projects: {project_count}")
            
            if 'skill' in tables:
                skill_count = Skill.query.count()
                print(f"📊 Skills: {skill_count}")
            
            if 'blog' in tables:
                blog_count = Blog.query.count()
                print(f"📊 Blog posts: {blog_count}")
            
            if 'contact' in tables:
                contact_count = Contact.query.count()
                print(f"📊 Contacts: {contact_count}")
                
        except Exception as e:
            print(f"❌ Error checking database: {e}")

if __name__ == "__main__":
    print("🚀 Portfolio Database Setup")
    print("=" * 50)
    
    try:
        init_database()
        check_database()
        print("\n🎉 Database setup completed successfully!")
        print("\n📝 Next steps:")
        print("1. Start your Flask application")
        print("2. Access admin panel at: http://localhost:5000/admin/login")
        print("3. Login with: admin / admin1234")
        print("4. You should now see sample data in the admin panel!")
        
    except Exception as e:
        print(f"\n❌ Database setup failed: {e}")
        print("Please check the error message above and try again.")

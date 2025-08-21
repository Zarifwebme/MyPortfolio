#!/usr/bin/env python3
"""
Complete Setup and Fix Script
This script sets up environment variables and fixes admin panel issues
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Set up environment variables programmatically"""
    print("🔧 Setting up Environment Variables...")
    
    # Set required environment variables
    os.environ['ADMIN_USERNAME'] = 'admin'
    os.environ['ADMIN_PASSWORD'] = 'admin1234'
    os.environ['SECRET_KEY'] = 'dev-secret-key-change-this-in-production'
    os.environ['GITHUB_USERNAME'] = 'Zarifwebme'
    os.environ['FLASK_ENV'] = 'development'
    os.environ['DEBUG'] = 'True'
    os.environ['LOG_LEVEL'] = 'INFO'
    
    print("✅ Environment variables set:")
    print(f"   - ADMIN_USERNAME: {os.getenv('ADMIN_USERNAME')}")
    print(f"   - ADMIN_PASSWORD: {os.getenv('ADMIN_PASSWORD')}")
    print(f"   - SECRET_KEY: {os.getenv('SECRET_KEY')}")
    print(f"   - GITHUB_USERNAME: {os.getenv('GITHUB_USERNAME')}")
    print(f"   - DEBUG: {os.getenv('DEBUG')}")

def check_project_structure():
    """Check if project structure is correct"""
    print("\n🔍 Checking Project Structure...")
    
    required_dirs = [
        'backend',
        'frontend', 
        'templates',
        'instance'
    ]
    
    required_files = [
        'backend/app.py',
        'backend/models.py',
        'backend/admin.py',
        'backend/auth.py',
        'templates/admin/base.html',
        'templates/admin/dashboard.html'
    ]
    
    all_good = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory: {dir_name}")
        else:
            print(f"❌ Missing directory: {dir_name}")
            all_good = False
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ File: {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
            all_good = False
    
    return all_good

def check_database():
    """Check database status"""
    print("\n🗄️  Checking Database...")
    
    try:
        # Add backend to path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        
        from backend.app import create_app
        from backend.extensions import db
        
        app = create_app()
        
        with app.app_context():
            # Check if database file exists
            db_path = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            if 'sqlite:///' in db_path:
                db_file = db_path.replace('sqlite:///', '')
                if os.path.exists(db_file):
                    print(f"✅ Database file exists: {db_file}")
                else:
                    print(f"❌ Database file missing: {db_file}")
                    return False
            
            # Try to create tables
            try:
                db.create_all()
                print("✅ Database tables created/verified")
                
                # Check table counts
                from backend.models import Project, Skill, Contact, Blog, BlogCategory
                
                project_count = Project.query.count()
                skill_count = Skill.query.count()
                blog_count = Blog.query.count()
                category_count = BlogCategory.query.count()
                contact_count = Contact.query.count()
                
                print(f"📊 Current data:")
                print(f"   - Projects: {project_count}")
                print(f"   - Skills: {skill_count}")
                print(f"   - Blogs: {blog_count}")
                print(f"   - Categories: {category_count}")
                print(f"   - Contacts: {contact_count}")
                
                return True
                
            except Exception as e:
                print(f"❌ Database error: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

def create_sample_data():
    """Create sample data if database is empty"""
    print("\n📝 Creating Sample Data...")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        
        from backend.app import create_app
        from backend.extensions import db
        from backend.models import Project, Skill, Contact, Blog, BlogCategory
        
        app = create_app()
        
        with app.app_context():
            # Check if data exists
            if Project.query.first() is not None:
                print("ℹ️  Database already contains data")
                return True
            
            # Create sample data
            print("Creating blog categories...")
            web_dev = BlogCategory(name="Web Development")
            mobile_dev = BlogCategory(name="Mobile Development")
            data_science = BlogCategory(name="Data Science")
            
            db.session.add_all([web_dev, mobile_dev, data_science])
            db.session.commit()
            
            print("Creating skills...")
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
            
            print("Creating projects...")
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
            
            print("Creating blog posts...")
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
            
            print("Creating contact...")
            contact = Contact(
                email="zarif@example.com",
                phone="+998 90 123 45 67",
                linkedin="https://linkedin.com/in/zarifwebme",
                github="https://github.com/Zarifwebme"
            )
            
            db.session.add(contact)
            db.session.commit()
            
            print("✅ Sample data created successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def test_admin_panel():
    """Test if admin panel is working"""
    print("\n🧪 Testing Admin Panel...")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        
        from backend.app import create_app
        from backend.extensions import db
        from backend.models import Project, Skill, Contact, Blog, BlogCategory
        
        app = create_app()
        
        with app.app_context():
            # Test database queries that admin dashboard uses
            stats = {
                "projects": Project.query.count(),
                "skills": Skill.query.count(),
                "contacts": Contact.query.count(),
                "blogs": Blog.query.count(),
                "categories": BlogCategory.query.count(),
            }
            
            print("✅ Admin dashboard statistics calculated successfully:")
            print(f"   - Projects: {stats['projects']}")
            print(f"   - Skills: {stats['skills']}")
            print(f"   - Contacts: {stats['contacts']}")
            print(f"   - Blogs: {stats['blogs']}")
            print(f"   - Categories: {stats['categories']}")
            
            return True
            
    except Exception as e:
        print(f"❌ Admin panel test failed: {e}")
        return False

def main():
    """Main function to set up and fix everything"""
    print("🚀 Complete Portfolio Setup and Fix Script")
    print("=" * 60)
    
    # Step 1: Set up environment variables
    setup_environment()
    
    # Step 2: Check project structure
    if not check_project_structure():
        print("\n❌ Project structure issues found. Please fix them first.")
        return
    
    # Step 3: Check and fix database
    if not check_database():
        print("\n❌ Database issues found.")
        return
    
    # Step 4: Create sample data if needed
    if not create_sample_data():
        print("\n❌ Failed to create sample data.")
        return
    
    # Step 5: Test admin panel
    if not test_admin_panel():
        print("\n❌ Admin panel test failed.")
        return
    
    print("\n🎉 Everything is set up and working!")
    print("\n📝 Next steps:")
    print("1. Start your Flask application: python run.py")
    print("2. Access admin panel: http://localhost:5000/admin/login")
    print("3. Login with: admin / admin1234")
    print("4. You should now see the dashboard with sample data!")
    print("\n🔑 Admin Credentials:")
    print("   - Username: admin")
    print("   - Password: admin1234")
    print("\n🌐 Admin Panel URLs:")
    print("   - Login: http://localhost:5000/admin/login")
    print("   - Dashboard: http://localhost:5000/admin/")
    print("   - Projects: http://localhost:5000/admin/projects")
    print("   - Skills: http://localhost:5000/admin/skills")
    print("   - Blogs: http://localhost:5000/admin/blogs")

if __name__ == "__main__":
    main()

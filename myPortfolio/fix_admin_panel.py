#!/usr/bin/env python3
"""
Admin Panel Fix Script
This script fixes common issues with the admin panel
"""

import os
import sys
from pathlib import Path

def check_project_structure():
    """Check if project structure is correct"""
    print("🔍 Checking Project Structure...")
    
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

def check_environment():
    """Check environment variables"""
    print("\n🔧 Checking Environment Variables...")
    
    required_vars = [
        'ADMIN_USERNAME',
        'ADMIN_PASSWORD',
        'SECRET_KEY'
    ]
    
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var in ['ADMIN_PASSWORD', 'SECRET_KEY']:
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
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

def main():
    """Main function to fix admin panel issues"""
    print("🔧 Admin Panel Fix Script")
    print("=" * 50)
    
    # Check project structure
    if not check_project_structure():
        print("\n❌ Project structure issues found. Please fix them first.")
        return
    
    # Check environment variables
    if not check_environment():
        print("\n❌ Environment variables missing. Please set them first.")
        print("Run: python setup_env.py")
        return
    
    # Check database
    if not check_database():
        print("\n❌ Database issues found.")
        return
    
    # Create sample data if needed
    if not create_sample_data():
        print("\n❌ Failed to create sample data.")
        return
    
    print("\n🎉 Admin panel should now work!")
    print("\n📝 Next steps:")
    print("1. Start your Flask application: python run.py")
    print("2. Access admin panel: http://localhost:5000/admin/login")
    print("3. Login with: admin / admin1234")
    print("4. You should now see the dashboard with sample data!")

if __name__ == "__main__":
    main()

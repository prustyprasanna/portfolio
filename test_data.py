from django.core.files import File
from pathlib import Path
from myportfolio.models import Register, Intro
import os
import random

def create_test_data():
    """Create test user and portfolio data"""
    try:
        # Generate unique email
        random_id = random.randint(1000, 9999)
        email = f"test{random_id}@example.com"
        
        # Delete existing test user if exists
        Register.objects.filter(email=email).delete()
        
        # Create new test user
        user = Register.objects.create(
            name=f"Test User {random_id}",
            email=email,
            password="testpass123"
        )
        print(f"Created test user: {user}")

        # Create portfolio data
        base_dir = Path(__file__).resolve().parent
        test_img_path = base_dir / 'test_files' / 'test_profile.jpg'
        test_pdf_path = base_dir / 'test_files' / 'test_resume.pdf'

        # Ensure test files exist
        if not test_img_path.exists() or not test_pdf_path.exists():
            print("Creating test files...")
            test_files_dir = base_dir / 'test_files'
            test_files_dir.mkdir(exist_ok=True)
            
            # Create dummy image if doesn't exist
            if not test_img_path.exists():
                with open(test_img_path, 'wb') as f:
                    f.write(b'dummy image data')
            
            # Create dummy PDF if doesn't exist
            if not test_pdf_path.exists():
                with open(test_pdf_path, 'wb') as f:
                    f.write(b'dummy PDF data')

        # Create portfolio
        with open(test_img_path, 'rb') as img_file, open(test_pdf_path, 'rb') as pdf_file:
            portfolio = Intro.objects.create(
                user=user,
                full_name=f"Test Full Name {random_id}",
                tagline="Python Developer & AI Enthusiast",
                about_me="Experienced developer with 5 years in web development...",
                location="New York, USA",
                email=email,
                phone="+1234567890",
                profile_picture=File(img_file, name='profile.jpg'),
                resume=File(pdf_file, name='resume.pdf'),
                linkedin=f"https://linkedin.com/in/testuser{random_id}",
                github=f"https://github.com/testuser{random_id}",
                twitter=f"https://twitter.com/testuser{random_id}",
                website=f"https://testuser{random_id}.dev"
            )
            print(f"Created portfolio: {portfolio}")

        return user, portfolio

    except Exception as e:
        print(f"Error creating test data: {str(e)}")
        return None, None

def verify_data(user, portfolio):
    """Verify the created test data"""
    try:
        verify_portfolio = Intro.objects.get(user=user)
        print("\nVerification Results:")
        print(f"User: {verify_portfolio.user.name}")
        print(f"Email: {verify_portfolio.user.email}")
        print(f"Full Name: {verify_portfolio.full_name}")
        print(f"Tagline: {verify_portfolio.tagline}")
        print(f"Location: {verify_portfolio.location}")
        print(f"Profile Picture: {verify_portfolio.profile_picture}")
        print(f"Resume: {verify_portfolio.resume}")
        
        # Check all portfolios
        all_portfolios = Intro.objects.all()
        print(f"\nTotal portfolios: {all_portfolios.count()}")
        for p in all_portfolios:
            print(f"Portfolio: {p.full_name} - {p.tagline}")
        
        return True
    except Exception as e:
        print(f"Verification failed: {str(e)}")
        return False

def run_tests():
    """Run all tests"""
    user, portfolio = create_test_data()
    if user and portfolio:
        return verify_data(user, portfolio)
    return False

# Run this in Django shell:
# python manage.py shell
# >>> from test_data import create_test_data
# >>> user, portfolio = create_test_data()
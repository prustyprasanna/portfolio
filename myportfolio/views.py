from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.urls import reverse
from datetime import datetime
import json
import uuid
import base64
import logging

from .models import Register, Intro, Company, Skill, SkillAssessment
from .forms import IntroForm
from .mock_data import mockDevelopers, mockCompanies

# Configure logging
logger = logging.getLogger(__name__)

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # For debugging - print values
        print(f"Received registration data: Username={username}, Email={email}")
        
        # Check if email already exists
        if Register.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'register.html')
        
        if password1 == password2:
            try:
                user = Register.objects.create(
                    name=username,
                    email=email,
                    password=password1
                )
                # Store user ID in session after registration
                request.session['user_id'] = user.pk  # Changed from id to pk
                
                # Get the saved values
                saved_user = Register.objects.get(pk=user.pk)  # Changed from id to pk
                print(f"Saved user data: Name={saved_user.name}, Email={saved_user.email}")
                
                messages.success(request, 'Registration successful!')
                return redirect('intro_view')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:   
            messages.error(request, 'Passwords do not match!')
    
    return render(request, 'register.html')

def user_profile(request):
    # Get user_id from session
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, 'Please login first')
        return redirect('myportfolio:login')
    
    user = get_object_or_404(Register, pk=user_id)
    try:
        intro = Intro.objects.get(user=user)
    except Intro.DoesNotExist:
        intro = None
    
    context = {
        'user': user,
        'intro': intro
    }
    return render(request, 'user_profile.html', context)

def portfolio_view(request, user_id):
    user = get_object_or_404(Register, id=user_id)
    try:
        intro = Intro.objects.get(user=user)
        
        # Get all portfolio values
        portfolio_data = {
            'user_info': {
                'name': user.name,
                'email': user.email
            },
            'portfolio_info': {
                'full_name': intro.full_name,
                'tagline': intro.tagline,
                'about_me': intro.about_me,
                'location': intro.location,
                'email': intro.email,
                'phone': intro.phone,
                'linkedin': intro.linkedin,
                'github': intro.github,
                'twitter': intro.twitter,
                'website': intro.website
            }
        }
        
        # Print portfolio data for debugging
        print("Portfolio Data:", portfolio_data)
        
        context = {
            'user': user,
            'intro': intro,
            'portfolio_data': portfolio_data
        }
        return render(request, 'portfolio_display.html', context)
    except Intro.DoesNotExist:
        messages.error(request, 'Portfolio not found')
        return redirect('intro_view')

# def intro_view(request):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Please login first')
        return redirect('myportfolio:login')

    try:
        user = Register.objects.get(pk=user_id)  # Changed from id to pk
    except Register.DoesNotExist:
        messages.error(request, 'User not found')
        return redirect('myportfolio:login')

    # Check if intro already exists
    intro = Intro.objects.filter(user=user).first()
    
    if request.method == 'POST':
        form = IntroForm(request.POST, request.FILES, instance=intro)
        if form.is_valid():
            try:
                intro = form.save(commit=False)
                intro.user = user
                intro.save()
                messages.success(request, 'Portfolio information saved successfully!')
                return redirect('portfolio_view', user_id=user.pk)
            except Exception as e:
                messages.error(request, f'Error saving portfolio: {str(e)}')
    else:
        form = IntroForm(instance=intro)
    
    return render(request, 'intro.html', {'form': form})

def login_view(request):  # Changed from login to login_view
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = Register.objects.get(name=username, password=password)
            request.session['user_id'] = user.pk
            messages.success(request, 'Login successful!')
            return redirect('myportfolio:intro')  # Add namespace
        except Register.DoesNotExist:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def home_view(request):
    try:
        # Get all portfolios with their related user data
        portfolios = Intro.objects.select_related('user').all()
        
        # For debugging
        print(f"Found {portfolios.count()} portfolios")
        for portfolio in portfolios:
            user_name = portfolio.user.name if portfolio.user else "Unknown"
            print(f"Portfolio: {portfolio.full_name}, User: {user_name}")
            
        context = {
            'portfolios': portfolios
        }
    except Exception as e:
        print(f"Error fetching portfolios: {str(e)}")
        context = {
            'portfolios': []
        }
    
    return render(request, 'index.html', context)


def company_login(request):
    return render(request, 'company_login.html')

def company_register(request):
    if request.method == 'POST':
        try:
            # Get form data
            company_data = {
                'company_name': request.POST.get('company_name'),
                'company_email': request.POST.get('company_email'),
                'industry': request.POST.get('industry'),
                'company_size': request.POST.get('company_size'),
                'password': request.POST.get('password')
            }

            # Create and save company
            company = Company.objects.create(**company_data)
            
            # Log success
            print(f"Company created: {company.company_name}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Company registered successfully'
            })
            
        except Exception as e:
            print(f"Error creating company: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'error': str(e)
            }, status=400)

    return render(request, 'company_register.html')

def portfolio_detail(request, developer_id):
    # Get mock data from your Python mock_data module
    from .mock_data import mockDevelopers
    
    developer = next((dev for dev in mockDevelopers if dev['id'] == developer_id), None)
    if not developer:
        raise Http404("Developer not found")
    
    return render(request, 'portfolio_detail.html', {
        'developer': developer
    })

def pricing_view(request):
    return render(request, 'pricing.html', {
        'companies': mockCompanies
    })

def companies_view(request):
    return render(request, 'companies.html', {
        'companies': mockCompanies
    })

def developers_view(request):
    return render(request, 'developers.html', {
        'developers': mockDevelopers
    })

def company_post(request):
    if request.method == 'POST':
        # Get project ID from form data
        project_id = request.POST.get('project_id')
        
        # Get technologies
        technologies = request.POST.get('technologies', '[]')
        try:
            tech_list = json.loads(technologies)
        except json.JSONDecodeError:
            tech_list = []

        project_data = {
            'id': project_id or str(uuid.uuid4()),  # Use existing ID or generate new one
            'title': request.POST.get('project_title'),
            'description': request.POST.get('project_description'),
            'min_budget': request.POST.get('min_budget'),
            'max_budget': request.POST.get('max_budget'),
            'project_type': request.POST.get('project_type'),
            'experience_level': request.POST.get('experience_level'),
            'remote_work': request.POST.get('remote_work') == 'on',
            'technologies': tech_list,
            'created_at': request.POST.get('created_at') or datetime.now().strftime('%Y-%m-%d')
        }

        # Handle logo upload
        if request.FILES.get('project_logo'):
            try:
                file = request.FILES['project_logo']
                file_data = base64.b64encode(file.read()).decode('utf-8')
                project_data['logo'] = {
                    'data': file_data,
                    'name': file.name,
                    'type': file.content_type
                }
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error processing logo: {str(e)}'
                }, status=400)

        # Get existing projects from session
        posted_projects = request.session.get('posted_projects', [])

        # If editing, update existing project
        if project_id:
            for i, project in enumerate(posted_projects):
                if str(project.get('id')) == str(project_id):
                    # Preserve logo if not uploading new one
                    if not request.FILES.get('project_logo') and 'logo' in project:
                        project_data['logo'] = project['logo']
                    posted_projects[i] = project_data
                    break
        else:
            # New project
            posted_projects.append(project_data)

        # Update session
        request.session['posted_projects'] = posted_projects
        request.session.modified = True

        return JsonResponse({
            'status': 'success',
            'message': 'Project updated successfully!' if project_id else 'Project posted successfully!',
            'redirect_url': request.build_absolute_uri(reverse('myportfolio:company_profile'))
        })

    return render(request, 'company_post.html')

def company_profile(request):
    # Get company data from session
    company = {
        'name': request.session.get('company_name', 'Tech Company'),
        'logo': request.session.get('company_logo', 'path/to/logo.png'),
        'location': request.session.get('company_location', 'San Francisco, CA'),
        'industry': request.session.get('company_industry', 'Software Development'),
        'size': request.session.get('company_size', '50-100 employees')
    }
    
    # Get projects from session
    projects = request.session.get('posted_projects', [])
    
    return render(request, 'company_profile.html', {
        'company': company,
        'projects': projects
    })

@csrf_exempt  # Only for development, remove in production
@require_POST
def delete_project(request, project_id):
    if not project_id:
        return JsonResponse({
            'status': 'error',
            'message': 'Project ID is required'
        }, status=400)

    try:
        # Get projects from session
        posted_projects = request.session.get('posted_projects', [])
        
        # Print for debugging
        print(f"Trying to delete project {project_id}")
        print(f"Current projects: {[p.get('id') for p in posted_projects]}")
        
        project_index = next((index for (index, project) in enumerate(posted_projects) 
                            if str(project.get('id')) == str(project_id)), None)
        
        if project_index is not None:
            # Remove the project
            deleted_project = posted_projects.pop(project_index)
            # Update session
            request.session['posted_projects'] = posted_projects
            request.session.modified = True
            
            print(f"Successfully deleted project {deleted_project.get('title')}")
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'Project with ID {project_id} not found'
            }, status=404)
            
    except Exception as e:
        print(f"Error deleting project: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@ensure_csrf_cookie
def intro(request):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                messages.error(request, 'Please login first')
                return redirect('myportfolio:login')

            user = Register.objects.get(pk=user_id)
            
            # Get existing portfolio or None
            try:
                portfolio = Intro.objects.get(user=user)
            except Intro.DoesNotExist:
                portfolio = None

            form = IntroForm(request.POST, request.FILES, instance=portfolio)
            
            print("POST data:", request.POST)
            print("FILES:", request.FILES)

            if form.is_valid():
                portfolio = form.save(commit=False)
                portfolio.user = user
                portfolio.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Portfolio saved successfully!',
                        'redirect_url': reverse('myportfolio:portfolio_view', kwargs={'user_id': user.pk})
                    })
                
                messages.success(request, 'Portfolio saved successfully!')
                return redirect('myportfolio:portfolio_view', user_id=user.pk)
            else:
                print("Form errors:", form.errors)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'errors': form.errors
                    }, status=400)
                
                messages.error(request, 'Please correct the errors below.')
                return render(request, 'intro.html', {'form': form})
                
        except Exception as e:
            print("Error:", str(e))
            messages.error(request, f'Error saving portfolio: {str(e)}')
            return render(request, 'intro.html', {'form': IntroForm()})

    # GET request
    try:
        user_id = request.session.get('user_id')
        if user_id:
            user = Register.objects.get(pk=user_id)
            portfolio = Intro.objects.filter(user=user).first()
            form = IntroForm(instance=portfolio)
        else:
            form = IntroForm()
    except Exception as e:
        print("Error loading form:", str(e))
        form = IntroForm()
    
    return render(request, 'intro.html', {'form': form})

def about_view(request):
    return render(request, 'about.html')

def community_view(request):
    return render(request, 'community.html')

def skills_assessment_view(request):
    if not request.user.is_authenticated:
        return redirect('myportfolio:login')
        
    if request.method == 'POST':
        skill_id = request.POST.get('skill_id')
        score = request.POST.get('score')
        
        if skill_id and score:
            SkillAssessment.objects.create(
                user=request.user,
                skill_id=skill_id,
                score=score
            )
            messages.success(request, 'Assessment completed!')
            
    skills = Skill.objects.all()
    completed_assessments = SkillAssessment.objects.filter(user=request.user)
    
    return render(request, 'skills_assessment.html', {
        'skills': skills,
        'completed_assessments': completed_assessments
    })

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Add your contact form processing logic here
        # For now, just show a success message
        messages.success(request, 'Thank you for your message. We will get back to you soon!')
        return redirect('myportfolio:contact')
        
    return render(request, 'contact.html')
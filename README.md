# DevConnect Portfolio Platform

DevConnect is a modern Django-based platform that connects top developers with innovative companies. It features developer and company directories, job listings, portfolio creation, skill assessments, and more—all with a clean, responsive UI.

---

## Features

- **User Authentication**: Secure registration and login for developers and companies.
- **Developer Directory**: Browse and view individual developer profiles.
- **Company Directory**: Browse companies and view detailed company profiles.
- **Job Listings**: Explore open positions and apply directly.
- **Portfolio Creation**: Developers can create and showcase their portfolios.
- **Skill Assessment**: Take and display skill assessments.
- **Community**: Access developer community resources and events.
- **Contact Form**: Reach out to the DevConnect team.
- **Responsive Design**: Works seamlessly on desktop and mobile.
- **Dark Theme**: Consistent, modern dark UI.

---

## Project Structure

```
portfolio/
├── myportfolio/         # Main Django app (views, models, urls)
├── static/              # Static files (css, js, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── companies.html
│   ├── developers.html
│   ├── contact.html
│   ├── skills_assessment.html
│   └── components/
├── manage.py
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Django 4.x
- pip

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/portfolio.git
    cd portfolio
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On Mac/Linux:
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Collect static files:**
    ```bash
    python manage.py collectstatic --noinput
    ```

6. **Create a superuser (optional, for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

8. **Visit the app:**
    - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Usage

- **Home:** Overview and navigation.
- **Developers:** Browse developer directory and profiles.
- **Companies:** Browse companies and view profiles.
- **Jobs:** View and apply for jobs.
- **Portfolio:** Developers can create and manage their portfolios.
- **Skills Assessment:** Take and view skill assessments.
- **Community:** Access forums, events, and resources.
- **Contact:** Send messages to the DevConnect team.

---

## Customization

- **Styling:** Edit files in `static/css/` for custom styles.
- **Templates:** Modify HTML in `templates/` for layout/content changes.
- **Models/Views:** Extend functionality in `myportfolio/models.py` and `myportfolio/views.py`.

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or support, please use the [Contact Us](http://127.0.0.1:8000/contact/) page in the app.

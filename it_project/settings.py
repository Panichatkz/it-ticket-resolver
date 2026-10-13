import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-offline-secure-mvt-mimo-development-key-token-spec'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Mount our custom app containing the global system cache loader configuration
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'ticketing_app.apps.TicketingAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'it_project.urls'

# Path rules maps where Django locates our HTML View Template Presentation assets
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'ticketing_app', 'templates')],
        'APP_DIRS': True,
    },
]

WSGI_APPLICATION = 'it_project.wsgi.application'

# INDUSTRY STANDARD: Native driver connection string variables mapping straight to local MongoDB
MONGODB_URI = "mongodb://127.0.0.1:27017/"
MONGODB_NAME = "enterprise_it_service_desk"

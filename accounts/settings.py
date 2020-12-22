import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = os.path.join(BASE_DIR, 'accounts/static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "accounts/static")]


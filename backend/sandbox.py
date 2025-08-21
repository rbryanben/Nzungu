from dotenv import load_dotenv
load_dotenv()

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()


from datetime import timedelta, datetime

from shared_models.models import ProductSale
from api.models import User

# 1 week ago 
fromDate = datetime.fromisoformat('2025-08-01')
user = User.getUserByUsername('rben')

ProductSale.getTellerSales(user,fromDate)
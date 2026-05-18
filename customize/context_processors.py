from datetime import datetime
from django.http import HttpRequest


def global_data(request: HttpRequest):
    """Global data"""
    return {
        "site_name": "My Django Shop",
        "current_year": datetime.now().year
    }
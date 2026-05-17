from datetime import datetime


def global_data(request):
    return {
        "site_name": "My Django Shop",
        "current_year": datetime.now().year
    }
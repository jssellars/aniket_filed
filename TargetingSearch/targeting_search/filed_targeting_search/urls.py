"""filed_targeting_search URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

from interest import views as interest_views
from language import views as language_views
from location import views as location_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'favicon\.ico', RedirectView.as_view(
        url='/static/favicon/favicon.ico')),
    path('languages', language_views.get_all),
    path('languages/match', language_views.match_languages),
    path('languages/update', language_views.update_languages),
    path('locations', location_views.get_all),
    path('locations/countries', location_views.get_countries),
    path('locations/country-groups', location_views.get_country_groups),
    path('locations/regions', location_views.get_regions),
    path('locations/geomarkets', location_views.get_geo_markets),
    path('locations/electoral-districts', location_views.get_electoral_districts),
    path('locations/match', location_views.match_locations),
    path('locations/update', location_views.update_locations),
    path('locations/update-country-groups', location_views.update_country_groups),
    path('locations/search/<str:query_string>', location_views.search_location),
    path('interests', interest_views.get_all),
    path('interests/<str: interest_key>', interest_views.get_interest_by_key),
    path('interests/search/<str:query>', interest_views.search_interest),
    path('interests/suggestions/<str:interests>', interest_views.suggest_interests),
    path('interests/update', interest_views.update_interests),
    path('interests/match', interest_views.match_interests),
    path('interests/tree', interest_views.get_interests_tree),
    path('interests/estimated-size', interest_views.get_estimated_audience_size)
]

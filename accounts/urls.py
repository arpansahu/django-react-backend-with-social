from django.urls import path
from .views import CustomUserCreate, AccountDetails

app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('account/', AccountDetails.as_view(), name="my_account")
]
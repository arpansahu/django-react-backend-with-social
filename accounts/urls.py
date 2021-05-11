from django.urls import path
from .views import CustomUserCreate, AccountDetails, ChangePasswordView, UpdateProfileView

app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('account/', AccountDetails.as_view(), name="my_account"),
    path('account/passwordchange/<int:pk>/', ChangePasswordView.as_view(),  name='auth_change_password'),
    path('account/update/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
]
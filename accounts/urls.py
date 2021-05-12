from django.urls import path
from .views import CustomUserCreate, AccountDetails, ChangePasswordView, UpdateProfileView, AccountActivateView, \
    ForgetPasswordView, ResetPasswordView

app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('account/', AccountDetails.as_view(), name="my_account"),
    path('account/passwordchange/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('account/update/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('account/activate/', AccountActivateView.as_view(), name='account_activate'),
    path('account/forgetpaassword/', ForgetPasswordView.as_view(), name='forget_password'),
    path('account/resetpassword/', ResetPasswordView.as_view(), name='reset_password')
]

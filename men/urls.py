from django.urls import path

from .views import *


urlpatterns = [
    path('', MenHome.as_view(), name='home'),
    path('tag/<slug:tag_slug>/', MenHome.as_view(), name='post_list_by_tag'), # tag/jyp/
    path('search/', SearchResult.as_view(), name='search'),
    path('add_page/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),

    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('profile/<int:user_pk>/update', UpdateUserProfile.as_view(), name='update_user_profile'),
    path('profile/<int:user_pk>/', UserProfile.as_view(), name='user_profile'),
    
    path('post/<slug:post_slug>', post_detail, name='post'),
    path('post/<slug:post_slug>/comment/', post_comment, name='post_comment'),
    path('category/<slug:cat_slug>', MenCategory.as_view(), name='category'),
    path('404/', PageNotFound.as_view(), name='404'),
    ]

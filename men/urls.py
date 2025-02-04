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
    path('post/<slug:post_slug>', post_detail, name='post'),
    path('post/<slug:post_slug>/comment/', post_comment, name='post_comment'),
    path('category/<slug:cat_slug>', MenCategory.as_view(), name='category'),
    path('404/', PageNotFound.as_view(), name='404'),
    ]

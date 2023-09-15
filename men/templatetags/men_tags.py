from django import template
# from django.http import Http404

from men.models import *

# register = template.Library() # регистрация собственных тегов
#
# @register.simple_tag(name='getcats')
# def get_categories(filter=None):
#     if not filter:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=filter)
#
#
# @register.inclusion_tag('men/list_categories.html')
# def show_categories(sort=None, cat_selected=0):
#     if not sort:
#         cats = Category.objects.all()
#     else:
#         cats = Category.objects.order_by(sort)
#     return {'cats': cats, 'cat_selected': cat_selected}
#
#
# @register.simple_tag() # по идеи лишний тег, но у меня он сейчас задействован
# def get_posts(cat_selected=None):
#     if not cat_selected:
#         return Men.objects.all()
#     else:
#         posts = Men.objects.filter(cat__slug=cat_selected)
#         print(posts)
#         if len(posts) == 0:
#             raise Http404()
#         else:
#             return posts





# from django import template
# from urllib.parse import urlencode
#
#
# register = template.Library()
#
# @register.simple_tag
# def url_replace (request, field, value):
#     dict_ = request.GET.copy()
#     dict_[field] = value
#
#     return dict_.urlencode()
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView, UpdateView
from django.views.decorators.http import require_POST

from taggit.models import Tag

from men.forms import *
from men.utils import *


class PageNotFound(DataMixin, TemplateView):
    template_name = 'men/404.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 303  # не уверена, что 303 - верный код
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Страница не найдена',)
        return context | c_def


class MenHome(DataMixin, ListView):
    model = Men
    template_name = 'men/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        post_list = Men.published.select_related('cat')
        if self.kwargs:
            tag = self.kwargs['tag_slug']
            tag = get_object_or_404(Tag, slug=tag)
            post_list = post_list.filter(tags__in=[tag])
        return post_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница',
                                      cat_selected=0)
        return context | c_def


class MenCategory(DataMixin, ListView):
    model = Men
    template_name = 'men/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Men.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])  # получает из браузера выбр.категорию и находит ее в БД
        c_def = self.get_user_context(title=str(c.name),
                                      cat_selected=c.pk)  # получает данные из ДатаМиксин и добавляет им еще
        return context | c_def


def post_detail(request, post_slug):
    """Отображение статьи и формы комментария (GET)"""
        
    post = get_object_or_404(Men, is_published=True, slug=post_slug)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    # 4 похожих поста: чем больше общих тегов, тем выше в рекомендациях
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Men.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-time_create')[:4]

    context = get_user_context(request=request, 
                               post=post,
                               comments=comments,
                               form=form,
                               similar_posts=similar_posts
        )

    return render(
        request=request,
        template_name='men/post.html',
        context=context
        )
    

@require_POST
def post_comment(request, post_slug):
    """Обработка формы комментария (POST)."""

    post = get_object_or_404(klass=Men, is_published=True, slug=post_slug)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    
    return redirect('post', post_slug=post_slug)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'men/addpage.html'
    success_url = reverse_lazy('home')
    login_url = '/admin/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return context | c_def
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Статья успешно добавлена.')
        return super().form_valid(form)


class SearchResult(DataMixin, ListView):
    model = Men
    template_name = 'men/search.html'
    context_object_name = 'posts'
    query = None

    def get_queryset(self):
        self.query = self.request.GET.get('q', '') 
        search_result = Men.published.annotate(search=SearchVector('title', 'content'),).filter(search=self.query)
        return search_result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Результаты поиска')
        context['query'] = self.query
        return context | c_def


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'men/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return context | c_def

    def form_valid(self, form):
        messages.success(self.request, 'Спасибо за обратную связь!')
        return redirect('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context | c_def

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        messages.success(self.request, 'Вы успешно зарегистрировались.')
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class UserProfile(DataMixin, DetailView):
    template_name = 'registration/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        user_pk = User.objects.filter(pk=self.kwargs['user_pk'])[0].pk
        profile = Profile.objects.filter(user_id=user_pk).select_related('user').get()
        return profile
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=self.get_object().user.username)
        return context | c_def


class UpdateUserProfile(DataMixin, UpdateView):
    template_name = 'registration/profile_update.html'
    context_object_name = 'user_profile'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('home')

    def get_object(self):
        user_pk = User.objects.filter(pk=self.kwargs['user_pk'])[0].pk
        profile = Profile.objects.filter(user_id=user_pk).select_related('user').get()
        return profile

    def get_context_data(self, **kwargs):
        context = super(UpdateUserProfile, self).get_context_data(**kwargs)
        user = self.request.user
        context['profile_form'] = ProfileUpdateForm(
            instance=self.request.user.profile,
            initial={'first_name': user.first_name, 
                     'last_name': user.last_name}
            )
        c_def = self.get_user_context(title=self.get_object().user.username)
        return context | c_def

    def form_valid(self, form):
        profile = form.save()
        user = profile.user
        user.last_name = form.cleaned_data['last_name']
        user.first_name = form.cleaned_data['first_name']
        user.save()
        messages.success(self.request, 'Профиль успешно изменен.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Возникла ошибка при редактировании профиля.')
        return self.render_to_response(self.get_context_data(form=form))

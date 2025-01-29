# TODO:
# -тесты моделей Men, Category на CRUD
# --создать объект Men, получить его и его атрибуты: title, content, cat (cat exist in db?)
# --Men.title, content изменить
# --удалить Men
# --создать Category, создать ему 2 поста
# --получить всю категорию
# --изменить название категории, получить ее и один пост
# --удалить категорию




from django.test import TestCase, Client

from men.models import *



class AuthorModelTest(TestCase):
@classmethod
def setUpTestData(cls):
    # Set up non-modified objects used by all test methods
    Author.objects.create(first_name='Big', last_name='Bob')

def test_first_name_label(self):
    author = Author.objects.get(id=1)
    field_label = author._meta.get_field('first_name').verbose_name  # поля почему-то можно только через _meta получить
    self.assertEqual(field_label, 'first name')

def test_first_name_max_length(self):
    author = Author.objects.get(id=1)
    max_length = author._meta.get_field('first_name').max_length
    self.assertEqual(max_length, 100)

def test_get_absolute_url(self):
    author = Author.objects.get(id=1)
    # This will also fail if the urlconf is not defined.
    self.assertEqual(author.get_absolute_url(), '/catalog/author/1')



class MenModelTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name='Певцы')

        User.objects.create(username='Админ',
                            email='admin@test.com',
                            password='Ololo965',
                            is_staff=True,
                            is_active=True)

        Men.objects.create(title='Ли Ёнбок',
                            content='Ли Ёнбок (англ. Lee Yong-bok, кор. 이용복), при рождении — Феликс Ли (англ. Felix Lee; род. 15 сентября 2000 года,— южнокорейский и австралийский певец, рэпер, ведущий танцор, композитор и автор песен.',
                            is_published=True,
                            cat_id=1,
                            user_id=1)

    # def test_post_title_max_length(self):
    #     post = Men.objects.get(pk=1)
    #     max_length = post._meta.get_field('title').max_length
    #     self.assertEqual(max_length, 255)

    def test_category_name(self):
        cat = Category.objects.get(id=1)
        self.assertEqual(cat.name, 'Певцы')

    def test_category_name_max_length(self):
        cat = Category.objects.get(id=1)
        self.assertEqual(cat._meta.get_field('name').max_length, 100)

    def test_get_title(self):
        title = Men.objects.get(pk=1).title
        self.assertEqual(title, 'Ли Ёнбок')

    def test_get_content(self):
        content = Men.objects.get(pk=1).content
        self.assertTrue(content)

    def test_update_title(self):
        pass

    def test_update_content(self):
        pass

    def test_time_created(self):
        pass


class CategoryModelTestCase(TestCase):
    pass





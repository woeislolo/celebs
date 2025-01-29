# -тесты views HTTP
# --Client

from django.test import TestCase, Client

from men.views import *

# views Django
class MenHomeViewTest(TestCase):
    c = Client()
    response = c.get("", {"username": "john", "password": "smith"})
    Men.objects.filter(is_published=True).select_related('cat')
    
    response.status_code

    response = c.get("/customer/details/")
    response.content


# views API
class MenAPIListViewTest(APITestCase):
    def setUp(self):
        Category.objects.create(name='Певцы')
        Category.objects.create(name='Актеры')

        self.admin = User.objects.create(username='Admin',
                                        email='admin@test.com',
                                        password='Ololo965',
                                        is_staff=True,
                                        is_active=True)
        self.user = User.objects.create(username='User',
                                        email='user@test.com',
                                        password='Ololo965',
                                        is_staff=False,
                                        is_active=True)

        for i in range(4):
            Men.objects.create(title=f'Ли Ёнбок {i}',
                              content='Южнокорейский и австралийский певец, рэпер, ведущий танцор, композитор и автор песен.',
                              is_published=True,
                              cat_id=1 if (i % 2) else 2,
                              user_id=1 if (i % 2) else 2)

    def tearDown(self):
        self.client.force_authenticate(user=None)
        # self.client.logout()

    def test_get_all_posts_by_unauthorised_user(self):
        url = reverse('post_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_posts_by_authorised_user(self):
        url = reverse('post_list')
        self.client.force_authenticate(self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_posts_by_admin(self):
        url = reverse('post_list')
        self.client.force_authenticate(self.admin)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_by_unauthorised_user(self):
        url = reverse('post_list')
        data = {'title': 'Пост Неавторизованного', 'content': 'Совсем другой текст', 'cat': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_by_authorised_user(self):
        url = reverse('post_list')
        self.client.force_authenticate(self.user)
        data = {'title': 'Пост Авторизованного', 'content': 'Совсем другой текст', 'cat': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], 'Пост Авторизованного')

    def test_create_post_by_admin(self):
        url = reverse('post_list')
        self.client.force_authenticate(self.admin)
        data = {'title': 'Пост Админа', 'content': 'Совсем другой текст', 'cat': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], 'Пост Админа')

    def test_create_post_without_title_by_admin(self):
        url = reverse('post_list')
        self.client.force_authenticate(self.admin)
        data = {'title': '', 'content': 'Контент', 'cat': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_without_content_by_admin(self):
        url = reverse('post_list')
        self.client.force_authenticate(self.admin)
        data = {'title': 'Пост Админа', 'content': '', 'cat': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_with_null_category_by_admin(self):
        url = reverse('post_list')
        self.client.force_authenticate(self.admin)
        data = {'title': 'Пост Админа', 'content': 'Контент', 'cat': 0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_without_category_by_admin(self):
        url = reverse('post_list')
        self.client.force_authenticate(self.admin)
        data = {'title': 'Пост Админа', 'content': 'Контент',}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MenAPIUpdateViewTest(APITestCase):
    def setUp(self):
        Category.objects.create(name='Певцы')
        Category.objects.create(name='Актеры')

        self.admin = User.objects.create(username='Админ',
                                         email='admin@test.com',
                                         password='Ololo965',
                                         is_staff=True,
                                         is_active=True)

        self.user = User.objects.create(username='Юзер',
                                        email='user@test.com',
                                        password='Ololo965',
                                        is_staff=False,
                                        is_active=True)

        for i in range(4):
            Men.objects.create(title=f'Ли Ёнбок {i}',
                               content='Ли Ёнбок (англ. Lee Yong-bok, кор. 이용복), при рождении — Феликс Ли (англ. Felix Lee; род. 15 сентября 2000 года,— южнокорейский и австралийский певец, рэпер, ведущий танцор, композитор и автор песен.',
                               is_published=True,
                               cat_id=1 if (i % 2) else 2,
                               user_id=1 if (i % 2) else 2)
    def tearDown(self):
        self.client.force_authenticate(user=None)
        # self.client.logout()

    def test_get_post_by_id_by_unauthorised_user(self):
        url = reverse('read_update_post', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_by_id_by_authorised_user(self):
        url = reverse('read_update_post', kwargs={'pk': 1})
        self.client.force_authenticate(self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_by_id_by_admin(self):
        url = reverse('read_update_post', kwargs={'pk': 1})
        self.client.force_authenticate(self.admin)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_by_wrong_id_by_admin(self):
        url = reverse('read_update_post', kwargs={'pk': 10})
        self.client.force_authenticate(self.admin)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_by_id_by_unauthorised_user(self):
        url = reverse('read_update_post', kwargs={'pk': 1})
        changed_data = {'title':'Изменили', 'content': 'Совсем другой текст', 'cat': 1}
        response = self.client.put(url, changed_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_by_id_by_authorised_user(self):
        url = reverse('read_update_post', kwargs={'pk': 1})
        self.client.force_authenticate(self.user)
        changed_data = {'title': 'Изменили', 'content': 'Совсем другой текст', 'cat': 1}
        response = self.client.put(url, changed_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post_by_id_by_admin(self):
        url = reverse('read_update_post', kwargs={'pk': 1})
        self.client.force_authenticate(self.admin)
        changed_data = {'title': 'Изменили', 'content': 'Совсем другой текст', 'cat': 1}
        response = self.client.put(url, changed_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_mist_by_id_by_admin(self):
        url = reverse('read_update_post', kwargs={'pk': 1})
        self.client.force_authenticate(self.admin)
        changed_data = {'title': 'Изменили', 'content': '', 'cat': 1}
        response = self.client.put(url, changed_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_post_mist2_by_id_by_admin(self):
        url = reverse('read_update_post', kwargs={'pk': 1})
        self.client.force_authenticate(self.admin)
        changed_data = {'title': 'Изменили', 'content': 'Content',}
        response = self.client.put(url, changed_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MenAPIDestroyViewTest(APITestCase):
    def setUp(self):
        Category.objects.create(name='Певцы')
        Category.objects.create(name='Актеры')

        self.admin = User.objects.create(username='Админ',
                                         email='admin@test.com',
                                         password='Ololo965',
                                         is_staff=True,
                                         is_active=True)

        self.user = User.objects.create(username='Юзер',
                                        email='user@test.com',
                                        password='Ololo965',
                                        is_staff=False,
                                        is_active=True)

        for i in range(4):
            Men.objects.create(title=f'Ли Ёнбок {i}',
                               content='Ли Ёнбок (англ. Lee Yong-bok, кор. 이용복), при рождении — Феликс Ли (англ. Felix Lee; род. 15 сентября 2000 года,— южнокорейский и австралийский певец, рэпер, ведущий танцор, композитор и автор песен.',
                               is_published=True,
                               cat_id=1 if (i % 2) else 2,
                               user_id=1 if (i % 2) else 2)
    def tearDown(self):
        self.client.force_authenticate(user=None)
        # self.client.logout()

    def test_delete_post_by_id_by_unauthorised_user(self):
        url = reverse('delete_post', kwargs={'pk': 1})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Men.objects.get(pk=1), True)

    def test_delete_post_by_id_by_authorised_user(self):
        url = reverse('delete_post', kwargs={'pk': 1})
        self.client.force_authenticate(self.user)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Men.objects.get(pk=1), True)

    def test_delete_post_by_id_by_admin(self):
        url = reverse('delete_post', kwargs={'pk': 1})
        self.client.force_authenticate(self.admin)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


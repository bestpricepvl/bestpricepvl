from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.test import Client

from bestprice.models import Prices

from django.contrib.auth.models import User, Group

import datetime
from django.utils import timezone

class PricesViewTest(TestCase):
    def setUp(self):
        # Создание пользователя
        test_user1 = User.objects.create_user(username='testuser1', password='Tt12345+')
        test_user1.save()
        # Группа менеджеров уже создана при миграции
        managers = Group.objects.get(name='Managers')
        # Пользователь с ролью менеджера 
        managers.user_set.add(test_user1)
    def test_logged_in_uses_correct_template(self):
        # Вход пользователя
        login = self.client.login(username='testuser1', password='Tt12345+')
        # Переход на указанную страницу (представление)
        resp = self.client.get(reverse('create'))
        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)
        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'create.html')
    # Проверка представление для неаутентифицированного пользователя,
    # если пользователь неавторизованный - перенаправит на страницу входа
    # LOGIN_REDIRECT_URL = '/', LOGIN_URL = '/login/'
    def test_view_deny_anonymous(self):
        response = self.client.get('/create/')
        self.assertRedirects(response, '/accounts/login/?next=/create/')             
        response = self.client.post('/create/')
        self.assertRedirects(response, '/accounts/login/?next=/create/')
    # Проверка POST-запроса, GET-запроса
    def test_view_post(self):
        # Добавляемые в запросе данные        
        data = {
            'datep': timezone.now(),
            'store': 'Магазин',
            'product': 'Молоко',
            'cost': 3000,
            'details': 'Примечание',
        }
        # Залогиниться
        login = self.client.login(username='testuser1', password='Tt12345+')
        # Отправить POST-запрос присваивание follow=True, в запросе, гарантирует что запрос вернёт окончательный URL-адрес пункта назначения (следовательно проверяется /catalog/, а не /)
        response = self.client.post(reverse('create'), data, follow=True)
        # Проверить возврат на страницу index после успешного сохранения
        self.assertRedirects(response, '/')        
        self.assertEqual( response.status_code, 200)
        # Получить id последнего добавленного объекта
        latest_obj = Prices.objects.latest('id')
        #print("latest obj id ", latest_obj.id)
        # Получить страницу с добавленным объектом
        response = self.client.get(reverse('edit', kwargs={'id': latest_obj.id,}))
        self.assertEqual(response.status_code, 200)
        

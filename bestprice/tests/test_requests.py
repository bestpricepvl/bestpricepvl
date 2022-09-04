from django.test import TestCase

from requests import head

from re import findall

from requests import get, head

from django.contrib.auth.models import User, Group
# Create your tests here.

DOMAIN = 'http://127.0.0.1:8000/'

PAGES = (
    '',
    'index/',
    'contact/',
)

PAGES = (DOMAIN + page for page in PAGES)

# переменная с регулярным выражением для ссылки
LINK_REGULAR_EXPRESSION = r'<a[^>]* href="([^"]*)"'

SITE_URL = 'http://127.0.0.1:8000/'

# Возвращает полную ссылку (с URL-адресом сайта)
def get_full_link(link: str) -> str:
    if not link.startswith('http'):
        link = SITE_URL + link
    return link

# Класс с тестами страниц
class PagesTests(TestCase):
    def setUp(self):
        # Создание пользователя
        test_user1 = User.objects.create_user(username='testuser1', password='Tt12345+')
        test_user1.save()
        # Группа менеджеров уже создана при миграции
        managers = Group.objects.get(name='Managers')
        # Пользователь с ролью менеджера 
        managers.user_set.add(test_user1)
    # Тест статус-кода
    def test_status_code(self):
        # Вход пользователя
        login = self.client.login(username='testuser1', password='Tt12345+')
        for page in PAGES:
            with self.subTest(f'{page=}'):
                response = head(page) 
                self.assertEqual(response.status_code, 200) 

    """
    #Тест ссылок страниц
    def test_links(self):
   
        valid_links = set()

        for page in PAGES:
            #page_content = get(page).content # (1)
            page_content = get(get_full_link(page)).content # (1)
            page_links = set( # (2)
                findall(LINK_REGULAR_EXPRESSION, str(page_content))
            )

            for link in page_links:
                if link in valid_links:
                    continue

                with self.subTest(f'{link=} | {page=}'):
                    response = head(link, allow_redirects=True)

                    if response.status_code == 200:
                        valid_links.add(link)

                    self.assertEqual(response.status_code, 200) # (3)
    """

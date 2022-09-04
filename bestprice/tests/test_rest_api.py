
from django.core import mail
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import (
    APITestCase, APIRequestFactory, force_authenticate
)
from ..views import PricesViewSet
from django.contrib.auth.models import User, Group
User = get_user_model()

from bestprice.models import Prices

from django.utils import timezone

# Create your tests here.
class PricesViewSetTest(APITestCase):

    def setUp(self):
        '''
        Create basic user/admin accounts needed to test this ViewSet.
        '''
        # Создание пользователя
        test_user1 = User.objects.create_user(username='testuser1', password='Tt12345+')
        test_user1.save()
        # Группа менеджеров уже создана при миграции
        managers = Group.objects.get(name='Managers')
        # Пользователь с ролью менеджера 
        managers.user_set.add(test_user1)        
        self.user = User.objects.create_user(
            username='user', password=make_password('user')
        )        
        self.view = PricesViewSet.as_view(actions={
            'get': 'list',
            'post': 'create',
            'options': 'options'
        })


    def test_view_returns_403_status_code_for_unauthenticated_get_request(self):

        factory = APIRequestFactory()
        request = factory.get('http://127.0.0.1:8000/api/prices/')

        response = self.view(request)
        response.render()
        #print('response.status_code ', response.status_code)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_view_returns_200_status_code_for_authenticated_user_get_request(self):
        factory = APIRequestFactory()
        request = factory.get('http://127.0.0.1:8000/api/prices/')
        force_authenticate(request, user=self.user)

        response = self.view(request)
        response.render()
        #print('response.status_code ', response.status_code)
        assert response.status_code == status.HTTP_200_OK
    '''
    def test_view_returns_list_of_all_users_for_admin_get_request(self):

        factory = APIRequestFactory()
        request = factory.get('http://127.0.0.1:8000/api/prices/')
        force_authenticate(request, user=self.user)

        response = self.view(request)
        response.render()

        prices = Prices.objects.all()
        for price in prices:
            print(price.store)
        
        results = [result['store'] for result in response.data['results']]

        print(results)
        result = all(prices.store in results for price in prices)

        self.astertTrue(result)
    '''
    def test_view_returns_201_status_code_for_successful_user_creation(self):

        factory = APIRequestFactory()
        request = factory.post('http://127.0.0.1:8000/api/prices/', {
            'datep': timezone.now(),
            'store': 'SMALL',
            'product': 'Товар',
            'cost': 666,
            'details': 'Детали'
        })

        response = self.view(request)
        response.render()

        #print('response.status_code ', response.status_code)

        assert response.status_code == status.HTTP_201_CREATED

    def _test_delete_detail_from_other_bot(self):
        prices = Prices.create()
        
        factory = APIRequestFactory()
        request = factory.delete('http://127.0.0.1:8000/api/prices/'(prices.pk))
        response = self.view(request)
        print('response.status_code ', response.status_code)
        assert response.status_code == status.HTTP_404_NOT_FOUND



        

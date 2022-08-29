from django.test import TestCase

# Create your tests here.

from django.utils.translation import gettext_lazy as _

from bestprice.forms import PricesForm
from bestprice.models import Prices
from django.contrib.auth.models import User

import datetime
from django.utils import timezone

# Тесты формы PricesFormTests
class PricesFormTests(TestCase):
    # Тест лейблов полей        
    def test_field_labels(self):
        form = PricesForm()
        datep_label = form.fields['datep'].label
        self.assertEqual(datep_label, _('The date'))
        store_label = form.fields['store'].label
        self.assertEqual(store_label, _('Place of Purchase'))
        product_label = form.fields['product'].label
        self.assertEqual(product_label, _('Product (commodity)'))
        cost_label = form.fields['cost'].label
        self.assertEqual(cost_label, _('Price'))
        details_label = form.fields['details'].label
        self.assertEqual(details_label, _('Details'))
        print("PricesFormTests.test_field_labels OK")
    # Тест создания новой записи
    def test_form_save(self):
        data = {"datep": timezone.now(), "store": "Магазин", "product": "Молоко", "cost": 300, "details": "Примечание"}
        form = PricesForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertIsInstance(form.save(), Prices)
        print("PricesFormTests.test_form_save OK")
        

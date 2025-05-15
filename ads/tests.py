from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad
from django.utils import timezone

class AdModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpassword123')
        cls.ad_with_all_fields = Ad.objects.create(
            user=cls.user,
            title='Тестовое объявление полное',
            description='Это описание тестового объявления.',
            image_url='http://example.com/image.jpg',
            category='Электроника',
            condition='Новый'
        )
        cls.ad_minimal_fields = Ad.objects.create(
            user=cls.user,
            title='Тестовое объявление минимальное',
            description='Описание.',
            category='Мебель',
            condition='Б/У'
        )

    def test_ad_creation(self):
        ad = self.ad_with_all_fields 
        self.assertEqual(ad.title, 'Тестовое объявление полное')
        self.assertEqual(ad.user.username, 'testuser')
        self.assertEqual(str(ad), 'Тестовое объявление полное')
        self.assertTrue(isinstance(ad, Ad))

    def test_ad_image_url_optional(self):
        self.assertIsNone(self.ad_minimal_fields.image_url)
        self.assertEqual(self.ad_with_all_fields.image_url, 'http://example.com/image.jpg')

    def test_ad_created_at_auto_filled(self):
        self.assertIsNotNone(self.ad_minimal_fields.created_at)
        self.assertLess((timezone.now() - self.ad_minimal_fields.created_at).total_seconds(), 5)
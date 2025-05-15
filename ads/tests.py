from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
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

class ExchangeProposalModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_sender = User.objects.create_user(username='sender', password='password123')
        cls.user_receiver = User.objects.create_user(username='receiver', password='password123')

        cls.ad_sender = Ad.objects.create(
            user=cls.user_sender,
            title='Объявление отправителя',
            description='Описание от отправителя',
            category='Книги',
            condition='Хорошее'
        )
        cls.ad_receiver = Ad.objects.create(
            user=cls.user_receiver,
            title='Объявление получателя',
            description='Описание от получателя',
            category='Игры',
            condition='Отличное'
        )

        cls.proposal = ExchangeProposal.objects.create(
            ad_sender=cls.ad_sender,
            ad_receiver=cls.ad_receiver,
            comment='Давай меняться!'
        )

    def test_exchange_proposal_creation(self):
        """Тест создания ExchangeProposal и проверки его полей."""
        self.assertEqual(self.proposal.ad_sender.title, 'Объявление отправителя')
        self.assertEqual(self.proposal.ad_receiver.title, 'Объявление получателя')
        self.assertEqual(self.proposal.comment, 'Давай меняться!')
        self.assertEqual(self.proposal.status, 'pending')
        self.assertTrue(isinstance(self.proposal, ExchangeProposal))

    def test_exchange_proposal_str_method(self):
        """Тест строкового представления ExchangeProposal."""
        expected_str = f"от {self.user_sender.username} для {self.ad_receiver.title}"
        self.assertEqual(str(self.proposal), expected_str)

    def test_exchange_proposal_created_at_auto_filled(self):
        self.assertIsNotNone(self.proposal.created_at)
        self.assertLess((timezone.now() - self.proposal.created_at).total_seconds(), 5)

class AdFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='formtestuser', password='password123')

    def test_ad_form_valid_data(self):
        """Тест AdForm с валидными данными."""
        form_data = {
            'title': 'Новое объявление из формы',
            'description': 'Подробное описание товара.',
            'category': 'Техника',
            'condition': 'Идеальное',
        }
        form = AdForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Форма не валидна, ошибки: {form.errors.as_json()}")

    def test_ad_form_missing_required_title(self):
        """Тест AdForm, когда отсутствует обязательное поле title."""
        form_data = {
            'description': 'Описание без заголовка.',
            'category': 'Мебель',
            'condition': 'Хорошее',
        }
        form = AdForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_ad_form_with_image_url(self):
        form_data = {
            'title': 'Объявление с картинкой',
            'description': 'Описание товара с картинкой.',
            'image_url': 'http://example.com/image.png',
            'category': 'Одежда',
            'condition': 'Новое',
        }
        form = AdForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Форма не валидна, ошибки: {form.errors.as_json()}")

class ExchangeProposalFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.proposing_user = User.objects.create_user(username='proposer', password='password123')
        cls.receiving_user = User.objects.create_user(username='receiver_owner', password='password123')
        cls.ad_owned_by_proposer = Ad.objects.create(
            user=cls.proposing_user,
            title='Мое объявление для обмена',
            description='Предлагаю это.',
            category='Электроника',
            condition='Хорошее'
        )
        cls.another_ad_owned_by_proposer = Ad.objects.create(
            user=cls.proposing_user,
            title='Еще одно мое объявление',
            description='Или это.',
            category='Книги',
            condition='Новое'
        )
        cls.ad_not_owned_by_proposer = Ad.objects.create(
            user=cls.receiving_user, 
            title='Чужое объявление',
            description='Не мое.',
            category='Инструменты',
            condition='Б/У'
        )

    def test_exchange_proposal_form_valid_data(self):
        form_data = {
            'ad_sender': self.ad_owned_by_proposer.pk, 
            'comment': 'Привет! Интересует обмен.',
        }
        form = ExchangeProposalForm(data=form_data, user=self.proposing_user)
        self.assertTrue(form.is_valid(), msg=f"Форма не валидна, ошибки: {form.errors.as_json()}")

    def test_exchange_proposal_form_missing_ad_sender(self):
        form_data = {
            'comment': 'Забыл выбрать свое объявление.',
        }
        form = ExchangeProposalForm(data=form_data, user=self.proposing_user)
        self.assertFalse(form.is_valid())
        self.assertIn('ad_sender', form.errors)

    def test_exchange_proposal_form_ad_sender_queryset(self):
        """Тест, что queryset для ad_sender фильтруется по пользователю."""
        form = ExchangeProposalForm(user=self.proposing_user)
        expected_ads_qs = Ad.objects.filter(user=self.proposing_user)
        self.assertQuerySetEqual(
            form.fields['ad_sender'].queryset.order_by('pk'),
            expected_ads_qs.order_by('pk'),
            transform=lambda x: x,
            ordered=False
        )
        self.assertNotIn(self.ad_not_owned_by_proposer, form.fields['ad_sender'].queryset)

    def test_exchange_proposal_form_comment_optional(self):
        form_data = {
            'ad_sender': self.another_ad_owned_by_proposer.pk,
        }
        form = ExchangeProposalForm(data=form_data, user=self.proposing_user)
        self.assertTrue(form.is_valid(), msg=f"Форма не валидна, ошибки: {form.errors.as_json()}")
from django.test import TestCase, Client
from django.urls import reverse
from .models import Recipe, Category


class MainViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        category = Category.objects.create(name='Test Category')
        for i in range(15):
            Recipe.objects.create(
                title=f'Recipe {i}',
                description='desc',
                instructions='instructions',
                ingredients='ingredients',
                category=category
            )

    def test_main_returns_200(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_main_uses_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, 'main.html')

    def test_main_returns_max_10_recipes(self):
        response = self.client.get(reverse('main'))
        self.assertLessEqual(len(response.context['recipes']), 10)


class CategoryDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Soups')
        Recipe.objects.create(
            title='Borscht',
            description='desc',
            instructions='instructions',
            ingredients='ingredients',
            category=self.category
        )

    def test_category_detail_returns_200(self):
        response = self.client.get(reverse('category_detail', args=[self.category.pk]))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_uses_correct_template(self):
        response = self.client.get(reverse('category_detail', args=[self.category.pk]))
        self.assertTemplateUsed(response, 'category_detail.html')

    def test_category_detail_returns_404_for_invalid_id(self):
        response = self.client.get(reverse('category_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_category_detail_shows_correct_recipes(self):
        response = self.client.get(reverse('category_detail', args=[self.category.pk]))
        self.assertIn('recipes', response.context)
        self.assertEqual(len(response.context['recipes']), 1)

from os import stat
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient # test client that can be ussed to make requests to our API and then check what the respone is.

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApisTests(TestCase):
    """Test the pubilically available Ingredient api """

    def SetUp(self):
        self.client = APIClient()

    
    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    
    class PrivateIngredientApisTests(TestCase):
        """Test the private Ingredient api that can only access by the authorized user"""


        def setUp(self):
            self.user = get_user_model().objects.create_user(
                'test@khalti.com',
                'password'
            )
            self.client.force_authenticate(self.user)


        def test_retrive_ingredient_list(self):
            """test to retrive list of the ingredients"""
            Ingredient.objects.create(user=self.user, name='coffee')
            Ingredient.objects.create(user=self.user, name='suger')

            res = self.client.get(INGREDIENT_URL)
            ingredients = Ingredient.objects.all().order_by('-name')
            serializer = IngredientSerializer(ingredients, many=True)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)

        
        def test_ingredients_limited_to_the_user(self):
            """Test that ingredient for the authenticated user are return"""

            user2 = get_user_model().objects.create_user(
                "otheruser@khalti.com",
                "password"
            )
            Ingredient.objects.create(user=user2, name='venigar')

            ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')

            res = self.client.get(INGREDIENT_URL)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(len(res.data), 1)
            self.assertEqual(res.data[0]['name'], ingredient.name)

        
        def test_create_ingredient_successful(self):
            """Test creating a new Ingredient"""

            payload = {'name': 'milk'}
            self.client.post(INGREDIENT_URL, payload)


            exists = Ingredient.objects.filter(
                user=self.user,
                name=payload['name'],
            ).exists()
            self.assertTrue(exists)

        
        def test_create_ingredient_invalid(self):
            """Test creating a new ingredient with invalid payload"""
            payload = {'name': ''}
            res = self.client.post(INGREDIENT_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)







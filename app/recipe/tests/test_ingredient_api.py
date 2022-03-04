from os import stat
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient # test client that can be ussed to make requests to our API and then check what the respone is.

from core.models import Ingredient, Recipe

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

        

        def test_retrieve_ingredients_assigned_to_recipes(self):
            """Test filtering ingredients by those assigned to recipes"""
            ingredient1 = Ingredient.objects.create(
                user=self.user, name='Apples'
            )
            ingredient2 = Ingredient.objects.create(
                user=self.user, name='Turkey'
            )
            recipe = Recipe.objects.create(
                title='Apple crumble',
                time_minutes=5,
                price=10,
                user=self.user
            )
            recipe.ingredient.add(ingredient1)

            res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})

            serializer1 = IngredientSerializer(ingredient1)
            serializer2 = IngredientSerializer(ingredient2)
            self.assertIn(serializer1.data, res.data)
            self.assertNotIn(serializer2.data, res.data)

        def test_retrieve_ingredient_assigned_unique(self):
            """Test filtering ingredients by assigned returns unique items"""
            ingredient = Ingredient.objects.create(user=self.user, name='Eggs')
            Ingredient.objects.create(user=self.user, name='Cheese')
            recipe1 = Recipe.objects.create(
                title='Eggs benedict',
                time_minutes=30,
                price=12.00,
                user=self.user
            )
            recipe1.ingredients.add(ingredient)
            recipe2 = Recipe.objects.create(
                title='Green eggs on toast',
                time_minutes=20,
                price=5.00,
                user=self.user
            )
            recipe2.ingredient.add(ingredient)

            res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})

            self.assertEqual(len(res.data), 1)
        


        # def test_retrieve_ingredient_assign_to_recipes(self):
        #     """Test filtering ingredient by those assign to receipts"""
        #     ingredient1 = Ingredient.objects.create(user= self.user, name="apple")
        #     ingredient2 = Ingredient.objects.create(user=self.user, name='turkey')

        #     recipe = Recipe.objects.create(
        #         title='something in dinner',
        #         time_minutes=5,
        #         price=10,
        #         user=self.user
        #     )
        #     recipe.ingredient.add(ingredient1)

        #     res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})

        #     serializer1 = IngredientSerializer(ingredient1)
        #     serializer2 = IngredientSerializer(ingredient2)

        #     self.assertIn(serializer1.data, res.data)
        #     self.assertNotIn(serializer2.data, res.data)


        # def test_retrieve_ingredients_assigned_unique(self):
        #     """Test filterig ingredient by assigned returns unique items"""
            

        #     ingredient = Ingredient.objects.create(user = self.user, name = 'coffee')
        #     Ingredient.objects.create(user=self.user, name='qwerty')

        #     recipe1 = Recipe.objects.create(
        #         title='pancake',
        #         time_minutes = 30,
        #         price=5,
        #         user=self.user
        #     )
        #     recipe1.ingredient.add(ingredient)

        #     recipe2 = Recipe.objects.create(
        #         title='curry',
        #         time_minutes=3,
        #         price=1,
        #         user=self.user
        #     )
        #     recipe2.ingredient.add(ingredient)

        #     res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})
        #     self.assertEqual(len(res.data), 1)






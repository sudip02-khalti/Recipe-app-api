from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@khalti.com', password='Test@0987'):
    """Create the sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@khalti.com"
        password = "Test@0987"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@KHALTI.com'
        user = get_user_model().objects.create_user(email, 'Test@0987')
        
        self.assertEqual(user.email, email.lower())


    def test_new_user_invalid_email(self):
        """Test createing user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Test@0987')

    
    def test_create_super_user(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            "test@khalti.com",
            'Test@0987'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    
    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    
    def test_ingredient_str(self):
        """Test the ingredient string representatin"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
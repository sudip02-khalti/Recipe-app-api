from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Ingredient, Tag, Recipe

from recipe import serializers


# class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
#     """Manage tags in the database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Tag.objects.all()
#     serializer_class = serializers.TagSerializer


#     def get_queryset(self):
#         """Return objects from the currrent authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')


#     def perform_create(self, serializer):
#         """Create new tag"""
#         serializer.save(user=self.request.user)

    
# class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
#     """Manage ingredients in the database"""

#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Ingredient.objects.all()
#     serializer_class = serializers.IngredientSerializer


#     def get_queryset(self):
#         """Returns objects from the authenticated user"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')

    
#     def perform_create(self, serialiser):
#         """Create new ingredient"""
#         serialiser.save(user=self.request.user)


# REFACTOR CODE......

class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipe in the database"""
    serializer_class = serializers.RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()


    def get_queryset(self):
        """Retrive the recipes for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    
    def get_serializer_class(self):
        """Return appropriate serialiser class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailsSerializer
        return self.serializer_class


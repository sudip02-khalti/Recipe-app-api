from pyexpat import model
from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)



class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the Ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the Recipe objects"""

    ingredient = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Ingredient.objects.all()
    )
    tag = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredient', 'tag', 'time_minutes', 'price', 'link')

        read_only_fields = ('id',)


class RecipeDetailsSerializer(RecipeSerializer):
    ingredient = IngredientSerializer(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)
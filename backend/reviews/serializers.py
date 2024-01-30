from django.shortcuts import get_object_or_404

from rest_framework import serializers

from organizations.models import Organization
from reviews.models import Review


class ReviewListSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов для LIST-метода."""

    id = serializers.IntegerField(
        label='id отзыва',
        help_text='id отзыва',
        read_only=True)
    text = serializers.CharField(
        label='Текст',
        help_text='Текст отзыва',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='email',
        help_text='Почта пользователя, оставившего отзыв',
        read_only=True
    )
    score = serializers.IntegerField(
        label='Оценка организации',
        help_text='Оценка организации от 1 до 5',
        read_only=True
    )
    pub_date = serializers.CharField(
        help_text='Дата публикации отзыва',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='email',
        read_only=True,
    )

    score = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id',)

    def validate(self, data):
        request = self.context.get('request')

        if request.method == 'POST':
            uuid = self.context['view'].kwargs.get('uuid')
            uuid_name = get_object_or_404(Organization, uuid=uuid)
            if Review.objects.filter(
                    author=request.user,
                    organization=uuid_name
            ).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв!')
        return data

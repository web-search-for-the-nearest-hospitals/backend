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

    first_name = serializers.CharField(
        source='author.first_name',
        help_text='Имя автора отзыва',
        required=False)

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
        fields = ('id', 'text', 'first_name', 'score', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        min_length=2,
        max_length=150,
        required=True,
        help_text='Имя пользователя',
        write_only='True'
    )

    score = serializers.IntegerField(
        min_value=1, max_value=5,
        help_text='Оценка организации')

    class Meta:
        model = Review
        fields = ('text', 'score', 'pub_date', 'first_name')

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

    def create(self, validated_data):
        r = self.context.get('request')
        user = r.user
        user.first_name = validated_data.pop('first_name')
        user.save(update_fields=['first_name'])
        return super().create(validated_data)

from django.shortcuts import get_object_or_404

from rest_framework import serializers

from organizations.models import Organization
from reviews.models import Review


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

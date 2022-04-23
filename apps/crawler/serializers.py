from rest_framework import serializers

from apps.crawler.models import Trend


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = '__all__'

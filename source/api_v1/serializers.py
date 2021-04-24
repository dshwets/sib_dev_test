from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file',)


class TopClientSerializer(serializers.Serializer):
    username = serializers.CharField(source="customer")
    spent_money = serializers.IntegerField(source="total")
    gems = serializers.ListField()


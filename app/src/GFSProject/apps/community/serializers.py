from django.shortcuts import get_object_or_404
from .models import MessageModel
from rest_framework.serializers import ModelSerializer, CharField
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient, body=validated_data['body'], user=user)
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

from accounts.models import User
from utils.serializers import ModelSerializer


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "user_type", "mobile", "password"]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

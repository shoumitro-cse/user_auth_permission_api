from rest_framework.exceptions import ValidationError

from accounts.models import User
from utils.serializers import ModelSerializer


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email", "user_type", "mobile", "address"]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        """ remove field if it's not permitted """
        data = super().to_representation(instance)
        current_user = self.context['request'].user
        print(current_user)
        for field_name, field_value in sorted(data.items()):
            full_perm_text = '{}.view_{}'.format(instance._meta.app_label, field_name)
            if not current_user.has_perm(full_perm_text):
                data.pop(field_name)
        return data

    def to_internal_value(self, data):
        errors = {}
        data = super().to_internal_value(data)
        current_user = self.context['request'].user
        for field_name, field_value in sorted(data.items()):
            full_perm_text = '{}.change_{}'.format(self.Meta.model._meta.app_label, field_name)
            if field_value and not current_user.has_perm(full_perm_text):
                # throw error if it's not permitted
                errors[field_name] = [f"{field_name} not allowed to change"]
        if errors:
            raise ValidationError(errors)
        return data

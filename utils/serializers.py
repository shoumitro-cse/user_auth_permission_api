from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError


class ModelSerializerFieldViewMixin(ModelSerializer):
    """
       This class will be used to restrict the given functionality.
         ** patch or put method field view permission
    """

    def to_representation(self, instance):
        """ for patch or put method field view permission """
        request = self.context['request']
        data = super().to_representation(instance)
        if not request:
            return data
        if str(request.method).upper() in ["PUT", "PATCH"]:
            request_data_keys = dict(request.data).keys()
            for field_name, field_value in sorted(data.items()):
                if field_name not in request_data_keys:
                    data.pop(field_name)
        return data


class ModelSerializerFieldPermissionMixin(ModelSerializerFieldViewMixin):
    """
       This class will be used to restrict the given functionality.
         ** column edit permission
         ** column view permission
    """
    def to_representation(self, instance):
        """ for column view permission """
        data = super().to_representation(instance)
        if self.context.get('request', None):
            current_user = self.context['request'].user
            for field_name, field_value in sorted(data.items()):
                full_perm_text = '{}.view_{}'.format(instance._meta.app_label, field_name)
                if not current_user.has_perm(full_perm_text):
                    # remove field if it's not permitted
                    data.pop(field_name)
        return data

    def to_internal_value(self, data):
        """ for column edit permission """
        errors = {}
        data = super().to_internal_value(data)
        if self.context.get('request', None):
            current_user = self.context['request'].user
            for field_name, field_value in sorted(data.items()):
                full_perm_text = '{}.change_{}'.format(self.Meta.model._meta.app_label, field_name)
                if field_value and not current_user.has_perm(full_perm_text):
                    # throw error if it's not permitted
                    errors[field_name] = [f"{field_name} not allowed to change"]
            if errors:
                raise ValidationError(errors)
        return data


class ModelSerializer(ModelSerializerFieldPermissionMixin):
    """
       This class will be used to restrict the given functionality.
         ** patch or put method field view permission
         ** column edit permission
         ** column view permission
    """
    pass

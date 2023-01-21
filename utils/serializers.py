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
            request_data_keys = request.data.keys()
            for field_name in sorted(data.keys()):
                if field_name not in request_data_keys:
                    data.pop(field_name)
        return data


class ModelSerializerFieldPermissionMixin(ModelSerializerFieldViewMixin):
    """
       This class will be used to restrict the given functionality.
         ** column edit permission
         ** column view permission

       Way to get field key:
        ** print(self.Meta.fields)
        ** print(sorted(data.keys()))
        ** print(sorted(data.items()))

        delete method can't these functions
            * Nothing

        for get method
        ---to_representation ---

        for post, patch, put method
        ---to_internal_value---
        ---to_representation ---
    """
    permission_fields = []

    def to_representation(self, instance):
        """ for column view permission"""
        data = super().to_representation(instance)
        if self.context.get('request', None):
            current_user = self.context['request'].user
            app_name = self.Meta.model._meta.app_label
            perm_name = str(self.Meta.model.__name__).lower()
            model_view_perm_text = '{}.view_{}'.format(app_name, perm_name)
            # check model or table level view permission
            if not current_user.has_perm(model_view_perm_text):
                # check field or column view level permission
                for field_name in self.permission_fields or sorted(data.keys()):
                    full_perm_text = '{}.view_{}'.format(app_name, field_name)
                    if not current_user.has_perm(full_perm_text):
                        # remove field if it's not permitted
                        data.pop(field_name)
        return data

    def to_internal_value(self, data):
        """ for column edit permission."""
        data = super().to_internal_value(data)
        request = self.context.get('request', None)

        if request:
            errors = {}
            current_user = request.user
            app_name = self.Meta.model._meta.app_label
            perm_name = str(self.Meta.model.__name__).lower()
            req_method = str(request.method).upper()

            if req_method == "POST":
                model_add_perm_text = '{}.add_{}'.format(app_name, perm_name)
                # check model or table level create permission
                if not current_user.has_perm(model_add_perm_text):
                    errors[perm_name] = [f"{perm_name} not allowed to add any record"]

            if req_method in ["PATCH", "PUT"]:
                model_edit_perm_text = '{}.change_{}'.format(app_name, perm_name)
                # check model or table level edit permission
                if not current_user.has_perm(model_edit_perm_text):
                    # check field or column edit level permission
                    for field_name in self.permission_fields or sorted(data.keys()):
                        full_perm_text = '{}.change_{}'.format(app_name, field_name)
                        if not current_user.has_perm(full_perm_text):
                            # throw error if it's not permitted
                            errors[field_name] = [f"{field_name} not allowed to change"]
            if errors:
                raise ValidationError(errors)
        return data


class PermissionModelSerializer(ModelSerializerFieldPermissionMixin):
    """
       This class will be used to restrict the given functionality.
         ** patch or put method field view permission
         ** column edit permission
         ** column view permission
    """
    pass

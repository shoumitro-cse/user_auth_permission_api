from rest_framework.serializers import ModelSerializer as BaseModelSerializer


class ModelSerializer(BaseModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request_data_keys = dict(self.context['request'].data).keys()
        for field_name, field_value in sorted(data.items()):
            if field_name not in request_data_keys:
                data.pop(field_name)
        return data

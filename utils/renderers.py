from rest_framework.renderers import JSONRenderer as BaseJSONRenderer


class JSONRenderer(BaseJSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {}
        if not str(status_code).startswith('2'):
            response["success"] = False
            try:
                response["error"] = data["detail"]
            except KeyError:
                response["error"] = data
        else:
            response = {
                "success": True,
                "data": data,
            }
        return super().render(response, accepted_media_type, renderer_context)


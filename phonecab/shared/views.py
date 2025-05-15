from django.http import HttpResponse
from django.views.generic import View


class PhonecabHomeView(View):

    model_class = Object
    template = ''

    def get_objects(self, request):
        pass

    def get(self, request):
        d = request.GET.dict()
        variables['items'] = self.get_objects(request)
        variables['d'] = d

        return render_to_response(
            self.template, RequestContext(request, variables))




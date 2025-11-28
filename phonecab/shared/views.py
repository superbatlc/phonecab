from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class PhonecabHomeView(View):

    model_class = Object
    template = ''

    def get_objects(self, request):
        pass

    def get(self, request):
        d = request.GET.dict()
        variables = {}
        variables['items'] = self.get_objects(request)
        variables['d'] = d

        return render(request,
            self.template, variables)




from django.http import HttpResponse



class HttpGenericResponse(HttpResponse):

    def __init__(self, status, content):
        self.status = status
        self.content = content
        self.content_type='application/json'


class Http404Response(HttpResponse):

    def __init__(self, content):
        super(Http404Response, self).__init__(404, content)


class Http400Response(HttpResponse):

    def __init__(self, content):
        super(Http400Response, self).__init__(400, content)


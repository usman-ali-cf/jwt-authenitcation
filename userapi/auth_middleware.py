from django.shortcuts import loader
from django.http import HttpResponse


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_urls = []
        # Your custom authentication
        if self.is_authenticated(request) is None and request.path not in allowed_urls:
            template = loader.get_template("login.html")
            return HttpResponse(template.render())
        response = self.get_response(request)
        return response

    def is_authenticated(self, request):
        return request.user.is_authenticated

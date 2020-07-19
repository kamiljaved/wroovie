from django.http import HttpResponseRedirect
from django.conf import settings

class SiteFlavorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.media_dir = settings.MEDIA_URL.strip('/')
        # One-time configuration and initialization.
        print(settings.BASE_DIR)
        print(settings.MEDIA_ROOT)

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        path_dirs = request.path.split('/')
        if not (len(path_dirs) > 1 and path_dirs[1] == self.media_dir):
            # if request is not for a media object, then redirect a mobile device
            if request.user_agent.is_mobile or request.user_agent.is_tablet:
                return HttpResponseRedirect(settings.MOBILE_SITE_URL + request.path)

        response = self.get_response(request)
        
        # Code to be executed for each request/response after
        # the view is called.
        return response
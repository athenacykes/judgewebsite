from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
import os
import datetime
import logging


logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response


class LogoutView(TemplateView):
    template_name = 'users/logout.html'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super().get(request, *args, **kwargs)


class OidcLogoutView(View):
    def post(self, request, *args, **kwargs):
        # TODO: perform standard OpenID Logout using ID Token implementation.
        current_host = request.get_host()
        current_protocol = "https://" if request.is_secure() else "http://"
        current_host_url = current_protocol + current_host + "/"

        if settings.OIDC_OP_LOGOUT_ENDPOINT:
            oidc_logout_url = settings.OIDC_OP_LOGOUT_ENDPOINT
            redirect_url = oidc_logout_url + '?redirect_uri=' + current_host_url
            response = HttpResponse("", status=302)
            response['Location'] = redirect_url
            auth.logout(request)
            return response
        else:
            auth.logout(request)
            return HttpResponseRedirect('/')
# [End of Views]


# AJAX function TinyMCE upload image.
# For Admin Console.
@method_decorator(csrf_exempt, name='dispatch')
class UploadImageView(View):
    def post(self, request, *args, **kwargs):
        f = request.FILES['file']
        file_name_suffix = f.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", "webp"]:
            return self.failed(message=_("Wrong image format"))
        upload_time = datetime.datetime.now().astimezone()
        path = os.path.join(
            settings.IMAGE_UPLOAD_PATH,
            upload_time.strftime("%Y-%m"),
        )
        # Create path if not exists
        if not os.path.exists(path):
            os.makedirs(path)
        file_path = os.path.join(path, upload_time.strftime("%Y%m%d_%H%M%S") + f'.{file_name_suffix}')
        file_url = file_path.split("judgewebsite")[-1].replace("\\", "/")
        if os.path.exists(file_path):
            return JsonResponse({
                "message": _("File already exists"),
                "src": file_url,
            })
        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return JsonResponse({
            "location": file_url
        })

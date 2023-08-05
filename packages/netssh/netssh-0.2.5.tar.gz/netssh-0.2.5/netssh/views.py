#!./venv/bin/python
from django.shortcuts import render
from django.views.generic import View
from django.templatetags.static import static
from django.urls import reverse
from django.contrib import staticfiles

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
from packaging import version
import json
import re



import paramiko 

import os
from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
if settings.DEBUG:
    application = StaticFilesHandler(get_wsgi_application())
else:
    application = get_wsgi_application() 





class ViewTerminal(PermissionRequiredMixin, View):
    permission_required = ('dcim.view_site')
    #queryset = Device.objects.all()
    template_name = 'netssh/home.html'

    def get(self, request):
        return render(request, self.template_name, {
        })


class ViewWebClient(PermissionRequiredMixin, View):
    permission_required = ('dcim.view_site')
    #queryset = Device.objects.all()
    template_name = 'netssh/index.html'
    
    def get(self, request):
        return render(request, self.template_name, {
        }) 
        


host = '192.168.0.142'
user = 'root'
secret = '121212'
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=secret, port=port)
stdin, stdout, stderr = client.exec_command('ls -l')
data = stdout.read() + stderr.read()
client.close()
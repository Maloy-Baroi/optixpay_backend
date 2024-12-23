from django.core.management.commands.runserver import Command as Runserver
from django_extensions.management.commands.runserver_plus import Command as RunserverPlus

class Command(RunserverPlus):
    def handle(self, *args, **options):
        options['use_reloader'] = False
        options['use_threading'] = True
        options['cert_file'] = 'optixpay_backend/certs/cert.pem'
        options['key_file'] = 'optixpay_backend/certs/key.pem'
        super().handle(*args, **options)

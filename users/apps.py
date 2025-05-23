from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='admin')
        Group.objects.get_or_create(name='user')


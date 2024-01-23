import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')

django.setup()

from loja.views import verificar_carrinhos_abertos

if __name__ == "__main__":
    verificar_carrinhos_abertos()


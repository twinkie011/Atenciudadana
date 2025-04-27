import csv
from django.core.management.base import BaseCommand
from autenticacion.models import MunicipioCP

class Command(BaseCommand):
    help = 'Importa municipios y códigos postales desde un archivo CSV'

    def handle(self, *args, **kwargs):
        with open('municipios_yucatan.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            creados = 0
            for row in reader:
                municipio = row['municipio'].strip()
                cp = row['codigo_postal'].strip()

                obj, creado = MunicipioCP.objects.get_or_create(
                    municipio=municipio,
                    codigo_postal=cp
                )
                if creado:
                    creados += 1

        self.stdout.write(self.style.SUCCESS(f'Se importaron {creados} registros correctamente.'))

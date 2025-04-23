from django.core.management.base import BaseCommand
from analisis.models import *
from registros.models import *
from autenticacion.models import *

import pandas as pd

class Command(BaseCommand):
    help = 'Export data to csv'
    
    def handle(self, *args, **options):
        paises=Pais.objects.all().values()
        deptos=Departamento.objects.all().values()
        municipios=Municipio.objects.all().values()
        comunidades=Comunidad.objects.all().values()
        variedades=Variedad.objects.all().values()
        certificaciones=Certificacion.objects.all().values()
        def1=DefectoT1.objects.all().values()
        def2=DefectoT2.objects.all().values()
        sabor=Sabor.objects.all().values()
        aroma=Aroma.objects.all().values()

        df_paises=pd.DataFrame(paises)
        df_deptos=pd.DataFrame(deptos)
        df_municipios=pd.DataFrame(municipios)
        df_comunidades=pd.DataFrame(comunidades)
        df_variedades=pd.DataFrame(variedades)
        df_certificaciones=pd.DataFrame(certificaciones)
        df_def1=pd.DataFrame(def1)
        df_def2=pd.DataFrame(def2)
        df_sabor=pd.DataFrame(sabor)
        df_aroma=pd.DataFrame(aroma)

        with pd.ExcelWriter("DATA.xlsx") as writer:
            df_paises.to_excel(writer, sheet_name='Paises')
            df_deptos.to_excel(writer, sheet_name='Departamentos')
            df_municipios.to_excel(writer, sheet_name='Municipios')
            df_comunidades.to_excel(writer, sheet_name='Comunidades')
            df_variedades.to_excel(writer, sheet_name='Variedades')
            df_certificaciones.to_excel(writer, sheet_name='Certificaciones')
            df_def1.to_excel(writer, sheet_name='DefectosT1')
            df_def2.to_excel(writer, sheet_name='DefectosT2')
            df_sabor.to_excel(writer, sheet_name='Sabores')
            df_aroma.to_excel(writer, sheet_name='Aromas')
        self.stdout.write(self.style.SUCCESS('Successfully exported data to csv'))
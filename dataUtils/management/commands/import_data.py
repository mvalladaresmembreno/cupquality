from asyncio.windows_events import NULL
from django.core.management.base import BaseCommand
from analisis.models import *
from registros.models import *
from autenticacion.models import *

import pandas as pd

class Command(BaseCommand):
    help = 'Import Data from XLSX'
    
    def handle(self, *args, **options):
        with pd.ExcelFile('DATA.xlsx') as xlsx:
            paises=pd.DataFrame(pd.read_excel(xlsx, 'Paises',index_col=None), columns=['idPais','namePais'])
            deptos=pd.DataFrame(pd.read_excel(xlsx, 'Departamentos',index_col=None), columns=['idDpto','fkPais_id','nameDpto'])
            municipios=pd.DataFrame(pd.read_excel(xlsx, 'Municipios',index_col=None), columns=['idMun','fkdpto_id','nameMun'])
            comunidades=pd.DataFrame(pd.read_excel(xlsx, 'Comunidades',index_col=None), columns=['idCom','fkMun_id','nameCom'])
            variedades=pd.DataFrame(pd.read_excel(xlsx, 'Variedades',index_col=None), columns=['id','nameVariedad'])
            certificaciones=pd.DataFrame(pd.read_excel(xlsx, 'Certificaciones',index_col=None), columns=['id','nameCert'])
            def1=pd.DataFrame(pd.read_excel(xlsx, 'DefectosT1',index_col=None), columns=['idDefecto','nameDefecto', 'granosNecesarios'])
            def2=pd.DataFrame(pd.read_excel(xlsx, 'DefectosT2',index_col=None), columns=['idDefecto','nameDefecto', 'granosNecesarios'])
            sabor=pd.DataFrame(pd.read_excel(xlsx, 'Sabores',index_col=None), columns=['idSabor','nameSabor', 'nivelSabor','pI_id','pII_id']).fillna(0)
            aroma=pd.DataFrame(pd.read_excel(xlsx, 'Aromas',index_col=None), columns=['idAroma','nameAroma', 'nivelAroma','pI_id','pII_id','pIII_id']).fillna(0)
            tamizado=pd.DataFrame(pd.read_excel(xlsx,'Tamizado',index_col=None), columns=['idTamizado', 'nameTamizado'])
            print(paises)
            for p in paises.itertuples():
                    Pais.objects.create(idPais=p.idPais, namePais=p.namePais)
            print(deptos)
            for d in deptos.itertuples():
                Departamento.objects.create(idDpto=d.idDpto, fkPais=Pais.objects.get(idPais=d.fkPais_id), nameDpto=d.nameDpto)
            print(municipios)
            for m in municipios.itertuples():
                Municipio.objects.create(idMun=m.idMun, fkdpto=Departamento.objects.get(idDpto=m.fkdpto_id), nameMun=m.nameMun)
            print(comunidades)
            for c in comunidades.itertuples():
                Comunidad.objects.create(idCom=c.idCom, fkMun=Municipio.objects.get(idMun=c.fkMun_id), nameCom=c.nameCom)
            print(variedades)
            for v in variedades.itertuples():
                Variedad.objects.create(nameVariedad=v.nameVariedad)
            print(certificaciones)
            for c in certificaciones.itertuples():
                Certificacion.objects.create(nameCert=c.nameCert)
            print(def1)
            for d in def1.itertuples():
                DefectoT1.objects.create(idDefecto=d.idDefecto, nameDefecto=d.nameDefecto, granosNecesarios=d.granosNecesarios)
            print(def2)
            for d in def2.itertuples():
                DefectoT2.objects.create(idDefecto=d.idDefecto, nameDefecto=d.nameDefecto, granosNecesarios=d.granosNecesarios)
            print(sabor)
            for s in sabor.itertuples():
                if s.pI_id==0:
                    Sabor.objects.create(idSabor=s.idSabor, nameSabor=s.nameSabor, nivelSabor=s.nivelSabor)
                elif s.pII_id==0:
                    Sabor.objects.create(idSabor=s.idSabor, nameSabor=s.nameSabor, nivelSabor=s.nivelSabor, pI=Sabor.objects.get(idSabor=s.pI_id))
                else:
                    Sabor.objects.create(idSabor=s.idSabor, nameSabor=s.nameSabor, nivelSabor=s.nivelSabor, pI=Sabor.objects.get(idSabor=s.pI_id), pII=Sabor.objects.get(idSabor=s.pII_id))
            print(aroma)
            for a in aroma.itertuples():
                if a.pI_id==0:
                    Aroma.objects.create(idAroma=a.idAroma, nameAroma=a.nameAroma, nivelAroma=a.nivelAroma)
                elif a.pII_id==0:
                    Aroma.objects.create(idAroma=a.idAroma, nameAroma=a.nameAroma, nivelAroma=a.nivelAroma, pI=Aroma.objects.get(idAroma=a.pI_id))
                elif a.pIII_id==0:
                    Aroma.objects.create(idAroma=a.idAroma, nameAroma=a.nameAroma, nivelAroma=a.nivelAroma, pI=Aroma.objects.get(idAroma=a.pI_id), pII=Aroma.objects.get(idAroma=a.pII_id))
                else:
                    Aroma.objects.create(idAroma=a.idAroma, nameAroma=a.nameAroma, nivelAroma=a.nivelAroma, pI=Aroma.objects.get(idAroma=a.pI_id), pII=Aroma.objects.get(idAroma=a.pII_id), pIII=Aroma.objects.get(idAroma=a.pIII_id))
            print(tamizado)
            for t in tamizado.itertuples():
                Tamizado.objects.create(idTamizado=t.idTamizado, nameTamizado=t.nameTamizado)
            print("Data imported successfully")
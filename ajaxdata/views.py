from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from registros.models import *
from analisis.models import *
from autenticacion.models import *
from laboratorios.models import Muestra as MuestraLab
from registros.views import getAromas,getDefectos,getSabor, getSensorial
# Create your views here.
#########TRABAJANDO CON PANDAS Y XLS#########
import pandas as pd
from io import BytesIO as IO
import xlsxwriter
import datetime


@login_required(login_url='/auth/login/', redirect_field_name='next')
def get_municipio(request, idDpto):
    mun=Municipio.objects.filter(fkdpto=idDpto).all().order_by('idMun')
    munlist=list()
    for m in mun:
        munlist.append([m.nameMun, m.idMun])
    data={
        'municipios':munlist,
    }
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def get_municipios(request, idDpto):
    idDpto=idDpto.split(',')
    mun=Municipio.objects.filter(fkdpto__in=idDpto).all().order_by('idMun')
    munlist=list()
    for m in mun:
        munlist.append([m.nameMun, m.idMun])
    data={
        'municipios':munlist,
    }
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def get_comunidad(request, idMun):
    com=Comunidad.objects.filter(fkMun=idMun).all().order_by('idCom')
    comlist=list()
    for c in com:
        comlist.append([c.nameCom, c.idCom])
    data={
        'comunidades':comlist,
    }
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def get_finca(request, idProd):
    fincas=Finca.objects.filter(fkProd=idProd,estado=1).all().order_by("idFinca")
    fincaList=list()
    for f in fincas:
        fincaList.append([f.idFinca, f.nameFinca])
    data={
        'fincas':fincaList
    }
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def get_lote(request, idFinca):
    lotes=Lote.objects.filter(fkFinca=idFinca, estado=1).all().order_by("idLote")
    loteList=list()
    for l in lotes:
        loteList.append([l.idLote, l.nameLote])
    data={
        'lotes':loteList
    }
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def get_muestra(request, idMuestra):
    user=User.objects.get(id=request.user.id)
    m=Muestra.objects.filter(idMuestra=idMuestra).values();
    data=m[0]
    data['catador']=user.first_name +" "+ user.last_name
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def get_sensorial(request, idMuestra):
    try:
        sensorial=Sensorial.objects.filter(fkMuestra=idMuestra).all().order_by("id")
        sensorialList=list()
        for s in sensorial:
            fulname=s.fkCatador.usuario.first_name +" "+ s.fkCatador.usuario.last_name
            sensorialList.append([s.id, fulname, s.fragancia, 
            s.pSabor, s.remanente, s.acidez, s.cuerpo, s.balance, 
            s.pUniformidad, s.cTLimpia, s.pDulzor, s.pCatador, 
            (5-int(s.cTLimpia)), s.getIntensidad(), s.pFinal])
        data={
            'sensorial':sensorialList,
            'idMuestra':idMuestra,
            'success':True

        }
    except:
        data={
            'success':False
        }
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def getFincaUnidad(request, idFinca):
    unidad=Finca.objects.get(idFinca=idFinca).unidad
    data={
        'unidad':unidad,
    }
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def OTexists(request, OT):
    print(MuestraLab.objects.filter(ordenTrabajo=OT).exists())
    return JsonResponse(data={'exists':MuestraLab.objects.filter(ordenTrabajo=OT).exists(), 'success':True}, safe=False)
    
@login_required(login_url='/auth/login/', redirect_field_name='next')
def getxlsMuestras(request):
    data=dict()
    muestras=Muestra.objects.filter(estado__in=[1,6,10,11,12])
    if not User.objects.get(username=request.user).groups.filter(name='Administrador').exists():
        muestras=muestras.filter(fkLote__fkFinca__fkProd__organizacion=Colaborador.objects.get(fkUser=request.user).org)
    if request.method == 'GET':
        if request.GET.get('org') and request.GET.get('org') != '':
            muestras=muestras.filter(fkLote__fkFinca__fkProd__organizacion__id_org=request.GET.get('org'))
        if request.GET.get('municipio') and request.GET.get('municipio') != '':
            muestras=muestras.filter(fkLote__fkFinca__fkProd__fkMun__idMun=request.GET.get('mun'))
        if request.GET.get('cert') and request.GET.get('cert') != '':
            certs=request.GET.get('cert').split('_')
            certs=[eval(c) for c in certs]
            muestras=muestras.filter(fkLote__fkCert__in=certs)
        if request.GET.get('procesos') and request.GET.get('procesos') != '':
            muestras=muestras.filter(procesado=request.GET.get('procesos'))
        if request.GET.get('genero') and request.GET.get('genero') != '':
            muestras=muestras.filter(fkLote__fkFinca__fkProd__genero=request.GET.get('genero'))
        if request.GET.get('sabores') and request.GET.get('sabores') != '':
            sab=request.GET.get('sabores').split('_')
            muestras=muestras.filter(Sensorial__sabor__in=sab)
    for m in muestras:
        data[m.idMuestra]={
            'muestra':m.idMuestra,
            'rechazo': 'Si' if m.rMuestra == 1 else 'No',
            'conciliado': 'Si' if m.estado == 6 else 'No',
            'aEfectuado': 'Fisico & Sensorial' if m.procesos ==3 else 'Fisico' if m.procesos == 1 else 'Sensorial',
            'genero': m.fkLote.fkFinca.fkProd.get_genero_display(),
            'DTI': getDefectos(m, 1),
            'DTII': getDefectos(m, 2),
            'aroma':getAromas(m),
            'sabor':getSabor(m),
            'pf': getSensorial(m),
        }

    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df=pd.DataFrame(data, index=['muestra', 'rechazo', 'conciliado', 'aEfectuado','genero', 'DTI', 'DTII', 'aroma', 'sabor', 'pf']).transpose()
    df=df.rename(columns={'muestra':'Muestra', 'rechazo':'Rechazo', 'conciliado':'Conciliado', 'aEfectuado': 'Análisis Efectuados','genero':'Genero', 'DTI':'Defectos de Tipo I', 'DTII': 'Defectos de Tipo II', 'aroma':'Aromas', 'sabor':'Sabores', 'pf':'Puntaje Final'})
    df.to_excel(xlwriter, sheet_name='Perfil de Muestras', index=False)
    sheet=xlwriter.sheets['Perfil de Muestras']
    for idx, col in enumerate(df):
        series=df[col]
        max_len=max((
            series.astype(str).map(len).max(),
            len(str(series.name))
        ))+1
        sheet.set_column(idx, idx, max_len)
    xlwriter.save()
    excel_file.seek(0)
    response=HttpResponse(excel_file.read(), content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = f'attachment; filename=Perfil de Muestras - '+datetime.datetime.now().strftime ("%Y%m%d")+'.xlsx'
    return response
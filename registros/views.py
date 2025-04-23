from urllib.request import Request
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from registros.models import *
from autenticacion.models import Colaborador
from analisis.models import *
from django.db.models import Count, Avg, Q, Max, Min
from registros.filtros import *

# Create your views here.
@login_required(login_url='/auth/login/', redirect_field_name='next')
def index(request):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    if context['isAdmin']:
        context['departamentos']=Departamento.objects.all()
    else:
        context['departamentos']=Departamento.objects.filter(idDpto=colab.org.ubicacion.fkdpto.idDpto)
    context['certificaciones']=Certificacion.objects.all()
    context['organizaciones']=Organizacion.objects.all()
    context['procesos']=list(Procesado)
    context['sabores']=Sabor.objects.all()
    return render(request, "registros/index.html", context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def filtros(request):
    muestras=Muestra.objects.filter(estado__in=[1,6,10,11,12])
    if not User.objects.get(username=request.user).groups.filter(name='Administrador').exists():
        muestras=muestras.filter(fkLote__fkFinca__fkProd__organizacion=Colaborador.objects.get(usuario=request.user).org)
    if request.method == 'GET':
        if request.GET.get('org') and request.GET.get('org') != '':
            muestras=muestras.filter(fkLote__fkFinca__fkProd__organizacion__id_org=request.GET.get('org'))
        if request.GET.get('municipio') and request.GET.get('municipio') != '':
            muestras=muestras.filter(fkLote__fkFinca__fkProd__fkMun__idMun=request.GET.get('mun'))
        if request.GET.get('cert') and request.GET.get('cert') != '':
            certs=request.GET.get('cert').split('_')
            muestras=muestras.filter(fkLote__fkCert__in=certs)
        if request.GET.get('procesos') and request.GET.get('procesos') != '':
            muestras=muestras.filter(procesado=request.GET.get('procesos'))
        if request.GET.get('genero') and request.GET.get('genero') != '':
            muestras=muestras.filter(fkLote__fkFinca__fkProd__genero=request.GET.get('genero'))
        if request.GET.get('sabores') and request.GET.get('sabores') != '':
            sab=request.GET.get('sabores').split('_')
            muestras=muestras.filter(Sensorial__sabor__in=sab)
        fisico=Fisico.objects.filter(fkMuestra__in=muestras)
        sensorial=Sensorial.objects.filter(fkMuestra__in=muestras)
        conciliacion=Conciliacion.objects.filter(fkCSensorial__fkMuestra__in=muestras)
        def1=FisicoDefectoTI.objects.filter(fkFisico__fkMuestra__in=muestras, defectos__gt=0)
        def2=FisicoDefectoTII.objects.filter(fkFisico__fkMuestra__in=muestras, defectos__gt=0)
        puntajes=sensorial
        for c in conciliacion:
            if c.fkCSensorial in puntajes:
                puntajes=puntajes.exclude(id=c.fkCSensorial.id)
        rangos=sensorial.aggregate(
        Rango1=(Count('id', filter=Q(pFinal__range=[0,69.99]))),
        Rango2=(Count('id', filter=Q(pFinal__range=[70.00,80.99]))),
        Rango3=(Count('id', filter=Q(pFinal__range=[80.99,83.99]))),
        Rango4=(Count('id', filter=Q(pFinal__range=[84.00,85.99]))),
        Rango5=(Count('id', filter=Q(pFinal__range=[85.99,100.00])))) if sensorial else 0
        dt1=def1.values('fkDefecto__nameDefecto').annotate(cant=Count('defectos')) if def1 else 0
        dt2=def2.values('fkDefecto__nameDefecto').annotate(cant=Count('defectos')) if def2 else 0
        motivos=muestras.values('caracteristicas') if muestras else 0
        conteo={
            'Derrame':0,
            'Olor no característico':0,
            'Empaque roto':0,
            'Buen estado':0,
        }
        if motivos:
            for m in motivos:
                for c in m['caracteristicas']:
                    for i in Caracteristicas:
                        if i[0] == int(c):
                            conteo[i[1]]+=1
        data={
            'TMR':muestras.count(),
            'TMAF':fisico.count(),
            'TMAS':sensorial.count() - conciliacion.count(),
            'PDTI':round(def1.aggregate(Avg('porDefecto'))['porDefecto__avg'],2) if def1.count() > 0 else 0,
            'PDTII':round(def2.aggregate(Avg('porDefecto'))['porDefecto__avg'],2) if def2.count() > 0 else 0,
            'PTM':puntajes.aggregate(Min('pFinal'))['pFinal__min'] if puntajes.count() > 0 else 0,
            'PPM':round(puntajes.aggregate(Avg('pFinal'))['pFinal__avg'],2) if puntajes.count() > 0 else 0,
            'PMAX':puntajes.aggregate(Max('pFinal'))['pFinal__max'] if puntajes.count() > 0 else 0,
            'DPT':[
                {'label':'0,69.99', 'cant':int(rangos['Rango1'])},
                {'label':'70.00,80.99', 'cant':int(rangos['Rango2'])},
                {'label':'80.99,83.99', 'cant':int(rangos['Rango3'])},
                {'label':'84.00,85.99', 'cant':int(rangos['Rango4'])},
                {'label':'85.99,100.00', 'cant':int(rangos['Rango5'])},
                ] if rangos else 0,
            'DTI':[{ 'label':d['fkDefecto__nameDefecto'], 'cant':d['cant'] } for d in dt1] if dt1 else 0,
            'DTII': [{ 'label':d['fkDefecto__nameDefecto'], 'cant':d['cant'] } for d in dt2] if dt2 else 0,
            'MRCHZ':{
                'labels':['Si','No'],
                'cant':[muestras.filter(rMuestra=1).count(), muestras.filter(rMuestra=0).count()]
            },
            'MTRCHZ':[{ 'label':key, 'cant':conteo[key] } for key in conteo] if conteo else 0,

        }
    return JsonResponse (data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def addProd(request):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()   
    if request.method=="POST":
        try:
            mun=Municipio.objects.get(idMun=request.POST.get('municipio'))
            prod=Productor(fkMun=mun, firstnameProd=request.POST.get('fname'), lastnameProd=request.POST.get('lname'),fechaNac=request.POST.get('fechaNac'), organizacion=Organizacion.objects.get(id_org=colab.org.id_org), genero=request.POST.get('genero'))
            if request.POST.get('codprod') != '' and request.POST.get('codprod'):
                prod.codigoProd=request.POST.get('codprod') 
            prod.save()
            if request.POST.get('addFinca') == 'true':
                request.session['prod']=prod.idProd
                return redirect('addFinca')
            return HttpResponseRedirect(reverse('addProd'))
        except:
            messages.add_message(request, messages.WARNING, 'No se pudo crear el productor')
    if context['isAdmin'] :
        context['productores']= Productor.objects.filter(estado=1).order_by('idProd')
    else:
        context['productores']= Productor.objects.filter(estado=1, organizacion=colab.org).order_by('idProd')
    context['paises']=Pais.objects.all().order_by('idPais')
    if context['isAdmin'] :
        context['departamentos']=Departamento.objects.all().order_by('idDpto')
    else:
        context['departamentos']=Departamento.objects.filter(fkPais=colab.org.ubicacion.fkdpto.fkPais).order_by('idDpto')
    context['ubicaciones']=Municipio.objects.all().order_by('idMun')
    return render(request, 'registros/productor.html', context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def addFinca(request):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()
    if request.method=="POST":
        try:
            com=Comunidad.objects.get(idCom=request.POST.get('comunidad'))
            prod=Productor.objects.get(idProd=request.POST.get('productor'))
            finca=Finca(fkProd=prod, fkCom=com, nameFinca=request.POST.get('nameFinca'), area=float(request.POST.get('areaFinca')), unidad=request.POST.get("unidad"))
            finca.save()
            if request.POST.get('addLote') == 'true':
                request.session['finca']=finca.idFinca
                return redirect('addLote')
            return HttpResponseRedirect(reverse('addFinca'))
        except:
            messages.add_message(request, messages.WARNING, 'No se pudo crear el la finca')
    if context['isAdmin'] :
        context['productores']= Productor.objects.filter(estado=1).order_by('idProd')
    else:
        context['productores']= Productor.objects.filter(estado=1, organizacion=colab.org).order_by('idProd')
    context['paises']=Pais.objects.all().order_by('idPais')
    if context['isAdmin'] :
        context['departamentos']=Departamento.objects.all().order_by('idDpto')
    else:
        context['departamentos']=Departamento.objects.filter(fkPais=colab.org.ubicacion.fkdpto.fkPais).order_by('idDpto')
    context['ubicaciones']=Municipio.objects.all().order_by('idMun')
    context['comunidades']=Comunidad.objects.all().order_by('idCom')
    if context['isAdmin'] :
        context['fincas']=Finca.objects.filter(estado=1).order_by('idFinca')
    else:
        context['fincas']=Finca.objects.filter(estado=1, fkProd__organizacion=colab.org).order_by('idFinca')
    if request.session.get('prod') :
        context['productor']=Productor.objects.get(idProd=request.session.get('prod'))
        del request.session['prod']
    return render(request, 'registros/finca.html', context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def addLote(request):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()
    if request.method=="POST":
        try:
            f=Finca.objects.get(idFinca=request.POST.get('finca'))
            certs=request.POST.getlist('certs')
            vars=request.POST.getlist('vars')
            l=Lote(nameLote=request.POST.get('nameLote'), area=float(request.POST.get('areaLote')), altitud=float(request.POST.get('altitudLote')), fkFinca=f, unidad=f.unidad)
            l.save() 
            if certs:
                for c in certs:
                    a=Certificacion.objects.get(id=int(c))
                    l.fkCert.add(a)
            if vars:
                for v in vars:
                    b=Variedad.objects.get(id=int(v))
                    l.fkVar.add(b)
            l.save()
            return HttpResponseRedirect(reverse('addLote'))
        except:
            messages.add_message(request, messages.WARNING, 'No se pudo crear el lote')
    if context['isAdmin'] :
        context['productores']= Productor.objects.filter(estado=1).order_by('idProd')
    else:
        context['productores']= Productor.objects.filter(estado=1, organizacion=colab.org).order_by('idProd')
    if context['isAdmin'] :
        context['fincas']=Finca.objects.filter(estado=1).order_by('idFinca')
    else:
        context['fincas']=Finca.objects.filter(estado=1, fkProd__organizacion=colab.org).order_by('idFinca')
    if context['isAdmin'] :
        context['lotes']=Lote.objects.filter(estado=1).order_by('idLote')
    else:
        context['lotes']=Lote.objects.filter(estado=1, fkFinca__fkProd__organizacion=colab.org).order_by('idLote')
    context['certificaciones']=Certificacion.objects.all().order_by('id')
    context['variedades']=Variedad.objects.all().order_by('id')
    if request.session.get('finca') :
        context['finca']=Finca.objects.get(idFinca=request.session.get('finca'))
        del request.session['finca']
    return render(request, 'registros/lote.html', context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def updateProd(request):
    data={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    if request.method=="POST":
        try:
            p=Productor.objects.get(idProd=request.POST.get("idProd"))
            mun=Municipio.objects.get(idMun=request.POST.get('municipio'))
            #GENERATE CODE
            p.fkMun=mun            
            p.firstnameProd=request.POST.get("fname")
            p.lastnameProd=request.POST.get("lname")
            p.fechaNac=request.POST.get('fechaNac')
            p.codigoProd=request.POST.get('codprod')
            p.genero=request.POST.get('genero')
            p.save()
            data['dpto']=mun.fkdpto.nameDpto
            data['mun']=mun.nameMun
            data['status']=200
            data['mensaje']='Productor Actualizado'
        except:
            data['status']=000
            data['mensaje']='Error en la solicitud'
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def updateFinca(request):
    data={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    if request.method=="POST":
        try:
            f=Finca.objects.get(idFinca=request.POST.get('idFinca'))
            p=Productor.objects.get(idProd=request.POST.get("productor"))
            com=Comunidad.objects.get(idCom=request.POST.get('comunidad'))
            #GENERATE CODE
            f.fkProd=p
            f.fkCom=com      
            f.nameFinca=request.POST.get("nameFinca")
            f.area=float(request.POST.get('areaFinca'))
            f.save()
            data['dpto']= f.fkCom.fkMun.fkdpto.nameDpto
            data['munic']=f.fkCom.fkMun.nameMun
            data['com']=f.fkCom.nameCom
            data['status']=200
            data['mensaje']='Finca Actualizada'
        except:
            data['status']=000
            data['mensaje']='Error en la solicitud'
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def updateLote(request):
    data={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    if request.method=="POST":
        try:
            f=Finca.objects.get(idFinca=request.POST.get('finca'))
            certs=request.POST.getlist('certs')
            vars=request.POST.getlist('vars')
            l=Lote.objects.get(idLote=request.POST.get('idLote')) 
            l.fkFinca=f
            l.nameLote=request.POST.get('nameLote')
            l.area=float(request.POST.get('areaLote'))
            l.altitud=float(request.POST.get('altitudLote'))
            l.save()
            if certs:
                l.fkCert.clear()
                for c in certs:
                    a=Certificacion.objects.get(id=int(c))
                    l.fkCert.add(a)
            if vars:
                l.fkVar.clear()
                for v in vars:
                    b=Variedad.objects.get(id=int(v))
                    l.fkVar.add(b)
            l.save()
            certis=list()
            vari=list()
            if l.fkCert.all():
                for c in l.fkCert.all():
                    certis.append(c.nameCert)
            if l.fkVar.all():
                for v in l.fkVar.all():
                    vari.append(v.nameVariedad)
            data['certificaciones']=certis
            data['variedades']=vari
            data['status']=200
            data['mensaje']='Lote Actualizado'

        except:
            data['status']=000
            data['mensaje']='Error en la solicitud'
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def rmProd(request):
    data={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    if request.method=="POST" and (colab.is_siteadmin() or colab.is_boss()):
        try:
            p=Productor.objects.get(idProd=request.POST.get("idProd"))
            p.estado=0
            p.save()
            data['status']=200
            data['mensaje']='Productor Eliminado'
        except:
            data['status']=000
            data['mensaje']='Error en la solicitud'
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def rmFinca(request):
    data={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    if request.method=="POST" and (colab.is_siteadmin() or colab.is_boss()):
        try:
            f=Finca.objects.get(idFinca=request.POST.get("idFinca"))
            f.estado=0
            f.save()
            data['status']=200
            data['mensaje']='Finca Actualizada'
        except:
            data['status']=000
            data['mensaje']='Error en la solicitud'
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def rmLote(request):
    data={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    if request.method=="POST" and (colab.is_siteadmin() or colab.is_boss()):
        try:
            l=Lote.objects.get(idLote=request.POST.get("idLote"))
            l.estado=0
            l.save()
            data['status']=200
            data['mensaje']='Lote Actualizado'
        except:
            data['status']=000
            data['mensaje']='Error en la solicitud'
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def perfilMuestras(request):
    context={}
    context['departamentos']=Departamento.objects.all()
    context['certificaciones']=Certificacion.objects.all()
    context['organizaciones']=Organizacion.objects.all()
    context['procesos']=list(Procesado)
    context['sabores']=Sabor.objects.all()
    return render(request, 'registros/perfilMuestras.html', context=context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def getPerfilMuestras(request):
    data=dict()
    muestras=Muestra.objects.filter(estado__in=[1,6,10,11,12])
    if not User.objects.get(username=request.user).groups.filter(name='Administrador').exists():
        muestras=muestras.filter(fkLote__fkFinca__fkProd__organizacion=Colaborador.objects.get(usuario=request.user).org)
    if request.method == 'GET':
        if request.GET.get('org') and request.GET.get('org') != '':
            muestras=muestras.filter(fkLote__fkFinca__fkProd__organizacion__id_org=request.GET.get('org'))
        if request.GET.get('municipio') and request.GET.get('municipio') != '':
            muestras=muestras.filter(fkLote__fkFinca__fkProd__fkMun__idMun=request.GET.get('mun'))
        if request.GET.get('cert') and request.GET.get('cert') != '':
            certs=request.GET.get('cert').split('_')
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
    return JsonResponse(data, safe=False)

def getDefectos(muestra, tipo):
    defectos=list()
    if tipo == 1:
        for d in FisicoDefectoTI.objects.filter(fkFisico__fkMuestra=muestra, defectos__gt=0):
            defectos.append(d.fkDefecto.nameDefecto)
    elif tipo == 2:
        for d in FisicoDefectoTII.objects.filter(fkFisico__fkMuestra=muestra, defectos__gt=0):
            defectos.append(d.fkDefecto.nameDefecto)
    return defectos

def getAromas(muestra):
    s=Sensorial.objects.filter(fkMuestra=muestra)
    conciliacion= Conciliacion.objects.filter(fkCSensorial__fkMuestra= muestra)
    if conciliacion:
        for c in conciliacion:
            s=s.exclude(id=c.fkCSensorial.id)
        
    if s:
        a=s[0].aroma.all()
        return [aroma.nameAroma for aroma in a]

def getSabor(muestra):
    s=Sensorial.objects.filter(fkMuestra=muestra)
    conciliacion= Conciliacion.objects.filter(fkCSensorial__fkMuestra= muestra)
    if conciliacion:
        for c in conciliacion:
            s=s.exclude(id=c.fkCSensorial.id)
    if s:
        sabor=s[0].sabor.all()
        return [sab.nameSabor for sab in sabor]

def getSensorial(muestra):
    s=Sensorial.objects.filter(fkMuestra=muestra)
    conciliacion= Conciliacion.objects.filter(fkCSensorial__fkMuestra= muestra)
    if conciliacion:
        for c in conciliacion:
            s=s.exclude(id=c.fkCSensorial.id)
    if conciliacion:
        return conciliacion[0].fkCSensorial.pFinal
    else:
        if s:
            return s[0].pFinal
        else:
            return 0
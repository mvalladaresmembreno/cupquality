from django.shortcuts import render
from django.template import context
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import JsonResponse, HttpResponseRedirect
from analisis.models import *
from registros.models import *
from autenticacion.models import *
from django.urls import reverse
from django.utils import timezone


# Create your views here.

@login_required(login_url='/auth/login/', redirect_field_name='next')
def addMuestra(request):
    context={}
    data={}
    estadoM=0
    analisis=0
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    if request.method=="POST":
        try:
            procesoMuestra=request.POST.getlist('procesoMuestra')
            if len(procesoMuestra) == 1 and procesoMuestra[0] == "1" :
                estadoM=3
                analisis=1
            elif "2" in procesoMuestra:
                estadoM=2
                analisis=3
            elif "1" in procesoMuestra and "2" in procesoMuestra:
                estadoM=2
                analisis=3
            lote = Lote.objects.get(idLote=int(request.POST.get("lote")))
            m = Muestra(fkLote=lote, fechaEntrega=request.POST.get("fechaEntregado"), 
            peso=request.POST.get("pMuestra"),tipo=int(request.POST.get("tMuestra")),
            caracteristicas=request.POST.getlist("dEmbalaje"), rMuestra=int(request.POST.get("aceptacionMuestra")), 
            procesos=analisis, procesado=int(request.POST.get("procesadoMuestra")),ciclo=int(request.POST.get("cicloAgricola")),
            observaciones=request.POST.get("observaciones"), estado=estadoM, fkOrg=Organizacion.objects.get(id_org=colab.org.id_org),
            sedeRecepcion=Sede.objects.get(id_sede=request.POST.get("sRecepcion")))
            m.save()
            data['status']=200
            data['mensaje']='Muestra Agregada'
            return JsonResponse(data, safe=False)
        except:
            data['status']=000
            data['mensaje']='Error en la solicitud'
            return JsonResponse(data, safe=False)
    context["productores"] = Productor.objects.filter(estado=1, organizacion=Colaborador.objects.get(usuario=request.user).org).order_by("idProd")
    context["fincas"]=Finca.objects.filter(estado=1).order_by("idFinca")
    context['cooperativas']=Organizacion.objects.all().order_by('id_org')
    context['ciclos']=list(Ciclo)
    context['sedes']=Organizacion.objects.get(id_org=colab.org.id_org).sedes.all()
    return render(request, "analisis/registro.html", context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def analizeMuestra(request):
    context={}
    muestras=request.POST.getlist("aMuestra")
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()
    context["muestras"]=Muestra.objects.filter(idMuestra__in= muestras)
    context['catador']=user.first_name+" "+user.last_name
    context['contM']=[]
    cant=len(muestras)
    fisico=0
    sensorial=0
    for m in context["muestras"]:
        if (m.procesos == 1 and m.estado == 3) or (m.procesos == 1 and m.estado == 2) or (m.procesos == 3 and m.estado == 2) or (m.procesos == 3 and m.estado == 3) or (m.procesos == 2 and m.estado == 2):
            fisico+=1
        elif (m.procesos == 2 and m.estado == 4) or (m.procesos == 3 and m.estado == 4):
            sensorial+=1
        if fisico == cant:
            context['sedes']=Organizacion.objects.get(id_org=colab.org.id_org).sedes.all()
            return render(request, "analisis/fisico.html", context)
        elif sensorial == cant:
            for m in Muestra.objects.filter(idMuestra__in= muestras):
                context['contM'].append(m.idMuestra)
            return render(request, "analisis/sensorial.html", context)
    return HttpResponseRedirect(reverse('MuestraHome'))

@login_required(login_url='/auth/login/', redirect_field_name='next')
def index(request):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()
    context['muestrasFISICO']=list()
    context['muestrasSENSORIAL']=list()
    context['muestrasCONCILIACION']=list()
    m=Muestra.objects.filter(fkOrg=colab.org).order_by("idMuestra")
    for e in m:
        if (e.procesos == 1 and e.estado ==3) or (e.procesos == 3 and e.estado == 2) or (e.procesos == 3 and e.estado == 3) or (e.procesos == 2 and e.estado == 2):
            context["muestrasFISICO"].append(e)
        elif (e.procesos == 2 and e.estado == 4) or (e.procesos == 3 and e.estado == 4):
            context["muestrasSENSORIAL"].append(e)
        elif e.estado==5:
            context["muestrasCONCILIACION"].append(e)
    return render(request, "analisis/index.html", context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def editMuestra(request, idMuestra):
    context={}
    estadoM=int()
    analisis=int()
    data={}
    if request.method=='POST':
        try:
            procesoMuestra=request.POST.getlist('procesoMuestra')
            if len(procesoMuestra) == 1 and procesoMuestra[0] == "1" :
                estadoM=3
                analisis=1
            elif "2" in procesoMuestra:
                estadoM=2
                analisis=3
            elif "1" in procesoMuestra and "2" in procesoMuestra:
                estadoM=2
                analisis=3
            m=Muestra.objects.get(idMuestra=idMuestra)
            lote=Lote.objects.get(idLote=request.POST.get("lote"))
            m.fkLote=lote 
            m.fechaEntrega=request.POST.get("fechaEntregado")
            m.peso=request.POST.get("pMuestra")
            m.tipo=int(request.POST.get("tMuestra"))
            m.caracteristicas=request.POST.getlist("dEmbalaje")
            m.rMuestra=int(request.POST.get("aceptacionMuestra"))
            m.procesos=analisis
            m.procesado=int(request.POST.get("procesadoMuestra"))
            m.ciclo=int(request.POST.get("cicloAgricola"))
            m.observaciones=request.POST.get("observaciones")
            m.sedeRecepcion=Sede.objects.get(id_sede=request.POST.get("sRecepcion"))
            m.estado=estadoM
            m.save()
            data['status']=200
            data['mensaje']='Muestra editada'
            return JsonResponse(data, safe=False)
        except:
            data['status']=000
            data['mensaje']='Error en la solicitud'
            return JsonResponse(data, safe=False)
    try:
        m=Muestra.objects.get(idMuestra=idMuestra)
        context['sedes']=Organizacion.objects.get(id_org=m.fkOrg.id_org).sedes.all()
        context["muestra"]=m
        context["productores"] = Productor.objects.filter(estado=1).order_by("idProd")
        context["fincas"]=Finca.objects.filter(estado=1).order_by("idFinca")
        context['fecha']=Muestra.objects.get(idMuestra=idMuestra).fechaEntrega.strftime("%Y-%m-%d")
        context['ciclos']=list(Ciclo)
        context['caracteristicas']=str(m.caracteristicas)
    except:
        messages.add_message(request, messages.WARNING, 'No se encontro la muestra')
        return HttpResponseRedirect(reverse('MuestraHome'))
    return render(request, "analisis/editar.html", context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def rmMuestra(request, idMuestra):
    data={}
    try:
        m=Muestra.objects.get(idMuestra=idMuestra)
        m.estado=7
        m.save()
        data['status']=200
        data['mensaje']='Muestra eliminada'
        return JsonResponse(data, safe=False)
    except:
        data['status']=000
        data['mensaje']='Error en la solicitud'
        return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def saveFisico(request):
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    data={}
    if request.method=='POST':
        try:
            muestra=request.POST.get("idMuestra")
            m=Muestra.objects.get(idMuestra=muestra)
            m.sedeAnalisis=Sede.objects.get(id_sede=request.POST.get("sAnalisis"))
            f=Fisico(fkCatador=colab, fkMuestra=m, pDefectos=float(request.POST.get("pDefectos")), porDefectos=float(request.POST.get("porDefectos")), temp=float(request.POST.get("temp")), humedad=float(request.POST.get("PORhumedad")), pesoTotalTamiz=float(request.POST.get("PCtotal")), porTotalTamiz=float(request.POST.get("PORtotal")), pesoTamiz=float(request.POST.get('pesoTamiz')))
            f.save()
            if request.POST.get("rend"):
                f.rendimiento=float(request.POST.get("rend"))
                f.save()
            tamizados=Tamizado.objects.all()
            for e in tamizados:
                if request.POST.get(str(e.idTamizado)):
                    FisicoTamizado.objects.create(fkFisico=f, fkTamizado=e, pesoGranos=float(request.POST.get(e.idTamizado)), porGranos=float(request.POST.get("POR_"+e.idTamizado)))
            defectost1=DefectoT1.objects.all()
            defecetost2=DefectoT2.objects.all()
            for d in defectost1:
                if request.POST.get(str("E_"+d.idDefecto)):
                    FisicoDefectoTI.objects.create(fkFisico=f, fkDefecto=d, encontrados=float(request.POST.get(str("E_"+d.idDefecto))), defectos=float(request.POST.get(str("D_"+d.idDefecto))), pesoDefecto=float(request.POST.get(str("P_"+d.idDefecto))), porDefecto=float(request.POST.get(str("POR_"+d.idDefecto))))
            for d2 in defecetost2:
                if request.POST.get(str("E_"+d2.idDefecto)):
                    FisicoDefectoTII.objects.create(fkFisico=f, fkDefecto=d2, encontrados=float(request.POST.get(str("E_"+d2.idDefecto))), defectos=float(request.POST.get(str("D_"+d2.idDefecto))), pesoDefecto=float(request.POST.get(str("P_"+d2.idDefecto))), porDefecto=float(request.POST.get(str("POR_"+d2.idDefecto))))
            if (m.estado == 2 and m.procesos == 3) or (m.estado == 3 and m.procesos == 3) or (m.estado == 2 and m.procesos == 2):
                m.estado=4
            elif (m.procesos == 1 and m.estado ==3):
                m.estado=10
            m.save()
            data['status']=200
            data['mensaje']='Analisis Guardado'
            return JsonResponse(data, safe=False)
        except:
            data['status']=000
            data['mensaje']='Error en la solicitud'
            return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def saveSensorial(request):
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    data={}
    if request.method=='POST':
        try: 
            muestra=request.POST.get("idMuestra")
            m=Muestra.objects.get(idMuestra=muestra)
            s=Sensorial(fkCatador=colab, fkMuestra=m, 
            cAgua=float(request.POST.get("agua")),
            nTueste=int(request.POST.get("tueste")),
            fragancia=float(request.POST.get("fragancia")),
            seco=float(request.POST.get("seco")), 
            espuma=float(request.POST.get("espuma")),
            pSabor=float(request.POST.get("sabor")),
            pUniformidad=float(request.POST.get("pUniformidad")),
            cUniformidad=float(request.POST.get("cUniformidad")),
            pTLimpia=float(request.POST.get("pTLimpia")),
            cTLimpia=float(request.POST.get("cTLimpia")),
            pDulzor=float(request.POST.get("pDulzor")), 
            cDulzor=float(request.POST.get("cDulzor")),
            remanente=float(request.POST.get("remanente")), 
            acidez=float(request.POST.get("acidez")),
            iAcidez=float(request.POST.get("iacidez")),
            cuerpo=float(request.POST.get("cuerpo")),
            iCuerpo=float(request.POST.get("icuerpo")),
            balance=float(request.POST.get("balance")),
            comentario=request.POST.get("comentarios"), 
            pCatador=float(request.POST.get("pCatador")),
            castigo=float(request.POST.get("castigo")),
            pFinal=float(request.POST.get("pFinal"))
            )
            s.save()
            s.total()
            if not len(request.POST.get("aromas"))==0 :
                aromas=request.POST.get("aromas").split(",")
                for e in aromas:
                    a=Aroma.objects.get(idAroma=e)
                    s.aroma.add(a)
            s.save()
            if not len(request.POST.get("sabores"))==0 :
                sabores=request.POST.get("sabores").split(",")
                for e in sabores:
                    sa=Sabor.objects.get(idSabor=e)
                    s.sabor.add(sa)
            s.save()
            if request.POST.get('repetir'):
                if m.procesos == 3 or m.procesos == 2:
                    m.estado=4
                m.repetir=True
            elif request.POST.get('conciliar'):
                m.estado=5
            else:
                m.estado=1
            m.save()
            data['status']=200
            data['mensaje']='Analisis Guardado'
            return JsonResponse(data, safe=False)
        except:
            data['status']=000
            data['mensaje']='Error en la solicitud'
            return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def completados(request):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()
    context['muestrasCompletadas']=Muestra.objects.filter(fkOrg=colab.org, estado__in=[1,10,12]).order_by("idMuestra")
    context['muestrasConciliadas']=Muestra.objects.filter(fkOrg=colab.org, estado=6).order_by("idMuestra")
    return render(request, "analisis/completados.html", context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def completarAnalisis(request):
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    if request.method == "POST" :
        try:
            a=Analisis.objects.get(id=int(request.POST.get("idAnalisis")))
            a.estado=1
            a.save()
            if a.fkFisico.all():
                for f in a.fkFisico.all():
                    f=Muestra.objects.get(idMuestra=f.fkMuestra.idMuestra)
                    if f.analizado == 2:
                        f.analizado = 1
                        f.estado=1
                        f.save()
            if a.fkSensorial.all():
                for s in a.fkSensorial.all():
                    s=Muestra.objects.get(idMuestra=s.fkMuestra.idMuestra)
                    if s.analizado == 2:
                        s.analizado = 1
                        s.estado=1
                        s.save()
            messages.add_message(request, messages.SUCCESS, 'Analisis marcado como listo.')
        except:
            messages.add_message(request, messages.WARNING, 'No se pudo completar el análisis.')
            return HttpResponseRedirect(reverse('homeAnalisis'))
    return HttpResponseRedirect(reverse('verResultados' , args=[int(request.POST.get("idAnalisis"))]))

@login_required(login_url='/auth/login/', redirect_field_name='next')
def conciliar(request, muestra):
    context={}
    data={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    if Conciliacion.objects.filter(fkCSensorial__fkMuestra__idMuestra=int(muestra)) :
        return HttpResponseRedirect(reverse('verResultados' , args=[muestra]))
    else:
        if request.method == "POST":
            try:
                m=Muestra.objects.get(idMuestra=int(request.POST.get("idMuestra")))
                s=Sensorial(fkCatador=Colaborador.objects.get(usuario__email="soporteict@solidaridadnetwork.org"), fkMuestra=m, balance=float(request.POST.get("balance")),
                pDulzor=float(request.POST.get("dulzor")), cTLimpia=float(request.POST.get("tLimpia")),
                remanente=float(request.POST.get("remanente")), acidez=float(request.POST.get("acidez")), 
                cuerpo=float(request.POST.get("cuerpo")),
                iCuerpo=int(request.POST.get("intensidad")), pUniformidad=float(request.POST.get("uniformidad")),
                pCatador=float(request.POST.get("pSensorial")), fragancia=float(request.POST.get("aroma")), 
                pSabor=float(request.POST.get("sabor")))
                s.save()
                s.total()
                Conciliacion.objects.create(fkCSensorial=s,estado=6)
                if m.estado==5:
                    m.estado=6
                    m.save()
                data['status']=200
                data['mensaje']='Conciliación exitosa'
                return JsonResponse(data, safe=False)
            except Exception as e:
                data['status']=000
                data['mensaje']='Error en la solicitud'
                return JsonResponse(data, safe=False)

        context['tittle']='Conciliación - Muestra: '+str(muestra)
        context['sensoriales']=Sensorial.objects.filter(fkMuestra=muestra).order_by("creation_date")
        context['muestra']=muestra
        return render(request, "analisis/conciliacion.html", context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def verPuntaje(request, idMuestra):
    context={}
    context['sensorial']=list()
    con=Conciliacion.objects.get(fkCSensorial__fkMuestra__idMuestra=idMuestra)
    senso=Sensorial.objects.get(id=con.fkCSensorial.id)
    context["conciliacion"]=(senso)
    context['tecnico']= con.fkCSensorial.fkCatador
    context['muestra']= idMuestra
    s=Sensorial.objects.filter(fkMuestra__idMuestra=idMuestra)
    if s:
        for s in s:
            if not s == con.fkCSensorial:
                context['sensorial'].append(s)
    return render(request, "analisis/verPuntaje.html", context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def pendientesConciliacion(request):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()
    analisis=Conciliacion.objects.all().order_by("-id")
    if colab.is_siteadmin() or colab.is_boss():
        analisis=Conciliacion.objects.all().order_by("-id")
    else:
        analisis= Conciliacion.objects.filter(fkAnalisis__fkMuestra__fkCooperativa=colab.cooperativa).order_by("-id").distinct()
    context['analisis']=analisis
    return render(request, "analisis/homeConciliacion.html", context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def verMuestras(request):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()
    muestras=request.POST.getlist("vMuestra")
    context["muestras"]=Muestra.objects.filter(idMuestra__in= muestras)
    context["fisicos"]=list()
    context["sensoriales"]=list()
    context['tazasList']=[1,2,3,4,5]
    for m in context['muestras']:
        f=Fisico.objects.filter(fkMuestra=m).latest('creation_date')
        if f:
            context["fisicos"].append(f)
        s=Sensorial.objects.filter(fkMuestra=m)
        if s:
            for s in s:
                if s not in Conciliacion.objects.filter(fkCSensorial__fkMuestra=s.fkMuestra):
                    context["sensoriales"].append(s)
    return render(request, "analisis/verResultados.html", context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def impresion(request, idMuestra):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()
    muestra=Muestra.objects.get(idMuestra = idMuestra)
    context['tazasList']=[1,2,3,4,5]
    f=Fisico.objects.filter(fkMuestra=muestra).latest('creation_date')
    if f:
        context["f"]=f
    s=Sensorial.objects.filter(fkMuestra=muestra)
    if s:
        for s in s:
            if s not in Conciliacion.objects.filter(fkCSensorial__fkMuestra=s.fkMuestra):
                context["s"]=s
    return render(request, "analisis/impresionResultados.html", context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def impresionProd(request, idMuestra):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()
    muestra=Muestra.objects.get(idMuestra = idMuestra)
    def1=FisicoDefectoTI.objects.filter(fkFisico__fkMuestra=muestra, defectos__gt=0).values('fkDefecto__nameDefecto')
    def2=FisicoDefectoTII.objects.filter(fkFisico__fkMuestra=muestra, defectos__gt=0).values('fkDefecto__nameDefecto')
    context['defectos']=list()
    if def1:
        for d in def1:
            context['defectos'].append(d['fkDefecto__nameDefecto'])
    if def2:
        for d in def2:
            context['defectos'].append(d['fkDefecto__nameDefecto'])
    f=Fisico.objects.filter(fkMuestra=muestra).latest('creation_date')
    if f:
        context["f"]=f
    s=Sensorial.objects.filter(fkMuestra=muestra)
    if s:
        for s in s:
            if s not in Conciliacion.objects.filter(fkCSensorial__fkMuestra=s.fkMuestra):
                context["s"]=s
    return render(request, "analisis/impresionProductores.html", context)
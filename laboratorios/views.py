from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from laboratorios.models import *
from autenticacion.models import *
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count, Avg, Q, Max, Min
from django.http.response import JsonResponse, HttpResponseRedirect
# Create your views here.
@login_required(login_url='/auth/login/', redirect_field_name='next')
def index(request):
    context={}
    context['procesos']=list(Procesado)
    context['ciclos']=list(Ciclo)
    context['codigoPais']=Muestra.objects.all().values("codigoPais").distinct()
    context['codigoExportador']=Muestra.objects.all().values("exportador").distinct()
    context['codigoLote']=Muestra.objects.all().values("lote").distinct()
    context['sabores']=Sabor.objects.all()
    return render(request, 'laboratorios/index.html', context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def filtros(request):
    muestras=Muestra.objects.filter(estado__in=[1,6,10,11,12], fkOrg=Colaborador.objects.get(usuario= request.user).org)
    if request.method == 'GET':
        if request.GET.get('cPais') and request.GET.get('cPais') != '':
            muestras=muestras.filter(codigoPais=request.GET.get('cPais'))
        if request.GET.get('cExportador') and request.GET.get('cExportador') != '':
            muestras=muestras.filter(exportador=request.GET.get('cExportador'))
        if request.GET.get('cLote') and request.GET.get('cLote') != '':
            muestras=muestras.filter(lote=request.GET.get('cLote'))
        if request.GET.get('cAgricola') and request.GET.get('cAgricola') != '':
            muestras=muestras.filter(ciclo=request.GET.get('cAgricola'))
        if request.GET.get('procesos') and request.GET.get('procesos') != '':
            muestras=muestras.filter(Procesado=request.GET.get('procesos'))
        if request.GET.get('sabores') and request.GET.get('sabores') != '':
            sab=request.GET.get('sabores').split('_')
            muestras=muestras.filter(LSensorial__sabor__in=sab)
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
            m = Muestra(ordenTrabajo=request.POST.get("ordenTrabajo"),
            fechaEntrega=request.POST.get("fechaEntregado"),
            codigoPais=request.POST.get("codigoPais"),
            exportador=request.POST.get("exportador"),
            lote=request.POST.get("lote"), 
            peso=request.POST.get("pMuestra"), tipo=int(request.POST.get("tMuestra")),
            caracteristicas=request.POST.getlist("dEmbalaje"), rMuestra=int(request.POST.get("aceptacionMuestra")), 
            procesos=analisis, procesado=int(request.POST.get("procesadoMuestra")),ciclo=int(request.POST.get("cicloAgricola")),
            observaciones=request.POST.get("observaciones"),estado=estadoM, fkOrg=Organizacion.objects.get(id_org=colab.org.id_org),
            sedeRecepcion=Sede.objects.get(id_sede=request.POST.get("sRecepcion")))
            m.save()
            data['status']=200
            data['mensaje']='Muestra Agregada'
            return JsonResponse(data, safe=False)
        except:
            data['status']=000
            data['mensaje']='Error en la solicitud'
            return JsonResponse(data, safe=False)
    context['ciclos']=list(Ciclo)
    context['sedes']=Organizacion.objects.get(id_org=colab.org.id_org).sedes.all()
    return render(request, 'laboratorios/addMuestra.html', context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def verMuestras(request):
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
    return render(request, 'laboratorios/verMuestra.html', context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def editMuestra(request, idMuestra):
    context={}
    estadoM=0
    analisis=0
    data={}
    if request.method=='POST':
        try:
            procesoMuestra=request.POST.getlist('procesoMuestra')
            print(procesoMuestra)
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
            m.ordenTrabajo=request.POST.get("ordenTrabajo")
            m.fechaEntrega=request.POST.get("fechaEntregado")
            m.codigoPais=request.POST.get("codigoPais")
            m.exportador=request.POST.get("exportador")
            m.lote=request.POST.get("lote")
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
        context["muestra"]=m
        context['sedes']=Organizacion.objects.get(id_org=m.fkOrg.id_org).sedes.all()
        context['fecha']=Muestra.objects.get(idMuestra=idMuestra).fechaEntrega.strftime("%Y-%m-%d")
        context['ciclos']=list(Ciclo)
        context['caracteristicas']=str(m.caracteristicas)
    except:
        messages.add_message(request, messages.WARNING, 'No se encontro la muestra')
        return HttpResponseRedirect(reverse('verMuestrasLab'))
    return render(request, 'laboratorios/editMuestra.html', context)

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
            return render(request, "laboratorios/fisico.html", context)
        elif sensorial == cant:
            for m in Muestra.objects.filter(idMuestra__in= muestras):
                context['contM'].append(m.idMuestra)
            return render(request, "laboratorios/sensorial.html", context)
    return HttpResponseRedirect(reverse('verMuestrasLab'))

@login_required(login_url='/auth/login/', redirect_field_name='next')
def saveFisico(request):
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    data={}
    if request.method=='POST':
        try:
            muestra=request.POST.get("idMuestra")
            m=Muestra.objects.get(idMuestra=muestra)
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
            defectost2=DefectoT2.objects.all()
            for d in defectost1:
                if request.POST.get(str("E_"+d.idDefecto)):
                    FisicoDefectoTI.objects.create(fkFisico=f, fkDefecto=d, encontrados=float(request.POST.get(str("E_"+d.idDefecto))), defectos=float(request.POST.get(str("D_"+d.idDefecto))), pesoDefecto=float(request.POST.get(str("P_"+d.idDefecto))), porDefecto=float(request.POST.get(str("POR_"+d.idDefecto))))
            for d2 in defectost2:
                if request.POST.get(str("E_"+d2.idDefecto)):
                    FisicoDefectoTII.objects.create(fkFisico=f, fkDefecto=d2, encontrados=float(request.POST.get(str("E_"+d2.idDefecto))), defectos=float(request.POST.get(str("D_"+d2.idDefecto))), pesoDefecto=float(request.POST.get(str("P_"+d2.idDefecto))), porDefecto=float(request.POST.get(str("POR_"+d2.idDefecto))))
            if (m.estado == 2 and m.procesos == 3) or (m.estado == 3 and m.procesos == 3) or (m.estado == 2 and m.procesos == 2):
                m.estado=4
            elif (m.procesos == 1 and m.estado ==3):
                m.estado=10
            m.sedeAnalisis=Sede.objects.get(id_sede=request.POST.get("sAnalisis"))
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
                if m.procesos == 1:
                    m.estado=3
                elif m.procesos == 3 or m.procesos == 2:
                    m.estado=3
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

#Impresion para laboratorio
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
    return render(request, "laboratorios/impresionResultadosLab.html", context)
    
@login_required(login_url='/auth/login/', redirect_field_name='next')
def completados(request):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()
    context['muestrasCompletadas']=Muestra.objects.filter(fkOrg=colab.org, estado__in=[1,10,12]).order_by("idMuestra")
    context['muestrasConciliadas']=Muestra.objects.filter(fkOrg=colab.org, estado=6).order_by("idMuestra")
    return render(request, "laboratorios/completados.html", context)

@login_required(login_url='/auth/login/', redirect_field_name='next')
def verResultado(request):
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
    return render(request, "laboratorios/verResultadosLab.html", context)
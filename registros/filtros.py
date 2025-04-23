from django.contrib.auth.models import User
from registros.models import Certificacion, Comunidad, Departamento, Finca, Lote, Municipio, Pais, Productor, Variedad
from autenticacion.models import Colaborador
from analisis.models import *
from django.db.models import Count, Avg, Q

def filtrar():
    context={}
    context['cRegistradas']=Muestra.objects.all().count()
    context['cCompletadas']=Analisis.objects.filter(estado=1).count()
    context['pAnalizar']=Analisis.objects.filter(estado=2).count()
    context['pConciliar']=Conciliacion.objects.filter(estado=2).count()
    context['analizadas']=Muestra.objects.filter(analizado=1)
    context['Sabor1']=list(Sabor.objects.annotate(total=Count('nameSabor')).order_by('nameSabor').filter(ASabor__sabor__nivelSabor=1, nivelSabor=1).values('nameSabor','total'))
    context['Sabor2']=list(Sabor.objects.annotate(total=Count('nameSabor')).order_by('nameSabor').filter(ASabor__sabor__nivelSabor=2, nivelSabor=2).values('nameSabor','total'))
    context['Sabor3']=list(Sabor.objects.annotate(total=Count('nameSabor')).order_by('nameSabor').filter(ASabor__sabor__nivelSabor=3, nivelSabor=3).values('nameSabor','total'))
    context['Aroma1']=list(Aroma.objects.annotate(total=Count('nameAroma')).order_by('nameAroma').filter(AAroma__aroma__nivelAroma=1, nivelAroma=1).values('nameAroma','total'))
    context['Aroma2']=list(Aroma.objects.annotate(total=Count('nameAroma')).order_by('nameAroma').filter(AAroma__aroma__nivelAroma=2, nivelAroma=2).values('nameAroma','total'))
    context['Aroma3']=list(Aroma.objects.annotate(total=Count('nameAroma')).order_by('nameAroma').filter(AAroma__aroma__nivelAroma=3, nivelAroma=3).values('nameAroma','total'))
    context['Aroma4']=list(Aroma.objects.annotate(total=Count('nameAroma')).order_by('nameAroma').filter(AAroma__aroma__nivelAroma=4, nivelAroma=4).values('nameAroma','total'))
    pDef=Fisico.objects.all().aggregate(Avg('pDefectos'))
    context['promDefectos']=pDef['pDefectos__avg']
    d1=DefectoT1.objects.filter(Defecto1Muestras__isnull=False).values('nameDefecto').annotate(cant=Count('idDefecto'))
    context['Defectos1']={'label': list(), 'data': list()}
    for d in d1:
        context['Defectos1']['label'].append(d['nameDefecto'])
        context['Defectos1']['data'].append(d['cant'])
    d2=DefectoT2.objects.filter(Defecto2Muestras__isnull=False).values('nameDefecto').annotate(cant=Count('idDefecto'))
    context['Defectos2']={'label': list(), 'data': list()}
    for e in d2:
        context['Defectos2']['label'].append(e['nameDefecto'])
        context['Defectos2']['data'].append(e['cant'])
    rangos=Conciliacion.objects.filter(estado=1).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['puntajesFinales']={
        '0,69.99': rangos['Rango1'],
        '70.00,80.99': rangos['Rango2'],
        '80.99,83.99': rangos['Rango3'],
        '84.00,85.99': rangos['Rango4'],
    }
    Alt1=Conciliacion.objects.filter(estado=1, fkCSensorial__fkMuestra__fkLote__altitud__range=[800,1000]).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['alt1']={
        '0,69.99': Alt1['Rango1'],
        '70.00,80.99': Alt1['Rango2'],
        '80.99,83.99': Alt1['Rango3'],
        '80.99,83.99': Alt1['Rango3'],
        '84.00,85.99': Alt1['Rango4'],
    }
    Alt2=Conciliacion.objects.filter(estado=1, fkCSensorial__fkMuestra__fkLote__altitud__range=[1001,1200]).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['alt2']={
        '0,69.99': Alt2['Rango1'],
        '70.00,80.99': Alt2['Rango2'],
        '80.99,83.99': Alt2['Rango3'],
        '80.99,83.99': Alt2['Rango4'],
        '84.00,85.99': Alt2['Rango5'],
    }
    Alt3=Conciliacion.objects.filter(estado=1, fkCSensorial__fkMuestra__fkLote__altitud__range=[1201,1500]).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['alt3']={
        '0,69.99': Alt3['Rango1'],
        '70.00,80.99': Alt3['Rango2'],
        '80.99,83.99': Alt3['Rango3'],
        '80.99,83.99': Alt3['Rango4'],
        '84.00,85.99': Alt3['Rango5'],
    }
    Alt4=Conciliacion.objects.filter(estado=1, fkCSensorial__fkMuestra__fkLote__altitud__gte=1500).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['alt4']={
        '0,69.99': Alt4['Rango1'],
        '70.00,80.99': Alt4['Rango2'],
        '80.99,83.99': Alt4['Rango3'],
        '80.99,83.99': Alt4['Rango4'],
        '84.00,85.99': Alt4['Rango5'],
    }
    context['tueste']={'label':list(), 'data':list()}
    tueste=Sensorial.objects.values("nTueste").annotate(cant=Count('id'))
    for t in tueste:
        for tn in TUESTE:
            if t['nTueste']==tn[0]:
                context['tueste']['label'].append(tn[1])
                context['tueste']['data'].append(t['cant'])
    return context

def generales(cooperativa): 
    print(cooperativa)
    context={}
    context['cRegistradas']=Muestra.objects.filter(fkLote__fkFinca__fkProd__cooperativa=cooperativa).count()
    context['cCompletadas']=Analisis.objects.filter(fkSensorial__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop,estado=1).count()
    context['pAnalizar']=Analisis.objects.filter(fkSensorial__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop, estado=2).count()
    context['pConciliar']=Conciliacion.objects.filter(fkCSensorial__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop,estado=2).count()
    context['analizadas']=Muestra.objects.filter(fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop, analizado=1).count()
    context['Sabor1']=list(Sabor.objects.annotate(total=Count('nameSabor')).order_by('nameSabor').filter(ASabor__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop, ASabor__sabor__nivelSabor=1, nivelSabor=1).values('nameSabor','total'))
    context['Sabor2']=list(Sabor.objects.annotate(total=Count('nameSabor')).order_by('nameSabor').filter(ASabor__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop, ASabor__sabor__nivelSabor=2, nivelSabor=2).values('nameSabor','total'))
    context['Sabor3']=list(Sabor.objects.annotate(total=Count('nameSabor')).order_by('nameSabor').filter(ASabor__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop, ASabor__sabor__nivelSabor=3, nivelSabor=3).values('nameSabor','total'))
    context['Aroma1']=list(Aroma.objects.annotate(total=Count('nameAroma')).order_by('nameAroma').filter(AAroma__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop,AAroma__aroma__nivelAroma=1, nivelAroma=1).values('nameAroma','total'))
    context['Aroma2']=list(Aroma.objects.annotate(total=Count('nameAroma')).order_by('nameAroma').filter(AAroma__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop,AAroma__aroma__nivelAroma=2, nivelAroma=2).values('nameAroma','total'))
    context['Aroma3']=list(Aroma.objects.annotate(total=Count('nameAroma')).order_by('nameAroma').filter(AAroma__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop,AAroma__aroma__nivelAroma=3, nivelAroma=3).values('nameAroma','total'))
    context['Aroma4']=list(Aroma.objects.annotate(total=Count('nameAroma')).order_by('nameAroma').filter(AAroma__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop,AAroma__aroma__nivelAroma=4, nivelAroma=4).values('nameAroma','total'))
    pDef=Fisico.objects.filter(fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop).aggregate(Avg('pDefectos'))
    context['promDefectos']=pDef['pDefectos__avg']
    d1=DefectoT1.objects.filter(Defecto1Muestras__isnull=False, Defecto1Muestras__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop).values('nameDefecto').annotate(cant=Count('idDefecto'))
    context['Defectos1']={'label': list(), 'data': list()}
    for d in d1:
        context['Defectos1']['label'].append(d['nameDefecto'])
        context['Defectos1']['data'].append(d['cant'])
    d2=DefectoT2.objects.filter(Defecto2Muestras__isnull=False, Defecto2Muestras__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop).values('nameDefecto').annotate(cant=Count('idDefecto'))
    context['Defectos2']={'label': list(), 'data': list()}
    for e in d2:
        context['Defectos2']['label'].append(e['nameDefecto'])
        context['Defectos2']['data'].append(e['cant'])
    rangos=Conciliacion.objects.filter(fkCSensorial__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop, estado=1).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['puntajesFinales']={
        '0,69.99': rangos['Rango1'],
        '70.00,80.99': rangos['Rango2'],
        '80.99,83.99': rangos['Rango3'],
        '84.00,85.99': rangos['Rango4'],
    }
    Alt1=Conciliacion.objects.filter(estado=1, fkCSensorial__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop, fkCSensorial__fkMuestra__fkLote__altitud__range=[800,1000]).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['alt1']={
        '0,69.99': Alt1['Rango1'],
        '70.00,80.99': Alt1['Rango2'],
        '80.99,83.99': Alt1['Rango3'],
        '80.99,83.99': Alt1['Rango4'],
        '84.00,85.99': Alt1['Rango5'],
    }
    Alt2=Conciliacion.objects.filter(estado=1,fkCSensorial__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop,  fkCSensorial__fkMuestra__fkLote__altitud__range=[1001,1200]).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['alt2']={
        '0,69.99': Alt2['Rango1'],
        '70.00,80.99': Alt2['Rango2'],
        '80.99,83.99': Alt2['Rango3'],
        '80.99,83.99': Alt2['Rango4'],
        '84.00,85.99': Alt2['Rango5'],
    }
    Alt3=Conciliacion.objects.filter(fkCSensorial__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop, estado=1, fkCSensorial__fkMuestra__fkLote__altitud__range=[1201,1500]).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['alt3']={
        '0,69.99': Alt3['Rango1'],
        '70.00,80.99': Alt3['Rango2'],
        '80.99,83.99': Alt3['Rango3'],
        '80.99,83.99': Alt3['Rango4'],
        '84.00,85.99': Alt3['Rango5'],
    }
    Alt4=Conciliacion.objects.filter(fkCSensorial__fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop, estado=1, fkCSensorial__fkMuestra__fkLote__altitud__gte=1500).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['alt4']={
        '0,69.99': Alt4['Rango1'],
        '70.00,80.99': Alt4['Rango2'],
        '80.99,83.99': Alt4['Rango3'],
        '80.99,83.99': Alt4['Rango4'],
        '84.00,85.99': Alt4['Rango5'],
    }

    context['tueste']={'label':list(), 'data':list()}
    tueste=Sensorial.objects.filter(fkMuestra__fkLote__fkFinca__fkProd__cooperativa__id_coop=cooperativa.id_coop).values("nTueste").annotate(cant=Count('id'))
    for t in tueste:
        for tn in TUESTE:
            if t['nTueste']==tn[0]:
                context['tueste']['label'].append(tn[1])
                context['tueste']['data'].append(t['cant'])
    return context


def adminStats():
    context={}
    context['cRegistradas']=Muestra.objects.all().count()
    context['cCompletadas']=Analisis.objects.filter(estado=1).count()
    context['pAnalizar']=Analisis.objects.filter(estado=2).count()
    context['pConciliar']=Conciliacion.objects.filter(estado=2).count()
    context['analizadas']=Muestra.objects.filter(analizado=1).count()
    context['Sabor1']=list(Sabor.objects.annotate(total=Count('nameSabor')).order_by('nameSabor').filter(ASabor__sabor__nivelSabor=1, nivelSabor=1).values('nameSabor','total'))
    context['Sabor2']=list(Sabor.objects.annotate(total=Count('nameSabor')).order_by('nameSabor').filter(ASabor__sabor__nivelSabor=2, nivelSabor=2).values('nameSabor','total'))
    context['Sabor3']=list(Sabor.objects.annotate(total=Count('nameSabor')).order_by('nameSabor').filter(ASabor__sabor__nivelSabor=3, nivelSabor=3).values('nameSabor','total'))
    context['Aroma1']=list(Aroma.objects.annotate(total=Count('nameAroma')).order_by('nameAroma').filter(AAroma__aroma__nivelAroma=1, nivelAroma=1).values('nameAroma','total'))
    context['Aroma2']=list(Aroma.objects.annotate(total=Count('nameAroma')).order_by('nameAroma').filter(AAroma__aroma__nivelAroma=2, nivelAroma=2).values('nameAroma','total'))
    context['Aroma3']=list(Aroma.objects.annotate(total=Count('nameAroma')).order_by('nameAroma').filter(AAroma__aroma__nivelAroma=3, nivelAroma=3).values('nameAroma','total'))
    context['Aroma4']=list(Aroma.objects.annotate(total=Count('nameAroma')).order_by('nameAroma').filter(AAroma__aroma__nivelAroma=4, nivelAroma=4).values('nameAroma','total'))
    pDef=Fisico.objects.all().aggregate(Avg('pDefectos'))
    context['promDefectos']=pDef['pDefectos__avg']
    d1=DefectoT1.objects.filter(Defecto1Muestras__isnull=False).values('nameDefecto').annotate(cant=Count('idDefecto'))
    context['Defectos1']={'label': list(), 'data': list()}
    for d in d1:
        context['Defectos1']['label'].append(d['nameDefecto'])
        context['Defectos1']['data'].append(d['cant'])
    d2=DefectoT2.objects.filter(Defecto2Muestras__isnull=False).values('nameDefecto').annotate(cant=Count('idDefecto'))
    context['Defectos2']={'label': list(), 'data': list()}
    for e in d2:
        context['Defectos2']['label'].append(e['nameDefecto'])
        context['Defectos2']['data'].append(e['cant'])
    rangos=Conciliacion.objects.filter(estado=1).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['puntajesFinales']={
        '0,69.99': rangos['Rango1'],
        '70.00,80.99': rangos['Rango2'],
        '80.99,83.99': rangos['Rango3'],
        '84.00,85.99': rangos['Rango4'],
    }
    Alt1=Conciliacion.objects.filter(estado=1, fkCSensorial__fkMuestra__fkLote__altitud__range=[800,1000]).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['alt1']={
        '0,69.99': Alt1['Rango1'],
        '70.00,80.99': Alt1['Rango2'],
        '80.99,83.99': Alt1['Rango3'],
        '80.99,83.99': Alt1['Rango4'],
        '84.00,85.99': Alt1['Rango5'],
    }
    Alt2=Conciliacion.objects.filter(estado=1, fkCSensorial__fkMuestra__fkLote__altitud__range=[1001,1200]).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['alt2']={
        '0,69.99': Alt2['Rango1'],
        '70.00,80.99': Alt2['Rango2'],
        '80.99,83.99': Alt2['Rango3'],
        '80.99,83.99': Alt2['Rango4'],
        '84.00,85.99': Alt2['Rango5'],
    }
    Alt3=Conciliacion.objects.filter(estado=1, fkCSensorial__fkMuestra__fkLote__altitud__range=[1201,1500]).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['alt3']={
        '0,69.99': Alt3['Rango1'],
        '70.00,80.99': Alt3['Rango2'],
        '80.99,83.99': Alt3['Rango3'],
        '80.99,83.99': Alt3['Rango4'],
        '84.00,85.99': Alt3['Rango5'],
    }
    Alt4=Conciliacion.objects.filter(estado=1, fkCSensorial__fkMuestra__fkLote__altitud__gte=1500).aggregate(
    Rango1=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[0,69.99]))),
    Rango2=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[70.00,80.99]))),
    Rango3=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[80.99,83.99]))),
    Rango4=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[84.00,85.99]))),
    Rango5=(Count('id', filter=Q(fkCSensorial__pPromedio__range=[85.99,100.00]))))
    context['alt4']={
        '0,69.99': Alt4['Rango1'],
        '70.00,80.99': Alt4['Rango2'],
        '80.99,83.99': Alt4['Rango3'],
        '80.99,83.99': Alt4['Rango4'],
        '84.00,85.99': Alt4['Rango5'],
    }

    context['tueste']={'label':list(), 'data':list()}
    tueste=Sensorial.objects.values("nTueste").annotate(cant=Count('id'))
    for t in tueste:
        for tn in TUESTE:
            if t['nTueste']==tn[0]:
                context['tueste']['label'].append(tn[1])
                context['tueste']['data'].append(t['cant'])
    return context
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import *
from django.http.response import JsonResponse
from django.contrib import messages
from .forms import *
from django.core.mail import EmailMultiAlternatives, mail_admins
from django.template.loader import get_template
# Create your views here.

def iniciar_sesion(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        try:
            username=User.objects.get(email=username).username
            colab=Colaborador.objects.get(usuario__username=username)
        except:
            return render(request,'registration/login.html', context={'error':'El usuario no existe'})
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.groups.filter(name="Laboratorio").exists() and user.groups.filter(name="Jefe").exists():
                    return HttpResponseRedirect('/lab')
                elif user.groups.filter(name="Laboratorio").exists() and user.groups.filter(name="Digitador").exists():
                    return HttpResponseRedirect('/lab/addMuestraLab')
                elif user.groups.filter(name="Laboratorio").exists() and user.groups.filter(name="Tecnico").exists():
                    return HttpResponseRedirect('/lab/verMuestrasLab')
                #INICIA VERIFICACION DE TIPO DE COOPERATIVA
                if user.groups.filter(name="Cooperativa").exists() and user.groups.filter(name="Jefe").exists():
                    return HttpResponseRedirect('/')
                elif user.groups.filter(name="Cooperativa").exists() and user.groups.filter(name="Digitador").exists():
                    return HttpResponseRedirect('/muestras/addMuestra')
                elif user.groups.filter(name="Cooperativa").exists() and user.groups.filter(name="Tecnico").exists():
                    return HttpResponseRedirect('/muestras/verMuestras')
                return HttpResponseRedirect('/')
        else: 
            return render(request,'registration/login.html', context={'error':'Credenciales Incorrectas. Intente de Nuevo.'})
    return render(request,'registration/login.html', context={'LOGIN':True})

def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/auth/login')

@login_required(login_url='/auth/login', redirect_field_name='next')
def crear_usuario(request):
    data={}
    context={}  
    if request.POST:
        context['name'] = name=request.POST['name']
        context['lastname'] = lastname=request.POST['lastname']
        context['usuario'] = femail = request.POST['email']
        cooperativa=request.POST['org']
        context['contrasena'] = password=request.POST['passwordc']
        context['org'] = Organizacion.objects.get(id_org=cooperativa).name_org
        context['roles'] =  request.POST.getlist('roles')
        username=femail.split("@")[0]
        username=username.lower()
        if not User.objects.filter(email=femail).exists():
            try:
                u=User.objects.create_user(first_name=name,last_name=lastname,username=username,email=femail,password=password)
                u.save()
                e=Colaborador(usuario=User.objects.get(id=u.id),org=Organizacion.objects.get(id_org=cooperativa))
                e.save()
                for g in request.POST.getlist('roles'):
                    u.groups.add(Group.objects.get(id=int(g)))
                try:
                    username=User.objects.get(email=femail).username
                    data['success']=True
                    data["mensaje"]="Usuario creado correctamente."
                    enviardatosUser(context,femail)
                    messages.add_message(request, messages.SUCCESS, 'Usuario creado con exito')
                except:
                    data['success']=False
                    data["mensaje"]="El Usuario no existe."
            except:
                data['success']=False
                data["mensaje"]="Hubo un problema con las credenciales, intentalo de nuevo."
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login', redirect_field_name='next')
def ver_usuario(request):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()  
    context['usuario']=Colaborador.objects.get(usuario=request.user)
    return render(request, 'registration/user.html', context)

@login_required(login_url='/auth/login', redirect_field_name='next')
def userAdmin(request):
    context={}
    user=User.objects.get(id=request.user.id)
    colab=Colaborador.objects.get(usuario = user)
    context['isAdmin']=colab.is_siteadmin()
    context['isBoss']=colab.is_boss()  
    context['usuarios']=Colaborador.objects.all().order_by('usuario__username')
    context['organizaciones']=Organizacion.objects.all()
    context['roles']=Group.objects.all()
    return render(request, 'registration/userAdmin.html', context)

@login_required(login_url='/auth/login', redirect_field_name='next')
def userAdminEdit(request):
    data={}
    try:
        if request.POST:
            user=User.objects.get(id=request.POST.get('id'))
            colab=Colaborador.objects.get(usuario = user)
            colab.org=Organizacion.objects.get(id_org=request.POST['org'])
            colab.save()
            user.first_name=request.POST['names']
            user.last_name=request.POST['lastnames']
            user.email=request.POST['email']
            user.save()
            user.groups.clear()
            user.save()
            for g in request.POST.getlist('roles'):
                user.groups.add(Group.objects.get(id=int(g)))
        data['success']=True
        data['mensaje']="Usuario actualizado correctamente"
        messages.add_message(request, messages.SUCCESS, 'Usuario actualizado correctamente')
    except:
        data['success']=False
        data['mensaje']="Hubo un problema al actualizar el usuario"
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login', redirect_field_name='next')
def userAdminDelete(request):
    data={}
    try:
        user=User.objects.get(id=request.POST.get('id'))
        if user.is_active:
            user.is_active=False
            user.save()
        data['success']=True
        data['mensaje']="Usuario eliminado correctamente"
        messages.add_message(request, messages.SUCCESS, 'Usuario eliminado correctamente')
    except:
        data['success']=False
        data['mensaje']="Hubo un problema al eliminar el usuario"
    return JsonResponse(data, safe=False)

@login_required(login_url='/auth/login', redirect_field_name='next')
def userAdminActivate(request):
    data={}
    try:
        user=User.objects.get(id=request.POST.get('id'))
        if not user.is_active:
            user.is_active=True
            user.save()
        data['success']=True
        data['mensaje']="Usuario activado correctamente"
        messages.add_message(request, messages.SUCCESS, 'Usuario activado correctamente')
    except:
        data['success']=False
        data['mensaje']="Hubo un problema al activar el usuario"
    return JsonResponse(data, safe=False)

def enviardatosUser(context, femail):
        asunto, de, para,= 'Bienvenido a la Plataforma Calidad de Taza', 'soporteict@solidaridadnetwork.org', femail
        mensaje=get_template('emails/newuser.html').render(context)
        msg=EmailMultiAlternatives(subject=asunto,body=mensaje, from_email=de, to=[para], reply_to=[de])
        msg.content_subtype='html'
        msg.send()
        context['permisos']=[]
        for g in context['roles']:
            name=Group.objects.get(id=int(g)).name
            context['permisos'].append(name)
        content=get_template('emails/usernotifAdmin.html').render(context)
   #     adminmail=EmailMultiAlternatives(subject='Nuevo usuario creado en Calidad de Taza',body=content, from_email=de, to=settings.ADMINS, reply_to=[de])
    #    adminmail.content_subtype='html'
     #   adminmail.send()


        

@login_required(login_url='/auth/login', redirect_field_name='next')
def firma(request):
    context={}
    if request.POST:
        form=ColaboradorForm(request.POST, instance=Colaborador.objects.get(usuario=request.user))
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Firma creada con exito')
            return HttpResponseRedirect('/auth/perfil')
    context['firma']=ColaboradorForm(instance=Colaborador.objects.get(usuario=request.user))
    context['usuario']=Colaborador.objects.get(usuario=request.user)
    return render(request, 'registration/firma.html', context)
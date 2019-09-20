from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.models import User
from django.conf import settings
from filemanager import FileManager

import os
from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode
from django.shortcuts import redirect
import users.utils as utilities


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
#           create folder
            newpath = settings.MEDIA_ROOT + "/" + username
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            messages.success(request, f'Account created for {username}! You can login now')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def view(request, path):
    extensions = ['html','htm','zip','py,''css','js','jpeg','jpg','png','pdf','mp3']
    extensions.extend(list(map(str.upper,extensions))) # add capital extensions (niv)
    user = request.user
    users = User.objects.all()

    if path != '' and '$' in path:
        info = path.split('?')
        id1 = int(info[0])
        path = info[1]
        id2 = int(info[2])
        user = request.user
        users = User.objects.all()
    fm = FileManager(settings.MEDIA_ROOT+"/"+user.username, extensions=extensions)
    return fm.render(request,path,users)

@login_required
def viewimages(request, path):
    extensions = ['html','htm','zip','py,''css','js','jpeg','jpg','png','pdf','mp3']
    extensions.extend(list(map(str.upper,extensions))) # add capital extensions (niv)
    users = User.objects.all()

    fm = FileManager(settings.MEDIA_ROOT+"/", extensions=extensions)
    return fm.render(request,path,users)

@login_required
def viewshared(request,path=''):
    extensions = ['html','htm','zip','py,''css','js','jpeg','jpg','png','pdf','mp3']
    extensions.extend(list(map(str.upper,extensions))) # add capital extensions (niv)
    user = request.user
    users = User.objects.all()
    if 'temp' in request.session:
        data = request.session['temp']
    else:
        data = None
        dirname = ''
   # path1 = request.GET.get('path')
    if data != None:

        info = data.split('$')
        id1 = int(info[0])
        filepath = info[1]
        filename = filepath.split('/')[-1]
        dirname = filepath[0:len(filepath)-len(filename)]
        id2 = int(info[2])

        if user.id != id1 and user.id != id2:
            errorstring = 'no authorized user:'+user.username
            # response = redirect('/docs/errors')
            return render(request, 'users/error.html', {'errorstring': errorstring})


    #    path1 = path[0:len(path) - len(fName)]
    #else:
     #   path1 = ""

    user1 = users.get(id=id1)
    fm = FileManager(settings.MEDIA_ROOT+"/"+user1.username+"/"+dirname, extensions=extensions)
    fm.sharepath = dirname
    if path != '':
        mediaexist = False
    else:
        mediaexist = True
    return fm.render(request,filename,users,mediaexist)

@login_required
def generate(request,path,id):
    user2 = User.objects.get(id=int(id))
    link = "/docs/share/"+encryptLink(request.user.id, path, id)
    return render(request,'docs/sendshare.html',{'path':path,'user1':request.user,'user2':user2,'link':link})

@login_required
def share(request, link):
    extensions = ['html','htm','zip','py,''css','js','jpeg','jpg','png','pdf','mp3']

    extensions.extend(list(map(str.upper,extensions))) # add capital extensions (niv)


    linkinfo = decryptLink(link).decode()


    response = redirect('/docs/viewshared/')
    request.session['temp'] = linkinfo
    return response
    #fm = FileManager(settings.MEDIA_ROOT + "/" + user.username + "/", extensions=extensions)
    #return fm.render(request, path1, users)


def encryptLink(id1,path, id2):
# encrypt link
    total = str(id1) + "$" + path + "$" + id2
    encrypted_total = encrypt(settings.SECRET_KEY_ENCRYPT, total)
    encoded_encrypted_total = b64encode(encrypted_total)

    return encoded_encrypted_total.decode() # convert from b'string' to string

def decryptLink(str_encoded_encrypted):
    encoded_encrypted = str_encoded_encrypted.encode()
    decoded_encrypted = b64decode(encoded_encrypted)
    link = decrypt(settings.SECRET_KEY_ENCRYPT,decoded_encrypted)
    return link




@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


        context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


@login_required
def sharebyemail(request):
    email = request.GET['email']
    host = request.get_host()
    note = request.GET['note']
    link = host + request.GET['link']
    user = request.user
    response = utilities.sharelinkbyemail(request, user,email,link,note)

    return response



@login_required
def sharebysms(request):
    phone = request.GET['sms']
    if len(phone) == 11:
        phone = '+'+phone
    host = request.get_host()
    note = request.GET['note']
    link = host + request.GET['link']
    user = request.user

    response = utilities.sharelinkbysms(request, user, phone, link, note)
    return response
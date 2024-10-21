from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.contrib.auth.models import User
#from django.contrib.auth import logout

def post_edit(request, pk):
     post = get_object_or_404(Post, pk=pk)
     if request.method == "POST":
         form = PostForm(request.POST, instance=post)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.published_date = timezone.now()
             post.save()
             return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm(instance=post)
     return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
     if request.method == "POST":
         form = PostForm(request.POST)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.published_date = timezone.now()
             post.save()
             return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm()
     return render(request, 'blog/post_edit.html', {'form': form})

def post_detail (request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') 
    return render(request, 'blog/post_list.html', {'posts': posts})


def login1(request):
    #se o metodo do html for POST
    if request.method == "POST":
        #captura usuario digitato no input com o name 'usuario'
        usuario = request.POST.get('usuario')
        #captura senha digitata no input com o name 'senha'
        senha = request.POST.get('senha')
        #autentica se realmente a senha e login esta certo, lembrando que tem que importar 'from django.contrib.auth import authenticate'
        usu = authenticate(username=usuario, password=senha)
        #Se tiver tudo certinho com o usuario
        if usu is not None:
            #consulta o usuario
            us = User.objects.filter(username=usuario)
            for u in us:
                #verifica o nivel de acesso
                if u.first_name == "1":
                    login(request, usu)
                    return redirect(post_list)
                else:
                    #significa que o acesso e diferente e vai pra outra pagina
                    pass
        else:
            return render(request, 'blog/login.html', {'msg': "Falha!"})
    return render(request, 'blog/login.html',{'msg': ''})


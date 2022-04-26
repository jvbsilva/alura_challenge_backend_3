from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import Transactions, History
from .forms import UploadFileForm, UserForm

from .aux_funcs import validate_transactions

### INDEX ###
def index(request):
    return redirect('login')

## CADASTRO ##
def cadastro(request):
    if request.method == 'POST':
        # Guardar informações do formulário
        first_name = request.POST.get('nome')
        email = request.POST.get('email')
        username = email

        # Verificar se email já cadastrado
        if User.objects.filter(email = email).exists():
            return HttpResponse('Email já cadastrado')

        ## Criar senha padrão
        senha = '123456'

        # Criar user e salvar no BD
        user = User.objects.create_user(username = username,first_name = first_name, email = email, password = senha, is_staff = False)
        user.save()
        
        # Após cadastro direcionar para página de login
        return redirect('login')

    return render(request, 'cadastro.html')

### LOGIN ###
def login(request):
    if request.method == 'POST':

        # Guardar informaçõe do formulário
        email = request.POST.get('email')
        username = email
        senha = request.POST.get('senha')

        # Checar se email já está cadastrado
        if not User.objects.filter(email = email).exists():
            messages.error(request, 'Usuário não cadastrado')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Autenticar usuário e senha
        auth_user = authenticate(username = username, email = email, password = senha)
        if auth_user:
            auth_login(request,auth_user)
            return redirect('imports')
        else:
            messages.error(request, 'Senha inválida')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'login.html')

### LOGOUT ###
def logout(request):
    auth_logout(request)
    return redirect('login')

### IMPORTAÇÕES ###
@login_required(login_url = '/login/')
def imports(request):

    username = None
    if request.user.is_authenticated:
        username = request.user.username
    
    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            # Guardar arquivo submetido
            f = request.FILES['file']
            # Consultar datas já armazenadas no BD
            dates = History.objects.values_list('date_transactions', flat=True)
            # Validar transações
            new_transactions, first_date, erro_msg = validate_transactions(f, dates)

            if new_transactions:
                # Enviar transações válidas para o BD
                Transactions.objects.bulk_create(new_transactions,batch_size=None)
                # Salvar histórico da importação
                h = History(date_transactions = first_date, user = username)
                h.save()

                messages.info(request, 'Dados importados')
            
            for msg in erro_msg:
                messages.error(request, msg)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else: 
        form = UploadFileForm()
        history = History.objects.all()
        context = {}
        context['form'] = form
        context['history'] = history
        return render(request, 'imports.html', context)

### TRANSAÇÕES ###
@login_required(login_url = '/login/')
def list_transactions(request,date_transactions):
    transactions = Transactions.objects.filter(date_transactions=date_transactions)
    context = {}
    context['transactions'] = transactions
    return render(request, 'list_transactions.html', context)

### USUÁRIOS ###
@login_required(login_url = '/login/')
def usuarios(request):
    # Get all users
    users = User.objects.all().order_by('pk')
    # Remove superuser
    users = [x for x in users if x.is_superuser == False]

    context = {}
    context['users'] = users
    return render(request, 'usuarios.html', context)

### CRIAR USUÁRIOS ###
@login_required(login_url = '/login/')
def create_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('usuarios')

    context = {}
    context['form'] = form
    return render(request, 'create_user.html', context)

### EDITAR USUÁRIOS ###
@login_required(login_url = '/login/')
def update_user(request,user_pk):

    edit_user = User.objects.filter(pk=user_pk).first()
    form = UserForm(request.POST or None, instance = edit_user)
    if form.is_valid():
        form.save()
        return redirect('usuarios')

    context = {}
    context['user'] = edit_user
    context['form'] = form
    return render(request, 'update_user.html', context)

### DELETAR USUÁRIOS ###
@login_required(login_url = '/login/')
def delete_user(request,user_pk):
    del_user = User.objects.filter(pk=user_pk).first()
    if del_user.is_active:
        messages.error(request, "Não é possível remover um usuário ativo.")
    else:
        del_user.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
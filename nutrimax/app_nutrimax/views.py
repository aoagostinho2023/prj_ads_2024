from django.shortcuts import render
from .models import Usuario

# Create your views here.
def home(request):
    return render(request,'pages/home.html')

def calcular_tmb(peso, altura, idade, sexo):
    # Fórmulas de Mifflin-St Jeor
    if sexo == 'M':  # Masculino
        tmb = 10 * peso + 6.25 * altura - 5 * idade + 5
    elif sexo == 'F':  # Feminino
        tmb = 10 * peso + 6.25 * altura - 5 * idade - 161
    else:
        raise ValueError("Sexo inválido. Use 'M' para masculino ou 'F' para feminino.")
    return tmb

def ajustar_por_atividade(tmb, atividade):
    # Fatores de atividade
    fatores_atividade = {
        'baixo': 1.2,
        'medio': 1.55,
        'alto': 1.9
    }
    fator = fatores_atividade.get(atividade.lower(), 1.2)  # Padrão para 'baixo' se atividade não for reconhecida
    return tmb * fator

def calcular_imc(peso, altura_cm):
    # Converter altura de cm para metros
    altura_m = altura_cm / 100
    # Fórmula de IMC
    imc = peso / (altura_m ** 2)
    return imc

def classificar_imc(imc):
    # Classificar IMC
    if imc < 18.5:
        return 'Baixo'
    elif 18.5 <= imc < 24.9:
        return 'Normal'
    elif 25 <= imc < 29.9:
        return 'Sobrepeso'
    else:
        return 'Obesidade'

def usuarios(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        idade = int(request.POST.get('idade'))
        sexo = request.POST.get('sexo').upper()  # Garantir que o sexo esteja em maiúsculo
        altura = int(request.POST.get('altura'))
        peso = int(request.POST.get('peso'))
        atividade = request.POST.get('atividade').lower()  # Garantir que a atividade esteja em minúsculo
        objetivo = request.POST.get('objetivo')

        # Calcular TMB
        tmb = calcular_tmb(peso, altura, idade, sexo)
        # Ajustar TMB com base no nível de atividade
        calorias_diarias = ajustar_por_atividade(tmb, atividade)
        # Calcular IMC
        imc = calcular_imc(peso, altura)
        # Classificar IMC
        imc_stat = classificar_imc(imc)

        # Criar e salvar o novo usuário
        novo_usuario = Usuario()
        novo_usuario.nome = nome
        novo_usuario.idade = idade
        novo_usuario.sexo = sexo
        novo_usuario.altura = altura
        novo_usuario.peso = peso
        novo_usuario.atividade = atividade
        novo_usuario.objetivo = objetivo
        novo_usuario.tmb = calorias_diarias
        novo_usuario.imc = imc
        novo_usuario.imc_stat = imc_stat
        novo_usuario.save()
        

    usuarios = {
        'usuarios': Usuario.objects.all()
    }

    return render(request, 'pages/usuarios.html', usuarios)

def base_usuarios(request):
    usuarios = {
        'usuarios': Usuario.objects.all()
    }

    return render(request, 'pages/usuarios.html', usuarios)
from django.shortcuts import render
from .models import Usuario

# Create your views here.
def home(request):
    return render(request,'pages/home.html')

def calcular_tmb(peso, altura, idade, sexo):
    # Fórmulas de Mifflin-St Jeor
    if sexo == 'M': 
        tmb = 10 * peso + 6.25 * altura - 5 * idade + 5
    else:
        tmb = 10 * peso + 6.25 * altura - 5 * idade - 161
    return tmb

def ajustar_por_atividade(tmb, atividade):
    fatores_atividade = {
        'baixo': 1.2,
        'medio': 1.55,
        'alto': 1.9
    }
    fator = fatores_atividade.get(atividade.lower(), 1.2)
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
        sexo = request.POST.get('sexo').upper()
        altura = int(request.POST.get('altura'))
        peso = int(request.POST.get('peso'))
        atividade = request.POST.get('atividade').lower()
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


def recomendacao_nutricional(request, usuario_id=None):
    usuarios = Usuario.objects.all()
    tmb = None
    macros_ganhar_peso = None
    macros_perder_peso = None
    macros_manter_peso = None

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        if usuario_id:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
            tmb = usuario.tmb

            if tmb:
                calorias_ganhar_peso = tmb * 1.15
                calorias_perder_peso = tmb * 0.85
                calorias_manter_peso = tmb

                macros_ganhar_peso = calcular_macros(calorias_ganhar_peso)
                macros_perder_peso = calcular_macros(calorias_perder_peso)
                macros_manter_peso = calcular_macros(calorias_manter_peso)

    elif usuario_id:
        usuario = Usuario.objects.get(id_usuario=usuario_id)
        tmb = usuario.tmb

        if tmb:
            calorias_ganhar_peso = tmb * 1.15
            calorias_perder_peso = tmb * 0.85
            calorias_manter_peso = tmb

            macros_ganhar_peso = calcular_macros(calorias_ganhar_peso)
            macros_perder_peso = calcular_macros(calorias_perder_peso)
            macros_manter_peso = calcular_macros(calorias_manter_peso)

    context = {
        'usuarios': usuarios,
        'tmb': tmb,
        'usuario_selecionado': usuario_id,
        'macros_ganhar_peso': macros_ganhar_peso,
        'macros_perder_peso': macros_perder_peso,
        'macros_manter_peso': macros_manter_peso,
    }

    return render(request, 'pages/recomendacao.html', context)



def calcular_macros(calorias):
    gramas_carboidratos = (calorias * 0.5) / 4
    gramas_proteinas = (calorias * 0.3) / 4
    gramas_gorduras = (calorias * 0.2) / 9

    return {
        'calorias': calorias,
        'carboidratos': gramas_carboidratos,
        'proteinas': gramas_proteinas,
        'gorduras': gramas_gorduras,
    }

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import json

# Create your views here.
def home(request):
    return render(request,'pages/home.html')

def alimentos(request):
    alimentos = {
        'alimentos': Alimentos.objects.all().order_by('nome')
    }

    return render(request, 'pages/alimentos.html', alimentos)

def cadastra_alimentos(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        calorias = float(request.POST.get('calorias'))
        carboidratos = float(request.POST.get('carboidratos'))
        proteinas = float(request.POST.get('proteinas'))
        gorduras = float(request.POST.get('gorduras'))

        # Criar e salvar o novo usuário
        novo_alimento = Alimentos()
        novo_alimento.nome = nome
        novo_alimento.calorias = calorias
        novo_alimento.carboidratos = carboidratos
        novo_alimento.proteinas = proteinas
        novo_alimento.gorduras = gorduras
        novo_alimento.save()
        

    alimentos = {
        'alimentos': Alimentos.objects.all().order_by('nome')
    }

    return render(request, 'pages/alimentos.html', alimentos)

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


def criador_cardapio(request, usuario_id=None):
    usuarios = Usuario.objects.all()
    tmb = None
    macros = None
    objetivo_usuario = None

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        if usuario_id:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
            tmb = usuario.tmb
            objetivo_usuario = usuario.objetivo

            if tmb:
                if objetivo_usuario == 'ganho':
                    calorias = tmb * 1.15
                elif objetivo_usuario == 'perda':
                    calorias = tmb * 0.85
                else:  # "manter"
                    calorias = tmb

                macros = calcular_macros(calorias)

    elif usuario_id:
        usuario = Usuario.objects.get(id_usuario=usuario_id)
        tmb = usuario.tmb
        objetivo_usuario = usuario.objetivo

        if tmb:
            if objetivo_usuario == 'ganho':
                calorias = tmb * 1.15
            elif objetivo_usuario == 'perda':
                calorias = tmb * 0.85
            else:  # "manter"
                calorias = tmb

            macros = calcular_macros(calorias)


    context = {
        'usuarios': usuarios,
        'tmb': tmb,
        'usuario_selecionado': usuario_id,
        'macros': macros,
        'objetivo_usuario': objetivo_usuario,
        'alimentos': Alimentos.objects.all().order_by('nome')
    }

    return render(request, 'pages/criador_cardapio.html', context)

def salvar_cardapio(request):
    if request.method == 'POST':
        try:
            # Parse do JSON recebido diretamente no corpo da requisição
            cardapio_data = json.loads(request.body)
            usuario_id = cardapio_data.get('usuario_id')
            alimentos = cardapio_data.get('alimentos', [])

            # Validar se o usuário existe
            usuario = Usuario.objects.filter(id_usuario=usuario_id).first()
            if not usuario:
                return JsonResponse({'error': 'Usuário não encontrado.'}, status=400)

            # Verificar se já existe cardápio salvo para o usuário
            cardapios_existentes = Cardapio.objects.filter(usuario=usuario)
            if cardapios_existentes.exists():
                # Deletar todos os registros anteriores
                cardapios_existentes.delete()

            # Salvar cada alimento na tabela Cardapio
            for item in alimentos:
                nome = item.get('nome')
                quantidade = item.get('quantidade', 100)  # Quantidade padrão: 100g
                alimento = Alimentos.objects.filter(nome=nome).first()

                if alimento:
                    Cardapio.objects.create(
                        usuario=usuario,
                        alimento=alimento,
                        quantidade=quantidade
                    )

            # Retornar uma resposta de sucesso
            return JsonResponse({'message': 'Cardápio salvo com sucesso!'}, status=200)

        except json.JSONDecodeError:
            # Erro ao interpretar o JSON
            return JsonResponse({'error': 'Erro no formato do JSON.'}, status=400)

        except Exception as e:
            # Tratar erros gerais
            return JsonResponse({'error': str(e)}, status=500)

    # Caso o método não seja POST
    return JsonResponse({'error': 'Método não permitido.'}, status=405)

def visualizar_cardapio(request, usuario_id):
    try:
        # Buscar o usuário
        usuario = Usuario.objects.get(id_usuario=usuario_id)

        # Buscar os alimentos do cardápio do usuário
        cardapio = Cardapio.objects.filter(usuario=usuario)

        # Preparar os dados para o template
        context = {
            'usuario': usuario,
            'cardapio': cardapio,
        }

        return render(request, 'pages/visualizar_cardapio.html', context)

    except Usuario.DoesNotExist:
        # Se o usuário não for encontrado, exibir mensagem de erro
        return render(request, 'pages/erro.html', {'mensagem': 'Usuário não encontrado.'})

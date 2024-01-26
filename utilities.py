
from datetime import datetime, date
import locale

# ======================================================================

" FUNÇÃO QUE VERIFICA SE O CAMPO É UM NÚMERO VÁLIDO PARA MOEDA AMERICANA "

def vrf_numerico(valor, campo, flag=None):
    try:
        # verifica se o valor do campo é vazio e a flag tá setada em NONE
        if valor == "" and flag is None:
            # se sim, ele retorna informando que o campo é obrigatório
            campo.error_text = "Este campo é obrigatório!"
            return False
        # verifica se o valor do campo é vazio, e a flag tá setada em TRUE
        elif valor == "" and flag:
            # se sim, ele atribui ZERO ao valor do campo
            valor = "0"
        # Tenta transformar o valor em float (se não for um float, vai ser capturado pelo except)
        float_valor = float(valor)
        # Se for um valor válido float, arredonda as casas decimais para duas, e retorna o valor
        return round(float_valor, 2)
    # Se não for um valor válido float, retorna o erro e é capturado abaixo
    except ValueError:
        campo.error_text = "Digite um valor válido! (Formatação Americana: 10,000.00)"
        return False

# ======================================================================

""" FUNÇÃO QUE FILTRA, ORGANIZA E ORDENA DATAS VÁLIDAS (FORMATOS AMERICANOS E BRASILEIROS)"""

def data_filtro(valor, campo):
    # Verifica se o valor é vazio
    if valor == "":
        # se sim, retorna a data atual
        return date.today().strftime("%d/%m/%Y")
    try:
        # tenta realizar a conversão da string para um formato de data válido (1° tentativa - formato brasileiro)
        date_obj = datetime.strptime(valor, "%d/%m/%Y")
        # se bem sucedida, retorna a data formatada
        return date_obj.strftime("%d/%m/%Y")  
    # caso a data da primeira tentativa retorne erro
    except ValueError:
        try:
            # tenta realizar a conversão da string para um formato de data válido (2° tentativa - formato americano)
            date_obj = datetime.strptime(valor, "%m/%d/%Y")
            # se bem sucedida, retorna a data formatada
            return date_obj.strftime("%d/%m/%Y") 
        except ValueError:
            # se não for bem sucedida em nenhum dos casos, retorna erro na data inserida
            campo.error_text = "Formato da Data inválido!"
            return False

# ======================================================================

""" FUNÇÃO QUE ORDENA, FILTRA E ORGANIZA VALORES EM DÓLAR """

def formatar_valor(valor):
    # Uso da biblioteca locale para setar o tipo de moeda a ser utilizado
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    # se o valor for menor que zero, ou seja negativo
    if valor < 0:
        # formata o valor para as casas decimais adequadas ao dólar e adiciona o simbolo de negativo á frente junto ao cifrão da moeda setada
        valor_formatado = f"-{locale.currency(abs(valor), grouping=True)}"
    else:
        # se o valor for maior que zero, apenas formata o valor e adiciona o cifrão correspondente
        valor_formatado = locale.currency(valor, grouping=True)
    return valor_formatado

# ======================================================================

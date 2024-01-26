# ============================================================================================================================================

import flet as ft
from database import Frota, conexao_bd, Alugueis, Historico, Clientes, Financeiro
import widgets as wd
import utilities as ut

# ============================================================================================================================================
# ============================================================================================================================================

        
# ============================================================================================================================================

""" FUNÇÃO DA PÁGINA FROTA ONDE TODOS OS ELEMENTOS SÃO CRIADOS, ARMAZENADOS E ENVIADOS PARA RENDERIZAÇÃO """

# ============================================================================================================================================



def page_frota(page, rail):
    def view_frota():
        cabecario = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Placa")),
            ft.DataColumn(ft.Text("Marca")),
            ft.DataColumn(ft.Text("Modelo")),
            ft.DataColumn(ft.Text("Vencimento Documento")),
            ft.DataColumn(ft.Text("Vencimento Seguro")),
            ft.DataColumn(ft.Text("Troca de Óleo")),
            ft.DataColumn(ft.Text("Observações")),
            ft.DataColumn(ft.Text("Cor")),
            ft.DataColumn(ft.Text("Status"))]
        itens = Frota.mostrar_frota(page)
        return wd.criar_datarow(cabecario, itens)
    
    page.update()

    placa = ft.TextField(label="Placa*", hint_text="Informe a placa do veículo", autofocus=True)
    marca = ft.TextField(label="Marca", hint_text="Informe a Marca do veículo")
    modelo = ft.TextField(label="Modelo", hint_text="Informe o Modelo do veículo")
    documento = ft.TextField(label="Vencimento do Documento", hint_text="Informe a data da documentação", prefix_icon="CALENDAR_MONTH_OUTLINED")
    seguro = ft.TextField(label="Vencimento Seguro", hint_text="Informe a data do seguro", prefix_icon="CALENDAR_MONTH_OUTLINED")
    oleo = ft.TextField(label="Última Troca de Óleo", hint_text="Informe a última troca de Óleo", prefix_icon="CALENDAR_MONTH_OUTLINED")
    obs = ft.TextField(label="Observações", hint_text="Informe as observações")
    cor = ft.TextField(label="Cor do Veículo", hint_text="Informe a cor do veículo", prefix_icon="COLOR_LENS_OUTLINED")
    status = ft.Dropdown(
                label="Status*",
                hint_text="Escolha o status do veiculo",
                options=[
                    ft.dropdown.Option("Disponivel"),
                    ft.dropdown.Option("Indisponivel"),
                ],
                border=ft.border.all(0.7, "red"),
            )
    obs_veiculo = ft.Text("Atenção, O Status do seu veículo afeta diretamente na possibilidade aluguel dele!", color="red", weight=ft.FontWeight.W_600)

    def abrir_modal(e):
        page.dialog = modal
        modal.open = True
        page.update()

    def fechar_modal(e):
        modal.open = False
        page.update()

    def add_carro(e):
        if not placa.value:
            placa.error_text = "Este campo é obrigatório"
            abrir_modal(e)
            return
        if not status.value:
            status.error_text = "Este campo é obrigatório"
            abrir_modal(e)
            return 
        
        campos_data = [documento, seguro, oleo]
        lista = []
        for data in campos_data:
            data_valor = ut.data_filtro(data.value, data)
            lista.append(data_valor)
            if not data_valor:
                abrir_modal(e)
                return
        documento_valor, seguro_valor, oleo_valor = lista

            
        fechar_modal(e)

        Frota.salvar_frota(placa.value, marca.value, modelo.value, documento_valor, seguro_valor, oleo_valor, obs.value, cor.value, status.value)
        page.update()
    
    def atualizar(e):
        page.clean()
        page.add(page_frota(page, rail))

    campos_modal = ft.Column(controls=[placa, marca, modelo, documento, seguro, oleo, obs, cor, status, obs_veiculo], height=500, width=800, scroll=ft.ScrollMode.ALWAYS)
    titulo = "Adicionar Carro na Frota: "
    modal = wd.criar_modal(titulo, campos_modal, fechar_modal, add_carro)

    return ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            ft.Column(
                [
                    ft.Row([ 
                        ft.OutlinedButton("Adicionar Carro", icon="ADD_CIRCLE", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), on_click=abrir_modal),
                        ft.OutlinedButton("Atualizar Tabela", icon="REFRESH", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), on_click=atualizar),   
                    ]),
                    view_frota(),
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
                scroll=ft.ScrollMode.ALWAYS,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )



# ============================================================================================================================================

""" FUNÇÃO DA PÁGINA ALUGUÉIS ONDE TODOS OS ELEMENTOS SÃO CRIADOS, ARMAZENADOS E ENVIADOS PARA RENDERIZAÇÃO """

# ============================================================================================================================================



def page_aluguel(page, rail):
    def view_aluguel():
        cabecario = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("ID - Frota")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Endereço")),
            ft.DataColumn(ft.Text("Identidade")),
            ft.DataColumn(ft.Text("Data do Aluguel")),
            ft.DataColumn(ft.Text("Data de Devolução")),
            ft.DataColumn(ft.Text("Observações")),
            ft.DataColumn(ft.Text("Valor do Aluguel (US$)")),
            ft.DataColumn(ft.Text("Valor Pago (US$)")),
            ft.DataColumn(ft.Text("Placa do Carro")),]
        itens = Alugueis.mostrar_alugueis(page)
        return wd.criar_datarow(cabecario, itens)
       
    page.update()

    nome = ft.TextField(label="Nome do Locatário*", hint_text="Informe o nome completo", autofocus=True)
    endereco = ft.TextField(label="Endereço do Locatário", hint_text="Informe o endereço", prefix_icon="LOCATION_ON_OUTLINED")
    identidade = ft.TextField(label="Identificação", hint_text="Informe um meio de Identificação")
    data_retirada = ft.TextField(label="Data do Aluguel", hint_text="Informe a data que foi alugado", prefix_icon="CALENDAR_MONTH_OUTLINED")
    data_devolucao= ft.TextField(label="Data da Devolução", hint_text="Informe a data que o veículo foi devolvido", prefix_icon="CALENDAR_MONTH_OUTLINED")
    valor = ft.TextField(label="Valor Aluguel*", hint_text="Informe o valor do aluguel", prefix_text="US$ ", prefix_icon="MONETIZATION_ON_OUTLINED")
    valor_pago = ft.TextField(label="Valor Pago*", hint_text="Informe o valor já pago", prefix_text="US$ ", prefix_icon="MONETIZATION_ON_OUTLINED")
    obs = ft.TextField(label="Observações", hint_text="Observações adicionais")

    frota_id = ft.Dropdown(
        label="Veiculo - Placa*",
        hint_text="Escolha o veiculo alugado (Pela Placa)",
        options=[])

    frota_id.options = [ft.dropdown.Option(id, placa) for id, placa in Frota.carros_frota('id, placa', 'status', 'Disponivel')]

    obs_veiculo = ft.Text("Os veículos acima são apenas aqueles presentes na sua frota com status disponível!", color="red", weight=ft.FontWeight.W_600)
    campos_modal = ft.Column(controls=[nome, endereco, identidade,
                                       data_retirada, data_devolucao,
                                       valor, valor_pago, obs,
                                       frota_id, obs_veiculo],
                             height=500, width=800, scroll=ft.ScrollMode.ALWAYS)

    def abrir_modal(e):
        page.dialog = modal
        modal.open = True
        page.update()

    def fechar_modal(e):
        modal.open = False
        page.update()

    def add_aluguel(e):
        if not nome.value:
            nome.error_text = "Este campo é obrigatório"
            abrir_modal(e)
            return
        if not frota_id.value:
            frota_id.error_text = "Este campo é obrigatório"
            abrir_modal(e)
            return 
    
        campos_valor = [valor, valor_pago]
        lista_valor = []
        for valores in campos_valor:
            valor_vrf = ut.vrf_numerico(valores.value, valores)
            lista_valor.append(valor_vrf)
            if valor_vrf is False:
                abrir_modal(e)
                return
        valor_aluguel_vrf, valor_pago_vrf = lista_valor

        campos_data = [data_retirada, data_devolucao]
        lista_data = []
        for datas in campos_data:
            data_valor = ut.data_filtro(datas.value, datas)
            lista_data.append(data_valor)
            if not data_valor:
                abrir_modal(e)
                return
        data_retirada_valor, data_devolucao_valor = lista_data

        fechar_modal(e)

        Alugueis.adicionar_aluguel(nome.value, endereco.value, identidade.value, data_retirada_valor, data_devolucao_valor, obs.value, valor_aluguel_vrf, valor_pago_vrf, frota_id.value)
        page.update()

    def atualizar(e):
        page.clean()
        page.add(page_aluguel(page, rail))

    titulo = "Adicionar Aluguel"
    modal = wd.criar_modal(titulo, campos_modal, fechar_modal, add_aluguel)

    return ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            ft.Column(
                [
                    ft.Row([  # Nova linha para os botões 
                        ft.OutlinedButton("Adicionar Aluguel", icon="ADD_CIRCLE", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), on_click=abrir_modal),
                        ft.OutlinedButton("Atualizar Tabela", icon="REFRESH", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), on_click=atualizar),
                    ]),
                    view_aluguel(),
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
                scroll=ft.ScrollMode.ALWAYS,),],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )



# ============================================================================================================================================

""" FUNÇÃO DA PÁGINA HISTÓRICO ONDE TODOS OS ELEMENTOS SÃO CRIADOS, ARMAZENADOS E ENVIADOS PARA RENDERIZAÇÃO """

# ============================================================================================================================================



def page_historico(page, rail):
    def view_historico():
        cabecario = [
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Endereço")),
                ft.DataColumn(ft.Text("Identidade")),
                ft.DataColumn(ft.Text("Data do Aluguel")),
                ft.DataColumn(ft.Text("Data de Devolução")),
                ft.DataColumn(ft.Text("Observações")),
                ft.DataColumn(ft.Text("Valor do Aluguel (US$)")),
                ft.DataColumn(ft.Text("Valor Pago (US$)")),]
        itens = Historico.mostrar_historico(page)
        return wd.criar_datarow(cabecario, itens)

    page.update()

    return ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            ft.Column(
                [
                    ft.Row([  # Nova linha para os botões
                        ft.Text("Abaixo estão todos aluguéis já feitos:", font_family="Roboto", weight=ft.FontWeight.W_600, size=20),
                    ]),
                    view_historico(),
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
                scroll=ft.ScrollMode.ALWAYS,),],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )



# ============================================================================================================================================

""" FUNÇÃO DA PÁGINA CLIENTES ONDE TODOS OS ELEMENTOS SÃO CRIADOS, ARMAZENADOS E ENVIADOS PARA RENDERIZAÇÃO """

# ============================================================================================================================================



def page_clientes(page, rail):
    def view_clientes():
        cabecario = [
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Endereço")),
                ft.DataColumn(ft.Text("Identidade")),]
        itens = Clientes.mostrar_clientes(page)
        return wd.criar_datarow(cabecario, itens)

    page.update()

    return ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            ft.Column(
                [
                    ft.Row([  # Nova linha para os botões
                        ft.Text("Abaixo estão todos os clientes que já alugaram um veículo:", font_family="Roboto", weight=ft.FontWeight.W_600, size=20),
                    ]),
                    view_clientes(),
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
                scroll=ft.ScrollMode.ALWAYS,),],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )




# ============================================================================================================================================

""" FUNÇÃO DA PÁGINA FINANCEIRO ONDE TODOS OS ELEMENTOS SÃO CRIADOS, ARMAZENADOS E ENVIADOS PARA RENDERIZAÇÃO """

# ============================================================================================================================================



def page_financeiro(page, rail):
    def view_geral():
        cabecario = [
                ft.DataColumn(ft.Text("Entrada (US$)")),
                ft.DataColumn(ft.Text("Saída (US$)")),
                ft.DataColumn(ft.Text("Valor Bruto (US$)")),
                ft.DataColumn(ft.Text("Valor Líquido (US$)")),
                ]
        itens = Financeiro.mostrar_financeiro(page)
        return wd.criar_datarow(cabecario, itens)
    
    def atualizar(e):
        page.clean()
        page.add(page_financeiro(page, rail))

    page.update()

    return ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            ft.Column(
                [   
                    ft.Row([
                        ft.OutlinedButton("Atualizar Tabela", icon="REFRESH", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), on_click=atualizar),
                    ]),
                    view_geral(),
                    ft.Text("Info: Esta tabela é composta pela junção das Tabelas de Dívidas + Lucros!", color="red", weight=ft.FontWeight.BOLD, size=16),
                    ft.Text("Para mais informações sobre as tabelas e seus cálculos, consulte o menu 'AJUDA' no canto superior direito!", color="red", weight=ft.FontWeight.BOLD, size=16)
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
                scroll=ft.ScrollMode.ALWAYS)],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )



# ============================================================================================================================================

""" FUNÇÃO DA PÁGINA LUCROS ONDE TODOS OS ELEMENTOS SÃO CRIADOS, ARMAZENADOS E ENVIADOS PARA RENDERIZAÇÃO """

# ============================================================================================================================================



def page_financeiro_aluguel(page, rail):
    def view_financeiro_aluguel():
        cabecario = [
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Entradas (US$)")),
                ft.DataColumn(ft.Text("Placa")),
                ft.DataColumn(ft.Text("Data do Aluguel")),
                ft.DataColumn(ft.Text("Lucros Administração (US$)")),
                ft.DataColumn(ft.Text("Bruto Empresa (US$)")),
                ft.DataColumn(ft.Text("Lucros Empresa (US$)"))]
        itens = Financeiro.mostrar_financeiro_aluguel(page)
        return wd.criar_datarow(cabecario, itens)
    
    def views_total():
        cabecario2 = [
                ft.DataColumn(ft.Text("Entradas Totais (US$)")),
                ft.DataColumn(ft.Text("Saídas Totais (US$)")),
                ft.DataColumn(ft.Text("Lucro Administração Total (US$)")),
                ft.DataColumn(ft.Text("Lucro Empresa Total (US$)"))]
        itens2 = Financeiro.financeiro_aluguel_total()
        return wd.criar_datarow(cabecario2, itens2)

    def atualizar(e):
        page.clean()
        page.add(page_financeiro_aluguel(page, rail))

    page.update()

    return ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            ft.Column([ft.Row([ft.OutlinedButton("Atualizar Tabela", icon="REFRESH", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), on_click=atualizar)]),
                    ft.Text("Dados Financeiros de cada Aluguel:", size=20, weight=ft.FontWeight.BOLD), 
                    view_financeiro_aluguel(),
                    ft.Text("\nDados Financeiros Totais de Aluguel:", size=20, weight=ft.FontWeight.BOLD),
                    views_total()
                    ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
                scroll=ft.ScrollMode.ALWAYS)
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,)



# ============================================================================================================================================

""" FUNÇÃO DA PÁGINA DÍVIDAS ONDE TODOS OS ELEMENTOS SÃO CRIADOS, ARMAZENADOS E ENVIADOS PARA RENDERIZAÇÃO """

# ============================================================================================================================================



def page_dividas(page, rail):
    def view_dividas():
        cabecario = [
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Entradas (US$)")),
                ft.DataColumn(ft.Text("Saídas (US$)")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Observações"))
                ]
        itens = Financeiro.mostrar_dividas(page)
        return wd.criar_datarow(cabecario, itens)
    
    def views_dividas_total():
        cabecario2 = [
                ft.DataColumn(ft.Text("Entrada Total (US$)")),
                ft.DataColumn(ft.Text("Saída Total (US$)")),
                ft.DataColumn(ft.Text("Líquido Total (US$)"))
                ]
        itens2 = Financeiro.dividas_total()
        return wd.criar_datarow(cabecario2, itens2)
    
    page.update()

    entradas = ft.TextField(label="Entradas", hint_text=" Informe as entradas", autofocus=True, prefix_text="US$ ", prefix_icon="MONETIZATION_ON_OUTLINED")
    gastos = ft.TextField(label="Saídas", hint_text=" Informe as saídas", prefix_text="US$ - ", prefix_icon="MONETIZATION_ON_OUTLINED")
    tipo = ft.Dropdown(
                label="Tipo do Gasto*",
                hint_text="Escolha o tipo do gasto",
                options=[
                    ft.dropdown.Option("Aluguel"),
                    ft.dropdown.Option("Outros"),
                ],
                border=ft.border.all(0.7),
            )
    obs = ft.TextField(label="Observações", hint_text="Informações adicionais")

    texto_obs_dividas = ("\nObservação: Você pode adicionar apenas a entrada e/ou saída!"
                         "\n\nInfo: Ao Adicionar tipo de gasto como aluguel, esse gasto será creditado na tabela financeira de lucros como uma saída!")
    obs_dividas = ft.Text(texto_obs_dividas, color="red", weight=ft.FontWeight.W_600)

    def abrir_modal(e):
        page.dialog = modal
        modal.open = True
        page.update()

    def fechar_modal(e):
        modal.open = False
        page.update()

    def add_financeiro(e):     
        if not tipo.value:
            tipo.error_text = "Este campo é obrigatório"
            abrir_modal(e)
            return
        if entradas.value and tipo.value == "Aluguel":
            tipo.error_text = "Aluguel não pode ser utilizado como o Tipo para ENTRADAS, apenas SAÍDAS."
            abrir_modal(e)
            return      

        campos_financeiro = [entradas, gastos]
        lista_financeiro = []
        for valores_financeiro in campos_financeiro:
            valor_vrf = ut.vrf_numerico(valores_financeiro.value, valores_financeiro, True)
            if valor_vrf is False:
                abrir_modal(e)
                return
            lista_financeiro.append(valor_vrf)
        entradas_valor, gastos_valor = lista_financeiro

        fechar_modal(e)
        conexao = conexao_bd()
        Financeiro.adicionar_dividas(entradas_valor, gastos_valor, tipo.value, obs.value, conexao)
        page.update()
    
    def atualizar(e):
        page.clean()
        page.add(page_dividas(page, rail))

    campos_modal = ft.Column(controls=[entradas, gastos, tipo, obs, obs_dividas], height=300, width=800, scroll=ft.ScrollMode.ALWAYS)
    titulo = "Adicionar Valores"
    modal = wd.criar_modal(titulo, campos_modal, fechar_modal, add_financeiro)

    return ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            ft.Column(
                [ft.Row([ft.OutlinedButton("Adicionar Valores", icon="ADD_CIRCLE", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), on_click=abrir_modal),
                        ft.OutlinedButton("Atualizar Tabela", icon="REFRESH", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), on_click=atualizar),]),
                        ft.Text("Dados Financeiros Unitários:", size=20, weight=ft.FontWeight.BOLD), 
                        view_dividas(),
                        ft.Text("\nDados Financeiros Totais:", size=20, weight=ft.FontWeight.BOLD),
                        views_dividas_total()
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
                scroll=ft.ScrollMode.ALWAYS,
            ),
            
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )



# ============================================================================================================================================

""" FUNÇÃO DA PÁGINA AJUDA ONDE TODOS OS ELEMENTOS SÃO CRIADOS, ARMAZENADOS E ENVIADOS PARA RENDERIZAÇÃO """

# ============================================================================================================================================



def page_ajuda(rail):

    # Título e Texto Geral
    titulo_tabelas = ft.Text("\nSobre as tabelas:", weight=ft.FontWeight.BOLD, size=30)
    texto_geral = (
        "Obs: As tabelas foram feitas levando em consideração a necessidade da sua empresa em específico."
        " Se necessitar de configurações diferentes, entre em contato clicando no botão esquerdo superior!"
    )
    texto1 = ft.Text(texto_geral, weight=ft.FontWeight.W_500, size=14)

    # Seção Tabela de Dívidas
    subtitulo1 = ft.Text("\nTabela de Dívidas:", weight=ft.FontWeight.W_700, size=16)
    texto_tabela_dividas = (
        "A tabela de dívidas é composta por 4 colunas: Entradas, Saídas, Tipo e Observações."
        " Nesta tabela, você pode adicionar entradas e saídas de dinheiro, mas ela é especialmente feita para as saídas."
        "\n\nTipo Aluguel:"
        "\n         Ao adicionar um gasto com o tipo 'ALUGUEL', esse gasto será creditado na tabela financeira de lucros como um gasto,"
        " reajustando o seu lucro líquido."
        "\n         Atenção: Ao escolher o tipo de gasto, tenha em mente que o TIPO 'ALUGUEL' é exclusivo para a adição de 'SAÍDAS/GASTOS/DÍVIDAS',"
        " não podendo ser utilizado como TIPO para quando forem valores de 'ENTRADAS/SALDOS'."
        "\n\nTipo Outros:"
        "\n         Ao adicionar um gasto com o tipo 'OUTROS', esse gasto não será creditado na tabela financeira de lucros, apenas na Tabela Financeira Geral."
        "\n         Atenção: Ao escolher o tipo de gasto, o TIPO 'OUTROS' pode ser utilizado para 'ENTRADAS/SALDOS' e 'SAÍDAS/GASTOS/DÍVIDAS'."
    )
    texto2 = ft.Text(texto_tabela_dividas)

    # Seção Tabela de Lucros
    subtitulo2 = ft.Text("\nTabela de Lucros:", weight=ft.FontWeight.W_700, size=16)
    texto_tabela_alugueis = (
        "A tabela de Lucro também chamada de Tabela de Aluguéis é dividida em: Entradas, Placa, Lucros Administração, Bruto Empresa e Lucros Empresa."
        " Nesta tabela, terá os valores para cada aluguel que você tiver feito separadamente, cada aluguel é identificado pela placa do carro alugado,"
        " e cada aluguel tem seus valores de entrada, lucro de administração, bruto da empresa e lucro da empresa, onde:"
        "\n\nEntradas e Bruto Empresa:"
        "\n         É o valor que o cliente pagou pelo aluguel do veículo total."
        "\n\nLucros Administração:"
        "\n         É o valor que a administração ganha em cima do valor do aluguel bruto, neste caso configurado como: 30%."
        "\n         Cálculo -> (30 / 100) * Entrada"
        "\n\nLucros Empresa:"
        "\n         É o valor bruto subtraído do lucros da administração, ou seja, o líquido de cada aluguel."
        "\n         Cálculo -> Entrada - Lucros Administração"
        "\n\nAo final da tabela, temos os valores totais de cada coluna somadas, te trazendo uma perspectiva geral dos aluguéis, onde:"
        "\n\nEntradas Totais:"
        "\n         A soma de todas as entradas de aluguéis."
        "\n\nSaídas Totais:"
        "\n         A soma de todas as saídas/gastos adicionadas na tabela de dívidas, que tiverem o tipo 'ALUGUEL'."
        "\n\nLucro Administração Total:"
        "\n         A soma de todos os lucros de administração de cada aluguel."
        "\n\nLucro Empresa Total:"
        "\n         A soma de todos os lucros da empresa de cada aluguel subtraído da soma de todas as saídas e gastos totais."
        "\n         Cálculo -> Lucro Empresa [O lucro empresa já inclui a subtração dos valores da administração] - Saídas Totais"
    )
    texto3 = ft.Text(texto_tabela_alugueis)

    # Seção Tabela Geral
    subtitulo3 = ft.Text("\nTabela Financeiro Geral:", weight=ft.FontWeight.W_700, size=16)

    texto_tabela_geral = (
    "A tabela de Financeiro Geral é dividida em: Entradas, Saída, Valor Bruto e Valor Líquido."
    " Nesta Tabela teremos a visão geral de todo o financeiro, uma junção das tabelas de Lucros e Dívidas onde:"
    "\n\nEntradas e Valor Bruto:"
    "\n         São os valores de todos aluguéis da tabela de lucros + valores de todas as entradas da tabela de dívidas."
    "\n         Cálculo -> Entradas totais aluguéis + Entradas totais de outros"
    "\n\nSaídas:"
    "\n         São os valores de todas as dívidas da tabela de dívidas, sejam elas do tipo aluguel ou não."
    "\n\nValor Líquido:"
    "\n         Os valores líquidos desta tabela são a subtração das duas colunas anteriores, de saídas e Entradas"
    "\n         Cálculo -> Entrada - Saídas"
    )
    texto4 = ft.Text(texto_tabela_geral)

    return ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            ft.Column(
                [
                    titulo_tabelas,
                    texto1,
                    subtitulo1,
                    texto2,
                    subtitulo2,
                    texto3,
                    subtitulo3,
                    texto4
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
                scroll=ft.ScrollMode.ALWAYS,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )



# ============================================================================================================================================
# ============================================================================================================================================

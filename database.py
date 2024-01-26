# ======================================================================

import flet as ft
import widgets as wd
import utilities as ut
import sqlite3
import logging
from sqlite3 import Error

loggerBd = logging.getLogger('bdebug')

# ======================================================================

""" FUNÇÃO QUE CRIA UMA CONEXÃO COM O BANCO DE DADOS """

def conexao_bd():
    conexao = None
    try:
        conexao = sqlite3.connect('./bd.sqlite3') 
        return conexao
    except Error as e:
        loggerBd.critical(f"Erro ao conectar ao SQLite: {e}...")
        return None
    
# ======================================================================
    
""" FUNÇÃO QUE EXECUTA UMA QUERY """

def executar_query(conexao, query):
    try:
        cursor = conexao.cursor()
        cursor.execute(query)
        conexao.commit()
    except Exception as e:
        loggerBd.critical(f"Erro de execução da Query: {e} \nQuery: {query}...")
    return

# ======================================================================

""" FUNÇÃO QUE CRIA O MODAL DE EDIÇÃO PARA CADA ITEM DA PÁGINA/TABELA DE ALUGUÉIS """

def modal_aluguel(page, id_aluguel):
    def confirmar(e):
        if not nome.value:
            nome.error_text = "Este campo é obrigatório"
            abrir_modal()
            return
        
        campos_valor = [valor, valor_pago]
        lista_valor = []
        for valores in campos_valor:
            valor_vrf = ut.vrf_numerico(valores.value, valores)
            lista_valor.append(valor_vrf)
            if valor_vrf is False:
                abrir_modal()
                return
        valor_aluguel_vrf, valor_pago_vrf = lista_valor

        data_devolucao_valor = ut.data_filtro(data_devolucao.value, data_devolucao)
        if not data_devolucao_valor:
            abrir_modal()
            return
    
        Alugueis.adicionar_aluguel(nome.value, endereco.value, identidade.value, data_retirada.value, data_devolucao_valor, 
                                   obs.value, valor_aluguel_vrf, valor_pago_vrf, frota_id, id_aluguel)
        alerta_dialogo.open = False
        page.update()

    def cancelar(e):
        alerta_dialogo.open = False
        page.update()

    titulo = "Edição de Carro da Frota: "
    dados_aluguel = Alugueis.aluguel_edit(id_aluguel)

    _, frota_id, nome_value, endereco_value, identidade_value, dada_retirada_value, dada_devolucao_value, obs_value, valor_value, valor_pago_value = dados_aluguel

    nome = ft.TextField(label="Nome do Locatário*", hint_text="Informe o nome completo", value=nome_value)
    endereco = ft.TextField(label="Endereço do Locatário", hint_text="Informe o endereço", value=endereco_value, prefix_icon="LOCATION_ON_OUTLINED")
    identidade = ft.TextField(label="Identificação", hint_text="Informe um meio de Identificação", value=identidade_value)
    data_retirada = ft.TextField(label="Data do Aluguel", hint_text="Informe a data que foi alugado", value=dada_retirada_value, prefix_icon="CALENDAR_MONTH_OUTLINED", disabled=True)
    data_devolucao= ft.TextField(label="Data da Devolução", hint_text="Informe a data que o veículo foi devolvido", value=dada_devolucao_value, prefix_icon="CALENDAR_MONTH_OUTLINED")
    obs = ft.TextField(label="Observações", hint_text="Observações adicionais", value=obs_value)
    valor = ft.TextField(label="Valor Aluguel*", hint_text="Informe o valor do aluguel", value=valor_value, prefix_text="US$ ", prefix_icon="MONETIZATION_ON_OUTLINED")
    valor_pago = ft.TextField(label="Valor Pago*", hint_text="Informe o valor já pago", autofocus=True, value=valor_pago_value, prefix_text="US$ ", prefix_icon="MONETIZATION_ON_OUTLINED")
    
    campos_modal = ft.Column(controls=[nome, endereco, identidade, data_retirada, data_devolucao, obs, valor, valor_pago], height=500, width=800, scroll=ft.ScrollMode.ALWAYS)
    alerta_dialogo = wd.criar_modal(titulo, campos_modal, cancelar, confirmar, "Cancelar", "Editar")

    def abrir_modal():
        page.dialog = alerta_dialogo
        alerta_dialogo.open = True
        page.update()

    abrir_modal()

# ======================================================================

""" FUNÇÃO QUE CRIA O MODAL DE EDIÇÃO PARA CADA ITEM DA PÁGINA/TABELA DE FROTA """

def modal_frota(page, id_carro):
    def confirmar(e):
        campos_data = [documento, seguro, oleo]
        lista = []
        for data in campos_data:
            data_valor = ut.data_filtro(data.value, data)
            lista.append(data_valor)
            if not data_valor:
                abrir_modal()
                return
        documento_valor, seguro_valor, oleo_valor = lista

        Frota.salvar_frota(placa.value, marca.value, modelo.value, documento_valor, seguro_valor, oleo_valor, obs.value, cor.value, status.value, id_carro)
        alerta_dialogo.open = False
        page.update()

    def cancelar(e):
        alerta_dialogo.open = False
        page.update()

    titulo = "Edição de Carro da Frota: "
    dados_frota = Frota.carros_frota('*', 'id', id_carro)[0]

    _, placa_value, marca_value, modelo_value, documento_value, seguro_value, oleo_value, obs_value, cor_value, status_value = dados_frota
    
    placa = ft.TextField(label="Placa do Veículo*", value=placa_value, disabled=True)
    marca = ft.TextField(label="Marca", hint_text="Informe a Marca do veículo", value=marca_value, autofocus=True)
    modelo = ft.TextField(label="Modelo", hint_text="Informe o Modelo do veículo", value=modelo_value)
    documento = ft.TextField(label="Vencimento do Documento", hint_text="Informe a data da documentação", value=documento_value, prefix_icon="CALENDAR_MONTH_OUTLINED")
    seguro = ft.TextField(label="Vencimento Seguro", hint_text="Informe a data do seguro", value=seguro_value, prefix_icon="CALENDAR_MONTH_OUTLINED")
    oleo = ft.TextField(label="Última Troca de Óleo", hint_text="Informe a última troca de Óleo", value=oleo_value, prefix_icon="CALENDAR_MONTH_OUTLINED")
    obs = ft.TextField(label="Observações", hint_text="Informe as observações", value=obs_value)
    cor = ft.TextField(label="Cor do Veículo", hint_text="Informe a cor do veículo", value=cor_value, prefix_icon="COLOR_LENS_OUTLINED")
    status = ft.Dropdown(
                label="Status*",
                value = status_value,
                options=[
                    ft.dropdown.Option("Disponivel"),
                    ft.dropdown.Option("Alugado", disabled=True),
                    ft.dropdown.Option("Indisponivel"),
                ],
                border=ft.border.all(0.7, "red"),
            )
    texto_obs_dividas = (
        "\nObservação: Não é possível alterar o status de um veículo disponível/indisponível para Alugado, somente mediante cadastro no sistema de aluguéis."
        "\n\nAtenção: Ao alterar um status de um Veículo alugado para disponível/indisponível, qualquer aluguel cadastrado será retirado imediatamente."
    )
    obs_dividas = ft.Text(texto_obs_dividas, color="red", weight=ft.FontWeight.W_600)
    campos_modal = ft.Column(controls=[placa, marca, modelo, documento, seguro, oleo, obs, cor, status, obs_dividas], height=500, width=800, scroll=ft.ScrollMode.ALWAYS)
    alerta_dialogo = wd.criar_modal(titulo, campos_modal, cancelar, confirmar, "Cancelar", "Editar")

    def abrir_modal():
        page.dialog = alerta_dialogo
        alerta_dialogo.open = True
        page.update()

    abrir_modal()

# ======================================================================

""" FUNÇÃO QUE CRIA O MODAL DE EXCLUSÃO PARA CADA ITEM DE TODAS AS PÁGINAS/TABELAS """

def modal_exclusao(id, page, texto1, texto2, acao: callable):
    def confirmar(e):
        alerta_dialogo.open=False
        acao(id)
        page.update()

    def cancelar(e):
        alerta_dialogo.open=False
        page.update()

    titulo = "Confirme a Ação!"
    linha1 = ft.Text(texto1, weight=ft.FontWeight.W_600)
    linha2 = ft.Text(texto2, color="red", weight=ft.FontWeight.W_600)
    campos_modal = ft.Column(controls=[linha1, linha2], height=100, width=400)
    alerta_dialogo = wd.criar_modal(titulo, campos_modal, cancelar, confirmar,"Cancelar","Excluir")

    def abrir_modal(): 
        page.dialog = alerta_dialogo
        alerta_dialogo.open=True
        page.update()

    abrir_modal()

# ======================================================================

""" FUNÇÃO QUE RETORNA A PLACA DO CARRO COM BASE NO ID DA FROTA """

def placa(conexao, frota_id):
    cursor = conexao.cursor()
    cursor.execute(f"SELECT placa FROM Frota WHERE id = {frota_id}")
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        loggerBd.critical(f"A placa do veículo {frota_id} não foi encontrada...")
        return "Sem Placa"



# ======================================================================

""" CLASSE QUE SE REFERE A TABELA 'Frota' NO BD / FUNÇÕES CRUD (CREATE, UPDATE, DELETE) DA TABELA """

class Frota:
    # ------------------------------------------------------------------

    " FUNÇÃO QUE CARREGA OS DADOS PARA A VISUALIZAÇÃO "

    def mostrar_frota(page):
        texto1 = "Deseja realmente excluir o Carro da Frota?"
        texto2 = "Atenção, a exclusão ativara o MODO CASCATA, excluindo também aluguéis com este veículo!"
        conexao = conexao_bd()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Frota")
        dados_frotas = cursor.fetchall()
        rows = []
        for dados_carro in dados_frotas:
            id_carro = dados_carro[0]
            row = ft.DataRow([ft.DataCell(ft.Text(dado)) for dado in dados_carro], 
                            on_select_changed = lambda e, id_carro=id_carro: modal_frota(page, id_carro),
                            on_long_press = lambda e, id_carro=id_carro: modal_exclusao(id_carro, page, texto1, texto2, Frota.excluir_carro),
                             )
            rows.append(row)
        return rows
    
    # ------------------------------------------------------------------

    " FUNÇÃO QUE CRIA E ADICIONA OS DADOS NA TABELA"

    def salvar_frota(placa, marca, modelo, venc_documento, venc_seguro, oleo, obs, cor, status, id_edicao=None):
        conexao = conexao_bd()
        marca = marca or 'Sem Marca'
        modelo = modelo or 'Sem Modelo'
        obs = obs or 'Sem observações'
        cor = cor or 'Sem cor'

        if id_edicao is None:
            # Adicionar novo registro
            query = f"""INSERT INTO Frota (placa, marca, modelo, venc_documento, venc_seguro, oleo, obs, cor, status)
                        VALUES ('{placa}','{marca}','{modelo}','{venc_documento}','{venc_seguro}','{oleo}','{obs}','{cor}','{status}')"""
        else:
            # Atualizar registro existente
            query = f"""UPDATE Frota SET marca = '{marca}', modelo = '{modelo}', venc_documento = '{venc_documento}', venc_seguro = '{venc_seguro}',
                        oleo = '{oleo}', obs = '{obs}', cor = '{cor}', status = '{status}' WHERE id = {id_edicao}"""
            if status != 'Alugado':
                Alugueis.excluir_aluguel(id_edicao, edicao=True)
        executar_query(conexao, query)
       
    # ------------------------------------------------------------------
    
    " FUNÇÃO QUE EXCLUI OS DADOS NA TABELA "

    def excluir_carro(id_carro: int):
        conexao = conexao_bd()
        query = f"""
        DELETE FROM Frota
        WHERE id = {id_carro}
        """
        executar_query(conexao, query)
        loggerBd.debug(f"Carro excluído da frota - ID: {id_carro}...")

        query = f"""
        DELETE FROM CarrosAlugados
        WHERE frota_id = {id_carro}
        """
        executar_query(conexao, query)
        loggerBd.debug(f"Carro excluído dos aluguéis - ID: {id_carro}...")

    # ------------------------------------------------------------------
            
    " FUNÇÃO QUE VERIFICA OS CARROS DA FROTA COM ALGUMA ESPECIFICIDADE "

    def carros_frota(coluna, condicao, valor):
        conexao = conexao_bd()
        cursor = conexao.cursor()
        query = f"""
        SELECT {coluna} FROM Frota 
        WHERE {condicao} = '{valor}';
        """
        cursor.execute(query)
        carros_frota = cursor.fetchall()
        loggerBd.debug(f"Verificando Carros da frota...")

        return carros_frota
    
    # ------------------------------------------------------------------

# ======================================================================



# ======================================================================

""" CLASSE QUE SE REFERE AS TABELAS DE FINANÇAS NO BD / FUNÇÕES CRUD (CREATE, UPDATE, DELETE) DAS TABELAS """

class Financeiro:

    # ------------------------------------------------------------------
    """ =================== FUNÇÕES ABAIXO SÃO DA TABELA 'FinanceiroAlugueis' =================== """
    # ------------------------------------------------------------------

    """ FUNÇÃO QUE RETORNA A VISUALIZAÇÃO DOS DADOS DA TABELA 'FinanceiroAlugueis' """

    def mostrar_financeiro_aluguel(page):
        texto1 = "Deseja realmente excluir este financeiro?"
        texto2 = "Atenção, a exclusão desse financeiro, não apagara o aluguel referente a ele!"
        conexao = conexao_bd()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM FinanceiroAlugueis")
        dados_financeiro = cursor.fetchall()
        rows = []
        for financeiro in dados_financeiro:
            id_financeiro, entradas, placa, data, lucros_admin, bruto_empresa, lucros_empresa = financeiro
            row = ft.DataRow([
                ft.DataCell(ft.Text(id_financeiro)),
                ft.DataCell(ft.Text(ut.formatar_valor(entradas))),
                ft.DataCell(ft.Text(placa)),
                ft.DataCell(ft.Text(data)),
                ft.DataCell(ft.Text(ut.formatar_valor(lucros_admin))),
                ft.DataCell(ft.Text(ut.formatar_valor(bruto_empresa))),
                ft.DataCell(ft.Text(ut.formatar_valor(lucros_empresa)))],
                on_select_changed = lambda e, id_financeiro=id_financeiro: 
                modal_exclusao(id_financeiro, page, texto1, texto2, Financeiro.excluir_financeiro_aluguel))      
            rows.append(row)
        return rows
    
    # ------------------------------------------------------------------

    """ FUNÇÃO QUE EXCLUI DADOS DA TABELA 'FinanceiroAlugueis' """

    def excluir_financeiro_aluguel(id_financeiro: int):
        conexao = conexao_bd()
        query = f"""
        DELETE FROM FinanceiroAlugueis
        WHERE id = {id_financeiro}
        """
        executar_query(conexao, query)
        loggerBd.debug(f"Valores excluídos do Financeiro - ID: {id_financeiro}...")

    # ------------------------------------------------------------------
        
    """ FUNÇÃO QUE RETORNA A SOMA TOTAL DAS COLUNAS DA TABELA 'FinanceiroAlugueis' """

    def financeiro_aluguel_total():
        conexao = conexao_bd()
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT (SELECT COALESCE(SUM(saida), 0) FROM FinanceiroDividas WHERE tipo = 'Aluguel'),
        COALESCE(SUM(valor), 0), 
        COALESCE(SUM(lucro_admin), 0), 
        COALESCE(SUM(liquido_empresa), 0) FROM FinanceiroAlugueis;
                       """)

        gastos_dividas, valor_alugueis, lucro_admin, liquido_empresa = cursor.fetchone()

        liquido_empresa_total = liquido_empresa - gastos_dividas

        rows = [ft.DataRow([
        ft.DataCell(ft.Text(ut.formatar_valor(round(valor_alugueis)))),
        ft.DataCell(ft.Text(ut.formatar_valor(round(gastos_dividas)))),
        ft.DataCell(ft.Text(ut.formatar_valor(round(lucro_admin)))),
        ft.DataCell(ft.Text(ut.formatar_valor(round(liquido_empresa_total))))
        ])]
        
        return rows
    
    # ------------------------------------------------------------------

    """ FUNÇÃO QUE CRIA E ADICIONA OS DADOS NA TABELA 'FinanceiroAlugueis' """

    def adicionar_financeiro_aluguel(entrada, placa, data, flag=None):
        try:
            lucro_admin = round((30 / 100) * entrada, 2)
            liquido_empresa = round(entrada - lucro_admin, 2)
        except Error as e:
            loggerBd.critical(f"Erro ao adicionar valores no Financeiro: {e}...")
            return None        
        conexao = conexao_bd()
        if flag is None:
            
            query = f"""
            INSERT INTO FinanceiroAlugueis (valor, placa, data, lucro_admin, bruto_empresa, liquido_empresa)
            VALUES ({entrada}, '{placa}', '{data}', {lucro_admin}, {entrada}, {liquido_empresa})
            """
            executar_query(conexao, query)
        else:
            query = f"""
            UPDATE FinanceiroAlugueis SET valor = {entrada}, lucro_admin = {lucro_admin}, bruto_empresa = {entrada}, liquido_empresa = {liquido_empresa}
            WHERE placa = '{placa}' AND data = '{data}'
            """
            cursor = conexao.cursor()
            cursor.execute(query)
            conexao.commit()
            if cursor.rowcount == 0:
                query = f"""
                INSERT INTO FinanceiroAlugueis (valor, placa, data, lucro_admin, bruto_empresa, liquido_empresa)
                VALUES ({entrada}, '{placa}', '{data}', {lucro_admin}, {entrada}, {liquido_empresa})
                """
                executar_query(conexao, query)
    
        loggerBd.debug(f"Valores Adicionados no Financeiro - Valor: {entrada} - Placa: {placa}...")


    # ------------------------------------------------------------------
    """ =================== FUNÇÕES ABAIXO É DA TABELA GERAL =================== """
    # ------------------------------------------------------------------
    
    """ FUNÇÃO QUE RETORNA A VISUALIZAÇÃO DOS DADOS DA TABELA GERAL """

    # obs: essa é a única função cujo não possui tabela no BD, apenas realiza a consulta em outras tabelas existentes
    def mostrar_financeiro(page):
        conexao = conexao_bd()
        cursor = conexao.cursor()
        cursor.execute("""SELECT 
            (SELECT COALESCE(SUM(valor), 0) FROM FinanceiroAlugueis),
            (SELECT COALESCE(SUM(lucro_admin), 0) FROM FinanceiroAlugueis),
            (SELECT COALESCE(SUM(entrada), 0) FROM FinanceiroDividas),
            (SELECT COALESCE(SUM(saida), 0) FROM FinanceiroDividas);
                        """)

        entradas_alugueis, saidas_alugueis, entradas_dividas, saidas_dividas = cursor.fetchone()

        entrada = round(entradas_alugueis + entradas_dividas, 2)
        saida = round(saidas_dividas + saidas_alugueis, 2)
        liquido = round(entrada - saida, 2)

        rows = [ft.DataRow([
        ft.DataCell(ft.Text(ut.formatar_valor(entrada))),
        ft.DataCell(ft.Text(ut.formatar_valor(saida))),
        ft.DataCell(ft.Text(ut.formatar_valor(entrada))),
        ft.DataCell(ft.Text(ut.formatar_valor(liquido)))
        ])]

        return rows


    # ------------------------------------------------------------------
    """ =================== FUNÇÕES ABAIXO SÃO DA TABELA 'FinanceiroDividas' =================== """
    # ------------------------------------------------------------------

    """ FUNÇÃO QUE RETORNA A VISUALIZAÇÃO DOS DADOS DA TABELA 'FinanceiroDividas' """

    def mostrar_dividas(page):
        texto1 = "Deseja realmente excluir este financeiro?"
        texto2 = "Atenção, a exclusão desse financeiro acarreta na mudança dos valores da Tabela Geral de Finanças!"

        conexao = conexao_bd()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM FinanceiroDividas")
        dados_dividas = cursor.fetchall()
        rows = []
        
        for dividas in dados_dividas:
            id_divida, entradas, saidas, tipo, obs = dividas
            row = ft.DataRow([
                ft.DataCell(ft.Text(id_divida)),
                ft.DataCell(ft.Text(ut.formatar_valor(entradas))),
                ft.DataCell(ft.Text(ut.formatar_valor(saidas))),
                ft.DataCell(ft.Text(tipo)),
                ft.DataCell(ft.Text(obs))],
                on_select_changed=lambda e, id_divida=id_divida: modal_exclusao(id_divida, page, texto1, texto2, Financeiro.excluir_divida))
            rows.append(row)
        return rows
    
    # ------------------------------------------------------------------

    """ FUNÇÃO QUE RETORNA A SOMA TOTAL DAS COLUNAS DA TABELA 'FinanceiroDividas' """

    def dividas_total():
        conexao = conexao_bd()
        cursor = conexao.cursor()

        cursor.execute("SELECT COALESCE(SUM(entrada), 0), COALESCE(SUM(saida), 0) FROM FinanceiroDividas;")
        entrada_total, saida_total = cursor.fetchone()
        liquido_total = round(entrada_total - saida_total, 2)

        rows = [ft.DataRow([
        ft.DataCell(ft.Text(ut.formatar_valor(entrada_total))),
        ft.DataCell(ft.Text(ut.formatar_valor(saida_total))),
        ft.DataCell(ft.Text(ut.formatar_valor(liquido_total))),
        ])]
        return rows
    
    # ------------------------------------------------------------------

    """ FUNÇÃO QUE CRIA E ADICIONA OS DADOS NA TABELA 'FinanceiroDividas' """

    def adicionar_dividas(entrada, saida, tipo, obs, conexao):
        query = f""" INSERT INTO FinanceiroDividas (entrada, saida, tipo, obs)
        VALUES ({entrada}, {saida}, '{tipo}', '{obs}') """
        executar_query(conexao, query)
        loggerBd.debug("Registro de dívida adicionado com sucesso!")

    # ------------------------------------------------------------------
        
    " FUNÇÃO QUE EXCLUI OS DADOS NA TABELA "

    def excluir_divida(id_divida: int):
        conexao = conexao_bd()
        query = f"""
        DELETE FROM FinanceiroDividas
        WHERE id = {id_divida}
        """
        executar_query(conexao, query)
        loggerBd.debug(f"Valor excluído de Finanças - ID: {id_divida}...")

    # ------------------------------------------------------------------
        
            
# ======================================================================



# ======================================================================
    
""" CLASSE QUE SE REFERE A TABELA 'CarrosAlugados' NO BD / FUNÇÕES CRUD (CREATE, UPDATE, DELETE) DA TABELA """

class Alugueis:  

    # ------------------------------------------------------------------

    """ FUNÇÃO QUE RETORNA A VISUALIZAÇÃO DOS DADOS DA TABELA """

    def mostrar_alugueis(page):
        texto1 = "Deseja realmente excluir o aluguel?"
        texto2 = "Atenção, a exclusão causara a disponibilidade do carro na Frota!"
        conexao = conexao_bd()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM CarrosAlugados")
        dados_alugueis = cursor.fetchall()
        
        rows = []
        for alugueis in dados_alugueis:
            id_aluguel, frota_id, nome, endereco, identidade, data_aluguel, data_devolucao, obs, valor_aluguel, valor_pago = alugueis
            placa_numero = placa(conexao, frota_id) 

            row = ft.DataRow([
                ft.DataCell(ft.Text(id_aluguel)), ft.DataCell(ft.Text(frota_id)), ft.DataCell(ft.Text(str(nome))),
                ft.DataCell(ft.Text(str(endereco))), ft.DataCell(ft.Text(str(identidade))), ft.DataCell(ft.Text(str(data_aluguel))),
                ft.DataCell(ft.Text(str(data_devolucao))), ft.DataCell(ft.Text(str(obs))), 
                ft.DataCell(ft.Text(ut.formatar_valor(valor_aluguel))), ft.DataCell(ft.Text(ut.formatar_valor(valor_pago))), 
                ft.DataCell(ft.Text(placa_numero))],

                on_select_changed = lambda e, id_aluguel=id_aluguel: modal_aluguel(page, id_aluguel),
                on_long_press=lambda e, id_aluguel=id_aluguel: modal_exclusao(id_aluguel, page, texto1, texto2, Alugueis.excluir_aluguel))
            rows.append(row)
           
        return rows

    # ------------------------------------------------------------------
    
    # ------------------------------------------------------------------

    """ FUNÇÃO QUE CRIA E ADICIONA OS DADOS NA TABELA """

    def adicionar_aluguel(nome, endereco, identidade, data_retirada, data_devolucao, obs, valor, valor_pago, frota_id, id_aluguel=None):
        conexao = conexao_bd()
        endereco = endereco or 'Sem Endereço'
        identidade = identidade or 'Sem Identidade'
        obs = obs or 'Sem observações'

        placa_numero = placa(conexao, frota_id)

        if id_aluguel is None:
            
            query1 = f""" INSERT INTO CarrosAlugados (nome, endereco, identidade, data_retirada, data_devolucao, obs, valor, valor_pago, frota_id)
            VALUES ('{nome}', '{endereco}', '{identidade}', '{data_retirada}', '{data_devolucao}', '{obs}', {valor}, {valor_pago}, {frota_id}) """
            executar_query(conexao, query1)
            loggerBd.debug("Registro de aluguel adicionado com sucesso!")

            query2 = f""" UPDATE Frota SET status = 'Alugado' WHERE id = {frota_id} """
            executar_query(conexao, query2)
            loggerBd.debug("Status do carro atualizado para 'Alugado'.")

            Financeiro.adicionar_financeiro_aluguel(valor_pago, placa_numero, data_retirada)
        else:
            query = f"""UPDATE CarrosAlugados SET nome = '{nome}', endereco = '{endereco}', identidade = '{identidade}', data_devolucao = '{data_devolucao}',
                     obs = '{obs}', valor = {valor}, valor_pago = {valor_pago} WHERE id = {id_aluguel}"""
            executar_query(conexao, query)
            Financeiro.adicionar_financeiro_aluguel(valor_pago, placa_numero, data_retirada, True)
            
    # ------------------------------------------------------------------
            
    """ FUNÇÃO QUE EXCLUI DADOS DA TABELA """        

    def excluir_aluguel(id_aluguel: int, edicao=None):
        conexao = conexao_bd()
        cursor = conexao.cursor()
        query_id = f""" SELECT * FROM CarrosAlugados WHERE id = {id_aluguel} """
        cursor.execute(query_id)
        aluguel_excluido = cursor.fetchone()
        if aluguel_excluido is not None:
            _, frota_id, nome, endereco, identidade, data_retirada, data_devolucao, obs, valor, valor_pago = aluguel_excluido
            Historico.adicionar_historico(nome, endereco, identidade, data_retirada, data_devolucao, obs, valor, valor_pago)
            Clientes.adicionar_cliente(nome, endereco, identidade)

            query1 = f"""
                        DELETE FROM CarrosAlugados
                        WHERE id = {id_aluguel}
                    """
            executar_query(conexao, query1)
            loggerBd.debug(f"Aluguel excluído - ID: {id_aluguel}...")

        if edicao is None:
            query2 = f""" UPDATE Frota SET status = 'Disponivel' WHERE id = {frota_id}; """
            executar_query(conexao, query2)
            loggerBd.debug(f"Status do carro atualizado para 'Disponivel' - ID: {frota_id}...")

    # ------------------------------------------------------------------
    
    """ FUNÇÃO QUE RETORNA OS DADOS DA TABELA COM BASE EM UM ID, PARA FUTURA EDIÇÃO DO MESMO """        

    def aluguel_edit(id_aluguel):
        conexao = conexao_bd()
        cursor = conexao.cursor()
        query_id = f""" SELECT * FROM CarrosAlugados WHERE id = {id_aluguel} """
        cursor.execute(query_id)
        aluguel_edit = cursor.fetchone()
        return aluguel_edit
    
    # ------------------------------------------------------------------

# ======================================================================




# ======================================================================
        
""" CLASSE QUE SE REFERE A TABELA 'Historico' NO BD / FUNÇÕES CRUD (CREATE, UPDATE, DELETE) DA TABELA """

class Historico:

    # ------------------------------------------------------------------

    """ FUNÇÃO QUE RETORNA A VISUALIZAÇÃO DOS DADOS DA TABELA """

    def mostrar_historico(page):
        conexao = conexao_bd()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Historico")
        dados_historico = cursor.fetchall()
        rows = []
        for historico  in dados_historico:
            row = ft.DataRow([ft.DataCell(ft.Text(dado)) for dado in historico])            
            rows.append(row)
        return rows
    
    # ------------------------------------------------------------------

    """ FUNÇÃO QUE CRIA E ADICIONA OS DADOS NA TABELA """

    def adicionar_historico(nome, endereco, identidade, data_retirada, data_devolucao, obs, valor, valor_pago):
        conexao = conexao_bd()
        query = f""" INSERT INTO Historico (nome, endereco, identidade, data_retirada, data_devolucao, obs, valor, valor_pago)
        VALUES ('{nome}', '{endereco}', '{identidade}', '{data_retirada}', '{data_devolucao}', '{obs}', {valor}, {valor_pago}) """
        executar_query(conexao, query)
        loggerBd.debug("Registro histórico adicionado com sucesso!")

    # ------------------------------------------------------------------

# ======================================================================
    


# ======================================================================
        
""" CLASSE QUE SE REFERE A TABELA 'Clientes' NO BD / FUNÇÕES CRUD (CREATE, UPDATE, DELETE) DA TABELA """

class Clientes:

    # ------------------------------------------------------------------

    """ FUNÇÃO QUE RETORNA A VISUALIZAÇÃO DOS DADOS DA TABELA """

    def mostrar_clientes(page):
        conexao = conexao_bd()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Clientes")
        dados_clientes = cursor.fetchall()
        rows = []
        for clientes in dados_clientes:
            row = ft.DataRow([ft.DataCell(ft.Text(dado)) for dado in clientes])            
            rows.append(row)
        return rows
    
    # ------------------------------------------------------------------

    """ FUNÇÃO QUE CRIA E ADICIONA OS DADOS NA TABELA """

    def adicionar_cliente(nome, endereco, identidade):
        conexao = conexao_bd()
        query = f""" INSERT INTO Clientes (nome, endereco, identidade) VALUES ('{nome}', '{endereco}', '{identidade}') """
        executar_query(conexao, query)
        loggerBd.debug("Registro de Cliente adicionado com sucesso!")
    
    # ------------------------------------------------------------------

# ======================================================================

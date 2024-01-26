# ======================================================================

import flet as ft
import logging
import logging.config
import os
import time
import widgets as wd
import plotting as pt
from pages import page_frota, page_aluguel, page_historico, page_clientes, page_financeiro, page_financeiro_aluguel, page_dividas, page_ajuda

# ======================================================================

# Definindo um variável de escopo global
selected_index_global = None

# ======================================================================

""" CONFIGURAÇÃO DOS LOGS """

dir_atual = os.path.dirname(os.path.abspath(__file__))
dir_logconf = os.path.join(dir_atual, ".log.ini")
dir_log = os.path.join(dir_atual, "logs.log")
logging.config.fileConfig(dir_logconf, defaults={'log_path': dir_log.replace('\\', '\\\\')})
loggerDebug = logging.getLogger('debug')
loggerDb = logging.getLogger('bdebug')

# ======================================================================

""" FUNÇÃO PRINCIPAL DO FLET """

def main(page: ft.Page):
    # ------------------------------------------------------------------

    """ SETA A JANELA PARA O TAMANHO MAXIMIZADO E COM SCROLL AUTOMÁTICO + TÍTULO DA JANELA """

    page.window_maximized = True
    page.auto_scroll = True
    page.title = "Gerenciamento de Aluguéis de Veículo"

    # ------------------------------------------------------------------
    
    """ REALIZA A VERIFICAÇÃO DE MINIMIZAÇÃO DA JANELA """

    def page_resize(e):
        # Verifica se foi minimizado para valores abaixo de 1000x600
        if page.window_width < 1000.0 or page.window_height < 600.0:
            # se sim, realiza a abertura do aviso
            page.banner.open = True
            page.update()
            loggerDebug.info("A página foi redimensionada...")

    def acao(e):
        # fecha o aviso
        page.banner.open = False
        # maximiza a janela novamente
        page.window_maximized = True
        page.update()

    titulo_aviso = "Ops! Parece que você minimizou a aplicação. Por favor, maximize novamente! 😊"

    # definição do aviso, ao ser fechado redireciona para a função "acao"
    page.banner = wd.criar_aviso(titulo_aviso, acao)

    # função que verifica todas os redimensionamentos de tela realizado na janela atual
    page.on_resize = page_resize
    page.update()

    # ------------------------------------------------------------------

    """ FUNÇÃO QUE INDEXA CADA PÁGINA DO MENU LATERAL E RENDERIZA CADA PÁGINA """

    def index_pagina(e):
        page.clean()

        # Seta a variável como um escopo global 
        global selected_index_global
        # e.control.selected_index é o index da página selecionada
        selected_index_global = e.control.selected_index

        # realiza um match case para determina a partir do index a qual página você será direcionado
        match e.control.selected_index:
            case 1:
                # cada page.add adiciona uma nova página em cima da página atual
                # cada elemento da página é criado dentro de sua respectiva função e renderizado pelo page.add
                page.add(page_aluguel(page, rail))
            case 2:
                page.add(page_frota(page, rail))
            case 3:
                page.add(page_historico(page, rail))
            case 4:
                page.add(page_clientes(page, rail))
            case 5:
                page.add(page_financeiro(page, rail))
            case 6:
                page.add(page_financeiro_aluguel(page, rail))
            case 7:
                page.add(page_dividas(page, rail))
            case _:
                home()

    # ------------------------------------------------------------------
                
    """ LISTA COM TODOS OS DESTINOS DO MENU LATERAL, SEUS ÍCONES E PROPRIEDADES GRÁFICAS """    

    destinos = [
        ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.MENU), label="Home"),
        ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.CAR_RENTAL_OUTLINED),
                                     selected_icon_content=ft.Icon(ft.icons.CAR_RENTAL),
                                     label="Aluguéis"),
        ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.DIRECTIONS_CAR_OUTLINED),
                                     selected_icon_content=ft.Icon(ft.icons.DIRECTIONS_CAR),
                                     label="Frota"),
        ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.UNARCHIVE_OUTLINED),
                                     selected_icon_content=ft.Icon(ft.icons.UNARCHIVE),
                                     label="Histórico"),
        ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.GROUPS_OUTLINED),
                                     selected_icon_content=ft.Icon(ft.icons.GROUPS),
                                     label="Clientes"),
        ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.MONETIZATION_ON_OUTLINED),
                                     selected_icon_content=ft.Icon(ft.icons.MONETIZATION_ON),
                                     label="Financeiro"),
        ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.TRENDING_UP),
                                     label="Lucros"),
        ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.TRENDING_DOWN),
                                     label="Dividas")]
    
    # ------------------------------------------------------------------

    """ FUNÇÃO QUE CRIA E RENDERIZA DE FATO O MENU LATERAL POR COMPLETO """

    rail = wd.criar_navrail(destinos, index_pagina)

    # ------------------------------------------------------------------

    """ FUNÇÃO QUE REALIZA A RENDERIZAÇÃO DAS TROCAS DE TEMAS ENTRE 'LIGHT' E 'DARK' """

    def tema(e):
        # Verifica se o tema atual é light, se sim, troca para dark, se não mantém em dark
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        icon_tema = appbar.actions[0]
        # realiza a troca do ícone do botão
        icon_tema.icon = ft.icons.DARK_MODE_OUTLINED if page.theme_mode == "dark" else ft.icons.WB_SUNNY_OUTLINED
        loggerDebug.info(f"A página está no modo {page.theme_mode}...")
        # verifica se o index selecionado é o index da página home e renderiza novamente todo os gráficos
        if selected_index_global == 0:
            home()
        page.update()

    # ------------------------------------------------------------------

    """ FUNÇÃO DO BOTÃO PARA REDIRECIONAR AO GITHUB """

    def github(e):
        page.launch_url('https://github.com/kakanetwork')
        loggerDebug.info("O link do github foi acessado...")

    # ------------------------------------------------------------------

    """ FUNÇÃO DO BOTÃO PARA REDIRECIONAR AO MENU DE AJUDA """

    def ajuda(e):
        page.clean()
        page.add(page_ajuda(rail))

    # ------------------------------------------------------------------
    
    """ DEFINIÇÕES, CRIAÇÃO E RENDERIZAÇÃO DA APPBAR (BARRA SUPERIOR) """

    titulo = "Gerenciamento de Aluguéis de Veículo"
    appbar = wd.criar_appbar(titulo, tema, github, ajuda, ft.icons.CODE)
    page.appbar = appbar

    # ------------------------------------------------------------------

    """ FUNÇÃO DA PÁGINA HOME ONDE TODOS OS ELEMENTOS SÃO CRIADOS E ARMAZENADOS """

    def home():
        page.clean()
        global selected_index_global
        selected_index_global = 0

        # Progress ring é um elemento de carregamento, onde ele é renderizado enquanto os gráficos estão sendo calculados e carregados.
        progress_ring = ft.Row([ft.Column(
            [ft.Text("Carregando Gráficos...\n", weight=ft.FontWeight.BOLD,
                     size=20), ft.ProgressRing(stroke_width=7)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
            )],
            alignment=ft.MainAxisAlignment.CENTER, expand=True
        )
        
        page.add(progress_ring)

        # Funções que são chamadas para criar os gráficos da página home
        grafico_linha = pt.grafico_linhas(page.theme_mode)
        grafico_linhas2= pt.grafico_linhas2()
        time.sleep(1)

        # remove o elemento de carregamento após os gráficos estarem prontos
        page.remove(progress_ring)

        # realiza todo o carregamento e renderização de todos os elementos da página e suas propriedades
        page.add(
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        [
                            ft.Row([
                                grafico_linha
                            ]),
                            ft.Row([
                                grafico_linhas2
                            ])
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        expand=True)
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
                expand=True
            ))

    # ------------------------------------------------------------------

    home()

    # ------------------------------------------------------------------

ft.app(main)

# ======================================================================

# TODO: Criar BD automaticamente caso não exista
# TODO: Criar PERFIS com nome para poder realizar a troca, onde cada perfil terá seu próprio BD
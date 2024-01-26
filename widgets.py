import flet as ft

# ======================================================================

" FUNÇÃO QUE CRIA UMA APPBAR "

def criar_appbar(titulo: str, tema: callable, acao: callable,ajuda: callable, icone: str):
    return ft.AppBar(
                leading=ft.IconButton(
                    icon=icone,
                    on_click=acao,
                    tooltip="Suporte de Código",
                    style=ft.ButtonStyle(color={"": ft.colors.WHITE})
                ),
                bgcolor="#003377",
                title=ft.Text(titulo, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                center_title=True,
                actions=[
                    
                    ft.IconButton(
                        on_click=tema,
                        icon=ft.icons.WB_SUNNY_OUTLINED,
                        tooltip="Trocar tema",
                        style=ft.ButtonStyle(color={"": ft.colors.WHITE})
                    ),
                    ft.IconButton(
                        on_click=acao,
                        icon=ft.icons.PERSON_OUTLINED,
                        tooltip="Trocar Usuário",
                        style=ft.ButtonStyle(color={"": ft.colors.WHITE})
                    ),
                    ft.IconButton(
                        on_click=ajuda,
                        icon=ft.icons.HELP_OUTLINE,
                        tooltip="Ajuda",
                        style=ft.ButtonStyle(color={"": ft.colors.WHITE})
                    ),
                ],
            )

# ======================================================================

" FUNÇÃO QUE CRIA UMA NAVRAIL "

def criar_navrail(destinos: list, on_change: callable):
    return ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=destinos,
        group_alignment=-1.0,
        on_change=on_change
    )

# ======================================================================

" FUNÇÃO QUE CRIA UMA MODAL "

def criar_modal(titulo: str, campos_modal: list, fechar_modal: callable, confirmar_modal: callable, botao1="Cancelar", botao2="Adicionar"):
    return ft.AlertDialog(
        modal=True,
        title=ft.Text(titulo, weight=ft.FontWeight.W_900),
        content=campos_modal,
        actions=[
            ft.TextButton(botao1, on_click=fechar_modal),
            ft.TextButton(botao2, on_click=confirmar_modal),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

# ======================================================================

" FUNÇÃO QUE CRIA UMA AVISO "

def criar_aviso(titulo: str, acao: callable):
    return ft.Banner(
        bgcolor=ft.colors.AMBER_900,
        leading=ft.Icon(ft.icons.WARNING_AMBER_SHARP),
        content=ft.Text(titulo),
        actions=[
            ft.TextButton("OK", on_click=acao),
        ],
    )
        
# ======================================================================

" FUNÇÃO QUE CRIA UMA DATATABLE/DATAROW "

def criar_datarow(cabecario: list, itens: callable):
    return ft.DataTable(
            border=ft.border.all(0.7, "#8c8c8c"),
            border_radius=0,
            column_spacing=15,
            horizontal_lines=ft.BorderSide(color='#8c8c8c', width=0.1),
            vertical_lines=ft.BorderSide(color='#3d3d3d', width=0.2),
            show_bottom_border=True,
            heading_row_color='#003377',
            heading_text_style=ft.TextStyle(color='white', weight=ft.FontWeight.BOLD),
            columns=cabecario,
            rows=itens)

# ======================================================================

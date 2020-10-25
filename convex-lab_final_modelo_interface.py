def web_report(file_BD):
    
    # Libraries ------------------------------------------
    # - App creation -------------------------------------

    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    import dash_table
    import dash_daq as daq
    import dash_bootstrap_components as dbc
    from dash.dependencies import Input, Output, State

    # - Data manipulation --------------------------------

    import pandas as pd
    import numpy as np
    from datetime import datetime
    from datetime import timedelta
    import sqlite3

    # - Data visualuzation -------------------------------

    import plotly.graph_objects as go
    import plotly.express as px

    # - Other libraries ----------------------------------

    import warnings
    warnings.filterwarnings('ignore')

    # ----------------------------------------------------
    # - Funções auxiliares -------------------------------

    def create_df(table):
        conn = sqlite3.connect(file_BD)
        df = pd.read_sql_query("SELECT * FROM "+table+";",conn)
        # Entradas ----
        if table == 'aluno':
            df = df.rename(columns={'id': 'ID', 'cpf': 'CPF', 'nome': 'Nome', 'email': 'E-mail', 'telefone': 'Telefone',
                                    'nome_responsavel': 'Responsável', 'telefone_responsavel': 'Telefone do Responsável',
                                    'nome_escola_origem': 'Escola de Origem','turma_id': 'Turma (ID)',
                                    'reprova':'Reprova?','continua':'Continua?'})        
        if table == 'formulario_inscricao':
            df = df.rename(columns={'id':'ID','nome':'Nome','cpf':'CPF','escola_id':'ID da Escola','serie_id':'ID da Série',
                                    'data_inscricao':'Data de Inscrição','ano_referencia':'Ano de Referência',
                                    'email_aluno':'E-mail','telefone_aluno':'Telefone','nome_responsavel':'Nome do Responsável',
                                    'telefone_responsavel':'Tel. do Responsável','nome_escola_origem':"Escola de Origem"})  
        if table == 'escola':
            df = df.rename(columns={'id':'ID','nome':'Nome','regiao_id':'ID da Região'})     
        if table == 'regiao':
            df = df.rename(columns={'id':'ID','nome':'Nome'})            
        if table == 'turma':
            df = df.rename(columns={'id':'ID','nome':'Nome','qtd_max_alunos':'N. Máx. Alunos',
                                    'qtd_professores_acd':'N. Máx. Prof. ACD',
                                    'qtd_professores_pedagogico':'N. Máx. Prof. Pedag.','escola_id':'ID da Escola',
                                    'serie_id':'ID da Série'}) 
        # Saídas ----
        if table == 'sol_aluno':
            df = df.rename(columns={'id': 'ID', 'cpf': 'CPF', 'nome': 'Nome', 'email': 'E-mail', 'telefone': 'Telefone',
                                    'nome_responsavel': 'Responsável', 'telefone_responsavel': 'Telefone do Responsável',
                                    'nome_escola_origem': 'Escola de Origem','sol_turma_id': 'Turma (ID)'})
        if table == 'sol_priorizacao_formulario' or table == 'sol_relatorio_formulario_nao_alocados':
            df = df.rename(columns={'id':'ID','nome':'Nome','cpf':'CPF','email_aluno':'E-mail','telefone_aluno':'Telefone',
                                    'nome_responsavel':'Nome do Responsável',
                                    'escola_id':'ID da Escola','serie_id':'ID da Série','nome_escola_origem':"Escola de Origem",
                                    'sol_turma_id': 'Turma (ID)','status_id':'Status'})
        if table == 'sol_turma':
            df = df.rename(columns={'id':'ID','nome':'Nome','qtd_max_alunos':'Num. Max de Alunos',
                                    'qtd_professores_acd':'N. Profs. ACD','qtd_professores_pedagogico':'N. Profs. Pedagógico',
                                    'escola_id':'ID da Escola','serie_id':'ID da Série','aprova':'Aprovado?'})
        if table == 'sol_relatorio_turma':
            df = df.rename(columns={'id':'ID','nome':'Turma','qtd_alunos_continuidade_alocados':'N. Continuidade',
                                    'qtd_alunos_formulario_alocados':'N. Formulário','qtd_max_alunos':'Qtd. Max. de Alunos',
                                    'proporcao_alunos_alocados':'Proporção de Alunos Alocados','total_alunos':'N. Total de Alunos'})
        if table == 'sol_relatorio_orcamento':
            df = df.rename(columns={'id':'ID','nome':'Nome','qtd_alunos_continuidade':'N. Alunos Continuidade',
                                    'qtd_alunos_formulario':'N. Alunos. Formulário','total_alunos':'N. Alunos Total',
                                    'custo_turma':'Custo da Turma','limite_custo':'Limite de Custo',
                                    'proporcao_custo_turma':"Prop. Custo Turma"})        
        return df

    def get_par(df_parametro,chave):
        return int(df_parametro.valor[df_parametro.chave==chave])

    def sunburst(table):

        df = create_df(table)
        fig2 = px.sunburst(df, path=['regiao_nome', 'escola_nome', 'serie_nome','nome'], values='total_alunos',
                           color='total_alunos',color_continuous_scale= ["white", "gray", "black"])
        fig2.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            margin={"r":0,"t":25,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')

        fig2.update_traces(hovertemplate=None)

        return fig2

    # ----------------------------------------------------
    # - Starting the app ---------------------------------

    app = dash.Dash(__name__,
                    external_stylesheets=[dbc.themes.SKETCHY],
                    meta_tags=[{'name': 'viewport',
                                'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                   )
    app.title = 'Convex-Lab App'
    server = app.server
    # ----------------------------------------------------
    # -- Layout ------------------------------------------

    # --- Navbar -----------------------------------------

    app.layout = html.Div([

        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Relatórios", href='/l/components/"button-in-1')),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Relatórios", header=True),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Sobre o Modelo", href="https://910d7474-b707-4eb1-978f-f95d4e7986d6.filesusr.com/ugd/c96224_2214fd87540d43b7ba6c9130ece15acc.pdf"),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Sobre o Desafio", href="https://www.unisoma.com.br/desafio/"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Menu",
                ),
            ],
            brand="Solução Convex-Lab",
            brand_href="#",
            color="primary",
            dark=True,
        ),
    # -----------------------------------------------------
        html.Br(),
        dbc.Row([
            dbc.Col([

                dbc.Jumbotron([
                    html.H2("Desafio UniSoma 2020"),
                    dcc.Markdown('''
                    Seja bem vindo ao relatório web do grupo Convex-Lab
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ), 

                    html.Hr(),
                    dcc.Markdown('''
                    Aqui você poderá avaliar as entradas e saídas do modelo que desenvolvemos. Clique nas janelas para
                    expandi-las. Você poderá encontrar mais informações sobre o modelo no relatório descritivo do modelo,
                    que pode ser acessado pelo menu acima.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ), 
                ]),

            ],xs = 11, md = 10, xl = 8)
        ], justify = 'center'),
        html.Br(),



    # - Entradas do Modelo ------------------------------

        dbc.Row([html.Br()]),
        dbc.Row([
            dbc.Col([
                html.H3(children = "Entradas do modelo"),
                dcc.Markdown('''
                    São informações fornecidas préviamente pela ONG e que podem alterar as saídas do modelo, de acordo com os 
                    valores atribuídos. O modelo desenvolvido não altera os valores do modelo. As tabelas geradas permitem a 
                    filtragem e ordenação dos valores. Você também pode esconder alguns colunas. Para recuperar as colunas 
                    escondidas, clique em "Toggle Columns".
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ),   
            ],xs = 11, md = 10, xl = 8)
        ], justify = 'center'),

    # --- Input: Alunos de Continuidade -----------------

        dbc.Row([
            dbc.Col([
                dbc.CardHeader(dbc.Button("Alunos de Continuidade Inscritos",
                                          color="link",id="button-in-1",style = {'margin-top': '0%'})                
                ),

            ], xs = 12)
        ], justify = 'center'),

        dbc.Collapse(
            dbc.Row([
                dbc.Col([
                    html.H4(children = "Lista de alunos de continuidade",
                    style = {'margin-top':'3%'}),
                    dcc.Markdown('''
                    Detalha os alunos de continuidade, antes da execução do modelo.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ), 
                    dbc.Alert(
                        "Existem alunos duplicados" if create_df('alerta_aluno_duplicado')['cpf'].count() > 0 else 'Não existem alunos duplicados',
                        color='dark',
                    ),

                    dash_table.DataTable(
                        id='DT-in-alunos-continuidade',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False}
                            if i=="Nome" or i=="Turma (ID)"
                            else {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
                            for i in create_df('aluno').columns
                        ],
                        data=create_df('aluno').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="none",  
                        row_selectable="none",     
                        row_deletable=False,         
        #                 selected_columns=[],        
        #                 selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
        #                 page_size=10,                
                        style_cell={'minWidth': 150, 'width': '300px'},
#                         style_cell={'minWidth': 15, 'maxWidth': 95, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('aluno').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),
                ], xs=11, lg=10, xl=8),
                html.Br(),

            ], justify = 'center'),
            id="collapse-in-1", is_open=False
        ),
    # -------------------------------------------------------
    # --- Input: Alunos de Formulário -----------------------

        dbc.Row([
            dbc.Col([
                dbc.CardHeader(dbc.Button("Alunos de Formulário Inscritos",
                                          color="link",id="button-in-2",style = {'margin-top': '0%'})                
                ),

            ], xs = 12)
        ], justify = 'center'),

        dbc.Collapse(
            dbc.Row([
                dbc.Col([
                    html.H4(children = "Lista de alunos de formulário",
                    style = {'margin-top':'3%'}),
                    dcc.Markdown('''
                    Detalha os alunos de formulário, que são todos os alunos incritos antes da admissão.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ), 
                    
                    dbc.Alert(
                        "Existem alunos duplicados" if create_df('alerta_formulario_duplicado')['cpf'].count() > 0 else 'Não existem alunos duplicados',
                        color='dark',
                    ),

                    dash_table.DataTable(
                        id='DT-in-aluno-formulario',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False}
                            if i=="Nome" or i=="Turma (ID)"
                            else {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
                            for i in create_df('formulario_inscricao').columns
                        ],
                        data=create_df('formulario_inscricao').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="none",  
                        row_selectable="none",     
                        row_deletable=False,         
        #                 selected_columns=[],        
        #                 selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
        #                 page_size=10,                
                        style_cell={'minWidth': 150, 'width': '300px'},
#                         style_cell={'minWidth': 15, 'maxWidth': 95, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('formulario_inscricao').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),
                ], xs=11, lg=10, xl=8),
                html.Br(),

            ], justify = 'center'),
            id="collapse-in-2", is_open=False
        ),
    # -------------------------------------------------------
    # --- Input: Parâmetros, Série e Região -----------------

        dbc.Row([
            dbc.Col([
                dbc.CardHeader(dbc.Button("Parâmetros, Escolas, Regiões, Turmas e Séries",
                                          color="link",id="button-in-3",style = {'margin-top': '0%'})                
                ),

            ], xs = 12)
        ], justify = 'center'),

        dbc.Collapse(
            dbc.Row([
                dbc.Col([
                    html.H4(children = "Parâmetros de entrada",
                    style = {'margin-top':'3%'}),
                    dcc.Markdown('''
                    São os parâmetros de entrada, setados pela ONG.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ),                 

                    dash_table.DataTable(
                        id='DT-in-parametros',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False}
                            if i=="Nome" or i=="Turma (ID)"
                            else {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
                            for i in create_df('parametro').columns
                        ],
                        data=create_df('parametro').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="none",  
                        row_selectable="none",     
                        row_deletable=False,         
        #                 selected_columns=[],        
        #                 selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
        #                 page_size=10,                
                        style_cell={'minWidth': 150, 'width': '300px'},
#                         style_cell={'minWidth': 15, 'maxWidth': 95, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('parametro').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),

                    html.Br(),

                    html.H4(children = "Escolas",
                    style = {'margin-top':'3%'}),
                    dcc.Markdown('''
                    Lista as escolas de onde os alunos se originam.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ),                 

                    dash_table.DataTable(
                        id='DT-in-escola',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False}
                            if i=="Nome" or i=="Turma (ID)"
                            else {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
                            for i in create_df('escola').columns
                        ],
                        data=create_df('escola').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="none",  
                        row_selectable="none",     
                        row_deletable=False,         
        #                 selected_columns=[],        
        #                 selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
        #                 page_size=10,                
                        style_cell={'minWidth': 150, 'width': '300px'},
#                         style_cell={'minWidth': 15, 'maxWidth': 95, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('escola').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),

                    html.Br(),

                    html.H4(children = "Regiões",
                    style = {'margin-top':'3%'}),
                    dcc.Markdown('''
                    Uma lista com as regiões que poderão receber turmas. 
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ),                 

                    dash_table.DataTable(
                        id='DT-in-regiao',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False}
                            if i=="Nome" or i=="Turma (ID)"
                            else {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
                            for i in create_df('regiao').columns
                        ],
                        data=create_df('regiao').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="none",  
                        row_selectable="none",     
                        row_deletable=False,         
        #                 selected_columns=[],        
        #                 selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
        #                 page_size=10,                
                        style_cell={'minWidth': 150, 'width': '300px'},
#                         style_cell={'minWidth': 15, 'maxWidth': 95, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('regiao').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),

                ], xs=11, lg=5, xl=4),

                dbc.Col([
                    html.H4(children = "Turmas",
                    style = {'margin-top':'3%'}),
                    dcc.Markdown('''
                    Lista de turmas atualmente ativas.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ),                 

                    dash_table.DataTable(
                        id='DT-in-turma',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False}
                            if i=="Nome" or i=="Turma (ID)"
                            else {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
                            for i in create_df('turma').columns
                        ],
                        data=create_df('turma').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="none",  
                        row_selectable="none",     
                        row_deletable=False,         
        #                 selected_columns=[],        
        #                 selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
        #                 page_size=10,                
                        style_cell={'minWidth': 150, 'width': '300px'},
#                         style_cell={'minWidth': 15, 'maxWidth': 95, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('turma').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),

                    html.Br(),

                    html.H4(children = "Séries",
                    style = {'margin-top':'3%'}),
                    dcc.Markdown('''
                    Lista de séries atualmente beneficiadas pelo programa.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ),                 

                    dash_table.DataTable(
                        id='DT-in-serie',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False}
                            if i=="Nome" or i=="Turma (ID)"
                            else {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
                            for i in create_df('serie').columns
                        ],
                        data=create_df('serie').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="none",  
                        row_selectable="none",     
                        row_deletable=False,         
        #                 selected_columns=[],        
        #                 selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
        #                 page_size=10,                
                        style_cell={'minWidth': 150, 'width': '300px'},
#                         style_cell={'minWidth': 15, 'maxWidth': 95, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('serie').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),

                ], xs=11, lg=5, xl=4),
                html.Br(),

            ], justify = 'center'),
            id="collapse-in-3", is_open=False
        ),
    # -------------------------------------------------------

        dbc.Row([
            dbc.Col([
                html.Br(),
                html.Hr(),
                html.Br(),
            ],xl = 10)
        ], justify = 'center'),

    # - Saídas do Modelo --------------------------------

        dbc.Row([html.Br()]),
        dbc.Row([
            dbc.Col([
                html.H3(children = "Saídas do modelo"),
                dcc.Markdown('''
                    São informações geradas pelo modelo e adicionadas ao arquivo .db de entrada. Tais informações são obtidas 
                    por meio de variáveis, parâmetros e regras fornecidos pela ONG e apresentados em "Entrada do modelo". Em 
                    **Relatório Geral** você encontrará um resumo dos principais indicadores após a otimização do modelo. 
                    Perceba que a figura central com formato circular (sunburst) é interativa. Você pode clicar na seções 
                    da figura para obter o número de alunos naquela subdivisão. Já o **Relatório de Turmas** apresenta com 
                    detalhes as turmas recomendas para manutenção ou abertura. Assim como as outras tabelas do relatório, 
                    você pode filtrar os valores e ordenar as colunas conforme necessário. O gráfico é responsivo às 
                    modificações na tabela e indica o número de alunos na turma a uma referência de lotação ideal.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ), 
            ],xs = 11, md = 10, xl = 8)
        ], justify = 'center'),

    # -- Relatório Geral --------------------------------

        dbc.Row([
            dbc.Col([
                dbc.CardHeader(dbc.Button("Relatório Geral",color="link",id="button-1",style = {'margin-top': '0%'})                
                ),

            ], xs = 12)
        ], justify = 'center'),

        dbc.Collapse(
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    dbc.Toast([

                        daq.LEDDisplay(color = 'gray',label = 'Custo total', labelPosition = 'top',size = 25,
                                       value=int(get_par(create_df('sol_relatorio_geral'),'total_custo')),
                                       style = {'margin-top': '1%'},
                                      ),

                        daq.LEDDisplay(color = 'gray',label = 'Custo médio por turma', labelPosition = 'top',size = 25,
                                       value=int(get_par(create_df('sol_relatorio_geral'),'total_custo') / get_par(create_df('sol_relatorio_geral'),'numero_turmas')),
                                       style = {'margin-top': '1%'},
                                      ),

                        daq.LEDDisplay(color = 'gray',label = 'Custo com alunos', labelPosition = 'top',size = 25,
                                       value=int((get_par(create_df('sol_relatorio_geral'),'qtd_alunos_continuidade') + get_par(create_df('sol_relatorio_geral'),'qtd_alunos_formulario')) * get_par(create_df('parametro'),'custo_aluno')),
                                       style = {'margin-top': '1%'},
                                      ),         

                        daq.LEDDisplay(color = 'gray',label = 'Custo com professores', labelPosition = 'top',size = 25,
                                       value=int(get_par(create_df('sol_relatorio_geral'),'numero_turmas') * (get_par(create_df('parametro'),'qtd_professores_pedagogico') + get_par(create_df('parametro'),'qtd_professores_acd')) * get_par(create_df('parametro'),'custo_professor')),
                                       style = {'margin-top': '1%'},
                                      ),

                        daq.GraduatedBar(showCurrentValue=True, max=100, color = 'gray',label = 'Percentual de recursos alocados', 
                                         labelPosition = 'top',
                                         value = round(get_par(create_df('sol_relatorio_geral'),'total_custo') / get_par(create_df('sol_relatorio_geral'),'limite_custo'),2)*100,
                                         style = {'margin-top': '1%'}
                                        ),                

                    ],header="Custos"), 

                ], xs = 11, md = 5, lg = 3, xl = 2),

                dbc.Col([
                    html.Br(),
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Turmas", className = "card-subtitle"),
                            daq.LEDDisplay(color = 'gray',label = 'Número de turmas', labelPosition = 'top',size = 25,
                                           value= int(get_par(create_df('sol_relatorio_geral'),'numero_turmas')),
                                           style = {'margin-top': '0%'},
                                          ),

                            daq.GraduatedBar(showCurrentValue=True, max=100, color = 'gray',label = 'Média de lotação das turmas', 
                                             labelPosition = 'top',
                                             value = create_df('sol_relatorio_turma')['N. Total de Alunos'].sum() / create_df('sol_relatorio_turma')['Qtd. Max. de Alunos'].sum()*100,
                                             style = {'margin-top': '1%'}
                                            ),
                            dcc.Graph(figure = sunburst('sol_relatorio_turma_lista_alunos'),
                                config={
                                    "displaylogo": False,
                                    'modeBarButtonsToRemove': ['pan2d','lasso2d','select2d','resetScale2d',
                                                                     'hoverClosestCartesian', 'hoverCompareCartesian'],
                                }),
                        ])
                    ),

                ], xs = 11, md = 10, lg = 4),

                dbc.Col([
                    html.Br(),
                    dbc.Toast([

                        daq.LEDDisplay(color = 'gray',label = 'Alunos de continuidade', labelPosition = 'top',size = 25,
                                       value = int(get_par(create_df('sol_relatorio_geral'),'qtd_alunos_continuidade')),
                                       style = {'margin-top': '1%'},
                                      ),

                        daq.GraduatedBar(showCurrentValue=True, max=100, color = 'gray',label = 'Alocação dos alunos de continuidade', 
                                         labelPosition = 'top',
                                         value = round(create_df('sol_relatorio_turma')['N. Continuidade'].sum() / create_df('sol_aluno')['CPF'].count(),2)*100, 
                                         style = {'margin-top': '1%'}
                                        ),  

                        daq.LEDDisplay(color = 'gray',label = 'Alunos de formulário alocados', labelPosition = 'top',size = 25,
                                       value= int(get_par(create_df('sol_relatorio_geral'),'qtd_alunos_formulario')),
                                       style = {'margin-top': '1%'},
                                      ),

                        daq.GraduatedBar(showCurrentValue=True, max=100, color = 'gray',label = 'Alocação dos alunos via formulário', 
                                         labelPosition = 'top',
                                         value = round(create_df('sol_relatorio_turma')['N. Formulário'].sum() / create_df('sol_priorizacao_formulario')['CPF'].count(),2)*100, 
                                         style = {'margin-top': '1%'}
                                        ),  

                        daq.GraduatedBar(showCurrentValue=True, max=100, color = 'gray',label = 'Proporção de novos alunos', 
                                         labelPosition = 'top',
                                         value = round(get_par(create_df('sol_relatorio_geral'),'qtd_alunos_formulario') / (get_par(create_df('sol_relatorio_geral'),'qtd_alunos_continuidade') + get_par(create_df('sol_relatorio_geral'),'qtd_alunos_formulario')),2)*100,
                                         style = {'margin-top': '1%'}
                                        ),  

                    ],header="Alunos"), 

                ], xs = 11, md = 5, lg = 3, xl = 2),

            ], justify = 'center'),
            id="collapse-1", is_open=False
        ),
    # --------------------------------------------------------
    # -- Relatório de Turmas ---------------------------------

        dbc.Row([
            dbc.Col([
                dbc.CardHeader(dbc.Button("Relatório de Turmas",color="link",id="button-2",style = {'margin-top': '0%'})                
                ),

            ], xs = 12)
        ], justify = 'center'),

        dbc.Collapse(
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    dash_table.DataTable(
                        id='DT_rel_turmas',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": True, "hideable":True}
                            for i in create_df('sol_relatorio_turma').columns
                        ],
                        data=create_df('sol_relatorio_turma').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="multi",  
                        row_selectable="multi",     
                        row_deletable=False,         
                        selected_columns=[],        
                        selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
                        style_cell={'minWidth': 150, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('sol_relatorio_turma').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),

                ], xs = 10, md = 6, lg = 5, xl = 4),

                dbc.Col([
                    html.Br(),
                    dcc.Graph(
                        id = 'bar-container',
                        config={
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d','lasso2d','select2d','resetScale2d',
                                                       'hoverClosestCartesian', 'hoverCompareCartesian'],
                            'modeBarButtonsToAdd':['drawline','drawrect','drawopenpath','eraseshape'],
                            'toImageButtonOptions': {
                                'format': 'svg', # one of png, svg, jpeg, webp
                                'filename': 'Souza_et_al._2020'
                            },
                        }
                    ),                  
                ], xs = 10, md = 6, lg = 5, xl = 4)

            ], justify = 'center'),
            id="collapse-2", is_open=False
        ),
    # --------------------------------------------------------    
    # -- Relatório de Alunos de Continuidade -----------------

        dbc.Row([
            dbc.Col([
                dbc.CardHeader(dbc.Button("Relatório de Alunos de Continuidade",
                                          color="link",id="button-3",style = {'margin-top': '0%'})                
                ),

            ], xs = 12)
        ], justify = 'center'),

        dbc.Collapse(
            dbc.Row([
                dbc.Col([
                    html.H4(children = "Alocação dos alunos de continuidade",
                    style = {'margin-top':'3%'}),
                    dcc.Markdown('''
                    Lista os alunos de continuidade que foram alocados pelo modelo, conforme restrições definidas pela 
                    ONG.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ),                 

                    dash_table.DataTable(
                        id='DT_alunos_continuidade',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False}
                            if i=="Nome" or i=="Turma (ID)"
                            else {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
                            for i in create_df('sol_aluno').columns
                        ],
                        data=create_df('sol_aluno').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="none",  
                        row_selectable="none",     
                        row_deletable=False,         
        #                 selected_columns=[],        
        #                 selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
        #                 page_size=10,                
                        style_cell={'minWidth': 150, 'width': '300px'},
#                         style_cell={'minWidth': 15, 'maxWidth': 95, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('sol_aluno').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),
                ], xs=11, lg=10, xl=8),
                html.Br(),

            ], justify = 'center'),
            id="collapse-3", is_open=False
        ),
    # -------------------------------------------------------
    # -- Relatório de Alunos de Formulário ------------------

        dbc.Row([
            dbc.Col([
                dbc.CardHeader(dbc.Button("Relatório de Alunos de Formulário",
                                          color="link",id="button-4",style = {'margin-top': '0%'})                
                ),

            ], xs = 12)
        ], justify = 'center'),

        dbc.Collapse(
            dbc.Row([
                dbc.Col([
                    html.H4(children = "Alocação dos alunos de formulário",
                    style = {'margin-top':'3%'}),
                    dcc.Markdown('''
                    Lista os alunos de formulário que foram alocados pelo modelo, conforme restrições definidas pela 
                    ONG.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ),                 

                    dash_table.DataTable(
                        id='DT_alunos_formulario',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False}
                            if i=="Nome" or i=="Turma (ID)"
                            else {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
                            for i in create_df('sol_priorizacao_formulario').columns
                        ],
                        data=create_df('sol_priorizacao_formulario').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="none",  
                        row_selectable="none",     
                        row_deletable=False,         
        #                 selected_columns=[],        
        #                 selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
        #                 page_size=10,                
                        style_cell={'minWidth': 150, 'width': '300px'},
#                         style_cell={'minWidth': 15, 'maxWidth': 95, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('sol_priorizacao_formulario').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),

                    html.Br(),

                    html.H4(children = "Alunos de formulário não alocados",
                    style = {'margin-top':'3%'}),
                    dcc.Markdown('''
                    Lista os alunos de formulário que **não** foram alocados pelo modelo, conforme restrições definidas pela 
                    ONG.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ),                 

                    dash_table.DataTable(
                        id='DT_alunos_n_formulario',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False}
                            if i=="Nome" or i=="Turma (ID)"
                            else {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
                            for i in create_df('sol_relatorio_formulario_nao_alocados').columns
                        ],
                        data=create_df('sol_relatorio_formulario_nao_alocados').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="none",  
                        row_selectable="none",     
                        row_deletable=False,         
        #                 selected_columns=[],        
        #                 selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
        #                 page_size=10,                
                        style_cell={'minWidth': 150, 'width': '300px'},
#                         style_cell={'minWidth': 15, 'maxWidth': 95, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('sol_relatorio_formulario_nao_alocados').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),

                ], xs=11, md=11, lg=10, xl=8),
                html.Br(),

            ], justify = 'center'),    
            id="collapse-4", is_open=False
        ),
    # -------------------------------------------------------
    # -- Relatório descritivo das turmas --------------------

        dbc.Row([
            dbc.Col([
                dbc.CardHeader(dbc.Button("Relatório Descritivo das Turmas",
                                          color="link",id="button-5",style = {'margin-top': '0%'})                
                ),

            ], xs = 12)
        ], justify = 'center'),

        dbc.Collapse(
            dbc.Row([
                dbc.Col([
                    html.H4(children = "Descrição das Turmas",
                    style = {'margin-top':'3%'}),
                    dcc.Markdown('''
                    Lista as turmas com mais detalhes, indicando o número máximo de alunos, professores e IDs de escolas e séries.
                    Além disso indica se a turma recomendada foi aprovada pela ONG ou não.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ),                 

                    dash_table.DataTable(
                        id='DT_turmas',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False}
                            for i in create_df('sol_turma').columns
                        ],
                        data=create_df('sol_turma').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="none",  
                        row_selectable="none",     
                        row_deletable=False,         
        #                 selected_columns=[],        
        #                 selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
        #                 page_size=10,                
                        style_cell={'minWidth': 150, 'width': '300px'},
#                         style_cell={'minWidth': 15, 'maxWidth': 95, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('sol_turma').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),
                    html.Br(),
                ], xs=11, md=11, lg=10, xl=8),
                html.Br(),

            ], justify = 'center'),
            id="collapse-5", is_open=False
        ),
    # -------------------------------------------------------  
    # -- Relatório de custo por turma  --------------------

        dbc.Row([
            dbc.Col([
                dbc.CardHeader(dbc.Button("Relatório Descritivo dos Custos",
                                          color="link",id="button-6",style = {'margin-top': '0%'})                
                ),

            ], xs = 12)
        ], justify = 'center'),

        dbc.Collapse(
            dbc.Row([
                dbc.Col([
                    html.H4(children = "Descrição dos custos por turma",
                    style = {'margin-top':'3%'}),
                    dcc.Markdown('''
                    Detalha os custos por turma, indicando os recursos alocados em cada uma delas, assim como a proporção 
                    do orçamento disponível. Os custos por turma são dependentes da quantidade de professores e alunos.
                    ''',
                    style = {
                        'textAlign':'left',
                        'textJustify':'center',
                        'margin-top': '1%',
                        'margin-botton':'1%',
                        'position':'relative'
                           }
                    ),                 

                    dash_table.DataTable(
                        id='DT_orcamento',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False}
                            for i in create_df('sol_relatorio_orcamento').columns
                        ],
                        data=create_df('sol_relatorio_orcamento').to_dict('records'),                           
                        editable=False,             
                        filter_action="native",     
                        sort_action="native",       
                        sort_mode="single",         
                        column_selectable="none",  
                        row_selectable="none",     
                        row_deletable=False,         
        #                 selected_columns=[],        
        #                 selected_rows=[],           
                        page_action="native",       
                        page_current=0,             
        #                 page_size=10,                
                        style_cell={'minWidth': 150, 'width': '300px'},
#                         style_cell={'minWidth': 15, 'maxWidth': 95, 'width': '300px'},

                        style_cell_conditional=[    
                            {
                                'if': {'column_id': c},
                                'textAlign': 'center'
                            } for c in create_df('sol_relatorio_orcamento').columns
                        ],
                        style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_table={'maxHeight': '300px','overflowY': 'scroll', 'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },          
                    ),
                    html.Br(),
                ], xs=11, md=11, lg=10, xl=8),
                html.Br(),

            ], justify = 'center'),
            id="collapse-6", is_open=False
        ),
    # -------------------------------------------------------    
    # - Rodapé -------------------------------------------------
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.Hr(),
                dcc.Markdown('''
                Relatório web desenvolvido pelo grupo Convex-Lab, participantes do desafio UniSoma 2020.
                ''',
                style = {
                    'textAlign':'center',
                    'textJustify':'center',
                    'margin-top': '1%',
                    'margin-botton':'1%',
                    'position':'relative'
                       }
                ),  
                html.Hr(),

            ], xs=11, lg=10, xl=8)
        ], justify = 'center')
    # - End of the layoyt --------------------------------------    
    ])

    # ----------------------------------------------------------
    # - Callbacks ----------------------------------------------

    # -- Barchart ----------------------------------------------
    @app.callback(
        Output(component_id='bar-container', component_property='figure'),
        [Input(component_id='DT_rel_turmas', component_property="derived_virtual_data"),
         Input(component_id='DT_rel_turmas', component_property='derived_virtual_selected_rows'),
         Input(component_id='DT_rel_turmas', component_property='derived_virtual_selected_row_ids'),
         Input(component_id='DT_rel_turmas', component_property='selected_rows'),
         Input(component_id='DT_rel_turmas', component_property='derived_virtual_indices'),
         Input(component_id='DT_rel_turmas', component_property='derived_virtual_row_ids'),
         Input(component_id='DT_rel_turmas', component_property='active_cell'),
         Input(component_id='DT_rel_turmas', component_property='selected_cells')]
    )
    def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
                   order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):

        dff = pd.DataFrame(all_rows_data)

        # used to highlight selected countries on bar chart

        fig1 = go.Figure()

        fig1.add_trace(go.Bar(
            x = dff["Turma"],
            y = dff["N. Total de Alunos"],
            marker_color = 'gray',
            name = "Turmas"
        ))

        fig1.add_trace(go.Scatter(
            x = dff["Turma"],
            y = dff['Qtd. Max. de Alunos'],
            line = dict(color='black', width=4, dash='dot'),
            hoverinfo = 'none',
            name = "Target"
        ))

        fig1.update_layout(margin={"r":0,"t":25,"l":0,"b":0},paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=350)
        fig1.update_yaxes(showline=True, linewidth=1, linecolor='gray')
        fig1.update_xaxes(showline=True, linewidth=1, linecolor='gray')
        fig1.update_layout(legend=dict(orientation="h",yanchor="top",y=1.1,xanchor="left",x=0.01))

        return fig1

    # -- Collapse Input ---------------------------------------------
    @app.callback(
        Output("collapse-in-1", "is_open"),
        [Input("button-in-1", "n_clicks")],
        [State("collapse-in-1", "is_open")],
    )
    def toggle_collapse_in_1(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse-in-2", "is_open"),
        [Input("button-in-2", "n_clicks")],
        [State("collapse-in-2", "is_open")],
    )
    def toggle_collapse_in_2(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse-in-3", "is_open"),
        [Input("button-in-3", "n_clicks")],
        [State("collapse-in-3", "is_open")],
    )
    def toggle_collapse_in_3(n, is_open):
        if n:
            return not is_open
        return is_open

    # -- Collapse Output ---------------------------------------------
    @app.callback(
        Output("collapse-1", "is_open"),
        [Input("button-1", "n_clicks")],
        [State("collapse-1", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse-2", "is_open"),
        [Input("button-2", "n_clicks")],
        [State("collapse-2", "is_open")],
    )
    def toggle_collapse2(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse-3", "is_open"),
        [Input("button-3", "n_clicks")],
        [State("collapse-3", "is_open")],
    )
    def toggle_collapse3(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse-4", "is_open"),
        [Input("button-4", "n_clicks")],
        [State("collapse-4", "is_open")],
    )
    def toggle_collapse4(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse-5", "is_open"),
        [Input("button-5", "n_clicks")],
        [State("collapse-5", "is_open")],
    )
    def toggle_collapse5(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse-6", "is_open"),
        [Input("button-6", "n_clicks")],
        [State("collapse-6", "is_open")],
    )
    def toggle_collapse6(n, is_open):
        if n:
            return not is_open
        return is_open
    # ----------------------------------------------------------
    # - Layout (END) -------------------------------------------
    if __name__ == "__main__":
    #     app.run_server(debug = True)
        app.run_server(port = 4050)
    #-----------------------------------------------------------
    
    return app
    
# -*- coding: utf-8 -*-
"""Convex-Lab_Desafio_Unisoma_2020

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1INg07Psp6JCkSPzRwN6k1Znl1PJ6zToy

# Instalacao de bibliotecas
"""

# !pip install pandas
# !pip install numpy
# !pip install scipy
# !pip install PuLP #Tem que instalar essa!


import sqlite3
import pandas as pd
import numpy as np
from pulp import *
import math

"""# Banco de dados - SQL"""

def get_parametro_from_table(df_parametro,chave):
  return int(df_parametro.valor[df_parametro.chave==chave])

def create_dataframe(table,conn):
  return pd.read_sql_query("SELECT * FROM "+table+";",conn)

def leitura_BD(file_BD, table_names, param_list):
  if os.path.isfile(file_BD):
    conn = sqlite3.connect(file_BD)
    
    dfs_dict = {}
    for tab in table_names:    
        dfs_dict[tab] = create_dataframe(tab,conn)    

    conn.close()

    param_dict = {}
    for par in param_list:   
      param_dict[par] = get_parametro_from_table(dfs_dict['parametro'],par)
  else:
    print("FILE NOT FOUND")
    return None, None
    
  return dfs_dict, param_dict

def salva_BD(file_BD, df_sol_turma, df_sol_aluno, df_sol_formulario):
  print("Salva BD em ", file_BD) 
  if os.path.isfile(file_BD):
    conn_sol = sqlite3.connect(file_BD)
  
    #Nao salva coluna ignore_index
    df_sol_turma[['id','nome', 'qtd_max_alunos', 'qtd_professores_acd', 'qtd_professores_pedagogico', 'escola_id', 'serie_id', 'aprova']].to_sql('sol_turma', con = conn_sol, if_exists = 'replace', chunksize = 1000, index=False)  
    df_sol_formulario.to_sql('sol_priorizacao_formulario', con = conn_sol, if_exists = 'replace', chunksize = 1000, index=False)
    df_sol_aluno.to_sql('sol_aluno', con = conn_sol, if_exists = 'replace', chunksize = 1000, index=False)

    conn_sol.close()
  else:
    print("FILE NOT FOUND")

def salva_BD_relatorio(file_BD, tab_name, df_relatorio):
  print("Salva relatorio BD " + tab_name + " em ", file_BD) 
  if os.path.isfile(file_BD):
    conn_sol = sqlite3.connect(file_BD)
  
    df_relatorio.to_sql(tab_name, con = conn_sol, if_exists = 'replace', chunksize = 1000, index=False)  
  
    conn_sol.close()
  else:
    print("FILE NOT FOUND")

"""# Pre-processamento - Tabelas

##Serie
"""

def calc_proxima_serie(df_aluno_param, df_serie, row, i, max_serie_ordem,incr=1): #default incrementa uma serie
  #print("incr",incr) #debug
  #print(row) #debug
  aluno_serie_valida=0
  #if row['ordem'] < max_serie_ordem :    
  if (row['ordem']+incr) <= max_serie_ordem :   #melhoria final
    next_ordem = (int(row['ordem'])+incr)    
    
    if next_ordem <= max_serie_ordem:
      next_serie = int(df_serie['id'][df_serie['ordem']==next_ordem])
      #Verificar se a serie que o aluno quer cursar esta ativas. Alunos que cursariam series inativas sao desconsiderados no planejamento
      #print("next serie:", next_serie) #debug
      #print("serie:", df_serie['ativa'][ df_serie['id']==next_serie ]) #debug
      if int(df_serie['ativa'][ df_serie['id']==next_serie ])==1 :
          df_aluno_param.loc[int(i),'serie_id_otim'] =next_serie     
          aluno_serie_valida=1 
    
  if aluno_serie_valida == 0:  
    #print("......... drop row", i) #debug
    #print(row) #debug
    df_aluno_param=df_aluno_param.drop([i],axis=0)

  return df_aluno_param

def pre_processamento_serie(df_serie):  
  #Determina ultima serie ativa da ONG (ativa)
  max_serie_ordem=max(df_serie['ordem'][df_serie['ativa']==1])
  max_serie_id= int(df_serie.id[df_serie['ordem']==max(df_serie['ordem'])])
  
  return df_serie, max_serie_ordem, max_serie_id

"""## Alunos de continuidade"""

def calc_alunos_continuidade_proxima_serie(df_aluno_serie, df_serie, max_serie_ordem, otimiza_dentro_do_ano):  
  df_aluno_serie['serie_id_otim']=0
  
  if otimiza_dentro_do_ano==0:     #identifica a próxima série dos alunos  
    for i, row in df_aluno_serie.iterrows():
      #print("aluno " + str(i) + "serie:" + str(df_aluno_serie['serie_id'][i]) + ", reprova? " + str(df_aluno_serie['reprova'][i])) #debug
      if df_aluno_serie['reprova'][i]==0:
        df_aluno_serie = calc_proxima_serie(df_aluno_serie, df_serie, row, i, max_serie_ordem)           
      else:
        df_aluno_serie.loc[int(i),'serie_id_otim'] = df_aluno_serie['serie_id'][i]      
        #df_aluno_serie['serie_id_otim'][i] = df_aluno_serie['serie_id'][i]      
        #print("aluno " + str(i) + " serie_id_otim:" + str(df_aluno_serie['serie_id_otim'][i])) #debug
  else: #caso contrario, usa a serie atual
    df_aluno_serie['serie_id_otim']=df_aluno_serie['serie_id']

  return df_aluno_serie

def pre_processamento_alunos_continuidade(df_aluno, df_turma, df_serie, otimiza_dentro_do_ano, max_serie_ordem):

  #--- Desconsiderar alunos que nao vao continuar na ONG -> TODO: colocar na query sql
  df_aluno = df_aluno[df_aluno['continua']==1]

  #----- Nova tabela df_aluno_serie: informações de escola e série dos alunos

  #Inclui serie_id  
  df_aluno_serie = df_aluno.merge(df_turma[['id','escola_id','serie_id']], how='left', left_on='turma_id', right_on='id',suffixes=('','_y'))   
  df_aluno_serie=df_aluno_serie.drop(columns=['id_y'])  #aqui vale que df_aluno_turma_id == turma.id (id_y)
  #Inclui serie.ordem
  df_aluno_serie = df_aluno_serie.merge(df_serie[['id','ordem']], how='left', left_on='serie_id', right_on='id', suffixes=('','_y'))
  df_aluno_serie=df_aluno_serie.drop(columns=['id_y']) 

  #--- Proxima serie dos alunos de continuidade, tabela: df_aluno_serie    
  df_aluno_serie = calc_alunos_continuidade_proxima_serie(df_aluno_serie, df_serie, max_serie_ordem, otimiza_dentro_do_ano)

  return df_aluno_serie

"""## Alunos de formulario"""

def calc_alunos_formulario_proxima_serie(df_formulario_inscricao_serie, df_serie, max_serie_ordem, ano_planejamento):
  #obs: ultima serie e a 5

  df_formulario_inscricao_serie['serie_id_otim']=0
  #df_formulario_inscricao_serie.head()

  #identifica a proxima serie dos alunos, quando ano<ano_planejamento
  for i, row in df_formulario_inscricao_serie.iterrows():
    #print("iter",i) #debug
    #print("ano_planejamento:",ano_planejamento) #debug
    #print("ano_ref_row:", row['ano_referencia']) #debug
    diferenca_ano_ref = ano_planejamento - row['ano_referencia']
    #if diferenca_ano_ref>0:
    if diferenca_ano_ref>=0: #melhoria final
      #print("diferenca ano-ref:",diferenca_ano_ref) #debug
      df_formulario_inscricao_serie = calc_proxima_serie(df_formulario_inscricao_serie, df_serie, row, i, max_serie_ordem,incr=diferenca_ano_ref)       

  return df_formulario_inscricao_serie

def pre_processamento_alunos_formulario(df_formulario_inscricao, df_serie, max_serie_ordem, ano_planejamento):
  #--- Inclui serie e serie.ordem na tabela dos alunos de formulario - Tabela: df_formulario_inscricao_serie: 

  #Tabela df_formulario_inscricao_serie  
  df_formulario_inscricao_serie = df_formulario_inscricao

  #inclui serie.ordem dos alunos de formulario
  df_formulario_inscricao_serie = df_formulario_inscricao_serie.merge(df_serie[['id','ordem']], how='left', left_on='serie_id', right_on='id', suffixes=('','_y'))
  df_formulario_inscricao_serie=df_formulario_inscricao_serie.drop(columns=['id_y'])

  #print("alunos formulario") #debug 
  #print(df_formulario_inscricao_serie.head(20)) #debug

  #--- Serie dos alunos de formulario: se ano de referencia < ano_planejamento, precisa colocar o aluno na proxima serie
  df_formulario_inscricao_serie = calc_alunos_formulario_proxima_serie(df_formulario_inscricao_serie, df_serie, max_serie_ordem, ano_planejamento)

  #--- Ordena alunos por data de inscricao

  df_formulario_inscricao_serie_rank=df_formulario_inscricao_serie

  df_formulario_inscricao_serie_rank['data_inscricao'] = pd.to_datetime(df_formulario_inscricao_serie_rank['data_inscricao'], format='%d/%m/%Y %H:%M:%S')

  df_formulario_inscricao_serie_rank['rank'] = df_formulario_inscricao_serie_rank['data_inscricao'].rank(method='dense', ascending = True).astype(int)
  df_formulario_inscricao_serie_rank.sort_values(by='rank',inplace = True)

  return df_formulario_inscricao_serie

"""# Fase 1 - aloca os alunos de continuidade - permite abertura de novas turmas

## Restricoes
"""

#Se alunos i e j estavam na mesma turma, então eles tem que continuar, desde que nenhum deles tenha sido reprovado.
def restricao_alunos_mesma_turma(model, xc, df_aluno, turmas_new_idx_list):  
  for i in df_aluno.index:
    if df_aluno['reprova'][i] == 0: #se o aluno i nao reprovar
      aluno_i_turma = df_aluno['turma_id'][i]
    
      for j in df_aluno.index:
        #se o aluno j nao reprovar e se i e j estavam na mesma turma
        if i!= j and df_aluno['reprova'][j] == 0 and aluno_i_turma == df_aluno['turma_id'][j]:
          #print('alunos ' + str(df_aluno['id'][i]) + ' e ' + str(df_aluno['id'][j])+ ' estavam na mesma turma') #debug
    
          for t in turmas_new_idx_list:
            #duvida: alunos de continuidade podem ser alocados em novas turmas?
            model += xc[(i,t)] == xc[(j,t)] 
  
  return model, xc

#Cada aluno deve ser alocado na serie apropriada, determinada de acordo com as regras:
def restricao_aluno_serie(model, x_par, y, df_aluno_par, df_serie, turmas_new_idx_list):
  
  for i in df_aluno_par.index:    
    for t in turmas_new_idx_list: #considera tanto as turmas ja existentes, quanto as novas que podem ser criadas
      s_id= df_aluno_par['serie_id_otim'][i] #serie que o aluno vai cursar
      #print('aluno_form: ' + str(df_aluno_par['id'][i]) + ',serie=' + str(s_id)) #debug
      s_index = df_serie[  df_serie['id'] ==s_id ].index[0]
      #print('aluno_form: ' + str(df_aluno_par['id'][i]) + ',serie=' + str(s_id) + ', index=' + str(s_index))  
      #print("ok") #debug
      model += x_par[(i,t)] <= y[(t,s_index)]
  return model, x_par, y

#Cada aluno i só pode ser alocado na turma t se a turma se ela existir na escola e que ele escolheu:
def restricao_aluno_escola(model, x_par, y, z, df_aluno_par, df_escola, turmas_new_idx_list):
  for i in df_aluno_par.index:
    for t in turmas_new_idx_list: #considera tanto as turmas ja existentes, quanto as novas que podem ser criadas
      e_id= df_aluno_par['escola_id'][i] #escola que o aluno vai estudar
      e_index = df_escola[ df_escola['id'] ==e_id ].index[0]
      #print('i:'+str(i)+ ', aluno: ' + str(df_aluno_par['id'][i]) + ', escola=' + str(e_id) + ', index=' + str(e_index))  
      model += x_par[(i,t)] <= z[(t,e_index)]

  return model, x_par, y, z

#Turmas pré-existentes já tem a série e a escola definidas.
def restricao_define_turma_existente(model, y, z, v_turma_aberta, df_turma, df_serie, df_escola, turmas_existentes_idx_list):
  for t in turmas_existentes_idx_list:  #turmas existentes    
    #Definir a serie da turma    
    s_id=df_turma['serie_id'][t]  
    s_index = df_serie[  df_serie['id'] ==s_id ].index[0]  
    #print(str(df_turma['nome'][t]) + ', turma=' + str(t)+ ':id=' + str(df_turma['id'][t]) +',serie=' + str(s_id) + ', index=' + str(s_index)) #debug
    model += y[(t,s_index)] == 1
    
    #Definir a escola da turma
    e_id=df_turma['escola_id'][t]  
    e_index = df_escola[  df_escola['id'] ==e_id ].index[0]    
    #print(str(df_turma['nome'][t]) + ', turma=' + str(t)+',escola=' + str(e_id) + ', index=' + str(e_index)) #debug
    model += z[(t,e_index)] == 1

    #Turmas pre existentes sao marcadas como abertas        
    model += v_turma_aberta[t] == 1
  
  return model, y, z, v_turma_aberta

#Custo maximo da ONG
def restricao_limite_custo_ONG(model, xc, xf, v_turma_aberta, df_aluno, df_formulario, turmas_new_idx_list, param_dict):
  custo_turma_professores_t = param_dict['custo_professor']*(param_dict['qtd_professores_pedagogico'] + param_dict['qtd_professores_acd'])
  
  #nao precisa multiplicar custo_turma_alunos_t por v_turma_aberta porque a restricao R8 garante que xc e xf so sao maiores do que 0 quando v_turma_aberta=1
  custo_turma_alunos_t=0
  for t in turmas_new_idx_list:    
    custo_turma_alunos_t += ( lpSum(xc[(i,t)] for i in df_aluno.index) + lpSum( xf[(i,t)] for i in df_formulario.index) )* param_dict['custo_aluno']
  #ok
  model += custo_turma_alunos_t + lpSum( custo_turma_professores_t* v_turma_aberta[t] for t in turmas_new_idx_list ) <= param_dict['limite_custo']
  
  return model, xc, xf, v_turma_aberta

def restricao_alunos_vagas_turma(model, xc, xf, v_folga, v_vagas_livres, v_turma_aberta, df_aluno, df_formulario, turmas_new_idx_list, param_dict):
  for t in turmas_new_idx_list:    
    #print('turma t=' + str(t))
    #Soma os alunos de continuidade e os de formulario em cada turma aberta, variavel de folga calcula as vagas sobrando em todas as turmas
    model += lpSum( xc[(i,t)] for i in df_aluno.index) + lpSum( xf[(i,t)] for i in df_formulario.index) + v_vagas_livres[t] == v_turma_aberta[t] * param_dict['qtd_max_alunos']    

  return model, xc, xf, v_folga, v_vagas_livres, v_turma_aberta

"""## Variaveis de decisao"""

#------------- Variaveis de decisao
def fase1_declara_vars_decisao(alunos_idx_list, formulario_idx_list, turmas_new_idx_list, serie_idx_list, escola_idx_list, param_dict):
  xc = LpVariable.dicts("aluno_turma",
                                [(i, t) for i in alunos_idx_list #indices dos alunos no dataframe
                                        for t in turmas_new_idx_list], #indice das turmas 
                                0, 1, LpBinary)

  xf = LpVariable.dicts("aluno_formulario",
                                [(i, t) for i in formulario_idx_list #indices dos alunos no dataframe
                                        for t in turmas_new_idx_list], #indice das turmas 
                                0, 1, LpBinary)
  
  v_turma_aberta = LpVariable.dicts("turma_aberta",  turmas_new_idx_list, 0,1, LpBinary ) #maior numero de vagas vazias em uma turma e qtd_max_alunos


  y = LpVariable.dicts("turma_serie",
                                [(t, s) for t in turmas_new_idx_list #indices dos alunos no dataframe
                                        for s in serie_idx_list], #indice das turmas 
                                0, 1, LpBinary)

  z = LpVariable.dicts("turma_escola",
                                [(t, s) for t in turmas_new_idx_list #indices dos alunos no dataframe
                                        for s in escola_idx_list], #indice das turmas 
                                0, 1, LpBinary)  
  v_folga = LpVariable.dicts("v_folga", turmas_new_idx_list, 0, param_dict['qtd_max_alunos'] ) #maior numero de vagas vazias em uma turma e qtd_max_alunos

  v_vagas_livres = LpVariable.dicts("v_vagas_livres", turmas_new_idx_list, 0, param_dict['qtd_max_alunos'] ) #maior numero de vagas vazias em uma turma e qtd_max_alunos

  return xc, xf, v_turma_aberta, y, z, v_folga, v_vagas_livres

"""## Fase 1 - Funcao objetivo"""

#Fase 1: Funcao objetivo
# minimiza as vagas vazias nas turmas
# so sao criadas turmas para acomodar os alunos de continuidade
# assim, nao e necessario maximizar o numero de alunos de formulario acomodados

def fase1_funcao_objetivo(model, v_vagas_livres, v_turma_aberta, xf, turmas_new_idx_list, turmas_existentes_idx_list, df_formulario):
  #Minimiza as vagas de folga das turmas, ou seja, maximiza as vagas utilizadas nas turmas, i.e. 
  vagas_folga_soma = lpSum(v_vagas_livres[t] for t in turmas_new_idx_list)

  #Turmas pre-existentes sao marcadas como abertas por padrao
  #isso significa que sempre sao consideradas as vagas remanescentes dela
  #dessa forma, so serao abertas novas turmas se nao for possivel alocar nas existentes
  
  tot_turmas_abertas = lpSum(v_turma_aberta[t] for t in turmas_new_idx_list)

  #Prioriza ordem de inscricao
  prioriza_ordem_inscr=0
  for i in df_formulario.index:
    prioriza_ordem_inscr += lpSum( xf[(i,t)]*df_formulario['rank'][i] for t in turmas_new_idx_list)  #minimizar o rank

  #Para ser minimizada:
  #fo = vagas_folga_soma + tot_turmas_abertas + 0.1*prioriza_ordem_inscr #Wrong
  #final 
  #TODO: Estimar coeficiente
  fo = vagas_folga_soma + tot_turmas_abertas + 0.00001*prioriza_ordem_inscr 
  
  model+=fo
  return model

def modelo_show_fo(model, v_vagas_livres, v_turma_aberta, xf, turmas_new_idx_list, turmas_existentes_idx_list, df_formulario):
  count_turmas=0

  vagas_folga_soma = lpSum(v_vagas_livres[t].varValue for t in turmas_new_idx_list)
  tot_turmas_abertas = lpSum(v_turma_aberta[t].varValue for t in turmas_new_idx_list)
  prioriza_ordem_inscr=0
  for i in df_formulario.index:
    prioriza_ordem_inscr += lpSum( xf[(i,t)].varValue*df_formulario['rank'][i] for t in turmas_new_idx_list)  #minimizar o rank

  print("vagas_folga_soma="+str(vagas_folga_soma))   
  print("tot_turmas_abertas="+str(tot_turmas_abertas))
  print("prioriza_ordem_inscr="+str(prioriza_ordem_inscr) + " -> " +str(0.001*prioriza_ordem_inscr) )
  print("FO total="+str(vagas_folga_soma+tot_turmas_abertas+0.001*prioriza_ordem_inscr))

"""## Extra"""

def fase1_define_all_turmas_list(df_turma,turma_id_max_existente, param_dict, numero_turmas_limitante):  
  #ub_turmas = calculo_limitante_superior_u(df_turma)  #entrega inicial
  #ub_turmas = calculo_limitante_superior_u(df_turma,turma_id_max_existente,numero_turmas_limitante) #final #apagar

  print("Numero de turmas atuais =" + str(len(df_turma.index)))
  ub_turmas = numero_turmas_limitante - len(df_turma.index)

  print("Limitante superior para o numero de turmas novas (1a fase)=",ub_turmas) #debug

  #max_turma_idx = int(max( df_turma['id'].index)) #entrega inicial
  max_new_turma_idx = turma_id_max_existente+ub_turmas
  #print("turma_id_max_existente") #debug #apagar
  #print(turma_id_max_existente) #debug #apagar
  #print("max_new_turma_idx") #debug #apagar
  #print(max_new_turma_idx) #debug #apagar

  #new_turmas = list(range( max_turma_idx+1, max_new_turma_idx ))  #entrega inicial
  new_turmas = list(range( turma_id_max_existente+1, max_new_turma_idx+1 ))  #final, +1 pois range [a,b)
  all_turmas_list = list(df_turma.index) + new_turmas 
  
  return all_turmas_list

def modelo_show_solucao(xc, xf, v_turma_aberta, y, z, v_vagas_livres, df_aluno, df_formulario, df_turma, df_serie, df_escola, turmas_new_idx_list):
  count_turmas=0

  #-------------- Resultado
  for t in turmas_new_idx_list:
    print("-------- Turma t="+str(t)) 
    print("Aberta=" + str(v_turma_aberta[t].varValue))
    
    if v_turma_aberta[t].varValue>0:
      count_turmas+=v_turma_aberta[t].varValue     
      if t < len(df_turma['id']):
        print("turma, id=" + str(df_turma['id'][t]))

      for s in df_serie.index:
        if y[(t,s)].varValue >0.1:
          print('serie='+str(s)+", id="+ str(df_serie['id'][s])+ ', y=' + str(  y[(t,s)].varValue))
      for e in df_escola.index:
        if z[(t,e)].varValue >0.1:
          print('escola='+str(e)+", id="+ str(df_escola['id'][e])+ ', y=' + str(  z[(t,e)].varValue))                      
      
      #print("Vagas folga="+ str(v_folga[t].varValue))
      print("Vagas livres="+ str(v_vagas_livres[t].varValue))
      
      for i in df_aluno.index:
        if xc[(i,t)].varValue > 0:
          print('xc['+ str(i)+':id='+str(df_aluno['id'][i]) + ',' + str(t) + ']=' + str(xc[(i,t)].varValue ))
      for i in df_formulario.index:
        if xf[(i,t)].varValue > 0:
          print('xf['+ str(i)+':id='+str(df_formulario['id'][i])  + ',' + str(t) + ']=' + str(xf[(i,t)].varValue ))

  print("turmas abertas = " + str(count_turmas))

#Lista com os alunos de formulario restantes, remove os de xf que ja foram alocados  
#Calcula o orçamento restante  
def apos_fase1_atualiza_dfs_restante(dfs_dict, param_dict, xc, xf, v_vagas_livres, v_turma_aberta, turmas_new_index_list):    
  
  df_formulario_restante = dfs_dict['formulario_inscricao'].copy()
  count_aluno_formulario=0
  for i in df_formulario_restante.index:
    for t in turmas_new_index_list:
      if xf[(i,t)].varValue == 1:
        count_aluno_formulario+=1
        #print("aluno form index=" + str(i)+ ', id=' + str(df_formulario_restante['id'][i]) + ' vai ser apagado') #debug
        df_formulario_restante.drop(i, inplace=True)
  
  count_aluno = 0
  for i in dfs_dict['aluno'].index:
      count_aluno+= sum( xc[(i,t)].varValue for  t in turmas_new_index_list)
      
  count_turma=0
  for t in turmas_new_index_list:
    aberta=sum( xc[(i,t)].varValue for i in dfs_dict['aluno'].index) + sum( xf[(i,t)].varValue for i in dfs_dict['formulario_inscricao'].index)
    if aberta >0:
      count_turma+=1
    
  #Quanto sobra de orcamento? 
  custo_turma_professores_t = param_dict['custo_professor']*(param_dict['qtd_professores_pedagogico'] + param_dict['qtd_professores_acd'])
  custo_turma_alunos_t = ( count_aluno + count_aluno_formulario)* param_dict['custo_aluno']
  orcamento = (count_turma * custo_turma_professores_t + custo_turma_alunos_t)

  orcamento_restante = param_dict['limite_custo'] - orcamento

  orcamento_count_alunos = (orcamento_restante - custo_turma_professores_t)/param_dict['custo_aluno']
  
  #Limitante superior para o numero de alunos na proxima turma:
  num_max_alunos = int(min(orcamento_count_alunos, param_dict['qtd_max_alunos']))
  
  return df_formulario_restante, orcamento_restante, num_max_alunos

"""## Fase 1 - Modelo"""

def fase1_modelo(dfs_dict, param_dict, turma_id_max_existente, numero_turmas_limitante): #final
  df_aluno = dfs_dict['aluno']
  df_formulario = dfs_dict['formulario_inscricao']
  df_turma =  dfs_dict['turma']
  df_serie =  dfs_dict['serie']
  df_escola = dfs_dict['escola']

  #------------- Conjunto de indices para turmas 
  turmas_existentes_idx_list = df_turma.index  #turmas ja existentes
  
  if param_dict['possibilita_abertura_novas_turmas']==0:
    turmas_new_idx_list=turmas_existentes_idx_list
  else:  
    turmas_new_idx_list= fase1_define_all_turmas_list(df_turma, turma_id_max_existente, param_dict, numero_turmas_limitante) #final
    #print("here ok")
    print(turmas_new_idx_list) #debug #apagar
  #------------- Inicia o modelo 
  model = LpProblem(name="desafio_unisoma_fase1", sense=LpMinimize)

  xc, xf, v_turma_aberta, y, z, v_folga, v_vagas_livres = fase1_declara_vars_decisao(df_aluno.index, df_formulario.index, turmas_new_idx_list, df_serie.index, df_escola.index, param_dict)
  
  #-------------- Funcao objetivo
  model = fase1_funcao_objetivo(model, v_vagas_livres, v_turma_aberta, xf, turmas_new_idx_list, turmas_existentes_idx_list, df_formulario)
  
  #-------------- Restricoes

  #R5
  #Alunos de continuidade (matriculados) tem que obrigatoriamente ser alocados em uma turma:
  for i in df_aluno.index: 
    model+= lpSum( xc[(i,t)] for t in turmas_new_idx_list) == 1
    
  #R1
  #Se alunos i e j estavam na mesma turma e foram aprovados, então eles tem que continuar na mesma turma:
  model, xc = restricao_alunos_mesma_turma(model, xc, df_aluno, turmas_new_idx_list)
  
  #R6
  #Cada aluno de formulario e alocado em no maximo uma turma:
  for i in df_formulario.index:
    model += lpSum( xf[(i,t)] for t in turmas_new_idx_list  ) <= 1

  #R4
  #Turmas pré-existentes já tem a série e a escola definidas:
  model, y, z, v_turma_aberta = restricao_define_turma_existente(model,y,z,v_turma_aberta, df_turma,df_serie,df_escola,turmas_existentes_idx_list)
    
  #R7
  #Cada turma pertence a uma unica serie e escola:
  for t in turmas_new_idx_list:
    model += lpSum( y[(t,s)] for s in df_serie.index) == 1
    model += lpSum( z[(t,e)] for e in df_escola.index) == 1
  
  #R2
  #Cada aluno deve ser alocado na serie apropriada, determinada de acordo com as regras:
  model, xc, y = restricao_aluno_serie(model, xc, y, df_aluno, df_serie, turmas_new_idx_list)    
  model, xf, y = restricao_aluno_serie(model, xf, y, df_formulario, df_serie, turmas_new_idx_list)    

  #R3
  #Cada aluno i só pode ser alocado na turma t se a turma se ela existir na escola que escolheu:
  model, xc, y, z = restricao_aluno_escola(model, xc, y, z, df_aluno, df_escola, turmas_new_idx_list)    
  model, xf, y, z = restricao_aluno_escola(model, xf, y, z, df_formulario, df_escola, turmas_new_idx_list)    

  #Abertura de turmas: Número máximo de alunos por turma e vagas livres
  model, xc, xf, v_folga, v_vagas_livres, v_turma_aberta = restricao_alunos_vagas_turma(model, xc, xf, v_folga, v_vagas_livres, v_turma_aberta, df_aluno, df_formulario, turmas_new_idx_list, param_dict)

  #R9
  #Custo maximo da ONG
  model, xc, xf, v_turma_aberta = restricao_limite_custo_ONG(model, xc, xf, v_turma_aberta, df_aluno, df_formulario, turmas_new_idx_list, param_dict)

  #-------------- Resolve
  print("Chama solver")
  status= model.solve() #COIN(maxSeconds=5) )
  
  #test
  if status > 0:
    #modelo_show_solucao(xc, xf, v_turma_aberta, y, z, v_vagas_livres, df_aluno, df_formulario, df_turma, df_serie, df_escola, turmas_new_idx_list) #debug #apagar
    modelo_show_fo(model, v_vagas_livres, v_turma_aberta, xf, turmas_new_idx_list, turmas_existentes_idx_list, df_formulario) #debug
    #print("Fase 1 - Solucao encontrada ", status)

  return xc, xf, y, z, v_vagas_livres, v_turma_aberta, turmas_new_idx_list, status

"""## Fase 1 - Salvar"""

def escolhe_nome_nova_turma(dfs_dict, df_sol_turma, nome_turma_serie):
  continua=1
  turma_char='A'
  while chr(ord(turma_char ) ).upper() != 'Z' and continua==1:
    #print(chr(ord(turma_char))) #debug
    nome_turma_tentativa = nome_turma_serie + turma_char
    #print("tentativa: ", nome_turma_tentativa)  #debug
    if nome_turma_tentativa in df_sol_turma['nome'].to_string(index=False).upper():
      continua=1
      #print("continua tentando") #debug
      turma_char = chr(ord(turma_char)+1)
    else:      
      continua=0
  
  if continua==1:
    nome_turma_completo=nome_turma_tentativa + 'b'
  else:
    nome_turma_completo=nome_turma_tentativa

  #print(nome_turma_completo)   #debug
  return nome_turma_completo

##Escrever os alunos de continuidade nas tabelas para o SQL - pegar infos da tabela aluno original
##Escrever os alunos de formulario ja alocados tambem 
##sol_turma - Se alguma turma existente nao for aberta, pode considerar como fechada.
##sol_aluno
##sol_priorizacao_formulario

def fase1_salva_resultados(dfs_dict, param_dict, xc, xf, y,z, v_vagas_livres, v_turma_aberta, turmas_new_idx_list):
  df_sol_aluno = pd.DataFrame(columns=['id','cpf','nome','email','telefone','nome_responsavel', 'telefone_responsavel','nome_escola_origem', 'sol_turma_id'])
  df_sol_formulario = pd.DataFrame(columns=['id','nome','cpf','email_aluno','telefone_aluno','nome_responsavel','telefone_responsavel','escola_id','serie_id','nome_escola_origem','sol_turma_id','status_id'])
  df_sol_turma = pd.DataFrame(columns=['id','nome', 'qtd_max_alunos', 'qtd_professores_acd', 'qtd_professores_pedagogico', 'escola_id', 'serie_id', 'aprova', 'ignore_index'])

  #------------------ Insere turmas no df_sol_turma (sql: sol_turma)
  for t in turmas_new_idx_list:
    aberta=sum( xc[(i,t)].varValue for i in dfs_dict['aluno'].index) + sum( xf[(i,t)].varValue for i in dfs_dict['formulario_inscricao'].index)
    if aberta >0:
      id_insert=0
      nome_insert=""
      
      #recupera a serie na qual a turma foi aberta
      s_idx=0
      for s in dfs_dict['serie'].index:
        if y[(t,s)].varValue >0.1:
          s_idx = s
      #recupera a escola na qual a turma foi aberta
      e_idx=0
      for e in dfs_dict['escola'].index:
        if z[(t,e)].varValue >0.1:
          e_idx = e

      #print("turma index" + str(t) + ", serie_idx="  + str(s_idx) + ", escola_idx" + str(e_idx) ) #debug
      
      #Turma ja existe
      if t in dfs_dict['turma']['id'].index:
        #print("ja existe: turma index" + str(t) + ', id='+ str(dfs_dict['turma']['id'][t]) + ' ja foi formada')   #debug      
        id_insert = dfs_dict['turma']['id'][t]
        nome_insert = dfs_dict['turma']['nome'][t]
        #print("nome_turma" + str(nome_insert))
        aprova_insert = 1
                
      else:  #Nova turma
        #print("(new) nova: turma t ="+str(t))   #debug        
        id_insert = max( df_sol_turma['id']) + 1        
        aprova_insert = 0
        
        regiao_id = dfs_dict['escola']['regiao_id'][e_idx]  
        regiao_nome = dfs_dict['regiao']['nome'][ dfs_dict['regiao']['id'] == regiao_id].to_string(index=False)   
        nome_turma_serie = regiao_nome.replace(' ','') + '_' + dfs_dict['serie']['nome'][s_idx][0]  
        nome_insert = escolhe_nome_nova_turma(dfs_dict,df_sol_turma, nome_turma_serie )

      #ADD TO DATAFRAME TURMA
      df_sol_turma = df_sol_turma.append({'id' : id_insert,
                                          'nome' : nome_insert,   
                                          'qtd_max_alunos' : param_dict['qtd_max_alunos'],
                                          'qtd_professores_acd' :  param_dict['qtd_professores_acd'],
                                          'qtd_professores_pedagogico' :  param_dict['qtd_professores_pedagogico'], #final corrigido
                                          'escola_id' : dfs_dict['escola']['id'][e_idx],
                                          'serie_id' : dfs_dict['serie']['id'][s_idx] ,
                                          'aprova' : aprova_insert,
                                          'ignore_index' : t}
                                         ,  ignore_index = True)  #todo: ignore_index = False? 


            
  #------------------ Insere alunos de formulario no df_sol_formulario (sql: sol_priorizacao_formulario)
  #lista parcial de alunos de formulario: alguns xf ja foram alocados - Essas turmas nao alteram mais

  for i in dfs_dict['formulario_inscricao'].index:
    for t in turmas_new_idx_list:
      if xf[(i,t)].varValue == 1:
        #print("aluno form index=" + str(i)+ ', id=' + str(dfs_dict['formulario_inscricao']['id'][i]) + ' alocado')  #debug
        #print("nome = " + str( dfs_dict['formulario_inscricao']['nome'][i]))  #debug
        #print(df_sol_turma['id'][ df_sol_turma['ignore_index']==t ])  #debug
        #print(int(df_sol_turma['id'][ df_sol_turma['ignore_index']==t ]))  #debug

        #ADD TO DATAFRAME SOL_PRIORIZACAO_FORMULARIO
        df_sol_formulario = df_sol_formulario.append({'id' : dfs_dict['formulario_inscricao']['id'][i],
                                                      'nome' : dfs_dict['formulario_inscricao']['nome'][i],
                                                      'cpf' : dfs_dict['formulario_inscricao']['cpf'][i],
                                                      'email_aluno' : dfs_dict['formulario_inscricao']['email_aluno'][i],
                                                      'telefone_aluno' : dfs_dict['formulario_inscricao']['telefone_aluno'][i],
                                                      'nome_responsavel' : dfs_dict['formulario_inscricao']['nome_responsavel'][i],
                                                      'telefone_responsavel' : dfs_dict['formulario_inscricao']['telefone_responsavel'][i],
                                                      'escola_id' : dfs_dict['formulario_inscricao']['escola_id'][i], 
                                                      'serie_id' : dfs_dict['formulario_inscricao']['serie_id_otim'][i],
                                                      'nome_escola_origem' : dfs_dict['formulario_inscricao']['nome_escola_origem'][i],
                                                      'sol_turma_id' : int(df_sol_turma['id'][ df_sol_turma['ignore_index']==t ]),
                                                      'status_id': ""
                                                      }, 
                ignore_index = True) 
      
  #------------------ Insere alunos de continuidade no df_sol_alunos (sql: sol_alunos)
  #todos os alunos de continuidade estao alocados
  for i in dfs_dict['aluno'].index:
    for t in turmas_new_idx_list:
      if xc[(i,t)].varValue == 1:
        #print("aluno continuidade index=" + str(i)+ ', id=' + str(dfs_dict['aluno']['id'][i]) + ' alocado')        
        #print("nome = " + str( dfs_dict['aluno']['nome'][i]))
        #print(df_sol_turma['id'][ df_sol_turma['ignore_index']==t ])
        #print(int(df_sol_turma['id'][ df_sol_turma['ignore_index']==t ]))

        #ADD TO DATAFRAME SOL_ALUNO
        df_sol_aluno = df_sol_aluno.append({'id' : dfs_dict['aluno']['id'][i],
                                            'cpf' : dfs_dict['aluno']['cpf'][i],
                                            'nome' : dfs_dict['aluno']['nome'][i],
                                            'email': dfs_dict['aluno']['email'][i],
                                            'telefone': dfs_dict['aluno']['telefone'][i],
                                            'nome_responsavel': dfs_dict['aluno']['nome_responsavel'][i],
                                            'telefone_responsavel': dfs_dict['aluno']['telefone_responsavel'][i],
                                            'nome_escola_origem': dfs_dict['aluno']['nome_escola_origem'][i],                                          
                                          'sol_turma_id' : int(df_sol_turma['id'][ df_sol_turma['ignore_index']==t]) },  
                ignore_index = True) 



  #conn_sol = sqlite3.connect("bd_saida_teste_fase1.db") #debug
 
  #debug
  #Nao salva coluna ignore_index
  #df_sol_turma[['id','nome', 'qtd_max_alunos', 'qtd_professores_acd', 'qtd_professores_pedagogico', 'escola_id', 'serie_id', 'aprova']].to_sql('sol_turma', con = conn_sol, if_exists = 'replace', chunksize = 1000)  
  #df_sol_formulario.to_sql('sol_priorizacao_formulario', con = conn_sol, if_exists = 'replace', chunksize = 1000)
  #df_sol_aluno.to_sql('sol_aluno', con = conn_sol, if_exists = 'replace', chunksize = 1000)

  return df_sol_turma, df_sol_aluno, df_sol_formulario

"""# Fase 2 - Cria novas turmas para os alunos de formulario

## Regra de desempate
"""

def escolhe_escola_desempate(dfs_dict, max_escolaid1, max_escolaid2,bool_escolhe_1, bool_escolhe_2, bool_escolhe_aleatoriamente):  
  qtd_alunos_1 = len(dfs_dict['escola'][dfs_dict['escola']['id']== max_escolaid1].index)
  qtd_alunos_2 = len(dfs_dict['escola'][dfs_dict['escola']['id']== max_escolaid12].index)

  if qtd_alunos_1 < qtd_alunos_2:
    bool_escolhe_1 = True
  elif qtd_alunos_2 < qtd_alunos_1:
    bool_escolhe_2 = True
  else: # escolhe a escola com menos turmas
    qtd_turmas_1 = len(dfs_dict['turma'][dfs_dict['turma']['escola_id']==max_escolaid1].index)
    qtd_turmas_2 = len(dfs_dict['turma'][dfs_dict['turma']['escola_id']==max_escolaid2].index)

    if qtd_turmas_1 < qtd_turmas_2:
      bool_escolhe_1 = True
    elif qtd_turmas_2 < qtd_turmas_1:
      bool_escolhe_2 = True
    else: #se a quantidade de turmas (e de alunos) nas escolas for igual entao escolhe aleatoriamente
      bool_escolhe_aleatoriamente = True
      
  return bool_escolhe_1, bool_escolhe_2, bool_escolhe_aleatoriamente

#escolhe a proxima serie/escola para abrir, so com alunos de formulario, de acordo com as regras de demanda
def fase2_calc_next_serie_abrir(dfs_dict,param_dict,df_formulario_restante, param_tolerancia):
  import random
  
  #Tres opcoes de escolha:
  bool_escolhe_1 = False #maior demanda
  bool_escolhe_2 = False #segunda maior demanda
  bool_escolhe_aleatoriamente = False #aleatorio

  max_dmd1=0
  max_serieid1=0
  max_escolaid1=0
  max_dmd2=0
  max_serieid2=0
  max_escolaid2=0

  serie_id_sel=0
  escola_id_sel=0
  demanda_sel=0

  for eidx in dfs_dict['escola'].index:
    for sidx in dfs_dict['serie'].index:
      #print("serie index=",sidx) #debug
      #print("escola index=",eidx) #debug
      
      demanda= len(df_formulario_restante[ (df_formulario_restante['serie_id_otim']== dfs_dict['serie']['id'][sidx] ) & (df_formulario_restante['escola_id']== dfs_dict['escola']['id'][eidx]) ].index)
      
      #print("demanda",demanda) #debug
      
      if demanda > max_dmd1:   
        max_dmd2=max_dmd1
        max_serieid2=max_serieid1
        max_escolaid2=max_escolaid1
        
        max_dmd1 = demanda
        max_serieid1 = dfs_dict['serie']['id'][sidx]
        max_escolaid1= dfs_dict['escola']['id'][eidx]
      elif demanda > max_dmd2:
        max_dmd2 = demanda
        max_serieid2 = dfs_dict['serie']['id'][sidx]
        max_escolaid2= dfs_dict['escola']['id'][eidx]

  tolerancia = param_tolerancia*param_dict['qtd_max_alunos']
 
  #print("max1..2")  #debug
  #print(max_dmd1)   #debug
  #print(max_dmd2)   #debug
  print("1a Maior demanda = " + str(max_dmd1) + ", serie="+ str(max_serieid1) + ", escola=" + str(max_escolaid1)) #debug 
  print("2a maior demanda = " + str(max_dmd2) + ", serie="+ str(max_serieid2) +  ", escola=" + str(max_escolaid2)) #debug 

  #Se a diferenca na demanda for maior do que a tolerancia, abre a turma com maior demanda
  if max_dmd1 - max_dmd2 > tolerancia or max_dmd2==0:
    #prioriza a maior demanda
    #print("dentro da tolerancia") #debug
    bool_escolhe_1 = True

  #Caso contrario deve ser priorizada a série mais nova, ou seja 9o ano tem maior prioridade, seguido do 1o ano, 2o ano e, por fim, 3o ano com a menor prioridade.
  else:
    max_ordem1 = int(dfs_dict['serie']['ordem'][ dfs_dict['serie']['id']== max_serieid1])
    max_ordem2 = int(dfs_dict['serie']['ordem'][ dfs_dict['serie']['id']== max_serieid2])

    #print("max...")
    #print(max_serieid1)
    #print(max_ordem2)  
    #print(max_serieid2)
    #print(max_ordem2)
    if max_ordem1 < max_ordem2:
      bool_escolhe_1 = True
    elif max_ordem2 < max_ordem1:
      bool_escolhe_2 = True
    else: #max_ordem1 == max_ordem2, ou seja mesma serie

      #conferir se as duas maiores demandas são na mesma  escola. Se sim, cai na seguinte pergunta do checkpoint 4:
      if max_escolaid1 == max_escolaid2:
        #pergunta 10: novo critério de desempate, duas maiores demandas na mesma escola e com o mesmo valor
        #os critérios de escolha são, na ordem: 
        #1) escolher a escola com menos alunos;
        # 2) escolher a escola com menos turmas; 
        #3) se o empate permanecer, a escolha deve ser feita aleatoriamente.
        bool_escolhe_1, bool_escolhe_2, bool_escolhe_aleatoriamente = escolhe_escola_desempate(dfs_dict, max_escolaid1, max_escolaid2,bool_escolhe_1, bool_escolhe_2, bool_escolhe_aleatoriamente)
        print("... desempate escola") #debug apagar
      #se estao na mesma serie e escolas diferentes, entao escolhe aleatoriamente  
      else:
        #escolhe aleatoriamente
        bool_escolhe_aleatoriamente = True
    
  if bool_escolhe_1 == True:
    print("Abre a 1a maior demanda")
    serie_id_sel = max_serieid1
    escola_id_sel = max_escolaid1
    demanda_sel=max_dmd1
  elif bool_escolhe_2 == True:
    print("Abre a 2a maior demanda")
    serie_id_sel = max_serieid2
    escola_id_sel = max_escolaid2
    demanda_sel=max_dmd2
  elif bool_escolhe_aleatoriamente == True:
    print("Escolhe aleatoriamente")
    serie_id_sel = random.choice([max_serieid1, max_serieid2])
    if serie_id_sel == max_serieid1:
      escola_id_sel = max_escolaid1
      demanda_sel=max_dmd1
    else:
      escola_id_sel = max_escolaid2
      demanda_sel=max_dmd2

  # print("..... bool_escolhe:="+ str(bool_escolhe_1) + ", " + str(bool_escolhe_2) + ", " + str(bool_escolhe_aleatoriamente))
  # print("..... serie_id_sel",serie_id_sel) #debug 
  # print("..... escola_id_sel",escola_id_sel) #debug
  # print("..... demanda_sel",demanda_sel) #debug

  return serie_id_sel, escola_id_sel

def fase2_novo_orcamento(param_dict, num_alunos_turma, orcamento_restante):
  custo_turma_professores_t = param_dict['custo_professor']*(param_dict['qtd_professores_pedagogico'] + param_dict['qtd_professores_acd'])
  custo_turma_alunos_t = ( num_alunos_turma )* param_dict['custo_aluno']
  orcamento = (custo_turma_professores_t + custo_turma_alunos_t)

  orcamento_restante2 = orcamento_restante- orcamento

  orcamento_count_alunos = (orcamento_restante2 - custo_turma_professores_t)/param_dict['custo_aluno']
  
  #Limitante superior para o numero de alunos na proxima turma:
  num_max_alunos = int(min(orcamento_count_alunos, param_dict['qtd_max_alunos']))

  return orcamento_restante2, num_max_alunos

"""## Fase 2 - Salvar"""

#salvar
def fase2_salva_resultados(dfs_dict, param_dict, df_sol_turma, df_sol_formulario, formulario_selecionados, serie_id_sel, escola_id_sel, turma_id_max_existente):
  #cria uma nova turma para esse pessoal        
  if len(df_sol_turma.index)>0:
    turma_id_insert = max(turma_id_max_existente, max( df_sol_turma['id'])) + 1  
  else : 
    turma_id_insert = turma_id_max_existente + 1
  
  print("turma_id e="+str(turma_id_insert))#test      
  aprova_insert = 0

  serie_id_sel 
  escola_id_sel
        
  regiao_id = int( dfs_dict['escola']['regiao_id'][  dfs_dict['escola']['id'] == escola_id_sel  ]   )  
  regiao_nome = dfs_dict['regiao']['nome'][ dfs_dict['regiao']['id'] == regiao_id].to_string(index=False)   
  nome_serie = dfs_dict['serie']['nome'][  dfs_dict['serie']['id']==serie_id_sel  ].to_string(index=False)
  nome_serie = nome_serie.replace(' ','') 
  nome_turma_serie = regiao_nome.replace(' ','') + '_' + nome_serie[0]    
  nome_insert = escolhe_nome_nova_turma(dfs_dict, df_sol_turma, nome_turma_serie )

  #print("reg id", regiao_id) #debug
  #print("reg nome", regiao_nome) #debug
  #print(nome_turma_serie) #debug
  #print("nome_insert") #debug
  #print( nome_insert) #debug

  #ADD TO DATAFRAME TURMA
  df_sol_turma = df_sol_turma.append({'id' : turma_id_insert,
                                      'nome' : nome_insert,   
                                      'qtd_max_alunos' : param_dict['qtd_max_alunos'],
                                      'qtd_professores_acd' :  param_dict['qtd_professores_acd'],
                                      #'qtd_professores_pedagogico' :  param_dict['qtd_professores_acd'],
                                      'qtd_professores_pedagogico' :  param_dict['qtd_professores_pedagogico'], #final
                                      'escola_id' : escola_id_sel,
                                      'serie_id' : serie_id_sel,
                                      'aprova' : 0,
                                      'ignore_index' : -1}
                                      ,  ignore_index = True) 


  #alunos formulario: 
  for i in formulario_selecionados.index:
    df_sol_formulario = df_sol_formulario.append({'id' : dfs_dict['formulario_inscricao']['id'][i],
                                                    'nome' : dfs_dict['formulario_inscricao']['nome'][i],
                                                    'cpf' : dfs_dict['formulario_inscricao']['cpf'][i],
                                                    'email_aluno' : dfs_dict['formulario_inscricao']['email_aluno'][i],
                                                    'telefone_aluno' : dfs_dict['formulario_inscricao']['telefone_aluno'][i],
                                                    'nome_responsavel' : dfs_dict['formulario_inscricao']['nome_responsavel'][i],
                                                    'telefone_responsavel' : dfs_dict['formulario_inscricao']['telefone_responsavel'][i],
                                                    'escola_id' : dfs_dict['formulario_inscricao']['escola_id'][i], 
                                                    'serie_id' : dfs_dict['formulario_inscricao']['serie_id_otim'][i],
                                                    'nome_escola_origem' : dfs_dict['formulario_inscricao']['nome_escola_origem'][i],
                                                    'sol_turma_id' : turma_id_insert,
                                                    'status_id': ""
                                                    }, 
              ignore_index = True) 

  #conn_sol = sqlite3.connect("bd_saida_teste_fase2.db") #debug
  #Escreve no sql - fase 2 #debug
  #df_sol_turma[['id','nome', 'qtd_max_alunos', 'qtd_professores_acd', 'qtd_professores_pedagogico', 'escola_id', 'serie_id', 'aprova']].to_sql('sol_turma', con = conn_sol, if_exists = 'replace', chunksize = 1000)  
  #df_sol_formulario.to_sql('sol_priorizacao_formulario', con = conn_sol, if_exists = 'replace', chunksize = 1000)
  
  return df_sol_turma, df_sol_formulario

"""# Relatorios

## Relatorio turma
"""

#salvar
def gera_relatorio_turma(file_BD,param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario):
  #turma
  #número de alunos de continuidade alocados na turma - qtd_alunos_continuidade
  #número de candidatos de formulário alocados na turma - qtd_alunos_formulario
  #número total de alunos alocados na turma - total_alunos
  #meta ou capacidade da turma (ou seja, quantidade de alunos que a turma pode atender) - qtd_max_alunos
  #meta atingida percentual (ou seja, proporção de alunos alocado em relação à meta daquela turma) - proporcao_alunos_alocados 

  df_relatorio_turma = pd.DataFrame(columns=['id','nome', 'qtd_alunos_continuidade_alocados', 'qtd_alunos_formulario_alocados', 
                                             'total_alunos', 'qtd_max_alunos','proporcao_alunos_alocados'])
        
  for i in df_sol_turma.index:
    #print(i)    
    aluno_turma = df_sol_aluno[ df_sol_aluno['sol_turma_id'] == df_sol_turma['id'][i]  ]
    qtd_alunos_continuidade = len(aluno_turma.index)
    form_turma = df_sol_formulario[ df_sol_formulario['sol_turma_id'] == df_sol_turma['id'][i]  ]
    qtd_alunos_formulario = len(form_turma.index)
    total_alunos = qtd_alunos_continuidade + qtd_alunos_formulario
    qtd_max_alunos = param_dict['qtd_max_alunos']
    proporcao_alunos_alocados = total_alunos/qtd_max_alunos
    
    #print("turma_id="+str(df_sol_turma['id'][i])) #debug
    #print("turma_nome="+str(df_sol_turma['nome'][i])) #debug
    #print("serie_id="+str(df_sol_turma['serie_id'][i])) #debug
    #print("alunos continuidade=" + str(qtd_alunos_continuidade)) #debug
    #print("List alunos: " + list_continuidade)  #debug
    #print("alunos formulario=" + str(qtd_alunos_formulario))   #debug
    #print("List formulario: " + list_formulario) #debug

    df_relatorio_turma = df_relatorio_turma.append({'id' : df_sol_turma['id'][i],
                                                    'nome' : df_sol_turma['nome'][i],
                                                    'qtd_alunos_continuidade_alocados' : qtd_alunos_continuidade,
                                                  'qtd_alunos_formulario_alocados' : qtd_alunos_formulario,
                                                  'total_alunos' : total_alunos,
                                                  'qtd_max_alunos' : qtd_max_alunos,
                                                  'proporcao_alunos_alocados' : proporcao_alunos_alocados},
                ignore_index = True)
    

    #df_relatorio_turma

  salva_BD_relatorio(file_BD, 'sol_relatorio_turma', df_relatorio_turma)
  return df_relatorio_turma

#df_relatorio_turma = gera_relatorio_turma(file_BD,param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario)
#df_relatorio_turma

"""## Relatorio turma - lista alunos"""

#salvar
def gera_relatorio_turma_list_alunos(file_BD, param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario, df_regiao, df_escola, df_serie):                                                                                            
  #turma
  #número de alunos de continuidade alocados na turma - qtd_alunos_continuidade
  #número de candidatos de formulário alocados na turma - qtd_alunos_formulario
  #número total de alunos alocados na turma - total_alunos
  #meta ou capacidade da turma (ou seja, quantidade de alunos que a turma pode atender) - qtd_max_alunos
  #meta atingida percentual (ou seja, proporção de alunos alocado em relação à meta daquela turma) - proporcao_alunos_alocados 

  df_relatorio_turma_list_alunos = pd.DataFrame(columns=['id','nome', 
                                                         'qtd_alunos_continuidade_alocados', 
                                                         'qtd_alunos_formulario_alocados', 
                                              'total_alunos', 'qtd_max_alunos','proporcao_alunos_alocados',
                                              'serie_id','serie_nome',
                                              'escola_id', 'escola_nome',
                                              'regiao_id','regiao_nome',
                                            'list_continuidade', 'list_formulario'])       
  for i in df_sol_turma.index:
    #print(i)    
    aluno_turma = df_sol_aluno[ df_sol_aluno['sol_turma_id'] == df_sol_turma['id'][i]  ]
    qtd_alunos_continuidade = len(aluno_turma.index)
    form_turma = df_sol_formulario[ df_sol_formulario['sol_turma_id'] == df_sol_turma['id'][i]  ]
    qtd_alunos_formulario = len(form_turma.index)
    total_alunos = qtd_alunos_continuidade + qtd_alunos_formulario
    qtd_max_alunos = param_dict['qtd_max_alunos']
    proporcao_alunos_alocados = total_alunos/qtd_max_alunos
    
    list_continuidade = str( tuple(aluno_turma['id'].tolist()) ) 
    list_formulario = str( tuple(form_turma['id'].tolist()) ) 
    
    serie_nome =  df_serie['nome'][df_serie['id'] == df_sol_turma['serie_id'][i] ].to_string(index=False) 
    escola_nome = df_escola['nome'][ df_escola['id'] == df_sol_turma['escola_id'][i] ].to_string(index=False) 

    regiao_id = int(df_escola['regiao_id'][ df_escola['id'] == df_sol_turma['escola_id'][i] ])
    regiao_nome = df_regiao['nome'][ df_regiao['id'] == regiao_id  ].to_string(index=False) 
    #print("turma_id="+str(df_sol_turma['id'][i])) #apagar
    #print("turma_nome="+str(df_sol_turma['nome'][i])) #apagar
    #print("serie_id="+str(df_sol_turma['serie_id'][i])) #apagar
    #print("alunos continuidade=" + str(qtd_alunos_continuidade)) #apagar
    #print("List alunos: " + list_continuidade)     #apagar
    #print("alunos formulario=" + str(qtd_alunos_formulario))  #apagar
    #print("List formulario: " + list_formulario) #apagar

    df_relatorio_turma_list_alunos = df_relatorio_turma_list_alunos.append({'id' : df_sol_turma['id'][i],
                                                    'nome' : df_sol_turma['nome'][i],
                                                    'qtd_alunos_continuidade_alocados' : qtd_alunos_continuidade,
                                                  'qtd_alunos_formulario_alocados' : qtd_alunos_formulario,
                                                  'total_alunos' : total_alunos,
                                                  'qtd_max_alunos' : qtd_max_alunos,
                                                  'proporcao_alunos_alocados' : proporcao_alunos_alocados,
                                                  'serie_id' : df_sol_turma['serie_id'][i],
                                                  'serie_nome': serie_nome,                                              
                                                  'escola_id' : df_sol_turma['escola_id'][i],
                                                  'escola_nome' : escola_nome,
                                                  'regiao_id' : regiao_id,
                                                  'regiao_nome' : regiao_nome,
                                                  'list_continuidade' : list_continuidade,
                                                  'list_formulario' : list_formulario},
                ignore_index = True)
    

  salva_BD_relatorio(file_BD, 'sol_relatorio_turma_lista_alunos', df_relatorio_turma_list_alunos)

  return df_relatorio_turma_list_alunos

#df_relatorio_turma_list_alunos = gera_relatorio_turma_list_alunos(file_BD, param_dict, df_sol_turma,  df_sol_aluno,df_sol_formulario, dfs_dict['regiao'], dfs_dict['escola'], dfs_dict['serie'])  
#df_relatorio_turma_list_alunos

"""## Relatorio orcamento"""

#salvar
def gera_relatorio_orcamento(file_BD,param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario):
  #turma
  #número de alunos de continuidade alocados na turma - qtd_alunos_continuidade
  #número de candidatos de formulário alocados na turma - qtd_alunos_formulario
  #número total de alunos alocados na turma - total_alunos
  #meta ou capacidade da turma (ou seja, quantidade de alunos que a turma pode atender) - qtd_max_alunos
  #meta atingida percentual (ou seja, proporção de alunos alocado em relação à meta daquela turma) - proporcao_alunos_alocados 

  df_relatorio_orcamento = pd.DataFrame(columns=['id','nome', 'qtd_alunos_continuidade', 'qtd_alunos_formulario', 
                                             'total_alunos', 'custo_turma', 'limite_custo', 'proporcao_custo_turma'])
                                             #'qtd_max_alunos',                                             
                                             #'proporcao_alunos_alocados'])
        
  for i in df_sol_turma.index:
    #print(i)    
    aluno_turma = df_sol_aluno[ df_sol_aluno['sol_turma_id'] == df_sol_turma['id'][i]  ]
    qtd_alunos_continuidade = len(aluno_turma.index)
    form_turma = df_sol_formulario[ df_sol_formulario['sol_turma_id'] == df_sol_turma['id'][i]  ]
    qtd_alunos_formulario = len(form_turma.index)
    total_alunos = qtd_alunos_continuidade + qtd_alunos_formulario
    qtd_max_alunos = param_dict['qtd_max_alunos']
    proporcao_alunos_alocados = total_alunos/qtd_max_alunos
    
    #print("turma_id="+str(df_sol_turma['id'][i])) #apagar
    #print("turma_nome="+str(df_sol_turma['nome'][i])) #apagar
    #print("serie_id="+str(df_sol_turma['serie_id'][i])) #apagar
    #print("alunos continuidade=" + str(qtd_alunos_continuidade)) #apagar
    #print("List alunos: " + list_continuidade)     #apagar
    #print("alunos formulario=" + str(qtd_alunos_formulario))   #apagar
    #print("List formulario: " + list_formulario)#apagar


    custo_turma_professores_t = param_dict['custo_professor']*(param_dict['qtd_professores_pedagogico'] + param_dict['qtd_professores_acd'])
    custo_turma_alunos_t = ( total_alunos)* param_dict['custo_aluno']
    custo_turma = ( custo_turma_professores_t + custo_turma_alunos_t)

    df_relatorio_orcamento = df_relatorio_orcamento.append({'id' : df_sol_turma['id'][i],
                                                    'nome' : df_sol_turma['nome'][i],'qtd_alunos_continuidade' : qtd_alunos_continuidade,
                                                  'qtd_alunos_formulario' : qtd_alunos_formulario,
                                                  'total_alunos' : total_alunos,
                                                  'custo_turma' : custo_turma,
                                                  'limite_custo' : param_dict['limite_custo'],
                                                  'proporcao_custo_turma' : custo_turma/param_dict['limite_custo']},
                ignore_index = True)
    

    #df_relatorio_turma

  salva_BD_relatorio(file_BD, 'sol_relatorio_orcamento', df_relatorio_orcamento[['id','nome', 'qtd_alunos_continuidade', 
                                                                             'qtd_alunos_formulario', 'total_alunos',
                                                                             'custo_turma', 'limite_custo', 'proporcao_custo_turma']])
  return df_relatorio_orcamento

#df_relatorio_orcamento = gera_relatorio_orcamento(file_BD,param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario)
#df_relatorio_orcamento

"""## Relatorio serie"""

#para cada serie, calcula o numero de turmas abertas
def gera_relatorio_serie(file_BD,param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario, df_serie):
  df_relatorio_serie = pd.DataFrame(columns = ['serie_id', 'serie_nome','numero_turmas', 'qtd_alunos_continuidade',
                                               'qtd_alunos_formulario', 'qtd_alunos_total'])
  

  for serie_id in pd.unique(df_sol_turma['serie_id']):
    #numero de turmas dessa serie 
    #print("serie id="+str(serie_id))
    turmas_id_list = list( df_sol_turma['id'][df_sol_turma['serie_id'] == serie_id] )
    numero_turmas = len(turmas_id_list)
    nome = df_serie['nome'][df_serie['id'] == serie_id].to_string(index=False)
    #print(nome)
    #print(turmas_id_list)
    #print(turmas_id_list[0])
    #print(turmas_id_list[1])    
    #print("numero turmas="+str(numero_turmas))
    #print(df_sol_aluno[ df_sol_aluno['sol_turma_id'].isin(turmas_id_list)])

    qtd_alunos_continuidade = len(df_sol_aluno[ df_sol_aluno['sol_turma_id'].isin(turmas_id_list)])
    qtd_alunos_formulario  = len(df_sol_formulario[ df_sol_formulario['sol_turma_id'].isin(turmas_id_list)])
    qtd_alunos_total = qtd_alunos_continuidade + qtd_alunos_formulario

    df_relatorio_serie = df_relatorio_serie.append({'serie_id': serie_id,
                                                    'serie_nome': nome,
                                                    'numero_turmas' : numero_turmas,
                                                    'qtd_alunos_continuidade' : qtd_alunos_continuidade,
                                                    'qtd_alunos_formulario' : qtd_alunos_formulario,
                                                    'qtd_alunos_total': qtd_alunos_total},
                                                   ignore_index=True)
  
  salva_BD_relatorio(file_BD, 'sol_relatorio_serie', df_relatorio_serie[['serie_id', 'serie_nome','numero_turmas', 'qtd_alunos_continuidade',
                                               'qtd_alunos_formulario', 'qtd_alunos_total']])    
  return df_relatorio_serie

#df_relatorio_serie = gera_relatorio_serie(file_BD, param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario, dfs_dict['serie'])
#df_relatorio_serie

"""## Relatorio escola"""

def gera_relatorio_escola(file_BD,param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario, df_escola, df_regiao):
  df_relatorio_escola = pd.DataFrame(columns = ['escola_id', 'escola_nome', 'regiao_id','regiao_nome','numero_turmas', 'qtd_series','qtd_alunos_continuidade',
                                               'qtd_alunos_formulario', 'qtd_alunos_total'])
  
  for escola_id in pd.unique(df_sol_turma['escola_id']):
    #numero de turmas dessa serie 
    #print("escola id="+str(escola_id)) #apagar
  
    turmas_id_list = list( df_sol_turma['id'][df_sol_turma['escola_id'] == escola_id] )
    numero_turmas = len(turmas_id_list)
    escola_row = df_escola[df_escola['id'] == escola_id]    
    escola_nome = escola_row['nome'].to_string(index=False)
    
    regiao_id = int(escola_row['regiao_id'])    
    regiao_nome = df_regiao['nome'][ df_regiao['id'] == regiao_id ].to_string(index=False)     
    
    #print("regiao_nome")#apagar
    #print(regiao_nome)#apagar
    #print(df_regiao['nome']) #apagar
    #print(nome) #apagar
    #print(turmas_id_list) #apagar
    #print(turmas_id_list[0]) #apagar
    #print(turmas_id_list[1])     #apagar
    #print("numero turmas="+str(numero_turmas)) #apagar
    #print(df_sol_aluno[ df_sol_aluno['sol_turma_id'].isin(turmas_id_list)]) #apagar

    qtd_series = len(pd.unique( df_sol_turma['serie_id'][ df_sol_turma['escola_id'] == escola_id] ) )

    qtd_alunos_continuidade = len(df_sol_aluno[ df_sol_aluno['sol_turma_id'].isin(turmas_id_list)])
    qtd_alunos_formulario  = len(df_sol_formulario[ df_sol_formulario['sol_turma_id'].isin(turmas_id_list)])
    qtd_alunos_total = qtd_alunos_continuidade + qtd_alunos_formulario

    df_relatorio_escola = df_relatorio_escola.append({'escola_id': escola_id,                                                      
                                                    'escola_nome': escola_nome,
                                                    'regiao_id' : regiao_id,
                                                    'regiao_nome' : regiao_nome,                                                  
                                                    'numero_turmas' : numero_turmas,
                                                    'qtd_series' : qtd_series,
                                                    'qtd_alunos_continuidade' : qtd_alunos_continuidade,
                                                    'qtd_alunos_formulario' : qtd_alunos_formulario,
                                                    'qtd_alunos_total': qtd_alunos_total},
                                                   ignore_index=True)
  salva_BD_relatorio(file_BD, 'sol_relatorio_escola', df_relatorio_escola[['escola_id', 'escola_nome', 'regiao_id','regiao_nome','numero_turmas', 'qtd_series','qtd_alunos_continuidade',
                                               'qtd_alunos_formulario', 'qtd_alunos_total']])    
  
  return df_relatorio_escola

# df_relatorio_escola = gera_relatorio_escola(file_BD, param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario, dfs_dict['escola'], dfs_dict['regiao'])
# df_relatorio_escola

"""## Relatorio alunos de formulario nao alocados"""

def gera_relatorio_formulario_nao_alocados(file_BD, df_formulario_restante):
  df_formulario_nao_alocados = pd.DataFrame(columns=['id','nome','cpf','email_aluno','telefone_aluno','nome_responsavel','telefone_responsavel','escola_id','serie_id','nome_escola_origem','ordem_inscricao'])
 
  for i in df_formulario_restante.index:
    df_formulario_nao_alocados = df_formulario_nao_alocados.append({'id' : df_formulario_restante['id'][i],
                                                    'nome' : df_formulario_restante['nome'][i],
                                                    'cpf' : df_formulario_restante['cpf'][i],
                                                    'email_aluno' : df_formulario_restante['email_aluno'][i],
                                                    'telefone_aluno' : df_formulario_restante['telefone_aluno'][i],
                                                    'nome_responsavel' : df_formulario_restante['nome_responsavel'][i],
                                                    'telefone_responsavel' : df_formulario_restante['telefone_responsavel'][i],
                                                    'escola_id' : df_formulario_restante['escola_id'][i], 
                                                    'serie_id' : df_formulario_restante['serie_id_otim'][i],
                                                    'nome_escola_origem' : df_formulario_restante['nome_escola_origem'][i],
                                                    'ordem_inscricao' : df_formulario_restante['rank'][i]
                                                    #'status_id': ""
                                                    }, 
              ignore_index = True) 
  
  salva_BD_relatorio(file_BD, 'sol_relatorio_formulario_nao_alocados', df_formulario_nao_alocados)    

  return df_formulario_nao_alocados

"""## Relatorio geral"""

def relatorio_append(df_relatorio_geral, id, chave, valor):
  df_relatorio_geral = df_relatorio_geral.append({'id' : id,
                                                  'chave' : chave,
                                                  'valor': valor   
      
  }, ignore_index = True)

  return df_relatorio_geral

##salvar
def gera_relatorio_geral(file_BD,param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario, df_formulario):                                                                                     

  df_relatorio_geral = pd.DataFrame(columns=['id', 'chave', 'valor'])
                                                 
  numero_turmas = len(df_sol_turma.index)
  df_relatorio_geral = relatorio_append(df_relatorio_geral, 1, 'numero_turmas', numero_turmas)
  
  qtd_alunos_continuidade = len(df_sol_aluno.index)
  df_relatorio_geral = relatorio_append(df_relatorio_geral, 2, 'qtd_alunos_continuidade', qtd_alunos_continuidade)

  qtd_alunos_formulario = len(df_sol_formulario.index)
  df_relatorio_geral = relatorio_append(df_relatorio_geral, 3, 'qtd_alunos_formulario', qtd_alunos_formulario)

  max_alunos_formulario = len(df_formulario.index)
  df_relatorio_geral = relatorio_append(df_relatorio_geral, 4, 'max_alunos_formulario', max_alunos_formulario)

  proporcao_alunos_formulario_alocados = qtd_alunos_formulario/max_alunos_formulario
  df_relatorio_geral = relatorio_append(df_relatorio_geral, 5, 'proporcao_alunos_formulario_alocados', proporcao_alunos_formulario_alocados)

  custo_turma_professores_t = param_dict['custo_professor']*(param_dict['qtd_professores_pedagogico'] + param_dict['qtd_professores_acd'])
  custo_turma_alunos_t = ( qtd_alunos_continuidade + qtd_alunos_formulario)* param_dict['custo_aluno']
  total_custo = (numero_turmas * custo_turma_professores_t + custo_turma_alunos_t)

  df_relatorio_geral = relatorio_append(df_relatorio_geral, 6, 'total_custo', total_custo)

  df_relatorio_geral = relatorio_append(df_relatorio_geral, 7, 'limite_custo', param_dict['limite_custo'])

  proporcao_custo_limite = total_custo / param_dict['limite_custo']
  df_relatorio_geral = relatorio_append(df_relatorio_geral, 8, 'proporcao_custo_limite', proporcao_custo_limite)

  salva_BD_relatorio(file_BD, 'sol_relatorio_geral', df_relatorio_geral[['id', 'chave', 'valor']])    
  
  return df_relatorio_geral

#df_relatorio_geral = gera_relatorio_geral(file_BD,param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario, dfs_dict['formulario_inscricao'] )
#df_relatorio_geral

"""Relatorios: 

alunos por turma: resumo (obrigatorio) - ok 1

alunos por turma com lista de alunos - ok 1 (apenas debug)

orçamento por turma - ok 1

alunos/ turmas por serie - ok 1

alunos/ turmas/ serie por escola - ok 1

turmas/ alunos alocados/ orçamento gerais - ok 1

Lista de espera: alunos de formulario - ok 1
"""

def relatorios_extras(file_BD, param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario, dfs_dict, df_formulario_restante):
  df_relatorio_turma_list_alunos = gera_relatorio_turma_list_alunos(file_BD, param_dict, df_sol_turma,  df_sol_aluno,df_sol_formulario, dfs_dict['regiao'], dfs_dict['escola'], dfs_dict['serie'])  
  df_relatorio_orcamento = gera_relatorio_orcamento(file_BD,param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario)    
  df_relatorio_serie = gera_relatorio_serie(file_BD, param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario, dfs_dict['serie'])
  df_relatorio_escola = gera_relatorio_escola(file_BD, param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario, dfs_dict['escola'], dfs_dict['regiao'])
  df_relatorio_geral = gera_relatorio_geral(file_BD,param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario, dfs_dict['formulario_inscricao'] )  
  df_relatorio_formulario_nao_alocados = gera_relatorio_formulario_nao_alocados(file_BD,df_formulario_restante)

"""# Alerta de consistencia"""

#Condicao de alerta: procura alunos duplicados e salva em uma tabela sql
def gera_alerta_alunos_param_duplicados(file_BD, df_aluno_param, tab_nome):
  df_aluno_param_duplicados = df_aluno_param[ df_aluno_param.duplicated(subset=['cpf'], keep=False) ]
  df_aluno_param_duplicados = df_aluno_param_duplicados.sort_values(by='id')
  salva_BD_relatorio(file_BD, tab_nome, df_aluno_param_duplicados)    

  return df_aluno_param_duplicados

def alertas_consistencia(file_BD, param_dict, dfs_dict):
  #consistencias relacionadas a desconsiderar os alunos que vao se formar ja sao feitas no pre-processamento

  #Alunos de continuidade duplicados
  df_aluno_duplicado = gera_alerta_alunos_param_duplicados(file_BD, dfs_dict['aluno'], 'alerta_aluno_duplicado')
  #Alunos de formulario duplicados
  df_formulario_duplicado = gera_alerta_alunos_param_duplicados(file_BD, dfs_dict['formulario_inscricao'], 'alerta_formulario_duplicado')

#alertas_consistencia(file_BD, param_dict, dfs_dict)

"""# Fase 0 - Confere factibilidade e ajusta

## Junta turmas
"""

#Tenta juntar as turmas ja existentes. Se for possivel modifica a turma dos alunos.
def junta_turmas(df_aluno, df_turma, param_dict):  

  #check every combination of
  turmas_id_list = df_aluno['turma_id'].unique()
  for t1 in turmas_id_list:
    #qtd_alunos_t1 = len(df_aluno[ df_aluno['turma_id'] == t1].index )
    qtd_alunos_t1 = len(df_aluno[ (df_aluno['turma_id'] == t1) & (df_aluno['reprova']==0)].index )
    if qtd_alunos_t1 > 0:
      # print("***** turma = " + str(t1)) #apagar
      #lista de turmas na mesma serie e mesma escola que t1
      serie_id = int( df_turma['serie_id'][df_turma['id']==t1] ) #estava na serie_id
      escola_id = int( df_turma['escola_id'][df_turma['id']==t1] )

      turmas_id_cand =  np.unique( list(df_turma['id'][ (df_turma['id']!= t1) & (df_turma['serie_id']==serie_id) & (df_turma['escola_id']==escola_id)  ]))
      #print("candidatas") #apagar
      #print(turmas_id_cand) #apagar
      for t2 in turmas_id_cand:
        qtd_alunos_t2 = len(df_aluno[ (df_aluno['turma_id'] == t2)  & (df_aluno['reprova']==0)].index )
     
        #print("----- serie=" + str(serie_id) + ", escola=" + str(escola_id) + ": alunos turma_id:"+str(t1)+" ="+str(qtd_alunos_t1)+", alunos turma_id:"+str(t2)+" ="+str(qtd_alunos_t2) + ", total de alunos="+ str(qtd_alunos_t1 + qtd_alunos_t2)) #apagar #debug
     
        if qtd_alunos_t1 + qtd_alunos_t2 <= param_dict['qtd_max_alunos']:
          #junta as turmas
          print("Junta turmas " + str(t1) + " e " + str(t2)) #apagar

          alunos_index = df_aluno[ df_aluno['turma_id'] == t2 ].index
          #print(alunos_index) #apagar
          df_aluno.loc[ alunos_index ,'turma_id'] = t1

  return df_aluno

"""## Fecha turmas desnecessarias"""

def fecha_turmas_desnecessarias(param_dict, param_dict_ajuste, df_aluno, df_turma):
  #Faz esse procecedimento em todos os casos. Mesmo se nao faltar orcamento, pode excluir turmas existentes se elas nao forem necessarias
  #opcao e so executar se for infactivel..

  #otimizacao dentro do ano: pode juntar as turmas e excluir as desnecessarias
  #otimizacao entre anos diferentes: pode excluir turmas existentes se elas nao forem necessarias para alocar os alunos de continuidade

  #para cada escola_id, serie_id em df_turma, confere quantos alunos
  serie_id_list = np.unique(list(df_aluno['serie_id_otim']) + list(df_turma['serie_id']) )
  turmas_necessarias_total = 0

  for s in serie_id_list:
    escola_id_list = np.unique( list(df_aluno['escola_id'][  df_aluno['serie_id_otim'] ==s ] ) + list(df_turma['escola_id'][  df_turma['serie_id'] ==s ] ))
    for e in escola_id_list: 
    
      #qtd total de alunos nessa serie/escola
      qtd_alunos = len(df_aluno[ (df_aluno['serie_id_otim']==s) & (df_aluno['escola_id']==e)].index)

      #qtd turmas necessarias = ceil( qtd_alunos / max_alunos  )
      qtd_turmas_necessarias = math.ceil( qtd_alunos/param_dict['qtd_max_alunos'])
      turmas_necessarias_total += qtd_turmas_necessarias

      #qtd de turmas existentes nessa escola/serie
      #df_turma = df_turma[ df]
      turmas_existentes = df_turma[ (df_turma['serie_id']==s) & (df_turma['escola_id']==e)]
      qtd_turmas_existentes = len( turmas_existentes.index )
      #print("----- serie=" + str(s) + ", escola=" + str(e) + ": qtd_turmas_necessarias="+str(qtd_turmas_necessarias) + ", qtd_turmas_existentes=" + str(qtd_turmas_existentes)) #debug #apagar
      
      turmas_extras = qtd_turmas_existentes - qtd_turmas_necessarias
      if turmas_extras > 0:
        # exclui qtd_turmas existentes - qtd turmas necessarias 

        #if qtd_turmas_existentes ==1: #se so tem uma turma e nao e mais necessaria
        #se so tem uma turma e nao e mais necessaria, ou se precisa fechar todas as turmas
        if qtd_turmas_existentes ==1 or turmas_extras==qtd_turmas_existentes:
          turmas_existentes_drop = turmas_existentes[:].index
        else:
          turmas_existentes_drop = turmas_existentes[1:].index

        for textra in turmas_existentes_drop:
          tid = int(df_turma['id'][ textra] )
         # if tid!=9:
          print("Fecha turma t_id=" + str(tid)) #debug
          df_turma.drop(textra, inplace=True)

      #se as turmas existentes nao sao suficientes para alocar todos os alunos de formulario, ja ajusta o parametro  
      elif turmas_extras < 0: 
        if param_dict['possibilita_abertura_novas_turmas'] == 0:
          print("As turmas pre-existentes deixariam o modelo infactivel.")
          print("Ajuste: permite a abertura de novas turmas para alocar os alunos de continuidade")
          param_dict_ajuste['possibilita_abertura_novas_turmas']=1

  print("Precisa de no minimo "+ str(turmas_necessarias_total) + " turmas") #debug
    
  df_turma.reset_index(inplace=True)

  return df_turma,param_dict_ajuste,turmas_necessarias_total


"""## Confere infactibilidade e ajusta turmas existentes"""

#Calcula o orçamento minimo necessário e se sera necessário abrir novas turmas:
def fase0_factibilidade_ajusta(df_aluno, df_turma, param_dict):
  #Calcula o id maximo das turmas existentes, nao deixa salvar novas turmas com id menor do que esse na fase 2
  if len(df_turma.index) >0:
    turma_id_max_existente = max(df_turma['id'])
  else:
    turma_id_max_existente = 0
  print("turma_max_id="+str(turma_id_max_existente)) #debug #apagar

  param_dict_ajuste = param_dict.copy()
  df_aluno = junta_turmas(df_aluno, df_turma, param_dict)

  #confere quantas turmas precisa de cada serie/escola para os alunos
  # se o problema for infactibilidade devido a falta de orçamento para as turmas desses alunos, ja ajusta
  df_turma,param_dict_ajuste,numero_turmas_min = fecha_turmas_desnecessarias(param_dict, param_dict_ajuste, df_aluno, df_turma)
  
  #calcula o numero de turmas necessarias para alocar os alunos de continuidade
  limite_custo_atual = param_dict['limite_custo']
  
  qtd_alunos_continuidade = len(df_aluno.index)
  custo_turma_professores_t = param_dict['custo_professor']*(param_dict['qtd_professores_pedagogico'] + param_dict['qtd_professores_acd'])
  custo_turma_alunos_t = ( qtd_alunos_continuidade )* param_dict['custo_aluno']
  orcamento_min = (numero_turmas_min * custo_turma_professores_t + custo_turma_alunos_t) 
  print("Numero minimo de turmas: " + str(numero_turmas_min))
  print("Numero de alunos de continuidade: " + str(qtd_alunos_continuidade))
  if limite_custo_atual < orcamento_min:
    print("O limite de custo atual R$" + str(limite_custo_atual) + " e infactivel" )
    #print("O Orcamento minimo para alocar os alunos de continuidade e R$" + str(orcamento_min) )
    param_dict_ajuste['limite_custo'] = orcamento_min
    print("Ajuste: O limite_custo foi ajustado para R$", param_dict_ajuste['limite_custo'])
   
  return param_dict_ajuste, df_aluno, df_turma, turma_id_max_existente, numero_turmas_min

def relatorio_param_ajuste(file_BD, param_dict_ajuste, param_dict):
  df_param_ajuste = pd.DataFrame(columns=['id', 'chave', 'valor'])

  id=1
  #orcamento foi ajustado para garantir a gac
  if param_dict_ajuste['limite_custo'] != param_dict['limite_custo']: 
    df_param_ajuste = relatorio_append(df_param_ajuste, id, 'limite_custo', param_dict_ajuste['limite_custo'])
    id = id+1
  
  if param_dict_ajuste['possibilita_abertura_novas_turmas'] != param_dict['possibilita_abertura_novas_turmas']:
    df_param_ajuste = relatorio_append(df_param_ajuste, id, 'possibilita_abertura_novas_turmas', param_dict_ajuste['possibilita_abertura_novas_turmas'])
    id = id+1
  
  salva_BD_relatorio(file_BD, 'sol_parametro_ajuste', df_param_ajuste[['id', 'chave', 'valor']])

"""# MAIN + modelo (fase1 e fase2)"""

def main(file_BD="Modelo de Dados - MatMov.db"):
  print("Banco de dados SQL: ", file_BD)
  table_names = {"aluno", "escola", "formulario_inscricao", "regiao", "serie", "status", "turma", "parametro" } 
  param_list = {"ano_planejamento", "otimiza_dentro_do_ano", "possibilita_abertura_novas_turmas", "limite_custo", "custo_aluno", "custo_professor", "qtd_max_alunos", "qtd_professores_pedagogico", "qtd_professores_acd" }

  #Leitura do BD: le tabelas e parametros em dicionarios
  #dfs_dict e um dicionario com dataframes, as chaves sao os nomes das tabelas em table_names
  #param_dict e um dicionario com os parametros, as chaves sao os nomes dos parametros em param_list
  dfs_dict, param_dict = leitura_BD(file_BD, table_names, param_list)

  if dfs_dict != None and param_dict != None:
    print("Otimiza dentro do ano:",param_dict['otimiza_dentro_do_ano']) #debug
    print("Possibilita abertura de novas turmas:",param_dict['possibilita_abertura_novas_turmas']) #debug

    #final: gera alerta de consistencia como tabelas no SQL se tiver alunos de formulario ou continuidade repetidos
    print("Gera alertas de consistencia")
    alertas_consistencia(file_BD, param_dict, dfs_dict)


    #Pre-processamento das tabelas
    dfs_dict['serie'], max_serie_ordem, max_serie_id = pre_processamento_serie(dfs_dict['serie'])
    dfs_dict['aluno'] = pre_processamento_alunos_continuidade(dfs_dict['aluno'], dfs_dict['turma'], dfs_dict['serie'], param_dict['otimiza_dentro_do_ano'], max_serie_ordem)
    dfs_dict['formulario_inscricao'] = pre_processamento_alunos_formulario(dfs_dict['formulario_inscricao'], dfs_dict['serie'], max_serie_ordem, param_dict['ano_planejamento'])
    dfs_dict['serie'] = dfs_dict['serie'][dfs_dict['serie']['ativa']==1]


    print("\n* Inicia fase 0")
    #Ajusta o parametro limite_custo se o modelo for infactivel
    #Se o modelo for infactivel, esses sao os ajustes minimos apenas para garantir que os alunos de continuidade sejam alocados corretamente
    #dessa forma, a fase 2 nao sera executada
    #Tenta juntar turmas existentes e exclui as turmas desnecessarias
    param_dict_ajuste,dfs_dict['aluno'], dfs_dict['turma'],turma_id_max_existente, numero_turmas_limitante = fase0_factibilidade_ajusta(dfs_dict['aluno'], dfs_dict['turma'], param_dict) #final

    #---------------- Resolve modelo

    #----------- Fase 1 - modelo de otimizacao
    # Aloca os alunos de continuidade e preenche as vagas remanescentes com alunos de formulario
    # permite abertura de novas turmas, apenas para alocar os de continuidade

    print("\n* Inicia fase 1")
    #A fase 1 considera os parametros ajustados para garantir a factibilidade do modelo #final 
    xc, xf, y, z, v_vagas_livres, v_turma_aberta, turmas_new_idx_list, status = fase1_modelo(dfs_dict, param_dict_ajuste, turma_id_max_existente, numero_turmas_limitante) #param_dict) #final

    #Modelo rodou com sucesso: #final: deve obrigatoriamente cair aqui
    if status > 0:
      print("Solver terminou com sucesso")
      # Salva os resultados ate o momento, retorna os dataframes.    
      df_sol_turma, df_sol_aluno, df_sol_formulario = fase1_salva_resultados(dfs_dict, param_dict, xc, xf, y, z, v_vagas_livres, v_turma_aberta, turmas_new_idx_list)   #TODO

      #----------- Fase 2 - novas turmas, procedimento iterativo
      df_formulario_restante, orcamento_restante,num_max_alunos = apos_fase1_atualiza_dfs_restante(dfs_dict, param_dict, xc, xf, v_vagas_livres, v_turma_aberta, turmas_new_idx_list) #ok?    
        
      continua=1
      #Final: so inicia a fase 2 se permitir a abertura de novas turmas
      if param_dict['possibilita_abertura_novas_turmas']==1: 
        print("\n* Inicia fase 2")
        print("Orcamento restante="+str(orcamento_restante))

        #Enquanto ainda tem orcamento e for possivel alocar pelo menos um aluno (considerando o custo dos professores)
        while orcamento_restante > 0 and num_max_alunos>=1 and continua==1:      
          #Escolhe a serie/escola de maior demanda, de acordo com a nova regra da ONG      
          serie_id_sel, escola_id_sel = fase2_calc_next_serie_abrir(dfs_dict,param_dict,df_formulario_restante, 0.25)       
          #Preenche com os primeiros num_max_alunos alunos. Como a lista esta rankeada por prioridade, vai sempre selecionar os que tem prioridade
          formulario_selecionados = df_formulario_restante[ (df_formulario_restante['serie_id_otim']==serie_id_sel) & (df_formulario_restante['escola_id']==escola_id_sel) ].head(num_max_alunos) 
          
          if len(df_formulario_restante.index) > 0:
            print("Ainda tem orcamento, abre serie_id="+ str(serie_id_sel) + ", na escola_id=" + str(escola_id_sel))
            df_sol_turma, df_sol_formulario = fase2_salva_resultados(dfs_dict, param_dict, df_sol_turma, df_sol_formulario, formulario_selecionados, serie_id_sel, escola_id_sel,turma_id_max_existente)        
            #Redefine df_formulario
            df_formulario_restante.drop(formulario_selecionados.index, inplace=True)
            #Calcula orcamento restante e quantos alunos cabem no orcamento (num_max_alunos)    
            orcamento_restante, num_max_alunos = fase2_novo_orcamento(param_dict, len(formulario_selecionados.index), orcamento_restante )       
          else:
            continua=0
      #else:
      #  print("Nao sao permitidas novas turmas")

      print("\nOrcamento restante final da ONG="+str(orcamento_restante))
      print("\nFim do modelo\n")       

      #Salva a solucao no banco de dados:    
      salva_BD(file_BD, df_sol_turma, df_sol_aluno, df_sol_formulario)

      #---------------- Relatorios
      #Gera relatorios no banco de dados
      df_relatorio_turma = gera_relatorio_turma(file_BD, param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario)
      #Relatorio dos parametros que foram ajustados, salva esses novos parametros em um relatorio
      relatorio_param_ajuste(file_BD, param_dict_ajuste, param_dict)
      #Relatorios extras sugeridos pela equipe Convex-Lab
      relatorios_extras(file_BD, param_dict, df_sol_turma, df_sol_aluno, df_sol_formulario, dfs_dict, df_formulario_restante)

      #return df_sol_turma, df_sol_aluno, df_sol_formulario, df_relatorio_turma, dfs_dict, param_dict, file_BD #test #debug

    else: #Com as correcoes realizadas, nao e para acontecer do modelo ser infactivel
      print("ERRO: Solver terminou com modelo infactivel")
    
      #return None, None, None, None, dfs_dict, param_dict, file_BD #test #debug
  else: #arquivo SQL nao encontrado
    print("Arquivo SQL nao encontrado")
    #return None, None, None, None, None, None, file_BD
  web_report(file_BD)
"""# Testes"""

# print("\n-------------\nTeste - arquivo SQL original\n-------------\n")
# main("cenarios_inicial/Modelo de Dados - MatMov.db") #ou main()

# print("\n-------------\nTeste - arquivo SQL original - sem novas turmas\n-------------\n")
# main("cenarios_final/Modelo de Dados - MatMov _sem_novas_turmas.db") #problema infactilbidade

print ("\n-------------\nTeste final - cenario 2\n-------------\n")
main("cenarios_final/cenario_2.db") #problema com alunos reprovados

# print ("\n-------------\nTeste final - cenario 2 - entre\n-------------\n")
# main("cenarios_final/cenario_2_entre.db") #problema com alunos reprovados

# print ("\n-------------\nTeste final - cenario 2 - entre - sem novas turmas\n-------------\n")
# main("cenarios_final/cenario_2_entre_sem_novas_turmas.db") #problema com alunos reprovados

# print ("\n-------------\nTeste final - cenario 5 - infactivel\n-------------\n")
# main("cenarios_final/cenario_5.db") ##infactivel

# print("\n-------------\nTeste 1\n-------------\n")
# main("cenarios_inicial/Modelo de Dados - MatMov - v1.db")

# print("\n-------------\nTeste 2\n-------------\n")
# main("cenarios_inicial/Modelo de Dados - MatMov - v2.db")

# print("\n-------------\nTeste 3\n-------------\n")
# main("cenarios_inicial/Modelo de Dados - MatMov - v3.db")

# print("\n-------------\nTeste 4\n-------------\n")
# main("cenarios_inicial/Modelo de Dados - MatMov - v4.db")

# print("\n-------------\nTeste 5\n-------------\n")
# main("cenarios_inicial/Modelo de Dados - MatMov - v5.db")

# print("\n-------------\nTeste 6\n-------------\n")
# main("cenarios_inicial/Modelo de Dados - MatMov - v6.db")

# print("\n-------------\nTeste 6_nenhuma_turma\n-------------\n")
# main("cenarios_final/Modelo de Dados - MatMov - v6_nenhuma_turma.db")

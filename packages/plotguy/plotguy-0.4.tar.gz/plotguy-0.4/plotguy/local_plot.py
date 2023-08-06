import pandas as pd
import numpy as np
import math
import os
import datetime

from dash import Dash, dcc, html, Input, Output, State, ALL     ## pip install dash
import dash_bootstrap_components as dbc                         ## pip install dash_bootstrap_components
import plotly.express as px
import plotly.graph_objs as go

class main:

    chart_bg = '#1f2c56'
    div_bg = 'rgba(0, 0, 0, 0)'
    date_df = pd.DataFrame()    ## Date
    result_df = pd.DataFrame()  ##
    graph_df = pd.DataFrame()   ## Perfomrance Matrix

    sort_method_current = ''
    filter_list = []
    add_button_count = 0
    chart1_button_clicks = 0
    chart2_button_clicks = 0
    line_selected = -1
    button_list = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    chart_type = 1

    init = True

    sort_method_list = ['Top 20 Net Profit to MDD', 'Top 20 Net Profit', ]

    filter_options = {
        'num_of_trade':'Trade Count',
        'annualized_sr': 'Sharp Ratio',
        'mdd_pct':'MDD Percentage',
        'cov':'COV',
        'win_rate':'Win Rate',
        'return_to_bah': 'Return to BnH Ratio',
        'exclude': 'Exclude',
    }

    ## Sort df according to sort method
    def sort_method_df(self, sort_method, result_df):
        if sort_method == 'Top 20 Net Profit':
            df_sorted = result_df.sort_values(by='net_profit', ascending=False).head(20).copy()
        elif sort_method == 'Top 20 Net Profit to MDD':
            df_sorted = result_df.sort_values(by='net_profit_to_mdd', ascending=False).head(20).copy()
        else:
            df_sorted = result_df.copy()

        df_sorted = df_sorted.reset_index(drop=True)

        line_colour = []
        for c in range(len(df_sorted)):
            profile = c % 6
            degree = (c // 6) / math.ceil(len(df_sorted) / 6)
            line_colour.append(self.assign_colour(profile, degree))
        df_sorted['line_colour'] = line_colour

        return df_sorted

    ## Assign Colour after sorting
    def assign_colour(self,profile, degree):
        if   profile == 0: rgb = (0, int(252 - 252 * degree), 252)
        elif profile == 1: rgb = (int(252 - 252 * degree), 252, 0)
        elif profile == 2: rgb = (252, 0, int(252 - 252 * degree))
        elif profile == 3: rgb = (0, 252, int(252 * degree))
        elif profile == 4: rgb = (252, int(252 * degree), 0)
        elif profile == 5: rgb = (int(252 * degree), 0, 252)
        return 'rgb' + str(rgb)


    ## Update checkbox list
    def update_check_list(self,para_dict,uni_list):
        checklist_div = []
        i = 1
        for para_name in para_dict:
            if not para_name == 'code':
                _options = uni_list[para_name]
                if _options == [False, True]:
                    _checklist = dcc.Checklist([str(tf) for tf in _options], [str(tf) for tf in _options], inline=True,
                                               id={'type': 'para-checklist', 'index': i},
                                               labelStyle={'font-size': '11px'},
                                               inputStyle={'margin-left': '10px', 'margin-right': '3px'})
                else:
                    _checklist = dcc.Checklist(_options, _options, inline=True,
                                               id={'type': 'para-checklist', 'index': i},
                                               labelStyle={'font-size': '11px'},
                                               inputStyle={'margin-left': '10px', 'margin-right': '3px'})
                row = html.Div(
                    dbc.Row([
                        html.Div(para_name),
                        html.Div(style={'height': '5px'}),
                        html.Div(_checklist),
                        html.Div(style={'height': '5px'}),
                    ]), style={'padding': '0px 20px', 'font-size': '11px'})

                checklist_div.append(row)
                i = i + 1

        return checklist_div



    def performance_matrix(self,start_date,end_date,df,para_dict):
        per_col1 = []
        per_col2 = []
        per_col_1_1 = []
        per_col_1_2 = []
        per_col_2_1 = []
        per_col_2_2 = []

        keys = ['num_of_trade','net_profit','net_profit_to_mdd',
                'mdd_dollar','mdd_pct','return_on_capital','annualized_return','annualized_std','annualized_sr',
                'return_to_bah','win_rate','cov',
                'bah_mdd_dollar','bah_mdd_pct','bah_return','bah_annualized_return','bah_annualized_std','bah_annualized_sr']

        try:
            df['net_profit'] = "{:,}".format(int(round(df['net_profit'],0)))
            df['net_profit_to_mdd'] = round(df['net_profit_to_mdd'], 2)

            df['mdd_dollar'] = "{:,}".format(int(round(df['mdd_dollar'], 0)))
            df['mdd_pct'] = "{:.0%}".format(df['mdd_pct']/100)
            df['return_on_capital'] = "{:.0%}".format(df['return_on_capital']/100)
            df['annualized_return'] = "{:.0%}".format(df['annualized_return']/100)

            df['cov'] = round(df['cov'], 2)
            df['win_rate'] = "{:.0%}".format(df['win_rate']/100)
            df['return_to_bah'] = round(df['return_to_bah'], 2)

            df['bah_mdd_dollar'] = "{:,}".format(int(round(df['bah_mdd_dollar'], 0)))
            df['bah_mdd_pct'] = "{:.0%}".format(df['bah_mdd_pct']/100)
            df['bah_return'] = "{:.0%}".format(df['bah_return']/100)
            df['bah_annualized_return'] = "{:.0%}".format(df['bah_annualized_return']/100)
        except Exception as e:
            # print(e)
            pass

        per_col_1_1.append(html.Div('Number of Trade'))
        per_col_1_1.append(html.Div('Net Profit'))
        per_col_1_1.append(html.Div('Net Profit to MDD'))
        per_col_1_1.append(html.Div(html.Img()))
        per_col_1_1.append(html.Div('MDD Dollar'))
        per_col_1_1.append(html.Div('MDD Percentage'))
        per_col_1_1.append(html.Div('Return on Capital'))
        per_col_1_1.append(html.Div('Annualized Return'))
        per_col_1_1.append(html.Div('Annualized Std'))
        per_col_1_1.append(html.Div('Annualized Sharp Ratio'))

        for i in range(3):
            per_col_1_2.append(html.Div(df[keys[i]],style={'text-align': 'center'}))
        per_col_1_2.append(html.Div(html.Img()))
        for i in range(3,9):
            per_col_1_2.append(html.Div(df[keys[i]],style={'text-align': 'center'}))

        per_col_2_1.append(html.Div('Return to BaH Ratio'))
        per_col_2_1.append(html.Div('Win Rate'))
        per_col_2_1.append(html.Div('COV'))
        per_col_2_1.append(html.Div(html.Img()))
        per_col_2_1.append(html.Div('BaH MDD Dollar'))
        per_col_2_1.append(html.Div('BaH MDD Percentage'))
        per_col_2_1.append(html.Div('BaH Return'))
        per_col_2_1.append(html.Div('BaH Annualized Return'))
        per_col_2_1.append(html.Div('BaH Annualized Std'))
        per_col_2_1.append(html.Div('BaH Annualized Sharp Ratio'))

        for i in range(9, 12):
            per_col_2_2.append(html.Div( str(df[keys[i]]) ,style={'text-align': 'center'}))
        per_col_2_2.append(html.Div(html.Img()))
        for i in range(12, 18):
            per_col_2_2.append(html.Div( str(df[keys[i]]) ,style={'text-align': 'center'}))

        per_col1.append(dbc.Row([dbc.Col(html.Div(per_col_1_1), width=9),
                                 dbc.Col(per_col_1_2, style={'padding':'0'}, width=3)]))
        per_col2.append(dbc.Row([dbc.Col(html.Div(per_col_2_1), width=9),
                                 dbc.Col(per_col_2_2, style={'padding':'0'}, width=3)]))


        start_date_year = datetime.datetime.strptime(start_date, '%Y-%m-%d').year
        end_date_year = datetime.datetime.strptime(end_date, '%Y-%m-%d').year
        year_list = list(range(start_date_year, end_date_year))

        year_col1 = []
        year_col2 = []

        if len(year_list) < 11:
            for i in range(len(year_list)):
                year_col1.append(dbc.Row([dbc.Col(year_list[i], style={'padding-left': '20px'}, width=3),
                                          dbc.Col(df[str(year_list[i])], style={'text-align': 'center'}
                                                  , width=3)], style={'font-size': '11px'}))

        # print(df)

        title = []
        for key in para_dict:
            title_div = []
            title_div.append(html.Div(key,style={'margin-right':'5px','display': 'inline'}))
            title_div.append(html.Div(':', style={'margin-right': '5px', 'display': 'inline'}))
            title_div.append(html.Div(str(df[key]) + ' ', style={'margin-right': '10px', 'display': 'inline'}))
            title.append(html.Span(title_div))

        matrix = html.Div([
            html.Div(style={'height': '5px', }),
            dbc.Row(html.Div(title),style={'padding-left': '10px','font-size': '14px'}),
            html.Div(style={'height': '5px', }),
            dbc.Row([
                dbc.Col(html.Div(children=per_col1), style={'font-size': '11px'}, width=4),

                dbc.Col(html.Div(children=per_col2), style={'font-size': '11px'}, width=4),

                dbc.Col([html.Div('Year Signal Count', style={'font-size': '12px'}),
                         html.Div(children=year_col1)], style={'padding-left':'30px'}, width=4),

            ], style={'padding': '10px'})
        ])

        return matrix


    def filter_row(self,elements):
        filter_button = []
        for i in range(len(elements)):
            element=elements[i]
            filter_full = []
            filter_full.append(html.Div(self.filter_options[element[0]],style={'margin-right':'15px','display': 'inline'}))
            filter_full.append( html.Div(element[1], style={'margin-right': '15px', 'display': 'inline'}))
            filter_full.append(html.Div(element[2], style={'margin-right': '15px', 'display': 'inline'}))
            filter_button.append(dbc.Row([
                dbc.Col(html.Div(filter_full,
                                 style={'font-size': '12px', 'padding': '0px', 'margin': '0px'}), width=10),
                dbc.Col(html.Div(children=html.Div('✗', style={'padding': '0px', 'margin': '0px'}),
                                 id='button_' + str(i),n_clicks=i,
                                 style={'font-size': '12px','backgroundColor': 'rgba(0, 0, 0, 0)',
                                        'border': '0px black solid','padding': '0px', 'padding-bottom': '10px',
                                        'margin': '0px', 'width': '5px','cursor': 'pointer'}),width=2)
            ]))
        for i in range(len(elements),10):
            filter_button.append(html.Div( id='button_' + str(i),n_clicks=i))

        return filter_button


    def prep_df_chart(self, df):
        df_chart = pd.DataFrame()
        df_chart['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df_chart['close'] = df['close']
        df_chart['bah'] = df['close'] * (100000 / df_chart.iloc[0].close)
        df_chart['equity_value'] = df['equity_value']
        df_chart['signal'] = df['signal']
        df_chart['volume'] = df['volume']
        df_chart['sma'] = df['sma']

        _open = []
        _stop_loss = []
        _close_logic = []
        _profit_taking = []

        for i in range(len(list(df['signal']))):
            element = list(df['signal'])[i]
            if element == 'open':
                _open.append(df_chart.iloc[i].bah)
                _stop_loss.append(None)
                _close_logic.append(None)
                _profit_taking.append(None)
            elif element == 'stop_loss':
                _open.append(None)
                _stop_loss.append(df_chart.iloc[i].bah)
                _close_logic.append(None)
                _profit_taking.append(None)
            elif element == 'close_logic':
                _open.append(None)
                _stop_loss.append(None)
                _close_logic.append(df_chart.iloc[i].bah)
                _profit_taking.append(None)
            elif element == 'profit_taking':
                _open.append(None)
                _stop_loss.append(None)
                _close_logic.append(None)
                _profit_taking.append(df_chart.iloc[i].bah)
            else:
                _open.append(None)
                _stop_loss.append(None)
                _close_logic.append(None)
                _profit_taking.append(None)

        df_chart['open'] = _open
        df_chart['stop_loss'] = _stop_loss
        df_chart['close_logic'] = _close_logic
        df_chart['profit_taking'] = _profit_taking

        return df_chart



    def gen_chart1(self, graph_df,para_key_list,gen_name,filename, start_date, end_date, para_dict):
        fig_line = px.line()
        fig_line.update_xaxes(showline=True, zeroline=False, linecolor='white', gridcolor='rgba(0, 0, 0, 0)')
        fig_line.update_yaxes(showline=True, zeroline=False, linecolor='white', gridcolor='rgba(0, 0, 0, 0)')
        fig_line.update_layout(plot_bgcolor=self.chart_bg, paper_bgcolor=self.chart_bg,height=350,
                               margin=dict(l=85, r=25, t=10, b=0),
                               showlegend=False,
                               font={"color": "white", 'size': 10.5}, yaxis={'title': 'Equity'},
                               xaxis={'title': ''}
                               )

        for i in graph_df.index:
            para_values = []
            hovertemplate = "%{x}<br>"
            for key in para_key_list:
                para_values.append(graph_df.iloc[i][key])
                hovertemplate = hovertemplate + \
                                key + " : " + str(graph_df.iloc[i][key]) + "<br>"
            hovertemplate = hovertemplate + "<br>"
            hovertemplate = hovertemplate + "Return to BaH Ratio : " + str(
                round(graph_df.iloc[i]['return_to_bah'], 2)) + "<br>"
            hovertemplate = hovertemplate + "Net Profit to MDD: " + str(
                round(graph_df.iloc[i]['net_profit_to_mdd'], 2)) + "<br>"
            hovertemplate = hovertemplate + "Sharp Ratio : " + str(graph_df.iloc[i]['annualized_sr']) + "<br>"
            hovertemplate = hovertemplate + "MDD Percentage : " + "{:.0%}".format(
                graph_df.iloc[i]['mdd_pct'] / 100) + "<br>"
            hovertemplate = hovertemplate + "Trade Count : " + str(graph_df.iloc[i]['num_of_trade']) + "<br>"
            hovertemplate = hovertemplate + "COV : " + str(round(graph_df.iloc[i]['cov'], 2)) + "<br>"
            hovertemplate = hovertemplate + "Win Rate : " + "{:.0%}".format(graph_df.iloc[i]['win_rate'] / 100) + "<br>"
            hovertemplate = hovertemplate + "<br>"

            save_name = gen_name(filename, start_date, end_date, para_dict, para_values)
            save_path = os.path.join('output', save_name)
            line_colour = graph_df.loc[i].line_colour

            df = pd.read_csv(save_path)
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

            hovertemplate = hovertemplate + "Equity : %{y:,.0f}"

            fig_line.add_trace(go.Scatter(mode='lines', hovertemplate=hovertemplate,
                                          x=df['date'], y=df['equity_value'],
                                          line=dict(color=line_colour, width=1.5), name=''), )

        return fig_line




    def gen_chart2(self,df_chart,line_colour):
        fig_line = px.line(df_chart, x='date', y="equity_value")
        fig_line.update_traces(line_color='rgba(0, 0, 0, 0)')
        fig_line.update_xaxes(showline=True, zeroline=False, linecolor='white', gridcolor='rgba(0, 0, 0, 0)')
        fig_line.update_yaxes(showline=True, zeroline=False, linecolor='white', gridcolor='rgba(0, 0, 0, 0)')
        fig_line.add_trace(go.Scatter(mode='lines', hoverinfo='skip',
                                      x=df_chart['date'], y=df_chart['equity_value'],
                                      line=dict(color=line_colour, width=1), name='Strategy Equity'), )
        fig_line.add_trace(go.Scatter(mode='lines', hoverinfo='skip',
                                      x=df_chart['date'], y=df_chart['bah'],
                                      line=dict(color='#00FFFF', width=1), name='BnH Equity'), )
        fig_line.update_layout(plot_bgcolor=self.chart_bg, paper_bgcolor=self.chart_bg,height=220,
                               margin=dict(l=85, r=25, t=25, b=0),
                               font={"color": "white", 'size': 9}, yaxis={'title': 'Equity'},
                               xaxis={'title': ''}
                               )
        fig_line.add_trace(go.Scatter(mode='markers', hoverinfo='skip',
                                      x=df_chart['date'], y=df_chart['open'], visible='legendonly',
                                      marker=dict(color='rgba(0, 0, 0, 0)', size=8,
                                                  line=dict(color='yellow', width=1.5)), name='open'), )
        fig_line.add_trace(go.Scatter(mode='markers', hoverinfo='skip',
                                      x=df_chart['date'], y=df_chart['close_logic'], visible='legendonly',
                                      marker=dict(color='rgba(0, 0, 0, 0)', size=8,
                                                  line=dict(color='green', width=1.5)), name='close_logic'), )
        fig_line.add_trace(go.Scatter(mode='markers', hoverinfo='skip',
                                      x=df_chart['date'], y=df_chart['profit_taking'], visible='legendonly',
                                      marker=dict(color='rgba(0, 0, 0, 0)', size=8,
                                                  line=dict(color='red', width=1.5)), name='profit_taking'), )
        fig_line.add_trace(go.Scatter(mode='markers', hoverinfo='skip',
                                      x=df_chart['date'], y=df_chart['stop_loss'], visible='legendonly',
                                      marker=dict(color='rgba(0, 0, 0, 0)', size=8,
                                                  line=dict(color='blue', width=1.5)), name='stop_loss'), )
        return fig_line


    def sub_chart(self,df_chart, element, line_type, line_color):
        if line_type == 'bar':
            fig = go.Figure(
                data=[
                    go.Bar(hoverinfo='skip', x=df_chart['date'], y=df_chart[element], showlegend=True,
                           marker_color=line_color, marker_line_color=line_color, name=element),
                ])
        else:
            fig = go.Figure(data=[
                go.Scatter(mode='lines', hoverinfo='skip', x=df_chart['date'], y=df_chart[element], showlegend=True,
                           line=dict(color=line_color, width=1.5), name=element), ] )
        fig.update_layout(plot_bgcolor='#1f2c56', paper_bgcolor='#1f2c56', height=60, width=700,
                          margin=dict(l=85, r=50, t=5, b=10),
                          font={"color": "white",'size': 9}, yaxis={'fixedrange': True}, xaxis={'fixedrange': True},
                          bargap=0, )
        fig.update_xaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#1f2c56', )
        fig.update_yaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#626567', mirror=True)

        return fig


    def gen_his(self, df, period):
        chart_bg = self.chart_bg
        col_pct = 'pct_change_' + str(period)
        col_rise = 'max_rise_' + str(period)
        col_fall = 'max_fall_' + str(period)
        df_his = df.copy()
        df_his[col_pct] = df_his['close'].pct_change(period)
        df_his[col_pct] = df_his[col_pct].shift(-1 * period)
        df_his[col_pct] = df_his[col_pct] * 100
        df_his[col_pct] = df_his[col_pct].map(lambda x: round(x, 2))
        df_his = df_his[df_his['signal'] == 'open']

        df_his[col_rise] = (df_his['high'].rolling(period).max().shift(-1 * (period)) / df_his['close']) - 1
        # df[col_fall] = abs((df['low'].rolling(period).max().shift(-1 * (period))/df['close']) - 1)
        df_his[col_fall] = (df_his['low'].rolling(period).min().shift(-1 * (period)) / df_his['close']) - 1

        df_his[col_rise] = df_his[col_rise] * 100
        df_his[col_fall] = df_his[col_fall] * 100

        df_his[col_rise] = df_his[col_rise].map(lambda x: round(x, 2))
        df_his[col_fall] = df_his[col_fall].map(lambda x: round(x, 2))

        df_his = df_his[['date'] + [col_pct, col_rise, col_fall]]

        margin = dict(l=5, r=5, t=5, b=5)
        h = 85
        w = 120
        f = {"color": "white", 'size': 8}

        fig_pct = go.Figure()
        fig_pct.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg, height=h, width=w, margin=margin,
                              font=f, bargap=0.1)
        fig_pct.update_xaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#1f2c56', )
        fig_pct.update_yaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#626567', )
        fig_pct.add_trace(go.Histogram(x=df_his[col_pct], marker_color='Cyan'))

        fig_rise = go.Figure()
        fig_rise.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg, height=h, width=w, margin=margin,
                               font=f, bargap=0.1)
        fig_rise.update_xaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#1f2c56', )
        fig_rise.update_yaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#626567', )
        fig_rise.add_trace(go.Histogram(x=df_his[col_rise], marker_color='Yellow'))

        fig_fall = go.Figure()
        fig_fall.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg, height=h, width=w, margin=margin,
                               font=f, bargap=0.1)
        fig_fall.update_xaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#1f2c56', )
        fig_fall.update_yaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#626567', )
        fig_fall.add_trace(go.Histogram(x=df_his[col_fall], marker_color='Fuchsia'))

        return fig_pct, fig_rise, fig_fall



    def plot(self, filename, start_date, end_date, para_dict, result_df, gen_name):

        chart_bg = self.chart_bg
        div_bg = self.div_bg
        self.result_df = result_df
        self.date_df = pd.date_range(start_date,end_date, freq='B').to_frame(index=False,name='date')['date']

        uni_list = {}  ## uniqpe key list
        for key in para_dict:
            if not key == 'code':
                uni_para = list(dict.fromkeys(result_df[key].tolist()))
                try:uni_para.sort()
                except:pass
                uni_list[key] = uni_para

        checklist_div = self.update_check_list(para_dict, uni_list)

        fig_line = px.line()
        fig_line.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg, margin=dict(l=85, r=25, t=30, b=0),
                               height=450, font={"color": chart_bg})
        fig_line.update_xaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor=chart_bg)
        fig_line.update_yaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor=chart_bg)



        col_df = result_df.columns.values.tolist()
        col_data = []
        for c in col_df: col_data.append('---')
        df_col = pd.DataFrame([col_data], columns=col_df)
        matrix = self.performance_matrix(start_date,end_date,df_col.iloc[0].copy(),para_dict)

        filter_div = self.filter_row(self.filter_list)


        app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO], suppress_callback_exceptions=True)

        sort_method_dropdown  = html.Div(
            dbc.Select(id='sort_method',
                       placeholder="Select Sorting Method",
                       options=[{'label': 'Top 20 Net Profit', 'value': 'Top 20 Net Profit'},
                                {'label': 'Top 20 Net Profit to MDD', 'value': 'Top 20 Net Profit to MDD'},],
                       style={'border-radius': '5px','font-size': '12px',}),
            style={'padding-left': '12.5px', 'width': '230px'})


        filter_dropdown = html.Div(id='filter_dropdown',
                                   children=dbc.Select(id='filter_name',
                                                       placeholder="Select Filter",
                                                       options=[
                                                           {'label': 'Exclude Stock', 'value': 'exclude'},
                                                           {'label': 'Return to BaH Ratio >','value': 'return_to_bah>'},
                                                           {'label': 'Return to BaH Ratio <','value': 'return_to_bah<'},
                                                           {'label': 'Sharp Ratio >', 'value': 'annualized_sr>'},
                                                           {'label': 'Sharp Ratio <', 'value': 'annualized_sr<'},
                                                           {'label': 'MDD Percentage >', 'value': 'mdd_pct>'},
                                                           {'label': 'MDD Percentage <', 'value': 'mdd_pct<'},
                                                           {'label': 'Trade Count >', 'value': 'num_of_trade>'},
                                                           {'label': 'Trade Count <', 'value': 'num_of_trade<'},
                                                           {'label': 'COV >', 'value': 'cov>'},
                                                           {'label': 'COV <', 'value': 'cov<'},
                                                           {'label': 'Win Rate >', 'value': 'win_rate>'},
                                                           {'label': 'Win Rate <', 'value': 'win_rate<'},
                                                       ],

                                                       style={'border-radius': '5px', 'font-size': '12px'}),
                                   style={'padding-left': '15px', 'width': '170px'})

        filter_dropdown_disabled = html.Div(id='filter_dropdown',
                                   children=dbc.Select(id='filter_name',disabled=True,
                                                       placeholder="Select Filter",
                                                       style={'border-radius': '5px', 'font-size': '12px',
                                                              'backgroundColor':'Gray'}),
                                   style={'padding-left': '15px', 'width': '170px'})


        filter_input = dbc.Input(id='filter_input',value=None,size="md",type='text'
                                 ,style={'width': '50px','margin-right':'5px','border-radius': '3px',
                                         'padding':'6px 5px','font-size': '12px',})


        filter_input_disabled = dbc.Input(id='filter_input',value=None,size="md",disabled=True
                                 ,style={'width': '50px','margin-right':'5px','border-radius': '3px',
                                         'padding':'6px 5px','font-size': '12px','backgroundColor':'Gray'})

        add_button_style = {'margin-left':'50px','width': '140px','backgroundColor':'blue',
                                        'border-radius': '5px','text-align': 'center','cursor': 'pointer'}

        add_button_style_disabled = {'margin-left': '50px', 'width': '140px', 'color':'Silver', 'backgroundColor': 'Gray',
                            'border-radius': '5px', 'text-align': 'center',}


        ## Layout
        app.layout = html.Div([

            html.Div(style={'height': '10px', }),

            html.Div(
                dbc.Row([
                    ## Left Column
                    dbc.Col(html.Div([
                        html.Div(style={'height': '10px', }),
                        sort_method_dropdown,
                        html.Div(style={'height': '10px', }),
                        html.Div(id='checklist-container',children=checklist_div),
                        html.Div('---------------------------------------',style={'margin-left': '15px'}),
                        html.Div('Filters:', style={'margin-left': '15px'}),
                        html.Div(style={'height': '10px', }),
                        html.Div(id='filter', children=filter_div,style={'padding': '0px 20px', }),


                        dbc.Row([
                            dbc.Col(id='filter_dropdown_div',children=filter_dropdown,width=8),
                            dbc.Col(id='filter_input_div',children=filter_input,width=3),
                        ]),

                        html.Div(style={'height': '10px', }),

                        html.Div(id='add_button',children='Add Filter',
                                 style=add_button_style),

                    ],style={'padding':'0px','border-radius':'5px','height': '704px','background-color':'rgba(0, 0, 0, 0)'})
                        , style={'padding':'0',}, width=3),


                    ## Right Column
                    dbc.Col(html.Div([
                        html.Div(id='matrix',children=matrix
                                 ,style={'padding': '5px', 'border-radius': '5px', 'background-color': chart_bg}),

                        html.Div(style={'height': '5px', }),

                        html.Div([  html.Div(html.Img(),style={'height':'5px'}),
                                    dbc.Row([
                                        dbc.Col(html.Div(id='chart1_button',children=''
                                                         ,style={'text-align':'left','cursor':'pointer','font-size':'12px'}), width=4),
                                        dbc.Col(html.Div(html.Img()), width=4),
                                        dbc.Col(html.Div(id='chart2_button',children=''), width=4)
                                    ],style={'margin':'0px 5px'}),
                                    html.Div(id='chart_area',children=dcc.Graph(id='line_chart',figure=fig_line)),
                                    html.Div(id='sub_chart1_area', \
                                             children=dcc.Graph(id='sub_chart1', figure=fig_line, \
                                                                config={'displayModeBar': False}),
                                             style={'display': 'none'}),
                                    html.Div(id='sub_chart2_area',\
                                             children=dcc.Graph(id='sub_chart2', figure=fig_line, \
                                                                config={'displayModeBar': False}),
                                             style={'display': 'none'}),
                                 ],style={'padding':'5px','border-radius':'5px','background-color':chart_bg}),

                        html.Div(style={'height': '5px', }),

                        html.Div(id='hist_area', children=html.Div()
                                 , style={'padding': '5px', 'border-radius': '5px', 'background-color': chart_bg}),

                    ]), style={'padding':'0','padding-left':'5px'}, width=9),
                ])
            ),


        ], style={'width':'950px','margin':'auto','padding':'0px','color':'white','background-color':div_bg})



        @app.callback(
            Output('line_chart', 'figure'),
            Output('filter', 'children'),
            Output('filter_dropdown_div', 'children'),
            Output('filter_input_div', 'children'),
            Output('add_button', 'style'),
            Output('filter_input', 'value'),
            Output('chart1_button', 'children'),
            Output('chart2_button', 'children'),
            Output('sub_chart1_area', 'style'),
            Output('sub_chart1', 'figure'),
            Output('sub_chart2_area', 'style'),
            Output('sub_chart2', 'figure'),
            Output('hist_area', 'children'),
            Input('sort_method', 'value'),
            Input({'type': 'para-checklist', 'index': ALL}, 'value'),
            State('filter_dropdown_div', 'children'),
            State('filter_input_div', 'children'),
            State('line_chart', 'figure'),
            State('filter', 'children'),
            Input('add_button', 'n_clicks'),
            Input('chart1_button', 'n_clicks'),
            Input('chart2_button', 'n_clicks'),
            State('add_button', 'style'),
            State('filter_name', 'value'),
            State('filter_input', 'value'),
            State('sub_chart1_area', 'style'),
            State('sub_chart1', 'figure'),
            State('sub_chart2_area', 'style'),
            State('sub_chart2', 'figure'),
            State('hist_area', 'children'),
            [Input('button_' + str(i), 'n_clicks') for i in range(10)],
        )
        def display_output(sort_method,para_checklist,filter_dropdown_div,filter_input_div,fig_line,\
                           filter_div,add_button_clicks,chart1_button_clicks,chart2_button_clicks,\
                           _add_button_style,filter_name,filter_input_value,sub_chart1_area,sub_chart1,\
                           sub_chart2_area,sub_chart2,hist_area,*vals):

            chart1_button_text = ''
            chart2_button_text = ''


            if chart1_button_clicks:
                if chart1_button_clicks > self.chart1_button_clicks:
                    self.chart1_button_clicks = chart1_button_clicks
                    self. chart_type = 1
                    sub_chart1_area = {'display': 'none'}
                    sub_chart2_area = {'display': 'none'}


            if chart2_button_clicks:
                if chart2_button_clicks > self.chart2_button_clicks:
                    self.chart2_button_clicks = chart2_button_clicks
                    print('Phase2 Button Pressed')
                    print(self.line_selected)
                    if self.chart_type == 2:
                        print('Already Chart 2')
                        chart1_button_text = '< Back'
                        return fig_line, filter_div, filter_dropdown_div, filter_input_div, _add_button_style, \
                               None, chart1_button_text, chart2_button_text, \
                               sub_chart1_area, sub_chart1, sub_chart2_area, sub_chart2, hist_area
                    else:
                        if self.line_selected > -1:
                            print(self.graph_df.iloc[self.line_selected].line_colour)
                            para_key_list = list(para_dict)
                            para_values = []
                            for key in para_key_list:
                                # print(key)
                                para_values.append(self.graph_df.iloc[self.line_selected][key])
                            #print(para_values)
                            save_name = gen_name(filename, start_date, end_date, para_dict, para_values)
                            save_path = os.path.join('output', save_name)
                            line_colour = self.graph_df.iloc[self.line_selected].line_colour
                            df = pd.read_csv(save_path)
                            df_chart = self.prep_df_chart(df)
                            fig_line = self.gen_chart2(df_chart,line_colour)

                            self.chart_type = 2
                            chart1_button_text = '< Back'

                            sub_chart1_area = {}
                            sub_chart2_area = {}
                            sub_chart1 = self.sub_chart(df_chart,'volume','bar','yellow')
                            sub_chart2 = self.sub_chart(df_chart, 'sma', 'line', '#FF01FE')

                            ### Histograms
                            period = [3,5,10,30,50]
                            pct_list = [dbc.Col(html.Div('pct_change',style={'margin-top':'30px','transform':'rotate(-90deg)'}),width=1)]
                            rise_list = [dbc.Col(width=1)]
                            fall_list = [dbc.Col(width=1)]

                            for p in period:
                                fig_pct, fig_rise, fig_fall = self.gen_his(df, p)
                                pct_list.append( dbc.Col(dcc.Graph(figure=fig_pct,config={'displayModeBar': False})
                                                         ,style={'padding':'0'},width=2))
                                rise_list.append(dbc.Col(dcc.Graph(figure=fig_rise,config={'displayModeBar': False})
                                                         ,style={'padding': '0'}, width=2))
                                fall_list.append(dbc.Col(dcc.Graph(figure=fig_fall,config={'displayModeBar': False})
                                                         ,style={'padding': '0'}, width=2))

                            pct_list = html.Div(dbc.Row(pct_list))
                            rise_list = html.Div(dbc.Row(rise_list))
                            fall_list = html.Div(dbc.Row(fall_list))


                            hist_area = [pct_list, rise_list, fall_list]






                            return fig_line, filter_div, filter_dropdown_div, filter_input_div, _add_button_style,\
                                   None, chart1_button_text, chart2_button_text, \
                                   sub_chart1_area, sub_chart1, sub_chart2_area, sub_chart2, hist_area


                        else:
                            print('No Line Selected')


            ## Initialize After Refresh
            if not self.init:
               if (not sort_method) and (not add_button_clicks):
                   self.sort_method_current = sort_method
                   self.filter_list = []
                   self.add_button_count = 0
                   self.chart2_button_clicks = 0
                   self.line_selected = -1
                   self.chart_type = 1
                   sub_chart1_area = {'display': 'none'}
                   sub_chart2_area = {'display': 'none'}
                   self.init = True
                   filter_dropdown_div = filter_dropdown
                   filter_input_div = filter_input
                   return fig_line, filter_div, filter_dropdown_div,filter_input_div,_add_button_style, \
                          None, chart1_button_text, chart2_button_text, \
                          sub_chart1_area, sub_chart1, sub_chart2_area, sub_chart2

            ## Add Button Pressed
            if add_button_clicks:
                if add_button_clicks > self.add_button_count: ## Add Button Pressed
                    self.add_button_count = add_button_clicks
                    if filter_name:
                        if filter_input_value: ## Paremeter
                            if filter_name == 'exclude':
                                self.filter_list.append(['exclude', ' ', filter_input_value])
                            else:
                                self.filter_list.append([filter_name[0:-1], filter_name[-1], filter_input_value])
                            filter_div = self.filter_row(self.filter_list)
                            if len(self.filter_list) > 11:
                                filter_dropdown_div = filter_dropdown_disabled
                                filter_input_div = filter_input_disabled
                                _add_button_style = add_button_style_disabled
                            else:
                                filter_dropdown_div = filter_dropdown
                                filter_input_div = filter_input
                            self.init = False

            else:
                self.add_button_count = 0  # Necessary for initialization

            ## Filrer Delete Button
            for i in range(len(vals)):
                if not vals[i] == self.button_list[i]:
                    self.filter_list.pop(i)
                    filter_div = self.filter_row(self.filter_list)
                    filter_dropdown_div = filter_dropdown
                    filter_input_div = filter_input
                    self.add_button_count =- 1  # Necessary for add button count
                    if len(self.filter_list) < 12:
                        filter_dropdown_div = filter_dropdown
                        filter_input_div = filter_input
                        _add_button_style = add_button_style
                    break

            ## With a valid Sort Method, generate Chart 1
            if sort_method:
                current_df = self.result_df.copy()

                ## Filter according to the filer list
                if len(self.filter_list) > 0:
                    for element in self.filter_list:
                        print(element)
                        if element[0] == 'exclude':
                            current_df = current_df.loc[current_df['code'] != str(element[2])]
                        elif element[1] == '<':
                            current_df = current_df.loc[current_df[element[0]] < float(element[2])]
                        else:
                            current_df = current_df.loc[current_df[element[0]] > float(element[2])]

                current_df = current_df.reset_index(drop=True)

                para_key_list = list(para_dict)
                if len(para_checklist) > 0:
                    and_list = []
                    for i in range(len(para_key_list)):
                        key = para_key_list[i]
                        if not key == 'code':
                            or_list = []
                            for element in para_checklist[i-1]: # -1 becaause code / para_dict index
                                if element == 'True':element = True
                                elif element == 'False':element = False
                                _list = current_df[key] == element
                                or_list.append(_list)
                            or_list = np.logical_or.reduce(or_list)
                            and_list.append(or_list)
                    and_list = np.logical_and.reduce(and_list)
                    df_checked = current_df.loc[pd.DataFrame(and_list, columns=['check'])['check']].reset_index(
                        drop=True).copy()
                else:
                    df_checked = current_df.copy()

                ## Sorting
                graph_df = self.sort_method_df(sort_method, df_checked)
                self.graph_df = graph_df

                ## Generation
                fig_line = self.gen_chart1(graph_df, para_key_list, gen_name, filename, start_date, end_date, para_dict)

                ## Disabkle Chart 2
                chart2_button_text = 'Strategy Analysis >'
                self.chart_type = 1
                sub_chart1_area = {'display': 'none'}
                sub_chart2_area = {'display': 'none'}




            return fig_line, filter_div, filter_dropdown_div,filter_input_div,_add_button_style, \
                   None, chart1_button_text, chart2_button_text, \
                   sub_chart1_area, sub_chart1, sub_chart2_area, sub_chart2, hist_area



        @app.callback(
            Output(component_id='matrix', component_property='children'),
            Output('chart2_button', 'style'),
            Input('line_chart', 'clickData'),
            State(component_id='matrix', component_property='children'),
        )
        def update_matrix(clickData,matrix):
            print(clickData)
            button_style = {'text-align': 'right','color':'grey','font-size':'12px'}
            if clickData:
                if self.chart_type == 1:
                    i = clickData['points'][0]['curveNumber'] - 1
                    matrix = self.performance_matrix(start_date, end_date, self.graph_df.iloc[i].copy(),para_dict)
                    self.line_selected = i
                    button_style = {'text-align': 'right','cursor': 'pointer','font-size':'12px'}
            return matrix, button_style




        return app
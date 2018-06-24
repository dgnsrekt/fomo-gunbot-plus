# SYSTEM IMPORTS
from time import sleep

# THIRD PARTY IMPORTS
import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Event
from plotly.offline import plot

# LOCAL IMPORTS
from .models.view import Status


class Chart:

    @classmethod
    def get_chart(cls):

        data = Status.fetch()

        top_div = html.Div([html.H1('FOMO DRIVEN DEVELOPMENT')])
        top_div2 = html.Div([html.H2('GUNBOT SUPER FILTER')])
        banner = html.Div([top_div, top_div2], className='banner')

        bottom_div = html.Div([
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(id='graph-update', interval=15*1000,)])

        app = dash.Dash(__name__)
        app.layout = html.Div([banner, bottom_div], className='container')

        app.css.append_css(
            {'external_url': 'https://fonts.googleapis.com/css?family=Source+Sans+Pro:200,300,400,600,700'})

        app.css.append_css(
            {'external_url': 'https://codepen.io/dgnsrekt/pen/wXXNWM.css'})

        app.css.append_css(
            {'external_url': 'https://codepen.io/dgnsrekt/pen/dKKKLP.css'})

        @app.callback(Output('live-graph', 'figure'),
                      events=[Event('graph-update', 'interval')])
        def update_graph():
            data = Status.fetch()

            b_trace = go.Scatter(
                name='balance-btc',
                x=list(data.index),
                y=list(data.balance),
                mode='lines',
                connectgaps=True
            )

            p_trace = go.Scatter(
                name='positions',
                x=list(data.index),
                y=list(data.positions),
                yaxis='y2',
                mode='markers'
            )
            layout = go.Layout(plot_bgcolor='#000000',
                               paper_bgcolor='#000000',
                               font=dict(family='Source Sans Pro'),
                               xaxis=dict(autorange=True,
                                          title='TIME'),
                               yaxis=dict(autorange=True,
                                          title='BTC BALANCE'),
                               yaxis2=dict(autorange=True,
                                           title='OPEN POSITIONS',
                                           overlaying='y',
                                           side='right',
                                           range=[0, 15])
                               )
            return {'data': [b_trace, p_trace], 'layout': layout}
        return app


if __name__ == '__main__':
    app = Chart.get_chart()
    app.run_server(debug=False)

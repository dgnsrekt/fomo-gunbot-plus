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
from .models.balance import Balance


class Chart:

    @classmethod
    def get_chart(cls):

        data = Balance.pull()

        app = dash.Dash(__name__)
        app.layout = html.Div([
            html.H1('FOMO DRIVEN DEVELOPMENT',
                    style={'textAlign': 'center'}),

            html.H1('GUNBOT SUPER FILTER',
                    style={'textAlign': 'center'}),

            dcc.Graph(id='live-graph', animate=True),

            dcc.Interval(id='graph-update',
                         interval=15*1000,
                         )
        ])

        @app.callback(Output('live-graph', 'figure'),
                      events=[Event('graph-update', 'interval')])
        def update_graph():
            data = Balance.pull()

            trace = go.Scatter(
                name='equity-curve',
                x=list(data.index),
                y=list(data.btc),
                mode='lines',
                connectgaps=True
            )
            layout = go.Layout(title='EQUITY CURVE',
                               xaxis=dict(autorange=True,
                                          title='TIME'),
                               yaxis=dict(autorange=True,
                                          title='BTC')
                               )
            return {'data': [trace], 'layout': layout}
        return app


if __name__ == '__main__':
    app = Chart.get_chart()
    app.run_server(debug=False)

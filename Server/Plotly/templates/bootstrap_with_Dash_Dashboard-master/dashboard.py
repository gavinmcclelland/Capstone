from dash import Dash
from layout import layout2 as dashboard

import plotly 
import random
import plotly.graph_objs as go 
from collections import deque
from dash.dependencies import Output,Input

app = Dash(__name__)
app.title = 'Dashboard'
app.layout = dashboard

X = deque(maxlen=20)
Y = deque(maxlen=20)
X.append(1)
Y.append(1)

@app.callback(Output('live-graph', 'figure'),
              [Input('update-interval', 'n_intervals')])

def update_graph_scatter(input_data):
    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout': go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}


if __name__ == '__main__':
    app.run_server(debug=True)

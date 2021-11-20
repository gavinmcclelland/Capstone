import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import pandas_datareader.data as web
import datetime

stock='TSLA'

app = dash.Dash()

start=datetime.datetime(2015,1,1)
end=datetime.datetime.now()


df = web.DataReader(stock,'yahoo',start,end)

test = str(df)
testsplit = test.splitlines()


app.layout = html.Div(children=[
    html.Div([
        # html.Plaintext(str(x)) for x in testsplit
        dcc.Graph(
        id='test-graph',
        figure = {
            'data': [
                {'x' : df.index, 'y':df.Close, 'type':'line', 'name':'input_data'},
            ],
            'layout': {
                'title': 'input_data'
            }
        })
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
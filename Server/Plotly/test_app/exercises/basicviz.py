import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[
    html.H2('Wi-Wait Test'),
    dcc.Graph(id='test',
                figure = {
                    'data': [
                        {'x' : [1,2,3,4,5], 'y':[5,6,7,2,1], 'type':'line', 'name':'object1'},
                        {'x' : [1,2,3,4,5], 'y':[8,4,6,2,9], 'type':'bar', 'name':'object2'},
                    ],
                    'layout': {
                        'title':'Bar Chart'
                    }
                })
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output

app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Input(id='input', value='Enter Something', type='text'),
    html.Div(id='output')
])

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='input', component_property='value')]
)

def update_value(input_data):
    try:
        return str(float(input_data)**2) # square input
    except:
        return "ERROR"

if __name__ == "__main__":
    app.run_server(debug=True)
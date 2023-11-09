import dash
from dash import dcc, html, Input, Output
import json

# Read the data from the JSON file
with open('result.json') as f:
    data = json.load(f)

# Extracting required data
identifiers = [profile['identifiant'] for profile in data['profiles']]
ips_scores = [profile['score_ips'] for profile in data['profiles']]
text_height = [0 for profile in data['profiles']]
astre_scores = [-profile['score_astre'] for profile in data['profiles']]  # Reversed the scores for astre
results = [profile['resultat_final'] for profile in data['profiles']]

# Calculate the number of IPS and Astres
num_etudiants = len(results)
num_ips = sum(1 for result in results if result == 'IPS')
num_astres = sum(1 for result in results if result == 'Astre')

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Option Astre ou IPS', style={'textAlign': 'center'}),
    html.Button('Mettre à jour le graphique', id='button'),
    dcc.Graph(id='graph'),
    html.Div(
        html.Table([
            html.Tr([html.Th('Nombre d\'étudiants'), html.Th('Nombre d\'IPS'), html.Th('Nombre d\'Astres')],
                    style={'border': '10px solid black', 'text-align': 'center'}),
            html.Tr([html.Td(num_etudiants), html.Td(num_ips), html.Td(num_astres)]),
        ], style={'margin': 'auto', 'text-align': 'center'})
    )
])

@app.callback(
    Output('graph', 'figure'),
    Input('button', 'n_clicks')
)
def update_graph(n_clicks):
    # Perform any necessary calculations here
    # For example, you can update the data based on new computations
    # Make sure to modify the 'figure' attribute accordingly

    # Example of returning the figure with updated data
    fig = {
        'data': [
            {'x': identifiers, 'y': ips_scores, 'type': 'bar', 'name': 'IPS'},
            {'x': identifiers, 'y': astre_scores, 'type': 'bar', 'name': 'Astre'},
            {'x': identifiers, 'y': text_height, 'type': 'text', 'text': results, 'mode': 'text',
             'textfont': {'color': 'black'}, 'name': 'Texte de résultat'}
        ],
        'layout': {
            'xaxis': {'title': 'Numéro étudiants'},
            'yaxis': {'title': 'Scores'},
            'barmode': 'relative',
            'plot_bgcolor': 'rgba(0,0,0,0)'
        }
    }
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

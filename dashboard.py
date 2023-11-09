import dash
from dash import dcc, html, Input, Output
import json
import engine

app = dash.Dash(__name__)

# Function to read data from the JSON file
def read_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

data = read_json_file('result.json')

allHypothese = engine.load_hypotheses('hypotheses.json')

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

app.layout = html.Div(children=[
    html.Div([
        element for i, hypothesis in enumerate(allHypothese) for element in [
            html.Label(f'Weight of Hypothesis {i+1}:'),
            dcc.Input(id=f'weight-{i}', type='number', value=hypothesis.poids),
            html.Br()
        ]
    ], style={'margin': 'auto', 'text-align': 'center'}),
    html.Button('Mettre à jour le graphique', id='button'),
    html.H1('Option Astre ou IPS', style={'textAlign': 'center'}),
    dcc.Graph(id='graph'),
    html.Div(
        html.Table([
            html.Tr([html.Th('Nombre d\'étudiants'), html.Th('Nombre d\'IPS'), html.Th('Nombre d\'Astres')],
                    style={'border': '10px solid black', 'text-align': 'center'}),
            html.Tr([html.Td(num_etudiants), html.Td(num_ips), html.Td(num_astres)]),
        ], style={'margin': 'auto', 'text-align': 'center'})
    ),
], style={'margin': 'auto', 'text-align': 'center'})

@app.callback(
    Output('graph', 'figure'),
    [Input('button', 'n_clicks')] + [Input(f'weight-{i}', 'value') for i in range(len(allHypothese))],
)
def update_graph(n_clicks, *weights):
    # Update the weights of the hypotheses
    for i, weight in enumerate(weights):
        allHypothese[i].poids = weight

    # Run the engine
    engine.process_data_and_write_to_json("data_cleaned.csv", "result.json",allHypothese)

    # Reload the data
    data = read_json_file('result.json')
    identifiers = [profile['identifiant'] for profile in data['profiles']]
    ips_scores = [profile['score_ips'] for profile in data['profiles']]
    text_height = [0 for profile in data['profiles']]
    astre_scores = [-profile['score_astre'] for profile in data['profiles']]
    results = [profile['resultat_final'] for profile in data['profiles']]

    num_etudiants = len(results)
    num_ips = sum(1 for result in results if result == 'IPS')
    num_astres = sum(1 for result in results if result == 'Astre')

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

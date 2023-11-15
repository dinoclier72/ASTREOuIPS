import dash
from dash import dcc, html, Input, Output
import json
import engine

app = dash.Dash(__name__,title='Astre ou IPS')

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
    html.H1('Astre ou IPS', style={'textAlign': 'center'}),
    html.P("Ce dashboard permet de visualiser les options que les étudiants vont choisir selon des hypothèses, vous pouvez modifier les poids de chaque hypothèse grâce aux slider dans la setion ci-dessous"),
    html.Div(className='hypothesis-container', children=[
html.Div(className='hypothesis', children=[
    html.Label("hypothèse "+str(i+1)+" "+hypothesis.option+":"+hypothesis.details+" "),
    dcc.Slider(
        id=f'weight-{i}',
        min=1,
        max=6,
        step=1,
        value=hypothesis.poids,
        marks={i: str(i) for i in range(1, 7)},
        className='rc-slider',
    )
]) for i, hypothesis in enumerate(allHypothese)
    ], style={'margin': 'auto', 'text-align': 'center'}),
    html.Br(),
    html.Button('Sauvergarder les poids', id='save-button'),
    dcc.Graph(id='graph'),
    html.Div(
    id='table-container',  # Add this line
    children=html.Table([
        html.Tr([html.Th('Nombre d\'étudiants'), html.Th('Nombre d\'IPS'), html.Th('Nombre d\'Astres')]),
        html.Tr([html.Td(num_etudiants), html.Td(num_ips), html.Td(num_astres)]),
    ])
    ),
], style={'margin': 'auto', 'text-align': 'center'})

@app.callback(
    [Output('graph', 'figure'),
     Output('table-container', 'children')],  # Add this line
    [Input(f'weight-{i}', 'value') for i in range(len(allHypothese))],
)
def update_graph(*weights):
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

    colors = ['#1F77B4' if result == 'IPS' else '#FF7F0E' for result in results]

    fig = {
        'data': [
            {'x': identifiers, 'y': ips_scores, 'type': 'bar', 'name': 'IPS', 'marker': {'color': colors}},
            {'x': identifiers, 'y': astre_scores, 'type': 'bar', 'name': 'Astre', 'marker': {'color': colors}},
            {'x': identifiers, 'y': text_height, 'type': 'text', 'text': results, 'mode': 'text',
             'textfont': {'color': 'black'}, 'name': 'Texte de résultat'}
        ],
        'layout': {
            'xaxis': {'title': 'Numéro étudiants'},
            'yaxis': {'title': 'Scores'},
            'barmode': 'relative',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'lightblue'
        }
    }
    # Create the table
    table = html.Table([
        html.Tr([html.Th('Nombre d\'étudiants'), html.Th('Nombre d\'IPS'), html.Th('Nombre d\'Astres')]),
        html.Tr([html.Td(num_etudiants), html.Td(num_ips), html.Td(num_astres)]),
    ])

    return fig, table  # Return the table as the second output

@app.callback(
    Output('save-button', 'n_clicks'),
    [Input('save-button', 'n_clicks')]
)
def save_weights(n_clicks):
    engine.save_hypotheses_to_json(allHypothese, 'hypotheses.json')

if __name__ == '__main__':
    app.run_server(debug=True)

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = dash.Dash(__name__)

# Stildefinitionen für helles Design
colors = {
    'background': '#ffffff',  # Weißer Hintergrund
    'text': '#333333',       # Dunkles Grau für Kontrast
    'accent': '#007bff',     # Helles Blau als Hauptakzent
    'secondary': '#ff9500',  # Orange als zweiter Akzent
}

styles = {
    'container': {'backgroundColor': colors['background'], 'padding': '30px', 'fontFamily': 'Helvetica, sans-serif'},
    'header': {'color': colors['text'], 'textAlign': 'center', 'fontSize': '36px', 'fontWeight': 'bold', 'marginBottom': '30px'},
    'graph': {'backgroundColor': '#f9f9f9', 'borderRadius': '12px', 'padding': '15px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'},
}

# Simulierte Daten
def generate_revenue_data():
    now = datetime.now()
    times = [now - timedelta(minutes=i) for i in range(10)]
    revenues = [np.random.randint(100, 1000) for _ in range(10)]
    return pd.DataFrame({'Time': times, 'Revenue': revenues})

def generate_map_data():
    cities = ['Zurich', 'Geneva', 'Bern', 'Basel', 'Lucerne']
    latitudes = [47.3769, 46.2044, 46.9480, 47.5596, 47.0502]
    longitudes = [8.5417, 6.1432, 7.4474, 7.5886, 8.3093]
    customer_counts = [np.random.randint(10, 100) for _ in cities]
    return pd.DataFrame({'City': cities, 'Lat': latitudes, 'Lon': longitudes, 'Customers': customer_counts})

def generate_product_data():
    products = ['Laptop', 'Smartphone', 'Tablet']
    sales = [np.random.randint(50, 500) for _ in products]
    return pd.DataFrame({'Product': products, 'Sales': sales})

# Layout
app.layout = html.Div(style=styles['container'], children=[
    html.H1("Interaktives Echtzeit-Dashboard", style=styles['header']),
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'justifyContent': 'center'}, children=[
        html.Div(style={'flex': '1', 'minWidth': '350px', 'maxWidth': '500px'}, children=[
            dcc.Graph(id='revenue-graph', style=styles['graph'])
        ]),
        html.Div(style={'flex': '1', 'minWidth': '350px', 'maxWidth': '500px'}, children=[
            dcc.Graph(id='product-graph', style=styles['graph'])
        ]),
        html.Div(style={'width': '100%', 'maxWidth': '1000px'}, children=[
            dcc.Graph(id='map-graph', style=styles['graph'])
        ]),
    ]),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0)
])

# Callbacks mit hellem Design
@app.callback(Output('revenue-graph', 'figure'), [Input('interval-component', 'n_intervals')])
def update_revenue_graph(n):
    df = generate_revenue_data()
    fig = px.line(df, x='Time', y='Revenue', title='Umsatzentwicklung (Live)',
                  template='plotly_white', color_discrete_sequence=[colors['accent']])
    fig.update_layout(title_font_size=20, margin={'l': 20, 'r': 20, 't': 40, 'b': 20},
                      font_color=colors['text'], plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9')
    fig.update_traces(line=dict(width=3))
    return fig

@app.callback(Output('map-graph', 'figure'), [Input('interval-component', 'n_intervals')])
def update_map_graph(n):
    df = generate_map_data()
    fig = px.scatter_mapbox(df, lat='Lat', lon='Lon', size='Customers', hover_name='City',
                            mapbox_style="carto-positron", zoom=7, title='Kundenverteilung in der Schweiz',
                            color_discrete_sequence=[colors['secondary']])
    fig.update_layout(title_font_size=20, margin={'l': 20, 'r': 20, 't': 40, 'b': 20},
                      font_color=colors['text'])
    return fig

@app.callback(Output('product-graph', 'figure'), [Input('interval-component', 'n_intervals')])
def update_product_graph(n):
    df = generate_product_data()
    fig = px.bar(df, x='Product', y='Sales', title='Top-Produkte nach Verkäufen',
                 template='plotly_white', color_discrete_sequence=[colors['accent']])
    fig.update_layout(title_font_size=20, margin={'l': 20, 'r': 20, 't': 40, 'b': 20},
                      font_color=colors['text'], plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
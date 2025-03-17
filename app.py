import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = dash.Dash(__name__)

# Simulierte Echtzeit-Daten für Umsatz
def generate_revenue_data():
    now = datetime.now()
    times = [now - timedelta(minutes=i) for i in range(10)]
    revenues = [np.random.randint(100, 1000) for _ in range(10)]
    return pd.DataFrame({'Time': times, 'Revenue': revenues})

# Simulierte Daten für Kundenverteilung in der Schweiz
def generate_map_data():
    cities = ['Zurich', 'Geneva', 'Bern']
    latitudes = [47.3769, 46.2044, 46.9480]
    longitudes = [8.5417, 6.1432, 7.4474]
    customer_counts = [np.random.randint(10, 100) for _ in cities]
    return pd.DataFrame({'City': cities, 'Lat': latitudes, 'Lon': longitudes, 'Customers': customer_counts})

# Simulierte Daten für Top-Produkte
def generate_product_data():
    products = ['Laptop', 'Smartphone', 'Tablet']
    sales = [np.random.randint(50, 500) for _ in products]
    return pd.DataFrame({'Product': products, 'Sales': sales})

# Layout des Dashboards
app.layout = html.Div([
    html.H1("Interaktives Echtzeit-Dashboard", style={'textAlign': 'center'}),
    html.Div([
        dcc.Graph(id='revenue-graph', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='product-graph', style={'width': '50%', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='map-graph', style={'width': '100%'}),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0)
])

# Callback für Umsatzdiagramm
@app.callback(Output('revenue-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_revenue_graph(n):
    df = generate_revenue_data()
    fig = px.line(df, x='Time', y='Revenue', title='Umsatzentwicklung (Live)')
    return fig

# Callback für Kartenvisualisierung
@app.callback(Output('map-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_map_graph(n):
    df = generate_map_data()
    fig = px.scatter_mapbox(df, lat='Lat', lon='Lon', size='Customers', hover_name='City',
                            mapbox_style="carto-positron", zoom=7, title='Kundenverteilung in der Schweiz')
    return fig

# Callback für Produktbalkendiagramm
@app.callback(Output('product-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_product_graph(n):
    df = generate_product_data()
    fig = px.bar(df, x='Product', y='Sales', title='Top-Produkte nach Verkäufen')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
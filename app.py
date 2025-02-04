import dash
from dash import Dash, dcc, html, page_registry, page_container
import dash_bootstrap_components as dbc
from callback_functions import generate_total_sales_treemap  # Import the function

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    style={
        "backgroundColor": "#121212",  
        "color": "blue", 
        "minHeight": "100vh", 
        "padding": "20px", 
    },
    children=[
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink(page["name"], href=page["relative_path"]))
                for page in page_registry.values()
            ],
            brand="Lazada Sales Analytic",
            brand_href="/",
            color="primary",
            dark=True,
            className="mb-4",
        ),
        page_container,
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)

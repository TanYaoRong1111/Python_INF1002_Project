import dash
from dash import Dash, dcc, html, page_registry, page_container
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout with a dark background
app.layout = html.Div(
    style={
        "backgroundColor": "#121212",  # Dark background color
         "color": "blue",  # Set all text to blue
        "minHeight": "100vh",  # Ensure the background covers the entire viewport height
        "padding": "20px",  # Add some padding for better spacing
    },
    children=[
        # Navbar
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
        # Page content
        page_container,
    ],
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
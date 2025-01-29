import dash
from dash import Dash, dcc, html, page_registry, page_container
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = html.Div([
    # Navbar
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(page["name"], href=page["relative_path"]))
            for page in page_registry.values()
        ] + [
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("External Link 1", href="https://example.com"),
                    dbc.DropdownMenuItem("External Link 2", href="https://example.org"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="Lazada Sales Analytic",
        brand_href="/",
        color="primary",
        dark=True,
        className="mb-4",
    ),

    # Page content
    page_container
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
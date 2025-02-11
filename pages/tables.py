import dash
from dash import dash_table, dcc, html, callback, register_page, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from callback_functions import update_table
from dash.exceptions import PreventUpdate
import dash_ag_grid as dag
import plotly.graph_objects as go

try:
    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import ChatPromptTemplate
except:
    print("langchain_ollama & langchain_core.prompts are not installed! Run `pip install langchain-ollama langchain-core` to install them.")

# Register page
register_page(__name__, name="Tables", path='/tables')

options = ['Laptop', 'Phones']
options2 = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia','Philippines']


# Define the AG Grid column definitions
columnDefs = [
    {"field": "Name", "filter": "agTextColumnFilter", "checkboxSelection": True},
    {"field": "Price", "filter": "agNumberColumnFilter"},
    {"field": "Brand", "filter": "agTextColumnFilter"},
    {"field": "Rating", "filter": "agNumberColumnFilter"},
    {"field": "Seller Name", "filter": "agTextColumnFilter"},
    {"field": "Number of Sales", "filter": "agNumberColumnFilter"},
    {"field": "Number of Reviews", "filter": "agNumberColumnFilter"}
]

df = pd.DataFrame({
    "Name": [],
    "Price": [],
    "Brand": [],
    "Rating": [],
    "Seller Name": [],
    "Number of Sales": [],
    "Number of Reviews": []
})

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H1("Welcome to AI Sales Analysis", className="text-center text-primary mb-4"),
                        html.P(
                            "Unlock insights into your sales data with AI-powered analytics.",
                            className="text-center lead mb-4"
                        ),
                    ],
                    style={
                        "background-color": "#f8f9fa",
                        "padding": "40px",
                        "border-radius": "10px",
                        "margin-bottom": "20px"
                    }
                ),
                width=12
            )
        ),

        # Dropdowns for Product Category and Country
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='product_category1',
                        options=options,
                        placeholder="Select Product Category",
                        className="mb-4"
                    ),
                    width=6, lg=4  # Responsive layout for mobile and desktop
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='select_country1',
                        options=options2,
                        placeholder="Select Country",
                        className="mb-4"
                    ),
                    width=6, lg=4  # Responsive layout for mobile and desktop
                )
            ],
            justify="center"  # Center-align the dropdowns
        ),

        # Output Alert
        dbc.Row(
            dbc.Col(
                html.Div(id="output", className="alert alert-info", role="alert"),
                className="mb-4"
            )
        ),

        # Data Table
        dbc.Row(
            dbc.Col(
                dag.AgGrid(
                    id="data-table2",
                    columnDefs=columnDefs,
                    rowData=df.to_dict("records"),
                    defaultColDef={
                        "filter": True,  # Enable filtering for all columns
                        "sortable": True,  # Enable sorting for all columns
                        "resizable": True,  # Allow resizing columns
                        "floatingFilter": True  # Add floating filters above the grid
                    },
                    dashGridOptions={"pagination": True, "paginationPageSize": 10, "rowSelection": "multiple"},
                    style={"height": 550, "width": "100%"}
                ),
                width=12
            )
        ),

        # Generate Insights Button
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Generate Insights Based on Selected Rows",
                    id="generate_insights_button",
                    color="primary",
                    size="lg",
                    className="mt-4 d-block mx-auto"
                ),
                width=6,
                className="d-flex justify-content-center"
            ),
            className="justify-content-center"
        ),

        # Loading Spinner and Text Area
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    id="loading-spinner",
                    type="circle",
                    children=[
                        dcc.Graph(id="loading-circle", style={"display": "none"}),
                        dcc.Textarea(
                            id="text-area",
                            placeholder="AI Generated Response...",
                            style={
                                "width": "100%",
                                "height": "400px",
                                "margin-top": "20px",
                                "text-align": "center",
                                "font-size": "24px",
                                "line-height": "400px",
                                "font-weight": "bold",
                                "color": "#aaa",
                                "background-color": "#f9f9f9",
                                "border": "none"
                            },
                            disabled=True
                        )
                    ]
                ),
                style={
                    "background-color": "#f0f8ff",
                    "padding": "20px",
                    "border-radius": "10px",
                    "margin-top": "20px"
                }
            )
        )
    ],
    fluid=True,
    style={'padding': '20px'}
    
)

@callback(
    Output('data-table2', 'rowData'),
    [Input('product_category1', 'value'), Input('select_country1', 'value')]
)
def update_content(product_category1, select_country1):
    if product_category1 is None or select_country1 is None:
        raise PreventUpdate
    else:
        return update_table(str(product_category1), str(select_country1))
        
# Callback to handle button click and selected rows
@callback(
    [
        Output("loading-circle", "style"),  # Control the visibility of the loading circle
        Output("text-area", "value"),       # Update the text area content
        Output("text-area", "style")        # Control the visibility of the text area
    ],
    [Input("generate_insights_button", "n_clicks")],
    [State("data-table2", "selectedRows")]
)
def update_content(n_clicks, selected_rows):
    if n_clicks is None or selected_rows is None:
        raise PreventUpdate
    
    try:

        # Convert selected rows to a textual format
        selected_data = pd.DataFrame(selected_rows)
        selected_text = selected_data.to_string(index=False)

        # Call the Llama3.1 AI model
        response = parse_with_ollama(dom_chunks=[selected_text], parse_description="Analyze the sales data and provide insights.")

        # Return the AI response and update the text area
        return {"display": "none"}, response, {"width": "100%", "height": 400, "margin-top": "20px", "display": "block"}
    except:
        return "Local AI Model Not Detected!!!", {"display": "block"}

# Function to interact with Llama3.1 AI
def parse_with_ollama(dom_chunks, parse_description):
    template = (
        "You are a highly skilled sales analyst tasked with providing meaningful, data-driven business insights based on the information provided in the following text content: {dom_content}. "
        "Your response should focus on identifying key trends, patterns, opportunities, and actionable recommendations that can help improve sales performance or decision-making. "
        "Ensure your insights are concise, professional, and directly tied to the data or context provided. "
        "Do not ask any questions, make assumptions beyond the given content, or include irrelevant information. "
        "Structure your response as follows: "
        "1. Key Observations: Highlight the most important findings from the data. "
        "2. Insights: Explain what these findings mean for the business. "
        "3. Recommendations: Provide clear, actionable steps the business can take to leverage these insights. "
        "4. Comparisions: Provide comparisions between products and explain the differences. "
    )

    model = OllamaLLM(model="llama3.1")

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        parsed_results.append(response)

    return "\n".join(parsed_results)


    
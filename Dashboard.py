import pandas as pd
import dash
from dash import dcc  # dash core components
from dash import html # dash html components 
from dash.dependencies import Input, Output
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_csv("saber11_bogota_limpio.csv")

estrato_col = "estrato_num"
estratos_orden = sorted(df[estrato_col].unique())
naturalezas = sorted(df["cole_naturaleza"].unique())

score_options = [
    "punt_global",
    "punt_matematicas",
    "punt_lectura_critica",
    "punt_c_naturales",
    "punt_sociales_ciudadanas",
    "punt_ingles",
]

app.layout = html.Div(
    style={"maxWidth": "1100px", "margin": "0 auto", "padding": "20px"},
    children=[
        html.H3("Saber 11 Bogotá"),
        html.H4("Puntaje vs Estrato"),
        html.P(
            "Cómo cambia la distribución de los puntajes según el estrato socioeconómico."
        ),

        html.Div(
            style={"display": "flex", "gap": "20px", "flexWrap": "wrap"},
            children=[
                html.Div(
                    style={"minWidth": "260px"},
                    children=[
                        html.Label("Selecciona el puntaje:"),
                        dcc.Dropdown(
                            id="score-col",
                            options=[{"label": c, "value": c} for c in score_options],
                            value="punt_global",
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    style={"minWidth": "260px"},
                    children=[
                        html.Label("Tipo de gráfico:"),
                        dcc.RadioItems(
                            id="plot-type",
                            options=[
                                {"label": "Boxplot", "value": "box"},
                                {"label": "Violin", "value": "violin"},
                            ],
                            value="box",
                            inline=True,
                        ),
                    ],
                ),
            ],
        ),

        html.Br(),

        dcc.Graph(id="puntaje-vs-estrato"),

        html.H4("Resumen por estrato"),
        html.Div(id="tabla-resumen", style={"marginTop": "10px"}),

        html.Hr(),
        html.H4("Histograma de densidad de probabilidad segun naturaleza del colegio"),
        html.Div(
            style={"display": "flex", "gap": "20px", "flexWrap": "wrap"},
            children=[
                html.Div(
                    style={"minWidth": "260px"},
                    children=[
                        html.Label("Selecciona el puntaje:"),
                        dcc.Dropdown(
                            id="score-col2",
                            options=[{"label": c, "value": c} for c in score_options],
                            value="punt_global",
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    style={"minWidth": "260px"},
                    children=[
                        html.Label("Tipo de gráfico:"),
                        dcc.RadioItems(
                            id="plot-type2",
                            options=[
                                {"label": "Histograma de densidad de probabilidad", "value": "prob"},
                                {"label": "Histograma de observaciones", "value": "obser"},
                            ],
                            value="box",
                            inline=True,
                        ),
                    ],
                ),
            ],
        ),

        dcc.Graph(id="scatter-naturaleza"),
        html.Hr(),
        html.H4("Puntaje según área de ubicación del colegio"),
        html.Label("Selecciona el puntaje que quiere observar:"),
        dcc.Dropdown(
            id="score-col3",
            options=[{"label": c, "value": c} for c in score_options],
            value="punt_global",
            clearable=False,
        ),

        dcc.Graph(id="box-area-colegio"),
    ],
)

@app.callback(
    Output("puntaje-vs-estrato", "figure"),
    Output("tabla-resumen", "children"),
    Input("score-col", "value"),
    Input("plot-type", "value"),
)
def update_dashboard(score_col, plot_type):
    # Figura
    if plot_type == "box":
        fig = px.box(
            df,
            x=estrato_col,
            y=score_col,
            category_orders={estrato_col: estratos_orden},
            points="outliers",  # muestra outliers
            labels={estrato_col: "Estrato", score_col: score_col},
            title=f"{score_col} por estrato (Boxplot)",
        )
    else:
        fig = px.violin(
            df,
            x=estrato_col,
            y=score_col,
            category_orders={estrato_col: estratos_orden},
            box=True,       # agrega box dentro del violín
            points="outliers",
            labels={estrato_col: "Estrato", score_col: score_col},
            title=f"{score_col} por estrato (Violin)",
        )

    fig.update_layout(template="simple_white")

    # Resumen por estrato (promedio, mediana, n)
    summary = (
        df.groupby(estrato_col)[score_col]
        .agg(["count", "mean", "median"])
        .reset_index()
        .sort_values(estrato_col)
    )

    table = html.Table(
        style={"borderCollapse": "collapse", "width": "520px"},
        children=[
            html.Thead(
                html.Tr([
                    html.Th("Estrato", style={"border": "1px solid #ccc", "padding": "6px"}),
                    html.Th("N", style={"border": "1px solid #ccc", "padding": "6px"}),
                    html.Th("Promedio", style={"border": "1px solid #ccc", "padding": "6px"}),
                    html.Th("Mediana", style={"border": "1px solid #ccc", "padding": "6px"}),
                ])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(int(row[estrato_col]), style={"border": "1px solid #ccc", "padding": "6px"}),
                    html.Td(int(row["count"]), style={"border": "1px solid #ccc", "padding": "6px"}),
                    html.Td(round(row["mean"], 2), style={"border": "1px solid #ccc", "padding": "6px"}),
                    html.Td(round(row["median"], 2), style={"border": "1px solid #ccc", "padding": "6px"}),
                ])
                for _, row in summary.iterrows()
            ]),
        ],
    )

    return fig, table

@app.callback(
    Output("scatter-naturaleza", "figure"),
    Input("score-col2", "value"),
    Input("plot-type2", "value")
)
def update_hist(score_col2,plot_type2):

    if plot_type2 == "prob":
        fig = px.histogram(
        df,
        x=score_col2,
        color="cole_naturaleza",
        nbins=40,
        barmode="overlay",
        opacity=0.6,
        histnorm="probability density",
        )
    
    else:
        fig = px.histogram(
        df,
        x=score_col2,
        color="cole_naturaleza",
        nbins=40,
        barmode="overlay",
        opacity=0.6,
        labels={score_col2: "Puntaje", "cole_naturaleza": "Naturaleza"},
        title=f"Distribución de {score_col2} por naturaleza del colegio",
        )

    fig.update_layout(template="simple_white")

    return fig

@app.callback(
    Output("box-area-colegio", "figure"),
    Input("score-col3", "value")
)
def update_box_internet(score_col3):

    fig = px.box(
        df,
        x="cole_area_ubicacion",
        y=score_col3,
        color="cole_area_ubicacion",
        labels={
            "cole_area_ubicacion": "¿En que area se encuentra el colegio?",
            score_col3: "Puntaje"
        },
        title=f"{score_col3} según área de ubicación del colegio",
        points="outliers"
    )

    fig.update_layout(template="simple_white")
    return fig

if __name__ == "__main__":
    app.run(debug=True)

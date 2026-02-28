import pandas as pd
import dash
from dash import dash_table
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
        html.H3("Análisis de datos pruebas saber 11 Bogotá"),
        html.P("En el siguiente tablero, podra evidenciar algunas visualizaciones pertinentes de las pruebas Saber 11" \
        " en la ciudad de Bogotá. Para esto, usted podra interactuar con los graficos para definir que tipo de" \
        " informacion quiere visualizar."
        ),
        html.H4("1. Diagrama de cajas y violín del puntaje segun el estrato socioeconomico"),
        html.P(
            "A continuacion, podrá observar cómo cambia la distribución de los" \
            " puntajes según el estrato socioeconómico de los estudiantes que presentan las pruebas saber 11." \
            " El objetivo del siguiente gráfico es que pueda ver la diferencia que se presenta entre los puntajes " \
            "de los diferentes estratos socioeconomicos. Para tal fin, por favor seleccione el puntaje" \
            " y tipo de gráfico que desea observar."
        ),

        html.Br(),

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
        html.Br(),
        html.P(
            "La gráfica muestra una relación claramente creciente entre el estrato socioeconómico y el puntaje" \
            " global: a medida que aumenta el estrato, se observa un desplazamiento hacia arriba en la mediana" \
            " y en la distribución general de los puntajes. Los estratos 1 y 2 presentan las medianas más bajas" \
            " y mayor concentración en rangos inferiores, mientras que los estratos 4, 5 y 6 exhiben puntajes" \
            " centrales más altos y una distribución ubicada en niveles superiores. Esto sugiere una asociación" \
            " positiva entre nivel socioeconómico y desempeño académico en la prueba Saber 11, evidenciando una" \
            " brecha sistemática entre los estratos más bajos y los más altos. Así mismo, esto se vuelve a" \
            " observar en la tabla de las estadisticas, donde tanto el promedio como la mediana evidencian los" \
            " resultados de la gráfica."
        ),

        html.Hr(),
        html.H4("2. Histograma del puntaje según naturaleza del colegio"),
        html.P(
            "En esta sección, podra observar un análisis de la prueba saber 11 observando diferencias en el puntaje"
            " que desee visualizar, dependiendo de la naturaleza del colegio de los estudiantes. Siendo oficial" \
            " los colegios publicos y no oficial los colegios privados. En esta sección puede escoger el puntaje que quiera" \
            " y podrá visualizar dos tipos de graficos, un histograma de densidad de probabilidad o un histograma de las" \
            " observaciones."
        ),

        html.Br(),
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
        html.Br(),

        html.H4("2.1. Diagrama de cajas del puntaje según naturaleza del colegio y bilingüismo"),
        html.P(
            "En esta sección, puede observar un diagrama de cajas que muestra la distribución del puntaje" \
            " según la naturaleza del colegio (oficial o no oficial) y si ofrece programas bilingües." \
            " Esto permite identificar si hay diferencias en el desempeño entre colegios con y sin programas bilingües."
        ),
        html.Br(),
        dcc.Graph(id="box-naturaleza-bilingue"),
        html.Br(),
        html.H4("Resumen por naturaleza y bilingüismo"),
        html.Div(id="tabla-bilingue", style={"marginTop": "10px"}),
        html.Br(),
        html.P(
            "Las características institucionales del colegio influyen de manera significativa en los puntajes del ICFES en Bogotá D.C." \
            " El análisis muestra que los colegios no oficiales presentan, en promedio, puntajes superiores frente a los oficiales," \
            " evidenciando una distribución desplazada hacia valores más altos y mayores medianas en los diagramas de cajas." \
            " Adicionalmente, la presencia de programas bilingües se asocia con un mejor desempeño académico, especialmente en los" \
            " colegios no oficiales, donde se observan los promedios más altos. En contraste, los colegios oficiales sin oferta" \
            " bilingüe presentan los puntajes más bajos del análisis." \
            " En conjunto, los resultados sugieren que tanto la naturaleza del colegio como la oferta de bilingüismo están" \
            " relacionadas con diferencias sistemáticas en el desempeño académico, reflejando posibles brechas en recursos," \
            " contexto socioeconómico y condiciones institucionales dentro del sistema educativo de la ciudad."
        ),
        html.Br(),
        

        html.Hr(),
        html.H4("3. Diagrama de cajas del puntaje según área de ubicación del colegio"),
        html.P(
            "En esta última sección, puede encontrar la visualización de un diagrama de cajas para observar la relación" \
            " entre el puntaje de las pruebas saber 11 y el área de ubicación del colegio (rural o urbana), separado por" \
            " la caracteristica del colegio (academico, tecnico/academico o tecnico). Este" \
            " grafico permitira observar si la ubicación del colegio y su caracteristica influye o no en" \
            " el desempeño de los estudiantes en las pruebas."
        ),
        html.Br(),
        html.Label("Seleccione el puntaje que quiere observar:"),
        dcc.Dropdown(
            id="score-col3",
            options=[{"label": c, "value": c} for c in score_options],
            value="punt_global",
            clearable=False,
        ),

        dcc.Graph(id="box-area-colegio"),
        html.Br(),
        html.H4("Resumen por area y caracteristica del colegio"),
        html.Div(id="tabla-resumen2", style={"marginTop": "10px"}),
        html.Br(),
        html.P(
            "La gráfica y la tabla muestran que las diferencias en el puntaje global entre área urbana" \
            " y rural no son tan marcadas como las observadas por estrato o naturaleza del colegio, aunque" \
            " sí se identifican variaciones según el carácter institucional. En zona rural, los colegios académicos" \
            " presentan el promedio más alto (287.75), superando incluso a los urbanos académicos (274.54)," \
            " mientras que los técnico/académico rurales registran los valores más bajos. En el área urbana," \
            " los colegios técnicos alcanzan ligeramente el mayor promedio (276.69), pero con medianas muy cercanas" \
            " entre los distintos caracteres, lo que evidencia una fuerte superposición en las distribuciones." \
            " En conjunto, los resultados sugieren que el carácter del colegio influye levemente en el desempeño," \
            " pero la brecha entre urbano y rural es relativamente moderada y no muestra diferencias estructurales" \
            " tan amplias como en otras variables analizadas."
        ),
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
            color=estrato_col
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
            color=estrato_col
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
        labels={score_col2: "Puntaje", "cole_naturaleza": "Naturaleza"},
        title=f"Densidad de probabilidad de {score_col2} por naturaleza del colegio",
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
    Output("tabla-resumen2", "children"),
    Input("score-col3", "value")
)
def update_box_internet(score_col3):
    df_filtrado = df[
        ~df["cole_caracter"].isin(["SIN REGISTRO", "NO APLICA","no aplica"])
]

    fig = px.box(
        df_filtrado,
        x="cole_area_ubicacion",
        y=score_col3,
        color="cole_caracter",
        labels={
            "cole_area_ubicacion": "¿En qué área se encuentra el colegio?",
            score_col3: "Puntaje",
            "cole_caracter": "Carácter del colegio"
        },
        title=f"{score_col3} según área y carácter del colegio",
        points="outliers"
    )

    fig.update_layout(template="simple_white", boxmode="group")

    summary = (
        df_filtrado.groupby(["cole_area_ubicacion", "cole_caracter"])[score_col3]
        .agg(["count", "mean", "median"])
        .reset_index()
        .sort_values(["cole_area_ubicacion", "cole_caracter"])
    )
    summary["mean"] = summary["mean"].round(2)
    summary["median"] = summary["median"].round(2)

    return fig,dash_table.DataTable(
        columns=[
            {"name": "Área", "id": "cole_area_ubicacion"},
            {"name": "Carácter", "id": "cole_caracter"},
            {"name": "N", "id": "count"},
            {"name": "Promedio", "id": "mean"},
            {"name": "Mediana", "id": "median"},
        ],
        data=summary.to_dict("records"),
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center"},
        style_header={"fontWeight": "bold"},
    )

@app.callback(
    Output("box-naturaleza-bilingue", "figure"),
    Output("tabla-bilingue", "children"),
    Input("score-col2", "value")
)
def update_bilingue(score_col2):
    # Filtrar datos sin "SIN REGISTRO"
    df_filtrado = df[~df["cole_bilingue"].isin(["SIN REGISTRO", "NO APLICA", "no aplica"])]
    
    # Crear boxplot
    fig = px.box(
        df_filtrado,
        x="cole_naturaleza",
        y=score_col2,
        color="cole_bilingue",
        labels={
            "cole_naturaleza": "Naturaleza del Colegio",
            score_col2: "Puntaje",
            "cole_bilingue": "¿Es Bilingüe?"
        },
        title=f"{score_col2} según naturaleza y bilingüismo del colegio",
        points="outliers"
    )
    
    fig.update_layout(template="simple_white", boxmode="group")
    
    # Crear tabla con resumen
    summary = (
        df_filtrado.groupby(["cole_naturaleza", "cole_bilingue"])[score_col2]
        .agg(["count", "mean", "median"])
        .reset_index()
        .sort_values(["cole_naturaleza", "cole_bilingue"])
    )
    summary["mean"] = summary["mean"].round(2)
    summary["median"] = summary["median"].round(2)
    
    return fig, dash_table.DataTable(
        columns=[
            {"name": "Naturaleza", "id": "cole_naturaleza"},
            {"name": "¿Es Bilingüe?", "id": "cole_bilingue"},
            {"name": "N", "id": "count"},
            {"name": "Promedio", "id": "mean"},
            {"name": "Mediana", "id": "median"},
        ],
        data=summary.to_dict("records"),
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center"},
        style_header={"fontWeight": "bold"},
    )

if __name__ == "__main__":
    app.run(debug=True)

import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware


def create_dash_app(weather_data):
    dash_app = Dash(__name__, requests_pathname_prefix="/dash/")

    dash_app.layout = html.Div(
        [
            html.H1("Визуализация погодных условий"),
            dcc.Dropdown(
                id="parameter",
                options=[
                    {"label": "Температура", "value": "temperature"},
                    {"label": "Скорость ветра", "value": "wind_speed"},
                    {"label": "Вероятность осадков", "value": "precipitation"},
                ],
                value="temperature",
                clearable=False,
            ),
            dcc.Graph(id="weather_graph"),
        ]
    )

    @dash_app.callback(Output("weather_graph", "figure"), [Input("parameter", "value")])
    def update_graph(selected_param):
        # Создаем списки значений для выбранного параметра и названий точек маршрута
        param_data = {
            "temperature": [point["temperature"] for point in weather_data],
            "wind_speed": [point["wind_speed"] for point in weather_data],
            "precipitation": [point["rain_probability"] for point in weather_data],
        }
        x_values = [f"Точка {i + 1}" for i in range(len(weather_data))]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=x_values, y=param_data[selected_param], mode="lines+markers")
        )
        fig.update_layout(title=f"График {selected_param}")

        return fig

    return dash_app


# Интеграция с FastAPI
def init_dash_app(fastapi_app: FastAPI, weather_data):
    dash_app = create_dash_app(weather_data)
    fastapi_app.mount("/dash", WSGIMiddleware(dash_app.server))

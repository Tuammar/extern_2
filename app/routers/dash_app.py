import plotly.graph_objs as go
from dash import Dash, dcc, html, dash
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware


# Функция для создания Dash-приложения
def create_dash_app(
    start_temperature,
    start_wind_speed,
    start_rain_probability,
    end_temperature,
    end_wind_speed,
    end_rain_probability,
):
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

    @dash_app.callback(
        dash.Output("weather_graph", "figure"), [dash.Input("parameter", "value")]
    )
    def update_graph(selected_param):
        # Пример данных, загруженных заранее. Это нужно заменить реальными данными.
        data = {
            "temperature": [start_temperature, end_temperature],
            "wind_speed": [start_wind_speed, end_wind_speed],
            "precipitation": [start_rain_probability, end_rain_probability],
        }
        x_values = ["В точке отправления", "В точке назначения"]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=x_values, y=data[selected_param], mode="lines+markers")
        )
        fig.update_layout(title=f"График {selected_param}")

        return fig

    return dash_app


# Интеграция с FastAPI
def init_dash_app(
    fastapi_app: FastAPI,
    start_temperature,
    start_wind_speed,
    start_precipitation,
    end_temperature,
    end_wind_speed,
    end_precipitation,
):
    dash_app = create_dash_app(
        start_temperature,
        start_wind_speed,
        start_precipitation,
        end_temperature,
        end_wind_speed,
        end_precipitation,
    )
    fastapi_app.mount("/dash", WSGIMiddleware(dash_app.server))

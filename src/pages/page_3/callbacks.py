from datetime import datetime as dt
from time import sleep

import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


def data_table_content(state):
    if state == "empty":
        df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/solar.csv")
        return df.to_dict("records"), "loaded"

    return dash.no_update, dash.no_update


def register_callbacks(app):
    @app.callback(Output("page_3_container", "hidden"), [Input("url", "pathname")])
    def show_page_3_container(pathname):
        if pathname == "/page_3":
            return False
        return True

    @app.callback(
        [Output("page_3_table", "data"), Output("page_3_state", "children")],
        [
            Input("url", "pathname"),
            Input("page_3_reload", "n_clicks"),
        ],
        [State("page_3_state", "children")],
    )
    def update_data_table(pathname, reload_clicked, page_3_state):

        ctx = dash.callback_context
        triggered = ctx.triggered[0].get("prop_id")

        if "page_3_reload" in triggered:
            page_3_state = "empty"

        if pathname == "/page_3":
            return data_table_content(page_3_state)
        raise PreventUpdate

    @app.callback(
        Output("page_3_saving", "children"),
        [Input("confirm_save", "n_clicks")],
        [State("save_data_checklist", "value")],
    )
    def trigger_save_page_3(save_clicked, values):
        if save_clicked and "page_3" in values:
            return f"Saving data started at {dt.utcnow()}"
        return dash.no_update

    @app.callback(
        Output("page_3_saved", "children"),
        [Input("page_3_saving", "children")],
        [State("page_3_table", "data")],
    )
    def save_page_3(saving, data):
        if saving:
            # Do something to save the data
            sleep(2)
            return f"Data saved at {dt.utcnow()}"
        return dash.no_update

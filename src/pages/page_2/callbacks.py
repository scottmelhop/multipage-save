from datetime import datetime as dt

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
    @app.callback(Output("page_2_container", "hidden"), [Input("url", "pathname")])
    def show_page_1_container(pathname):
        if pathname == "/page_2":
            return False
        return True

    @app.callback(
        [Output("page_2_table", "data"), Output("page_2_state", "children")],
        [
            Input("url", "pathname"),
            Input("page_2_reload", "n_clicks"),
        ],
        [State("page_2_state", "children")],
    )
    def update_data_table(pathname, reload_clicked, page_2_state):

        ctx = dash.callback_context
        triggered = ctx.triggered[0].get("prop_id")

        if "page_2_reload" in triggered:
            page_2_state = "empty"

        if pathname == "/page_2":
            return data_table_content(page_2_state)
        raise PreventUpdate

    @app.callback(
        Output("page_2_saving", "children"),
        [Input("confirm_save", "n_clicks")],
        [State("save_data_checklist", "value")],
    )
    def trigger_save_page_2(save_clicked, values):
        if save_clicked and "page_2" in values:
            return f"Saving data started at {dt.utcnow()}"
        return dash.no_update

    @app.callback(
        Output("page_2_saved", "children"),
        [Input("page_2_saving", "children")],
        [State("page_2_table", "data")],
    )
    def save_page_2(saving, data):
        if saving:
            # Do something to save the data
            return f"Data saved at {dt.utcnow()}"
        return dash.no_update

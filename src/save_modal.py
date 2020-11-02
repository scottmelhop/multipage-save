from ast import literal_eval

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from src.config import PAGE_LIST

data_pages = PAGE_LIST[1:]


spinner = dbc.Spinner(color="primary")


checklist = html.Div(
    [
        html.Div(
            dcc.Checklist(
                id="save_data_checklist",
                options=[],
                value=[],
                labelClassName="cogs-checkbox",
                inputClassName="checkbox-ui",
            )
        ),
    ]
)


save_modal = dbc.Modal(
    [
        html.Div(
            html.Div(id="save_spinner"), id="save_spinner_container", className="save-spinner-container", hidden=True
        ),
        dbc.ModalHeader("Data to Save"),
        dbc.ModalBody(
            [
                checklist,
                html.Div(id="save_status"),
                html.Div(id="saved_pages", hidden=True),
            ],
            className="save_modal_body",
        ),
        dbc.ModalFooter(
            [
                dbc.Button("Select All", id="save_modal_select_all", className="cogs-btn"),
                dbc.Button(
                    "Save",
                    id="confirm_save",
                    className="cogs-btn cogs-btn-danger",
                    disabled=True,
                ),
                dbc.Button("Close", id="close_save", className="cogs-btn"),
            ]
        ),
    ],
    id="save_modal",
)


def save_modal_callbacks(app):
    @app.callback(
        [Output("save_modal", "is_open"), Output("save_data_checklist", "options")],
        [Input("save_data", "n_clicks"), Input("close_save", "n_clicks")],
        [
            State("save_modal", "is_open"),
            *[State(f"{page['href']}_state", "children") for page in data_pages],
        ],
    )
    def show_save_data_modal(*args):
        if args[0] or args[1]:
            options = dash.no_update
            is_open = args[2]
            states = args[3:]
            if not is_open:
                options = [
                    {
                        "label": f"{data_pages[i]['name']} Data",
                        "value": data_pages[i]["href"],
                        "disabled": states[i] != "loaded",
                    }
                    for i in range(len(states))
                ]

            return not is_open, options
        raise PreventUpdate

    @app.callback(
        Output("save_data_checklist", "value"),
        [Input("save_modal_select_all", "n_clicks")],
        [State("save_data_checklist", "options")],
    )
    def toggle_save_all(select_clicked, options):
        if select_clicked:
            return [option["value"] for option in options if not option["disabled"]]
        raise PreventUpdate

    @app.callback(Output("confirm_save", "disabled"), [Input("save_data_checklist", "value")])
    def enable_save_button(value):
        if value:
            return False
        else:
            return True

    @app.callback(
        [
            Output("save_spinner", "children"),
            Output("saved_pages", "children"),
            Output("save_spinner_container", "hidden"),
            Output("save_status", "children"),
        ],
        [
            Input("confirm_save", "n_clicks"),
            Input("save_modal", "is_open"),
            *[Input(f"{page['href']}_saved", "children") for page in data_pages],
        ],
        [State("save_data_checklist", "value"), State("saved_pages", "children")],
    )
    def set_save_status(*args):
        ctx = dash.callback_context
        triggered = [trigger["prop_id"].replace("_saved.children", "") for trigger in ctx.triggered]

        if "save_modal.is_open" in triggered and not args[1]:
            return dash.no_update, dash.no_update, dash.no_update, ""

        if "confirm_save.n_clicks" in triggered:
            return spinner, "[]", False, ""

        if args[-1] and args[-2]:
            pages_to_save = sorted(args[-2])
            saved_pages = literal_eval(args[-1])
            saved_pages.extend(triggered)
            if pages_to_save == sorted(saved_pages):
                return "", "", True, "Saving Finished"
            else:
                return spinner, f"[{', '.join(saved_pages)}]", False, ""

        raise PreventUpdate

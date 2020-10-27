import importlib

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from src.config import PAGE_LIST
from src.navigation import navigation_layout
from src.pages.page_1.layout import layout as layout_page_1
from src.pages.page_2.layout import layout as layout_page_2
from src.pages.page_3.layout import layout as layout_page_3
from src.save_modal import save_modal, save_modal_callbacks

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)


app.layout = html.Div(
    [
        navigation_layout,
        html.Div([layout_page_1, layout_page_2, layout_page_3], id="main_container"),
        dcc.Location(id="url", refresh=False),
        save_modal,
    ]
)


@app.callback(Output("main_container", "children"), [Input("url", "pathname")])
def update_main_container(pathname):
    if pathname is None or pathname == "/":
        return dcc.Location(href="/page_1", id="initial-redirect")
    raise PreventUpdate


save_modal_callbacks(app)


for page in PAGE_LIST:
    modname = f'src.pages.{page["href"]}.callbacks'
    if importlib.util.find_spec(modname) is not None:  # type: ignore # noqa
        callback_module = importlib.import_module(modname)
        if hasattr(callback_module, "register_callbacks"):
            callback_module.register_callbacks(app)  # type: ignore # noqa

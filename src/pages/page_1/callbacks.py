from dash.dependencies import Input, Output


def register_callbacks(app):
    @app.callback(Output("page_1_container", "hidden"), [Input("url", "pathname")])
    def show_page_1_container(pathname):
        if pathname == "/page_1":
            return False
        return True

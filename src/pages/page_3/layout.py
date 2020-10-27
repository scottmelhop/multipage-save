import dash_core_components as dcc
import dash_html_components as html
import dash_table

columns = [
    "State",
    "Number of Solar Plants",
    "Installed Capacity (MW)",
    "Average MW Per Plant",
    "Generation (GWh)",
]

layout = html.Div(
    [
        html.Div("empty", id="page_3_state", hidden=True),
        html.Div(id="page_3_saving", hidden=True),
        html.Div(False, id="page_3_saved", hidden=True),
        html.Button("Reload Table", id="page_3_reload", className="cogs-btn cogs-btn-secondary"),
        dcc.Loading(
            dash_table.DataTable(
                id="page_3_table",
                columns=[{"name": i, "id": i} for i in columns],
                data=[{column: "" for column in columns}],
                editable=True,
            )
        ),
    ],
    id="page_3_container",
    hidden=True,
)

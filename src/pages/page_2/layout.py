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
        html.Div("empty", id="page_2_state", hidden=True),
        html.Div(id="page_2_saving", hidden=True),
        html.Div(False, id="page_2_saved", hidden=True),
        html.Button("Reload Table", id="page_2_reload", className="cogs-btn cogs-btn-secondary"),
        dcc.Loading(
            dash_table.DataTable(
                id="page_2_table",
                columns=[{"name": i, "id": i} for i in columns],
                data=[{column: "" for column in columns}],
                editable=True,
            )
        ),
    ],
    id="page_2_container",
    hidden=True,
)

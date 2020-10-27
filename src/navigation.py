import dash_core_components as dcc
import dash_html_components as html

from src.config import PAGE_LIST

navigation_layout = html.Div(
    [
        *[dcc.Link(page["name"], href=f"/{page['href']}", className="cogs-btn") for page in PAGE_LIST],
        html.Button(
            "Save Data",
            id="save_data",
            className="cogs-btn cogs-btn-primary cogs-btn-outline",
        ),
    ],
    className="navigation_header",
)

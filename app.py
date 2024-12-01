import dash
from dash import Dash, html, dcc

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        "/assets/vendor/fontawesome-free/css/all.min.css",
        "/assets/css/sb-admin-2.min.css",
    ],
    external_scripts=[
        "/assets/vendor/jquery/jquery.min.js",
        "/assets/vendor/bootstrap/js/bootstrap.bundle.min.js",
        "/assets/vendor/jquery-easing/jquery.easing.min.js",
        "/assets/js/sb-admin-2.min.js",
    ]
)

app.layout = html.Div([
    html.H1('Chloe - Header pour simplifier la naviation entre page'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
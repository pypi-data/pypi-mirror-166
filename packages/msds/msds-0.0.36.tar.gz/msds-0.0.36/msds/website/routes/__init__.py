from msds.website.app.home import display_home, display_data

def init_app(app):
    app.add_url_rule('/', view_func = display_home)
    app.add_url_rule('/data', view_func = display_data)
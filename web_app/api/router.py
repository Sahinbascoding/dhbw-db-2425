from web_app.api.routes.route_index import index
from web_app.api.routes.route_add_data import add_data
from web_app.api.routes.route_reports import reports
from web_app.api.routes.route_converter import convert
from web_app.api.routes.route_view_table import view_table
from web_app.api.routes.route_update_row import update_row
from web_app.api.routes.route_database_stats import get_database_stats
from web_app.api.routes.route_import_sql import import_sql_db
from web_app.api.routes.route_reset_sql import reset_mysql_db
from web_app.api.routes.route_reset_mongo import reset_mongo_db


def register_routes(app):
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/add-data', 'add_data', add_data, methods=['GET', 'POST'])
    app.add_url_rule('/reports', 'reports', reports, methods=['GET', 'POST'])
    app.add_url_rule('/convert', 'convert', convert, methods=['GET', 'POST'])
    app.add_url_rule('/view-table', 'view_table', view_table, methods=['GET', 'POST'])
    app.add_url_rule('/update/<table_name>', 'update_row', update_row, methods=['POST'])
    app.add_url_rule('/database-stats', 'get_database_stats', get_database_stats, methods=['GET'])

    # Zusätzliche Hilfsrouten
    app.add_url_rule('/import-sql', 'import_sql_db', import_sql_db, methods=['POST'])
    app.add_url_rule('/reset-mysql', 'reset_mysql_db', reset_mysql_db, methods=['POST'])
    app.add_url_rule('/reset-mongo', 'reset_mongo_db', reset_mongo_db, methods=['POST'])

# Datei: api/routes/route_view_table.py

from flask import render_template, request, redirect, url_for
from sqlalchemy import MetaData, text
import logging
from app import mysql_engine

logger = logging.getLogger(__name__)

def view_table():
    if request.method in ['POST', 'GET']:
        selected_table = (
            request.form.get('selected_table')
            if request.method == 'POST'
            else request.args.get('selected_table')
        )
        page = int(request.args.get('page', 1))
        rows_per_page = 10

        if selected_table:
            meta = MetaData()
            meta.reflect(bind=mysql_engine)
            table = meta.tables[selected_table]
            rows = []
            total_rows = 0

            with mysql_engine.connect() as conn:
                try:
                    count_query = text(f"SELECT COUNT(*) FROM {selected_table}")
                    total_rows_query = conn.execute(count_query)
                    total_rows = total_rows_query.scalar()

                    offset = (page - 1) * rows_per_page
                    query = table.select().limit(rows_per_page).offset(offset)
                    result = conn.execute(query)

                    if hasattr(result, 'keys'):
                        rows = [dict(zip(result.keys(), row)) for row in result]
                    else:
                        rows = [row._asdict() for row in result]

                    logger.info(f"{len(rows)} rows loaded from {selected_table}.")
                except Exception as exc:
                    logger.error(f"Error processing rows from {selected_table}: {exc}")
                    rows = []

            total_pages = (total_rows + rows_per_page - 1) // rows_per_page

            return render_template(
                'view_table.html',
                table_name=selected_table,
                rows=rows,
                page=page,
                total_pages=total_pages,
                rows_per_page=rows_per_page,
                selected_table=selected_table
            )

    return redirect(url_for('index'))

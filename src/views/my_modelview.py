# src/views/base_modelview.py
from flask_admin.contrib.sqla import ModelView
from flask import flash, current_app
from flask_login import current_user
from flask import redirect, url_for, request, Response
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
import csv
from flask_admin import expose
from io import StringIO  # StringIO importálása

class MyModelView(ModelView):
    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop('role', None)
        self.columns_to_export = kwargs.pop('columns_to_export', None)  # Beállítható oszlopok exportálása
        super(MyModelView, self).__init__(*args, **kwargs)
        
    def is_accessible(self):
        # Check if the user is authenticated and has the required role
        if not current_user.is_authenticated:
            return False
        if self.role and current_user.role != self.role:
            return False
        return True

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login if access is denied
        return redirect(url_for('user_ctrl.login'))
    
    def on_model_change(self, form, model, is_created):
        try:
            self.session.add(model)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
        super(MyModelView, self).on_model_change(form, model, is_created)

    def handle_view_exception(self, exc):
        flash(f'An unexpected error occurred: {exc}', 'error')
        return False
    
    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True, page_size=20):
        """
            Return records from the database.

            :param page:
                Page number
            :param sort_column:
                Sort column name
            :param sort_desc:
                Descending or ascending sort
            :param search:
                Search query
            :param execute:
                Execute query immediately? Default is `True`
            :param filters:
                List of filter tuples
            :param page_size:
                Number of results. Defaults to ModelView's page_size. Can be
                overriden to change the page_size limit. Removing the page_size
                limit requires setting page_size to 0 or False.
        """

        # Will contain join paths with optional aliased object
        joins = {}
        count_joins = {}

        query = self.get_query()
        count_query = self.get_count_query() if not self.simple_list_pager else None

        # Ignore eager-loaded relations (prevent unnecessary joins)
        # TODO: Separate join detection for query and count query?
        if hasattr(query, '_join_entities'):
            for entity in query._join_entities:
                for table in entity.tables:
                    joins[table] = None

        # Apply search criteria
        if self._search_supported and search:
            query, count_query, joins, count_joins = self._apply_search(query,
                                                                        count_query,
                                                                        joins,
                                                                        count_joins,
                                                                        search)

        # Apply filters
        if filters and self._filters:
            query, count_query, joins, count_joins = self._apply_filters(query,
                                                                         count_query,
                                                                         joins,
                                                                         count_joins,
                                                                         filters)

        # Calculate number of rows if necessary
        count = count_query.scalar() if count_query else None

        # Auto join
        for j in self._auto_joins:
            query = query.options(joinedload(j))

        # Sorting
        query, joins = self._apply_sorting(query, joins, sort_column, sort_desc)

        self.query_all = query
        
        query = self._apply_pagination(query, page, page_size)
        self.query_page = query
        # Execute if needed
        if execute:
            query = query.all()

        return count, query
    
    def get_sum(self, column_name):
        """
        Calculate the sum of a specified column.

        :param column_name: The name of the column to sum.
        :return: The total sum of the specified column.
        """
        # Ensure the column exists in the model
        if not hasattr(self.model, column_name):
            raise ValueError(f"Column '{column_name}' does not exist in the model.")

        try:
            query = self.query_all
            total_sum = query.with_entities(func.sum(getattr(self.model, column_name))).scalar()
            return total_sum if total_sum is not None else 0
        except Exception as e:
            # Handle specific exceptions or log the error as needed
            current_app.logger.error(f"Error calculating sum for column '{column_name}': {str(e)}")
            return 0
        
    @expose('/export/csv/')
    def export_csv(self):
        """
        Exportálja az aktuális szűrt adatokat CSV formátumban.
        """
        try:
            # Aktuális lekérdezés
            query = self.get_query()

            # Alkalmazza a szűrőket, ha léteznek
            filters = self._filters
            query = self.apply_filters(query, filters)

            # Fejléc (column_labels alapján vagy column_list alapján)
            if self.columns_to_export:
                column_headers = list(self.columns_to_export.values())  # Felhasználói oszlopok
                column_list = list(self.columns_to_export.keys())
            else:
                column_headers = [
                    self.column_labels.get(col, col)  # Oszlop címke, ha elérhető
                    for col in self.column_list
                ]
                column_list = self.column_list


            # Adatok előkészítése
            rows = []
            for item in query:
                row = []
                for col in column_list:
                    attr = self._get_attr_value(item, col)
                    # Ha szám, akkor formázzuk tizedesvesszővel
                    if isinstance(attr, float):
                        attr = f"{attr:.2f}".replace('.', ',')  # Tizedesvesszőre cserél
                    row.append(attr)
                rows.append(row)

            # CSV válasz generálása
            output = StringIO()  # StringIO objektum létrehozása
            writer = csv.writer(output, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(column_headers)  # Fejléc sor
            for row in rows:
                writer.writerow(row)  # Adatsorok

            # HTTP válasz előkészítése
            output.seek(0)  # Visszaállítjuk az olvasási pozíciót
            csv_data = output.getvalue()  # CSV tartalom karakterláncként
            # Encode-olás ISO-8859-2 kódolással
            response = Response(csv_data.encode('iso-8859-2'), mimetype='text/csv')
            response.headers['Content-Disposition'] = 'attachment; filename=export.csv'
            return response

        except Exception as e:
            self.session.rollback()
            current_app.logger.error(f"CSV exportálási hiba: {str(e)}")
            return "Hiba történt az exportálás során.", 500


    def apply_filters(self, query, filters):
        """
        Szűrők alkalmazása a lekérdezéshez.
        Ez a metódus szűrők alkalmazásával módosítja a lekérdezést.
        """
        if filters:
            for filter in filters:
                # Ha a filter egy szűrő objektum (pl. CustomDateRangeFilter), akkor alkalmazza az apply metódust
                if hasattr(filter, 'apply'):
                    filter_value = getattr(filter, 'value', None)  # Biztosítjuk, hogy ne legyen 'None' érték
                    if filter_value is not None:
                        query = filter.apply(query, filter_value)  # Passzoljuk át a szűrő értéket
                elif isinstance(filter, tuple) and len(filter) == 2:
                    # Ha a filter egy egyszerű tuple (pl. ('field', value)), akkor alkalmazzuk a szűrést
                    field, value = filter
                    if value:
                        query = query.filter(getattr(self.model, field) == value)
        return query

    def _get_attr_value(self, obj, column):
        """
        Oszlopnév alapján attribútum érték lekérése.
        Támogatja a pontozott elérést (pl. 'car.license_plate').
        """
        try:
            for attr in column.split('.'):
                obj = getattr(obj, attr, None)
            return obj if obj is not None else ''
        except Exception:
            return ''



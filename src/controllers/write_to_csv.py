import csv
from flask import Response, current_app
from flask_admin import expose
from io import StringIO  # StringIO importálása

class ExportCSVMixin:
    """
    Általános keverékosztály (mixin) a CSV exportáláshoz Flask-Admin nézetekben.
    """

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
            column_headers = [
                self.column_labels.get(col, col)  # Oszlop címke, ha elérhető
                for col in self.column_list
            ]

            # Adatok előkészítése
            rows = []
            for item in query:
                row = []
                for col in self.column_list:
                    attr = self._get_attr_value(item, col)
                    row.append(attr)
                rows.append(row)

            # CSV válasz generálása
            output = StringIO()  # StringIO objektum létrehozása
            writer = csv.writer(output, delimiter=',')
            writer.writerow(column_headers)  # Fejléc sor
            for row in rows:
                writer.writerow(row)  # Adatsorok

            # HTTP válasz
            output.seek(0)  # Állítsuk vissza az olvasási pozíciót a StringIO objektumban
            response = Response(output.getvalue(), mimetype='text/csv')
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

import openpyxl as xl
import psycopg2 as pc


class DataBase():
    def __init__(self):
        try:
            self.db = pc.connect(
                dbname='bkfqvmiu',
                user='bkfqvmiu',
                password='kbc0-qYKx_NKBooqfoaf_xSoFYTyfaEb',
                host='lallah.db.elephantsql.com'
            )
        except Exception as ex:
            print(f"[ERROR] Algo fue mal. - {ex}")
        self.cursor = self.db.cursor()
        self.init_files()
        self.gestioner()

    def init_files(self):
        self.sexo_sheet = xl.load_workbook('files\Sexo.xlsx').active
        self.tipo_carrera_sheet = xl.load_workbook(
            'files\TipoCarrera.xlsx').active

    def __del__(self):
        # save file and database
        self.cursor.close()
        self.db.commit()
        self.db.close()

    def gestioner(self):
        """ call funcitons """
        # self.add_sexo()
        self.add_tipo_carrera()

    def add_sexo(self):
        structure = f"""
            INSERT INTO Sexo (sexo_id, nombre)
            VALUES (?, ?)
        """
        self.add(structure, self.sexo_sheet)

    def add_tipo_carrera(self):
        structure = f"""
            INSERT INTO TipoCarrera (tipo_carrera_id, nombre, presencial)
            VALUES (?, ?, ?)
        """
        self.add(structure, self.tipo_carrera_sheet)

    def add(self, structure, sheet):
        """ structure is something like:
            INSERT INTO table_name (some attrs)
            VALUES (? ,? , ...)
        """
        ws = sheet
        max_col = ws.max_column + 1
        max_row = ws.max_row + 1
        queries = []
        for row in ws.iter_rows(min_row=2, max_row=max_row, max_col=max_col):
            attrs = []
            for cell in row:
                if cell.value is None:
                    continue
                attrs.append(cell.value)
            if not attrs:
                continue
            query = structure
            for attr in attrs:
                query = query.replace('?', str(attr), 1)
            if not ';' in query:
                query += ';'
            queries.append(query)

        for index, query in enumerate(queries):
            print(f"[{index}] -> {query}")


def main():
    db = DataBase()


if __name__ == "__main__":
    main()

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

    def __del__(self):
        # save file and database
        self.cursor.close()
        self.db.commit()
        self.db.close()

    def gestioner(self):
        """ call funcitons """
        self.add_sexo()

    def add_sexo(self):
        ws = self.sexo_sheet
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
            structure = f"""
                INSERT INTO Sexo (sexo_id, nombre)
                VALUES ({attrs[0]}, {attrs[1]})
            """
            queries.append(structure)
        for index, query in enumerate(queries):
            print(f"[{index}] -> {query}")


def main():
    db = DataBase()


if __name__ == "__main__":
    main()

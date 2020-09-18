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

        self.sheets = {}
        self.simple_sheets = [
            'Sexo',
            'TipoCarrera',
            'TipoIdentificacion',
            'TipoDeuda',
            'TipoAsignatura',
            'DiaSemana',
            'Direccion',
            'Edificio',
            'Escuelas',
            'EstadoAsignatura',
            'Facultad',
            'PlanEstudios',
            'Carreras',
        ]

        for sheet in self.simple_sheets:

            self.sheets[sheet] = xl.load_workbook(f'files/{sheet}.xlsx').active

        print(self.sheets)

        # More complex tables

        # self.
    

    def __del__(self):
        # save file and database
        self.cursor.close()
        # self.db.commit()
        self.db.close()

    def gestioner(self):
        """ call funcitons """
        # self.add_sexo()
        # self.add_tipo_carrera()
        # self.add_tipo_identificacion()
        # self.add_tipo_deuda()
        # self.add_tipo_asignatura()
        # self.add_dia_semana()
        # self.add_direccion()
        # self.add_edificio()
        # self.add_escuela()
        # self.add_estado_asignatura()
        # self.add_facultad()
        self.add_plan_estudios()
        # self.add_carreras()

    def add_sexo(self):
        structure = f"""
            INSERT INTO Sexo (sexo_id, nombre)
            VALUES (?, ?)
        """
        self.add(structure, self.sheets['Sexo'])

    def add_tipo_carrera(self):
        structure = f"""
            INSERT INTO TipoCarrera (tipo_carrera_id, nombre, presencial)
            VALUES (?, ?, ?)
        """
        self.add(structure, self.sheets['TipoCarrera'])

    def add_tipo_identificacion(self):
        structure = f"""
            INSERT INTO TipoIdentificacion (tipo_identificacion_id, nombre)
            VALUES (?, ?)
        """
        self.add(structure, self.sheets['TipoIdentificacion'])

    def add_tipo_deuda(self):
        structure = f"""
            INSERT INTO TipoDeuda (tipo_deuda_id, nombre, maximo)
            VALUES (?, ?, ?)
        """
        self.add(structure, self.sheets['TipoDeuda'])

    def add_tipo_asignatura(self):
        structure = f"""
            INSERT INTO Carrera (tipo_asignatura_id, descripcion)
            VALUES (?, ?)
        """
        self.add(structure, self.sheets['TipoAsignatura'])

    def add_dia_semana(self):
        structure = f"""
            INSERT INTO DiaSemana (dia_semana_id, nombre)
            VALUES (?, ?)
        """
        self.add(structure, self.sheets['DiaSemana'])

    def add_direccion(self):
        structure = f"""
            INSERT INTO Direccion (direccion_id, calle, numero_a, numero_b, ciudad, departamento)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.add(structure, self.sheets['Direccion'])
    
    def add_edificio(self):
        structure = f"""
            INSERT INTO Edificio (edificio_id, nombre)
            VALUES (?, ?)
        """
        self.add(structure, self.sheets['Edificio'])
    
    def add_escuela(self):
        structure = f"""
            INSERT INTO Escuela (escuela_id, nombre, facultad_fk, edificio_fk)
            VALUES (?, ?, ?, ?)
        """
        self.add(structure, self.sheets['Escuela'])
    
    def add_estado_asignatura(self):
        structure = f"""
            INSERT INTO EstadoAsignatura (estado_asignatura_id, descripcion)
            VALUES (?, ?)
        """
        self.add(structure, self.sheets['EstadoAsignatura'])
    
    def add_facultad(self):
        structure = f"""
            INSERT INTO Facultad (facultad_id, facultad_nombre)
            VALUES (?, ?)
        """
        self.add(structure, self.sheets['Facultad'])
    
    def add_plan_estudios(self):
        structure = f"""
            INSERT INTO PlanEstudios (plan_estudios_id, numero_plan, carrera_fk)
            VALUES (?, ?, ?)
        """
        self.add(structure, self.sheets['PlanEstudios'])

    def add_carreras(self):
        structure = f"""
            INSERT INTO Carrera (carrera_id, nombre, plan_actual, cantidad_semestres, escuela_fk, tipo_carrera_fk)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.add(structure, self.sheets['Carreras'])

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

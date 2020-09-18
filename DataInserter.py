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
        self.tipo_identificacion_sheet = xl.load_workbook(
            'files\TipoIdentificacion.xlsx').active
        self.tipo_deuda_sheet = xl.load_workbook('files\TipoDeuda.xlsx').active
        self.tipo_asignatura_sheet = xl.load_workbook(
            'files\TipoAsignatura.xlsx').active
        self.dia_semana_sheet = xl.load_workbook('files\DiaSemana.xlsx').active
        self.direccion_sheet = xl.load_workbook('files\Direccion.xlsx').active
        self.edificio_sheet = xl.load_workbook('files\Edificios.xlsx').active
        self.escuela_sheet = xl.load_workbook('files\Escuelas.xlsx').active
        self.estado_asignatura_sheet = xl.load_workbook('files\EstadoAsignatura.xlsx').active
        self.facultad_sheet = xl.load_workbook('files\Facultad.xlsx').active
        self.plan_estudios_sheet = xl.load_workbook('files\PlanEstudios.xlsx').active
        self.carrera_sheet = xl.load_workbook('files\Carreras.xlsx').active

    def __del__(self):
        # save file and database
        self.cursor.close()
        self.db.commit()
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
        self.add(structure, self.sexo_sheet)

    def add_tipo_carrera(self):
        structure = f"""
            INSERT INTO TipoCarrera (tipo_carrera_id, nombre, presencial)
            VALUES (?, ?, ?)
        """
        self.add(structure, self.tipo_carrera_sheet)

    def add_tipo_identificacion(self):
        structure = f"""
            INSERT INTO TipoIdentificacion (tipo_identificacion_id, nombre)
            VALUES (?, ?)
        """
        self.add(structure, self.tipo_identificacion_sheet)

    def add_tipo_deuda(self):
        structure = f"""
            INSERT INTO TipoDeuda (tipo_deuda_id, nombre, maximo)
            VALUES (?, ?, ?)
        """
        self.add(structure, self.tipo_deuda_sheet)

    def add_tipo_asignatura(self):
        structure = f"""
            INSERT INTO Carrera (tipo_asignatura_id, descripcion)
            VALUES (?, ?)
        """
        self.add(structure, self.tipo_asignatura_sheet)

    def add_dia_semana(self):
        structure = f"""
            INSERT INTO DiaSemana (dia_semana_id, nombre)
            VALUES (?, ?)
        """
        self.add(structure, self.dia_semana_sheet)

    def add_direccion(self):
        structure = f"""
            INSERT INTO Direccion (direccion_id, calle, numero_a, numero_b, ciudad, departamento)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.add(structure, self.direccion_sheet)
    
    def add_edificio(self):
        structure = f"""
            INSERT INTO Edificio (edificio_id, nombre)
            VALUES (?, ?)
        """
        self.add(structure, self.edificio_sheet)
    
    def add_escuela(self):
        structure = f"""
            INSERT INTO Escuela (escuela_id, nombre, facultad_fk, edificio_fk)
            VALUES (?, ?, ?, ?)
        """
        self.add(structure, self.escuela_sheet)
    
    def add_estado_asignatura(self):
        structure = f"""
            INSERT INTO EstadoAsignatura (estado_asignatura_id, descripcion)
            VALUES (?, ?)
        """
        self.add(structure, self.estado_asignatura_sheet)
    
    def add_facultad(self):
        structure = f"""
            INSERT INTO Facultad (facultad_id, facultad_nombre)
            VALUES (?, ?)
        """
        self.add(structure, self.facultad_sheet)
    
    def add_plan_estudios(self):
        structure = f"""
            INSERT INTO PlanEstudios (plan_estudios_id, numero_plan, carrera_fk)
            VALUES (?, ?, ?)
        """
        self.add(structure, self.plan_estudios_sheet)

    def add_carreras(self):
        structure = f"""
            INSERT INTO Carrera (carrera_id, nombre, plan_actual, cantidad_semestres, escuela_fk, tipo_carrera_fk)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.add(structure, self.carrera_sheet)

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

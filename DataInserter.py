import openpyxl as xl
import psycopg2 as pc

import random

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
        # self.simple_sheets = [
        #     'Sexo',
        #     'TipoCarrera',
        #     'TipoIdentificacion',
        #     'TipoDeuda',
        #     'TipoAsignatura',
        #     'DiaSemana',
        #     'Direccion',
        #     'Edificio',
        #     'Escuelas',
        #     'EstadoAsignatura',
        #     'Facultad',
        #     'PlanEstudios',
        #     'Carreras',
        # ]

        # for sheet in self.simple_sheets:

        #     self.sheets[sheet] = xl.load_workbook(f'files/{sheet}.xlsx').active

        # print(self.sheets)

        # More complex tables

        self.complex_sheets = [
            'Franja',
            'Grupo',
            'Asignatura',
            'Edificio'
        ]

        for sheet in self.complex_sheets:

            self.sheets[sheet] = xl.load_workbook(f'files/{sheet}.xlsx').active
    

    def __del__(self):
        # save file and database
        self.cursor.close()
        # self.db.commit()
        self.db.close()

    def gestioner(self):
        """ call functions """
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
        # self.add_plan_estudios()
        # self.add_carreras()
        
        self.add_rooms()
        

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
    
    def add_fromlist(self, structure, nestedlist):

        queries = []

        for elements in nestedlist:

            query = structure

            for attr in elements:

                query = query.replace('?', str(attr), 1)
            
            if not ';' in query:
                query += ';'
            
            queries.append(query)
        
        # for index, query in enumerate(queries):
        #     print(f"[{index}] -> {query}")
        
        return queries


    
    def add_rooms(self):

        structure = f"""
            INSERT INTO Salon (salon_id, codigo, capacidad, edificio_fk)
            VALUES (?, ?, ?, ?)
        """
        
        groups_sheet = self.sheets['Grupo']
        buildings_sheet = self.sheets['Edificio']

        buildings = {}

        for row in buildings_sheet.iter_rows(min_row=2):

            building_id = row[0].value

            if building_id is None:
                continue

            building_name = (row[1].value).upper()

            buildings.setdefault(building_name, int(building_id))
            

        self.room_queries = []

        current_id = 0

        unique_ids = set()

        for row in groups_sheet.iter_rows(min_row=2):

            room_code = str(row[5].value).split(' ')[1].strip()
            room_capacity = int(row[2].value)

            try:

                room_building = buildings[str(row[4].value).upper()]
            
            except KeyError as e:

                room_building = random.randint(1, 20)

            room_uniqueid = f'{room_building}{room_code}'

            if room_uniqueid not in unique_ids:
                self.room_queries.append([
                    current_id,
                    room_code,
                    room_capacity,
                    room_building
                ])
            
            else:
                unique_ids.add(room_uniqueid)
        
        queries = self.add_fromlist(structure, self.room_queries)

        with open('out.txt', 'w') as f:

            for query in queries:

                f.write(str(query) + '\n')



def main():
    db = DataBase()


if __name__ == "__main__":
    main()

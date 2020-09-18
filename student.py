import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
import numpy as np
import os
import random
from data import man_names as men
from data import woman_names as women
from data import departamentos

NUM_STUDENTS = 1300
NUM_GRADES = 1000
NUM_DEBTS = 2000

class Personer():
    def __init__(self, amount, wb, address_sheet_name='address.xlsx'):
        self.amount = amount
        self.wb = wb
        self.id = 0  # init id
        self.attrs = [
            "persona_id",
            "nombre",
            "identificacion",
            "celular",
            "direccion_fk",
            "sexo_fk",
            "tipo_identificacion_fk"]
        self.sheet = wb.active
        self.address_id = 0
        self.init_address_sheet(address_sheet_name)
        self.init_sheets()
        self.fill_people()

    def __del__(self):
        self.wb.save('Persona.xlsx')
        self.address_wb.save('Direccion.xlsx')

    def init_address_sheet(self, addr_name):
        try:
            self.address_wb = openpyxl.load_workbook(addr_name)
        except FileNotFoundError:
            self.address_wb = openpyxl.Workbook()
        self.address_sheet = self.address_wb.active
        self.address_attrs = [
            'direccion_id',
            'calle',
            'numero_a',
            'numero_b',
            'ciudad',
            'departamento'
        ]

    def init_sheets(self):
        max_col = len(self.attrs)

        for row in self.sheet.iter_rows(min_col=1, max_col=max_col):
            for header, cell in zip(self.attrs, row):
                cell.value = header
                cell.alignment = Alignment(horizontal='center')

        max_col = len(self.address_attrs)

        for row in self.address_sheet.iter_rows(min_col=1, max_col=max_col):
            for header, cell in zip(self.address_attrs, row):
                cell.value = header
                cell.alignment = Alignment(horizontal='center')

    def create_person(self, persona_id=None, nombre=None, identificacion=None, celular=None, direccion_fk=None,  sexo_fk=None, tipo_identificacion_fk=None):
        data = {}
        if not nombre:
            if random.random():
                nombre = random.sample(men, 1)[0]
                sexo_fk = 1
            else:
                nombre = random.sample(women, 1)[0]
                sexo_fk = 2
            if not sexo_fk:
                sexo_fk = random.randint(1, 2)
        if not persona_id:
            self.id += 1
            persona_id = self.id
        if not identificacion:
            identificacion = random.randrange(1000000000, 9999999999)
        if not celular:
            celular = str(random.randint(
                300, 399)) + str(random.randint(100, 999)) + str(random.randint(1, 999)).zfill(3)

        direccion_fk = self.create_address()

        if random.random() <= 0.9:
            tipo_identificacion_fk = 1
        else:
            tipo_identificacion_fk = 2

        args = list(locals().values())[1:-1]

        for attr, value in zip(self.attrs, args):
            data.setdefault(attr, value)

        return data

    def fill_people(self, sheet=None):
        """ write people attrs into a given worksheet """
        if not sheet:
            sheet = self.sheet

        men_names = random.sample(men, int(np.ceil(2 * self.amount / 3)))
        men_names = [(name, 1) for name in men_names]
        women_names = random.sample(women, int(np.ceil(self.amount / 3)))
        women_names = [(name, 2) for name in women_names]

        # join lists
        names = men_names + women_names
        random.shuffle(names)

        # last_letter = get_column_letter(len(fields))
        # last_cell_coord = last_letter + str(self.amount + 1)
        for i in range(self.amount):
            data = self.create_person()
            self.add(data, sheet)
            # for attr, cell in zip(self.attrs, row):
            # cell.value = data[attr]
            # cell.Alignment(horizontal = 'center')

    def create_address(self, direccion_id=None, calle=None, numero_a=None, numero_b=None, ciudad=None, departamento=None):
        data = {}
        if not departamento:
            if random.random() <= 0.85:
                departamento = 'Santander'
            else:
                departamento = random.sample(departamentos.keys(), 1)[0]

        if not ciudad:
            ciudades = departamentos[departamento]
            ciudad = random.sample(ciudades, 1)[0]
        else:
            if not ciudad in departamentos[departamento]:
                ciudad = random.sample(departamentos[departamento], 1)
        if not direccion_id:
            self.address_id += 1
            direccion_id = self.address_id
        else:
            if direccion_id <= self.address_id:
                direccion_id = self.address_id + 1
                self.address_id = direccion_id
        if not calle:
            calle = str(random.randint(1, 100))

        args = list(locals().values())[1:-1]

        for attr, value in zip(self.address_attrs, args):
            data.setdefault(attr, value)
        self.add(data, self.address_sheet, people=False)
        return data['direccion_id']

    def add(self, data, sheet, people=True):
        # target_row = 1
        letter = get_column_letter(len(data))
        row = sheet.max_row + 1
        for row in sheet[f"A{row}:{letter}{row}"]:
            if people:
                for attr, cell in zip(self.attrs, row):
                    cell.value = str(data[attr])
                    cell.alignment = Alignment(horizontal='center')
            else:
                for attr, cell in zip(self.address_attrs, row):
                    cell.value = str(data[attr])
                    cell.alignment = Alignment(horizontal='center')


def generate_grades(index, sheet,order, n=3, student_fk=None, asignatura_fk=None):

    for i in range(1, n+1):
        data = []
        grade = round(random.random() * 5, 2)
        data.extend([index + i, grade, student_fk, asignatura_fk])

        letter = get_column_letter(len(data))
        row_target = sheet.max_row + 1

        for row in sheet[f"A{row_target}:{letter}{row_target}"]:
            for attr, value, cell in zip(order, data, row):
                cell.value = str(value)
                cell.alignment = Alignment(horizontal='center')


def fill_grades(n, sheet):
    order = [
        'calificacion_id',
        'nota',
        'estudiante_fk',
        'asignatura_fk'
    ]
    max_col = len(order)

    for row in sheet.iter_rows(min_col=1, max_col=max_col):
        for header, cell in zip(order, row):
            cell.value = header
            cell.alignment = Alignment(horizontal='center')
    index = 0
    for i in range(n):
        generate_grades(index, sheet, order)
        index += 3

def generate_debts(sheet, description=None, tipo_deuda_fk=None, estudiante_fk=None):
    order = [
        'deuda_id',
        'cantidad',
        'descripcion',
        'tipo_deuda_fk',
        'estudiante_fk',
    ]
    max_col = len(order)

    for row in sheet.iter_rows(min_col=1, max_col=max_col):
        for header, cell in zip(order, row):
            cell.value = header
            cell.alignment = Alignment(horizontal='center')
            
    for i in range(1, NUM_DEBTS + 1):
        data = []
        value = random.randint(1, 100000)
        debt_type = random.randint(1, 4)
        data.extend([i, value, description, debt_type, estudiante_fk])

        letter = get_column_letter(len(data))
        row_target = sheet.max_row + 1
        for row in sheet[f"A{row_target}:{letter}{row_target}"]:
            for attr, value, cell in zip(order, data, row):
                cell.value = str(value)
                cell.alignment = Alignment(horizontal='center')


def main():
    try:
        wb = openpyxl.load_workbook('Debts.xlsx')
    except FileNotFoundError:
        wb = openpyxl.Workbook()
    ws = wb.active
    # pepe = Personer(NUM_STUDENTS, wb)
    # fill_grades(NUM_GRADES, ws)
    generate_debts(ws)
    wb.save('Debts.xlsx')


if __name__ == "__main__":
    main()

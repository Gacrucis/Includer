import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
import numpy as np
import os
import random
from Names import man_names as men
from Names import woman_names as women

NUM_STUDENTS = 500


def fill_people(sheet):
    """ write people attrs into a given worksheet """
    fields = [
        "persona_id",
        "nombre",
        "identificacion",
        "celular",
        "direccion_fk",
        "sexo_fk",
        "tipo_identificacion_fk"]

    men_names = random.sample(men, int(np.ceil(2 * NUM_STUDENTS / 3)))
    men_names = [(name, 1) for name in men_names]
    women_names = random.sample(women, int(np.ceil(NUM_STUDENTS / 3)))
    women_names = [(name, 2) for name in women_names]

    #join lists
    names = men_names + women_names
    random.shuffle(names)

    #get last coord
    last_letter = get_column_letter(len(fields))
    last_cell_coord = last_letter + str(NUM_STUDENTS + 1)

    for cell, header in zip(sheet.iter_cols(0, len(fields)), fields):
        cell[0].value = header
        cell.alignment = Alignment(horizontal='center')

    for index, row in enumerate(sheet['A2':last_cell_coord]):
        data = []
        name, sexo_id = names[index]
        id_num = random.randrange(1000000000, 9999999999)
        phone = '3' + str(random.randrange(100000000, 999999999))
        address = index  # TODO: make direciton address more realistic
        id_type = random.randrange(0, 3)
        data.extend([index, name, id_num, phone, address, sexo_id, id_type])

        #iter cols
        for cell, field_value in zip(row, data):
            cell.value = str(field_value)
            cell.alignment = Alignment(horizontal='center')

def main():
    try:
        wb = openpyxl.load_workbook('people.xlsx')
    except FileNotFoundError:
        wb = openpyxl.Workbook()
    ws = wb.active
    fill_people(ws)
    wb.save('people.xlsx')


if __name__ == "__main__":
    main()

import openpyxl as xl
import psycopg2 as pc

def main():

    conn = pc.connect(
        dbname='bkfqvmiu',
        user='bkfqvmiu',
        password='kbc0-qYKx_NKBooqfoaf_xSoFYTyfaEb',
        host='lallah.db.elephantsql.com'
    )

    cursor = conn.cursor()

if __name__ == "__main__":
    main()

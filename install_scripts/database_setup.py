import pymysql


def create_database():

    try:
        conn = pymysql.connect(host='localhost', user='root', password='root')
        conn.cursor().execute('create database etl')
    except pymysql.Error as e:
        print(e)


if __name__ == '__main__':
    create_database()

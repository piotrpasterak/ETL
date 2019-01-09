"""Tiny module for create database during installation process.

Note:
    Expected is that in database user "root" with password 'root' exists.
    Mysql is required.

"""
import pymysql


def create_database():
    """Just create etl database (without tables).
    """

    try:
        conn = pymysql.connect(host='localhost', user='root', password='root')
        conn.cursor().execute('create database etl')
    except pymysql.Error as e:
        print(e)


if __name__ == '__main__':
    create_database()

import sqlite3
from config import db_name

def create_table():
        con = sqlite3.connect(db_name)
        cursor = con.execute('''
        CREATE TABLE IF NOT EXISTS user (
        id INTEGER, 
        role TEXT
        )
        ''')
        con.commit()
        con.close()

class User:
    @staticmethod
    def add_user(id):
        con = sqlite3.connect(db_name)
        cursor_object = con.execute(f"""
                INSERT OR REPLACE INTO user (id) 
                VALUES ('{id}')
                """)
        con.commit()
        con.close()

    @staticmethod
    def add_role_to_user(id, role):
        con = sqlite3.connect(db_name)
        cursor_object = con.execute(f"""
                UPDATE user 
                SET role = '{role}'
                WHERE id = '{id}'
                """)
        con.commit()
        con.close()

    @staticmethod
    def get_role_by_id(id):
        con = sqlite3.connect(db_name)
        cursor_object = con.execute(f"""
                                    SELECT role
                                    FROM user
                                    WHERE id = {id}
                                    """)

        return cursor_object.fetchone()[0]

    def get_role_by_id(id):
        con = sqlite3.connect(db_name)
        cursor = con.cursor()
        cursor.execute("""
            SELECT role FROM user WHERE id = ?
        """, (id,))
        result = cursor.fetchone()
        return result[0] if result else None
        con.close()
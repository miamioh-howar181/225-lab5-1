import sqlite3

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def clear_test_tasks():
    db = connect_db()
    db.execute("DELETE FROM tasks WHERE description LIKE 'Test Task %'")
    db.commit()
    print('Test tasks cleared from the database.')
    db.close()

if __name__ == '__main__':
    clear_test_tasks()

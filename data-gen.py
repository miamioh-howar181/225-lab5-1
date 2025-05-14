import sqlite3

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def generate_test_tasks(num_tasks):
    db = connect_db()
    for i in range(num_tasks):
        desc = f'Test Task {i}'
        db.execute('INSERT INTO tasks (description, status) VALUES (?, ?)', (desc, 'Pending'))
    db.commit()
    print(f'{num_tasks} test tasks added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_tasks(10)

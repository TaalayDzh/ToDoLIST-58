import sqlite3
from db import queries
from config import path_db


def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_TASK)
    print('База данных подключена!')
    conn.commit()
    conn.close()

def add_task(task):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASK, (task, ))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def get_tasks(filter_type='all'):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    # cursor.execute(queries.SELECT_TASK)
    if filter_type == 'completion':
        cursor.execute(queries.SELECT_TASK_COMPLETION)
    elif filter_type == 'uncompletion':
        cursor.execute(queries.SELECT_TASK_UNCOMPLETION)
    else:
        cursor.execute(queries.SELECT_TASK)

    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_tasks(task_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK,(task_id, ))
    conn.commit()
    conn.close()

def update_tasks(new_task=None, task_id=None, completion=None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    
    if new_task is not None and task_id is not None:
        cursor.execute(queries.UPDATE_TASK, (new_task, task_id))
    if completion is not None and task_id is not None:
        cursor.execute('UPDATE tasks SET completion = ? WHERE id = ?', (completion, task_id))   
    conn.commit()
    conn.close()

def delete_all():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_ALL_TASKS)
    conn.commit()
    conn.close()







CREATE_TABLE_TASK = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        completion INTEGER DEFAULT 0
    )
"""

INSERT_TASK = 'INSERT INTO tasks (task) VALUES (?)'
SELECT_TASK = 'SELECT id, task, completion FROM tasks'
SELECT_TASK_COMPLETION = 'SELECT id, task, completion FROM tasks WHERE completion = 1'
SELECT_TASK_UNCOMPLETION = 'SELECT id, task, completion FROM tasks WHERE completion = 0'
UPDATE_TASK = 'UPDATE tasks SET task = ? WHERE id = ?'
DELETE_TASK = 'DELETE FROM tasks WHERE id = ?'
DELETE_ALL_TASKS = 'DELETE FROM tasks'


from db import Database

class TaskNovaManager:
    def __init__(self):
        self.db = Database()

    def add_task(self, task, due_date, priority, user_id):
        query = """
        INSERT INTO tasks (task, status, due_date, priority, user_id)
        VALUES (%s, 'Pending', %s, %s, %s)
        """
        self.db.execute(query, (task, due_date, priority, user_id))

    def get_tasks(self, user_id):
        query = """
        SELECT id, task, status, due_date, priority
        FROM tasks
        WHERE user_id=%s
        ORDER BY due_date
        """
        return self.db.fetch(query, (user_id,))

    def complete_task(self, task_id, user_id):
        query = """
        UPDATE tasks SET status='Completed'
        WHERE id=%s AND user_id=%s
        """
        self.db.execute(query, (task_id, user_id))

    def delete_task(self, task_id, user_id):
        query = """
        DELETE FROM tasks
        WHERE id=%s AND user_id=%s
        """
        self.db.execute(query, (task_id, user_id))

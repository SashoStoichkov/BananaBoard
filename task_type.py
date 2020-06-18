from database import DB


class TaskType:
    def __init__(self, title):
        self.title = title

    def create(self):
        with DB() as db:
            values = (None, self.title)

            db.execute(
                '''
                    INSERT INTO task_types
                    VALUES (?, ?)
                ''', values
            )

            return self

    @staticmethod
    def get_all_types():
        with DB() as db:
            return db.execute(
                '''
                    SELECT * FROM task_types
                '''
            ).fetchall()

    @staticmethod
    def get_task_type_by_title(title):
        if not title:
            return None

        with DB() as db:
            return db.execute(
                '''
                    SELECT * FROM task_types
                    WHERE title = ?
                ''', (title,)
            ).fetchone()

    @staticmethod
    def get_task_type_title_by_id(task_type_id):
        if not task_type_id:
            return None

        with DB() as db:
            return db.execute(
                '''
                    SELECT title FROM task_types
                    WHERE id = ?
                ''', (str(task_type_id),)
            ).fetchone()[0]

    @staticmethod
    def update_task_type_title_for_id(task_type_id, new_title):
        if not task_type_id:
            return None

        with DB() as db:
            row = db.execute(
                '''
                    SELECT * FROM task_types
                    WHERE id = ?
                ''', (str(task_type_id),)
            ).fetchone()

            if row:
                db.execute(
                    '''
                        UPDATE task_types
                        SET title = ?
                        WHERE id = ?
                    ''', (new_title, str(task_type_id),)
                )

            else:
                return False

    def delete(self):
        with DB() as db:
            db.execute(
                '''
                    DELETE FROM task_types
                    WHERE title = ?
                ''', (self.title,)
            )

            return self

from database import DB


class Task:
    def __init__(self, title, content, task_status_id, task_type_id):
        this.id = None
        this.title = title
        this.content = content
        this.task_status_id = task_status_id
        this.task_type_id = task_type_id

    def create(self, user_id):
        with DB() as db:
            values = (
                None, self.title, self.content,
                self.task_status_id, self.task_type_id
            )

            db.execute(
                '''
                    INSERT INTO tasks
                    VALUES (?, ?, ?, ?, ?)
                ''', values
            )

            id = db.execute(
                '''
                    SELECT id FROM tasks
                    WHERE tasks.title = ?
                ''', (self.title,)
            ).fetchone()

            db.execute(
                '''
                    INSERT INTO user_tasks
                    VALUES (?, ?)
                ''', (user_id, id)
            )

            return self

    @staticmethod
    def display_all(user_id):
        with DB() as db:
            return db.execute(
                '''
                    SELECT tasks.title, tasks.content, task_types.title
                    FROM tasks
                        INNER JOIN task_types
                            ON tasks.task_type_id = task_type.id
                        INNER JOIN user_tasks
                            ON tasks.id = user_tasks.task_id
                        INNER JOIN users
                            ON user_tasks.user_id = users.id
                    WHERE users.id = ?
                ''', (user_id,)
            ).fetchall()

    @staticmethod
    def count_all(user_id):
        with DB() as db:
            return db.execute(
                '''
                    SELECT COUNT(user_tasks.task_id) FROM user_tasks
                    WHERE users.id = ?
                ''', (user_id,)
            ).fetchone()

    @staticmethod
    def display_by_status(user_id, status_id):
        with DB() as db:
            return db.execute(
                '''
                    SELECT tasks.title, tasks.content, task_types.title
                    FROM tasks
                        INNER JOIN task_types
                            ON tasks.task_type_id = task_type.id
                        INNER JOIN user_tasks
                            ON tasks.id = user_tasks.task_id
                        INNER JOIN users
                            ON user_tasks.user_id = users.id
                    WHERE users.id = ? AND tasks.task_status_id = ?
                ''', (user_id, status_id)
            ).fetchall()

    @staticmethod
    def display_by_type(user_id, task_type):
        with DB() as db:
            return db.execute(
                '''
                    SELECT tasks.title, tasks.content, task_types.title
                    FROM tasks
                        INNER JOIN task_types
                            ON tasks.task_type_id = task_type.id
                        INNER JOIN user_tasks
                            ON tasks.id = user_tasks.task_id
                        INNER JOIN users
                            ON user_tasks.user_id = users.id
                    WHERE users.id = ? AND task_types.title = ?
                ''', (user_id, task_type)
            ).fetchall()

    @staticmethod
    def select_by_title(user_id, title):
        if not title:
            return None

        with DB() as db:
            row = db.execute(
                '''
                    SELECT tasks.title, tasks.content,
                        tasks.task_type_id, tasks.task_status_id
                    FROM tasks
                        INNER JOIN user_tasks
                            ON tasks.id = user_tasks.task_id
                    WHERE user_tasks.user_id = ? AND tasks.title = ?
                ''', (user_id, title)
            ).fetchone()

            if row:
                return Task(*row)
            else:
                return False

    @staticmethod
    def edit_content(task_id, content):
        if not content:
            return None

        with DB() as db:
            row = db.execute(
                '''
                    SELECT * FROM tasks
                    WHERE id = ?
                ''', (task_id,)
            ).fetchone()

            if row:
                db.execute(
                    '''
                        UPDATE tasks
                        SET content = ?
                        WHERE id = ?
                    ''', (content, task_id)
                )

            else:
                return False

    @staticmethod
    def edit_title(task_id, title):
        if not title:
            return None

        with DB() as db:
            row = db.execute(
                '''
                    SELECT * FROM tasks
                    WHERE id = ?
                ''', (task_id,)
            ).fetchone()

            if row:
                db.execute(
                    '''
                        UPDATE tasks
                        SET title = ?
                        WHERE id = ?
                    ''', (title, task_id)
                )

            else:
                return False

    @staticmethod
    def edit_type(task_id, type_id):
        if not type_id:
            return None

        with DB() as db:
            row = db.execute(
                '''
                    SELECT * FROM tasks
                    WHERE id = ?
                ''', (task_id,)
            ).fetchone()

            if row:
                db.execute(
                    '''
                        UPDATE tasks
                        SET task_type_id = ?
                        WHERE id = ?
                    ''', (type_id, task_id)
                )

            else:
                return False

    @staticmethod
    def edit_status(task_id, status_id):
        if not status_id:
            return None

        with DB() as db:
            row = db.execute(
                '''
                    SELECT * FROM tasks
                    WHERE id = ?
                ''', (task_id,)
            ).fetchone()

            if row:
                db.execute(
                    '''
                        UPDATE tasks
                        SET task_status_id = ?
                        WHERE id = ?
                    ''', (status_id, task_id)
                )

            else:
                return False

    def delete(self):
        with DB() as db:
            db.execute(
                '''
                    DELETE FROM tasks
                    WHERE title = ?
                ''', (self.title,)
            )

            return self

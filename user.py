import hashlib
from database import DB


class User:
    def __init__(self, username, email):
        self.id = None
        self.username = username
        self.email = email
        self.password = None

    def create(self, password):
        with DB() as db:
            encr_password = User.encrypt_password(password)
            values = (None, self.username, encr_password, self.email)
            db.execute(
                '''
                    INSERT INTO users
                    VALUES (?, ?, ?, ?)
                ''', values
            )

            return self

    @staticmethod
    def encrypt_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def verify_password(password, email):
        with DB() as db:
            passwd = db.execute(
                '''
                    SELECT password FROM users
                    WHERE email = ?
                ''', (email,)
            ).fetchone()[0]

        return passwd ==\
            hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def get_username_by_id(id):
        with DB() as db:
            return db.execute(
                '''
                    SELECT name FROM users
                    WHERE id = ?
                ''', (id,)
            ).fetchone()[0]

    @staticmethod
    def get_user_by_id(user_id):
        if not user_id:
            return None

        with DB() as db:
            row = db.execute(
                '''
                    SELECT name, email FROM users
                    WHERE id = ?
                ''', (user_id,)
            ).fetchone()

            if row:
                return User(*row)

            return False

    @staticmethod
    def get_user_by_username(username):
        if not username:
            return None

        with DB() as db:
            row = db.execute(
                '''
                    SELECT name, email FROM users
                    WHERE name = ?
                ''', (username,)
            ).fetchone()

            if row:
                return User(*row)

            return False

    @staticmethod
    def get_user_by_email(email):
        if not email:
            return None

        with DB() as db:
            row = db.execute(
                '''
                    SELECT name, email FROM users
                    WHERE email = ?
                ''', (email,)
            ).fetchone()

            if row:
                return User(*row)

            return False

    @staticmethod
    def update_password_for_email(email, new_password):
        if not email:
            return None

        with DB() as db:
            row = db.execute(
                '''
                    SELECT * FROM users
                    WHERE email = ?
                ''', (email,)
            ).fetchone()

            if row:
                encr_password = User.encrypt_password(new_password)
                db.execute(
                    '''
                        UPDATE users
                        SET password = ?
                        WHERE email = ?
                    ''', (encr_password, email,)
                )

            else:
                return False

    @staticmethod
    def update_username_for_email(email, new_username):
        if not email:
            return None

        with DB() as db:
            row = db.execute(
                '''
                    SELECT * FROM users
                    WHERE email = ?
                ''', (email,)
            ).fetchone()

            if row:
                db.execute(
                    '''
                        UPDATE users
                        SET name = ?
                        WHERE email = ?
                    ''', (new_username, email,)
                )

            else:
                return False

    @staticmethod
    def update_email_for_email(email, new_email):
        if not email:
            return None

        with DB() as db:
            row = db.execute(
                '''
                    SELECT * FROM users
                    WHERE email = ?
                ''', (email,)
            ).fetchone()

            if row:
                db.execute(
                    '''
                        UPDATE users
                        SET email = ?
                        WHERE email = ?
                    ''', (new_email, email,)
                )

            else:
                return False

    def delete(self):
        with DB() as db:
            db.execute(
                '''
                    DELETE FROM users
                    WHERE email = ?
                ''', (self.email,)
            )

            return self

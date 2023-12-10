import aiosqlite

class DataBase:
    def __init__(self, db_file="data/users.db"):
        self.db_file = db_file

    async def create_table(self) -> None:
        """
        Creates table which contains user's information:
        user_id,
        name,
        age,
        gender,
        look_for,
        description,
        picture_id,
        likes,
        viewed_profiles.
        """
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    looking_for TEXT NOT NULL,
                    description TEXT,
                    picture_id TEXT,
                    likes INTEGER NOT NULL,
                    viewed_profiles TEXT
                )
            """)
            await db.commit()

    async def add_user(self, user_id: int, name: str, age: int, gender: str, looking_for: str, description: str, picture_id: str, likes: int) -> None:
        """
        Adds user to table.
        """
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("""
                INSERT INTO users (
                    user_id, name, age, gender, looking_for, description, picture_id, likes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, name, age, gender, looking_for, description, picture_id, likes))
            await db.commit()

    async def get_user(self, user_id: int):
        """
        Gets user from table by user_id.
        """
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                return await cursor.fetchone()

    async def user_exists(self, user_id: int) -> bool:
        """
        Checks if user exists in table and returns bool expression.
        """
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)) as cursor:
                return await cursor.fetchone() is not None

    async def delete_user(self, user_id: int) -> None:
        """
        Deletes user from table
        """
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            await db.commit()

    async def find_profiles(self, user_id: int):
        """
        Searches for suitable profiles for the user based on his preferences and already viewed profiles.

        This function searches the user database to find profiles that match the search criteria
        user (gender, who is looking for, age). The feature also excludes already viewed profiles to avoid repetitions.
        """

        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute("SELECT gender, looking_for, viewed_profiles, age FROM users WHERE user_id = ?",
                                  (user_id,)) as cursor:
                user_data = await cursor.fetchone()

            if not user_data:
                return -1

            user_gender, user_looking_for, viewed, user_age = user_data
            viewed_profiles = set(viewed.split(',')) if viewed else set()

            placeholders = ','.join('?' for _ in viewed_profiles)
            query = f"""
                SELECT user_id FROM users
                WHERE gender = ? AND looking_for = ? AND user_id != ?
                AND user_id NOT IN ({placeholders})
                ORDER BY ABS(age - ?)
                LIMIT 1
            """
            params = [user_looking_for, user_gender, user_id] + list(viewed_profiles) + [user_age]
            async with db.execute(query, params) as cursor:
                profile = await cursor.fetchone()

            if profile:
                new_viewed = ','.join(list(viewed_profiles) + [str(profile[0])])
                await db.execute("UPDATE users SET viewed_profiles = ? WHERE user_id = ?", (new_viewed, user_id))
                await db.commit()
                return profile[0]

            return -1

    async def increment_like(self, user_id):
        """
        Increments amount of likes by user_id.
        """
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute("SELECT likes FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()
                if result is None:
                    return False

            current_likes = result[0]

            await db.execute("UPDATE users SET likes = ? WHERE user_id = ?", (current_likes + 1, user_id))
            await db.commit()
            return True
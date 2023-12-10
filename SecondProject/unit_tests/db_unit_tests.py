import aiosqlite
from data.database import DataBase

class TestDataBase():

    async def asyncSetUp(self):
        self.db = DataBase("../data/test_users.db")
        await self.db.create_table()

    async def test_add_and_get_user(self):
        await self.db.add_user(1, "Test User", 25, "male", "female", "Test description", "test_pic_id", 0)
        user = await self.db.get_user(1)
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "Test User")

    async def test_user_exists(self):
        exists = await self.db.user_exists(1)
        self.assertTrue(exists)
        not_exists = await self.db.user_exists(2)
        self.assertFalse(not_exists)

    async def test_increment_like(self):
        success = await self.db.increment_like(1)
        self.assertTrue(success)
        user = await self.db.get_user(1)
        self.assertEqual(user[7], 1)

    async def test_delete_user(self):
        await self.db.delete_user(1)
        user = await self.db.get_user(1)
        self.assertIsNone(user)

    async def asyncTearDown(self):
        await aiosqlite.connect("../data/test_users.db").execute("DROP TABLE users")
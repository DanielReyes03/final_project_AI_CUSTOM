import unittest

from backend.context_store import ContextStore


class TestContextStore(unittest.TestCase):
    def setUp(self):
        self.store = ContextStore()

    def test_save_returns_true(self):
        result = self.store.save("ana", "style", "formal")
        self.assertTrue(result)

    def test_save_stores_key_value(self):
        self.store.save("ana", "style", "formal")
        context = self.store.list_for_user("ana")
        self.assertIn({"key": "style", "value": "formal"}, context)

    def test_list_empty_for_new_user(self):
        context = self.store.list_for_user("usuario_inexistente")
        self.assertEqual(context, [])

    def test_save_updates_existing_key(self):
        self.store.save("ana", "audience", "principiante")
        self.store.save("ana", "audience", "experto")
        context = self.store.list_for_user("ana")
        keys = [item["key"] for item in context]
        self.assertEqual(keys.count("audience"), 1)
        self.assertIn({"key": "audience", "value": "experto"}, context)

    def test_multiple_users_isolated(self):
        self.store.save("ana", "style", "formal")
        self.store.save("luis", "style", "informal")
        ana_context = self.store.list_for_user("ana")
        luis_context = self.store.list_for_user("luis")
        self.assertIn({"key": "style", "value": "formal"}, ana_context)
        self.assertIn({"key": "style", "value": "informal"}, luis_context)
        self.assertNotIn({"key": "style", "value": "informal"}, ana_context)
        self.assertNotIn({"key": "style", "value": "formal"}, luis_context)

    def test_multiple_keys_same_user(self):
        self.store.save("ana", "audience", "principiante")
        self.store.save("ana", "style", "con analogias")
        self.store.save("ana", "language", "espanol")
        context = self.store.list_for_user("ana")
        self.assertEqual(len(context), 3)
        keys = [item["key"] for item in context]
        self.assertIn("audience", keys)
        self.assertIn("style", keys)
        self.assertIn("language", keys)


if __name__ == "__main__":
    unittest.main()

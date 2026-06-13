import unittest

from backend.cag import apply_context


class TestApplyContext(unittest.TestCase):
    def test_no_context_returns_base_answer(self):
        result = apply_context("ana", "Que es CAG?", "Respuesta base.", context_items=None)
        self.assertEqual(result["answer"], "Respuesta base.")
        self.assertEqual(result["context_used"], [])

    def test_context_answer_contains_value(self):
        context_items = [{"key": "audience", "value": "explicar como principiante"}]
        result = apply_context("luis", "Que es CAG?", "Respuesta base.", context_items)
        self.assertIn("explicar como principiante", result["answer"])

    def test_context_used_contains_key(self):
        context_items = [{"key": "audience", "value": "explicar como principiante"}]
        result = apply_context("luis", "Que es CAG?", "Respuesta base.", context_items)
        self.assertIn("audience", result["context_used"])

    def test_empty_context_list(self):
        result = apply_context("ana", "Que es RAG?", "Respuesta base.", context_items=[])
        self.assertEqual(result["answer"], "Respuesta base.")
        self.assertEqual(result["context_used"], [])


if __name__ == "__main__":
    unittest.main()

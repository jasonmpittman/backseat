import unittest

class TestMethods(unittest.TestCase):
    
    def test_comp_true(self):
        self.assertTrue(10 > 5)

    def test_comp_false(self):
        self.assertFalse(10 < 5)
    
    def test_comp_none(self):
        self.assertIsNone(print())

class TestAdd(unittest.TestCase):
    def test_correct(self):
        self.assertEqual(5+5, 10)
        

    def test_incorrect(self):
        self.assertNotEqual(4+5, 10)
    

if __name__ == "__main--":
    unittest.main()

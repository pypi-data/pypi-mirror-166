from empty import *
import unittest

class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(empty("Hello World"), False, "Not empty string")
        self.assertEqual(empty(""), True,"Empty string")
        self.assertEqual(empty(20), False, "Not empty int")
        self.assertEqual(empty(0), True, "Empty int")
        self.assertEqual(empty(20.5), False, "Not empty float")
        self.assertEqual(empty(0.0000), True, "Empty float")
        self.assertEqual(empty(1j), False, "Not empty complex")
        self.assertEqual(empty(0), True, "Empty complex")
        self.assertEqual(empty(["apple", "banana", "cherry"]), False, "Not empty list")
        self.assertEqual(empty([]), True, "Empty list")
        self.assertEqual(empty(("apple", "banana", "cherry")), False, "Not empty tuple")
        self.assertEqual(empty(()), True, "Empty tuple")
        self.assertEqual(empty({"name" : "John", "age" : 36}), False, "Not empty dict")
        self.assertEqual(empty({}), True, "Empty dict")
        self.assertEqual(empty({"apple", "banana", "cherry"}), False, "Not empty set")
        self.assertEqual(empty(set()), True, "Empty set")
        self.assertEqual(empty(True), False, "Not empty bool")
        self.assertEqual(empty(False), True, "Empty bool")
        self.assertEqual(empty(b"Hello"), False, "Not empty byte string")
        self.assertEqual(empty(b""), True, "Empty byte string")
        self.assertEqual(empty(b"Hello"), False, "Not empty byte string")
        self.assertEqual(empty(b""), True, "Empty byte string")
        self.assertEqual(empty(None), True)
        
if __name__ == '__main__':
    unittest.main()
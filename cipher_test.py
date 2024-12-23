import unittest
from cipher import Cipher  # Assuming your file is named cipher.py

class TestCipher(unittest.TestCase):

    def setUp(self):
        self.cipher = Cipher()

    # Tests for encode_bacon
    def test_encode_bacon_valid(self):
        self.assertEqual(self.cipher.encode_bacon("hello", "a", "b"), "baabb abaaa ababb ababb abbbb")
        self.assertEqual(self.cipher.encode_bacon("WORLD", "x", "y"), "yyyyx ybbbb yxbyb yxbbb yxxax")
        self.assertEqual(self.cipher.encode_bacon("Python", "A", "B"), "BABBB ABBAB YBABB YBAAB ABBAB ABBBB")
        self.assertEqual(self.cipher.encode_bacon("Test 123", "m", "n"), "nnnnm mmmmm mnmnn nmmmm m")
        self.assertEqual(self.cipher.encode_bacon("Hello World!", "a", "z"), "aazzz aazaa azazz azazz azzza zazza azzza zaaaz azazz aaazz")

    def test_encode_bacon_invalid_letters(self):
        with self.assertRaises(ValueError):
            self.cipher.encode_bacon("test", "12", "a")
        with self.assertRaises(ValueError):
            self.cipher.encode_bacon("test", "a", "bcd")

    def test_encode_bacon_non_alpha_letters(self):
        with self.assertRaises(ValueError):
            self.cipher.encode_bacon("test", "1", "2")

    def test_encode_bacon_equal_letters(self):
        with self.assertRaises(ValueError):
            self.cipher.encode_bacon("test", "a", "a")

    def test_encode_bacon_reverse_order(self):
        with self.assertRaises(ValueError):
            self.cipher.encode_bacon("test", "z", "a")

    # Tests for decode_bacon ... (similar structure as above)
    def test_decode_bacon_valid(self):
        self.assertEqual(self.cipher.decode_bacon("aabbb aabaa ababb ababb abbba", "a", "b"), "hello")
        self.assertEqual(self.cipher.decode_bacon("a", "a", "b"), "a")
        self.assertEqual(self.cipher.decode_bacon("yyyyx ybbbb yxbyb yxbbb yxxax", "x", "y"), "world")
        self.assertEqual(self.cipher.decode_bacon("BABBB ABBAB YBABB YBAAB ABBAB ABBBB", "A", "B"), "python")
        self.assertEqual(self.cipher.decode_bacon("ykkyy kkyyy kykkk ykkyk kykkk ykkyk kkkkk kkkky kkkkk kkkyk kyyyk kyyky kyykk kkykk ykkyk ykkyk kkkkk kkyyk kkykk", "k", "y"), "helloworld")

    def test_decode_bacon_invalid_letters(self):
        with self.assertRaises(ValueError):
            self.cipher.decode_bacon("test", "12", "a")
            self.cipher.decode_bacon("test", "a", "a")

    # ... (Continue with tests for other methods in a similar pattern)
    def test_encode_caesar_valid(self):
        encoded_msg = self.cipher.encode_caesar("Hello world!", 7)
        self.assertEqual(encoded_msg, "Olssv dvysk!")

        encoded_msg = self.cipher.encode_caesar("This is a Caesar cipher!", 26)
        self.assertEqual(encoded_msg, "This is a Caesar cipher!")

        encoded_msg = self.cipher.encode_caesar("Negative shift.", -10)
        self.assertEqual(encoded_msg, "Duwqjylu ixyvj.")

        encoded_msg = self.cipher.encode_caesar("Python is fun...", 1)
        self.assertEqual(encoded_msg, "Qzuipo jt gvo...")

        encoded_msg = self.cipher.encode_caesar("No shift.", 0)
        self.assertEqual(encoded_msg, "No shift.")
    
    def test_encode_caesar_invalid(self):
        with self.assertRaises(TypeError):
            self.cipher.encode_caesar("test", 0.5)

    def test_decode_caesar_valid(self):
        decoded_msg = self.cipher.decode_caesar("Olssv dvysk!", 7)
        self.assertEqual(decoded_msg, "Hello world!")

        decoded_msg = self.cipher.decode_caesar("This is a Caesar cipher!", 26)
        self.assertEqual(decoded_msg, "This is a Caesar cipher!")

        decoded_msg = self.cipher.decode_caesar("Duwqjylu ixyvj.", -10)
        self.assertEqual(decoded_msg, "Negative shift.")

        decoded_msg = self.cipher.decode_caesar("Qzuipo jt gvo...", 1)
        self.assertEqual(decoded_msg, "Python is fun...")

        decoded_msg = self.cipher.decode_caesar("No shift.", 0)
        self.assertEqual(decoded_msg, "No shift.")

    def test_decode_caesar_invalid(self):
        with self.assertRaises(TypeError):
            self.cipher.decode_caesar("Qzuipo jt gvo.", "14")

    # No exceptions thrown for the Complement cipher
    def test_encode_complement(self):
        encoded_message = self.cipher.encode_complement("Hello World!")
        self.assertEqual(encoded_message, "Svool Dliow!")

        encoded_message = self.cipher.encode_complement("Using a Complement cipher")
        self.assertEqual(encoded_message, "Fhrmt z Xlnkovnvmg xrksvi")

        encoded_message = self.cipher.encode_complement("test")
        self.assertEqual(encoded_message, "gvhg")

        encoded_message = self.cipher.encode_complement("")
        self.assertEqual(encoded_message, "")

        encoded_message = self.cipher.encode_complement("123")
        self.assertEqual(encoded_message, "123")

    def test_decode_complement(self):
        decoded_msg = self.cipher.decode_complement("Svool Dliow!")
        self.assertEqual(decoded_msg, "Hello World!")

        decoded_msg = self.cipher.decode_complement("Fhrmt z Xlnkovnvmg xrksvi")
        self.assertEqual(decoded_msg, "Using a Complement cipher")

        decoded_msg = self.cipher.decode_complement("gvhg")
        self.assertEqual(decoded_msg, "test")

        decoded_msg = self.cipher.decode_complement("")
        self.assertEqual(decoded_msg, "")

        decoded_msg = self.cipher.decode_complement("Gvhg 123")
        self.assertEqual(decoded_msg, "Test 123")

    def test_encode_vigenere_valid(self):
        encoded_msg = self.cipher.encode_vigenere("Hello world!", "KEY")
        self.assertEqual(encoded_msg, "Rijvs uyvjn!")

        encoded_msg = self.cipher.encode_vigenere("This is a Vigenere cipher!", "STEAM")
        self.assertEqual(encoded_msg, "Lams uk t Ziswgirq ubthqj!")

        encoded_msg = self.cipher.encode_vigenere("Using a lowercase key.", "xml")
        self.assertEqual(encoded_msg, "Retks l iahbdnxep hqj.")

        encoded_msg = self.cipher.encode_vigenere("The", "THE")
        self.assertEqual(encoded_msg, "Moi")

        encoded_msg = self.cipher.encode_vigenere("Short message.", "THISISASORTOFLONGKEY")
        self.assertEqual(encoded_msg, "Lowjb eekgrzs.")

    def test_encode_vigenere_invalid(self):
        with self.assertRaises(ValueError):
            self.cipher.encode_vigenere("Vigenere cipher test.", "Bad Key.")

    def test_decode_vigenere_valid(self):
        decoded_msg = self.cipher.decode_vigenere("Rijvs Uyvjn!", "KEY")
        self.assertEqual(decoded_msg, "Hello World!")

        decoded_msg = self.cipher.decode_vigenere("Lams uk t Ziswgirq ubthqj!", "STEAM")
        self.assertEqual(decoded_msg, "This is a Vigenere cipher!")

        decoded_msg = self.cipher.decode_vigenere("Retks l iahbdnxep hqj.", "xml")
        self.assertEqual(decoded_msg, "Using a lowercase key.")

        decoded_msg = self.cipher.decode_vigenere("Moi", "THE")
        self.assertEqual(decoded_msg, "The")

        decoded_msg = self.cipher.decode_vigenere("Lowjb eekgrzs.", "THISISASORTOFLONGKEY")
        self.assertEqual(decoded_msg, "Short message.")

    def test_decode_vigenere_invalid(self):
        with self.assertRaises(ValueError):
            self.cipher.decode_vigenere("Vskcnovc ic xfe liqt.", "A KEY")
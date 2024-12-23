import re

class Cipher:
    """A class implementing various classical crytographic ciphers.

    This class provides methods for Bacon, Viginere, lexicological complement,
    and Caesar ciphers. These methods encrypt and decrypt messages according
    to the aforementioned cipher algorithms.

    Class Constants:
        START_UPPER (int): ASCII value for uppercase 'A' (65)
        START_LOWER (int): ASCII value for lowercase 'a' (97)
        NUM_LETTERS (int): Number of letters in the English alphabet (26)
    """

    START_UPPER = 65
    START_LOWER = 97
    NUM_LETTERS = 26

    def encode_bacon(self, message: str, let1: str, let2: str) -> str:
        """Encode a message using Bacon's cipher.
        
        Converts each letter in the message to a 5-character binary representation
        using two specified letters. Non-alphabetic characters are removed and
        the message is converted to lowercase before encoding.

        Args:
            message (str): The text to encode.
            let1 (str): First letter for binary representation (represents 0).
            let2 (str): Second letter for binary representation (represents 1).

        Returns:
            str: The encoded message with binary representations using let1 and let2,
                 with each letter's encoding separated by spaces.

        Raises:
            ValueError: If letters are not single characters.
            ValueError: If letters are not alphabetical.
            ValueError: If letters are not unique.
            ValueError: If let1's position in alphabet is greater than let2's.
        """
        if len(let1) != 1 or len(let2) != 1:
            raise ValueError("Letters must be one character each.")
        
        if not let1.isalpha() and not let2.isalpha():
            raise ValueError("Letters must be alphabetical characters.")
        
        if let1 == let2:
            raise ValueError("Letters must be unique.")
        
        if ord(let1) > ord(let2):
            raise ValueError("The position of the first letter must be less than the position of the second letter. i.e. D comes before R.")
        
        encoded_message = ""
    
        message = re.sub("[^A-Za-z]", "", message).lower()
        
        for i in range(len(message)):
            dec = ord(message[i]) - self.START_LOWER

            binary_string = ""

            while dec != 0:
                binary_string = str(dec % 2) + binary_string
                dec //= 2

            binary_string = binary_string.replace("0", let1).replace("1", let2).rjust(5, let1)

            encoded_message += binary_string + " "

        return encoded_message.strip()

    def decode_bacon(self, message: str, let1: str, let2: str) -> str:
        """Decode a Bacon cipher encoded message.

        Converts groups of 5 characters (using the specified binary representation letters)
        back into their original alphabetic characters.

        Args:
            message (str): The encoded text to decode.
            let1 (str): First letter used in the encoding (represents 0).
            let2 (str): Second letter used in the encoding (represents 1).

        Returns:
            str: The decoded message.

        Raises:
            ValueError: If letters are not single characters.
            ValueError: If letters are not alphabetical.
            ValueError: If letters are not unique.
            ValueError: If let1's position in alphabet is greater than let2's.
            ValueError: If message contains letters other than let1 and let2.
        """
        if len(let1) != 1 or len(let2) != 1:
            raise ValueError("Letters must be one character each.")
        
        if not let1.isalpha() and not let2.isalpha():
            raise ValueError("Letters must be alphabetical characters.")
        
        if let1 == let2:
            raise ValueError("Letters must be unique.")
        
        if ord(let1) > ord(let2):
            raise ValueError("The position of the first letter must be less than the position of the second letter. i.e. D comes before R.")
        
        matches = re.findall(rf"[^{let1}{let2} ]", message)
        if matches:
            raise ValueError("The message does not contain only the specified letters.")
        
        decoded_message = ""

        message = re.sub("[^A-Za-z ]", "", message).strip()

        message_tokens = message.split(" ")

        for i in range(len(message_tokens)):
            binary_string = message_tokens[i].replace(let1, "0").replace(let2, "1")

            dec = 0
            curr_pow = len(binary_string) - 1
            for j in range(len(binary_string)):
                dec += int(binary_string[j]) * 2 ** curr_pow
                curr_pow -= 1

            dec += self.START_LOWER

            decoded_message += chr(dec)

        return decoded_message

    def encode_caesar(self, message: str, shift: int) -> str:
        """Encode a message using the Caesar cipher.

        Shifts each letter in the message by the specified number of positions in
        the alphabet. Preserves case and non-alphabetic characters.

        Args:
            message (str): The text to encode.
            shift (int): Number of positions to shift each letter (automatically wrapped to 0-25).

        Returns:
            str: The encoded message.

        Raises:
            TypeError: If shift is not an integer.
        """
        if not isinstance(shift, int):
            raise TypeError("Shift must be an integer value.")
        
        shift %= self.NUM_LETTERS
        encoded_message = ""

        for i in range(len(message)):
            if message[i].isupper():
                pos_let = ord(message[i]) - self.START_UPPER
                new_let = (pos_let + shift) % self.NUM_LETTERS + self.START_UPPER
                encoded_message += chr(new_let)
            elif message[i].islower():
                pos_let = ord(message[i]) - self.START_LOWER
                new_let = (pos_let + shift) % self.NUM_LETTERS + self.START_LOWER
                encoded_message += chr(new_let)
            else:
                encoded_message += message[i]

        return encoded_message
    
    def decode_caesar(self, message: str, shift: int) -> str:
        """Decode a Caesar cipher encoded message.

        Shifts each letter in the message backwards by the specified number of positions
        in the alphabet. Preserves case and non-alphabetic characters.

        Args:
            message (str): The encoded text to decode.
            shift (int): The shift value used in encoding.

        Returns:
            str: The decoded message.

        Raises:
            TypeError: If shift is not an integer.
        """
        if not isinstance(shift, int):
            raise TypeError("Shift must be an integer value.")
        
        shift %= self.NUM_LETTERS
        decoded_message = ""

        for i in range(len(message)):
            if message[i].isupper():
                pos_let = ord(message[i]) - self.START_UPPER
                new_let = (pos_let - shift) % self.NUM_LETTERS + self.START_UPPER
                decoded_message += chr(new_let)
            elif message[i].islower():
                pos_let = ord(message[i]) - self.START_LOWER
                new_let = (pos_let - shift) % self.NUM_LETTERS + self.START_LOWER
                decoded_message += chr(new_let)
            else:
                decoded_message += message[i]

        return decoded_message
    
    def encode_complement(self, message: str) -> str:
        """Encode a message using the lexicographical complement cipher.

        Replaces each letter with its complement in the alphabet (e.g., 'a' becomes 'z',
        'b' becomes 'y', etc.). Preserves case and non-alphabetic characters.

        Args:
            message (str): The text to encode.

        Returns:
            str: The encoded message.
        """
        encoded_message = ""

        for i in range(len(message)):
            if message[i].isupper():
                pos_let = ord(message[i]) - self.START_UPPER
                new_let = (self.NUM_LETTERS - pos_let - 1) % self.NUM_LETTERS + self.START_UPPER
                encoded_message += chr(new_let)
            elif message[i].islower():
                pos_let = ord(message[i]) - self.START_LOWER
                new_let = (self.NUM_LETTERS - pos_let - 1) % self.NUM_LETTERS + self.START_LOWER
                encoded_message += chr(new_let)
            else:
                encoded_message += message[i]

        return encoded_message
    
    def decode_complement(self, message: str) -> str:
        """Decode a lexicographical complement encoded message.

        This is identical to encoding since the complement cipher is its own inverse.

        Args:
            message (str): The encoded text to decode.

        Returns:
            str: The decoded message.
        """
        return self.encode_complement(message)

    def encode_vigenere(self, message: str, key: str) -> str:
        """Encode a message using the Vigenère cipher.

        Applies a polyalphabetic substitution using the provided key. The key is repeated
        as needed to match the message length. Preserves case and non-alphabetic characters.

        Args:
            message (str): The text to encode.
            key (str): The encryption key (must be alphabetic).

        Returns:
            str: The encoded message.

        Raises:
            ValueError: If key contains non-alphabetic characters.
        """
        key_index = 0
        encoded_msg = ""
        key = key.upper()

        if not key.isalpha():
            raise ValueError("Key must only contain letters.")

        for i in range(len(message)):
            if message[i].isalpha():
                if message[i].isupper():
                    pos_let = ord(message[i]) - self.START_UPPER
                    pos_key = ord(key[key_index]) - self.START_UPPER
                    char = (pos_let + pos_key) % self.NUM_LETTERS + self.START_UPPER
                    encoded_msg += chr(char)
                else:
                    pos_let = ord(message[i]) - self.START_LOWER
                    pos_key = ord(key[key_index]) - self.START_UPPER
                    char = (pos_let + pos_key) % self.NUM_LETTERS + self.START_LOWER
                    encoded_msg += chr(char)
                key_index = (key_index + 1) % len(key)
            else:
                encoded_msg += message[i]
        return encoded_msg

    def decode_vigenere(self, message: str, key: str) -> str:
        """Decode a Vigenère cipher encoded message.

        Reverses the polyalphabetic substitution using the provided key. The key is repeated
        as needed to match the message length. Preserves case and non-alphabetic characters.

        Args:
            message (str): The encoded text to decode.
            key (str): The key used for encoding (must be alphabetic).

        Returns:
            str: The decoded message.

        Raises:
            ValueError: If key contains non-alphabetic characters.
        """
        key_index = 0
        decoded_msg = ""
        key = key.upper()
        
        if not key.isalpha():
            raise ValueError("Key must only contain letters.")
        for i in range(len(message)):
            if message[i].isalpha():
                if message[i].isupper():
                    pos_let = ord(message[i]) - self.START_UPPER
                    pos_key = ord(key[key_index]) - self.START_UPPER
                    char = (pos_let - pos_key + 26) % self.NUM_LETTERS + self.START_UPPER
                    decoded_msg += chr(char)
                else:
                    pos_let = ord(message[i]) - self.START_LOWER
                    pos_key = ord(key[key_index]) - self.START_UPPER
                    char = (pos_let - pos_key + 26) % self.NUM_LETTERS + self.START_LOWER
                    decoded_msg += chr(char)
                key_index = (key_index + 1) % len(key)
            else:
                decoded_msg += message[i]
        return decoded_msg
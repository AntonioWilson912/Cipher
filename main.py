from cipher import Cipher
import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as tkMessage

class Window(tk.Tk):
    """
    A Tkinter GUI application for encoding and decoding messages 
    using the Vigenère cipher.

    This application allows users to input a message and a key, 
    select an action (encode or decode), and view the resulting 
    encoded or decoded message. It also provides options to copy 
    the output to the clipboard.

    Attributes:
        cipher (VigenereCipher): An instance of the VigenereCipher class.
        error (bool): A flag to indicate if there are errors in the input.
    """

    def __init__(self):
        """
        Initializes the main application window and its components.

        Sets up the layout, including labels, entry fields, buttons, 
        and event bindings. Configures the window properties such 
        as size, title, and background color.
        """
        super().__init__()

        self.cipher = Cipher()

        self.geometry("760x600")
        self.title("Vigenere Cipher")
        self.config(bg="black", padx=20, pady=20)
        self.resizable(False, False)

        # Label for action selection
        self.crypt_label = tk.Label(text="Action to Perform:")
        self.crypt_label.config(fg="white", bg="black")
        self.crypt_label.grid(row=0, column=0, pady=10, sticky="w")
        
        # Dropdown for selecting encoding or decoding
        crypt_list = ["Encode", "Decode"]
        self.selected_method = tk.StringVar(value=crypt_list[0])
        self.selected_method.trace_add("write", self.handle_method_change)

        self.crypt_select = tk.OptionMenu(self, self.selected_method, *crypt_list)
        self.crypt_select.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Message entry field
        self.message = tk.StringVar(value="")
        self.message_label = tk.Label(text="Message to Encode:", fg="white", bg="black")
        self.message_label.grid(row=1, column=0, sticky="nw")

        self.message_entry = tk.Text(self)
        self.message_entry.grid(row=1, column=1, padx=10)

        # Key entry field
        self.key = tk.StringVar(self)
        self.key_label = tk.Label(text="Key:", fg="white", bg="black")
        self.key_label.grid(row=2, column=0, pady=10, sticky="w")

        self.key_entry = tk.Entry(self)
        self.key_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Button to trigger encoding/decoding
        self.crypt_button = tk.Button(
            text="Watch the Magic!", 
            command=self.handle_cryption, 
            fg="black", 
            bg="white", 
            activebackground="white",
            highlightbackground="white",
            relief=tk.FLAT
        )
        self.crypt_button.grid(row=3, columnspan=2, padx=10, pady=10)

        # Output label
        self.output = tk.Label(text="Output")
        self.output.config(bg="black", font=tkFont.Font(family="Courier New", size=12, weight="bold"), wraplength=720, justify="left")
        self.output.grid(row=4, columnspan=2, sticky="w")

        # Button to copy output to clipboard
        self.copy_button = tk.Button(
            text="Copy Text",
            command=self.handle_copy,
            fg="black",
            bg="white",
            activebackground="white",
            highlightbackground="white",
            relief=tk.FLAT
        )
        self.copy_button.grid(row=5, pady=10, sticky="w")

        # Bind the Enter key to the handle_cryption method
        self.bind("<Return>", self.handle_cryption)

        self.error = True

    def handle_method_change(self, *args):
        """
        Update the message label based on the selected action.

        Changes the label to indicate whether the user is encoding 
        or decoding a message.
        """
        if self.selected_method.get() == "Encode":
            self.message_label.config(text="Message to Encode:")
        else:
            self.message_label.config(text="Message to Decode:")

    def handle_copy(self, *args):
        """
        Copy the output message to the clipboard.

        If there are no errors, the text from the output label is 
        copied to the clipboard, and a success message is displayed.
        If there are errors, an error message is shown.
        """
        if not self.error:
            message_to_copy = self.output.cget("text")
            colon_index = message_to_copy.index(":") + 2
            message_to_copy = message_to_copy[colon_index:]
            self.clipboard_clear()
            self.clipboard_append(message_to_copy)
            self.update()
            tkMessage.showinfo("Success!", "Message successfully copied!")
        else:
            tkMessage.showerror("Error!", "Please fix the errors with your message to copy!")

    def handle_cryption(self, *args):
        """
        Perform encoding or decoding based on user input.

        Retrieves the message and key from the entry fields and 
        either encodes or decodes the message based on the selected 
        action. Updates the output label with the result or an 
        error message if inputs are invalid.
        """
        message = self.message_entry.get("1.0", tk.END).strip()
        key = self.key_entry.get().strip()

        if len(message) == 0 and len(key) == 0:
            self.output.config(text="Must enter the message and the key.", fg="red")
            self.error = True
        elif len(key) == 0:
            self.output.config(text="Must enter the key.", fg="red")
            self.error = True
        elif len(message) == 0:
            self.output.config(text="Must enter the message.", fg="red")
            self.error = True
        else:
            if self.selected_method.get() == "Encode":
                self.output.config(text=f"Your encoded message: {self.cipher.encode_vigenere(message=message, key=key)}", fg="white")
            else:
                self.output.config(text=f"Your decoded message: {self.cipher.decode_vigenere(message=message, key=key)}", fg="white")
            self.error = False

if __name__ == "__main__":
    # Start the event loop
    window = Window()
    window.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os


class ImageEncryptionApp:

    def __init__(self, root):
        """Initialize the Image Encryption application with GUI components"""
        self.root = root
        self.root.title("Image Encryption Tool")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        self.root.configure(padx=20, pady=20)

        # Initialize image variables
        self.image = None
        self.original_image = None
        self.encrypted_image = None
        self.image_path = None
        self.display_image = None
        self.last_operation = None  # Track the last operation (encrypt or decrypt)

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface"""
        # Title
        title_label = ttk.Label(self.root,
                                text="Image Encryption/Decryption",
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Control frame
        control_frame = ttk.LabelFrame(self.root, text="Controls")
        control_frame.pack(fill="x", padx=5, pady=5)

        # Create a grid inside the control frame
        for i in range(2):
            control_frame.grid_columnconfigure(i, weight=1)

        # Method frame (left side)
        method_frame = ttk.Frame(control_frame)
        method_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Encryption method selection
        ttk.Label(method_frame, text="Encryption Method:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.encryption_method = tk.StringVar()
        self.encryption_method.set("add")  # Default method

        # Radio buttons for encryption methods in a frame
        methods_frame = ttk.Frame(method_frame)
        methods_frame.grid(row=0, column=1, sticky="w")

        self.add_radio = ttk.Radiobutton(methods_frame, text="Add Key", variable=self.encryption_method, value="add")
        self.add_radio.pack(side="left", padx=5)

        self.xor_radio = ttk.Radiobutton(methods_frame, text="XOR Key", variable=self.encryption_method, value="xor")
        self.xor_radio.pack(side="left", padx=5)

        self.swap_radio = ttk.Radiobutton(methods_frame, text="Swap Channels", variable=self.encryption_method, value="swap")
        self.swap_radio.pack(side="left", padx=5)

        # Encryption key
        ttk.Label(method_frame, text="Encryption Key:").grid(row=1, column=0,  sticky="w", padx=5, pady=5)
        key_frame = ttk.Frame(method_frame)
        key_frame.grid(row=1, column=1, sticky="w")

        self.image_key = ttk.Spinbox(key_frame, from_=1, to=255, width=5)
        self.image_key.pack(side="left")
        self.image_key.set(10)  # Default key value

        # Button frame (right side)
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=1, sticky="e", padx=10, pady=5)

        # Load image button
        self.load_button = ttk.Button(button_frame, text="Load Image", command=self.load_image, width=15)
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        # Encrypt image button
        self.encrypt_button = ttk.Button(button_frame, text="Encrypt Image", command=self.encrypt_image, width=15)
        self.encrypt_button.grid(row=0, column=1, padx=5, pady=5)
        self.encrypt_button.config(state="disabled")

        # Decrypt image button
        self.decrypt_button = ttk.Button(button_frame, text="Decrypt Image", command=self.decrypt_image, width=15)
        self.decrypt_button.grid(row=0, column=2, padx=5, pady=5)
        self.decrypt_button.config(state="disabled")

        # Save image button
        self.save_button = ttk.Button(button_frame, text="Save Image", command=self.save_image, width=15)
        self.save_button.grid(row=1, column=1, padx=5, pady=5)
        self.save_button.config(state="disabled")

        # Reset button
        self.reset_button = ttk.Button(button_frame, text="Reset to Original", command=self.reset_to_original, width=15)
        self.reset_button.grid(row=1, column=0, padx=5, pady=5)
        self.reset_button.config(state="disabled")

        # Image display frame
        self.image_frame = ttk.LabelFrame(self.root, text="Image Preview")
        self.image_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Image display
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(padx=10, pady=10)

        # Status label
        self.status_label = ttk.Label(self.root,
                                      text="Status: Ready to load an image",
                                      font=("Arial", 10))
        self.status_label.pack(pady=5, anchor="w")

        # Information frame
        info_frame = ttk.LabelFrame(self.root, text="Information")
        info_frame.pack(fill="x", padx=5, pady=5)

        # Info text
        info_text = """
        This application encrypts and decrypts images using various pixel manipulation techniques:
        
        1. Add Key: Adds the key value to each color channel (R,G,B) of every pixel
        2. XOR Key: Performs bitwise XOR operation with the key on each color channel
        3. Swap Channels: Rearranges the RGB channels (R→G, G→B, B→R) for encryption
        
        To use:
        - Load an image using the 'Load Image' button
        - Select an encryption method
        - Set an encryption key (for Add and XOR methods)
        - Click 'Encrypt Image' to see the encrypted result
        - Click 'Decrypt Image' to reverse the process
        - Use 'Reset to Original' to restore the original image
        - Save the result using the 'Save Image' button
        """

        info_label = ttk.Label(info_frame, text=info_text, wraplength=760, justify="left")
        info_label.pack(padx=10, pady=10)

    def load_image(self):
        """Load an image file for encryption/decryption"""
        try:
            # Open file dialog to select an image
            file_path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])

            if not file_path:  # User canceled
                return

            # Load and store the image
            self.image_path = file_path
            self.image = Image.open(file_path)

            # Convert to RGB mode if not already (handles PNG transparency)
            if self.image.mode != 'RGB':
                self.image = self.image.convert('RGB')

            # Store the original image
            self.original_image = self.image.copy()

            # Display image preview
            self.display_preview(self.image)

            # Update status and buttons
            self.set_status(f"Image loaded: {os.path.basename(file_path)}")
            self.encrypt_button.config(state="normal")
            self.decrypt_button.config(state="normal")
            self.reset_button.config(state="normal")
            self.save_button.config(state="disabled")

        except Exception as e:
            self.set_status(f"Error loading image: {str(e)}")
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def encrypt_image(self):
        """Encrypt the loaded image using selected pixel manipulation method"""
        if self.image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return

        try:
            # Get encryption key and method
            method = self.encryption_method.get()
            key = 0

            if method in ["add", "xor"]:
                try:
                    key = int(self.image_key.get())
                    if key < 1 or key > 255:
                        raise ValueError("Key must be between 1 and 255")
                except ValueError as e:
                    messagebox.showerror("Error",
                                         f"Invalid key value: {str(e)}")
                    return

            # Create a copy of the image for encryption
            img = self.image.copy()
            pixels = img.load()

            # Get image dimensions
            width, height = img.size

            # Process each pixel based on the selected method
            for y in range(height):
                for x in range(width):
                    # Get pixel RGB values
                    r, g, b = pixels[x, y]

                    # Initialize new RGB values
                    new_r, new_g, new_b = r, g, b

                    if method == "add":
                        # Add key to each channel
                        new_r = (r + key) % 256
                        new_g = (g + key) % 256
                        new_b = (b + key) % 256
                    elif method == "xor":
                        # XOR each channel with key
                        new_r = r ^ key
                        new_g = g ^ key
                        new_b = b ^ key
                    elif method == "swap":
                        # Swap channels (R->G, G->B, B->R)
                        new_r = g
                        new_g = b
                        new_b = r

                    # Update pixel with new values
                    pixels[x, y] = (new_r, new_g, new_b)

            # Store processed image as current image and encrypted image
            self.encrypted_image = img
            self.image = img.copy()

            # Display encrypted image
            self.display_preview(img)

            # Update status and buttons
            self.set_status(f"Image encrypted using {method.upper()} method!")
            self.save_button.config(state="normal")
            self.last_operation = "encrypt"

        except Exception as e:
            self.set_status(f"Encryption error: {str(e)}")
            messagebox.showerror("Error", f"Failed to encrypt image: {str(e)}")

    def decrypt_image(self):
        """Decrypt the encrypted image"""
        if self.image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return

        try:
            # Get encryption key and method
            method = self.encryption_method.get()
            key = 0

            if method in ["add", "xor"]:
                try:
                    key = int(self.image_key.get())
                    if key < 1 or key > 255:
                        raise ValueError("Key must be between 1 and 255")
                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid key value: {str(e)}")
                    return

            # Create a copy of the image for decryption
            img = self.image.copy()
            pixels = img.load()

            # Get image dimensions
            width, height = img.size

            # Process each pixel based on the selected method
            for y in range(height):
                for x in range(width):
                    # Get pixel RGB values
                    r, g, b = pixels[x, y]

                    # Initialize new RGB values
                    new_r, new_g, new_b = r, g, b

                    if method == "add":
                        # Subtract key from each channel
                        new_r = (r - key) % 256
                        new_g = (g - key) % 256
                        new_b = (b - key) % 256
                    elif method == "xor":
                        # XOR is its own inverse, so same operation as encryption
                        new_r = r ^ key
                        new_g = g ^ key
                        new_b = b ^ key
                    elif method == "swap":
                        # Reverse swap (R->B, G->R, B->G)
                        new_r = b
                        new_g = r
                        new_b = g
                    # Update pixel with new values
                    pixels[x, y] = (new_r, new_g, new_b)
            # Store processed image as current image and encrypted image
            self.encrypted_image = img
            self.image = img.copy()
            # Display decrypted image
            self.display_preview(img)
            # Update status and buttons
            self.set_status(f"Image decrypted using {method.upper()} method!")
            self.save_button.config(state="normal")
            self.last_operation = "decrypt"

        except Exception as e:
            self.set_status(f"Decryption error: {str(e)}")
            messagebox.showerror("Error", f"Failed to decrypt image: {str(e)}")

    def save_image(self):
        """Save the encrypted/decrypted image"""
        if self.encrypted_image is None:
            messagebox.showwarning("Warning", "No processed image to save")
            return

        try:
            # Open file dialog to save the image
            file_path = filedialog.asksaveasfilename(
                title="Save Image",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                           ("BMP files", "*.bmp")])

            if not file_path:  # User canceled
                return

            # Save the image
            self.encrypted_image.save(file_path)

            # Update status
            self.set_status(f"Image saved to: {os.path.basename(file_path)}")

        except Exception as e:
            self.set_status(f"Error saving image: {str(e)}")
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")

    def display_preview(self, image):
        """Display an image preview in the GUI"""
        # Resize image for preview if it's too large
        max_width, max_height = 750, 400
        img_width, img_height = image.size

        # Calculate aspect ratio
        aspect_ratio = img_width / img_height

        # Determine new dimensions while maintaining aspect ratio
        if img_width > max_width or img_height > max_height:
            if aspect_ratio > 1:  # Width > Height
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:  # Height > Width
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
        else:
            new_width, new_height = img_width, img_height
        # Create a resized copy for display
        preview = image.copy()
        preview.thumbnail((new_width, new_height))
        # Convert to PhotoImage for Tkinter
        photo = ImageTk.PhotoImage(preview)
        # Update image label
        self.display_image = photo  # Keep reference to prevent garbage collection
        self.image_label.config(image=photo)

    def reset_to_original(self):
        """Reset image to its original state"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "No original image available")
            return
        # Reset current image to original
        self.image = self.original_image.copy()
        # Display original image
        self.display_preview(self.image)
        # Update status
        self.set_status("Image reset to original state")

    def set_status(self, status):
        """Set the status label with the given status"""
        self.status_label.configure(text=f"Status: {status}")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = ImageEncryptionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

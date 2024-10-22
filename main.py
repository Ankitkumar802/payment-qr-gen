import tkinter as tk
from tkinter import messagebox, StringVar
import qrcode
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk

# Initialize global variable for QR label
qr_label = None

# Function to generate QR code
def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(f"{filename}.png")
    return f"{filename}.png"  # Return the filename

# Function to generate Barcode
def generate_barcode(data, filename):
    code128 = barcode.get('code128', data, writer=ImageWriter())
    code128.save(filename)  # Save barcode as an image
    return f"{filename}.png"  # Return the filename

# Function to generate Payment QR Code or Barcode
def generate_payment_code(payee, amount, filename):
    if not payee or not amount:
        messagebox.showerror("Error", "Payee (Phone number or UPI ID) and Amount are required!")
        return

    # Create UPI payment URL based on input
    payment_data = f"upi://pay?pa={payee}&am={amount}&cu=INR"

    # Check the selected type (QR Code or Barcode)
    if code_type.get() == "QR Code":
        return generate_qr_code(payment_data, filename)
    elif code_type.get() == "Barcode":
        return generate_barcode(payment_data, filename)

# Function to handle user choice and generate the payment code
def generate_code():
    amount = entry_amount.get()
    payee = entry_payee.get()
    filename = entry_filename.get()

    if filename and amount and payee:
        code_image = generate_payment_code(payee, amount, filename)
        
        # Display the generated code image
        display_code_image(code_image)
        clear_fields()  # Clear fields after generation
    else:
        messagebox.showerror("Error", "Please enter payee, amount, and filename for Payment Code.")

# Function to display the generated code in the GUI
def display_code_image(image_path):
    global qr_label  # Declare qr_label as global
    try:
        # Open the image and resize it
        img = Image.open(image_path)
        img.thumbnail((250, 250))  # Resize for display
        img = ImageTk.PhotoImage(img)

        # Clear the previous image if any
        if qr_label is not None:
            qr_label.destroy()

        # Create a label to display the code
        qr_label = tk.Label(root, image=img)
        qr_label.image = img  # Keep a reference to avoid garbage collection
        qr_label.grid(row=5, column=0, columnspan=2, pady=10)
        
    except Exception as e:
        messagebox.showerror("Error", f"Could not display code: {e}")

# Function to clear input fields after code generation
def clear_fields():
    entry_payee.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_filename.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Payment Code Generator")

# Labels and input fields for Payee (Phone number or UPI ID), Amount, and Filename
tk.Label(root, text="Enter Payee (Phone number or UPI ID):").grid(row=0, column=0, pady=10)
entry_payee = tk.Entry(root)
entry_payee.grid(row=0, column=1, padx=10)

tk.Label(root, text="Enter Amount:").grid(row=1, column=0, pady=10)
entry_amount = tk.Entry(root)
entry_amount.grid(row=1, column=1, padx=10)

tk.Label(root, text="Enter Filename:").grid(row=2, column=0, pady=10)
entry_filename = tk.Entry(root)
entry_filename.grid(row=2, column=1, padx=10)

# Option to choose between QR Code and Barcode
code_type = StringVar(value="QR Code")
tk.Radiobutton(root, text="QR Code", variable=code_type, value="QR Code").grid(row=3, column=0)
tk.Radiobutton(root, text="Barcode", variable=code_type, value="Barcode").grid(row=3, column=1)

# Button to generate the Payment Code
btn_generate = tk.Button(root, text="Generate Payment Code", command=generate_code)
btn_generate.grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk

# Theme Colors
COLOR_BG = "#0F172A"            # Deep Slate background
COLOR_CARD = "#1E293B"          # Card background
COLOR_BORDER = "#334155"        # Cool Slate border
COLOR_ENTRY_BG = "#0F172A"      # Input field background
COLOR_TEXT = "#F8FAFC"          # Bright white text
COLOR_TEXT_MUTED = "#94A3B8"    # Muted gray text

COLOR_ACCENT = "#6366F1"        # Indigo primary
COLOR_ACCENT_HOVER = "#4F46E5"  # Indigo hover
COLOR_ACCENT_ACTIVE = "#4338CA" # Indigo active

COLOR_SUCCESS = "#10B981"       # Emerald secondary
COLOR_SUCCESS_HOVER = "#059669" # Emerald hover
COLOR_SUCCESS_ACTIVE = "#047857"# Emerald active

# Function to generate QR Code
def generate_qr():
    global qr_image

    data = entry.get().strip()

    if data == "":
        messagebox.showerror("Error", "Please enter some text or URL to generate QR Code.")
        return

    try:
        # Generate QR
        img = qrcode.make(data)

        # Resize image to fit nicely inside the card
        img = img.resize((230, 230))

        # Save temporarily
        img.save("temp_qr.png")

        # Display in Tkinter
        qr_image = ImageTk.PhotoImage(Image.open("temp_qr.png"))
        
        # Switch from placeholder text to the QR image
        placeholder_label.pack_forget()
        image_label.config(image=qr_image)
        image_label.pack(expand=True)

        # Store image for Saving
        image_label.image_data = img
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate QR Code: {str(e)}")

# Function to save QR code
def save_qr():
    if not hasattr(image_label, "image_data"):
        messagebox.showwarning("Warning", "Please generate a QR code first.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png")]
    )

    if file_path:
        try:
            image_label.image_data.save(file_path)
            messagebox.showinfo("Success", "QR code saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save QR Code: {str(e)}")


def create_modern_button(parent, text, command, bg_color, hover_color, active_color):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 11, "bold"),
        fg=COLOR_TEXT,
        bg=bg_color,
        activeforeground=COLOR_TEXT,
        activebackground=active_color,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=18,
        pady=8
    )
    
    def on_enter(e):
        btn.config(bg=hover_color)
        
    def on_leave(e):
        btn.config(bg=bg_color)
        
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# Main Window
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x580+100+100")
root.resizable(False, False)
root.config(bg=COLOR_BG)

# Title Label
title = tk.Label(
    root,
    text="QR CODE GENERATOR",
    font=("Segoe UI", 18, "bold"),
    fg=COLOR_TEXT,
    bg=COLOR_BG
)
title.pack(pady=(25, 5))

# Subtitle / Instruction Label
subtitle = tk.Label(
    root,
    text="Enter Text or URL below:",
    font=("Segoe UI", 10, "bold"),
    fg=COLOR_TEXT_MUTED,
    bg=COLOR_BG
)
subtitle.pack(pady=(10, 5))

# Styled Entry Frame (simulates a custom flat border)
entry_frame = tk.Frame(root, bg=COLOR_BORDER, bd=0, padx=1, pady=1)
entry_frame.pack(pady=10)

entry = tk.Entry(
    entry_frame,
    width=28,
    font=("Segoe UI", 12),
    bg=COLOR_ENTRY_BG,
    fg=COLOR_TEXT,
    insertbackground=COLOR_TEXT, # Caret color
    relief="flat",
    bd=6 # Internal padding
)
entry.pack()

# Input Focus Highlighting
def on_entry_focus_in(e):
    entry_frame.config(bg=COLOR_ACCENT)

def on_entry_focus_out(e):
    entry_frame.config(bg=COLOR_BORDER)

entry.bind("<FocusIn>", on_entry_focus_in)
entry.bind("<FocusOut>", on_entry_focus_out)

# Action Buttons Frame
btn_frame = tk.Frame(root, bg=COLOR_BG)
btn_frame.pack(pady=15)

generate_btn = create_modern_button(
    btn_frame,
    text="Generate",
    command=generate_qr,
    bg_color=COLOR_ACCENT,
    hover_color=COLOR_ACCENT_HOVER,
    active_color=COLOR_ACCENT_ACTIVE
)
generate_btn.pack(side="left", padx=10)

save_btn = create_modern_button(
    btn_frame,
    text="Save Code",
    command=save_qr,
    bg_color=COLOR_SUCCESS,
    hover_color=COLOR_SUCCESS_HOVER,
    active_color=COLOR_SUCCESS_ACTIVE
)
save_btn.pack(side="left", padx=10)

# Preview Area Card
preview_frame = tk.Frame(
    root,
    bg=COLOR_CARD,
    width=260,
    height=260,
    highlightthickness=1,
    highlightbackground=COLOR_BORDER
)
preview_frame.pack_propagate(False)
preview_frame.pack(pady=(15, 25))

# Placeholder text within the card
placeholder_label = tk.Label(
    preview_frame,
    text="Your generated QR code\nwill appear here.",
    font=("Segoe UI", 10, "italic"),
    fg=COLOR_TEXT_MUTED,
    bg=COLOR_CARD
)
placeholder_label.pack(expand=True)

# Actual Image Label (packed when QR code is generated)
image_label = tk.Label(preview_frame, bg=COLOR_CARD)

root.mainloop()



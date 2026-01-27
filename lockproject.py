import os
import shutil
import base64
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
from hashlib import sha256

# ---------- ENCRYPTION ----------
def make_key(password):
    return base64.urlsafe_b64encode(sha256(password.encode()).digest())

# ---------- ACTIONS ----------
def lock_folder():
    folder = filedialog.askdirectory()
    if not folder:
        return

    password = entry.get()
    if not password:
        status("ACCESS DENIED: PASSWORD REQUIRED")
        return

    key = make_key(password)
    fernet = Fernet(key)

    shutil.make_archive(folder, 'zip', folder)

    with open(folder + ".zip", "rb") as f:
        encrypted = fernet.encrypt(f.read())

    with open(folder + ".locked", "wb") as f:
        f.write(encrypted)

    shutil.rmtree(folder)
    os.remove(folder + ".zip")

    status("FOLDER ENCRYPTED SUCCESSFULLY")

def unlock_folder():
    file = filedialog.askopenfilename(filetypes=[("Locked Files", "*.locked")])
    if not file:
        return

    password = entry.get()
    key = make_key(password)
    fernet = Fernet(key)

    try:
        with open(file, "rb") as f:
            decrypted = fernet.decrypt(f.read())

        zip_path = file.replace(".locked", ".zip")
        with open(zip_path, "wb") as f:
            f.write(decrypted)

        shutil.unpack_archive(zip_path, os.path.dirname(file))
        os.remove(zip_path)
        os.remove(file)

        status("ACCESS GRANTED: FOLDER DECRYPTED")

    except:
        status("ACCESS DENIED: WRONG PASSWORD")

# ---------- UI ----------
def status(msg):
    status_label.config(text=msg)

app = tk.Tk()
app.title("HACKER FOLDER LOCK")
app.geometry("420x260")
app.configure(bg="black")

FONT = ("Consolas", 11)

tk.Label(app, text=">> ENTER PASSWORD <<",
         fg="#00ff00", bg="black", font=FONT).pack(pady=10)

entry = tk.Entry(app, show="*", fg="#00ff00", bg="black",
                 insertbackground="#00ff00", font=FONT, width=30)
entry.pack()

btn_style = {
    "fg": "#00ff00",
    "bg": "black",
    "activebackground": "#003300",
    "activeforeground": "#00ff00",
    "font": FONT,
    "width": 25,
    "bd": 2,
    "highlightbackground": "#00ff00"
}

tk.Button(app, text="[ LOCK FOLDER ]",
          command=lock_folder, **btn_style).pack(pady=10)

tk.Button(app, text="[ UNLOCK FOLDER ]",
          command=unlock_folder, **btn_style).pack()

status_label = tk.Label(app, text="SYSTEM READY",
                        fg="#00ff00", bg="black", font=("Consolas", 10))
status_label.pack(pady=20)

app.mainloop()

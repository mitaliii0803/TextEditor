import tkinter as tk
from tkinter import filedialog, messagebox


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Simple Text Editor")
root.geometry("800x600")
root.minsize(500, 300)


# ---------------- TEXT AREA ----------------

text = tk.Text(
    root,
    wrap=tk.WORD,
    font=("Helvetica", 18),
    undo=True
)

text.grid(
    row=0,
    column=0,
    sticky="nsew"
)


# ---------------- STATUS BAR ----------------

status_bar = tk.Label(
    root,
    text="Words: 0 | Characters: 0",
    anchor="w",
    relief=tk.SUNKEN,
    padx=10
)

status_bar.grid(
    row=1,
    column=0,
    sticky="ew"
)


# Make text area expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


# ---------------- WORD & CHARACTER COUNT ----------------

def update_count(event=None):
    content = text.get("1.0", "end-1c")

    words = len(content.split())
    characters = len(content)

    status_bar.config(
        text=f"Words: {words} | Characters: {characters}"
    )


# Update count whenever user types
text.bind("<KeyRelease>", update_count)


# ---------------- NEW FILE ----------------

def new_file():
    text.delete("1.0", tk.END)
    update_count()


# ---------------- OPEN FILE ----------------

def open_file():
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            text.delete("1.0", tk.END)
            text.insert(tk.END, content)

            update_count()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not open file.\n\n{e}"
            )


# ---------------- SAVE FILE ----------------

def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        try:
            content = text.get("1.0", "end-1c")

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

            messagebox.showinfo(
                "Saved",
                "File saved successfully!"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not save file.\n\n{e}"
            )


# ---------------- FIND & REPLACE ----------------

def find_replace():

    find_window = tk.Toplevel(root)
    find_window.title("Find & Replace")
    find_window.geometry("400x200")
    find_window.resizable(False, False)

    # Find
    tk.Label(
        find_window,
        text="Find:"
    ).pack(pady=(15, 5))

    find_entry = tk.Entry(
        find_window,
        width=40
    )
    find_entry.pack()

    # Replace
    tk.Label(
        find_window,
        text="Replace with:"
    ).pack(pady=(10, 5))

    replace_entry = tk.Entry(
        find_window,
        width=40
    )
    replace_entry.pack()


    # Replace first occurrence
    def replace_one():

        find_text = find_entry.get()
        replace_text = replace_entry.get()

        if find_text == "":
            messagebox.showwarning(
                "Warning",
                "Please enter text to find."
            )
            return

        content = text.get("1.0", "end-1c")

        if find_text not in content:
            messagebox.showinfo(
                "Not Found",
                "Text not found."
            )
            return

        new_content = content.replace(
            find_text,
            replace_text,
            1
        )

        text.delete("1.0", tk.END)
        text.insert("1.0", new_content)

        update_count()


    # Replace all occurrences
    def replace_all():

        find_text = find_entry.get()
        replace_text = replace_entry.get()

        if find_text == "":
            messagebox.showwarning(
                "Warning",
                "Please enter text to find."
            )
            return

        content = text.get("1.0", "end-1c")

        count = content.count(find_text)

        if count == 0:
            messagebox.showinfo(
                "Not Found",
                "Text not found."
            )
            return

        new_content = content.replace(
            find_text,
            replace_text
        )

        text.delete("1.0", tk.END)
        text.insert("1.0", new_content)

        update_count()

        messagebox.showinfo(
            "Replaced",
            f"{count} occurrence(s) replaced."
        )


    # Buttons
    button_frame = tk.Frame(find_window)
    button_frame.pack(pady=20)

    tk.Button(
        button_frame,
        text="Replace",
        command=replace_one
    ).pack(
        side=tk.LEFT,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Replace All",
        command=replace_all
    ).pack(
        side=tk.LEFT,
        padx=5
    )


# ---------------- FILE MENU ----------------

menu = tk.Menu(root)
root.config(menu=menu)


file_menu = tk.Menu(
    menu,
    tearoff=0
)

menu.add_cascade(
    label="File",
    menu=file_menu
)

file_menu.add_command(
    label="New",
    command=new_file
)

file_menu.add_command(
    label="Open",
    command=open_file
)

file_menu.add_command(
    label="Save",
    command=save_file
)

file_menu.add_separator()

file_menu.add_command(
    label="Exit",
    command=root.quit
)


# ---------------- EDIT MENU ----------------

edit_menu = tk.Menu(
    menu,
    tearoff=0
)

menu.add_cascade(
    label="Edit",
    menu=edit_menu
)


# Cut
edit_menu.add_command(
    label="Cut",
    command=lambda: text.event_generate("<<Cut>>")
)


# Copy
edit_menu.add_command(
    label="Copy",
    command=lambda: text.event_generate("<<Copy>>")
)


# Paste
edit_menu.add_command(
    label="Paste",
    command=lambda: text.event_generate("<<Paste>>")
)


# Select All
edit_menu.add_command(
    label="Select All",
    command=lambda: text.event_generate("<<SelectAll>>")
)


edit_menu.add_separator()


# Find & Replace
edit_menu.add_command(
    label="Find & Replace",
    command=find_replace
)


edit_menu.add_separator()


# Undo
edit_menu.add_command(
    label="Undo",
    command=lambda: text.event_generate("<<Undo>>")
)


# Redo
edit_menu.add_command(
    label="Redo",
    command=lambda: text.event_generate("<<Redo>>")
)


# ---------------- START APPLICATION ----------------

root.mainloop()
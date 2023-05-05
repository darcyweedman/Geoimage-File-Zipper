import os
import sys
import tempfile
import subprocess
from tkinter import filedialog, messagebox, StringVar
from ttkbootstrap import Style
import tkinter as tk
import zipfile
from shutil import copyfileobj
from pkg_resources import resource_stream


def extract_resource(resource_path: str) -> str:
    if hasattr(sys, '_MEIPASS'):
        with resource_stream(__name__, resource_path) as resource_file, tempfile.NamedTemporaryFile(delete=False) as temp_file:
            copyfileobj(resource_file, temp_file)
            return temp_file.name
    else:
        return resource_path


class ZipFilesGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry('600x600')
        style = Style('minty')  # Set the ttkbootstrap style to 'minty'
        style.theme_use('minty')  # Set the ttkbootstrap theme to 'minty'
        style.configure('TButton', font=('Helvetica', 12))

        # Initialize the selected directories
        self.input_directory = None
        self.output_directory = None

        # Create the folder path variables
        self.input_folder_path = StringVar()
        self.output_folder_path = StringVar()

        # Create the status bar
        self.status_var = StringVar()

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.master, text="Geoimage File Zipper", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(10, 20))

        logo_path = extract_resource("logo.png")
        logo_image = tk.PhotoImage(file=logo_path)
        logo_label = tk.Label(self.master, image=logo_image)
        logo_label.image = logo_image
        logo_label.pack(pady=(10, 20))

        frame = tk.Frame(self.master)
        frame.pack(padx=20, pady=20)

        input_label = tk.Label(frame, text="Input Directory:", font=("Helvetica", 12))
        input_label.grid(row=0, column=0, sticky="E", padx=(0, 10))
        self.input_button = tk.Button(frame, text="Browse", command=self.select_input_directory)
        self.input_button.grid(row=0, column=1)

        output_label = tk.Label(frame, text="Output Directory:", font=("Helvetica", 12))
        output_label.grid(row=1, column=0, sticky="E", padx=(0, 10),)
        self.output_button = tk.Button(frame, text="Browse", command=self.select_output_directory)
        self.output_button.grid(row=1, column=1)

        input_folder_label = tk.Label(self.master, textvariable=self.input_folder_path, fg="#1c1c1c", font=("Helvetica", 10, "italic"), wraplength=400)
        output_folder_label = tk.Label(self.master, textvariable=self.output_folder_path, fg="#1c1c1c", font=("Helvetica", 10, "italic"), wraplength=400)

        input_folder_label.pack(pady=(10, 0))
        output_folder_label.pack(pady=(0, 20))

        process_button = tk.Button(self.master, text="Zip Files", command=self.zip_files)
        process_button.pack(padx=10, pady=10)

        self.open_output_folder_button = tk.Button(self.master, text="Open Output Folder", command=self.open_output_folder, state="disabled")
        self.open_output_folder_button.pack(padx=10, pady=(10, 10))

        status_bar = tk.Label(self.master, textvariable=self.status_var, font=("Helvetica", 12), wraplength=400)
        status_bar.pack(pady=(10, 0))

    def select_input_directory(self):
        self.input_directory = filedialog.askdirectory()
        if self.input_directory:
            self.input_folder_path.set(f"Input folder: {self.input_directory}")

    def select_output_directory(self):
        self.output_directory = filedialog.askdirectory()
        if self.output_directory:
            self.output_folder_path.set(f"Output folder: {self.output_directory}")

    def open_output_folder(self):
        if not self.output_directory:
            messagebox.showerror("Error", "No output directory selected.")
        else:
            subprocess.Popen(f'explorer "{os.path.realpath(self.output_directory)}"')

    def zip_files(self):
        if not self.input_directory:
            messagebox.showerror("Error", "No input directory selected.")
        elif not self.output_directory:
            messagebox.showerror("Error", "No output directory selected.")
        else:
            file_dict = {}

            for filename in os.listdir(self.input_directory):
                file_path = os.path.join(self.input_directory, filename)

                if os.path.isdir(file_path):
                    continue

                file_name = os.path.splitext(filename)[0]

                if file_name in file_dict:
                    file_dict[file_name].append(file_path)
                else:
                    file_dict[file_name] = [file_path]

            for file_name, file_paths in file_dict.items():
                zip_filename = os.path.join(self.output_directory, file_name + ".zip")

                with zipfile.ZipFile(zip_filename, "w") as zip_file:
                    for file_path in file_paths:
                        zip_path = os.path.basename(file_path)
                        zip_file.write(file_path, zip_path)

            self.status_var.set("Zip files created successfully.")
            messagebox.showinfo("Zip Files", "Zip files created successfully.")

            self.open_output_folder_button.config(state="normal")


# Create the main window and start the event loop
root = tk.Tk()
app = ZipFilesGUI(root)
root.mainloop()

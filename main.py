import tkinter as tk
from tkinter import filedialog
from xml.etree import ElementTree as ET

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:
        parse_xml(file_path)

def parse_xml(file_path):
    global tags
    tree = ET.parse(file_path)
    root = tree.getroot()
    tags = set()
    for elem in root.iter():
        tags.add(elem.tag)
    display_checkboxes(tags)

def display_checkboxes(tags):
    for widget in frame.winfo_children():
        widget.destroy()
    for tag in tags:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(frame, text=tag, variable=var)
        checkbox.pack(anchor='w')

def filter_tags(*args):
    search_term = search_var.get().lower()
    filtered_tags = {tag for tag in tags if search_term in tag.lower()}
    display_checkboxes(filtered_tags)

root = tk.Tk()
root.title("XML Tag Selector")

search_var = tk.StringVar()
search_var.trace("w", filter_tags)

search_entry = tk.Entry(root, textvariable=search_var)
search_entry.pack(pady=10)

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)

frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

open_button = tk.Button(root, text="Escolhe arquivo", command=open_file)
open_button.pack(pady=10)

root.mainloop()
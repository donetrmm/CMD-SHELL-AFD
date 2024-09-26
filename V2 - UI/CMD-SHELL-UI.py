import tkinter as tk
from tkinter import filedialog, messagebox
from docx import Document
import csv

final_states = {6, 41, 25, 54, 37, 75, 80}

transitions = {
    80: {'a-z': 80, '0-9': 80, '-': 80, '.': 80},
    79: {'a-z': 80, '0-9': 80, '.': 80},
    78: {' ': 52},
    77: {'{': 33, '\\': 29},
    76: {'a-z': 76, '0-9': 76, '-': 76, '.': 76, ' ': 77},
    75: {' ': 65},
    74: {'a-z': 74, '0-9': 74, '/': 74, '-': 74, '.': 74, ' ': 52},
    72: {'a-z': 74, '0-9': 74, '/': 74, '.': 74},
    71: {'a-z': 71, '0-9': 71, '/': 71, '-': 71, '.': 71, ' ': 72},
    70: {'a-z': 71, '0-9': 71, '/': 71, '.': 71},
    69: {'a-z': 76, '0-9': 76, '.': 76},
    68: {'a-z': 76, '0-9': 76, '.': 76},
    67: {' ': 79},
    66: {' ': 70},
    65: {'>': 5},
    64: {' ': 69},
    63: {'t': 64},
    62: {'p': 66, 'a': 63},
    61: {' ': 68},
    60: {'p': 61},
    59: {'e': 60},
    58: {'r': 59},
    57: {' ': 77},
    56: {'e': 48},
    55: {'-': 56},
    54: {' ': 55},
    53: {'d': 54, 'f': 54},
    52: {'\\': 29},
    51: {' ': 38},
    50: {'c': 51},
    49: {'e': 50},
    48: {'x': 49},
    47: {' ': 53},
    46: {'e': 47},
    45: {'p': 46},
    44: {'y': 45},
    43: {'t': 44, 'e': 48},
    42: {'-': 43},
    41: {'a-z': 41, '0-9': 41, '-': 41, '.': 41, ' ': 42},
    40: {'a-z': 41, '0-9': 41, '.': 41},
    39: {'s': 57},
    38: {'g': 58, 'c': 62, 'l': 39},
    37: {'a-z': 37, '0-9': 37, '-': 37, '.': 37, ' ': 55},
    36: {'a-z': 37, '0-9': 37, '.': 37},
    33: {'}': 78},
    32: {' ': 36},
    31: {'e': 32},
    30: {'m': 31},
    29: {';': 75},
    28: {'a': 30},
    27: {'n': 28, 'e': 9},
    26: {'-': 27},
    25: {' ': 26},
    24: {'d': 25, 'f': 25},
    23: {' ': 40},
    22: {'e': 23},
    20: {'m': 22},
    18: {' ': 24},
    16: {'e': 18},
    15: {'p': 16},
    14: {' ': 38},
    13: {'c': 14},
    12: {'e': 13},
    11: {'a': 20},
    10: {'y': 15},
    9: {'x': 12},
    8: {'n': 11, 't': 10, 'e': 9},
    7: {'-': 8},
    6: {'a-z': 6, '0-9': 6, '/': 6, '.': 6, ' ': 7},
    5: {'>': 67, ' ': 79},
    4: {' ': 6},
    3: {'d': 4},
    2: {'n': 3},
    1: {'i': 2},
    0: {'f': 1},
}

def is_in_range(char, symbol):
    if symbol == 'a-z':
        return 'a' <= char <= 'z'
    elif symbol == '0-9':
        return '0' <= char <= '9'
    return char == symbol

def read_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for i, para in enumerate(doc.paragraphs):
            full_text.append((i + 1, para.text))  
        return full_text
    except Exception as e:
        print(f"Error al leer el archivo .docx: {e}")
        return []

def simulate_automaton(input_string):
    current_state = 0  
    for i, char in enumerate(input_string):
        found_transition = False
        for symbol, next_state in transitions.get(current_state, {}).items():
            if is_in_range(char, symbol):  
                current_state = next_state
                found_transition = True
                break
        if not found_transition:
            return False, i  
    return current_state in final_states, len(input_string)  

def save_to_csv(data, output_file):
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Fila", "Columna", "Cadena", "Resultado"])
            for row in data:
                writer.writerow(row)
        print(f"Resultados guardados en '{output_file}'")
    except Exception as e:
        print(f"Error al escribir en el archivo CSV: {e}")

def process_file(file_path, output_csv):
    content = read_docx(file_path)
    results = []
    for line_num, text in content:
        if text.strip(): 
            accepted, last_position = simulate_automaton(text)
            result = "Aceptada" if accepted else "No aceptada"
            results.append([line_num, last_position, text, result])

    save_to_csv(results, output_csv)

def select_file():
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo .docx",
        filetypes=[("Archivos DOCX", "*.docx")])
    if file_path:
        output_csv = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")],
            title="Guardar como CSV"
        )
        if output_csv:
            process_file(file_path, output_csv)
            messagebox.showinfo("Éxito", "El archivo CSV se ha guardado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó un archivo para guardar el CSV.")
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó un archivo DOCX.")

def create_gui():
    root = tk.Tk()
    root.title("Procesador de Autómata con .docx")
    root.geometry("300x150")

    label = tk.Label(root, text="Selecciona un archivo .docx para procesar:")
    label.pack(pady=20)

    select_button = tk.Button(root, text="Seleccionar archivo", command=select_file)
    select_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()

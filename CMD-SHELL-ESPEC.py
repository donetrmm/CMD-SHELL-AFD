import tkinter as tk
from tkinter import filedialog, messagebox
from docx import Document
import csv

def load_formal_spec(file_path):
    transitions = {}
    final_states = set()
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            print("Contenido del archivo de especificación:")
            for line in lines:
                print(line.strip())  
            
            for line in lines:
                if line.startswith("F ="):
                    final_states = set(map(int, line.strip()[3:].strip('{} ').split(',')))

                if line.startswith("D ="):
                    transitions_list = line.strip()[3:].strip('{} ').split('),')
                    for transition in transitions_list:
                        transition = transition.strip('() ')
                        
                        parts = transition.split(',')
                        if len(parts) == 3:
                            current_state, symbol, next_state = parts
                            current_state = int(current_state)
                            next_state = int(next_state.strip())
                            symbol = symbol.strip().strip('"')
                            
                            if current_state not in transitions:
                                transitions[current_state] = {}
                            transitions[current_state][symbol] = next_state
                        else:
                            print(f"Advertencia: Transición inválida o mal formateada: {transition}")
    
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no fue encontrado.")
    except Exception as e:
        print(f"Error al cargar el archivo de especificación: {e}")

    return transitions, final_states

transitions, final_states = load_formal_spec('./especificacion-formal.txt')

print("Transiciones cargadas:")
for state, trans in transitions.items():
    print(f"Estado {state}: {trans}")

def is_in_range(char, symbol):
    if symbol == 'a-z':
        return 'a' <= char <= 'z'
    elif symbol == '0-9':
        return '0' <= char <= '9'
    else:
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
    print(f"Inicio en el estado: {current_state}")

    for i, char in enumerate(input_string):
        found_transition = False
        print(f"Evaluando carácter: '{char}' en estado: {current_state}")
        
        for symbol, next_state in transitions.get(current_state, {}).items():
            print(f"Comparando con transición: '{symbol}'")

            if is_in_range(char, symbol):  
                print(f"Transición válida: {current_state} --'{symbol}'--> {next_state}")
                current_state = next_state
                found_transition = True
                break
        
        if not found_transition:
            print(f"Fallo en el estado: {current_state}, carácter: '{char}' no tiene una transición válida")
            return False, i  
    
    is_accepted = current_state in final_states
    if is_accepted:
        print(f"Cadena aceptada en el estado: {current_state}")
    else:
        print(f"Cadena no aceptada, terminó en el estado: {current_state}")
    return is_accepted, len(input_string)  

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

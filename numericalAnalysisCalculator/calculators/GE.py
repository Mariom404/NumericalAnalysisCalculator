import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import random

class GaussEliminationCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gauss Elimination Solver (3x3)")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        self.matrix_entries = []
        self.pivoting = tk.BooleanVar(value=True)
        
        self.setup_ui()
        self.create_matrix_inputs()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Checkbutton(main_frame, text="Use Partial Pivoting", variable=self.pivoting).pack(pady=5)
        
        self.matrix_frame = ttk.LabelFrame(main_frame, text="Enter 3x3 Matrix A and Vector b")
        self.matrix_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.solution_text = tk.Text(main_frame, height=15, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(main_frame, command=self.solution_text.yview)
        self.solution_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.solution_text.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Solve", command=self.solve).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Random Fill", command=self.random_fill).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Example", command=self.load_example).pack(side=tk.LEFT, padx=5)
    
    def create_matrix_inputs(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        
        self.matrix_entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                e = ttk.Entry(self.matrix_frame, width=6)
                e.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(e)
            ttk.Separator(self.matrix_frame, orient=tk.VERTICAL).grid(row=i, column=3, sticky='ns', padx=5)
            e = ttk.Entry(self.matrix_frame, width=6)
            e.grid(row=i, column=4, padx=2, pady=2)
            row_entries.append(e)
            self.matrix_entries.append(row_entries)
    
    def get_matrix(self):
        try:
            A = np.zeros((3, 3))
            b = np.zeros(3)
            for i in range(3):
                for j in range(3):
                    A[i,j] = float(self.matrix_entries[i][j].get())
                b[i] = float(self.matrix_entries[i][3].get())
            return A, b
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers in all fields")
            return None, None
    
    def clear(self):
        for row in self.matrix_entries:
            for entry in row:
                entry.delete(0, tk.END)
        self.solution_text.delete(1.0, tk.END)
    
    def random_fill(self):
        """Fill the matrix with random values"""
        self.clear()
        for i in range(3):
            for j in range(3):
                self.matrix_entries[i][j].insert(0, f"{random.uniform(-10, 10):.2f}")
            self.matrix_entries[i][3].insert(0, f"{random.uniform(-10, 10):.2f}")
    
    def load_example(self):
        example = [[4,1,-1,-2], [5,1,2,4], [6,1,1,6]]
        for i in range(3):
            for j in range(4):
                self.matrix_entries[i][j].delete(0, tk.END)
                self.matrix_entries[i][j].insert(0, str(example[i][j]))
    
    def solve(self):
        A, b = self.get_matrix()
        if A is None: return
        
        self.solution_text.delete(1.0, tk.END)
        Ab = np.column_stack((A.copy(), b.copy()))
        
        self.solution_text.insert(tk.END, "=== GAUSS ELIMINATION ===\n")
        self.print_matrix(Ab, "Initial [A|b]:")
        
        for i in range(3):
            if self.pivoting.get():
                max_row = np.argmax(np.abs(Ab[i:, i])) + i
                if max_row != i:
                    Ab[[i, max_row]] = Ab[[max_row, i]]
                    self.solution_text.insert(tk.END, f"Pivot: Swapped row {i+1} ↔ {max_row+1}\n")
                    self.print_matrix(Ab, "After pivot:")
            
            for j in range(i+1, 3):
                m = Ab[j,i]/Ab[i,i]
                self.solution_text.insert(tk.END, f"m {j+1}{i+1} = {Ab[j,i]:.4} / {Ab[i,i]:.4} = {m:.4f} \n")
                Ab[j,i:] -= m * Ab[i,i:]
                self.solution_text.insert(tk.END, f"Row {j+1} -= {m:.4f} * Row {i+1}\n")
                self.print_matrix(Ab[:,:-1], "Current A:")
        
        x = np.zeros(3)
        for i in range(2, -1, -1):
            x[i] = (Ab[i,3] - np.sum(Ab[i,i+1:3]*x[i+1:3])) / Ab[i,i]
            self.solution_text.insert(tk.END, f"x[{i}] = {x[i]:.4f}\n")
    
    def print_matrix(self, matrix, label=""):
        self.solution_text.insert(tk.END, f"{label}\n")
        for row in matrix:
            self.solution_text.insert(tk.END, " ".join(f"{x:7.3f}" for x in row) + "\n")
        self.solution_text.insert(tk.END, "\n")

def run():
    root = tk.Toplevel()
    app = GaussEliminationCalculator(root)
    root.mainloop()
    
if __name__ == "__main__":
    run()
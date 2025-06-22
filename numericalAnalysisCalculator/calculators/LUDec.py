import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import random

class LUSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("LU Decomposition Solver (3x3)")
        self.root.geometry("850x750")  # Slightly larger to show all steps
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
        
        self.solution_text = tk.Text(main_frame, height=22, wrap=tk.WORD, font=('Consolas', 10))
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
                e = ttk.Entry(self.matrix_frame, width=8)
                e.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(e)
            ttk.Separator(self.matrix_frame, orient=tk.VERTICAL).grid(row=i, column=3, sticky='ns', padx=5)
            e = ttk.Entry(self.matrix_frame, width=8)
            e.grid(row=i, column=4, padx=2, pady=2)
            row_entries.append(e)
            self.matrix_entries.append(row_entries)
    
    def get_matrix(self):
        try:
            A = np.zeros((3, 3))
            b = np.zeros(3)
            for i in range(3):
                for j in range(3):
                    val = float(self.matrix_entries[i][j].get())
                    A[i, j] = val
                b_val = float(self.matrix_entries[i][3].get())
                b[i] = b_val
            return A, b
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers in all fields")
            return None, None
    
    def clear(self):
        """Clear all input fields and the solution text"""
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
        """Load an example system"""
        self.clear()
        example_A = [
            [4, 1, -1],
            [5, 1, 2],
            [6, 1, 1]
        ]
        example_b = [-2, 4, 6]
        
        for i in range(3):
            for j in range(3):
                self.matrix_entries[i][j].insert(0, str(example_A[i][j]))
            self.matrix_entries[i][3].insert(0, str(example_b[i]))
    
    def print_matrix(self, matrix, title=""):
        """Helper method to print a matrix in the solution text"""
        self.solution_text.insert(tk.END, f"\n{title}\n")
        if len(matrix.shape) == 1:  # Vector 1D
            for i in range(matrix.shape[0]):
                self.solution_text.insert(tk.END, f"[ {matrix[i]:10.6f} ]\n")
        else:  # Matrix
            for i in range(matrix.shape[0]):
                row = "[ "
                for j in range(matrix.shape[1]):
                    row += f"{matrix[i,j]:10.6f} "
                row += "]\n"
                self.solution_text.insert(tk.END, row)
        self.solution_text.insert(tk.END, "\n")
    
    def solve(self):
        A, b = self.get_matrix()
        if A is None: return
        
        self.solution_text.delete(1.0, tk.END)
        L = np.eye(3)
        U = A.copy()
        P = np.eye(3)
        b = b.copy()
        
        # ===== LU DECOMPOSITION =====
        self.solution_text.insert(tk.END, "=== LU DECOMPOSITION STEPS ===\n")
        self.print_matrix(A, "Initial Matrix A:")
        
        for i in range(3):
            self.solution_text.insert(tk.END, f"--- STAGE {i+1} ---\n")
            
            # Pivoting
            if self.pivoting.get():
                max_row = np.argmax(np.abs(U[i:, i])) + i
                if max_row != i:
                    U[[i, max_row], i:] = U[[max_row, i], i:]
                    if i > 0:
                        L[[i, max_row], :i] = L[[max_row, i], :i]
                    P[[i, max_row]] = P[[max_row, i]]
                    b[[i, max_row]] = b[[max_row, i]]
                    self.solution_text.insert(tk.END, f"Pivot: Swapped row {i+1} ↔ row {max_row+1}\n")
                    self.print_matrix(U, "U after pivot:")
                    self.print_matrix(L, "L after pivot:")
            
            # Elimination
            for j in range(i+1, 3):
                L[j,i] = U[j,i]/U[i,i]
                self.solution_text.insert(tk.END, f"m{j+1}{i+1} = {U[j,i]:.4f} / {U[i,i]:.4f} = {L[j,i]:.4f}\n")
                U[j,i:] -= L[j,i] * U[i,i:]
                self.solution_text.insert(tk.END, f"Row {j+1} -= {L[j,i]:.4f} * Row {i+1}\n")
                self.print_matrix(U, "Updated U:")
                self.print_matrix(L, "Updated L:")
        
        # ===== FORWARD SUBSTITUTION =====
        self.solution_text.insert(tk.END, "\n=== FORWARD SUBSTITUTION (Lc = b) ===\n")
        c = np.zeros(3)
        for i in range(3):
            c[i] = b[i] - np.sum(L[i,:i] * c[:i])
            self.solution_text.insert(tk.END, f"\nc[{i}] = b[{i}] - sum(L[{i},:]*c[:])")
            self.solution_text.insert(tk.END, f"\n     = {b[i]:.4f} - {np.sum(L[i,:i] * c[:i]):.4f} = {c[i]:.6f}\n")
        
        # ===== BACK SUBSTITUTION =====
        self.solution_text.insert(tk.END, "\n=== BACK SUBSTITUTION (Ux = c) ===\n")
        x = np.zeros(3)
        for i in range(2, -1, -1):
            self.solution_text.insert(tk.END, f"\nSolving for x[{i}]:\n")
            self.solution_text.insert(tk.END, f"x[{i}] = [c[{i}] - (")
            
            # Show the terms being subtracted
            terms = []
            for j in range(i+1, 3):
                terms.append(f"U[{i},{j}]*x[{j}]")
            self.solution_text.insert(tk.END, " + ".join(terms) + f")] / U[{i},{i}]\n")
            
            # Show numerical calculation
            sum_terms = np.sum(U[i,i+1:3] * x[i+1:3])
            self.solution_text.insert(tk.END, f"     = [{c[i]:.6f} - ({sum_terms:.6f})] / {U[i,i]:.6f}\n")
            x[i] = (c[i] - sum_terms) / U[i,i]
            self.solution_text.insert(tk.END, f"     = {x[i]:.8f}\n")
        
        # ===== FINAL SOLUTION =====
        self.solution_text.insert(tk.END, "=== FINAL SOLUTION ===\n")
        for i in range(3):
            self.solution_text.insert(tk.END, f"x[{i}] = {x[i]:.8f}\n")

def run():
    root = tk.Toplevel()
    app = LUSolver(root)
    root.mainloop()
    
if __name__ == "__main__":
    run()
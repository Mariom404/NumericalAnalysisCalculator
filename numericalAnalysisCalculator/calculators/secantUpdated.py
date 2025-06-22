import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math

class SecantCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Secant Method Calculator")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        self.setup_ui()
        
    def setup_ui(self):
        # Create main container
        main_frame = tk.Frame(self.root, bg="#f0f2f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Input frame
        input_frame = tk.LabelFrame(main_frame, text="Input Parameters", bg="#f0f2f5", fg="#333", font=('Arial', 12, 'bold'))
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Function input
        tk.Label(input_frame, text="Function f(x):", bg="#f0f2f5", font=('Arial', 10)).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.function_entry = tk.Entry(input_frame, width=40, font=('Arial', 10))
        self.function_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Initial guesses and tolerance
        tk.Label(input_frame, text="Initial guess xi-1:", bg="#f0f2f5", font=('Arial', 10)).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.xi_minus1_entry = tk.Entry(input_frame, font=('Arial', 10))
        self.xi_minus1_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        tk.Label(input_frame, text="Initial guess xi:", bg="#f0f2f5", font=('Arial', 10)).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.xi_entry = tk.Entry(input_frame, font=('Arial', 10))
        self.xi_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        tk.Label(input_frame, text="Error tolerance (ε):", bg="#f0f2f5", font=('Arial', 10)).grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.eps_entry = tk.Entry(input_frame, font=('Arial', 10))
        self.eps_entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        tk.Label(input_frame, text="Max iterations:", bg="#f0f2f5", font=('Arial', 10)).grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.max_iter_entry = tk.Entry(input_frame, font=('Arial', 10))
        self.max_iter_entry.grid(row=4, column=1, sticky='w', padx=5, pady=5)
        
        # Calculate button
        btn_calculate = tk.Button(main_frame, text="Calculate", command=self.start_secant, 
                                 bg="#4CAF50", fg="white", font=('Arial', 10, 'bold'))
        btn_calculate.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Results tab
        results_tab = tk.Frame(self.notebook, bg="#f0f2f5")
        self.notebook.add(results_tab, text="Results")
        
        self.result_box = scrolledtext.ScrolledText(results_tab, width=90, height=15, 
                                                   wrap=tk.WORD, font=('Arial', 10), bg="white")
        self.result_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Root display
        self.root_result_label = tk.Label(results_tab, text="", bg="#f0f2f5", 
                                         font=('Arial', 12, 'bold'), fg="#388E3C")
        self.root_result_label.pack(pady=5)
        
        # Calculations tab
        calculations_tab = tk.Frame(self.notebook, bg="#f0f2f5")
        self.notebook.add(calculations_tab, text="Calculations")
        
        self.calc_box = scrolledtext.ScrolledText(calculations_tab, width=90, height=15, 
                                                wrap=tk.WORD, font=('Arial', 10), bg="white")
        self.calc_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Example function button
        btn_example = tk.Button(main_frame, text="Load Example", command=self.load_example, 
                               bg="#2196F3", fg="white", font=('Arial', 10))
        btn_example.pack(pady=5)
    
    def load_example(self):
        self.function_entry.delete(0, tk.END)
        self.function_entry.insert(0, "2*x**3 - 11.7*x**2 + 17.7*x - 5")
        self.xi_minus1_entry.delete(0, tk.END)
        self.xi_minus1_entry.insert(0, "3")
        self.xi_entry.delete(0, tk.END)
        self.xi_entry.insert(0, "4")
        self.eps_entry.delete(0, tk.END)
        self.eps_entry.insert(0, "0.5")
        self.max_iter_entry.delete(0, tk.END)
        self.max_iter_entry.insert(0, "50")
    
    def evaluate_function(self, func_str, x_val):
        """Evaluates the user-defined function at a given x value."""
        x = x_val
        try:
            return eval(func_str, {'x': x, 'math': math, 'exp': math.exp, 'log': math.log, 
                                 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                                 'sqrt': math.sqrt})
        except Exception as e:
            messagebox.showerror("Error", f"Invalid function: {e}")
            return None
    
    def secant_method(self, func_str, xi_minus1, xi, eps, max_iter):
        """Performs the secant method to find the root of the function."""
        self.result_box.delete(1.0, tk.END)
        self.calc_box.delete(1.0, tk.END)
        self.root_result_label.config(text="")
        
        f_xi_minus1 = self.evaluate_function(func_str, xi_minus1)
        f_xi = self.evaluate_function(func_str, xi)
        
        if f_xi_minus1 is None or f_xi is None:
            return None
        
        # Display initial points
        self.display_iteration(0, xi_minus1, xi, f_xi_minus1, f_xi, float('inf'))
        self.display_calculations(0, xi_minus1, xi, f_xi_minus1, f_xi, None, None,float('inf'))
        
        for iter_count in range(1, max_iter + 1):
            # Check for division by zero
            if abs(f_xi_minus1 - f_xi) < 1e-20:
                messagebox.showerror("Error", "Division by zero detected in Secant Method.")
                return None
            
            # Secant formula
            xi_plus1 = xi - (f_xi * (xi_minus1 - xi)) / (f_xi_minus1 - f_xi)
            f_xi_plus1 = self.evaluate_function(func_str, xi_plus1)
            
            if f_xi_plus1 is None:
                return None
            
            # Calculate error
            error = abs((xi_plus1 - xi) / xi_plus1) * 100 if xi_plus1 != 0 else float('inf')
            
            # Display iteration results
            self.display_iteration(iter_count, xi, xi_plus1, f_xi, f_xi_plus1, error)
            
            # Show calculations for this step
            self.display_calculations(iter_count, xi_minus1, xi, f_xi_minus1, f_xi, xi_plus1, f_xi_plus1, error)
            
            # Check stopping criteria
            if error <= eps:
                self.root_result_label.config(text=f"Root found: {xi_plus1:.8f} (after {iter_count} iterations)", fg="#388E3C")
                return xi_plus1
            
            # Update points for next iteration
            xi_minus1, f_xi_minus1 = xi, f_xi
            xi, f_xi = xi_plus1, f_xi_plus1
        
        messagebox.showwarning("Warning", f"Maximum iterations ({max_iter}) reached without convergence.")
        self.root_result_label.config(text=f"Approximate root: {xi:.8f} (max iterations reached)", fg="#FF5722")
        return xi
    
    def display_iteration(self, iter_count, xi_minus1, xi, f_xi_minus1, f_xi, error):
        """Displays the iteration results in the results tab."""
        result_text = (f"Iteration {iter_count}:\n"
                      f"xi-1 = {xi_minus1:.8f}, f(xi-1) = {f_xi_minus1:.8f}\n"
                      f"xi = {xi:.8f}, f(xi) = {f_xi:.8f}\n"
                      f"Error = {error:.8f}%\n\n" if iter_count != 0 else
                      f"Iteration {iter_count} (Initial points):\n"
                      f"xi-1 = {xi_minus1:.8f}, f(xi-1) = {f_xi_minus1:.8f}\n"
                      f"xi = {xi:.8f}, f(xi) = {f_xi:.8f}\n"
                      f"Error = -\n\n")
        
        self.result_box.insert(tk.END, result_text)
        self.result_box.see(tk.END)
    
    def display_calculations(self, iter_count, xi_minus1, xi, f_xi_minus1, f_xi, xi_plus1, f_xi_plus1, error):
        """Shows the detailed calculations for each step in the calculations tab."""
        if iter_count == 0:
            calc_text = (f"Initial points:\n"
                        f"x0 = {xi_minus1:.8f}, f(x0) = {f_xi_minus1:.8f}\n"
                        f"x1 = {xi:.8f}, f(x1) = {f_xi:.8f}\n\n")
        else:
            denominator = f_xi_minus1 - f_xi
            calc_text = (f"Step {iter_count}:\n"
                        f"1. Calculate denominator: f(xi-1) - f(xi) = {f_xi_minus1:.8f} - {f_xi:.8f} = {denominator:.8f}\n"
                        f"2. Calculate numerator: f(xi)*(xi-1 - xi) = {f_xi:.8f} * ({xi_minus1:.8f} - {xi:.8f}) = {f_xi*(xi_minus1-xi):.8f}\n"
                        f"3. Calculate xi+1 = xi - numerator/denominator = {xi:.8f} - {f_xi*(xi_minus1-xi):.8f}/{denominator:.8f} = {xi_plus1:.8f}\n"
                        f"4. Evaluate f(xi+1) = {f_xi_plus1:.8f}\n"
                        f"5. Evaluate error = abs(xi_plus1 - xi) / xi_plus1) * 100 = abs(({xi_plus1:.8f}-{xi:.8f})/{xi_plus1:.8f})*100 = {error:.8f}%\n\n")
                        
        
        self.calc_box.insert(tk.END, calc_text)
        self.calc_box.see(tk.END)
    
    def start_secant(self):
        """Starts the secant method calculation with user inputs."""
        func_str = self.function_entry.get()
        try:
            xi_minus1 = float(self.xi_minus1_entry.get())
            xi = float(self.xi_entry.get())
            eps = float(self.eps_entry.get())
            max_iter = int(self.max_iter_entry.get())
            
            if max_iter <= 0:
                messagebox.showerror("Error", "Maximum iterations must be a positive integer.")
                return
            
            if xi_minus1 == xi:
                messagebox.showerror("Error", "Initial guesses must be different.")
                return
            
            # Check initial points
            f_xi_minus1 = self.evaluate_function(func_str, xi_minus1)
            f_xi = self.evaluate_function(func_str, xi)
            
            if f_xi_minus1 is None or f_xi is None:
                return
            
            self.secant_method(func_str, xi_minus1, xi, eps, max_iter)
            
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def run():
    root = tk.Toplevel()
    app = SecantCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    run()
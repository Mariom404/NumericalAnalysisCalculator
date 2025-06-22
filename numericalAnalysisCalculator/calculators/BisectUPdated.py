import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math

class BisectionCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Bisection Method Calculator")
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
        
        # Bounds and tolerance
        tk.Label(input_frame, text="Lower bound (xl):", bg="#f0f2f5", font=('Arial', 10)).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.xl_entry = tk.Entry(input_frame, font=('Arial', 10))
        self.xl_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        tk.Label(input_frame, text="Upper bound (xu):", bg="#f0f2f5", font=('Arial', 10)).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.xu_entry = tk.Entry(input_frame, font=('Arial', 10))
        self.xu_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        tk.Label(input_frame, text="Error tolerance (ε):", bg="#f0f2f5", font=('Arial', 10)).grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.eps_entry = tk.Entry(input_frame, font=('Arial', 10))
        self.eps_entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        tk.Label(input_frame, text="Max iterations:", bg="#f0f2f5", font=('Arial', 10)).grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.max_iter_entry = tk.Entry(input_frame, font=('Arial', 10))
        self.max_iter_entry.grid(row=4, column=1, sticky='w', padx=5, pady=5)
        
        # Calculate button
        btn_calculate = tk.Button(main_frame, text="Calculate", command=self.start_bisection, 
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
        self.function_entry.insert(0, "4*x**3 - 6*x**2 + 7*x - 2.3")
        self.xl_entry.delete(0, tk.END)
        self.xl_entry.insert(0, "0")
        self.xu_entry.delete(0, tk.END)
        self.xu_entry.insert(0, "1")
        self.eps_entry.delete(0, tk.END)
        self.eps_entry.insert(0, "1.0")
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
    
    def bisection_method(self, func_str, xl, xu, eps, max_iter):
        """Performs the bisection method to find the root of the function."""
        self.result_box.delete(1.0, tk.END)
        self.calc_box.delete(1.0, tk.END)
        self.root_result_label.config(text="")
        
        f_xl = self.evaluate_function(func_str, xl)
        f_xu = self.evaluate_function(func_str, xu)
        
        if f_xl is None or f_xu is None:
            return None
        
        if f_xl * f_xu > 0:
            messagebox.showerror("Error", "Invalid input: f(xl) and f(xu) must have opposite signs.")
            return None
        
        xrold = None
        for iter_count in range(1, max_iter + 1):
            xr = (xl + xu) / 2.0
            f_xr = self.evaluate_function(func_str, xr)
            
            if f_xr == 0:
                error = 0.0
            else:
                error = abs((xr - xrold) / xr) * 100 if xrold is not None else float('inf')
            
            # Display iteration results
            self.display_iteration(iter_count, xl, xu, xr, f_xl, f_xu, f_xr, error)
            
            # Show calculations for this step
            self.display_calculations(iter_count, xl, xu, xr, f_xl, f_xu, f_xr, xrold, error)
            
            # Check stopping criteria
            if error is not None and error <= eps:
                self.root_result_label.config(text=f"Root found: {xr:.8f} (after {iter_count} iterations)", fg="#388E3C")
                return xr
            
            # Update bounds for next iteration
            if f_xl * f_xr < 0:
                xu, f_xu = xr, f_xr
            else:
                xl, f_xl = xr, f_xr
            
            xrold = xr
        
        messagebox.showwarning("Warning", f"Maximum iterations ({max_iter}) reached without convergence.")
        self.root_result_label.config(text=f"Approximate root: {xrold:.8f} (max iterations reached)", fg="#FF5722")
        return xrold
    
    def display_iteration(self, iter_count, xl, xu, xr, f_xl, f_xu, f_xr, error):
        """Displays the iteration results in the results tab."""
        result_text = (f"Iteration {iter_count}:\n"
                      f"xl = {xl:.8f}, f(xl) = {f_xl:.8f}\n"
                      f"xu = {xu:.8f}, f(xu) = {f_xu:.8f}\n"
                      f"xr = {xr:.8f}, f(xr) = {f_xr:.8f}\n"
                      f"Error = {error:.8f}%\n\n") 
        self.result_box.insert(tk.END, result_text)
        self.result_box.see(tk.END)
    
    def display_calculations(self, iter_count, xl, xu, xr, f_xl, f_xu, f_xr,xrold, error):
        """Shows the detailed calculations for each step in the calculations tab."""
        calc_text = (f"Step {iter_count}:\n"
                    f"1. Calculate xr = (xl + xu)/2 = ({xl:.8f} + {xu:.8f})/2 = {xr:.8f}\n"
                    f"2. Evaluate f(xr) = {f_xr:.8f}\n"
                    f"3. Evaluate error = abs((xr - xrold) / xr) * 100 = abs(({xr:.8f}-{xrold:.8f})/{xr:.8f})*100 = {error:.8f}%\n "
                    f"4. Check sign:\n"
                    f"   - f(xl) = {f_xl:.8f}, f(xr) = {f_xr:.8f}\n"
                    f"   - Product f(xl)*f(xr) = {f_xl*f_xr:.8f}\n" 
                    
                    if iter_count != 1 else
                    f"Step {iter_count}:\n"
                    f"1. Calculate xr = (xl + xu)/2 = ({xl:.8f} + {xu:.8f})/2 = {xr:.8f}\n"
                    f"2. Evaluate f(xr) = {f_xr:.8f}\n"
                    f"3. Check sign:\n"
                    f"   - f(xl) = {f_xl:.8f}, f(xr) = {f_xr:.8f}\n"
                    f"   - Product f(xl)*f(xr) = {f_xl*f_xr:.8f}\n" )
        
        if f_xl * f_xr < 0:
            calc_text += "   - Sign change detected between xl and xr\n"
            calc_text += "   - New interval: [xl, xr]\n"
        else:
            calc_text += "   - No sign change between xl and xr\n"
            calc_text += "   - New interval: [xr, xu]\n"
        
        calc_text += "\n"
        self.calc_box.insert(tk.END, calc_text)
        self.calc_box.see(tk.END)
    
    def start_bisection(self):
        """Starts the bisection method calculation with user inputs."""
        func_str = self.function_entry.get()
        try:
            xl = float(self.xl_entry.get())
            xu = float(self.xu_entry.get())
            eps = float(self.eps_entry.get())
            max_iter = int(self.max_iter_entry.get())
            
            if max_iter <= 0:
                messagebox.showerror("Error", "Maximum iterations must be a positive integer.")
                return
            
            if xl >= xu:
                messagebox.showerror("Error", "Lower bound must be less than upper bound.")
                return
            
            # Check initial bounds
            f_xl = self.evaluate_function(func_str, xl)
            f_xu = self.evaluate_function(func_str, xu)
            
            if f_xl is None or f_xu is None:
                return
            
            if f_xl * f_xu >= 0:
                messagebox.showerror("Error", "The function must have opposite signs at the bounds.")
                return
            
            self.bisection_method(func_str, xl, xu, eps, max_iter)
            
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def run():
    root = tk.Toplevel()
    app = BisectionCalculator(root)
    root.mainloop()
    
if __name__ == "__main__":
    run()
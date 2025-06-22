import tkinter as tk
from tkinter import ttk
import math

class GoldenSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Golden Section Search")
        self.R = (math.sqrt(5) - 1)/2  # Golden ratio
        self.root.resizable(False, False)
        
        # Variables
        self.function_str = tk.StringVar(value="2*sin(x) - x**2/10")
        self.xl_var = tk.StringVar(value="0")
        self.xu_var = tk.StringVar(value="4")
        self.max_iter_var = tk.StringVar(value="8")
        self.optimization_type = tk.StringVar(value="max")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        mainframe = ttk.Frame(self.root, padding="10")
        mainframe.grid(row=0, column=0, sticky="nsew")
        
        # Input Frame
        input_frame = ttk.LabelFrame(mainframe, text="Parameters", padding="10")
        input_frame.grid(row=0, column=0, sticky="ew", pady=5)
        
        ttk.Label(input_frame, text="f(x):").grid(row=0, column=0, sticky="w")
        ttk.Entry(input_frame, textvariable=self.function_str, width=25).grid(row=0, column=1, sticky="ew")
        
        ttk.Label(input_frame, text="Lower bound (xl):").grid(row=1, column=0, sticky="w")
        ttk.Entry(input_frame, textvariable=self.xl_var, width=10).grid(row=1, column=1, sticky="w")
        
        ttk.Label(input_frame, text="Upper bound (xu):").grid(row=2, column=0, sticky="w")
        ttk.Entry(input_frame, textvariable=self.xu_var, width=10).grid(row=2, column=1, sticky="w")
        
        ttk.Label(input_frame, text="Max iterations:").grid(row=3, column=0, sticky="w")
        ttk.Entry(input_frame, textvariable=self.max_iter_var, width=10).grid(row=3, column=1, sticky="w")
        
        ttk.Radiobutton(input_frame, text="Maximize", variable=self.optimization_type, 
                       value="max").grid(row=4, column=0, sticky="w")
        ttk.Radiobutton(input_frame, text="Minimize", variable=self.optimization_type, 
                       value="min").grid(row=4, column=1, sticky="w")
        
        ttk.Button(mainframe, text="Run", command=self.run).grid(row=1, column=0, pady=10)
        
        # Results Notebook
        self.notebook = ttk.Notebook(mainframe)
        self.notebook.grid(row=2, column=0, sticky="nsew")
        
        # Results Table Tab
        table_frame = ttk.Frame(self.notebook)
        self.notebook.add(table_frame, text="Results")
        
        cols = ("Iter", "xl", "f(xl)", "x1", "f(x1)", "x2", "f(x2)", "xu", "f(xu)", "d")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=10)
        for col in cols:
            self.tree.column(col, width=70, anchor="center")
            self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Calculation Steps Tab
        self.steps_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.steps_frame, text="Calculation Steps")
        
        self.steps_text = tk.Text(self.steps_frame, wrap="word", width=80, height=15)
        scrollbar = ttk.Scrollbar(self.steps_frame, command=self.steps_text.yview)
        self.steps_text.configure(yscrollcommand=scrollbar.set)
        
        self.steps_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Result Label
        self.result_var = tk.StringVar()
        ttk.Label(mainframe, textvariable=self.result_var, font=('TkDefaultFont', 10, 'bold')).grid(row=3, column=0, sticky="w")
    
    def evaluate(self, x):
        """Safely evaluate the function at point x"""
        safe_dict = {**{f: getattr(math, f) for f in ['sin', 'cos', 'tan', 'sqrt', 'exp', 'log']},
                    'pi': math.pi, 'e': math.e, 'x': x}
        return eval(self.function_str.get(), {"__builtins__": None}, safe_dict)
    
    def run(self):
        """Run the golden section search algorithm"""
        # Clear previous results
        self.tree.delete(*self.tree.get_children())
        self.steps_text.delete(1.0, tk.END)
        
        try:
            # Get and validate inputs
            xl, xu = float(self.xl_var.get()), float(self.xu_var.get())
            if xl >= xu:
                raise ValueError("Lower bound must be less than upper bound")
            
            max_iter = int(self.max_iter_var.get())
            maximize = self.optimization_type.get() == "max"
            
            # Initial setup
            d = self.R * (xu - xl)
            x1, x2 = xl + d, xu - d
            fx1, fx2 = self.evaluate(x1), self.evaluate(x2)
            
            # Initial steps documentation
            self.steps_text.insert(tk.END, "=== INITIAL SETUP ===\n")
            self.steps_text.insert(tk.END, f"R = (√5-1)/2 ≈ {self.R:.6f}\n")
            self.steps_text.insert(tk.END, f"Initial interval: [{xl:.6f}, {xu:.6f}]\n")
            self.steps_text.insert(tk.END, f"d = R*(xu-xl) = {d:.6f}\n")
            self.steps_text.insert(tk.END, f"x1 = xl+d = {x1:.6f}, f(x1) = {fx1:.6f}\n")
            self.steps_text.insert(tk.END, f"x2 = xu-d = {x2:.6f}, f(x2) = {fx2:.6f}\n\n")
            
            # Main iteration loop
            for i in range(max_iter):
                fxl, fxu = self.evaluate(xl), self.evaluate(xu)
                
                # Add to results table
                self.tree.insert("", "end", values=(
                    i+1, f"{xl:.6f}", f"{fxl:.6f}", f"{x1:.6f}", f"{fx1:.6f}",
                    f"{x2:.6f}", f"{fx2:.6f}", f"{xu:.6f}", f"{fxu:.6f}", f"{d:.6f}"
                ))
                
                # Document this iteration
                self.steps_text.insert(tk.END, f"=== ITERATION {i+1} ===\n")
                self.steps_text.insert(tk.END, f"Current: xl={xl:.6f}, x1={x1:.6f}, x2={x2:.6f}, xu={xu:.6f}\n")
                self.steps_text.insert(tk.END, f"Values: f(x1)={fx1:.6f}, f(x2)={fx2:.6f}\n")
                
                if (maximize and fx1 > fx2) or (not maximize and fx1 < fx2):
                    self.steps_text.insert(tk.END, f"Keep LEFT interval (f(x1) {'>' if maximize else '<'} f(x2))\n")
                    xl, x2, fx2 = x2, x1, fx1
                    d = self.R * (xu - xl)
                    x_opt= x1
                    f_opt= fx1
                    x1 = xl + d
                    fx1 = self.evaluate(x1)
                else:
                    self.steps_text.insert(tk.END, f"Keep RIGHT interval (f(x1) {'<=' if maximize else '>='} f(x2))\n")
                    xu, x1, fx1 = x1, x2, fx2
                    d = self.R * (xu - xl)
                    x_opt= x2
                    f_opt= fx2
                    x2 = xu - d
                    fx2 = self.evaluate(x2)
                
                self.steps_text.insert(tk.END, f"New interval: [{xl:.6f}, {xu:.6f}]\n")
                self.steps_text.insert(tk.END, f"New d = {d:.6f}, x1 = {x1:.6f}, x2 = {x2:.6f}\n\n")
            
            # Final result
            result = f"{'Maximum' if maximize else 'Minimum'} at x = {x_opt:.6f}, f(x) = {f_opt:.6f}"
            self.result_var.set(result)
                                                
            self.steps_text.insert(tk.END, "=== FINAL RESULT ===\n")
            self.steps_text.insert(tk.END, f"Final interval: [{xl:.6f}, {xu:.6f}]\n")
            self.steps_text.insert(tk.END, f"Optimal x ≈ {x_opt:.6f}\n")
            self.steps_text.insert(tk.END, f"f(x) = {f_opt:.6f}\n")
            self.steps_text.insert(tk.END, f"\nRESULT: {result}\n")
            self.steps_text.see(1.0)
            
            self.notebook.select(self.steps_frame)
            
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")

def run():
    root = tk.Toplevel()
    app = GoldenSearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    run()
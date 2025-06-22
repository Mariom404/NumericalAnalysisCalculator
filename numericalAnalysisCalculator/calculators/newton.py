import tkinter as tk
from tkinter import ttk, messagebox
import math

class NewtonMethodCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Newton's Method Calculator")
        self.root.geometry("700x600")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Newton's Method Root Finder", 
                 font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0,15))
        
        # Function input
        ttk.Label(main_frame, text="Function f(x):").grid(row=1, column=0, sticky=tk.W, pady=(0,5))
        self.function_entry = ttk.Entry(main_frame, width=40)
        self.function_entry.grid(row=1, column=1, sticky=tk.W, pady=(0,5))
        self.function_entry.insert(0, "-0.9*x**2 + 1.7*x + 2.5")  # Default example
        
        # Derivative input
        ttk.Label(main_frame, text="Derivative f'(x):").grid(row=2, column=0, sticky=tk.W, pady=(0,5))
        self.derivative_entry = ttk.Entry(main_frame, width=40)
        self.derivative_entry.grid(row=2, column=1, sticky=tk.W, pady=(0,5))
        self.derivative_entry.insert(0, "-1.8*x + 1.7")  # Default example
        
        # Parameters frame
        params_frame = ttk.LabelFrame(main_frame, text="Parameters", padding=10)
        params_frame.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(10,5))
        
        # Initial guess
        ttk.Label(params_frame, text="Initial guess (x₀):").grid(row=0, column=0, sticky=tk.W)
        self.x0_entry = ttk.Entry(params_frame, width=15)
        self.x0_entry.grid(row=0, column=1, sticky=tk.W, padx=(5,15))
        self.x0_entry.insert(0, "5.0")
        
        # Tolerance
        ttk.Label(params_frame, text="Tolerance:").grid(row=0, column=2, sticky=tk.W)
        self.tol_entry = ttk.Entry(params_frame, width=15)
        self.tol_entry.grid(row=0, column=3, sticky=tk.W, padx=(5,15))
        self.tol_entry.insert(0, "0.7")
        
        # Max iterations
        ttk.Label(params_frame, text="Max iterations:").grid(row=0, column=4, sticky=tk.W)
        self.max_iter_entry = ttk.Entry(params_frame, width=15)
        self.max_iter_entry.grid(row=0, column=5, sticky=tk.W)
        self.max_iter_entry.insert(0, "100")
        
        # Calculate button
        self.calc_button = ttk.Button(main_frame, text="Calculate", command=self.calculate)
        self.calc_button.grid(row=4, column=0, columnspan=2, pady=(15,10))
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Iterations", padding=10)
        results_frame.grid(row=5, column=0, columnspan=2, sticky=tk.NSEW, pady=(5,10))
        
        # Configure grid weights for resizing
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Treeview for displaying iterations
        self.tree = ttk.Treeview(results_frame, 
                               columns=('Iter', 'x_n', 'f(x_n)', 'fDash(x_n)', 'Error'), 
                               show='headings', 
                               height=12)
        
        # Configure columns
        self.tree.heading('Iter', text='Iteration')
        self.tree.heading('x_n', text='xₙ')
        self.tree.heading('f(x_n)', text='f(xₙ)')
        self.tree.heading('fDash(x_n)', text='fDash(xₙ)')
        self.tree.heading('Error', text='Error')
        
        self.tree.column('Iter', width=70, anchor=tk.CENTER)
        self.tree.column('x_n', width=140, anchor=tk.CENTER)
        self.tree.column('f(x_n)', width=140, anchor=tk.CENTER)
        self.tree.column('fDash(x_n)', width=140, anchor=tk.CENTER)
        self.tree.column('Error', width=140, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Grid the tree and scrollbar
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        
        # Final result
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=6, column=0, columnspan=2, sticky=tk.EW, pady=(5,0))
        
        ttk.Label(result_frame, text="Approximate root:", font=('Arial', 10)).pack(side=tk.LEFT)
        self.result_var = tk.StringVar()
        ttk.Label(result_frame, textvariable=self.result_var, 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(5,0))
        
    def calculate(self):
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.result_var.set("")
        
        try:
            # Get inputs
            func_str = self.function_entry.get()
            df_str = self.derivative_entry.get()
            x0 = float(self.x0_entry.get())
            tol = float(self.tol_entry.get())
            max_iter = int(self.max_iter_entry.get())
            
            # Initialize variables
            x = x0
            converged = False
            result = None
            x_prev= 0
            
            for i in range(max_iter):
                # Evaluate function and derivative
                fx = eval(func_str, {'x': x, 'math': math})
                dfx = eval(df_str, {'x': x, 'math': math})
                
                if abs(dfx) < 1e-15:
                    messagebox.showwarning("Warning", "Derivative is zero. Method cannot continue.")
                    return
                
                
                # Calculate next value
                x_next = x - (fx / dfx)
                
                error = abs((x - x_prev)/x)*100 
                
                x_prev = x
                # Format values for display
                def format_num(num):
                    if abs(num) < 1e-4 or abs(num) > 1e6:
                        return "{:.6e}".format(num)
                    return "{:.8f}".format(num)
                
                # Add to treeview
                if i > 0 :    
                    self.tree.insert('', tk.END, 
                                    values=(i, 
                                           format_num(x),
                                           format_num(fx),
                                           format_num(dfx),
                                           format_num(error)))
                else : 
                    self.tree.insert('', tk.END, 
                                    values=(i, 
                                           format_num(x),
                                           format_num(fx),
                                           format_num(dfx)))                
                
                
                # Check convergence
                if error < tol:
                    converged = True
                    result = x
                    break
                 
                x = x_next
            
            # Display final result
            if result is None:
                result = x  # In case max_iter reached
                
            if converged:
                self.result_var.set(f"{format_num(result)} (Converged after {i+1} iterations)")
            else:
                self.result_var.set(f"{format_num(result)} (Max iterations reached)")
            
            # Auto-scroll to the bottom
            self.tree.yview_moveto(1)
            
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def run():
    root = tk.Toplevel()
    app = NewtonMethodCalculator(root)
    
    # Set minimum window size
    root.minsize(650, 550)
    
    # Center the window
    window_width = 700
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    root.mainloop()
if __name__ == "__main__":
    run()
import tkinter as tk
from tkinter import ttk
from calculators import BisectUPdated, FalsePosUpdated, newton, secantUpdated, GE, LUDec, goldenSectionSearch

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator Launcher")
        self.root.geometry("400x400")
        
        self.create_widgets()
    
    def create_widgets(self):
        ttk.Label(self.root, text="Select Calculator Type", font=('Arial', 16)).pack(pady=20)
        
        # Create buttons for each calculator
        calculators = [
            ("Bisection Method", BisectUPdated.run),
            ("The False Position Method", FalsePosUpdated.run),
            ("Newton Method", newton.run),
            ("Secant Method", secantUpdated.run),
            ("Gauss Elimination", GE.run),
            ("LU Decomposistion", LUDec.run),
            ("Golden-Section Search", goldenSectionSearch.run)
        ]
        
        for name, command in calculators:
            ttk.Button(
                self.root, 
                text=name, 
                command=command,
                width=40
            ).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
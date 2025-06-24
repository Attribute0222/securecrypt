import tkinter as tk
from tkinter import ttk
from typing import Optional

class PasswordEntry(ttk.Frame):
    """Secure password entry with toggle visibility"""
    def __init__(self, master, show_char: str = "•", **kwargs):
        super().__init__(master)
        self.password_var = tk.StringVar()
        
        self.entry = ttk.Entry(
            self, 
            textvariable=self.password_var, 
            show=show_char,
            **kwargs
        )
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.toggle_btn = ttk.Button(
            self, 
            text="👁", 
            width=3,
            command=self.toggle_visibility
        )
        self.toggle_btn.pack(side=tk.RIGHT)
    
    def toggle_visibility(self):
        current_show = self.entry.cget("show")
        self.entry.config(show="" if current_show else "•")
        self.toggle_btn.config(text="👁" if current_show else "🔒")
    
    def get(self) -> str:
        return self.password_var.get()

class ProgressDialog(tk.Toplevel):
    """Animated progress dialog"""
    def __init__(self, master, title: str = "Processing...", width: int = 300):
        super().__init__(master)
        self.title(title)
        self.geometry(f"{width}x100")
        self.resizable(False, False)
        
        # Center dialog
        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() - width) // 2
        y = master.winfo_y() + (master.winfo_height() - 100) // 2
        self.geometry(f"+{x}+{y}")
        
        self.progress = ttk.Progressbar(
            self, 
            orient="horizontal",
            length=width-20,
            mode="indeterminate"
        )
        self.progress.pack(pady=20)
        
        self.label = ttk.Label(self, text=title)
        self.label.pack()
        
        self.progress.start(10)  # Start animation
    
    def update_status(self, text: str):
        self.label.config(text=text)
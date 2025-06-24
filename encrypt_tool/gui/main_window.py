import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..core import AESCipher
from ..utils.file_io import get_output_filename
from .widgets import PasswordEntry, ProgressDialog
import threading

class EncryptionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔒 SecureCrypt - AES-256 Tool")
        self.geometry("500x300")
        self.cipher = AESCipher()
        self._setup_ui()
        
    def _setup_ui(self):
        # Styling
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, font=('Helvetica', 10))
        self.style.configure("TLabel", font=('Helvetica', 11))
        
        # Header
        ttk.Label(self, text="Secure File Encryption", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # File Selection
        file_frame = ttk.Frame(self)
        file_frame.pack(pady=10, padx=20, fill=tk.X)
        
        ttk.Label(file_frame, text="File:").pack(side=tk.LEFT)
        self.file_entry = ttk.Entry(file_frame, width=40)
        self.file_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Browse", command=self._browse_file).pack(side=tk.LEFT)
        
        # Password
        pass_frame = ttk.Frame(self)
        pass_frame.pack(pady=10, padx=20, fill=tk.X)
        
        ttk.Label(pass_frame, text="Password:").pack(side=tk.LEFT)
        self.password_entry = PasswordEntry(pass_frame)
        self.password_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Action Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)
        
        ttk.Button(
            btn_frame, 
            text="Encrypt File", 
            style="Accent.TButton",
            command=lambda: self._run_operation("encrypt")
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            btn_frame, 
            text="Decrypt File", 
            command=lambda: self._run_operation("decrypt")
        ).pack(side=tk.LEFT, padx=10)
        
        # Status Bar
        self.status = ttk.Label(self, text="Ready", relief=tk.SUNKEN)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
    
    def _run_operation(self, mode):
        filepath = self.file_entry.get()
        password = self.password_entry.get()
        
        if not filepath:
            messagebox.showerror("Error", "Please select a file first!")
            return
            
        if not password:
            messagebox.showerror("Error", "Password cannot be empty!")
            return
            
        # Run in background thread to prevent GUI freeze
        thread = threading.Thread(
            target=self._perform_crypto_operation,
            args=(filepath, password, mode),
            daemon=True
        )
        thread.start()
    
    def _perform_crypto_operation(self, filepath, password, mode):
        try:
            progress = ProgressDialog(self, title=f"{mode.capitalize()}ing File...")
            self.status.config(text=f"{mode.capitalize()}ing...")
            
            output_file = get_output_filename(
                filepath, 
                suffix="_encrypted" if mode == "encrypt" else "_decrypted"
            )
            
            with open(filepath, 'rb') as f:
                data = f.read()
            
            if mode == "encrypt":
                result = self.cipher.encrypt(data, password)
            else:
                result = self.cipher.decrypt(data, password)
            
            with open(output_file, 'wb') as f:
                f.write(result)
            
            messagebox.showinfo(
                "Success", 
                f"File {mode}ed successfully!\nSaved as: {output_file}"
            )
            self.status.config(text="Ready")
            
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"{mode.capitalize()}ion failed:\n{str(e)}"
            )
            self.status.config(text="Failed")
        finally:
            progress.destroy()
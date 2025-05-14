import tkinter as tk
from tkinter import ttk
import dataManager
import sys
from io import StringIO

class ScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create scan entry field
        self.scan_label = ttk.Label(main_frame, text="Scan QR Code:")
        self.scan_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.scan_entry = ttk.Entry(main_frame, width=50)
        self.scan_entry.grid(row=1, column=0, padx=5, pady=5)
        self.scan_entry.focus()  # Set focus to entry field
        
        # Create data display with label
        data_label = ttk.Label(main_frame, text="Scanned Data:")
        data_label.grid(row=2, column=0, padx=5, pady=(5,0), sticky=tk.W)
        
        self.data_text = tk.Text(main_frame, height=5, width=50)
        self.data_text.grid(row=3, column=0, padx=5, pady=(0,5))
        
        # Create console output display with label
        console_label = ttk.Label(main_frame, text="Console Output:")
        console_label.grid(row=4, column=0, padx=5, pady=(5,0), sticky=tk.W)
        
        self.console_text = tk.Text(main_frame, height=5, width=50, bg='#f0f0f0')
        self.console_text.grid(row=5, column=0, padx=5, pady=(0,5))
        
        # Bind the Return key event (barcode scanners typically send Return)
        self.scan_entry.bind('<Return>', self.process_scan)

    def process_scan(self, event=None):
        # Get the scanned data
        scanned_data = self.scan_entry.get().strip()
        
        try:
            # Parse scanned data
            mac, serial, date, version = scanned_data.split(',')
            
            # Update the display
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, f"MAC Address: {mac}\n")
            self.data_text.insert(tk.END, f"Serial: {serial}\n")
            self.data_text.insert(tk.END, f"Date: {date}\n")
            self.data_text.insert(tk.END, f"Version: {version}\n")
            
            # Capture console output
            old_stdout = sys.stdout
            console_output = StringIO()
            sys.stdout = console_output
            
            # Update the CSV file
            dataManager.append_data(mac, serial, date, version)
            
            # Restore stdout and get the output
            sys.stdout = old_stdout
            output = console_output.getvalue()
            
            # Update console display
            self.console_text.delete(1.0, tk.END)
            self.console_text.insert(tk.END, output)
            
        except Exception as e:
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, f"Error processing scanned code: {str(e)}")
            self.console_text.delete(1.0, tk.END)
            self.console_text.insert(tk.END, f"Error: {str(e)}")
        
        # Clear the entry field for next scan
        self.scan_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = ScannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

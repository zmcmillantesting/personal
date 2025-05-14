import tkinter as tk
from tkinter import ttk
import dataManager
import sys
from io import StringIO

class DataManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Manager Application")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create Scanner tab
        self.scanner_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.scanner_frame, text='Scanner')
        self.setup_scanner_tab()
        
        # Create Data View tab
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text='Current Data')
        self.setup_data_tab()

    def setup_scanner_tab(self):
        # Create scan entry field
        scan_label = ttk.Label(self.scanner_frame, text="Scan QR Code:")
        scan_label.pack(pady=(10,0))
        
        self.scan_entry = ttk.Entry(self.scanner_frame, width=50)
        self.scan_entry.pack(pady=5)
        self.scan_entry.focus()
        
        # Create data display
        data_label = ttk.Label(self.scanner_frame, text="Scanned Data:")
        data_label.pack(pady=(10,0))
        
        self.data_text = tk.Text(self.scanner_frame, height=5, width=50)
        self.data_text.pack(pady=5)
        
        # Create console output display
        console_label = ttk.Label(self.scanner_frame, text="Console Output:")
        console_label.pack(pady=(10,0))
        
        self.console_text = tk.Text(self.scanner_frame, height=5, width=50, bg='#f0f0f0')
        self.console_text.pack(pady=5)
        
        # Bind the Return key event
        self.scan_entry.bind('<Return>', self.process_scan)

    def setup_data_tab(self):
        # Create current data display
        current_data_label = ttk.Label(self.data_frame, text="Current Record in Database:")
        current_data_label.pack(pady=(10,0))
        
        self.current_data_text = tk.Text(self.data_frame, height=5, width=50)
        self.current_data_text.pack(pady=5)
        
        # Refresh button
        refresh_button = ttk.Button(self.data_frame, text="Refresh Data", command=self.refresh_current_data)
        refresh_button.pack(pady=5)
        
        # Initial data load
        self.refresh_current_data()

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
            
            # Refresh the current data tab
            self.refresh_current_data()
            
        except Exception as e:
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, f"Error processing scanned code: {str(e)}")
            self.console_text.delete(1.0, tk.END)
            self.console_text.insert(tk.END, f"Error: {str(e)}")
        
        # Clear the entry field for next scan
        self.scan_entry.delete(0, tk.END)

    def refresh_current_data(self):
        current_record = dataManager.get_last_record()
        self.current_data_text.delete(1.0, tk.END)
        
        if current_record:
            mac, serial, date, version = current_record
            self.current_data_text.insert(tk.END, f"MAC Address: {mac}\n")
            self.current_data_text.insert(tk.END, f"Serial: {serial}\n")
            self.current_data_text.insert(tk.END, f"Date: {date}\n")
            self.current_data_text.insert(tk.END, f"Version: {version}\n")
        else:
            self.current_data_text.insert(tk.END, "No data available")

def main():
    root = tk.Tk()
    app = DataManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

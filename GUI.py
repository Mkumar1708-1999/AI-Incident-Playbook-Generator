import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests

API_URL = "http://localhost:8001/summarize"

def get_summary(email_content):
    response = requests.post(API_URL, json={"email_content": email_content})
    if response.status_code == 200:
        return response.json().get("summary")
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

def summarize_input():
    email_content = input_text.get("1.0", tk.END).strip()
    if not email_content:
        messagebox.showwarning("Input Missing", "Please enter incident details.")
        return
    try:
        summary = get_summary(email_content)
        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, summary)
        output_text.config(state='disabled')
    except Exception as e:
        messagebox.showerror("API Error", str(e))

# GUI setup
root = tk.Tk()
root.title("AI Incident Summarizer")

# Input Label
tk.Label(root, text="Enter AI Incident Detail:").pack(anchor='w', padx=10, pady=(10, 0))

# Input Text Area
input_text = scrolledtext.ScrolledText(root, height=8, width=80, wrap=tk.WORD)
input_text.pack(padx=10, pady=5)

# Submit Button
tk.Button(root, text="Generate Summary", command=summarize_input).pack(pady=10)

# Output Label
tk.Label(root, text="Generated Summary:").pack(anchor='w', padx=10, pady=(5, 0))

# Output Text Area (Read-only)
output_text = scrolledtext.ScrolledText(root, height=8, width=80, wrap=tk.WORD, state='disabled')
output_text.pack(padx=10, pady=(0, 10))

root.mainloop()

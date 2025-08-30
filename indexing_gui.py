import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import os

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

class IndexingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Indexing API Tool")
        self.root.geometry("700x500")

        self.credentials = None
        self.http = None
        self.urls = []
        self.current_index = 0

        # JSON File Selection
        self.json_label = tk.Label(root, text="Select Service Account JSON:")
        self.json_label.pack(pady=5)

        self.json_path_var = tk.StringVar()
        self.json_entry = tk.Entry(root, textvariable=self.json_path_var, width=60)
        self.json_entry.pack(pady=5)

        self.json_button = tk.Button(root, text="Browse", command=self.browse_json)
        self.json_button.pack(pady=5)

        self.owner_label = tk.Label(root, text="Service Account Email: Not Loaded")
        self.owner_label.pack(pady=5)

        # URLs Input
        self.urls_label = tk.Label(root, text="Enter URLs (one per line):")
        self.urls_label.pack(pady=5)

        self.urls_text = scrolledtext.ScrolledText(root, width=80, height=10)
        self.urls_text.pack(pady=5)

        # Start Button
        self.start_button = tk.Button(root, text="Start Indexing", command=self.start_indexing, bg="green", fg="white")
        self.start_button.pack(pady=10)

        # Logs
        self.log_label = tk.Label(root, text="Logs:")
        self.log_label.pack(pady=5)

        self.log_text = scrolledtext.ScrolledText(root, width=80, height=10, state="disabled")
        self.log_text.pack(pady=5)

    def browse_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if path:
            self.json_path_var.set(path)
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    email = data.get("client_email", "Not found in JSON")
                    self.owner_label.config(text=f"Service Account Email: {email}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load JSON: {e}")

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.yview(tk.END)
        self.log_text.config(state="disabled")
        self.root.update_idletasks()

    def start_indexing(self):
        json_path = self.json_path_var.get()
        if not os.path.exists(json_path):
            messagebox.showerror("Error", "Please select a valid JSON key file.")
            return

        urls = self.urls_text.get("1.0", tk.END).strip().splitlines()
        if not urls:
            messagebox.showerror("Error", "Please enter at least one URL.")
            return

        try:
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, SCOPES)
            self.http = self.credentials.authorize(httplib2.Http())
        except Exception as e:
            messagebox.showerror("Error", f"Authentication failed: {e}")
            return

        self.urls = [u.strip() for u in urls if u.strip()]
        self.current_index = 0
        self.log("🚀 Starting indexing...")
        self.root.after(100, self.process_next_url)  # start loop

    def process_next_url(self):
        if self.current_index < len(self.urls):
            url = self.urls[self.current_index]
            body = {"url": url, "type": "URL_UPDATED"}
            try:
                response, content = self.http.request(
                    ENDPOINT,
                    method="POST",
                    body=json.dumps(body),
                    headers={"Content-Type": "application/json"}
                )
                self.log(f"📌 Sent: {url}")
                self.log(f"Response: {content.decode('utf-8')}\n")
            except Exception as e:
                self.log(f"❌ Failed for {url}: {e}")

            self.current_index += 1
            # wait 1000 ms (1 sec) then send next
            self.root.after(1000, self.process_next_url)
        else:
            messagebox.showinfo("Done", "✅ Indexing requests completed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = IndexingApp(root)
    root.mainloop()

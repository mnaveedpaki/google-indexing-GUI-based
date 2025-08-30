# Google Indexing API Tool (GUI)

This is a simple **Python Tkinter-based desktop application** that allows you to send URL update requests to the **Google Indexing API** using a **Service Account JSON key**.  

With this tool, you can:  
✅ Authenticate with Google Indexing API using a service account JSON file  
✅ Enter multiple URLs at once (one per line)  
✅ Send indexing requests sequentially (1-second interval to avoid UI freeze)  
✅ View real-time logs inside the app  

---

## 🚀 Features

- GUI built with **Tkinter**
- Select Google API **Service Account JSON** file easily
- Automatically extracts and displays the **Service Account email**
- Submit multiple URLs at once
- Built-in logs viewer for request/response tracking
- Waits 1 second between requests (prevents UI freeze)

---

## 📦 Requirements

Make sure you have **Python 3.7+** installed.  
Install the required Python packages:

```bash
pip install oauth2client httplib2
```

---

## ⚙️ Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/mnaveedpaki/google-indexing-GUI-based.git
   cd google-indexing-GUI-based
   ```

2. Enable the **Indexing API** in your [Google Cloud Console](https://console.cloud.google.com/).

3. Create a **Service Account**, download the **JSON key file**, and save it locally.

4. Add the **Service Account email** (from JSON file) as an **Owner** in [Google Search Console](https://search.google.com/search-console).

5. Run the app:
   ```bash
   python indexing_tool.py
   ```

---

## 🖥️ Usage

1. Launch the app (`indexing_tool.py`).  
2. Click **Browse** to select your service account JSON file.  
   - The tool will display the **Service Account email**.  
3. Enter your **URLs** (one per line) in the text box.  
4. Click **Start Indexing**.  
5. Monitor logs in the log window.  

---

## 📸 Screenshot (Example)

> *(Add a screenshot here after running the app, showing JSON selection, URLs input, and logs.)*

---

## ✅ Example Log Output

```
🚀 Starting indexing...
📌 Sent: https://example.com/page1
Response: {"urlNotificationMetadata": {...}}

📌 Sent: https://example.com/page2
Response: {"urlNotificationMetadata": {...}}
✅ Indexing requests completed!
```

---

## 🔑 Notes

- The service account must be **added as an owner** in Google Search Console for the property (website) you want to index.  
- This tool uses:
  - `oauth2client` for authentication  
  - `httplib2` for API requests  
- Each URL is submitted with `type: "URL_UPDATED"`.  

---

## 📜 License

MIT License – Feel free to use and modify.  

---

👉 Repo: [google-indexing-GUI-based](https://github.com/mnaveedpaki/google-indexing-GUI-based)  

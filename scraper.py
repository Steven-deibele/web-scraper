import tkinter as tk
import tkinter.filedialog as fd
import os
import socket
import re
import ssl
from threading import Thread

def scrape_and_save(url, folder_path, status_var):
    """
    Very basic web scraper without external libraries.
    Fetches the HTML content and extracts image URLs (very rudimentary).

    Args:
        url: The URL of the webpage to scrape.
        folder_path: The path to the folder where files will be saved.
        status_var: StringVar to update the status in the UI
    """
    try:
        status_var.set("Creating folder...")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        status_var.set("Connecting to website...")
        # 1. Parse URL (very basic)
        protocol, rest = url.split("://", 1)
        if "/" not in rest:
            rest += "/"
        host, path = rest.split("/", 1)
        port = 80 if protocol == "http" else 443  # Default ports

        # 2. Make HTTP Request (very basic)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if protocol == "https":
            # Very basic SSL - doesn't verify certificates!
            context = ssl.create_default_context()
            s = context.wrap_socket(s, server_hostname=host)

        s.connect((host, port))
        request = f"GET /{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode())

        status_var.set("Downloading webpage...")
        # 3. Receive Response (very basic)
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
        s.close()

        status_var.set("Processing webpage content...")
        # 4. Separate Headers and Body (very basic)
        header_part, body_part = response.split(b"\r\n\r\n", 1)

        # 5. Save HTML Content
        html_filename = os.path.join(folder_path, "page.html")
        with open(html_filename, "wb") as f:
            f.write(body_part)

        # 6. Extract Image URLs (extremely basic)
        html_content = body_part.decode("utf-8", errors="ignore") # Try to decode as UTF-8
        img_urls = re.findall(r'<img.*?src=["\'](.*?)["\']', html_content)

        status_var.set(f"Found {len(img_urls)} images. Starting download...")
        # 7. Download and Save Images (very basic)
        for i, img_url in enumerate(img_urls):
            status_var.set(f"Downloading image {i+1} of {len(img_urls)}...")
            # Handle relative URLs (very basic)
            if not img_url.startswith("http"):
                img_url = url + img_url if img_url.startswith("/") else url + "/" + img_url

            try:
                # Download image
                img_protocol, img_rest = img_url.split("://", 1)
                img_host, img_path = img_rest.split("/", 1)
                img_port = 80 if img_protocol == "http" else 443

                img_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if img_protocol == "https":
                    img_context = ssl.create_default_context()
                    img_s = img_context.wrap_socket(img_s, server_hostname=img_host)

                img_s.connect((img_host, img_port))
                img_request = f"GET /{img_path} HTTP/1.1\r\nHost: {img_host}\r\nConnection: close\r\n\r\n"
                img_s.sendall(img_request.encode())

                img_response = b""
                while True:
                    img_chunk = img_s.recv(4096)
                    if not img_chunk:
                        break
                    img_response += img_chunk
                img_s.close()

                # Get image content (skip headers - very basic)
                _, img_content = img_response.split(b"\r\n\r\n", 1)

                # Save image
                img_name = f"image_{i}.jpg" # You should really get the name from the URL
                img_name = re.sub(r'[\\/*?:"<>|]', "", img_name)  # Remove invalid characters for filenames
                img_path = os.path.join(folder_path, img_name)
                with open(img_path, "wb") as img_file:
                    img_file.write(img_content)

            except Exception as e:
                print(f"Error downloading image: {img_url} - {e}")

        status_var.set("Scraping completed successfully!")

    except Exception as e:
        status_var.set(f"Error: {str(e)}")

def get_folder():
    folder_selected = fd.askdirectory()
    folder_path.set(folder_selected)

def run_scraper():
    url = url_entry.get()
    path = folder_path.get()

    if not url or not path:
        tk.messagebox.showerror("Error", "Please enter both URL and folder path.")
        return

    status_var.set("Starting scraper...")
    # Run the scraper in a separate thread to prevent freezing the UI
    thread = Thread(target=scrape_and_save, args=(url, path, status_var))
    thread.start()

# Create main window
root = tk.Tk()
root.title("Web Scraper")

# URL input
url_label = tk.Label(root, text="Website URL:")
url_label.grid(row=0, column=0, padx=5, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=10)

# Folder selection
folder_path = tk.StringVar()
folder_label = tk.Label(root, text="Save to Folder:")
folder_label.grid(row=1, column=0, padx=5, pady=10)
folder_entry = tk.Entry(root, width=50, textvariable=folder_path)
folder_entry.grid(row=1, column=1, padx=5, pady=10)
folder_button = tk.Button(root, text="Browse", command=get_folder)
folder_button.grid(row=1, column=2, padx=5, pady=10)

# Run button
run_button = tk.Button(root, text="Run Scraper", command=run_scraper)
run_button.grid(row=2, column=1, padx=5, pady=20)

# Status bar
status_var = tk.StringVar()
status_var.set("Ready")
status_label = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.grid(row=3, column=0, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)

root.mainloop()
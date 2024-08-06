import tkinter as tk
from tkinter import scrolledtext, filedialog
import requests
import threading
import time
import subprocess
import socket
from urllib.parse import urlparse
from datetime import datetime

class LatencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Latency Measurement Tool")
        self.root.geometry("900x400")  # Set the window size to 900x400 pixels
        self.thread = None
        self.stop_event = threading.Event()

        # URL / IP Entry
        tk.Label(root, text="URL / IP:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.url_entry = tk.Entry(root, width=30)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        # Port Entry
        tk.Label(root, text="Port:").grid(row=0, column=2, padx=10, pady=10, sticky='e')
        self.port_entry = tk.Entry(root, width=10)
        self.port_entry.grid(row=0, column=3, padx=10, pady=10)

        # HTTP Proxy Entry
        tk.Label(root, text="HTTP Proxy:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.proxy_entry = tk.Entry(root, width=30)
        self.proxy_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

        # Buttons
        tk.Button(root, text="Ping", command=self.run_ping).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(root, text="Get Request", command=self.run_get_request).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(root, text="Check Port", command=self.run_check_port).grid(row=2, column=2, padx=10, pady=10)
        tk.Button(root, text="NSLookup", command=self.run_nslookup).grid(row=2, column=3, padx=10, pady=10)
        tk.Button(root, text="Check Proxy", command=self.run_check_proxy).grid(row=2, column=4, padx=10, pady=10)
        tk.Button(root, text="Reset", command=self.reset_output).grid(row=2, column=5, padx=10, pady=10)
        tk.Button(root, text="Stop", command=self.stop_thread).grid(row=2, column=6, padx=10, pady=10)
        tk.Button(root, text="Download Output", command=self.download_output).grid(row=2, column=7, padx=10, pady=10)

        # Output Area
        self.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15)
        self.output_area.grid(row=3, column=0, columnspan=8, padx=10, pady=10)

    def run_ping(self):
        self.start_thread(self.ping)

    def run_get_request(self):
        self.start_thread(self.get_request)

    def run_check_port(self):
        self.start_thread(self.check_port)

    def run_nslookup(self):
        self.start_thread(self.nslookup)

    def run_check_proxy(self):
        self.start_thread(self.check_proxy)

    def start_thread(self, target):
        if self.thread is None or not self.thread.is_alive():
            self.stop_event.clear()
            self.thread = threading.Thread(target=target)
            self.thread.start()

    def stop_thread(self):
        if self.thread is not None and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join(timeout=1)  # Set a timeout to prevent blocking

    def ping(self):
        url = self.url_entry.get()
        try:
            for i in range(4):
                if self.stop_event.is_set():
                    self.output_area.insert(tk.END, "Ping stopped by user.\n")
                    return
                output = subprocess.check_output(["ping", "-c", "1", url], universal_newlines=True)
                self.output_area.insert(tk.END, f"Ping Result {i+1} for {url}:\n{output}\n")
                time.sleep(1)  # Add a small delay to simulate the process
        except Exception as e:
            self.output_area.insert(tk.END, f"Error pinging {url}: {e}\n")

    def get_request(self):
        url = self.url_entry.get()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        proxy = self.proxy_entry.get()
        if proxy and not self.is_valid_proxy(proxy):
            self.output_area.insert(tk.END, f"Invalid proxy URL: {proxy}\n")
            return
        proxies = {"http": proxy, "https": proxy} if proxy else None
        try:
            self.output_area.insert(tk.END, "Starting GET request...\n")
            start_time = time.time()
            response = self.make_request(url, proxies)
            elapsed_time = (time.time() - start_time) * 1000  # in milliseconds
            self.output_area.insert(tk.END, "Request completed.\n")
            if self.stop_event.is_set():
                self.output_area.insert(tk.END, "GET request stopped by user.\n")
                return
            self.output_area.insert(tk.END, f"GET Request to {url}:\n")
            self.output_area.insert(tk.END, f"Status Code: {response.status_code}\n")
            self.output_area.insert(tk.END, f"Headers: {response.headers}\n")
            self.output_area.insert(tk.END, f"Content: {response.text[:200]}...\n")
            self.output_area.insert(tk.END, f"Time taken: {elapsed_time:.2f} ms\n\n")
        except requests.exceptions.RequestException as e:
            if self.stop_event.is_set():
                self.output_area.insert(tk.END, "GET request stopped by user.\n")
            else:
                self.output_area.insert(tk.END, f"Error making GET request to {url}: {e}\n")

    def make_request(self, url, proxies):
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get(url, proxies=proxies, timeout=(5, 10))  # Connect timeout and read timeout
        return response

    def check_port(self):
        url = self.url_entry.get()
        port = self.port_entry.get()
        if not port.isdigit():
            self.output_area.insert(tk.END, "Invalid port number. Please enter a valid port.\n")
            return

        port = int(port)
        try:
            sock = socket.create_connection((url, port), timeout=10)
            if self.stop_event.is_set():
                sock.close()
                self.output_area.insert(tk.END, "Port check stopped by user.\n")
                return
            sock.close()
            self.output_area.insert(tk.END, f"Port {port} on {url} is open.\n")
        except Exception as e:
            self.output_area.insert(tk.END, f"Port {port} on {url} is closed: {e}\n")

    def nslookup(self):
        url = self.url_entry.get()
        try:
            output = subprocess.check_output(["nslookup", url], universal_newlines=True)
            if self.stop_event.is_set():
                self.output_area.insert(tk.END, "NSLookup stopped by user.\n")
                return
            self.output_area.insert(tk.END, f"NSLookup Results for {url}:\n{output}\n")
        except Exception as e:
            self.output_area.insert(tk.END, f"Error performing NSLookup for {url}: {e}\n")

    def check_proxy(self):
        proxy = self.proxy_entry.get()
        if proxy and not self.is_valid_proxy(proxy):
            self.output_area.insert(tk.END, f"Invalid proxy URL: {proxy}\n")
            return
        proxies = {"http": proxy, "https": proxy} if proxy else None
        test_url = self.url_entry.get()  # Use the URL entered in the "URL / IP" field
        if not test_url.startswith('http://') and not test_url.startswith('https://'):
            test_url = 'http://' + test_url  # Ensure the URL has a scheme

        try:
            start_time = time.time()
            response = self.make_request(test_url, proxies)
            elapsed_time = (time.time() - start_time) * 1000  # in milliseconds
            if self.stop_event.is_set():
                self.output_area.insert(tk.END, "Proxy check stopped by user.\n")
                return
            if response.status_code == 200:
                self.output_area.insert(tk.END, f"Proxy '{proxy}' is working for {test_url}.\n")
            else:
                self.output_area.insert(tk.END, f"Proxy '{proxy}' returned status code {response.status_code} for {test_url}.\n")
            self.output_area.insert(tk.END, f"Time taken: {elapsed_time:.2f} ms\n\n")
        except requests.exceptions.RequestException as e:
            if self.stop_event.is_set():
                self.output_area.insert(tk.END, "Proxy check stopped by user.\n")
            else:
                self.output_area.insert(tk.END, f"Error using proxy '{proxy}' for {test_url}: {e}\n")

    def is_valid_proxy(self, proxy_url):
        parsed_url = urlparse(proxy_url)
        return all([parsed_url.scheme in ['http', 'https'], parsed_url.netloc])

    def reset_output(self):
        self.output_area.delete(1.0, tk.END)

    def download_output(self):
        # Get the current time
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Determine the operation type based on the last operation
        content = self.output_area.get("1.0", tk.END)
        if "Ping Result" in content:
            operation_type = "ping"
        elif "GET Request" in content:
            operation_type = "get_request"
        elif "Port" in content:
            operation_type = "check_port"
        elif "NSLookup" in content:
            operation_type = "nslookup"
        elif "Proxy" in content:
            operation_type = "check_proxy"
        else:
            operation_type = "output"

        filename = f"{operation_type}_{timestamp}.txt"
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=filename, filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filepath:
            with open(filepath, 'w') as file:
                file.write(content)

if __name__ == "__main__":
    root = tk.Tk()
    app = LatencyApp(root)
    root.mainloop()


# Latency Measurement Tool

## Overview

The Latency Measurement Tool is a desktop application built using Python's `tkinter` library. It allows users to measure various network parameters such as latency, port status, DNS lookup, and proxy functionality. The tool provides a user-friendly interface to perform these operations and view the results.

## Features

- **Ping Test**: Measure the latency to a specified URL or IP address.
- **GET Request**: Perform an HTTP GET request to a specified URL and measure the response time.
- **Port Check**: Check if a specific port on a specified URL or IP address is open.
- **NSLookup**: Perform a DNS lookup for a specified URL.
- **Proxy Check**: Verify if an HTTP proxy is functioning correctly for a specified URL.
- **Stop Operation**: Ability to stop ongoing operations.
- **Reset Output**: Clear the output display area.
- **Download Output**: Save the results to a text file.

## Installation

### For Windows

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/bacalu93/latency_connext.git
   cd latency_connext
   ```

2. **Install Dependencies**:
   Ensure you have Python installed on your machine. You can install the required Python packages using pip:
   ```bash
   pip install requests
   ```

3. **Run the Application**:
   ```bash
   python connext_windows.py
   ```

4. **Convert to Executable (Optional)**:
   If you want to convert the Python script to an executable file, you can use `pyinstaller`. First, install `pyinstaller`:
   ```bash
   pip install pyinstaller
   ```

   Then, create the executable:
   ```bash
   pyinstaller --onefile connext_windows.py
   ```
   This will generate a `dist` folder containing the `connext_windows.exe` file.

### For Linux

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/bacalu93/latency_connext.git
   cd latency_connext
   ```

2. **Install Dependencies**:
   Ensure you have Python installed on your machine. You can install the required Python packages using pip:
   ```bash
   pip install requests
   ```

3. **Run the Application**:
   ```bash
   python connext_linux.py
   ```

## Usage

1. **Enter URL / IP**: Input the URL or IP address you want to test.
2. **Enter Port (Optional)**: Specify the port number if you are checking a port status.
3. **Enter HTTP Proxy (Optional)**: Input the proxy URL if you want to perform requests through a proxy.
4. **Click Buttons**: Click on the desired operation button (`Ping`, `Get Request`, `Check Port`, `NSLookup`, `Check Proxy`) to start the operation.
5. **View Output**: The results will be displayed in the output area.
6. **Stop Operation**: Click `Stop` to terminate any ongoing operation.
7. **Reset Output**: Click `Reset` to clear the output display.
8. **Download Output**: Click `Download Output` to save the results to a text file.

## Code Structure

- **connext_windows.py**: Application file for Windows containing the `LatencyApp` class and GUI logic.
- **connext_linux.py**: Application file for Linux containing the `LatencyApp` class and GUI logic.
- **README.md**: This readme file.

## Contributions

Contributions are welcome! Please fork the repository and submit pull requests for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or suggestions, please contact [andrei.bacalu93@gmail.com](mailto:andrei.bacalu93@gmail.com).

---

Feel free to customize this README file according to your specific needs and project details.

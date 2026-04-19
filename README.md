
# 🧰 DeskUtility Pro

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

**DeskUtility Pro** is a powerful, lightweight, and single-file desktop application designed to boost your productivity. Built with modern Python and CustomTkinter, it bundles essential daily tools into one beautifully designed, dark-themed interface.

---

## 🚀 Key Features

### 📐 Unit Converter
Convert values seamlessly across 5 major categories:
- **Length, Weight, Speed, Volume, and Temperature.**
- Features instant calculation and a handy "Swap Units" button.

### 🧮 Advanced Calculator
Not just a basic calculator.
- Supports complex expressions and parentheses.
- Built-in **History Panel** to track all your previous calculations.
- Keyboard support for rapid typing.

### ⏱ Time Center (Timer / Alarm / Stopwatch)
Fully multi-threaded time tracking:
- **Timer:** Precise countdown with a visual progress bar.
- **Alarm:** Set a 24-hour clock alarm that triggers locally.
- **Stopwatch:** Tracks elapsed time with millisecond precision and a Lap recording system.

### 📋 Clipboard Manager
Never lose copied text again.
- Automatically monitors your system clipboard in the background.
- Stores up to 30 recent clipboard items.
- One-click copy to restore previous items to your active clipboard.

### 🔧 Window Tools
Control how the application behaves on your desktop:
- **Always On Top:** Pin the app above all other windows.
- **Window Opacity:** Adjust transparency from $50\%$ to $100\%$ for a seamless desktop experience.

---

## 📸 Screenshots

*(Replace these links with actual screenshots of your app)*
<div align="center">
  <img src="https://via.placeholder.com/400x250.png?text=Main+Dashboard" width="45%" alt="Dashboard" />
  <img src="https://via.placeholder.com/400x250.png?text=Calculator+History" width="45%" alt="Calculator" />
</div>

---

## 💻 Installation & Usage

You can run DeskUtility Pro directly via Python or build it into a standalone executable.

### Method 1: Run with Python
1. Clone the repository:
   ```bash
   git clone https://github.com/MRThugh/DeskUtility.git
   cd DeskUtility
   ```
2. Install the required dependencies:
   ```bash
   pip install customtkinter pyperclip
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Method 2: Build a Standalone Executable (.exe)
If you want to run the app without installing Python:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico main.py
```
*The `.exe` file will be generated in the `dist` folder.*

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! 
If you want to add a new tool to the sidebar, feel free to fork the project and submit a Pull Request.

---

Made with ❤️ by [MRThugh](https://github.com/MRThugh)  
⭐ **If you find this tool helpful, please leave a star on the repository!**

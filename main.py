# =============================================================================
# DeskUtility Pro - A Fully Functional Desktop Utility Toolbox
# Built with Python + CustomTkinter (Single-File Application) By Ali Kamrani
# =============================================================================

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import math
import time
import threading
import webbrowser
import pyperclip
import datetime
import re
from collections import deque

# =============================================================================
# APP CONFIGURATION
# =============================================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =============================================================================
# UNIT CONVERTER FRAME
# =============================================================================
class UnitConverterFrame(ctk.CTkFrame):
    """Handles unit conversions for Length, Weight, Speed, Volume, Temperature."""

    CONVERSIONS = {
        "Length": {
            "units": ["Meter", "Kilometer", "Mile", "Yard", "Foot", "Inch", "Centimeter", "Millimeter"],
            "to_base": {
                "Meter": 1, "Kilometer": 1000, "Mile": 1609.344,
                "Yard": 0.9144, "Foot": 0.3048, "Inch": 0.0254,
                "Centimeter": 0.01, "Millimeter": 0.001
            }
        },
        "Weight": {
            "units": ["Kilogram", "Gram", "Pound", "Ounce", "Ton", "Milligram"],
            "to_base": {
                "Kilogram": 1, "Gram": 0.001, "Pound": 0.453592,
                "Ounce": 0.0283495, "Ton": 1000, "Milligram": 0.000001
            }
        },
        "Speed": {
            "units": ["m/s", "km/h", "mph", "knot", "ft/s"],
            "to_base": {
                "m/s": 1, "km/h": 0.277778, "mph": 0.44704,
                "knot": 0.514444, "ft/s": 0.3048
            }
        },
        "Volume": {
            "units": ["Liter", "Milliliter", "Gallon (US)", "Quart", "Pint", "Cup", "Fluid Ounce"],
            "to_base": {
                "Liter": 1, "Milliliter": 0.001, "Gallon (US)": 3.78541,
                "Quart": 0.946353, "Pint": 0.473176, "Cup": 0.236588,
                "Fluid Ounce": 0.0295735
            }
        },
        "Temperature": {
            "units": ["Celsius", "Fahrenheit", "Kelvin"],
            "to_base": None  # Special case handled separately
        }
    }

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._build_ui()

    def _build_ui(self):
        # Title
        ctk.CTkLabel(self, text="Unit Converter", font=("Helvetica", 22, "bold")).pack(pady=(10, 5))
        ctk.CTkLabel(self, text="Convert between different measurement units",
                     font=("Helvetica", 12), text_color="gray").pack(pady=(0, 15))

        # Category selector
        cat_frame = ctk.CTkFrame(self)
        cat_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(cat_frame, text="Category:", font=("Helvetica", 13)).pack(side="left", padx=10, pady=10)
        self.category_var = ctk.StringVar(value="Length")
        self.category_menu = ctk.CTkOptionMenu(
            cat_frame, variable=self.category_var,
            values=list(self.CONVERSIONS.keys()),
            command=self._on_category_change, width=180
        )
        self.category_menu.pack(side="left", padx=10, pady=10)

        # Conversion area
        conv_frame = ctk.CTkFrame(self)
        conv_frame.pack(fill="x", padx=20, pady=10)

        # From side
        from_frame = ctk.CTkFrame(conv_frame, fg_color="transparent")
        from_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(from_frame, text="From:", font=("Helvetica", 13, "bold")).pack(anchor="w")
        self.from_unit = ctk.StringVar(value="Meter")
        self.from_menu = ctk.CTkOptionMenu(from_frame, variable=self.from_unit, values=[], width=160)
        self.from_menu.pack(fill="x", pady=5)
        self.from_entry = ctk.CTkEntry(from_frame, placeholder_text="Enter value", height=40, font=("Helvetica", 14))
        self.from_entry.pack(fill="x", pady=5)

        # Arrow label
        arrow_frame = ctk.CTkFrame(conv_frame, fg_color="transparent")
        arrow_frame.pack(side="left", padx=5, pady=20)
        ctk.CTkLabel(arrow_frame, text="→", font=("Helvetica", 28)).pack(expand=True)

        # To side
        to_frame = ctk.CTkFrame(conv_frame, fg_color="transparent")
        to_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(to_frame, text="To:", font=("Helvetica", 13, "bold")).pack(anchor="w")
        self.to_unit = ctk.StringVar(value="Kilometer")
        self.to_menu = ctk.CTkOptionMenu(to_frame, variable=self.to_unit, values=[], width=160)
        self.to_menu.pack(fill="x", pady=5)
        self.result_label = ctk.CTkLabel(
            to_frame, text="Result: —", font=("Helvetica", 16, "bold"),
            fg_color=("gray85", "gray25"), corner_radius=8, height=40
        )
        self.result_label.pack(fill="x", pady=5)

        # Convert button
        ctk.CTkButton(
            self, text="Convert", height=42, font=("Helvetica", 14, "bold"),
            command=self._convert
        ).pack(pady=10, padx=20, fill="x")

        # Swap button
        ctk.CTkButton(
            self, text="⇄ Swap Units", height=36, font=("Helvetica", 13),
            fg_color="transparent", border_width=1, command=self._swap_units
        ).pack(pady=5, padx=20, fill="x")

        # Initialize menus
        self._on_category_change("Length")

    def _on_category_change(self, category):
        """Update unit dropdowns when category changes."""
        units = self.CONVERSIONS[category]["units"]
        self.from_menu.configure(values=units)
        self.to_menu.configure(values=units)
        self.from_unit.set(units[0])
        self.to_unit.set(units[1] if len(units) > 1 else units[0])
        self.result_label.configure(text="Result: —")

    def _swap_units(self):
        """Swap the from and to units."""
        f, t = self.from_unit.get(), self.to_unit.get()
        self.from_unit.set(t)
        self.to_unit.set(f)

    def _convert(self):
        """Perform the conversion and display the result."""
        try:
            value = float(self.from_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        category = self.category_var.get()
        from_u = self.from_unit.get()
        to_u = self.to_unit.get()

        if category == "Temperature":
            result = self._convert_temperature(value, from_u, to_u)
        else:
            to_base = self.CONVERSIONS[category]["to_base"]
            base_value = value * to_base[from_u]
            result = base_value / to_base[to_u]

        self.result_label.configure(text=f"Result: {result:.6g} {to_u}")

    def _convert_temperature(self, value, from_u, to_u):
        """Special handler for temperature conversions."""
        # Convert to Celsius first
        if from_u == "Celsius":
            celsius = value
        elif from_u == "Fahrenheit":
            celsius = (value - 32) * 5 / 9
        else:  # Kelvin
            celsius = value - 273.15

        # Convert from Celsius to target
        if to_u == "Celsius":
            return celsius
        elif to_u == "Fahrenheit":
            return celsius * 9 / 5 + 32
        else:  # Kelvin
            return celsius + 273.15


# =============================================================================
# ADVANCED CALCULATOR FRAME
# =============================================================================
class CalculatorFrame(ctk.CTkFrame):
    """Advanced calculator with expression evaluation and history."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.history = deque(maxlen=50)  # Store up to 50 entries
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Advanced Calculator", font=("Helvetica", 22, "bold")).pack(pady=(10, 5))
        ctk.CTkLabel(self, text="Supports arithmetic, parentheses, and expressions",
                     font=("Helvetica", 12), text_color="gray").pack(pady=(0, 10))

        # Main area: calculator on left, history on right
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10)

        # --- Calculator Panel ---
        calc_panel = ctk.CTkFrame(main_frame)
        calc_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Display
        self.display_var = ctk.StringVar(value="0")
        self.display = ctk.CTkEntry(
            calc_panel, textvariable=self.display_var,
            font=("Helvetica", 24, "bold"), height=60,
            justify="right", state="readonly"
        )
        self.display.pack(fill="x", padx=10, pady=(10, 5))

        # Expression label (shows what's being built)
        self.expr_var = ctk.StringVar(value="")
        ctk.CTkLabel(calc_panel, textvariable=self.expr_var,
                     font=("Helvetica", 11), text_color="gray", anchor="e").pack(fill="x", padx=12)

        # Button grid
        btn_frame = ctk.CTkFrame(calc_panel, fg_color="transparent")
        btn_frame.pack(padx=10, pady=10, fill="both", expand=True)

        buttons = [
            ["C", "←", "(", ")"],
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
        ]

        # Configure grid weights for even distribution
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)

        for r, row in enumerate(buttons):
            for c, label in enumerate(row):
                color = self._get_btn_color(label)
                btn = ctk.CTkButton(
                    btn_frame, text=label, width=70, height=55,
                    font=("Helvetica", 16, "bold"), fg_color=color,
                    hover_color=self._get_hover_color(label),
                    command=lambda l=label: self._on_btn_press(l)
                )
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

        # Current expression buffer
        self.expr_buffer = ""

        # Keyboard binding
        self.display.bind("<Key>", self._on_key)
        self.bind("<Key>", self._on_key)

    def _get_btn_color(self, label):
        if label == "=":
            return "#1f6aa5"
        elif label in ["C", "←"]:
            return "#8B0000"
        elif label in ["+", "-", "*", "/", "(", ")"]:
            return "#2d5a2d"
        return ("gray30", "gray25")

    def _get_hover_color(self, label):
        if label == "=":
            return "#2980b9"
        elif label in ["C", "←"]:
            return "#c0392b"
        elif label in ["+", "-", "*", "/", "(", ")"]:
            return "#3d7a3d"
        return ("gray40", "gray35")

    def _on_btn_press(self, label):
        """Handle calculator button press."""
        if label == "C":
            self.expr_buffer = ""
            self.display_var.set("0")
            self.expr_var.set("")
        elif label == "←":
            self.expr_buffer = self.expr_buffer[:-1]
            self.display_var.set(self.expr_buffer or "0")
        elif label == "=":
            self._evaluate()
        else:
            self.expr_buffer += label
            self.display_var.set(self.expr_buffer)
            self.expr_var.set("")

    def _on_key(self, event):
        """Handle keyboard input for calculator."""
        key = event.char
        if key in "0123456789.+-*/()":
            self._on_btn_press(key)
        elif event.keysym == "Return":
            self._evaluate()
        elif event.keysym == "BackSpace":
            self._on_btn_press("←")
        elif event.keysym == "Escape":
            self._on_btn_press("C")

    def _evaluate(self):
        """Safely evaluate the expression and update history."""
        expr = self.expr_buffer
        if not expr:
            return
        try:
            # Safely evaluate mathematical expression
            allowed = set("0123456789.+-*/()% ")
            if not all(c in allowed for c in expr):
                raise ValueError("Invalid characters in expression")
            result = eval(expr, {"__builtins__": {}}, {})  # Restricted eval
            result_str = str(result)
            self.display_var.set(result_str)
            self.expr_var.set(f"{expr} =")
            # Add to history
            entry = f"{expr} = {result_str}"
            self.history.appendleft(entry)
            self._update_history()
            self.expr_buffer = result_str
        except ZeroDivisionError:
            self.display_var.set("Error: Div/0")
            self.expr_buffer = ""
        except Exception:
            self.display_var.set("Error")
            self.expr_buffer = ""

    def _build_ui(self):
        ctk.CTkLabel(self, text="Advanced Calculator", font=("Helvetica", 22, "bold")).pack(pady=(10, 5))
        ctk.CTkLabel(self, text="Supports arithmetic, parentheses, and expressions",
                     font=("Helvetica", 12), text_color="gray").pack(pady=(0, 10))

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10)

        # --- Calculator Panel ---
        calc_panel = ctk.CTkFrame(main_frame)
        calc_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.display_var = ctk.StringVar(value="0")
        self.display = ctk.CTkEntry(
            calc_panel, textvariable=self.display_var,
            font=("Helvetica", 24, "bold"), height=60,
            justify="right", state="readonly"
        )
        self.display.pack(fill="x", padx=10, pady=(10, 5))

        self.expr_var = ctk.StringVar(value="")
        ctk.CTkLabel(calc_panel, textvariable=self.expr_var,
                     font=("Helvetica", 11), text_color="gray", anchor="e").pack(fill="x", padx=12)

        btn_frame = ctk.CTkFrame(calc_panel, fg_color="transparent")
        btn_frame.pack(padx=10, pady=10, fill="both", expand=True)

        buttons = [
            ["C", "←", "(", ")"],
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
        ]

        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)

        for r, row in enumerate(buttons):
            for c, label in enumerate(row):
                color = self._get_btn_color(label)
                btn = ctk.CTkButton(
                    btn_frame, text=label, width=70, height=55,
                    font=("Helvetica", 16, "bold"), fg_color=color,
                    hover_color=self._get_hover_color(label),
                    command=lambda l=label: self._on_btn_press(l)
                )
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

        self.expr_buffer = ""

        # --- History Panel ---
        hist_panel = ctk.CTkFrame(main_frame, width=220)
        hist_panel.pack(side="left", fill="both", padx=(5, 0))
        hist_panel.pack_propagate(False)

        ctk.CTkLabel(hist_panel, text="History", font=("Helvetica", 15, "bold")).pack(pady=(10, 5))
        self.history_box = ctk.CTkScrollableFrame(hist_panel, fg_color="transparent")
        self.history_box.pack(fill="both", expand=True, padx=5)

        ctk.CTkButton(
            hist_panel, text="Clear History", height=32,
            fg_color="#8B0000", hover_color="#c0392b",
            command=self._clear_history
        ).pack(pady=8, padx=5, fill="x")

    def _update_history(self):
        """Refresh the history panel with current entries."""
        for widget in self.history_box.winfo_children():
            widget.destroy()
        for entry in self.history:
            lbl = ctk.CTkLabel(
                self.history_box, text=entry,
                font=("Helvetica", 11), anchor="w",
                wraplength=190
            )
            lbl.pack(fill="x", pady=2, padx=3)
            # Divider
            ctk.CTkFrame(self.history_box, height=1, fg_color="gray40").pack(fill="x", padx=3)

    def _clear_history(self):
        self.history.clear()
        self._update_history()


# =============================================================================
# TIMER / ALARM / STOPWATCH FRAME
# =============================================================================
class TimerFrame(ctk.CTkFrame):
    """Timer, Alarm, and Stopwatch functionality in tabs."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        # Stopwatch state
        self.sw_running = False
        self.sw_start_time = 0
        self.sw_elapsed = 0
        self.sw_laps = []
        self.sw_thread = None

        # Timer state
        self.timer_running = False
        self.timer_remaining = 0
        self.timer_thread = None

        # Alarm state
        self.alarm_active = False
        self.alarm_thread = None

        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Timer / Alarm / Stopwatch", font=("Helvetica", 22, "bold")).pack(pady=(10, 5))

        # Tab view
        self.tabs = ctk.CTkTabview(self, height=480)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=5)

        self.tabs.add("⏱ Timer")
        self.tabs.add("⏰ Alarm")
        self.tabs.add("⏲ Stopwatch")

        self._build_timer_tab()
        self._build_alarm_tab()
        self._build_stopwatch_tab()

    # --- TIMER TAB ---
    def _build_timer_tab(self):
        tab = self.tabs.tab("⏱ Timer")

        ctk.CTkLabel(tab, text="Set Timer Duration", font=("Helvetica", 15, "bold")).pack(pady=(15, 10))

        input_frame = ctk.CTkFrame(tab)
        input_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(input_frame, text="Minutes:", font=("Helvetica", 13)).grid(row=0, column=0, padx=10, pady=10)
        self.timer_min = ctk.CTkEntry(input_frame, width=80, placeholder_text="0", font=("Helvetica", 14))
        self.timer_min.grid(row=0, column=1, padx=5, pady=10)

        ctk.CTkLabel(input_frame, text="Seconds:", font=("Helvetica", 13)).grid(row=0, column=2, padx=10, pady=10)
        self.timer_sec = ctk.CTkEntry(input_frame, width=80, placeholder_text="0", font=("Helvetica", 14))
        self.timer_sec.grid(row=0, column=3, padx=5, pady=10)

        # Timer display
        self.timer_display = ctk.CTkLabel(
            tab, text="00:00", font=("Helvetica", 64, "bold"),
            fg_color=("gray85", "gray20"), corner_radius=12, width=250, height=100
        )
        self.timer_display.pack(pady=20)

        # Progress bar
        self.timer_progress = ctk.CTkProgressBar(tab, width=300)
        self.timer_progress.set(0)
        self.timer_progress.pack(pady=5)

        # Buttons
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="▶ Start", width=100, command=self._start_timer).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="⏸ Pause", width=100, command=self._pause_timer,
                      fg_color="gray40").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="↺ Reset", width=100, command=self._reset_timer,
                      fg_color="#8B0000", hover_color="#c0392b").pack(side="left", padx=5)

        self.timer_status = ctk.CTkLabel(tab, text="Ready", font=("Helvetica", 13), text_color="gray")
        self.timer_status.pack(pady=5)

    def _start_timer(self):
        if self.timer_running:
            return
        try:
            mins = int(self.timer_min.get() or 0)
            secs = int(self.timer_sec.get() or 0)
        except ValueError:
            messagebox.showerror("Error", "Enter valid integers for minutes and seconds.")
            return
        total = mins * 60 + secs
        if total <= 0:
            messagebox.showwarning("Warning", "Please set a time greater than 0.")
            return
        self.timer_total = total
        if self.timer_remaining == 0 or self.timer_remaining == total:
            self.timer_remaining = total
        self.timer_running = True
        self.timer_status.configure(text="Running...", text_color="#00bb00")
        self.timer_thread = threading.Thread(target=self._run_timer, daemon=True)
        self.timer_thread.start()

    def _run_timer(self):
        while self.timer_running and self.timer_remaining > 0:
            self._update_timer_display()
            time.sleep(1)
            self.timer_remaining -= 1
        self._update_timer_display()
        if self.timer_remaining == 0 and self.timer_running:
            self.timer_running = False
            self.after(0, self._timer_done)

    def _update_timer_display(self):
        m, s = divmod(self.timer_remaining, 60)
        self.after(0, lambda: self.timer_display.configure(text=f"{m:02d}:{s:02d}"))
        progress = 1 - (self.timer_remaining / self.timer_total) if self.timer_total > 0 else 0
        self.after(0, lambda: self.timer_progress.set(progress))

    def _pause_timer(self):
        self.timer_running = False
        self.timer_status.configure(text="Paused", text_color="orange")

    def _reset_timer(self):
        self.timer_running = False
        self.timer_remaining = 0
        self.timer_display.configure(text="00:00")
        self.timer_progress.set(0)
        self.timer_status.configure(text="Ready", text_color="gray")

    def _timer_done(self):
        self.timer_display.configure(text="DONE!", fg_color="#1f6aa5")
        self.timer_status.configure(text="Timer finished!", text_color="#00bb00")
        messagebox.showinfo("Timer", "⏱ Time's up!")
        self.timer_display.configure(fg_color=("gray85", "gray20"))

    # --- ALARM TAB ---
    def _build_alarm_tab(self):
        tab = self.tabs.tab("⏰ Alarm")

        ctk.CTkLabel(tab, text="Set Alarm Time (24h format)", font=("Helvetica", 15, "bold")).pack(pady=(15, 10))

        input_frame = ctk.CTkFrame(tab)
        input_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(input_frame, text="Hour (0–23):", font=("Helvetica", 13)).grid(row=0, column=0, padx=10, pady=10)
        self.alarm_hour = ctk.CTkEntry(input_frame, width=80, placeholder_text="HH", font=("Helvetica", 14))
        self.alarm_hour.grid(row=0, column=1, padx=5, pady=10)

        ctk.CTkLabel(input_frame, text="Minute (0–59):", font=("Helvetica", 13)).grid(row=0, column=2, padx=10, pady=10)
        self.alarm_minute = ctk.CTkEntry(input_frame, width=80, placeholder_text="MM", font=("Helvetica", 14))
        self.alarm_minute.grid(row=0, column=3, padx=5, pady=10)

        # Current time display
        self.current_time_label = ctk.CTkLabel(
            tab, text="Current Time: --:--:--",
            font=("Helvetica", 18), text_color="cyan"
        )
        self.current_time_label.pack(pady=15)
        self._update_current_time()

        self.alarm_status = ctk.CTkLabel(tab, text="No alarm set", font=("Helvetica", 14), text_color="gray")
        self.alarm_status.pack(pady=10)

        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="⏰ Set Alarm", width=130, command=self._set_alarm).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel Alarm", width=130, command=self._cancel_alarm,
                      fg_color="#8B0000", hover_color="#c0392b").pack(side="left", padx=5)

    def _update_current_time(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.current_time_label.configure(text=f"Current Time: {now}")
        self.after(1000, self._update_current_time)

    def _set_alarm(self):
        try:
            h = int(self.alarm_hour.get())
            m = int(self.alarm_minute.get())
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter valid hour (0-23) and minute (0-59).")
            return

        self.alarm_active = True
        self.alarm_time = (h, m)
        self.alarm_status.configure(text=f"Alarm set for {h:02d}:{m:02d}", text_color="#00bb00")
        self.alarm_thread = threading.Thread(target=self._run_alarm, daemon=True)
        self.alarm_thread.start()

    def _run_alarm(self):
        """Check every second if alarm time is reached."""
        while self.alarm_active:
            now = datetime.datetime.now()
            if now.hour == self.alarm_time[0] and now.minute == self.alarm_time[1] and now.second == 0:
                self.alarm_active = False
                self.after(0, self._alarm_triggered)
                break
            time.sleep(1)

    def _alarm_triggered(self):
        self.alarm_status.configure(text="ALARM TRIGGERED!", text_color="red")
        messagebox.showinfo("Alarm", f"⏰ Alarm! It's {self.alarm_time[0]:02d}:{self.alarm_time[1]:02d}!")
        self.alarm_status.configure(text="No alarm set", text_color="gray")

    def _cancel_alarm(self):
        self.alarm_active = False
        self.alarm_status.configure(text="Alarm cancelled", text_color="orange")

    # --- STOPWATCH TAB ---
    def _build_stopwatch_tab(self):
        tab = self.tabs.tab("⏲ Stopwatch")

        self.sw_display = ctk.CTkLabel(
            tab, text="00:00:00.0",
            font=("Helvetica", 52, "bold"),
            fg_color=("gray85", "gray20"), corner_radius=12,
            width=320, height=100
        )
        self.sw_display.pack(pady=25)

        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="▶ Start", width=90, command=self._sw_start).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="⏸ Stop", width=90, command=self._sw_stop,
                      fg_color="gray40").pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="🏁 Lap", width=90, command=self._sw_lap,
                      fg_color="#2d5a2d").pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="↺ Reset", width=90, command=self._sw_reset,
                      fg_color="#8B0000", hover_color="#c0392b").pack(side="left", padx=4)

        ctk.CTkLabel(tab, text="Lap Times:", font=("Helvetica", 13, "bold")).pack(pady=(15, 5))
        self.lap_box = ctk.CTkScrollableFrame(tab, height=160)
        self.lap_box.pack(fill="x", padx=20)

    def _sw_start(self):
        if not self.sw_running:
            self.sw_running = True
            self.sw_start_time = time.time() - self.sw_elapsed
            self.sw_thread = threading.Thread(target=self._run_stopwatch, daemon=True)
            self.sw_thread.start()

    def _run_stopwatch(self):
        while self.sw_running:
            self.sw_elapsed = time.time() - self.sw_start_time
            self.after(0, self._update_sw_display)
            time.sleep(0.1)

    def _update_sw_display(self):
        e = self.sw_elapsed
        h = int(e // 3600)
        m = int((e % 3600) // 60)
        s = int(e % 60)
        ms = int((e * 10) % 10)
        self.sw_display.configure(text=f"{h:02d}:{m:02d}:{s:02d}.{ms}")

    def _sw_stop(self):
        self.sw_running = False

    def _sw_lap(self):
        if self.sw_running:
            e = self.sw_elapsed
            h = int(e // 3600)
            m = int((e % 3600) // 60)
            s = int(e % 60)
            ms = int((e * 10) % 10)
            lap_str = f"Lap {len(self.sw_laps) + 1}: {h:02d}:{m:02d}:{s:02d}.{ms}"
            self.sw_laps.append(lap_str)
            ctk.CTkLabel(self.lap_box, text=lap_str, font=("Helvetica", 12), anchor="w").pack(fill="x", padx=5, pady=2)

    def _sw_reset(self):
        self.sw_running = False
        self.sw_elapsed = 0
        self.sw_laps.clear()
        self.sw_display.configure(text="00:00:00.0")
        for widget in self.lap_box.winfo_children():
            widget.destroy()


# =============================================================================
# CLIPBOARD MANAGER FRAME
# =============================================================================
class ClipboardFrame(ctk.CTkFrame):
    """Monitors and manages clipboard history."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.clipboard_history = []
        self.last_clip = ""
        self.monitoring = True
        self._build_ui()
        self._start_monitoring()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Clipboard Manager", font=("Helvetica", 22, "bold")).pack(pady=(10, 5))
        ctk.CTkLabel(self, text="Automatically tracks clipboard changes",
                     font=("Helvetica", 12), text_color="gray").pack(pady=(0, 10))

        # History list
        ctk.CTkLabel(self, text="Clipboard History:", font=("Helvetica", 14, "bold")).pack(anchor="w", padx=20)
        self.list_frame = ctk.CTkScrollableFrame(self, height=320)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Action buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(btn_frame, text="📋 Copy Selected", command=self._copy_selected).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑 Clear All", command=self._clear_all,
                      fg_color="#8B0000", hover_color="#c0392b").pack(side="left", padx=5)

        self.status_label = ctk.CTkLabel(self, text="Monitoring clipboard...", text_color="gray",
                                         font=("Helvetica", 11))
        self.status_label.pack(pady=5)

        # Track selected item
        self.selected_text = None

    def _start_monitoring(self):
        """Start background thread to monitor clipboard."""
        self.monitor_thread = threading.Thread(target=self._monitor_clipboard, daemon=True)
        self.monitor_thread.start()

    def _monitor_clipboard(self):
        """Continuously check clipboard for new content."""
        while self.monitoring:
            try:
                current = pyperclip.paste()
                if current and current != self.last_clip:
                    self.last_clip = current
                    if current not in self.clipboard_history:
                        self.clipboard_history.insert(0, current)
                        if len(self.clipboard_history) > 30:
                            self.clipboard_history.pop()
                        self.after(0, self._refresh_list)
            except Exception:
                pass
            time.sleep(0.8)

    def _refresh_list(self):
        """Rebuild the visual list of clipboard entries."""
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for i, text in enumerate(self.clipboard_history):
            entry_frame = ctk.CTkFrame(self.list_frame, corner_radius=6)
            entry_frame.pack(fill="x", pady=3, padx=2)

            preview = text[:80] + "..." if len(text) > 80 else text
            lbl = ctk.CTkLabel(
                entry_frame, text=preview, font=("Helvetica", 12),
                anchor="w", wraplength=400, justify="left"
            )
            lbl.pack(side="left", padx=10, pady=5, fill="x", expand=True)

            # Highlight on click
            entry_frame.bind("<Button-1>", lambda e, t=text, f=entry_frame: self._select_item(t, f))
            lbl.bind("<Button-1>", lambda e, t=text, f=entry_frame: self._select_item(t, f))

        count = len(self.clipboard_history)
        self.status_label.configure(text=f"Monitoring clipboard... ({count} items stored)")

    def _select_item(self, text, frame):
        """Highlight selected clipboard item."""
        # Reset all frames
        for widget in self.list_frame.winfo_children():
            widget.configure(fg_color=("gray80", "gray20"))
        frame.configure(fg_color=("lightblue", "#1a3a5c"))
        self.selected_text = text

    def _copy_selected(self):
        if self.selected_text:
            pyperclip.copy(self.selected_text)
            self.status_label.configure(text="✓ Copied to clipboard!", text_color="#00bb00")
            self.after(2000, lambda: self.status_label.configure(
                text=f"Monitoring clipboard... ({len(self.clipboard_history)} items stored)",
                text_color="gray"
            ))
        else:
            messagebox.showwarning("No Selection", "Click an item to select it first.")

    def _clear_all(self):
        self.clipboard_history.clear()
        self.selected_text = None
        self._refresh_list()


# =============================================================================
# WINDOW TOOLS FRAME
# =============================================================================
class WindowToolsFrame(ctk.CTkFrame):
    """Window management utilities."""

    def __init__(self, parent, app_root):
        super().__init__(parent, fg_color="transparent")
        self.app_root = app_root  # Reference to main window
        self.always_on_top = False
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Window Tools", font=("Helvetica", 22, "bold")).pack(pady=(10, 5))
        ctk.CTkLabel(self, text="Manage application and window behavior",
                     font=("Helvetica", 12), text_color="gray").pack(pady=(0, 20))

        # Cards layout
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="both", expand=True, padx=30)

        # --- Minimize All Card ---
        min_card = ctk.CTkFrame(cards_frame, corner_radius=12)
        min_card.pack(fill="x", pady=10)
        ctk.CTkLabel(min_card, text="🗕 Minimize Window", font=("Helvetica", 16, "bold")).pack(pady=(15, 5), padx=20, anchor="w")
        ctk.CTkLabel(
            min_card,
            text="Minimizes this application window to the taskbar.",
            font=("Helvetica", 12), text_color="gray", wraplength=350, justify="left"
        ).pack(padx=20, pady=5, anchor="w")
        ctk.CTkButton(
            min_card, text="Minimize Window", height=40,
            command=self._minimize_window
        ).pack(pady=(5, 15), padx=20, anchor="w")

        # --- Always On Top Card ---
        aot_card = ctk.CTkFrame(cards_frame, corner_radius=12)
        aot_card.pack(fill="x", pady=10)
        ctk.CTkLabel(aot_card, text="📌 Always On Top", font=("Helvetica", 16, "bold")).pack(pady=(15, 5), padx=20, anchor="w")
        ctk.CTkLabel(
            aot_card,
            text="Keep this window always visible above other windows.",
            font=("Helvetica", 12), text_color="gray", wraplength=350, justify="left"
        ).pack(padx=20, pady=5, anchor="w")

        toggle_row = ctk.CTkFrame(aot_card, fg_color="transparent")
        toggle_row.pack(padx=20, pady=(5, 15), anchor="w")

        self.aot_switch = ctk.CTkSwitch(
            toggle_row, text="Enable Always On Top",
            command=self._toggle_always_on_top
        )
        self.aot_switch.pack(side="left")

        self.aot_label = ctk.CTkLabel(
            toggle_row, text="  OFF", font=("Helvetica", 12, "bold"), text_color="gray"
        )
        self.aot_label.pack(side="left")

        # --- Window Opacity Card ---
        opacity_card = ctk.CTkFrame(cards_frame, corner_radius=12)
        opacity_card.pack(fill="x", pady=10)
        ctk.CTkLabel(opacity_card, text="🔆 Window Opacity", font=("Helvetica", 16, "bold")).pack(pady=(15, 5), padx=20, anchor="w")
        ctk.CTkLabel(
            opacity_card,
            text="Adjust the transparency of this window (50% – 100%).",
            font=("Helvetica", 12), text_color="gray", wraplength=350, justify="left"
        ).pack(padx=20, pady=5, anchor="w")

        self.opacity_slider = ctk.CTkSlider(
            opacity_card, from_=50, to=100, number_of_steps=50,
            command=self._set_opacity
        )
        self.opacity_slider.set(100)
        self.opacity_slider.pack(padx=20, pady=(5, 5), fill="x")

        self.opacity_label = ctk.CTkLabel(opacity_card, text="Opacity: 100%", font=("Helvetica", 12))
        self.opacity_label.pack(padx=20, pady=(0, 15), anchor="w")

    def _minimize_window(self):
        """Minimize the main application window."""
        self.app_root.iconify()

    def _toggle_always_on_top(self):
        """Toggle the always-on-top attribute of the main window."""
        self.always_on_top = not self.always_on_top
        self.app_root.attributes("-topmost", self.always_on_top)
        if self.always_on_top:
            self.aot_label.configure(text="  ON", text_color="#00bb00")
        else:
            self.aot_label.configure(text="  OFF", text_color="gray")

    def _set_opacity(self, value):
        """Adjust window transparency."""
        opacity = int(value) / 100.0
        self.app_root.attributes("-alpha", opacity)
        self.opacity_label.configure(text=f"Opacity: {int(value)}%")


# =============================================================================
# MAIN APPLICATION CLASS
# =============================================================================
class DeskUtilityPro(ctk.CTk):
    """Main application window for DeskUtility Pro."""

    APP_TITLE = "DeskUtility Pro"
    APP_GEOMETRY = "1050x680"
    MIN_SIZE = (900, 600)

    SIDEBAR_TOOLS = [
        ("📐", "Unit Converter"),
        ("🧮", "Calculator"),
        ("⏱", "Timer / Alarm"),
        ("📋", "Clipboard"),
        ("🔧", "Window Tools"),
    ]

    def __init__(self):
        super().__init__()
        self._configure_window()
        self._build_layout()
        self._load_first_frame()

    def _configure_window(self):
        """Set up window properties."""
        self.title(self.APP_TITLE)
        self.geometry(self.APP_GEOMETRY)
        self.minsize(*self.MIN_SIZE)

        # Place your .ico file path here
        # self.iconbitmap("path/to/your/icon.ico")

    def _build_layout(self):
        """Construct the main UI layout."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_sidebar()
        self._build_content_area()

    def _build_header(self):
        """Build the top header bar with logo placeholder and title."""
        header = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=("gray15", "gray10"))
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        # Logo placeholder area
        logo_frame = ctk.CTkFrame(header, width=50, height=50, corner_radius=8,
                                  fg_color=("gray25", "gray20"))
        logo_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        logo_frame.grid_propagate(False)

        # Place your logo file path here
        # logo_img = ctk.CTkImage(Image.open("path/to/logo.png"), size=(44, 44))
        # ctk.CTkLabel(logo_frame, image=logo_img, text="").place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(logo_frame, text="DU", font=("Helvetica", 16, "bold"),
                     text_color="cyan").place(relx=0.5, rely=0.5, anchor="center")

        # App title
        title_label = ctk.CTkLabel(
            header, text="DeskUtility Pro",
            font=("Helvetica", 20, "bold"), text_color="white"
        )
        title_label.grid(row=0, column=1, sticky="w", padx=5)

        subtitle = ctk.CTkLabel(
            header, text="All-in-one desktop utility toolkit",
            font=("Helvetica", 11), text_color="gray"
        )
        subtitle.grid(row=0, column=2, sticky="e", padx=20)

        # About Us button in header
        about_btn = ctk.CTkButton(
            header, text="About Us", width=100, height=32,
            font=("Helvetica", 12),
            fg_color="transparent", border_width=1, border_color="gray50",
            command=self._open_about
        )
        about_btn.grid(row=0, column=3, padx=(5, 15), pady=10, sticky="e")

    def _build_sidebar(self):
        """Build the left navigation sidebar with tool buttons."""
        sidebar = ctk.CTkFrame(self, width=190, corner_radius=0,
                               fg_color=("gray18", "gray13"))
        sidebar.grid(row=1, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # Sidebar label
        ctk.CTkLabel(sidebar, text="TOOLS", font=("Helvetica", 11, "bold"),
                     text_color="gray50").pack(pady=(20, 10), padx=15, anchor="w")

        # Store sidebar button references for highlighting
        self.sidebar_buttons = {}
        self.active_tool = None

        for icon, name in self.SIDEBAR_TOOLS:
            btn = ctk.CTkButton(
                sidebar,
                text=f"  {icon}  {name}",
                anchor="w",
                height=44,
                font=("Helvetica", 13),
                fg_color="transparent",
                hover_color=("gray30", "gray25"),
                text_color=("gray80", "gray80"),
                corner_radius=8,
                command=lambda n=name: self._switch_frame(n)
            )
            btn.pack(fill="x", padx=10, pady=3)
            self.sidebar_buttons[name] = btn

        # Spacer + version label at bottom
        ctk.CTkLabel(sidebar, text="", fg_color="transparent").pack(expand=True)
        ctk.CTkLabel(sidebar, text="v1.0.0", font=("Helvetica", 10),
                     text_color="gray40").pack(pady=(0, 15))

    def _build_content_area(self):
        """Build the right-side content frame container."""
        self.content_area = ctk.CTkFrame(self, corner_radius=0,
                                          fg_color=("gray92", "gray17"))
        self.content_area.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        # Dictionary to hold instantiated frames
        self.frames = {}

    def _get_frame(self, name):
        """Lazy-load and cache tool frames."""
        if name not in self.frames:
            if name == "Unit Converter":
                self.frames[name] = UnitConverterFrame(self.content_area)
            elif name == "Calculator":
                self.frames[name] = CalculatorFrame(self.content_area)
            elif name == "Timer / Alarm":
                self.frames[name] = TimerFrame(self.content_area)
            elif name == "Clipboard":
                self.frames[name] = ClipboardFrame(self.content_area)
            elif name == "Window Tools":
                self.frames[name] = WindowToolsFrame(self.content_area, self)
            self.frames[name].grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        return self.frames[name]

    def _switch_frame(self, name):
        """Switch the visible tool frame and update sidebar highlight."""
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_remove()

        # Show requested frame
        frame = self._get_frame(name)
        frame.grid()

        # Update sidebar button highlighting
        for btn_name, btn in self.sidebar_buttons.items():
            if btn_name == name:
                btn.configure(fg_color=("gray35", "gray28"), text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=("gray80", "gray80"))

        self.active_tool = name

    def _load_first_frame(self):
        """Load the first tool frame on startup."""
        self._switch_frame("Unit Converter")

    def _open_about(self):
        """Open the About Us URL in the default web browser."""
        webbrowser.open("https://github.com/MRThugh")


# =============================================================================
# ENTRY POINT
# =============================================================================
def main():
    """Main function to initialize and run the DeskUtility Pro application."""
    app = DeskUtilityPro()
    app.mainloop()


if __name__ == "__main__":
    main()


# =============================================================================
# DEVELOPER NOTES
# =============================================================================
#
# 1. HOW TO REPLACE THE LOGO:
#    - Locate the comment "# Place your logo file path here" inside the
#      _build_header() method of DeskUtilityPro class.
#    - Install Pillow: pip install Pillow
#    - Uncomment the two lines:
#        from PIL import Image  (add at top of file)
#        logo_img = ctk.CTkImage(Image.open("path/to/logo.png"), size=(44, 44))
#        ctk.CTkLabel(logo_frame, image=logo_img, text="").place(...)
#    - Replace "path/to/logo.png" with your actual logo file path.
#    - Recommended size: 44x44 pixels, PNG with transparent background.
#
# 2. HOW TO REPLACE THE WINDOW ICON (.ico):
#    - Locate the comment "# Place your .ico file path here" inside the
#      _configure_window() method of DeskUtilityPro class.
#    - Uncomment the line:
#        self.iconbitmap("path/to/your/icon.ico")
#    - Replace "path/to/your/icon.ico" with your actual .ico file path.
#    - Note: .ico format is required for Windows; on Linux/macOS use .png
#      with self.iconphoto(True, tk.PhotoImage(file="icon.png"))
#
# 3. HOW TO RUN THE SCRIPT:
#    Step 1: Make sure Python 3.9+ is installed on your system.
#    Step 2: Install required packages:
#              pip install customtkinter pyperclip
#    Step 3: Run the script:
#              python desk_utility_pro.py
#    Optional: To build a standalone executable:
#              pip install pyinstaller
#              pyinstaller --onefile --windowed desk_utility_pro.py
#
# =============================================================================

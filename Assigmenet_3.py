import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class InvestmentSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Investment Simulation Calculator")
        self.root.geometry("700x760")
        self.root.configure(bg="#f0f0f0")

        title = tk.Label(
            root, text="Investment Simulation (Monthly Compounding)",
            font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333333"
        )
        title.pack(pady=10)

        input_frame = ttk.Frame(root)
        input_frame.pack(pady=10, padx=20, fill="x")

        # Initial Money
        ttk.Label(input_frame, text="Initial Money:").grid(row=0, column=0, sticky="w", pady=6)
        self.initial_entry = ttk.Entry(input_frame, width=30)
        self.initial_entry.grid(row=0, column=1, pady=6, padx=10)
        self.initial_entry.insert(0, "1000")

        # Monthly Saving
        ttk.Label(input_frame, text="Monthly Saving:").grid(row=1, column=0, sticky="w", pady=6)
        self.monthly_entry = ttk.Entry(input_frame, width=30)
        self.monthly_entry.grid(row=1, column=1, pady=6, padx=10)
        self.monthly_entry.insert(0, "100")

        # Months
        ttk.Label(input_frame, text="Investment Period (months):").grid(row=2, column=0, sticky="w", pady=6)
        self.months_entry = ttk.Entry(input_frame, width=30)
        self.months_entry.grid(row=2, column=1, pady=6, padx=10)
        self.months_entry.insert(0, "60")

        # Annual rate (%)
        ttk.Label(input_frame, text="Annual Rate (% per year):").grid(row=3, column=0, sticky="w", pady=6)
        self.annual_rate_entry = ttk.Entry(input_frame, width=30)
        self.annual_rate_entry.grid(row=3, column=1, pady=6, padx=10)
        self.annual_rate_entry.insert(0, "9.5")  # example: 9.5%

        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Simulate & Show Graph", command=self.simulate).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Clear", command=self.clear).pack(side="left", padx=6)

        self.result_label = ttk.Label(root, text="", font=("Arial", 10))
        self.result_label.pack(pady=6, padx=20, anchor="w")

        # Canvas frame
        self.canvas_frame = ttk.Frame(root)
        self.canvas_frame.pack(pady=10, padx=20, fill="both", expand=True)

    def clear(self):
        self.initial_entry.delete(0, tk.END)
        self.initial_entry.insert(0, "1000")
        self.monthly_entry.delete(0, tk.END)
        self.monthly_entry.insert(0, "100")
        self.months_entry.delete(0, tk.END)
        self.months_entry.insert(0, "60")
        self.annual_rate_entry.delete(0, tk.END)
        self.annual_rate_entry.insert(0, "9.5")
        self.result_label.config(text="")

        for w in self.canvas_frame.winfo_children():
            w.destroy()

    def simulate(self):
        try:
            initial_money = float(self.initial_entry.get())
            monthly_saving = float(self.monthly_entry.get())
            months = int(self.months_entry.get())
            annual_rate_percent = float(self.annual_rate_entry.get())

            if months <= 0:
                messagebox.showerror("Error", "Investment period (months) must be positive.")
                return
            if initial_money < 0 or monthly_saving < 0:
                messagebox.showerror("Error", "Initial money and monthly saving must be non-negative.")
                return

            # Convert annual rate (%) -> decimal
            annual_rate = annual_rate_percent / 100.0

            # Requirement: annual_rate -> monthly_rate using **
            # Effective monthly rate assuming compounding:
            monthly_rate = (1 + annual_rate) ** (1/12) - 1

            month_list = []
            balance_list = []

            balance = initial_money


            for m in range(1, months + 1):
                balance = balance * (1 + monthly_rate) + monthly_saving
                month_list.append(m)
                balance_list.append(balance)

            final_balance = balance_list[-1]
            total_contributed = initial_money + monthly_saving * months
            total_gain = final_balance - total_contributed

            self.result_label.config(
                text=(
                    f"Monthly rate ≈ {monthly_rate*100:.4f}% | "
                    f"Final = {final_balance:,.2f} | "
                    f"Contributed = {total_contributed:,.2f} | "
                    f"Gain/Loss = {total_gain:,.2f}"
                )
            )

            # Clear old chart
            for w in self.canvas_frame.winfo_children():
                w.destroy()

            # Plot
            fig = Figure(figsize=(6.2, 4.6), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(month_list, balance_list, marker="o", linewidth=2)
            ax.set_title("Accumulated Balance by Month")
            ax.set_xlabel("Month")
            ax.set_ylabel("Balance")
            ax.grid(True, alpha=0.3)

            # Embed
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentSimulatorApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Interrupted by user — closing application.")
        try:
            root.destroy()
        except Exception:
            pass

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import numpy as np

class SavingsCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chicken Fried Saving Money Calculator")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")
        
        # Animation state
        self.animation_running = False
        self.animation_frame = 0
        self.animation_data = {}
        
        # Title
        title_label = tk.Label(
            root,
            text="Savings Money Calculator",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=10)
        
        # Input Frame
        input_frame = ttk.Frame(root)
        input_frame.pack(pady=10, padx=20, fill="x")
        
        # Initial Money
        ttk.Label(input_frame, text="Initial Money ($):").grid(row=0, column=0, sticky="w", pady=5)
        self.initial_money_entry = ttk.Entry(input_frame, width=30)
        self.initial_money_entry.grid(row=0, column=1, pady=5, padx=10)
        self.initial_money_entry.insert(0, "1000")
        
        # Monthly Saving
        ttk.Label(input_frame, text="Monthly Saving ($):").grid(row=1, column=0, sticky="w", pady=5)
        self.monthly_saving_entry = ttk.Entry(input_frame, width=30)
        self.monthly_saving_entry.grid(row=1, column=1, pady=5, padx=10)
        self.monthly_saving_entry.insert(0, "100")
        
        # Number of Months
        ttk.Label(input_frame, text="Number of Months:").grid(row=2, column=0, sticky="w", pady=5)
        self.months_entry = ttk.Entry(input_frame, width=30)
        self.months_entry.grid(row=2, column=1, pady=5, padx=10)
        self.months_entry.insert(0, "12")
        
        # Button Frame
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)
        
        calculate_btn = ttk.Button(button_frame, text="Calculate & Show Graph", command=self.calculate)
        calculate_btn.pack(side="left", padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_inputs)
        clear_btn.pack(side="left", padx=5)
        
        # Result Frame
        result_frame = ttk.Frame(root)
        result_frame.pack(pady=10, padx=20, fill="x")
        
        self.result_label = ttk.Label(result_frame, text="", font=("Arial", 10))
        self.result_label.pack(anchor="w", pady=5)
        
        # Canvas for Chart
        self.canvas_frame = ttk.Frame(root)
        self.canvas_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    def clear_inputs(self):
        self.animation_running = False
        self.initial_money_entry.delete(0, tk.END)
        self.initial_money_entry.insert(0, "1000")
        self.monthly_saving_entry.delete(0, tk.END)
        self.monthly_saving_entry.insert(0, "100")
        self.months_entry.delete(0, tk.END)
        self.months_entry.insert(0, "12")
        self.result_label.config(text="")
        
        # Clear canvas
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
    
    def calculate(self):
        try:
            initial_money = float(self.initial_money_entry.get())
            monthly_saving = float(self.monthly_saving_entry.get())
            months = int(self.months_entry.get())
            
            if months <= 0:
                messagebox.showerror("Error", "Number of months must be positive!")
                return
            
            month_list = []
            money_list = []
            total_money = initial_money
            
            for month in range(1, months + 1):
                total_money += monthly_saving
                month_list.append(month)
                money_list.append(total_money)
            
            final_money = total_money
            total_saved = final_money - initial_money
            
            # Update result label
            result_text = f"Final Amount: ${final_money:,.2f} | Total Saved: ${total_saved:,.2f}"
            self.result_label.config(text=result_text)
            
            # Clear previous canvas
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            # Create figure with animation
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.set_xlim(0, months + 1)
            ax.set_ylim(min(money_list) * 0.9, max(money_list) * 1.1)
            ax.set_xlabel("Month", fontsize=10)
            ax.set_ylabel("Total Money ($)", fontsize=10)
            ax.set_title("Savings Progress Over Time", fontsize=12, fontweight="bold")
            ax.grid(True, alpha=0.3)
            
            # Line and scatter for animation
            line, = ax.plot([], [], marker="o", linestyle="-", linewidth=2.5, markersize=6, color="#4CAF50", label="Savings")
            scatter = ax.scatter([], [], color="#FF6B6B", s=100, zorder=5, alpha=0)
            text_annotation = ax.text(0.02, 0.98, "", transform=ax.transAxes, 
                                     verticalalignment='top', fontsize=9,
                                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            ax.legend(loc="upper right")
            
            fig.tight_layout()
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Animation state
            self.animation_frame = 0
            self.animation_running = True
            self.animation_data = {
                'month_list': month_list,
                'money_list': money_list,
                'line': line,
                'scatter': scatter,
                'text_annotation': text_annotation,
                'fig': fig,
                'canvas': canvas
            }
            
            # Start animation loop
            self.animate_step()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
    
    def animate_step(self):
        """Animate the graph step by step"""
        if not self.animation_running:
            return
        
        data = self.animation_data
        month_list = data['month_list']
        money_list = data['money_list']
        line = data['line']
        scatter = data['scatter']
        text_annotation = data['text_annotation']
        canvas = data['canvas']
        
        frame = self.animation_frame
        
        # Update line data
        line.set_data(month_list[:frame + 1], money_list[:frame + 1])
        
        # Update scatter point
        if frame > 0:
            scatter.set_offsets(np.c_[month_list[frame:frame+1], money_list[frame:frame+1]])
            scatter.set_alpha(min(1.0, (frame % 10) / 10.0))
        
        # Update text annotation
        if frame > 0:
            progress = f"Month {month_list[frame]}: ${money_list[frame]:,.2f}"
            text_annotation.set_text(progress)
        
        # Redraw canvas
        canvas.draw()
        
        # Move to next frame
        self.animation_frame += 1
        
        # Loop animation
        if self.animation_frame >= len(month_list):
            self.animation_frame = 0
        
        # Schedule next frame
        self.root.after(200, self.animate_step)

if __name__ == "__main__":
    root = tk.Tk()
    app = SavingsCalculatorApp(root)
    root.mainloop()
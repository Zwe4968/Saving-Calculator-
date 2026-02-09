import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

print("\n--- Chicken Fried Saving Money  ---")

initial_money = float(input("Enter initial money: "))
monthly_saving = float(input("Enter monthly saving: "))
months = int(input("Enter number of months: "))

month_list = []
money_list = []
total_money = initial_money

for month in range(1, months + 1):
    total_money += monthly_saving
    month_list.append(month)
    money_list.append(total_money)


fig, ax = plt.subplots()
ax.set_xlim(1, months)
ax.set_ylim(min(money_list) * 0.9, max(money_list) * 1.1)
ax.set_xlabel("Month")
ax.set_ylabel("Total Money")
ax.set_title("Saving Money ")

line, = ax.plot([], [])

def update(frame):
    line.set_data(month_list[:frame + 1], money_list[:frame + 1])
    return line,

animation = FuncAnimation(
    fig,
    update,
    frames=months,
    interval=500,
    repeat=False
)

plt.show()
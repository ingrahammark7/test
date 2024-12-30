import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, Label, Canvas, Scrollbar, Frame, Button
import matplotlib.backends.backend_tkagg as tkagg

# Load the dataset (ensure the file path is correct)
df = pd.read_excel('fighter.xlsx')  # Update with your actual file path
#remove everything except data

# Function to clean and prepare data based on your schema
def prepare_data(df):
    fighters = []
    current_fighter = None
    fighter_data = []
    conflicts = []

    for index, row in df.iterrows():
        if pd.isna(row.iloc[0]):
            if current_fighter:
                fighters.append((current_fighter, conflicts, fighter_data))
            current_fighter = None
            fighter_data = []
            conflicts = []
        elif pd.notna(row.iloc[0]) and pd.isna(row.iloc[1]) and pd.isna(row.iloc[2]) and pd.isna(row.iloc[3]):
            current_fighter = row.iloc[0]
        elif pd.notna(row.iloc[1]) or pd.notna(row.iloc[2]) or pd.notna(row.iloc[3]):
            if current_fighter:
                fighter_data.append((row.iloc[1], row.iloc[2], row.iloc[3]))
                conflicts.append(str(row.iloc[0]))

    if current_fighter:
        fighters.append((current_fighter, conflicts, fighter_data))

    return fighters

# Prepare the data
fighters = prepare_data(df)

# Initialize Tkinter window
root = Tk()
root.title("Aircraft Data Visualization")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to 75% of screen width and 80% of screen height
window_width = int(screen_width * 0.75)
window_height = int(screen_height * 0.80)
root.geometry(f"{window_width}x{window_height}")
root.configure(bg="white")

# Function to toggle dark mode
def toggle_dark_mode():
    current_bg = root.cget("bg")
    if current_bg == "white":
        root.configure(bg="#333333")
        fighters_frame.configure(bg="#333333")
        for widget in fighters_frame.winfo_children():
            widget.configure(bg="#333333", fg="white")
    else:
        root.configure(bg="white")
        fighters_frame.configure(bg="white")
        for widget in fighters_frame.winfo_children():
            widget.configure(bg="white", fg="black")

# Add a Dark Mode Button
dark_mode_button = Button(root, text="Toggle Dark Mode", command=toggle_dark_mode, bg="#444", fg="white", relief="flat")
dark_mode_button.pack(pady=10)

# Create a canvas and a scrollbar for scrolling
canvas_frame = Frame(root)
canvas_frame.pack(fill="both", expand=True)

canvas = Canvas(canvas_frame)
scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

fighters_frame = Frame(canvas)
canvas.create_window((0, 0), window=fighters_frame, anchor="nw")

# Function to plot data for a fighter with advanced styling
def plot_data_for_fighter(fighter, conflicts, data, fighter_frame, plot_width):
    kills = [entry[0] for entry in data]
    losses = [entry[1] for entry in data]
    grounds = [entry[2] for entry in data]

    # Use Seaborn style for plots
    sns.set(style="whitegrid")

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(plot_width, 6))
    ax.bar(conflicts, kills, label='Kills', alpha=0.7, color=sns.color_palette("Blues")[2])
    ax.bar(conflicts, losses, label='Losses', alpha=0.7, color=sns.color_palette("Reds")[2])
    ax.bar(conflicts, grounds, label='Ground', alpha=0.7, color=sns.color_palette("Greens")[2])

    ax.set_xlabel('Conflict', fontsize=14, fontweight='bold')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax.set_title(f'{fighter} Data by Conflict', fontsize=16, fontweight='bold')
    ax.legend(title="Types", fontsize=12)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Embed the plot in Tkinter window
    canvas = tkagg.FigureCanvasTkAgg(fig, master=fighter_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# Function to update the window and scroll region
def update_scroll_region():
    fighters_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Plot width is 90% of screen width
plot_width = screen_width * 0.90 / 100

# Create the UI for all fighters in the frame
for fighter, conflicts, data in fighters:
    fighter_frame = Frame(fighters_frame)
    fighter_label = Label(fighter_frame, text=f"Fighter: {fighter}", font=("Helvetica", 14, "bold"))
    fighter_label.pack()

    plot_data_for_fighter(fighter, conflicts, data, fighter_frame, plot_width)

    fighter_frame.pack(fill="both", expand=True, pady=10)

# Update the scroll region after all fighters are added
update_scroll_region()

# Start the Tkinter main loop
root.mainloop()

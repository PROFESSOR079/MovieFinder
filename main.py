# main.py
# Movie Finder App - Search Bar + UI Components

import tkinter as tk

# --- Constants ---
BG_COLOR = "#1a1a2e"
SECONDARY_BG = "#16213e"
ACCENT_COLOR = "#e94560"
TEXT_COLOR = "#eaeaea"
SUBTEXT_COLOR = "#a8a8b3"
CARD_BG = "#0f3460"

FONT_TITLE = ("Helvetica", 22, "bold")
FONT_NORMAL = ("Helvetica", 12)
FONT_SMALL = ("Helvetica", 10)

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 650


def build_window():
    root = tk.Tk()
    root.title("🎬 Movie Finder")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)

    # --- Header ---
    header_frame = tk.Frame(root, bg=SECONDARY_BG, pady=15)
    header_frame.pack(fill="x")

    title_label = tk.Label(
        header_frame,
        text="🎬 Movie Finder",
        font=FONT_TITLE,
        bg=SECONDARY_BG,
        fg=ACCENT_COLOR,
    )
    title_label.pack()

    subtitle_label = tk.Label(
        header_frame,
        text="Search any movie and explore details",
        font=FONT_NORMAL,
        bg=SECONDARY_BG,
        fg=SUBTEXT_COLOR,
    )
    subtitle_label.pack()

    # --- Search Bar ---
    search_frame = tk.Frame(root, bg=BG_COLOR, pady=15)
    search_frame.pack(fill="x", padx=30)

    search_entry = tk.Entry(
        search_frame,
        font=("Helvetica", 14),
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        insertbackground=TEXT_COLOR,
        relief="flat",
        width=40,
    )
    search_entry.pack(side="left", ipady=10, ipadx=10)
    search_entry.insert(0, "Search movies...")
    search_entry.config(fg=SUBTEXT_COLOR)

    # Placeholder effect
    def on_focus_in(event):
        if search_entry.get() == "Search movies...":
            search_entry.delete(0, tk.END)
            search_entry.config(fg=TEXT_COLOR)

    def on_focus_out(event):
        if search_entry.get() == "":
            search_entry.insert(0, "Search movies...")
            search_entry.config(fg=SUBTEXT_COLOR)

    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)

    def on_search():
        query = search_entry.get()
        if query and query != "Search movies...":
            status_label.config(text=f"Searching for: {query}...")

    search_entry.bind("<Return>", lambda event: on_search())

    search_btn = tk.Button(
        search_frame,
        text="🔍 Search",
        font=FONT_NORMAL,
        bg=ACCENT_COLOR,
        fg=TEXT_COLOR,
        relief="flat",
        padx=15,
        pady=8,
        cursor="hand2",
        activebackground="#c73652",
        activeforeground=TEXT_COLOR,
        command=on_search,
    )
    search_btn.pack(side="left", padx=10)

    # --- Status Label ---
    status_label = tk.Label(
        root,
        text="Type a movie name and press Search or Enter",
        font=FONT_SMALL,
        bg=BG_COLOR,
        fg=SUBTEXT_COLOR,
    )
    status_label.pack()

    # --- Results Area ---
    results_frame = tk.Frame(root, bg=BG_COLOR)
    results_frame.pack(fill="both", expand=True, padx=20, pady=10)

    canvas = tk.Canvas(results_frame, bg=BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Placeholder text in results
    placeholder = tk.Label(
        scrollable_frame,
        text="🎬 Your results will appear here...",
        font=FONT_NORMAL,
        bg=BG_COLOR,
        fg=SUBTEXT_COLOR,
    )
    placeholder.pack(pady=50)

    return root


def main():
    root = build_window()
    root.mainloop()


if __name__ == "__main__":
    main()
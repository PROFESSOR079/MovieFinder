import tkinter as tk

# --- Constants ---
BG_COLOR = "#1a1a2e"
SECONDARY_BG = "#16213e"
ACCENT_COLOR = "#e94560"
TEXT_COLOR = "#eaeaea"
SUBTEXT_COLOR = "#a8a8b3"

FONT_TITLE = ("Helvetica", 22, "bold")
FONT_NORMAL = ("Helvetica", 12)

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

    # --- Main Content Area ---
    content_frame = tk.Frame(root, bg=BG_COLOR)
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    placeholder_label = tk.Label(
        content_frame,
        text="Search for a movie to get started...",
        font=FONT_NORMAL,
        bg=BG_COLOR,
        fg=SUBTEXT_COLOR,
    )
    placeholder_label.pack(expand=True)

    return root


def main():
    root = build_window()
    root.mainloop()


if __name__ == "__main__":
    main()
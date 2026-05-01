import tkinter as tk
from api_handler import search_movies

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
FONT_CARD_TITLE = ("Helvetica", 13, "bold")

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 650


def show_movie_details(root, movie_id):
    """Open a popup window with full movie details."""
    from api_handler import get_movie_details, download_poster

    details = get_movie_details(movie_id)
    if not details:
        return

    # --- Popup Window ---
    popup = tk.Toplevel(root)
    popup.title(details.get("title", "Movie Details"))
    popup.geometry("600x500")
    popup.configure(bg=BG_COLOR)
    popup.resizable(False, False)
    popup.grab_set()

    # --- Top Section: Poster + Basic Info ---
    top_frame = tk.Frame(popup, bg=SECONDARY_BG, pady=15, padx=15)
    top_frame.pack(fill="x")

    # Poster
    poster_label = tk.Label(top_frame, bg=SECONDARY_BG, text="🎬", font=("Helvetica", 40))
    poster_label.pack(side="left", padx=(0, 20))

    def load_poster():
        img = download_poster(details.get("poster_path", ""))
        if img:
            poster_label.config(image=img, text="")
            poster_label.image = img

    popup.after(100, load_poster)

    # Info
    info_frame = tk.Frame(top_frame, bg=SECONDARY_BG)
    info_frame.pack(side="left", fill="both", expand=True)

    tk.Label(
        info_frame,
        text=details.get("title", "N/A"),
        font=FONT_CARD_TITLE,
        bg=SECONDARY_BG,
        fg=ACCENT_COLOR,
        wraplength=400,
        justify="left",
    ).pack(anchor="w")

    release = details.get("release_date", "N/A")
    year = release[:4] if release and release != "N/A" else "N/A"
    runtime = details.get("runtime", 0)
    rating = details.get("vote_average", 0)
    votes = details.get("vote_count", 0)

    tk.Label(
        info_frame,
        text=f"📅 {year}   ⏱ {runtime} min   ⭐ {rating:.1f}/10  ({votes} votes)",
        font=FONT_SMALL,
        bg=SECONDARY_BG,
        fg=SUBTEXT_COLOR,
    ).pack(anchor="w", pady=5)

    # Genres
    genres = [g["name"] for g in details.get("genres", [])]
    genres_text = "  ".join([f"#{g}" for g in genres]) if genres else "N/A"
    tk.Label(
        info_frame,
        text=genres_text,
        font=FONT_SMALL,
        bg=SECONDARY_BG,
        fg="#4fc3f7",
    ).pack(anchor="w")

    # Budget / Revenue
    budget = details.get("budget", 0)
    revenue = details.get("revenue", 0)

    if budget:
        tk.Label(
            info_frame,
            text=f"💰 Budget: ${budget:,}",
            font=FONT_SMALL,
            bg=SECONDARY_BG,
            fg=SUBTEXT_COLOR,
        ).pack(anchor="w", pady=(5, 0))

    if revenue:
        tk.Label(
            info_frame,
            text=f"💵 Revenue: ${revenue:,}",
            font=FONT_SMALL,
            bg=SECONDARY_BG,
            fg=SUBTEXT_COLOR,
        ).pack(anchor="w")

    # --- Overview ---
    tk.Label(
        popup,
        text="Overview",
        font=("Helvetica", 13, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR,
    ).pack(anchor="w", padx=15, pady=(15, 5))

    overview_text = tk.Text(
        popup,
        font=FONT_SMALL,
        bg=SECONDARY_BG,
        fg=SUBTEXT_COLOR,
        relief="flat",
        wrap="word",
        height=6,
        padx=10,
        pady=10,
    )
    overview_text.insert("1.0", details.get("overview", "No description available."))
    overview_text.config(state="disabled")
    overview_text.pack(fill="x", padx=15)

    # Tagline
    tagline = details.get("tagline", "")
    if tagline:
        tk.Label(
            popup,
            text=f'✨ "{tagline}"',
            font=("Helvetica", 11, "italic"),
            bg=BG_COLOR,
            fg="#f5c518",
            wraplength=560,
        ).pack(pady=10)

    # Close Button
    tk.Button(
        popup,
        text="✖ Close",
        font=FONT_NORMAL,
        bg=ACCENT_COLOR,
        fg=TEXT_COLOR,
        relief="flat",
        padx=20,
        pady=8,
        cursor="hand2",
        command=popup.destroy,
    ).pack(pady=10)


def create_movie_card(parent, movie):
    """Create a single movie card widget with poster."""
    from api_handler import download_poster

    card = tk.Frame(parent, bg=CARD_BG, pady=10, padx=10, cursor="hand2")
    card.pack(fill="x", padx=10, pady=5)

    # Left side — poster
    poster_frame = tk.Frame(card, bg=CARD_BG, width=80)
    poster_frame.pack(side="left", padx=(0, 15))
    poster_frame.pack_propagate(False)

    poster_label = tk.Label(poster_frame, bg=CARD_BG, text="🎬", font=("Helvetica", 30))
    poster_label.pack(expand=True)

    def load_poster():
        poster_path = movie.get("poster_path", "")
        img = download_poster(poster_path)
        if img:
            poster_label.config(image=img, text="")
            poster_label.image = img

    parent.after(100, load_poster)

    # Right side — info
    info_frame = tk.Frame(card, bg=CARD_BG)
    info_frame.pack(side="left", fill="both", expand=True)

    # Title
    title = movie.get("title", "Unknown Title")
    tk.Label(
        info_frame,
        text=title,
        font=FONT_CARD_TITLE,
        bg=CARD_BG,
        fg=TEXT_COLOR,
        anchor="w",
        wraplength=580,
    ).pack(fill="x")

    # Release date + Rating
    meta_frame = tk.Frame(info_frame, bg=CARD_BG)
    meta_frame.pack(fill="x", pady=4)

    release = movie.get("release_date", "N/A")
    year = release[:4] if release and release != "N/A" else "N/A"

    tk.Label(
        meta_frame,
        text=f"📅 {year}",
        font=FONT_SMALL,
        bg=CARD_BG,
        fg=SUBTEXT_COLOR,
    ).pack(side="left", padx=(0, 15))

    rating = movie.get("vote_average", 0)
    rating_color = "#f5c518" if rating >= 7 else "#a8a8b3"
    tk.Label(
        meta_frame,
        text=f"⭐ {rating:.1f}/10",
        font=FONT_SMALL,
        bg=CARD_BG,
        fg=rating_color,
    ).pack(side="left")

    # Overview
    overview = movie.get("overview", "No description available.")
    if len(overview) > 200:
        overview = overview[:200] + "..."

    tk.Label(
        info_frame,
        text=overview,
        font=FONT_SMALL,
        bg=CARD_BG,
        fg=SUBTEXT_COLOR,
        anchor="w",
        justify="left",
        wraplength=650,
    ).pack(fill="x")

    # Hover effect
    all_widgets = [card, poster_frame, poster_label, info_frame, meta_frame]

    def on_enter(e):
        for w in all_widgets:
            try:
                w.config(bg="#1a4a8a")
            except Exception:
                pass

    def on_leave(e):
        for w in all_widgets:
            try:
                w.config(bg=CARD_BG)
            except Exception:
                pass

    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)

    # Click to open details
    movie_id = movie.get("id")

    def on_click(e, mid=movie_id):
        show_movie_details(parent.winfo_toplevel(), mid)

    card.bind("<Button-1>", on_click)
    for widget in card.winfo_children():
        widget.bind("<Button-1>", on_click)

    return card


def build_window():
    root = tk.Tk()
    root.title("🎬 Movie Finder")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)

    # --- Header ---
    header_frame = tk.Frame(root, bg=SECONDARY_BG, pady=15)
    header_frame.pack(fill="x")

    tk.Label(
        header_frame,
        text="🎬 Movie Finder",
        font=FONT_TITLE,
        bg=SECONDARY_BG,
        fg=ACCENT_COLOR,
    ).pack()

    tk.Label(
        header_frame,
        text="Search any movie and explore details",
        font=FONT_NORMAL,
        bg=SECONDARY_BG,
        fg=SUBTEXT_COLOR,
    ).pack()

    # --- Search Bar ---
    search_frame = tk.Frame(root, bg=BG_COLOR, pady=15)
    search_frame.pack(fill="x", padx=30)

    search_entry = tk.Entry(
        search_frame,
        font=("Helvetica", 14),
        bg=SECONDARY_BG,
        fg=SUBTEXT_COLOR,
        insertbackground=TEXT_COLOR,
        relief="flat",
        width=40,
    )
    search_entry.pack(side="left", ipady=10, ipadx=10)
    search_entry.insert(0, "Search movies...")

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

    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

    def on_search():
        query = search_entry.get().strip()
        if not query or query == "Search movies...":
            return

        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        status_label.config(text=f"Searching for: '{query}'...")
        root.update()

        movies = search_movies(query)

        if not movies:
            status_label.config(text="No results found. Try another title.")
            tk.Label(
                scrollable_frame,
                text="😕 No movies found.",
                font=FONT_NORMAL,
                bg=BG_COLOR,
                fg=SUBTEXT_COLOR,
            ).pack(pady=50)
            return

        status_label.config(text=f"Found {len(movies)} results for '{query}'")
        for movie in movies:
            create_movie_card(scrollable_frame, movie)

    search_entry.bind("<Return>", lambda e: on_search())

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

    return root


def main():
    root = build_window()
    root.mainloop()


if __name__ == "__main__":
    main()
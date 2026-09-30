"""User Interface Module for ISL Accessibility Translator (Phase 1).

Builds a clean, responsive desktop GUI using Tkinter and Pillow.
Provides input field, translation trigger, gloss sequencing display,
unknown word reporting, and horizontal sign card presentation with
automatic placeholder generation for missing sign images.
"""

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from PIL import Image, ImageDraw, ImageFont, ImageTk

from ..config import (
    APP_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLOR_BG,
    COLOR_PANEL_BG,
    COLOR_PRIMARY,
    COLOR_TEXT_MAIN,
    COLOR_TEXT_MUTED,
    COLOR_CARD_BORDER,
    COLOR_CARD_BG,
    COLOR_ALERT_WARN,
    COLOR_ACCENT,
    SIGN_IMAGE_WIDTH,
    SIGN_IMAGE_HEIGHT,
    SIGNS_DIR,
    DICTIONARY_PATH,
)
from ..nlp.text_processor import tokenize_text
from ..isl.sign_mapper import SignMapper


class ISLTranslatorUI:
    """Main Tkinter GUI Application for Phase 1."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the UI layout, controllers, and state.

        Args:
            root: Root Tkinter window instance.
        """
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(700, 600)
        self.root.configure(bg=COLOR_BG)

        # Initialize mapper and load dictionary
        self.sign_mapper = SignMapper(DICTIONARY_PATH)

        # Keep image references alive so Tkinter garbage collection doesn't blank them out
        self._image_cache: list[ImageTk.PhotoImage] = []

        # Build UI layout
        self._setup_styles()
        self._build_widgets()

    def _setup_styles(self) -> None:
        """Configure ttk styles for a clean, consistent appearance."""
        style = ttk.Style()
        style.theme_use("clam")

        # Configure generic styles
        style.configure("TFrame", background=COLOR_BG)
        style.configure("Card.TFrame", background=COLOR_PANEL_BG, relief="solid", borderwidth=1)
        style.configure(
            "Header.TLabel",
            background=COLOR_BG,
            foreground=COLOR_TEXT_MAIN,
            font=("Segoe UI", 16, "bold"),
        )
        style.configure(
            "SubHeader.TLabel",
            background=COLOR_BG,
            foreground=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10),
        )
        style.configure(
            "FieldLabel.TLabel",
            background=COLOR_PANEL_BG,
            foreground=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "FieldValue.TLabel",
            background=COLOR_PANEL_BG,
            foreground=COLOR_TEXT_MAIN,
            font=("Segoe UI", 11),
        )
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=6,
        )

    def _build_widgets(self) -> None:
        """Construct the UI widget hierarchy matching the Phase 1 wireframe."""
        # Top Container
        main_container = tk.Frame(self.root, bg=COLOR_BG, padx=24, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header Title
        title_label = ttk.Label(
            main_container,
            text="ISL ACCESSIBILITY TRANSLATOR",
            style="Header.TLabel",
        )
        title_label.pack(anchor="w", pady=(0, 2))

        subtitle_label = ttk.Label(
            main_container,
            text="Phase 1 Prototype: English Text → ISL Sign Representation",
            style="SubHeader.TLabel",
        )
        subtitle_label.pack(anchor="w", pady=(0, 16))

        # Input Section Card
        input_card = tk.LabelFrame(
            main_container,
            text=" Input ",
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT_MAIN,
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=14,
            relief="solid",
            bd=1,
        )
        input_card.pack(fill=tk.X, pady=(0, 14))

        input_prompt = tk.Label(
            input_card,
            text="Enter English sentence:",
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT_MAIN,
            font=("Segoe UI", 10),
        )
        input_prompt.pack(anchor="w", pady=(0, 6))

        # Text entry and button row
        entry_row = tk.Frame(input_card, bg=COLOR_PANEL_BG)
        entry_row.pack(fill=tk.X)

        self.input_entry = ttk.Entry(entry_row, font=("Segoe UI", 12))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(0, 10))
        self.input_entry.bind("<Return>", lambda event: self.handle_translate())
        self.input_entry.focus_set()

        self.translate_btn = tk.Button(
            entry_row,
            text="TRANSLATE",
            command=self.handle_translate,
            bg=COLOR_PRIMARY,
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=4,
            relief="flat",
            cursor="hand2",
        )
        self.translate_btn.pack(side=tk.LEFT, padx=(0, 6))

        self.clear_btn = tk.Button(
            entry_row,
            text="Clear",
            command=self.handle_clear,
            bg="#E2E8F0",
            fg=COLOR_TEXT_MAIN,
            activebackground="#CBD5E1",
            activeforeground=COLOR_TEXT_MAIN,
            font=("Segoe UI", 10),
            padx=12,
            pady=4,
            relief="flat",
            cursor="hand2",
        )
        self.clear_btn.pack(side=tk.LEFT)

        # Status / Feedback Banner (for empty input warnings, etc.)
        self.status_var = tk.StringVar(value="Ready. Enter a sentence and press Translate.")
        self.status_label = tk.Label(
            input_card,
            textvariable=self.status_var,
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 9, "italic"),
            anchor="w",
        )
        self.status_label.pack(fill=tk.X, pady=(8, 0))

        # Output Section Card
        self.output_card = tk.LabelFrame(
            main_container,
            text=" Translation & Sign Output ",
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT_MAIN,
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=14,
            relief="solid",
            bd=1,
        )
        self.output_card.pack(fill=tk.BOTH, expand=True)

        # 1. English Input Echo
        echo_frame = tk.Frame(self.output_card, bg=COLOR_PANEL_BG)
        echo_frame.pack(fill=tk.X, pady=(0, 6))
        tk.Label(
            echo_frame,
            text="English Input:",
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10, "bold"),
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT)
        self.echo_val_label = tk.Label(
            echo_frame,
            text="—",
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT_MAIN,
            font=("Segoe UI", 10),
            anchor="w",
        )
        self.echo_val_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 2. ISL Sequence
        seq_frame = tk.Frame(self.output_card, bg=COLOR_PANEL_BG)
        seq_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(
            seq_frame,
            text="ISL Sequence:",
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10, "bold"),
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT)
        self.seq_val_label = tk.Label(
            seq_frame,
            text="—",
            bg=COLOR_PANEL_BG,
            fg=COLOR_ACCENT,
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        )
        self.seq_val_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 3. Horizontal Sign Images Container
        sign_label = tk.Label(
            self.output_card,
            text="Sign Output:",
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        )
        sign_label.pack(fill=tk.X, pady=(0, 6))

        # Canvas with horizontal scrollbar for cards
        self.canvas_frame = tk.Frame(self.output_card, bg=COLOR_BG, bd=1, relief="solid")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.cards_canvas = tk.Canvas(
            self.canvas_frame,
            bg=COLOR_BG,
            highlightthickness=0,
            height=SIGN_IMAGE_HEIGHT + 60,
        )
        self.cards_scrollbar = ttk.Scrollbar(
            self.canvas_frame,
            orient=tk.HORIZONTAL,
            command=self.cards_canvas.xview,
        )
        self.cards_canvas.configure(xscrollcommand=self.cards_scrollbar.set)

        self.cards_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.cards_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.cards_inner_frame = tk.Frame(self.cards_canvas, bg=COLOR_BG)
        self.cards_canvas_window = self.cards_canvas.create_window(
            (0, 0),
            window=self.cards_inner_frame,
            anchor="nw",
        )

        self.cards_inner_frame.bind(
            "<Configure>",
            lambda event: self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all")),
        )

        # Display initial prompt in the cards area
        self._display_initial_canvas_message("No sentence translated yet.")

        # 4. Unknown Words
        unknown_frame = tk.Frame(self.output_card, bg=COLOR_PANEL_BG)
        unknown_frame.pack(fill=tk.X, pady=(4, 0))
        tk.Label(
            unknown_frame,
            text="Unknown words:",
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10, "bold"),
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT)
        self.unknown_val_label = tk.Label(
            unknown_frame,
            text="None",
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT_MAIN,
            font=("Segoe UI", 10),
            anchor="w",
        )
        self.unknown_val_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _display_initial_canvas_message(self, message: str) -> None:
        """Display a placeholder hint inside the card gallery area."""
        for child in self.cards_inner_frame.winfo_children():
            child.destroy()
        hint = tk.Label(
            self.cards_inner_frame,
            text=message,
            bg=COLOR_BG,
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 11),
            pady=40,
            padx=20,
        )
        hint.pack(anchor="center")

    def handle_clear(self) -> None:
        """Clear user input and reset the output view."""
        self.input_entry.delete(0, tk.END)
        self.echo_val_label.config(text="—")
        self.seq_val_label.config(text="—", fg=COLOR_ACCENT)
        self.unknown_val_label.config(text="None", fg=COLOR_TEXT_MAIN)
        self.status_var.set("Cleared. Ready for new input.")
        self.status_label.config(fg=COLOR_TEXT_MUTED)
        self._image_cache.clear()
        self._display_initial_canvas_message("No sentence translated yet.")
        self.input_entry.focus_set()

    def handle_translate(self) -> None:
        """Translate the input sentence into ISL glosses and display signs."""
        raw_text = self.input_entry.get().strip()

        # Handle empty input error gracefully
        if not raw_text:
            self.status_var.set("Please enter an English sentence first.")
            self.status_label.config(fg=COLOR_ALERT_WARN)
            return

        # 1. Text Preprocessing
        tokens = tokenize_text(raw_text)
        if not tokens:
            self.status_var.set("No valid words found after removing punctuation.")
            self.status_label.config(fg=COLOR_ALERT_WARN)
            return

        # 2. ISL Mapping
        mapping_result = self.sign_mapper.map_tokens(tokens)
        glosses = mapping_result.get("glosses", [])
        images = mapping_result.get("images", [])
        unknown = mapping_result.get("unknown", [])

        # 3. Update Text Info
        self.echo_val_label.config(text=raw_text)

        if glosses:
            sequence_text = " → ".join(glosses)
            self.seq_val_label.config(text=sequence_text, fg=COLOR_ACCENT)
        else:
            self.seq_val_label.config(text="None", fg=COLOR_TEXT_MUTED)

        if unknown:
            self.unknown_val_label.config(text=", ".join(unknown), fg=COLOR_ALERT_WARN)
        else:
            self.unknown_val_label.config(text="None", fg=COLOR_TEXT_MAIN)

        # 4. Display Cards / Sign Images
        self._render_sign_cards(glosses, images)

        # Update status banner
        if glosses and not unknown:
            self.status_var.set(f"Translation complete. {len(glosses)} sign(s) mapped.")
            self.status_label.config(fg=COLOR_ACCENT)
        elif glosses and unknown:
            self.status_var.set(
                f"Translation complete with {len(unknown)} unknown word(s) not in dictionary."
            )
            self.status_label.config(fg=COLOR_ALERT_WARN)
        else:
            self.status_var.set("No matching signs found in dictionary for the provided words.")
            self.status_label.config(fg=COLOR_ALERT_WARN)

    def _render_sign_cards(self, glosses: list[str], image_filenames: list[str]) -> None:
        """Render a horizontal list of cards containing images or placeholders."""
        # Clear existing card widgets and image cache
        for child in self.cards_inner_frame.winfo_children():
            child.destroy()
        self._image_cache.clear()

        if not glosses:
            self._display_initial_canvas_message(
                "No signs available to display for the entered words."
            )
            return

        for idx, (gloss, filename) in enumerate(zip(glosses, image_filenames)):
            # Create a card frame for each sign
            card = tk.Frame(
                self.cards_inner_frame,
                bg=COLOR_PANEL_BG,
                relief="solid",
                bd=1,
                padx=8,
                pady=8,
            )
            card.pack(side=tk.LEFT, padx=10, pady=10)

            # Order indicator (e.g. #1, #2)
            step_label = tk.Label(
                card,
                text=f"Sign {idx + 1}",
                bg=COLOR_PANEL_BG,
                fg=COLOR_TEXT_MUTED,
                font=("Segoe UI", 8, "bold"),
            )
            step_label.pack(anchor="w", pady=(0, 4))

            # Retrieve image or generate fallback placeholder
            photo = self._load_or_create_placeholder(filename, gloss)
            self._image_cache.append(photo)

            img_label = tk.Label(card, image=photo, bg=COLOR_CARD_BG)
            img_label.pack()

            # Sign Gloss label below the image
            gloss_label = tk.Label(
                card,
                text=gloss,
                bg=COLOR_PANEL_BG,
                fg=COLOR_TEXT_MAIN,
                font=("Segoe UI", 11, "bold"),
                pady=4,
            )
            gloss_label.pack()

        # Update scrollregion
        self.root.update_idletasks()
        self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all"))

    def _load_or_create_placeholder(self, filename: str, gloss: str) -> ImageTk.PhotoImage:
        """Load an image from signs/ if present, otherwise create a clean placeholder.

        Gracefully handles:
        - Missing file
        - Corrupted / unreadable file
        - Incorrect image formats
        """
        # Ensure signs directory exists
        SIGNS_DIR.mkdir(parents=True, exist_ok=True)

        target_path = SIGNS_DIR / filename if filename else None

        if target_path and target_path.is_file():
            try:
                with Image.open(target_path) as img:
                    img = img.convert("RGB")
                    # Fit into box while keeping aspect ratio
                    img.thumbnail((SIGN_IMAGE_WIDTH, SIGN_IMAGE_HEIGHT), Image.Resampling.LANCZOS)

                    # Create a centered square background
                    canvas_img = Image.new(
                        "RGB",
                        (SIGN_IMAGE_WIDTH, SIGN_IMAGE_HEIGHT),
                        color=(255, 255, 255),
                    )
                    offset_x = (SIGN_IMAGE_WIDTH - img.width) // 2
                    offset_y = (SIGN_IMAGE_HEIGHT - img.height) // 2
                    canvas_img.paste(img, (offset_x, offset_y))
                    return ImageTk.PhotoImage(canvas_img)
            except Exception as err:
                print(f"[Warning] Could not load image file '{filename}': {err}")

        # Fallback: Generate placeholder image with Pillow
        return self._generate_placeholder_image(gloss)

    def _generate_placeholder_image(self, gloss: str) -> ImageTk.PhotoImage:
        """Generate an informative, clean placeholder image with Pillow.

        Displays:
            ┌───────────────────┐
            │    [NO IMAGE]     │
            │                   │
            │    SIGN IMAGE     │
            │   NOT ADDED YET   │
            │                   │
            │   Gloss: HELLO    │
            └───────────────────┘
        """
        width = SIGN_IMAGE_WIDTH
        height = SIGN_IMAGE_HEIGHT

        # Background color: subtle light slate
        img = Image.new("RGB", (width, height), color=(241, 245, 249))
        draw = ImageDraw.Draw(img)

        # Draw a clean border
        draw.rectangle([1, 1, width - 2, height - 2], outline=(203, 213, 225), width=2)

        # Draw inner decorative box
        draw.rectangle([10, 10, width - 11, height - 11], outline=(226, 232, 240), width=1)

        # Draw placeholder text
        font = ImageFont.load_default()

        lines = [
            "[ NO IMAGE ]",
            "",
            "SIGN IMAGE",
            "NOT ADDED YET",
            "",
            f"Gloss: {gloss}",
        ]

        # Calculate text position
        y_cursor = 35
        for line in lines:
            if line:
                # Approximate center positioning with default font
                bbox = draw.textbbox((0, 0), line, font=font)
                text_w = bbox[2] - bbox[0]
                x_pos = max(0, (width - text_w) // 2)
                # Differentiate header vs body vs gloss
                color = (71, 85, 105) if "Gloss" not in line else (37, 99, 235)
                draw.text((x_pos, y_cursor), line, fill=color, font=font)
            y_cursor += 18

        return ImageTk.PhotoImage(img)

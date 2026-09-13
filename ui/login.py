import customtkinter as ctk

from database.all_users_db import all_users_database
from ui.theme import (
    APP_BG,
    BORDER,
    ERROR,
    FONT_FAMILY,
    INPUT_BG,
    MUTED_TEXT,
    PRIMARY,
    PRIMARY_HOVER,
    SURFACE,
    SURFACE_ELEVATED,
    TEXT,
)
from ui.window_lifecycle import close_window


class login_window:
    def __init__(self) -> None:
        self.user_name_app = ""
        self.vault_key = None
        self.mode = "login"
        self.user_db = all_users_database("all_user")

        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk(fg_color=APP_BG)
        self.root.title("Save Password")
        self.root.geometry("560x650")
        self.root.minsize(500, 600)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._close)
        self._build_ui()

    def _build_ui(self):
        card = ctk.CTkFrame(
            self.root,
            fg_color=SURFACE,
            border_color=BORDER,
            border_width=1,
            corner_radius=22,
        )
        card.pack(fill="both", expand=True, padx=42, pady=38)
        card.grid_columnconfigure(0, weight=1)

        brand_row = ctk.CTkFrame(card, fg_color="transparent")
        brand_row.grid(row=0, column=0, padx=42, pady=(42, 12), sticky="w")
        badge = ctk.CTkFrame(
            brand_row,
            width=46,
            height=46,
            fg_color=PRIMARY,
            corner_radius=13,
        )
        badge.pack(side="left")
        badge.pack_propagate(False)
        ctk.CTkLabel(
            badge,
            text="SP",
            text_color=TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        ).place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(
            brand_row,
            text="SAVE PASSWORD",
            text_color=MUTED_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
        ).pack(side="left", padx=(14, 0))

        self.title_label = ctk.CTkLabel(
            card,
            text="Welcome back",
            text_color=TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=30, weight="bold"),
        )
        self.title_label.grid(row=1, column=0, padx=42, pady=(6, 4), sticky="w")
        self.subtitle = ctk.CTkLabel(
            card,
            text="Unlock your encrypted password vault.",
            text_color=MUTED_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
        )
        self.subtitle.grid(row=2, column=0, padx=42, pady=(0, 28), sticky="w")

        form = ctk.CTkFrame(card, fg_color="transparent")
        form.grid(row=3, column=0, padx=42, sticky="ew")
        form.grid_columnconfigure(0, weight=1)

        self._field_label(form, "Username", 0)
        self.user_entry = self._entry(form, "Enter your username")
        self.user_entry.grid(row=1, column=0, pady=(7, 18), sticky="ew")

        self._field_label(form, "Master password", 2)
        self.password_entry = self._entry(form, "Enter your master password", show="*")
        self.password_entry.grid(row=3, column=0, pady=(7, 18), sticky="ew")

        self.confirm_label = ctk.CTkLabel(
            form,
            text="Confirm master password",
            text_color=TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
        )
        self.confirm_entry = self._entry(form, "Repeat your master password", show="*")

        self.status_label = ctk.CTkLabel(
            card,
            text="",
            text_color=ERROR,
            anchor="w",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
        )
        self.status_label.grid(row=4, column=0, padx=42, pady=(18, 6), sticky="ew")

        self.action_button = ctk.CTkButton(
            card,
            text="Unlock vault",
            height=46,
            corner_radius=12,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color=TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            command=self._submit,
        )
        self.action_button.grid(row=5, column=0, padx=42, pady=(8, 12), sticky="ew")

        self.switch_button = ctk.CTkButton(
            card,
            text="Create a new vault",
            height=42,
            corner_radius=12,
            fg_color="transparent",
            hover_color=SURFACE_ELEVATED,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT,
            command=self._switch_mode,
        )
        self.switch_button.grid(row=6, column=0, padx=42, pady=(0, 10), sticky="ew")

        ctk.CTkButton(
            card,
            text="Exit application",
            height=34,
            fg_color="transparent",
            hover_color=SURFACE_ELEVATED,
            text_color=MUTED_TEXT,
            command=self._close,
        ).grid(row=7, column=0, padx=42, pady=(0, 34), sticky="ew")

        self.user_entry.focus_set()
        for entry in (self.user_entry, self.password_entry, self.confirm_entry):
            entry.bind("<Return>", lambda _event: self._submit())

    def _field_label(self, parent, text, row):
        ctk.CTkLabel(
            parent,
            text=text,
            text_color=TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
        ).grid(row=row, column=0, sticky="w")

    def _entry(self, parent, placeholder, show=None):
        options = {
            "height": 44,
            "corner_radius": 11,
            "fg_color": INPUT_BG,
            "border_color": BORDER,
            "text_color": TEXT,
            "placeholder_text": placeholder,
            "placeholder_text_color": MUTED_TEXT,
            "font": ctk.CTkFont(family=FONT_FAMILY, size=14),
        }
        if show is not None:
            options["show"] = show
        return ctk.CTkEntry(
            parent,
            **options,
        )

    def _switch_mode(self):
        self.mode = "signup" if self.mode == "login" else "login"
        self.status_label.configure(text="")
        self.password_entry.delete(0, "end")
        self.confirm_entry.delete(0, "end")

        if self.mode == "signup":
            self.title_label.configure(text="Create your vault")
            self.subtitle.configure(text="Your master password unlocks this vault only.")
            self.confirm_label.grid(row=4, column=0, sticky="w")
            self.confirm_entry.grid(row=5, column=0, pady=(7, 0), sticky="ew")
            self.action_button.configure(text="Create vault")
            self.switch_button.configure(text="Back to sign in")
        else:
            self.title_label.configure(text="Welcome back")
            self.subtitle.configure(text="Unlock your encrypted password vault.")
            self.confirm_label.grid_remove()
            self.confirm_entry.grid_remove()
            self.action_button.configure(text="Unlock vault")
            self.switch_button.configure(text="Create a new vault")

    def _submit(self):
        user_email = self.user_entry.get().strip()
        password = self.password_entry.get()

        if not user_email or not password:
            self._show_error("Enter both your username and master password.")
            return

        if self.mode == "signup":
            if password != self.confirm_entry.get():
                self._show_error("The master passwords do not match.")
                return
            self._sign_up(user_email, password)
        else:
            self._log_in(user_email, password)

    def _sign_up(self, user_email, password):
        try:
            if self.user_db.look_for_user(user_email):
                self._show_error("That username already has a vault.")
                return

            self.vault_key = self.user_db.add_new_user(user_email, password)
            self.user_name_app = user_email
            self.root.quit()
        except (RuntimeError, ValueError) as exc:
            self._show_error(str(exc))

    def _log_in(self, user_email, password):
        try:
            if not self.user_db.look_for_user(user_email):
                self._show_error("No vault was found for that username.")
                return

            self.vault_key = self.user_db.unlock_user(user_email, password)
            if self.vault_key is None:
                self._show_error("The master password is incorrect.")
                return

            self.user_name_app = user_email
            self.root.quit()
        except RuntimeError as exc:
            self._show_error(str(exc))

    def _show_error(self, message):
        self.status_label.configure(text=message)

    def _close(self):
        self.root.quit()

    def gui(self):
        self.root.mainloop()
        if not self.user_name_app:
            close_window(self.root)
            raise SystemExit
        return self.user_name_app

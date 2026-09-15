import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk

from database.user_db import user_database
from ui.theme import (
    APP_BG,
    BORDER,
    DANGER,
    DANGER_HOVER,
    ERROR,
    FONT_FAMILY,
    INPUT_BG,
    MUTED_TEXT,
    PRIMARY,
    PRIMARY_HOVER,
    SIDEBAR_BG,
    SUCCESS,
    SURFACE,
    SURFACE_ELEVATED,
    TEXT,
)
from ui.window_lifecycle import close_window


class main_window:
    def __init__(self, user_app, vault_key, root=None) -> None:
        self.user_app = user_app
        self.data = user_database(self.user_app, vault_key)
        self.password_visible = False

        self.root = root or ctk.CTk()
        for child in self.root.winfo_children():
            child.destroy()
        self.root.configure(fg_color=APP_BG)
        self.root.title(f"Save Password — {self.user_app}")
        self.root.geometry("1180x760")
        self.root.minsize(1080, 650)
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self._close)
        self._build_ui()

    def _build_ui(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self._build_sidebar()

        content = ctk.CTkFrame(self.root, fg_color="transparent")
        content.grid(row=0, column=1, padx=32, pady=28, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(3, weight=1)

        self._build_header(content)
        self._build_editor(content)
        self._build_table(content)
        self.refresh_entries(initial=True)

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(
            self.root,
            width=250,
            fg_color=SIDEBAR_BG,
            corner_radius=0,
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=24, pady=(30, 28))
        badge = ctk.CTkFrame(brand, width=38, height=38, fg_color=PRIMARY, corner_radius=11)
        badge.pack(side="left")
        badge.pack_propagate(False)
        ctk.CTkLabel(
            badge,
            text="SP",
            text_color=TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
        ).place(relx=0.5, rely=0.5, anchor="center")
        brand_text = ctk.CTkFrame(brand, fg_color="transparent")
        brand_text.pack(side="left", padx=(12, 0))
        ctk.CTkLabel(
            brand_text,
            text="Save Password",
            text_color=TEXT,
            anchor="w",
            font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"),
        ).pack(anchor="w")
        ctk.CTkLabel(
            brand_text,
            text="LOCAL VAULT",
            text_color=MUTED_TEXT,
            anchor="w",
            font=ctk.CTkFont(family=FONT_FAMILY, size=10, weight="bold"),
        ).pack(anchor="w")

        account_card = ctk.CTkFrame(
            sidebar,
            fg_color=SURFACE,
            border_color=BORDER,
            border_width=1,
            corner_radius=14,
        )
        account_card.pack(fill="x", padx=20, pady=(0, 28))
        ctk.CTkLabel(
            account_card,
            text="SIGNED IN AS",
            text_color=MUTED_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=10, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(14, 2))
        ctk.CTkLabel(
            account_card,
            text=self.user_app,
            text_color=TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(0, 14))

        ctk.CTkLabel(
            sidebar,
            text="VAULT",
            text_color=MUTED_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=10, weight="bold"),
        ).pack(anchor="w", padx=26, pady=(0, 8))

        ctk.CTkButton(
            sidebar,
            text="↻  Refresh vault",
            height=42,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color=TEXT,
            anchor="w",
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            command=self.refresh_entries,
        ).pack(fill="x", padx=20, pady=4)
        ctk.CTkButton(
            sidebar,
            text="⌫  Clear editor",
            height=42,
            fg_color="transparent",
            hover_color=SURFACE_ELEVATED,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT,
            anchor="w",
            command=self._clear_form,
        ).pack(fill="x", padx=20, pady=4)

        security_note = ctk.CTkFrame(sidebar, fg_color="transparent")
        security_note.pack(side="bottom", fill="x", padx=24, pady=(0, 14))
        ctk.CTkLabel(
            security_note,
            text="ENCRYPTED LOCALLY",
            text_color=SUCCESS,
            anchor="w",
            font=ctk.CTkFont(family=FONT_FAMILY, size=10, weight="bold"),
        ).pack(anchor="w")
        ctk.CTkLabel(
            security_note,
            text="Your vault is unlocked only while this window is open.",
            text_color=MUTED_TEXT,
            justify="left",
            wraplength=190,
            anchor="w",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
        ).pack(anchor="w", pady=(4, 14))
        ctk.CTkButton(
            security_note,
            text="Close vault",
            height=40,
            fg_color="transparent",
            hover_color=SURFACE_ELEVATED,
            border_width=1,
            border_color=BORDER,
            text_color=MUTED_TEXT,
            command=self._close,
        ).pack(fill="x")

    def _build_header(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Your vault",
            text_color=TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=30, weight="bold"),
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            header,
            text="Manage your encrypted login credentials in one place.",
            text_color=MUTED_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
        ).grid(row=1, column=0, pady=(4, 0), sticky="w")

        self.status_label = ctk.CTkLabel(
            header,
            text="",
            fg_color=SURFACE_ELEVATED,
            corner_radius=10,
            text_color=SUCCESS,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            padx=12,
            pady=7,
        )
        self.status_label.grid(row=0, column=1, rowspan=2, sticky="e")

    def _build_editor(self, parent):
        editor = ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            border_color=BORDER,
            border_width=1,
            corner_radius=16,
        )
        editor.grid(row=1, column=0, pady=(28, 18), sticky="ew")
        editor.grid_columnconfigure(1, weight=1)
        editor.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(
            editor,
            text="Add or edit an entry",
            text_color=TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"),
        ).grid(row=0, column=0, columnspan=4, padx=20, pady=(18, 2), sticky="w")
        ctk.CTkLabel(
            editor,
            text="Select a saved account to update, reveal, or remove it.",
            text_color=MUTED_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
        ).grid(row=1, column=0, columnspan=4, padx=20, pady=(0, 16), sticky="w")

        self._label(editor, "Account", 2, 0)
        self.account_entry = self._entry(editor, "e.g. Google")
        self.account_entry.grid(row=3, column=0, columnspan=2, padx=(20, 12), pady=(6, 14), sticky="ew")

        self._label(editor, "Username or email", 2, 2)
        self.username_entry = self._entry(editor, "e.g. name@example.com")
        self.username_entry.grid(row=3, column=2, columnspan=2, padx=(12, 20), pady=(6, 14), sticky="ew")

        self._label(editor, "Password", 4, 0)
        self.password_entry = self._entry(editor, "Password", show="*")
        self.password_entry.grid(row=5, column=0, columnspan=2, padx=(20, 12), pady=(6, 20), sticky="ew")

        actions = ctk.CTkFrame(editor, fg_color="transparent")
        actions.grid(row=5, column=2, columnspan=2, padx=(12, 20), pady=(6, 20), sticky="e")
        ctk.CTkButton(
            actions,
            text="Save entry",
            width=112,
            height=42,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color=TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            command=self._add_entry,
        ).pack(side="left", padx=4)
        ctk.CTkButton(
            actions,
            text="Update",
            width=92,
            height=42,
            fg_color=SURFACE_ELEVATED,
            hover_color=BORDER,
            text_color=TEXT,
            command=self._update_entry,
        ).pack(side="left", padx=4)
        ctk.CTkButton(
            actions,
            text="Delete",
            width=86,
            height=42,
            fg_color=DANGER,
            hover_color=DANGER_HOVER,
            text_color=TEXT,
            command=self._delete_entry,
        ).pack(side="left", padx=4)
        self.reveal_button = ctk.CTkButton(
            actions,
            text="Show password",
            width=126,
            height=42,
            fg_color="transparent",
            hover_color=SURFACE_ELEVATED,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT,
            command=self._toggle_password,
        )
        self.reveal_button.pack(side="left", padx=(4, 0))

    def _build_table(self, parent):
        table_panel = ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            border_color=BORDER,
            border_width=1,
            corner_radius=16,
        )
        table_panel.grid(row=3, column=0, sticky="nsew")
        table_panel.grid_columnconfigure(0, weight=1)
        table_panel.grid_rowconfigure(1, weight=1)

        table_header = ctk.CTkFrame(table_panel, fg_color="transparent")
        table_header.grid(row=0, column=0, padx=20, pady=(18, 10), sticky="ew")
        table_header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            table_header,
            text="Saved accounts",
            text_color=TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"),
        ).grid(row=0, column=0, sticky="w")
        self.entry_count_label = ctk.CTkLabel(
            table_header,
            text="0 entries",
            text_color=MUTED_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
        )
        self.entry_count_label.grid(row=0, column=1, sticky="e")

        self._configure_table_style()
        table_container = ctk.CTkFrame(table_panel, fg_color=INPUT_BG, corner_radius=10)
        table_container.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

        self.entries_table = ttk.Treeview(
            table_container,
            columns=("account", "username"),
            show="headings",
            style="Vault.Treeview",
        )
        self.entries_table.heading("account", text="ACCOUNT")
        self.entries_table.heading("username", text="USERNAME")
        self.entries_table.column("account", width=300, minwidth=180)
        self.entries_table.column("username", width=440, minwidth=240)
        self.entries_table.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nsew")
        self.entries_table.bind("<<TreeviewSelect>>", self._select_entry)

        scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.entries_table.yview,
            style="Vault.Vertical.TScrollbar",
        )
        scrollbar.grid(row=0, column=1, padx=(8, 10), pady=10, sticky="ns")
        self.entries_table.configure(yscrollcommand=scrollbar.set)

    def _configure_table_style(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Vault.Treeview",
            background=INPUT_BG,
            fieldbackground=INPUT_BG,
            foreground=TEXT,
            borderwidth=0,
            rowheight=42,
            font=(FONT_FAMILY, 14),
        )
        style.configure(
            "Vault.Treeview.Heading",
            background=SURFACE_ELEVATED,
            foreground=MUTED_TEXT,
            borderwidth=0,
            relief="flat",
            font=(FONT_FAMILY, 11, "bold"),
            padding=(12, 11),
        )
        style.map(
            "Vault.Treeview",
            background=[("selected", PRIMARY)],
            foreground=[("selected", TEXT)],
        )
        style.map(
            "Vault.Treeview.Heading",
            background=[("active", SURFACE_ELEVATED)],
            foreground=[("active", TEXT)],
        )
        style.configure(
            "Vault.Vertical.TScrollbar",
            background=SURFACE_ELEVATED,
            troughcolor=INPUT_BG,
            bordercolor=INPUT_BG,
            arrowcolor=MUTED_TEXT,
        )

    def _label(self, parent, text, row, column):
        ctk.CTkLabel(
            parent,
            text=text,
            text_color=MUTED_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
        ).grid(row=row, column=column, padx=20 if column == 0 else 12, sticky="w")

    def _entry(self, parent, placeholder, show=None):
        options = {
            "height": 42,
            "corner_radius": 10,
            "fg_color": INPUT_BG,
            "border_color": BORDER,
            "text_color": TEXT,
            "placeholder_text": placeholder,
            "placeholder_text_color": MUTED_TEXT,
            "font": ctk.CTkFont(family=FONT_FAMILY, size=14),
        }
        if show is not None:
            options["show"] = show
        return ctk.CTkEntry(parent, **options)

    def refresh_entries(self, initial=False):
        try:
            for item in self.entries_table.get_children():
                self.entries_table.delete(item)
            records = self.data.list_entries()
            for account, username in records:
                self.entries_table.insert("", tk.END, values=(account, username))
            count = len(records)
            self.entry_count_label.configure(
                text=f"{count} {'entry' if count == 1 else 'entries'}"
            )
            self._set_status("Vault ready" if initial else "Vault refreshed")
        except (RuntimeError, ValueError) as exc:
            self._set_status(str(exc), error=True)

    def _select_entry(self, _event=None):
        selected = self.entries_table.selection()
        if not selected:
            return
        account, username = self.entries_table.item(selected[0], "values")
        self.account_entry.delete(0, tk.END)
        self.account_entry.insert(0, account)
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, username)
        self.password_entry.delete(0, tk.END)
        self.password_entry.configure(show="*")
        self.password_visible = False
        self.reveal_button.configure(text="Show password")
        self._set_status("Entry selected")

    def _toggle_password(self):
        account = self.account_entry.get().strip()
        if not account:
            self._set_status("Select or enter an account first.", error=True)
            return

        if self.password_visible:
            self.password_entry.configure(show="*")
            self.password_visible = False
            self.reveal_button.configure(text="Show password")
            self._set_status("Password hidden")
            return

        try:
            password = self.data.get_password(account)
            if password is None:
                self._set_status("Account not found.", error=True)
                return
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            self.password_entry.configure(show="")
            self.password_visible = True
            self.reveal_button.configure(text="Hide password")
            self._set_status("Password retrieved")
        except (RuntimeError, ValueError) as exc:
            self._set_status(str(exc), error=True)

    def _add_entry(self):
        account, username, password = self._form_values()
        if not self._validate_form(account, username, password):
            return
        try:
            self.data.submit(account, username, password)
            self._clear_form()
            self.refresh_entries()
            self._set_status("Entry saved")
        except (RuntimeError, ValueError) as exc:
            self._set_status(str(exc), error=True)

    def _update_entry(self):
        account, username, password = self._form_values()
        if not self._validate_form(account, username, password):
            return
        try:
            self.data.update(account, username, password)
            self._clear_form()
            self.refresh_entries()
            self._set_status("Entry updated")
        except (RuntimeError, ValueError) as exc:
            self._set_status(str(exc), error=True)

    def _delete_entry(self):
        account = self.account_entry.get().strip()
        if not account:
            self._set_status("Select or enter an account first.", error=True)
            return
        if not messagebox.askyesno("Delete entry", f"Delete '{account}'?"):
            return
        try:
            self.data.delete(account)
            self._clear_form()
            self.refresh_entries()
            self._set_status("Entry deleted")
        except RuntimeError as exc:
            self._set_status(str(exc), error=True)

    def _form_values(self):
        return (
            self.account_entry.get().strip(),
            self.username_entry.get().strip(),
            self.password_entry.get(),
        )

    def _validate_form(self, account, username, password):
        if not account or not username or not password:
            self._set_status("Account, username, and password are required.", error=True)
            return False
        return True

    def _clear_form(self):
        for entry in (self.account_entry, self.username_entry, self.password_entry):
            entry.delete(0, tk.END)
        self.password_entry.configure(show="*")
        self.password_visible = False
        self.reveal_button.configure(text="Show password")
        self.entries_table.selection_remove(self.entries_table.selection())
        self._set_status("Editor cleared")

    def _set_status(self, message, error=False):
        self.status_label.configure(
            text=f"  {message}  ",
            text_color=ERROR if error else SUCCESS,
        )

    def _close(self):
        self.root.quit()

    def gui(self):
        try:
            self.root.mainloop()
        finally:
            close_window(self.root)

from tkinter import TclError

from customtkinter.windows.widgets.appearance_mode.appearance_mode_tracker import (
    AppearanceModeTracker,
)


def close_window(root):
    """Stop Tk callbacks before destroying a CustomTkinter root window."""
    try:
        root.quit()
    except TclError:
        pass

    try:
        pending_callbacks = root.tk.call("after", "info")
        if isinstance(pending_callbacks, str):
            pending_callbacks = (pending_callbacks,)
        for callback_id in pending_callbacks:
            try:
                root.after_cancel(callback_id)
            except (TclError, ValueError):
                pass
    except TclError:
        pass

    # CustomTkinter keeps roots in a process-wide tracker list. Remove this
    # root so a later window can start its own appearance-mode update loop.
    try:
        if root in AppearanceModeTracker.app_list:
            AppearanceModeTracker.app_list.remove(root)
        if not AppearanceModeTracker.app_list:
            AppearanceModeTracker.update_loop_running = False
    except (AttributeError, TclError):
        pass

    try:
        if root.winfo_exists():
            root.destroy()
    except TclError:
        pass

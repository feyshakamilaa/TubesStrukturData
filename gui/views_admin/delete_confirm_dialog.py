# gui/views_admin/delete_confirm_dialog.py
from PyQt6.QtWidgets import QMessageBox

def confirm_delete(parent):
    result = QMessageBox.question(
        parent,
        "Confirm Delete",
        "Are you sure you want to delete this song?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    return result == QMessageBox.StandardButton.Yes
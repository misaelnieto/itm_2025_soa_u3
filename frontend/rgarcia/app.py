"""Module creates a PyQt6 application with tabs and a button."""

import json
import sys

import api_consumer
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class App(QMainWindow):
    """Test app for the Receta module."""

    def __init__(self):
        super().__init__()
        self.title = "Recetas | dogAteTaco"
        self.setGeometry(0, 0, 600, 600)
        self.setWindowTitle(self.title)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.center()
        self.show()

    def center(self):
        """Centers the window on the screen (PyQt6 way)."""
        screen = QApplication.primaryScreen().availableGeometry()
        window = self.frameGeometry()
        window.moveCenter(screen.center())
        self.move(window.topLeft())

class MyTableWidget(QWidget):
    """A table widget to display the data."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.list_tab = self.list_widget()
        self.modify_tab = self.crud_widget()

        # Add tabs
        self.tabs.addTab(self.modify_tab, "Administración")
        self.tabs.addTab(self.list_tab, "Listado")
        

    
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)  # Now it's safe to set
    def crud_widget(self):
        """Create a tab widget with a form for Receta."""
        tab_widget = QWidget()
        form_layout = QFormLayout()

        # Form fields
        self.id_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.descripcion_input = QLineEdit()
        self.min_preparacion_input = QSpinBox()
        self.min_preparacion_input.setMinimum(1)

        self.ingredientes_input = QTextEdit()
        self.metodo_preparacion_input = QTextEdit()

        # Add fields to form
        form_layout.addRow("Id", self.id_input)
        form_layout.addRow("Nombre", self.nombre_input)
        form_layout.addRow("Descripción", self.descripcion_input)
        form_layout.addRow("Minutos de Preparación", self.min_preparacion_input)
        form_layout.addRow("Ingredientes", self.ingredientes_input)
        form_layout.addRow("Método de Preparación", self.metodo_preparacion_input)

        tab_widget.setLayout(form_layout)
        # Save button

        button_layout = QHBoxLayout()

        # Enter searches for the object
        self.id_input.returnPressed.connect(self.load_recipe)
        self.id_input.textChanged.connect(self.clear_form_fields)

        # Post button
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(lambda: self.save_recipe())

        button_layout.addWidget(self.saveButton)

        # Delete button
        self.deleteButton = QPushButton("Eliminar")
        self.deleteButton.clicked.connect(lambda: self.delete_recipe())
        button_layout.addWidget(self.deleteButton)
        
        form_layout.addRow(button_layout)
        return tab_widget
    
    def save_recipe(self):
        """Save the current recipe."""
        # Checks if the recipe exists already by Id
        response = api_consumer.get_recipe(int(self.id_input.text())) if self.id_input.text() else None
        if not response:
            # If it doesn't exist it creates a new one
            response = api_consumer.post_recipe({
                "nombre": self.nombre_input.text(),
                "descripcion": self.descripcion_input.text(),
                "min_preparacion": self.min_preparacion_input.value(),
                "ingredientes": self.ingredientes_input.toPlainText(),
                "metodo_preparacion": self.metodo_preparacion_input.toPlainText()
            })
            self.id_input.setText(str(response))
        else:
            api_consumer.put_recipe({
            "id": self.id_input.text(),
            "nombre": self.nombre_input.text(),
            "descripcion": self.descripcion_input.text(),
            "min_preparacion": self.min_preparacion_input.value(),
            "ingredientes": self.ingredientes_input.toPlainText(),
            "metodo_preparacion": self.metodo_preparacion_input.toPlainText()
        })
        self.load_recipe()
        self.refreshButton.click()

    def load_recipe(self):
        """Load the recipe data based on the entered recipe id."""
        recipe_id = self.id_input.text()

        if not recipe_id.isdigit():
            # If the id is not a number, you can add an error message or handle it accordingly
            self.showDialog('Las claves solamente pueden contener númreos.','Clav inválida',QMessageBox.Icon.Critical)
            return
        # Get the recipe by ID
        recipe = api_consumer.get_recipe(int(recipe_id))

        # If recipe is not empty, update the form fields with the loaded data
        if recipe:
            self.nombre_input.setText(recipe.get("nombre", ""))
            self.descripcion_input.setText(recipe.get("descripcion", ""))
            self.min_preparacion_input.setValue(recipe.get("min_preparacion", 0))
            self.ingredientes_input.setPlainText(recipe.get("ingredientes", ""))
            self.metodo_preparacion_input.setPlainText(recipe.get("metodo_preparacion", ""))
        else:
            self.id_input.setText('')
        # Sets focus on Nombre field
        self.nombre_input.setFocus()

    def delete_recipe(self):
        """Delete the selected recipe."""
        recipe_id = self.id_input.text()
        if not recipe_id.isdigit():
            # If the id is not a number, you can add an error message or handle it accordingly
            self.showDialog('Las claves solamente pueden contener númreos.','Clav inválida',QMessageBox.Icon.Critical)
            return
        api_consumer.delete_recipe(self.id_input.text())
        self.refreshButton.click()
        self.clear_form_fields()
        self.id_input.setText('')
        self.id_input.setFocus()

    def clear_form_fields(self):
        """Clear all form fields except the ID field."""
        self.nombre_input.clear()
        self.descripcion_input.clear()
        self.min_preparacion_input.setValue(1)  # Reset to minimum value
        self.ingredientes_input.clear()
        self.metodo_preparacion_input.clear()

    def showDialog(self, message: str, title: str, icon=QMessageBox.Icon.Information):
        """Dialog box that blocks until closed."""
        msgBox = QMessageBox()
        msgBox.setIcon(icon)
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Close)  # Add a close button
        msgBox.exec()
    
    
    def list_widget(self):
        """Show a list of the available Recipes in the database."""
        tab_widget = QWidget()
        form_layout = QVBoxLayout()
        list_text_edit = QTextEdit()
        
        list_text_edit.setText(self.get_recipes())

        tab_widget.setLayout(form_layout)
        tab_widget.layout().addWidget(list_text_edit)

        # Refresh Button
        self.refreshButton = QPushButton("Refresh")
        self.refreshButton.clicked.connect(lambda: list_text_edit.setText(self.get_recipes()))

        tab_widget.layout().addWidget(self.refreshButton)

        return tab_widget
    
    def get_recipes(self):
        """Get all the recipes from the API."""
        result = api_consumer.get_recipes()  
        return json.dumps(result, indent=4, ensure_ascii=False)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    ex = App()
    sys.exit(app.exec())

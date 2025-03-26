"""Module creates a PyQt6 application with tabs and a button."""

import json
import sys

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from frontend.rgarcia import api_consumer


class App(QMainWindow):
    """Test app for the Receta module."""

    def __init__(self):
        super().__init__()
        self.title = "PyQt6 tabs - pythonspot.com"
        self.setGeometry(0, 0, 600, 600)
        self.setWindowTitle(self.title)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):
    """A table widget to display the data."""
    
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

        # Load button
        self.loadButton = QPushButton("Buscar")
        self.loadButton.clicked.connect(lambda: self.load_recipe()) 
        self.id_input.returnPressed.connect(self.load_recipe)
        button_layout.addWidget(self.loadButton)

        # Post button
        self.addButton = QPushButton("Save")
        self.addButton.clicked.connect(lambda: api_consumer.post_recipe({
            "nombre": self.nombre_input.text(),
            "descripcion": self.descripcion_input.text(),
            "min_preparacion": self.min_preparacion_input.value(),
            "ingredientes": self.ingredientes_input.toPlainText(),
            "metodo_preparacion": self.metodo_preparacion_input.toPlainText()
        }))
        button_layout.addWidget(self.addButton)

        
        button_layout.addWidget(self.loadButton)

        # Update button
        self.updateButton = QPushButton("Actualizar")
        self.updateButton.clicked.connect(lambda: api_consumer.put_recipe({
            "id": self.id_input.text(),
            "nombre": self.nombre_input.text(),
            "descripcion": self.descripcion_input.text(),
            "min_preparacion": self.min_preparacion_input.value(),
            "ingredientes": self.ingredientes_input.toPlainText(),
            "metodo_preparacion": self.metodo_preparacion_input.toPlainText()
        }))
        button_layout.addWidget(self.updateButton)

        # Delete button
        self.deleteButton = QPushButton("Eliminar")
        self.deleteButton.clicked.connect(lambda: api_consumer.delete_recipe(self.id_input.text()))
        button_layout.addWidget(self.deleteButton)
        
        
       
        form_layout.addRow(button_layout)
        return tab_widget
    
    def load_recipe(self):
        """Load the recipe data based on the entered recipe id."""
        recipe_id = self.id_input.text()
        print('metodo de load_recipe')
        if not recipe_id.isdigit():
            # If the id is not a number, you can add an error message or handle it accordingly
            print("Please enter a valid recipe ID")
            return
        print(recipe_id)
        # Get the recipe by ID
        recipe = api_consumer.get_recipe(int(recipe_id))
        print(recipe)
        # If recipe is not empty, update the form fields with the loaded data
        if recipe:
            self.nombre_input.setText(recipe.get("nombre", ""))
            self.descripcion_input.setText(recipe.get("descripcion", ""))
            self.min_preparacion_input.setValue(recipe.get("min_preparacion", 0))
            self.ingredientes_input.setPlainText(recipe.get("ingredientes", ""))
            self.metodo_preparacion_input.setPlainText(recipe.get("metodo_preparacion", ""))

    def list_widget(self):
        """Create a tab widget with a form for Receta."""
        tab_widget = QWidget()
        form_layout = QVBoxLayout()
        list_text_edit = QTextEdit()
        
        list_text_edit.setText(self.get_recipes())

        tab_widget.setLayout(form_layout)
        tab_widget.layout().addWidget(list_text_edit)
        # Save button
        self.updateButton = QPushButton("Refresh")
        self.updateButton.clicked.connect(lambda: list_text_edit.setText(self.get_recipes()))

        tab_widget.layout().addWidget(self.updateButton)

        
        return tab_widget
    
    def get_recipes(self):
        """Get all the recipes from the API."""
        result = api_consumer.get_recipes()  
        return json.dumps(result, indent=4, ensure_ascii=False)
    
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.list_tab = self.list_widget()
        self.modify_tab = self.crud_widget()

        # Add tabs
        self.tabs.addTab(self.list_tab, "Lista")
        self.tabs.addTab(self.modify_tab, "CRUD")

    
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)  # Now it's safe to set


    @pyqtSlot()
    def on_click(self):
        """Handle the button click event."""
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    ex = App()
    sys.exit(app.exec())

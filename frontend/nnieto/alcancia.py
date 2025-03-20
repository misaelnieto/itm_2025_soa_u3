"""Frontend module for the Alcancía application.

This module provides the user interface for interacting with the Alcancía REST API.
It includes modal screens, forms, and a table for displaying transactions, as well
as methods for communicating with the backend API.

Classes:
    - ModalLoading: A modal screen that displays a loading indicator.
    - ModalError: A modal screen that displays an error message.
    - ModalForm: A modal screen for user input (deposit or withdraw).
    - TransactionsTable: A table for displaying transaction history.
    - Alcancia: The main application class for the frontend.

Functions:
    - run_app(): Runs the Alcancía application.
"""
from decimal import Decimal
from typing import Literal

import httpx
from textual import on
from textual.app import App, ComposeResult
from textual.containers import (
    Center,
    Container,
    Horizontal,
    HorizontalGroup,
    VerticalGroup,
)
from textual.screen import ModalScreen
from textual.validation import Number
from textual.widgets import Button, DataTable, Digits, Header, Input, Label, LoadingIndicator

from .utils import datefmt, moneyfmt

API_BASE_URL = "http://127.0.0.1:8000"


class ModalLoading(ModalScreen):
    """A modal screen that displays a loading indicator.

    This screen is shown while the application is waiting for a response
    from the backend.
    """

    def compose(self):
        """Compose the loading modal screen."""
        yield Container(
            Label("Contactando al backend, por favor espere un momento ..."),
            LoadingIndicator(),
            id="loading",
        )


class ModalError(ModalScreen):
    """A modal screen that displays an error message.

    Args:
        message (str): The error message to display.

    """

    message: str

    def __init__(self, message: str):
        self.message = message
        super().__init__()

    def compose(self):
        """Compose the error modal screen."""
        yield Center(
            Label(self.message, expand=True),
            Container(
                Button.error("Salir", id="quit"),
            ),
        )

    @on(Button.Pressed, "#quit")
    def dimiss_modal(self):
        """Dismiss the modal and exit the application."""
        self.app.pop_screen()
        self.app.exit(1)


TransactionType = Literal["deposit", "withdraw"]
"""The type of transaction. Can be either 'deposit' or 'withdraw'."""


class ModalForm(ModalScreen[Decimal | None]):
    """A modal screen for user input (deposit or withdraw).

    Args:
        variant (TransactionType): The type of transaction ('deposit' or 'withdraw').
        saldo (Decimal): The current balance of the Alcancía.

    """

    cantidad: Decimal
    variant: TransactionType
    saldo: Decimal

    def __init__(self, variant: TransactionType, saldo: Decimal):
        self.variant = variant
        self.saldo = saldo
        super().__init__(id="modal-form")

    def compose(self) -> ComposeResult:
        """Compose the form modal screen."""
        if self.variant == "deposit":
            form_label = "💰 ¿Cuánto quieres depositar? 💰"
            validator = Number(
                minimum=1, failure_description="No puedes depositar valores negativos",
            )
        else:
            form_label = "💰 ¿Cuánto quieres retirar? 💰"
            validator = Number(
                minimum=1, maximum=self.saldo, failure_description="Saldo insuficiente",
            )
        yield Container(
            Label(form_label, expand=True),
            Input(
                type="number",
                valid_empty=False,
                id="cantidad",
                validators=[validator],
            ),
            Label("", classes="hidden", id="validation-errors"),
            Horizontal(
                Button.error("Cancelar", id="cancel"),
                Button.success("Continuar", id="ok", disabled=True),
                id="buttons",
            ),
            id="dialog",
        )

    @on(Button.Pressed, "#cancel")
    def dimiss_modal(self):
        """Dismiss the modal without returning a value."""
        self.app.pop_screen()

    @on(Button.Pressed, "#ok")
    def dismiss_and_return_transaction_vlaue(self):
        """Dismiss the modal and return the entered transaction value."""
        value = self.query_one(Input).value
        self.dismiss(Decimal(value))

    @on(Input.Changed)
    def update_action_button(self, event: Input.Changed) -> None:
        """Update the action button based on input validation."""
        ok_button = self.query_one("#ok")
        messages = self.query_one("#validation-errors")
        if event.validation_result.is_valid:
            cantidad = Decimal(event.value)
            if self.variant == "deposit" or cantidad <= self.saldo:
                messages.update("")
                ok_button.disabled = False
            else:
                messages.classes = ""
                messages.update(f"Solo puedes retirar hasta ${self.saldo}")
                ok_button.disabled = True
        else:
            messages.classes = ""
            messages.update("\n".join(event.validation_result.failure_descriptions))
            ok_button.disabled = True


class TransactionsTable(DataTable):
    """A table for displaying transaction history.

    Attributes:
        BORDER_TITLE (str): The title of the table border.
        BORDER_SUBTITLE (str): The subtitle of the table border.

    """

    BORDER_TITLE = "Lista de movimientos"
    BORDER_SUBTITLE = "Más recientes primero"


class Alcancia(App):
    """The main application class for the Alcancía frontend.

    This class manages the user interface and communicates with the backend API.
    """

    TITLE = "Alcancía"
    SUB_TITLE = "Frontend para app REST de Alcancía"
    CSS_PATH = "css/alcancia.tcss"
    BINDINGS = [("d", "hacer_deposito", "Depositar")]
    SCREENS = {"loading": ModalLoading, "error":ModalError}
    _balance: Decimal = Decimal(0)
    _transactions: list = {}

    def update_balance(self, value: Decimal):
        """Update the displayed balance."""
        self._balance = value
        self.query_one(Digits).update(moneyfmt(self._balance))
        if self._balance > 0:
            self.query_one("#btn-withdraw").disabled = False

    def update_transactions(self, transactions: list):
        """Update the displayed transaction history."""
        self._transactions = transactions
        table = self.query_one(TransactionsTable)
        table.clear()
        table.add_rows(
            [
                (
                    datefmt(t["created_at"]),
                    "🤑 Retiro" if t["amount"] < 0 else "🤩 Depósito",
                    f"{moneyfmt(Decimal(t['amount'] / 100))}",
                )
                for t in transactions
            ],
        )

    def compose(self) -> ComposeResult:
        """Compose the main application layout."""
        yield Header()
        yield HorizontalGroup(
            Container(
                Label("🪙 El saldo de tu alcancía es de 🪙", expand=True),
                Digits(moneyfmt(self._balance), id="saldo-digits"),
                id="saldo",
            ),
            VerticalGroup(
                Button.success("Depósito", id="btn-deposit"),
                Button.warning("Retiro", id="btn-withdraw", disabled=True),
                id="acciones",
            ),
            id="principal",
        )
        table = TransactionsTable()
        table.add_columns("Fecha", "Tipo", "cantidad")
        yield Container(table, id="movimientos")

    async def on_mount(self) -> None:
        """Run tasks when the application is mounted."""
        self.theme = "monokai"
        self.run_worker(self.api_get_transactions)

    @on(Button.Pressed, "#btn-deposit")
    def hacer_deposito(self):
        """Handle the deposit button press."""
        def _callback(amount: Decimal):
            self.run_worker(self.api_put_transaction("deposit", amount), exclusive=True)

        self.push_screen(ModalForm("deposit", self._balance), _callback)

    @on(Button.Pressed, "#btn-withdraw")
    def hacer_retiro(self):
        """Handle the withdraw button press."""
        def _callback(amount: Decimal):
            self.run_worker(
                self.api_put_transaction("withdraw", amount), exclusive=True,
            )

        self.push_screen(ModalForm("withdraw", self._balance), _callback)

    async def api_get_transactions(self) -> None:
        """Fetch the current balance and transactions from the backend."""
        url = f"{API_BASE_URL}/api/v1/nnieto/alcancia/transactions"
        async with httpx.AsyncClient() as client:
            self.push_screen("loading")
            try:
                response = await client.get(url)
                payload = response.json()
            except httpx.ConnectError as e:
                self.log(e)
                self.pop_screen()
                await self.push_screen_wait(ModalError(str(e)))
            else:
                self.pop_screen()
                _balance = sum([t["amount"] for t in payload], start=0)
                self.update_balance(Decimal(_balance) / 100)
                self.update_transactions(reversed(payload))
                self.notify("Saldo y movimientos actualizados")

    async def api_put_transaction(self, txn_variant: TransactionType, amount: Decimal):
        """Send a transaction (deposit or withdraw) to the backend."""
        self.push_screen("loading")
        async with httpx.AsyncClient() as client:
            try:
                txn_response = await client.put(
                    f"{API_BASE_URL}/api/v1/nnieto/alcancia/transaction/{txn_variant}/{int(amount * 100)}",
                )
                txn_payload = txn_response.json()
                txn_lst_response = await client.get(
                    f"{API_BASE_URL}/api/v1/nnieto/alcancia/transactions",
                )
                txn_lst = txn_lst_response.json()
            except httpx.ConnectError as e:
                self.log(e)
                self.notify(str(e), severity="error")
        self.pop_screen()
        if txn_response.status_code != httpx.codes.CREATED:
            self.notify(
                f"Error en la transacción: {txn_response.status_code}", severity="error",
            )
            return
        if txn_lst_response.status_code != httpx.codes.OK:
            self.notify(
                f"Error al descargar saldo y movmientos: {txn_response.status_code}",
                severity="error",
            )
            return
        _balance = txn_payload["balance"]
        self.update_balance(Decimal(_balance) / 100)
        self.update_transactions(txn_lst)
        if txn_payload["result"] == "rejected":
            self.notify("Rechazado por fondos insuficientes", severity="error")
        else:
            self.notify("Saldo y movimientos actualizados")


def run_app():
    """Run the Alcancía application."""
    app = Alcancia()
    app.run()


if __name__ == "__main__":
    run_app()

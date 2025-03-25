"""# 🧪 Test Suite for Alcancia API.

This module contains tests for the Alcancia API endpoints. It verifies the following:
- ✅ The behavior of the API when the database is empty.
- 💰 Deposit transactions.
- 💸 Withdrawal transactions.
- 🔍 Validation of input data for transactions.
"""

from fastapi import status

from app.proyectos.imoreno.schemas import OperationResponse, OperationResult, OperationType

BASE_PATH = "/api/v1/imoreno/hotel"

def test_empty_database(rest_api):
    """🗃️ Tests the API with an empty database."""
    response = rest_api.get(f"{BASE_PATH}/operations")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_operation_add(rest_api):
    """💰 Test adding and updating operations."""
    # First, the operations db is empty
    response = rest_api.get(f"{BASE_PATH}/operations")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    # Now let's register a client
    response = rest_api.put(
        f"{BASE_PATH}/operations/{OperationType.add}/_",
    )
    assert response.status_code == status.HTTP_201_CREATED
    r = OperationResponse(**response.json())
    assert r.result == OperationResult.success


# def test_transaction_withdraw(rest_api):
#     """💸 Test withdrawal transactions."""
#     # First, the Alcancia is empty
#     response = rest_api.get(f"{BASE_PATH}/transactions")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == []

#     # Withdrawing money from an empty Alcancia is not allowed
#     response = rest_api.put(
#         f"{BASE_PATH}/transaction/{OperationType.withdraw}/1",
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     r = OperationResponse(**response.json()["detail"])
#     assert r.result == OperationResult.rejected
#     assert r.previous_balance == 0
#     assert r.balance == 0

#     # Now let's deposit 1 Cent
#     response = rest_api.put(
#         f"{BASE_PATH}/transaction/{OperationType.deposit}/1",
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     r = OperationResponse(**response.json())
#     assert r.result == OperationResult.settled
#     assert r.previous_balance == 0
#     assert r.balance == 1

#     # We cannot withdraw more than 1 cent
#     response = rest_api.put(
#         f"{BASE_PATH}/transaction/{OperationType.withdraw}/2",
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     r = OperationResponse(**response.json()["detail"])
#     assert r.result == OperationResult.rejected
#     assert r.previous_balance == 1
#     assert r.balance == 1

#     # Now let's withdraw that cent
#     response = rest_api.put(
#         f"{BASE_PATH}/transaction/{OperationType.withdraw}/1",
#     )
#     r = OperationResponse(**response.json())
#     assert r.result == OperationResult.settled
#     assert r.previous_balance == 1
#     assert r.balance == 0

#     # We cannot withdraw anything more, not even a cent
#     response = rest_api.put(
#         f"{BASE_PATH}/transaction/{OperationType.withdraw}/1",
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     r = OperationResponse(**response.json()["detail"])
#     assert r.result == OperationResult.rejected
#     assert r.previous_balance == 0
#     assert r.balance == 0


# def test_transaction_validation(rest_api):
#     """🔍 Test validation of transaction inputs."""
#     # We cannot deposit zero cents
#     response = rest_api.put(
#         f"{BASE_PATH}/transaction/{OperationType.deposit}/0",
#     )
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
#     r = response.json()
#     assert r["detail"][0]['loc'] == ['path', 'quantity']
#     assert r["detail"][0]['msg'] == "Input should be greater than 0"

#     # We cannot deposit negative cents
#     response = rest_api.put(
#         f"{BASE_PATH}/transaction/{OperationType.deposit}/-1",
#     )
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
#     r = response.json()
#     assert r["detail"][0]['msg'] == "Input should be greater than 0"

#     # We cannot deposit floating point numbers
#     response = rest_api.put(
#         f"{BASE_PATH}/transaction/{OperationType.deposit}/1.50",
#     )
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
#     r = response.json()
#     assert r["detail"][0]['msg'] == "Input should be a valid integer, unable to parse string as an integer"

#     # We cannot deposit garbage
#     response = rest_api.put(
#         f"{BASE_PATH}/transaction/{OperationType.deposit}/falñdkfs",
#     )
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
#     r = response.json()
#     assert r["detail"][0]['msg'] == "Input should be a valid integer, unable to parse string as an integer"


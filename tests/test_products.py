# Testes para os ambientes de Devolopment (Dev),Staging (Sta) e Production (Prod)

import pytest
import requests
import requests_mock
from fastapi.testclient import TestClient

from products import app, get_user_data, USER_SERVICE_URL, PRODUCTS_DB

# Mock data para resposta do users service 
MOCK_USER_PROFILE = {
    "id": 1,
    "username": "alice",
    "role": "admin"
}

# Setup Pytest Fixtures - TestcClient fixtrua para requests http para a app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

#  Unit Tests 

# Verificação resposta externa com sucesso 
@pytest.mark.unit
@pytest.mark.dev
def test_unit_get_user_data_success(requests_mock):
    user_id = 1
    requests_mock.get(f'{USER_SERVICE_URL}/user/profile/{user_id}', json=MOCK_USER_PROFILE, status_code=200)
    user_info = get_user_data(user_id)
    assert user_info["username"] == "alice"


# Testes de integração (API endpoints) e dependências externas)

#Vericaçaõ do endpoint do produto
@pytest.mark.integration
@pytest.mark.dev
@pytest.mark.staging
def test_integration_product_details_success(client, requests_mock):
    product_id = 101
    owner_id = PRODUCTS_DB[product_id]['owner_id']
    requests_mock.get(f'{USER_SERVICE_URL}/user/profile/{owner_id}', json=MOCK_USER_PROFILE, status_code=200)
    
    response = client.get(f"/product/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["product"]["id"] == 101
    assert data["owner_details"]["username"] == "alice"


# E2E Tests 

# Verificação da comunicação 
@pytest.mark.e2e
@pytest.mark.staging
def test_e2e_critical_data_aggregation(client, requests_mock):
    product_id = 103
    owner_id = PRODUCTS_DB[product_id]['owner_id']
    mock_payload = {"id": owner_id, "username": "charlie_owner", "role": "power_user"}
    requests_mock.get(f'{USER_SERVICE_URL}/user/profile/{owner_id}', json=mock_payload, status_code=200)

    response = client.get(f"/product/{product_id}")
    assert response.status_code == 200
    data = response.json()
    
    assert data["product"]["name"] == "Keyboard"
    assert data["owner_details"]["username"] == "charlie_owner"


# Sanity Tests 

# Verifcação status root endpoint
@pytest.mark.sanity
@pytest.mark.dev
@pytest.mark.staging
@pytest.mark.prod
def test_sanity_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), list) or isinstance(response.json(), dict)
    
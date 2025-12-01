# Testes para os ambientes de Devolopment (Dev),Staging (Sta) e Production (Prod)

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from users import app, get_user_profile

# Setup Pytest Fixtures - TestcClient fixtrua para requests http para a app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Unit Tests 

# Vericficação resposta com sucesso
@pytest.mark.unit
@pytest.mark.dev
def test_unit_get_user_profile_success():
    user_id = 1
    result = get_user_profile(user_id)
    assert result.body == b'{"id":1,"username":"alice","role":"admin"}'

# Verificaçâo de resposta errada/valor nao encontrado
@pytest.mark.unit
@pytest.mark.dev
def test_unit_get_user_profile_not_found():
    with pytest.raises(HTTPException) as excinfo:
        get_user_profile(999)
    assert excinfo.value.status_code == 404


# Testes de integração (API endpoints)

# Verificação do formato de resposta json
@pytest.mark.integration
@pytest.mark.dev
@pytest.mark.staging
def test_integration_profile_endpoint_json_structure(client: TestClient):
    response = client.get("/user/profile/2")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "bob"


# Testes E2E 

# Verificação full user check
@pytest.mark.e2e
@pytest.mark.staging
def test_e2e_full_user_check(client: TestClient):
    profile_response = client.get("/user/profile/1")
    assert profile_response.status_code == 200
    status_response = client.get("/user/status")
    assert status_response.status_code == 200

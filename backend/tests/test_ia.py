from unittest.mock import patch

def test_sugestao_ia_com_mock(client):
    with patch("app.routers.ia.descricao_IA") as mock_ia:
        mock_ia.return_value = {
            "descricao": "Mock: introdução à álgebra",
            "tags": ["álgebra", "equações", "ensino médio"]
        }
        response = client.post("/ia/sugestao", json={
            "titulo": "Álgebra Linear",
            "tipo": "video"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["descricao"] == "Mock: introdução à álgebra"
        assert data["tags"] == "álgebra, equações, ensino médio"
def test_criar_recurso(client):
    response = client.post("/recursos/", json={
        "titulo": "Matemática Básica",
        "tipo": "pdf",
        "descricao": "Apostila introdutória",
        "link": "http://exemplo.com/mat.pdf",
        "tags": "matemática, básico"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Matemática Básica"
    assert "id" in data

def test_listar_recursos(client):
    client.post("/recursos/", json={
        "titulo": "Outro recurso",
        "tipo": "video",
        "descricao": "Vídeo aula",
        "link": "http://exemplo.com/video",
        "tags": "aula, vídeo"
    })
    response = client.get("/recursos/?skip=0&limit=10")
    assert response.status_code == 200
    json_data = response.json()
    assert "items" in json_data
    assert len(json_data["items"]) > 0
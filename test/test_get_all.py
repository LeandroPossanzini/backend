def test_get_all(client):
    #Verifico que la ruta funcione
    res = client.get("/get_all")
    assert res.status_code == 200

def test_response(client):
    #Verifico que el tipo de dato sea una lista
    res = client.get("/get_all")
    data = res.get_json()
    assert isinstance(data, list)

def test_response_fields(client):
    #Chequeo que me devuelva los campos esperados
    res = client.get("/get_all")
    data = res.get_json()
    if len(data) > 0:
        product = data[0]
        for field in ["id", "title", "price", "currency", "images", "seller", "additional_details", "payment_methods"]:
            assert field in product

def test_get_all_whit_token(client, test_token):
    #Verifico que la ruta funcione
    headers = {"Authorization": f"Bearer {test_token}"}
    res = client.get("/get_all", headers=headers)
    assert res.status_code == 200
# x = requests.get('https://www.agurait.com/ubp/sia/2022/roberto/')
# {'S1':'-1', 'S2':'1', 'S3':'-1', 'S4':'-1'}
# body = [{'S1':'-1', 'S2':'-1', 'S3':'-1', 'S4':'1', 'M1':'1', 'M2':'-1'}]
import requests

class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self):
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            data = response.json()
            if data != None:
                return data[0]['Resp']
            else:
                raise ValueError("Respuesta inesperada del servidor")
        except requests.RequestException as e:
            raise RuntimeError(f"Error en la solicitud GET: {e}")

    def post(self, resultado: dict):
        payload = [resultado]
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            data = response.json()
            if data != None:
                return data
            else:
                raise ValueError("Respuesta inesperada del servidor")
        except requests.RequestException as e:
            raise RuntimeError(f"Error en la solicitud POST: {e}")
        
    def ArraytoJSON(self, array):
        if not isinstance(array, list) or len(array) != 6:
            raise ValueError("El array debe tener exactamente 6 elementos.")

        keys = ['S1', 'S2', 'S3', 'S4', 'M1', 'M2']
        str_values = [str(v) for v in array]

        return [dict(zip(keys, str_values))]
        
    def JSONtoArray(self, json):
        claves = ['S1', 'S2', 'S3', 'S4']
        return [int(json[clave]) for clave in claves]
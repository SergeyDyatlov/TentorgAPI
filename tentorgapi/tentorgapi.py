from datetime import datetime, timedelta, timezone
import json
import chardet
import requests


class TentorgAPI:
    def __init__(self, email, password):
        self.base_url = "https://api.tentorg.ru/openapi"
        self.email = email
        self.password = password
        self.token = None

    def authenticate(self):
        url = f"{self.base_url}/sign/in"
        payload = {"email": self.email, "password": self.password}

        response = requests.post(url, data=payload)
        response_data = response.json()

        if response_data.get("status") == "ok":
            self.token = response_data["body"]["openapi_token"]
            print("Авторизация прошла успешно, токен:", self.token)
        else:
            raise Exception(f"Ошибка авторизации: {response_data.get('message')}")

    def make_request(self, endpoint, method="GET", data=None):
        if not self.token:
            raise Exception("Необходимо авторизоваться перед выполнением запросов.")

        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        if method.upper() == "GET":
            response = requests.get(url, headers=headers, json=data)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, json=data)
        else:
            raise ValueError("Метод запроса не поддерживается.")

        return response.json()

    def get_orders(self, page=1):
        response_data = self.make_request(f"order?page={page}")
        decoded_response_data = fix_and_decode(response_data)
        
        orders = []
        for response in decoded_response_data:
            json_property = response.get("json_property", {})
            if isinstance(json_property, str):
                json_property = json.loads(json_property)
                response["json_property"] = json_property
            if isinstance(json_property, dict):
                # Приведение всех дат к единому формату '%d.%m.%Y %H:%M:%S %z'
                creation_time = datetime.strptime(json_property['creation_time'], "%d.%m.%Y %H:%M:%S %z")
                json_property['creation_time'] = creation_time.strftime('%d.%m.%Y %H:%M:%S %z')

                tender_start = datetime.strptime(json_property['tender_start'], "%d.%m.%Y %H:%M:%S %z")
                json_property['tender_start'] = tender_start.strftime('%d.%m.%Y %H:%M:%S %z')
                
                tender_end = datetime.fromtimestamp(json_property['tender_end'], tz=timezone(timedelta(hours=3)))
                json_property['tender_end'] = tender_end.strftime('%d.%m.%Y %H:%M:%S %z')

                orders.append(json.dumps(json_property, indent=4, ensure_ascii=False))
      
        return orders


def fix_and_decode(data):
    if isinstance(data, dict):
        return {key: fix_and_decode(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [fix_and_decode(item) for item in data]
    elif isinstance(data, str):
        byte_data = data.encode()
        detected_encoding = chardet.detect(byte_data)
        encoding = detected_encoding.get("encoding")
        if encoding:
            return byte_data.decode(encoding)
        else:
            return data  # Возвращаем исходную строку, если не удалось определить кодировку
    else:
        return data  # Возвращаем неизмененные данные, если это не строка, список или словарь


if __name__ == '__main__':
    client = TentorgAPI("user@example.com", "password123")
    client.authenticate()

    orders = client.get_orders(page=1)
    [print(order) for order in orders]

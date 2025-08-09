import requests

headers = {
        "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImV4cCI6MTc1NTM1ODI2OH0._F0jJRx9CH7z4cYJ3KsV06enjqgZSx0S7MD00jYNW-4"

}

request = requests.get("http://127.0.0.1:8000/auth/refresh",headers=headers)
print(request)
print(request.json)
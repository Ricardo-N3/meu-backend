import requests

headers = {
        "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzU1NDY3Nzc2fQ.OSms2XEu-3Iec9DDHBgmg3wY8q9PNPnJNkP5DSHk9_Y"

}

response = requests.get("http://127.0.0.1:8000/auth/refresh",headers=headers)
print(response)
print(response.json())

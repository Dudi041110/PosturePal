import time
import requests

def send_signal(server_url, route="/signal", data=None):
    """
    Sends data to another Flask server.

    server_url : base URL of target server
    route      : endpoint to call
    data       : dictionary containing any data
    """

    url = f"{server_url}{route}"

    try:
        response = requests.get(url, json=data)

        print("Signal sent!")
        print("Response:", response.text)

    except Exception as e:
        print("Failed to send signal:", e)

print("Website link: https://suave-quietly-irvin.ngrok-free.dev")
print("Press enter to send a test signal...")
time.sleep(0.5)
while True:
    input("> ")
    time.sleep(0.1)
    send_signal(
        "http://192.168.1.199:8090",
        "/signal",
        {"message": "Bad posture detected"}
    )
    time.sleep(0.4)
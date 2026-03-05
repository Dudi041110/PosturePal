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

def test_send_sensitivity(flask_ip, slider_value):
    """
    Test function to send a slider value to PosturePal backend.

    Parameters:
    - flask_ip: str -> IP of your Flask server (e.g., "192.168.1.202")
    - slider_value: int -> 0-100 slider value
    """

    url = f"http://{flask_ip}:8090/setSensitivity"
    payload = {"sliderValue": slider_value}

    try:
        response = requests.post(url, json=payload, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                print(f"[Test] Sensitivity set to {data['angleThreshold']}°")
            else:
                print(f"[Test] Error from server: {data}")
        else:
            print(f"[Test] Server responded with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[Test] Failed to connect to Flask server: {e}")

print("Website link: https://suave-quietly-irvin.ngrok-free.dev")
print("Please type 1 to send a notification test and type 2 to change the sensitivity...")
time.sleep(0.5)
while True:
    if input("> ") == "1":
        time.sleep(0.1)
        send_signal(
            "http://192.168.1.199:8090",
            "/signal",
            {"message": "Bad posture detected"}
        )
        time.sleep(0.4)
    else:
        time.sleep(0.1)
        while True:
            try:
                x = int(input("What would you like to set the sensitivity to (type an integer between 0 and 100). \n> "))
                break
            except:
                print("Type an integer between 0 and 100.")

        # Replace with your Flask server IP
        flask_ip = "192.168.1.199"

        # Test sending slider value 50 (should map to 6°)
        test_send_sensitivity(flask_ip, x)

        time.sleep(0.4)
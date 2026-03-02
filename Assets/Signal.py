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
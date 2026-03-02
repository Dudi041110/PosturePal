import Signal
import time

print("Website link: https://suave-quietly-irvin.ngrok-free.dev")
print("Press enter to send a test signal...")
time.sleep(0.5)
while True:
    input("> ")
    time.sleep(0.1)
    Signal.send_signal(
        "http://192.168.1.199:8090",
        "/signal",
        {"message": "Bad posture detected"}
    )
    time.sleep(0.4)
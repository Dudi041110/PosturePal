## REQUIREMENTS
- Python (and pip) must be installed on your computer (If you want to run the server).
- You must have the PosturePal device with you (or at least the part needed to build one (details below...)).
- Arduino IDE.
- A 2.4Ghz wifi (Username + Password).
## HOW TO RUN (server)
- Step 1: Have python (and pip) installed on your computer.
- Step 2: Install the libraries within "Assets\requirements.txt".
  - You can try this command however it may not always work (You must be in the directory "PosturePal"):
      ```Shell
      pip install -r Assets/requirements.txt
      ```
- Step 3:
  - IF YOUR ON MAC/LINUX:
    - Step 1: Open terminal.
    - Step 2: Change the directory to the path of the file "Run (Mac~Linux).sh".
    - Step 3: Run these 2 commands in the terminal:
        ```Batchfile
        chmod +x "Run (Mac\~Linux).sh"
        ./"Run (Mac\~Linux).sh"
        ```
    - WARNING:
      - This may not work as it has not been tested as thoroughly as the windows version
  - IF YOUR ON WINDOWS:
    - Run the "Run (Windows).bat" file by double clicking it.
## HOW TO BUILD (The PosturePal device)
- Requirements:
  - 2 MPU6050 modules.
  - A vibration module.
  - A NodeMCU V2 board.
  - Micro-USB cable.
  - Jumper Wires.
  - BreadBoard (Optional)
- Instructions:
  - Step 1:
    - Connect the NodeMCU V2 pins to all of these (It is recommended to use a breadboard for organization and simplicity):
      - MPU6050 module (1) (From NodeMCU to MPU6050):
        - 3V3 => VCC
        - GND => GND
        - D1 => SCL
        - D2 => SDA
        - 3V3 => AD0
      - MPU6050 module (2) (From NodeMCU to MPU6050):
        - 3V3 => VCC
        - GND => GND
        - D1 => SCL
        - D2 => SDA
        - GND => AD0
      - Vibration Module (From NodeMCU to Vibration Module):
        - D5 => IN
        - VIN => VCC
        - GND => GND
  - Step 2:
    - Open Arduino IDE and open the file named "Gyro_vibro.ino" located in "Assets\Gyro_vibro".
    - Open File then Preferences and add this url under "Additional Board Managar URLs":
      > http://arduino.esp8266.com/stable/package_esp8266com_index.json
    - Go to Tools then Board then Board Manager then search ESP8266 and install "ESP8266 Arduino Core".
    - After installing go to Tools then Board then ESP8266 Boards then select "NodeMCU 1.0 (ESP-12E Module)"
    - After selecting the boards, you must download the CP210x driver from [here](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads):
      > https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads
    - After downloading the driver, open the downloaded file and click install.
    - Via Library Manager, install the Wire and MPU6050 libraries.
  - Step 3:
    - After installing all the required files, you need to set the baud rate to 115200 baud.
    - Go to Tools then Upload speed and set it to 115200.
    - Go to Tools then Port and select the port that you plugged the board into.
    - Scroll to the top of the file and replace the username and password with whatever the password is to the username and password of your 2.4Ghz wifi:
        ```C++
        const char* ssid = "DUDI041110 0002";  //(Replace DUDI041110 0002 with your wifi username)
        const char* password = "adam12345";    //(Replace adam12345 with your wifi password)
        ```
    - Scroll slightly lower to this function:
        ```C++
        void sendNotification() {
            WiFiClient client;
        
            Serial.println("Sending notification...");
        
            if (client.connect("192.168.1.202", 8090)) {
                client.print(String("GET /signal HTTP/1.1\r\n") +
                             "Host: 192.168.1.202\r\n" +
                             "Connection: close\r\n\r\n");
        
                Serial.println("Notification sent!");
            } else {
                Serial.println("Connection failed");
            }
        
            client.stop();
        }
        ```
    - Replace the IP with the second IP you get from activating the server:
        ```C++
        if (client.connect("192.168.1.202", 8090)) {  //(Replace 192.168.1.202 with your IP)
        ```
    - And finally you can Upload the program to the board.
## HOW TO OPEN/DOWNLOAD THE WEBSITE/APP
- How to open the website:
  - After following the tutorials within the How to Build and How to Run sections of the README, Open this [link](https://suave-quietly-irvin.ngrok-free.dev):
    > https://suave-quietly-irvin.ngrok-free.dev
- How to download the app:
  - ON YOUR IPHONE (I don't know how to do it on Samsung):
    - Open the [link](https://suave-quietly-irvin.ngrok-free.dev) on safari:
      > https://suave-quietly-irvin.ngrok-free.dev
    - Go to Share then scroll down untill you find Add to Home Screen.
    - Click the button and now you will have the app on your Home Screen; HOWEVER, it will not work unless the server is active (follow the steps in How to Run for information on how to activate the server).

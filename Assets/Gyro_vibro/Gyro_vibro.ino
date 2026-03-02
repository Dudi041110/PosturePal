#include <Wire.h>
#include <MPU6050.h>
#include <ESP8266WiFi.h>

//////////////////// WIFI ////////////////////
const char* ssid = "DUDI041110 0002";
const char* password = "adam12345";

const char* host = "192.168.1.202";
const int port = 8090;

//////////////////// MPU ////////////////////
MPU6050 mpu1(0x68);
MPU6050 mpu2(0x69);

float xThreshold = 1000;

int16_t startAx1, startAx2;

//////////////////// MOTOR ////////////////////
const int motorPin = D5;

//////////////////// TIMER ////////////////////
unsigned long vibrationStart = 0;
const unsigned long notifyTime = 30000; // 30 sec

bool vibrating = false;
bool notificationSent = false;

////////////////////////////////////////////////

void sendNotification() {
    WiFiClient client;

    Serial.println("Sending notification...");

    if (client.connect(host, port)) {
        client.print(String("GET /signal HTTP/1.1\r\n") +
                     "Host: " + host + "\r\n" +
                     "Connection: close\r\n\r\n");

        Serial.println("Notification sent!");
    } else {
        Serial.println("Connection failed");
    }

    client.stop();
}

////////////////////////////////////////////////

void setup() {
    Serial.begin(115200);

    Wire.begin(D2, D1); // SDA, SCL
    pinMode(motorPin, OUTPUT);

    ////// WiFi //////

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    Serial.print("Connecting WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nWiFi Connected");
    Serial.println(WiFi.localIP());

    ////// MPU INIT //////

    mpu1.initialize();
    mpu2.initialize();

    if (!mpu1.testConnection()) {
        Serial.println("MPU1 FAIL");
        while (1);
    }

    if (!mpu2.testConnection()) {
        Serial.println("MPU2 FAIL");
        while (1);
    }

    int16_t ax1, ay1, az1, gx1, gy1, gz1;
    int16_t ax2, ay2, az2, gx2, gy2, gz2;

    mpu1.getMotion6(&ax1,&ay1,&az1,&gx1,&gy1,&gz1);
    mpu2.getMotion6(&ax2,&ay2,&az2,&gx2,&gy2,&gz2);

    startAx1 = ax1;
    startAx2 = ax2;

    Serial.println("Calibration complete");
}

////////////////////////////////////////////////

void loop() {

    int16_t ax1, ay1, az1, gx1, gy1, gz1;
    int16_t ax2, ay2, az2, gx2, gy2, gz2;

    mpu1.getMotion6(&ax1,&ay1,&az1,&gx1,&gy1,&gz1);
    mpu2.getMotion6(&ax2,&ay2,&az2,&gx2,&gy2,&gz2);

    int xDiff = abs((ax1 - startAx1) - (ax2 - startAx2));

    Serial.println(xDiff);

    ////////////////// POSTURE CHECK //////////////////

    if (xDiff > xThreshold) {

        digitalWrite(motorPin, HIGH);

        if (!vibrating) {
            vibrating = true;
            vibrationStart = millis();
            notificationSent = false;
            Serial.println("Bad posture detected");
        }

        // 30s reached
        if (!notificationSent &&
            millis() - vibrationStart >= notifyTime) {

            sendNotification();
            notificationSent = true;
        }

    } 
    else {

        digitalWrite(motorPin, LOW);
        vibrating = false;
        notificationSent = false;
    }

    delay(100);
}

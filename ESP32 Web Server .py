import network
import socket
from machine import Pin
import time

# Built-in LED
led = Pin(2, Pin.OUT)

# Wi-Fi details
SSID = "YOUR_WIFI_NAME"
PASSWORD = "YOUR_WIFI_PASSWORD"

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Connecting to Wi-Fi...")

while not wifi.isconnected():
    time.sleep(1)

print("Wi-Fi Connected!")
print("ESP32 IP Address:", wifi.ifconfig()[0])

# Create web server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 80))
server.listen(1)

print("Web server started...")

while True:

    client, address = server.accept()

    request = client.recv(1024).decode()

    # Turn LED ON
    if "/LED=ON" in request:
        led.value(1)

    # Turn LED OFF
    if "/LED=OFF" in request:
        led.value(0)

    # Web page
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 Web Server</title>
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
    </head>

    <body style="text-align:center;
                 font-family:Arial;
                 background-color:#f2f2f2;">

        <h1>ESP32 Web Server</h1>

        <h2>LED Control</h2>

        <a href="/LED=ON">
            <button style="font-size:25px;
                           padding:15px;">
                LED ON
            </button>
        </a>

        <br><br>

        <a href="/LED=OFF">
            <button style="font-size:25px;
                           padding:15px;">
                LED OFF
            </button>
        </a>

    </body>
    </html>
    """

    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html\r\n"
    response += "Connection: close\r\n\r\n"
    response += html

    client.send(response)
    client.close()

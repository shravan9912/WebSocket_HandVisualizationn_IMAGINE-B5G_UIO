import socket
import cv2
import asyncio
import websockets
import re

async def video_stream(websocket, path):
    vid = cv2.VideoCapture(0)
    
    while vid.isOpened():
        ret, frame = vid.read()
        if not ret:
            break
            
        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        message = buffer.tobytes()  # Get the bytes of the encoded image
        
        try:
            await websocket.send(message)  # Send the frame
        except Exception as e:
            print("Error sending data:", e)
            break

    vid.release()

def is_valid_ip(ip):
    """ Validate IP address (IPv4 or IPv6) """
    ipv4_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    ipv6_pattern = r'^[0-9a-fA-F:]{1,}$'
    return re.match(ipv4_pattern, ip) is not None or re.match(ipv6_pattern, ip) is not None

def is_valid_port(port):
    """ Validate port number (1-65535) """
    return 1 <= port <= 65535

def get_server_details():
    """ Prompt user for server IP and port """
    while True:
        ip = input("Enter the IP address of this computer server (IPv4 or IPv6): ")
        if is_valid_ip(ip):
            break
        print("Invalid IP address. Please enter a valid IP address.")
    
    while True:
        try:
            port = int(input("Enter the port number (1-65535): "))
            if is_valid_port(port):
                break
            else:
                print("Invalid port number. Please enter a valid port number.")
        except ValueError:
            print("Invalid input. Please enter a numeric port number.")
    
    return ip, port

# Get server details from the user
server_ip, server_port = get_server_details()
start_server = websockets.serve(video_stream, server_ip, server_port)
print(f"Starting WebSocket server on ws://{server_ip}:{server_port}")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


import socket
import cv2
import asyncio
import websockets

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

# Fetch local IP address
def get_local_ip():
    try:
        # Create a socket and connect to an external service
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's public DNS server
        ip = s.getsockname()[0]     # Get the local IP address
    finally:
        s.close()
    return ip

# Get the local IP and start the WebSocket server
local_ip = get_local_ip()
start_server = websockets.serve(video_stream, local_ip, 10050)
print(f"Starting WebSocket server on ws://{local_ip}:10050")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


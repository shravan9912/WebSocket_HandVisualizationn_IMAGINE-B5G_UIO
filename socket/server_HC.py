import socket
import cv2
import pickle
import struct
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

start_server = websockets.serve(video_stream, '192.168.50.164', 10050)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


import av
import cv2
import numpy as np

input_container = av.open("input.mp4")
output_container = av.open("output.mp4", mode='w')

input_stream = input_container.streams.video[0]
output_stream = output_container.add_stream('libx264', rate=input_stream.rate)
output_stream.width = input_stream.width
output_stream.height = input_stream.height
output_stream.pix_fmt = 'yuv420p'

for frame in input_container.decode(video=0):
    # Convert frame to numpy array
    img = frame.to_ndarray(format='bgr24')
    
    # Apply OpenCV effects
    processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)  # back to 3 channels
    
    # Create new frame
    new_frame = av.VideoFrame.from_ndarray(processed_img, format='bgr24')
    new_frame.pts = frame.pts
    new_frame.time_base = frame.time_base

    # Encode and mux
    for packet in output_stream.encode(new_frame):
        output_container.mux(packet)

# Flush encoder
for packet in output_stream.encode():
    output_container.mux(packet)

input_container.close()
output_container.close()

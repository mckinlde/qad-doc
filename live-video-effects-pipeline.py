import av
import cv2
import numpy as np

print('start')
input_container = av.open("/Users/douglasmckinley/VSCodeProjects/qad-doc-folder/qad-doc/RickRoll.mp4")
output_container = av.open("output.mp4", mode='w')
print('opened filed')
input_stream = input_container.streams.video[0]
output_stream = output_container.add_stream('libx264', rate=input_stream.average_rate)
output_stream.width = input_stream.width
output_stream.height = input_stream.height
output_stream.pix_fmt = 'yuv420p'
print("init'd streams")
for frame in input_container.decode(video=0):
    print('frame')
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
print('end frames')
# Flush encoder
for packet in output_stream.encode():
    output_container.mux(packet)
print('end mux')
input_container.close()
output_container.close()
print('containers closed; exiting')
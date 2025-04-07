import av
import cv2
import numpy as np

print('start')
input_container = av.open("RickRoll.mp4")
output_container = av.open("output.mp4", mode='w')
print('opened file')

# Set up video stream
input_video_stream = next(s for s in input_container.streams if s.type == 'video')
output_video_stream = output_container.add_stream('libx264', rate=input_video_stream.average_rate or 30)
output_video_stream.width = input_video_stream.width
output_video_stream.height = input_video_stream.height
output_video_stream.pix_fmt = 'yuv420p'

# Set up audio stream (passthrough without decoding/encoding)
input_audio_stream = next((s for s in input_container.streams if s.type == 'audio'), None)
if input_audio_stream:
    output_audio_stream = output_container.add_stream(input_audio_stream.codec.name)
else:
    output_audio_stream = None

print("init'd streams")

# Loop through packets from all streams (demux)
for packet in input_container.demux():
    if packet.stream == input_video_stream:
        # Decode video packets into frames
        for frame in packet.decode():
            # Apply a grayscale effect using OpenCV
            # Because even though the 80s feel like 20 years ago...
            img = frame.to_ndarray(format='bgr24')
            processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            processed_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)

            # Re-encode the processed frame
            new_frame = av.VideoFrame.from_ndarray(processed_img, format='bgr24')
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base

            for out_packet in output_video_stream.encode(new_frame):
                # Mux the encoded video packet into output container
                output_container.mux(out_packet)

    elif output_audio_stream and packet.stream == input_audio_stream:
        # Mux audio packet directly (no decoding/encoding)
        if packet.dts is not None:
            output_container.mux(packet)

# Flush remaining buffered video frames from encoder
for packet in output_video_stream.encode():
    output_container.mux(packet)

print('end flush')
input_container.close()
output_container.close()
print('containers closed; exiting')

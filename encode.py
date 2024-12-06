import cv2
import numpy as np


def encode_wav(msg: bytearray, wav_data: bytearray, params) -> bytearray:
    res = wav_data

    size = len(msg)

    msg_bits = [(size >> i)&1 for i in range(4 * 8)]
    for c in msg:
        msg_bits += [(c>>i)&1 for i in range(8)]

    j = 0
    for i in range(0, len(wav_data), params.sampwidth):
        if wav_data[i] % 2 != msg_bits[j]:
            s = 1
            if wav_data[i] == 255:
                s = -1

            res[i] += s
        
        j += 1
        if j>=len(msg_bits):
            break

    return res

def encode_image(msg: bytearray, image_data: bytearray, params) -> bytearray:
    res = image_data

    size = len(msg)

    msg_bits = [(size >> i)&1 for i in range(4 * 8)]
    for c in msg:
        msg_bits += [(c>>i)&1 for i in range(8)]

    j = 0
    for i in range(0, len(image_data)):
        if image_data[i] % 2 != msg_bits[j]:
            s = 1
            if image_data[i] == 255:
                s = -1

            res[i] += s

        j += 1
        if j>=len(msg_bits):
            break

    return res

def encode_video(msg: bytearray, video_capture: cv2.VideoCapture, output_video_file: str) -> None:
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))

    h = int(video_capture.get(cv2.CAP_PROP_FOURCC))

    out = cv2.VideoWriter(output_video_file,cv2.VideoWriter_fourcc(*'FFV1'), video_capture.get(cv2.CAP_PROP_FPS), (frame_width,frame_height))

    size = len(msg)

    msg_bits = [(size >> i)&1 for i in range(4 * 8)]
    for c in msg:
        msg_bits += [(c>>i)&1 for i in range(8)]

    j = 0
    while(True):
        ret, frame = video_capture.read()
        if not ret:
            break

        frame_shape = frame.shape
        frame = bytearray(frame.tobytes())

        if j < len(msg_bits):
            for i in range(0, len(frame)):
                if frame[i] % 2 != msg_bits[j]:
                    s = 1
                    if frame[i] == 255:
                        s = -1

                    frame[i] += s

                j += 1
                if j>=len(msg_bits):
                    break

        frame_data = np.frombuffer(frame, dtype=np.uint8)

        frame = frame_data.reshape(frame_shape)
        out.write(frame)
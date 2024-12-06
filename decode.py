import cv2

def decode_wav(wav_data: bytearray, params) -> bytearray:
    msg_data = bytearray()

    size_bits = []
    for i in range(0, 4 * 2 * 8, 2):
        size_bits.append(wav_data[i] % 2)

    msg_size = 0
    for j, size_bit in enumerate(size_bits):
        msg_size |= (size_bit<<j)

    bits = []
    for i in range(4 * 2 * 8, (4 + msg_size + 1) * 2 * 8, 2):
        bits.append(wav_data[i] % 2)

    value = 0
    j = 0

    for j, bit in enumerate(bits):
        if j % 8 == 0 and j != 0:
            msg_data.append(value)
            value = 0
        value |= (bit<<(j % 8))

    return msg_data

def decode_image(image_data: bytearray, params) -> bytearray:
    msg_data = bytearray()

    size_bits = []
    for i in range(0, 4 * 8):
        size_bits.append(image_data[i] % 2)

    msg_size = 0
    for j, size_bit in enumerate(size_bits):
        msg_size |= (size_bit<<j)

    bits = []
    for i in range(4 * 8, (4 + msg_size + 1) * 8):
        bits.append(image_data[i] % 2)

    value = 0
    for j, bit in enumerate(bits):
        if j % 8 == 0 and j != 0:
            msg_data.append(value)
            value = 0
        value |= (bit<<(j % 8))

    return msg_data

def decode_video(video_capture: cv2.VideoCapture) -> bytearray:
    msg_data = bytearray()

    ret, frame = video_capture.read()

    if not ret:
        return msg_data
    
    frame = bytearray(frame.tobytes())
    
    size_bits = []
    for i in range(0, 4 * 8):
        size_bits.append(frame[i] % 2)

    msg_size = 0
    for j, size_bit in enumerate(size_bits):
        msg_size |= (size_bit<<j)

    frame = frame[32:-1]

    value = 0
    j = 0
    while(True):
        bits = []
        for i in range(0, min(len(frame), (msg_size + 1) * 8)):
            bits.append(frame[i] % 2)

        for bit in bits:
            if j % 8 == 0 and j != 0:
                msg_data.append(value)
                value = 0
            value |= (bit<<(j % 8))
            j += 1

        ret, frame = video_capture.read()
        if not ret:
            break 

        frame = bytearray(frame.tobytes())

    return msg_data

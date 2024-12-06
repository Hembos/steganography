import wave
from config import read_works
from work import check_work, WorkType, Work, FileWorkType
from decode import decode_wav, decode_image, decode_video
from encode import encode_wav, encode_image, encode_video
import cv2
import numpy as np
import tqdm


def read_wav_file(wav_file_name: str) -> tuple:
    with wave.open(wav_file_name, mode='rb') as wav:
        frames = bytearray(wav.readframes(wav.getnframes()))
        params = wav.getparams()

    return frames, params

def write_wav_file(wav_file_name: str, params, data: bytearray) -> None:
    with wave.open(wav_file_name, 'wb') as wav:
        wav.setparams(params)
        wav.writeframes(bytes(data))

def read_image_file(image_file_name: str) -> tuple:
    image = cv2.imread(image_file_name)

    return bytearray(image.tobytes()), {'shape': image.shape}

def write_image_file(image_file_name: str, params, data: bytearray) -> None:
    image_data = np.frombuffer(data, dtype=np.uint8)

    image = image_data.reshape(params['shape'])

    cv2.imwrite(image_file_name, image)

def read_video_file(video_file_name: str) -> cv2.VideoCapture:
    return cv2.VideoCapture(video_file_name)

read_func = {
    FileWorkType.AUDIO: read_wav_file,
    FileWorkType.IMAGE: read_image_file
}

write_func = {
    FileWorkType.AUDIO: write_wav_file,
    FileWorkType.IMAGE: write_image_file
}

decode_func = {
    FileWorkType.AUDIO: decode_wav,
    FileWorkType.IMAGE: decode_image
}

encode_func = {
    FileWorkType.AUDIO: encode_wav,
    FileWorkType.IMAGE: encode_image
}

def decode_work(work: Work) -> None:
    with open(work.outFile, mode='wb') as msg_file:
        if work.fileType == FileWorkType.VIDEO:
            cap = read_video_file(work.inFile)

            if (cap.isOpened()): 
                msg = decode_video(cap)
                msg_file.write(msg)

            return

        data, params = read_func[work.fileType](work.inFile)
        msg = decode_func[work.fileType](data, params)
        msg_file.write(msg)

def encode_work(work: Work) -> None:
    with open(work.inFile, mode='rb') as msg_file:
        b = msg_file.read()
        msg = bytearray(b)

        if work.fileType == FileWorkType.VIDEO:
            cap = read_video_file(work.toFile)
            encode_video(msg, cap, work.outFile)
            return

        data, params = read_func[work.fileType](work.toFile)

        stego_data = encode_func[work.fileType](msg, data, params)

        write_func[work.fileType](work.outFile, params, stego_data)

if __name__=="__main__":
    works = read_works("config.xml")

    for i, work in enumerate(tqdm.tqdm(works)):
        if not check_work(work):
            print(f"Work {i}: incorrect configuration")
            continue

        if work.type == WorkType.ENCODE:
            encode_work(work)
        else:
            decode_work(work)

import torch
from easyocr import Reader


class CaptchaReader:
    def __init__(self):
        gpu = torch.cuda.is_available()
        self.reader = Reader(lang_list=['en'], gpu=gpu)

    def read(self, captcha_image: bytes):
        result = self.reader.readtext(captcha_image)
        return result[0][1]


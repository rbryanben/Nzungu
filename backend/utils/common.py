import hashlib
import PIL
import io
from rembg import remove

def hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def resizeAndRemoveBackground(image : bytes, toImageHeight = 120) -> PIL.Image:
    img = PIL.Image.open(image)
    w,h =  img.size
    scale = toImageHeight / h
    img = img.resize((int(w * scale),toImageHeight))
    img = remove(img)
    return img
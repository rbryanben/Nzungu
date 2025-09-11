import hashlib
import PIL
import io
from rembg import remove

def hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def resizeAndRemoveBackground(image : bytes, toImageHeight = 512) -> PIL.Image:
    img = PIL.Image.open(image)
    w,h =  img.size
    scale = toImageHeight / h
    img = img.resize((int(w * scale),toImageHeight))
    img = remove(img)
    return img

def mask_id(id_str: str) -> str:
    """
    Masks the given ID by keeping the first 3 and last 2 characters visible,
    and replacing the rest with '*'.
    """
    if len(id_str) <= 5:
        return "*" * len(id_str)  # if too short, mask everything
    
    return id_str[:3] + "*" * (len(id_str) - 5) + id_str[-2:]
from System.Drawing import Bitmap, Size
from System import Convert
from System.IO import MemoryStream

if base64_imgstr:
    b64_bytearray = Convert.FromBase64String(base64_imgstr)
    stream = MemoryStream(b64_bytearray)
    bitmap = Bitmap(stream)

    if not scale:
        scale = 1.0
    size = Size(bitmap.Width * scale, bitmap.Height * scale)
    bitmap = Bitmap(bitmap, size)

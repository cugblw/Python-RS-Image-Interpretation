from PIL.PngImagePlugin import PngImageFile, PngInfo

img_path = "E:/Coding/Python/Python-RS-Image-Interpretation/14_12223_7048.png"


targetImage = PngImageFile(img_path)

metadata = PngInfo()
metadata.add_text("tile", "A string")
metadata.add_text("resolution", str(1234))

targetImage.save("NewPath.png", pnginfo=metadata)
targetImage = PngImageFile("NewPath.png")

print(targetImage.text)
from PIL import Image
import os
os.makedirs("assets/images", exist_ok=True)
logo = Image.open("assets/images/logo.jpg").convert("RGB")
for s in (192, 512):
    logo.resize((s, s), Image.LANCZOS).save(f"assets/images/icon-{s}.png", "PNG", optimize=True)
logo.resize((180, 180), Image.LANCZOS).save("assets/images/apple-touch-icon.png", "PNG", optimize=True)
logo.save("assets/images/logo-opt.jpg", "JPEG", quality=86, optimize=True, progressive=True)
print(sorted(os.listdir("assets/images")))

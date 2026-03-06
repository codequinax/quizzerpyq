import os

# Folder containing images
folder = r"static/pyq/1st_year/Soft_skills/unit_5"

files = os.listdir(folder)

# Keep only image files
images = [f for f in files if f.endswith((".png", ".jpg", ".jpeg"))]

images.sort()

for i, file in enumerate(images, start=1):
    old_path = os.path.join(folder, file)
    new_name = f"{i}.png"
    new_path = os.path.join(folder, new_name)

    os.rename(old_path, new_path)

print("✅ Images renamed successfully")
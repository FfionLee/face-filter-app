import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_all_fun_assets():
    os.makedirs('static/filters', exist_ok=True)

    # ---------------- 1. DOG ASSETS (Left Ear, Right Ear, Nose/Muzzle) ----------------
    ear_w, ear_h = 240, 320
    ear_img = Image.new('RGBA', (ear_w, ear_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ear_img)
    outer_poly = [(60, 20), (180, 10), (230, 120), (200, 290), (120, 315), (50, 260), (20, 140)]
    draw.polygon(outer_poly, fill=(160, 95, 45, 255))
    inner_poly = [(80, 50), (160, 45), (195, 125), (170, 250), (115, 270), (70, 220), (50, 140)]
    draw.polygon(inner_poly, fill=(235, 160, 150, 255))
    ear_img.save('static/filters/dog_ear_left.png')
    ear_right = ear_img.transpose(Image.FLIP_LEFT_RIGHT)
    ear_right.save('static/filters/dog_ear_right.png')

    nose_w, nose_h = 300, 240
    nose_img = Image.new('RGBA', (nose_w, nose_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(nose_img)
    draw.ellipse([30, 70, 170, 200], fill=(245, 225, 195, 240))
    draw.ellipse([130, 70, 270, 200], fill=(245, 225, 195, 240))
    for dx, dy in [(70, 130), (95, 120), (80, 155), (205, 120), (230, 130), (220, 155)]:
        draw.ellipse([dx-4, dy-4, dx+4, dy+4], fill=(120, 75, 40, 200))
    draw.polygon([(100, 75), (200, 75), (215, 100), (160, 145), (150, 148), (140, 145), (85, 100)], fill=(30, 25, 25, 255))
    draw.ellipse([90, 70, 210, 110], fill=(35, 30, 30, 255))
    draw.ellipse([115, 78, 145, 92], fill=(240, 240, 250, 190))
    tongue_poly = [(125, 175), (175, 175), (170, 230), (150, 245), (130, 230)]
    draw.polygon(tongue_poly, fill=(245, 105, 130, 255))
    draw.ellipse([125, 210, 175, 245], fill=(245, 105, 130, 255))
    draw.line([(150, 175), (150, 230)], fill=(200, 70, 95, 255), width=3)
    nose_img.save('static/filters/dog_nose.png')

    # ---------------- 2. THUG LIFE / PIXEL SHADES ----------------
    shades_w, shades_h = 420, 120
    shades_img = Image.new('RGBA', (shades_w, shades_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shades_img)
    # Bridge
    draw.rectangle([170, 42, 250, 56], fill=(10, 10, 10, 255))
    # Left Lens (pixelated stepped blocks)
    draw.rectangle([30, 30, 185, 90], fill=(15, 15, 15, 255))
    draw.rectangle([45, 90, 170, 105], fill=(15, 15, 15, 255))
    # Right Lens
    draw.rectangle([235, 30, 390, 90], fill=(15, 15, 15, 255))
    draw.rectangle([250, 90, 375, 105], fill=(15, 15, 15, 255))
    # White pixel glares
    for lx in [60, 90, 120]:
        draw.rectangle([lx, 42, lx+18, 54], fill=(255, 255, 255, 230))
    for rx in [265, 295, 325]:
        draw.rectangle([rx, 42, rx+18, 54], fill=(255, 255, 255, 230))
    shades_img.save('static/filters/pixel_shades.png')

    # ---------------- 3. GOLD CROWN ----------------
    crown_w, crown_h = 360, 200
    crown_img = Image.new('RGBA', (crown_w, crown_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(crown_img)
    # Crown base band
    draw.rectangle([40, 140, 320, 185], fill=(255, 215, 0, 255))
    draw.rectangle([40, 170, 320, 185], fill=(218, 165, 32, 255))
    # Crown spikes
    points = [
        (40, 140),
        (40, 50),
        (90, 105),
        (180, 20),
        (270, 105),
        (320, 50),
        (320, 140)
    ]
    draw.polygon(points, fill=(255, 215, 0, 255))
    # Jewels / Rubies / Emeralds
    draw.ellipse([160, 95, 200, 135], fill=(230, 30, 60, 255))  # Central ruby
    draw.ellipse([75, 125, 105, 155], fill=(30, 200, 240, 255))  # Left sapphire
    draw.ellipse([255, 125, 285, 155], fill=(50, 220, 90, 255))  # Right emerald
    # Golden balls on tips
    draw.ellipse([28, 38, 52, 62], fill=(255, 240, 150, 255))
    draw.ellipse([166, 8, 194, 36], fill=(255, 240, 150, 255))
    draw.ellipse([308, 38, 332, 62], fill=(255, 240, 150, 255))
    crown_img.save('static/filters/crown.png')

    # ---------------- 4. ANIME CAT EARS + BLUSH ----------------
    # Cat Ear Left
    cat_w, cat_h = 200, 200
    cat_left = Image.new('RGBA', (cat_w, cat_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(cat_left)
    draw.polygon([(20, 180), (100, 20), (180, 180)], fill=(40, 40, 40, 255))
    draw.polygon([(50, 170), (100, 60), (150, 170)], fill=(255, 150, 180, 255))
    # Soft inner fluff
    draw.polygon([(70, 160), (100, 90), (130, 160)], fill=(255, 220, 235, 255))
    cat_left.save('static/filters/cat_ear_left.png')
    cat_right = cat_left.transpose(Image.FLIP_LEFT_RIGHT)
    cat_right.save('static/filters/cat_ear_right.png')

    # Anime Cheek Blush
    blush_w, blush_h = 160, 90
    blush_img = Image.new('RGBA', (blush_w, blush_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(blush_img)
    draw.ellipse([10, 15, 150, 75], fill=(255, 105, 150, 130))
    # Cute diagonal anime stripes
    for sx in [45, 75, 105]:
        draw.line([(sx, 25), (sx + 20, 65)], fill=(255, 40, 100, 180), width=4)
    blush_img.save('static/filters/anime_blush.png')

    # ---------------- 5. DEVIL HORNS ----------------
    horn_w, horn_h = 140, 180
    horn_left = Image.new('RGBA', (horn_w, horn_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(horn_left)
    # Curved sharp red horn
    poly_horn = [(30, 170), (15, 120), (45, 50), (115, 15), (95, 75), (85, 130), (75, 170)]
    draw.polygon(poly_horn, fill=(225, 25, 45, 255))
    # Highlight shine
    draw.line([(45, 115), (70, 65), (105, 28)], fill=(255, 120, 140, 230), width=4)
    horn_left.save('static/filters/devil_horn_left.png')
    horn_right = horn_left.transpose(Image.FLIP_LEFT_RIGHT)
    horn_right.save('static/filters/devil_horn_right.png')

    print("All fun teenage aesthetic assets generated successfully!")

if __name__ == '__main__':
    generate_all_fun_assets()

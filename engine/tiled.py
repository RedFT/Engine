import engine as en
import os
import json


def load_tiles(tmx_filename, scale):
    tmx_path = os.path.join(en.get_resources_directory(), tmx_filename)
    with open(tmx_path, 'r') as f:
        tmx = json.load(f)

    image_filename = tmx["tilesets"][0]["image"]
    tileset = en.graphics.load_image(image_filename)

    tilemap = tmx['tilesets'][0]
    rects = [None]
    for i in range(tilemap['tilecount']):
        row = i // (tilemap['imagewidth']//tilemap['tilewidth'])
        col = i % (tilemap['imagewidth']//tilemap['tilewidth'])

        tx = tilemap['margin'] + col * (tilemap['tilewidth'] + tilemap['spacing'])
        ty = tilemap['margin'] + row * (tilemap['tileheight'] + tilemap['spacing'])

        tx *= scale
        ty *= scale

        rects.append((tx, ty,
            scale * tilemap['tilewidth'],
            scale * tilemap['tileheight']))

    tiles = {
        'image': tileset,
        'data': tmx['layers'][0]['data'],
        'height': tmx['layers'][0]['height'],
        'width': tmx['layers'][0]['width'],
        'rects': rects
    }
    return tiles

"""
Graphics library. 
"""

import ctypes
import atexit
import platform
import os

# path of shared library
os_name = platform.system().lower()
machine_name = platform.machine().lower()
libfile = os.path.join(os.path.dirname(__file__), "bin", ("basic_lib_%s_%s.so" % (os_name, machine_name)))

gfx = ctypes.CDLL(str(libfile))

# Called on normal exit() from Python code so that we don't raise exception in GFX thread on shutdown
def deinitialize():
    gfx.off()

gfx.on()
atexit.register(deinitialize)

def scr(mode):
    """Sets video mode.

    Args:
        mode (int): Desired graphics mode.

        Mode    Screen Res
        0       240 x 135
        1       480 x 270
        2       960 x 540
        3       1920 x 1080
    """
    gfx.video(mode)


def get_scr_w():
    """Returns screen width.

    Returns:
        int: Screen width in pixels.
    """
    return gfx.get_screen_w()


def get_scr_h():
    """Returns screen height.

    Returns:
        int: Screen height in pixels.
    """
    return gfx.get_screen_h()


def camera(x, y):
    """Sets camera X, Y position.

    Camera position is subtracted from every graphic object on the screen. Therefore
    moving camera to the right for N pixels will move all objects to the right for N pixels.
    Similarly, moving camera for M pixels up will move all objects for M pixels down.

    Args:
        x (int): camera X position
        y (int): camera Y position
    """
    gfx.camera(x, y)


def get_camera_x():
    """Returns camera X position."""
    return gfx.get_camera_x()


def get_camera_y():
    """Returns camera Y position."""
    return gfx.get_camera_y()


def tileset(image_path, col_count, row_count):
    """Loads tile set from image file.

    Tileset is collection of rectangular images, or tiles. Images in tileset can be used as sprite animation frames or
    background (map) tiles. 

    Args:
        image_path (string): Image file path.
        col_count (int): Number of tile columns.
        row_count (int): Number of tile rows.

    Returns:
        int: tileset_id - number which can be used to reference this tileset
    """
    return gfx.load_tileset(str.encode(image_path), col_count, row_count)


def rm_tileset(tileset_id):
    """Removes tileset from the memory."""
    return gfx.load_tileset(str.encode(image_path), col_count, row_count)


def spr(sprite_id):
    """Creates new sprite.

    Args:
        sprite_id (int): Id of tileset that defines the sprite graphics

    Returns:
        int: sprite_id - number which can be used to reference this sprite.
    """
    return gfx.spr(sprite_id)

def rm_spr(sprite_id):
    """Removes sprite from the memory.

    Args:
        sprite_id (int): Id of sprite that should be removed.
    """
    return gfx.rm_spr(sprite_id)


def spr_tile(sprite_id, tile_offset):
    """Sets sprite tile.

    Each tile has unique offset in the tileset. Tile in top left corner of the tileset gets offset 0.
    Then offset is increased incrementaly from left to right and from top to bottom.

    Example for 4x4 tileset:
    +----+----+----+----+
    |  0 |  1 |  2 |  3 |
    +----+----+----+----+
    |  4 |  5 |  6 |  7 |
    +----+----+----+----+
    |  8 |  9 | 10 | 11 |
    +----+----+----+----+
    | 12 | 13 | 14 | 15 |
    +----+----+----+----+

    Args:
        sprite_id (int): id of the sprite.
        tile_offset (int): Offset of the tile that the sprite should use.
    """
    gfx.spr_tile(sprite_id, tile_offset)


def spr_layer(sprite_id, layer):
    """Sets layer of the sprite.

    Objects wil lower layer number are drawn on top of objects with higher layer number.

    Args:
        sprite_id (id): Sprite id.
        layer (int): Layer that sprite should be assigned to.
    """
    gfx.spr_layer(sprite_id, layer)


def spr_xy(sprite_id, x, y):
    """Sets sprite position on the screen.

    Args:
        sprite_id (int): Sprite id.
        x (int): Sprite X position.
        y (int): Sprite Y position.
    """
    gfx.spr_xy(sprite_id, x, y)


def spr_visible(sprite_id, visible):
    """Set sprite visibility.

    Args:
        sprite_id (int): Sprite id.
        visible (bool): True if sprite is visibile, False if sprite is invisible
    """
    gfx.spr_visible(sprite_id, visible)


def get_spr_tile(sprite_id):
    """Returns sprite tile offset."""
    return gfx.get_spr_tile(sprite_id)


def get_spr_layer(sprite_id):
    """Returns sprite layer."""
    return gfx.get_spr_layer(sprite_id)


def get_spr_x(sprite_id):
    """Returns sprite X position."""
    return gfx.get_spr_x(sprite_id)


def get_spr_y(sprite_id):
    """Returns sprite Y position."""
    return gfx.get_spr_y(sprite_id)


def get_spr_visible(sprite_id):
    """Returns True if sprite is visible and False if it's not."""
    return gfx.get_spr_visible(sprite_id)


def map(tileset_id, col_count, row_count):
    """Creates new tile map.

    Tile map is usually used to represent tiled background (game playing area). This is a grid in which each cell 
    is filled by one tile image.

    Args:
        tileset_id (int): Id of the tileset which will be used to draw this map.
        col_count (int): Horizontal size of the grid (number of columns).
        row_count (int): Vertical size of the grid (number of rows).

    Returns:
        int: Id which will be used to reference this map.
    """
    return gfx.map(tileset_id, col_count, row_count)


def rm_map(map_id):
    """Removes map from the memory.

    Args:
        map_id (int): Id of the map that should be removed.
    """
    gfx.rm_map(map_id)


def map_layer(map_id, layer):
    """Sets layer of the map.

    Objects wil lower layer number are drawn on top of objects with higher layer number.

    Args:
        map_id (int): Map id.
        layer (int): Layer which the map should use.
    """
    gfx.map_layer(map_id, layer)


def map_tile(map_id, col, row, tile_offset):
    """Set tile image for one map cell.

    Example of cell coordinates (col, row) for 4x4 map:
    +-----+-----+-----+-----+
    | 0,0 | 1,0 | 2,0 | 3,0 |
    +-----+-----+-----+-----+
    | 0,1 | 1,1 | 2,1 | 3,1 |
    +-----+-----+-----+-----+
    | 0,2 | 1,2 | 2,2 | 3,2 |
    +-----+-----+-----+-----+
    | 0,3 | 1,3 | 2,3 | 3,3 |
    +-----+-----+-----+-----+

    Args:
        map_id (int): Map id.
        col (int): Cell horizontal position (column index).
        row (int): Cell vertical position (row index).
        tile_offset (int): Offset of the tile in the tileset.
    """
    gfx.map_tile(map_id, col, row, tile_offset)


def map_visible(map_id, visible):
    """Set map visiility.

    Args:
        map_id (int): Id of the map.
        visible (Bool): True if map should be visible and False if it should be invisible.
    """
    gfx.map_visible(map_id, visible)


def get_map_rows(map_id):
    """Get map row count.

    Args:
        map_id (int): Map id.

    Returns:
        int: row count
    """
    return gfx.get_map_rows(map_id)


def get_map_rows(map_id):
    """Get map column count.

    Args:
        map_id (int): Map id.

    Returns:
        int: column count
    """
    return gfx.get_map_cols(map_id)


def get_map_layer(map_id):
    """Get map layer.

    Args:
        map_id (int): Map id.

    Returns:
        int: layer
    """
    return gfx.get_map_layer(map_id)


def get_map_tile(map_id, col, row):
    """Get tile offset on specific position in the map.

    Args:
        map_id (int): Map id.
        col (int): Column index.
        row (int): Row index.

    Returns:
        int: Offset of the tile on (col,row) position.
    """
    return gfx.get_map_tile(map_id, col, row)


def get_map_visible(map_id):
    """Get map visibility.

    Args:
        map_id (int): Map id.

    Returns:
        bool: True if map is visible and False if it's not.
    """


def next_frame():
    """Vaits for the next frame."""
    gfx.next_frame()


def screenshot(path):
    """Takes screenshot and saves it into the image file.

    Args:
        path (string): Image file path.
    """


SPEC = 256
str2key = {
    "F1" : SPEC + 0,
    "F2" : SPEC + 1,
    "F3" : SPEC + 2,
    "F4" : SPEC + 3,
    "F5" : SPEC + 4,
    "F6" : SPEC + 5,
    "F7" : SPEC + 6,
    "F8" : SPEC + 7,
    "F9" : SPEC + 8,
    "F10" : SPEC + 9,
    "F11" : SPEC + 10,
    "F12" : SPEC + 11,
    "LEFT" : SPEC + 12,
    "UP" : SPEC + 13,
    "RIGHT" : SPEC + 14,
    "DOWN" : SPEC + 15,
    "PAGE_UP" : SPEC + 16,
    "PAGE_DOWN" : SPEC + 17,
    "HOME" : SPEC + 18,
    "END" : SPEC + 19,
    "INSERT" : SPEC + 20
}


def key(key_):
    """Checks if the key is pressed.

    Args:
        key_ (string): String with character that we want to check. For example: "a". 
        Besides single characters user can pass names of special keys:
            - F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12
            - LEFT, UP, RIGHT, DOWN
            - PAGE_UP, PAGE_DOWN
            - HOME, END, INSERT

    Returns:
        bool: True if the key is pressed, False if it's not pressed.
    """
    if len(key_) == 1:
        return gfx.key(ord(key_))
    else:
        return gfx.key(str2key[key_])

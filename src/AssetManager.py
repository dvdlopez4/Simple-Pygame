from pygame import image, transform, mixer
from Util.constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASSET_FILE_PATH


class AssetManager(object):
    def __init__(self):
        self.assets = {}

        # Background images
        rawImage = image.load(
            f'{ASSET_FILE_PATH}/background/game_background_4.png').convert()
        self.assets["NATURE_BACKGROUND_IMAGE"] = transform.scale(
            rawImage, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Sprites
        self.assets["BASIC_ENEMY_SPRITE"] = image.load(
            f'{ASSET_FILE_PATH}sprites/enemy.png').convert_alpha()
        self.assets["PLAYER_ADVENTURER_SPRITE"] = image.load(
            f"{ASSET_FILE_PATH}/sprites/adventurer-Sheet.png").convert_alpha()

        # Sound files
        self.assets["PLAYER_JUMP_SOUNDS"] = [
            mixer.Sound(f"{ASSET_FILE_PATH}/sound/Jump2_01.wav"),
            mixer.Sound(f"{ASSET_FILE_PATH}/sound/Jump_01.wav")
        ]
        self.assets["PLAYER_SWORD_ATTACK_SOUND"] = mixer.Sound(
            f"{ASSET_FILE_PATH}/sound/Sword_01.wav")

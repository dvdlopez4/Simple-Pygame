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


class SoundManager(object):
    mixer.pre_init(44100, -16, 1, 64)
    mixer.init()
    sounds = {
        "PLAYER_JUMP_SOUND_1": mixer.Sound(f"{ASSET_FILE_PATH}/sound/Jump2_01.wav"),
        "PLAYER_JUMP_SOUND_2": mixer.Sound(f"{ASSET_FILE_PATH}/sound/Jump_01.wav"),
        "PLAYER_SWORD_ATTACK_SOUND": mixer.Sound(f"{ASSET_FILE_PATH}/sound/Sword_01.wav"),
        "ENEMY_SOUND_1": mixer.Sound(f'{ASSET_FILE_PATH}/sound/Enemy1.wav'),
        "ENEMY_SOUND_2": mixer.Sound(f'{ASSET_FILE_PATH}/sound/Enemy2.wav'),
        "ENEMY_SOUND_3": mixer.Sound(f'{ASSET_FILE_PATH}/sound/Enemy3.wav'),
        "ENEMY_SOUND_4": mixer.Sound(f'{ASSET_FILE_PATH}/sound/Enemy4.wav')
    }

    @staticmethod
    def play_sound(sound_key: str):
        if sound_key not in SoundManager.sounds:
            return

        SoundManager.sounds[sound_key].play()

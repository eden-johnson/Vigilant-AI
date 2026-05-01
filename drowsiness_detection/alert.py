import pygame
import threading

class AlertSystem:
    def __init__(self, sound_path=None):
        pygame.mixer.init()
        self.sound_path = sound_path
        self.is_playing = False

        if sound_path:
            try:
                self.sound = pygame.mixer.Sound(sound_path)
            except:
                self.sound = None
                print("[ALERT] Sound file not found. Using beep fallback.")
        else:
            self.sound = None

    def trigger(self, reason="DROWSINESS DETECTED"):
        """Play alert sound + print warning."""
        print(f"[!!!] ALERT: {reason}")
        if self.sound and not self.is_playing:
            self._play_async()

    def _play_async(self):
        def play():
            self.is_playing = True
            self.sound.play()
            pygame.time.wait(int(self.sound.get_length() * 1000))
            self.is_playing = False
        thread = threading.Thread(target=play, daemon=True)
        thread.start()

    def stop(self):
        if self.sound:
            self.sound.stop()
        self.is_playing = False

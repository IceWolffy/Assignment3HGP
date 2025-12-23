from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import os

class MusicManager:
    def __init__(self):
        self.audio_output = QAudioOutput()
        self.music_player = QMediaPlayer()
        self.music_player.setAudioOutput(self.audio_output)
        
        # Load the music file
        music_path = os.path.join(os.path.dirname(__file__), "assets", "music", "totallyOriginalOST.mp3")
        self.music_player.setSource(QUrl.fromLocalFile(music_path))
        
        # Connect the mediaStatusChanged signal to loop the music
        self.music_player.mediaStatusChanged.connect(self.loop_music)
        
        # Set volume (0.0 to 1.0)
        self.audio_output.setVolume(0.5)
    
    def play(self):
        """Start playing the music"""
        self.music_player.play()
    
    def loop_music(self, status):
        """When the music ends, restart it"""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.music_player.setPosition(0)
            self.music_player.play()
    
    def get_player(self):
        """Return the music player instance"""
        return self.music_player
    
    def get_audio_output(self):
        """Return the audio output instance"""
        return self.audio_output

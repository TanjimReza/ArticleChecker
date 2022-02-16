from pydub import AudioSegment
from pydub.playback import play
sound1 = AudioSegment.from_mp3("1.mp3")
sound2 = AudioSegment.from_mp3("2.mp3")
sound3 = sound1+sound2
# sound3.export("/3.mp3", format="mp3")
play(sound3)
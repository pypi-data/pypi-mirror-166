from pytube import YouTube
class Yukla():
    def __init__(self, video_manzili: str, sifati: str):
        self.video_manzili = video_manzili
        self.sifati = sifati
        try:
            video = YouTube(self.video_manzili)
            if self.sifati.upper() == "H":
                print("[*] Yuklanmoqda...")
                video.streams.get_highest_resolution().download()
                print(f"[***]  Video muvaffaqiyatli yuklandi!")
            elif self.sifati.upper() == "L":
                print("[*] Yuklanmoqda...")
                video.streams.get_lowest_resolution().download()
                print(f"[***]  Video muvaffaqiyatli yuklandi!")
            elif self.sifati.upper() == "M":
                print("[*] Yuklanmoqda...")
                video.streams.get_audio_only().download()
                print(f"[***]  Audio muvaffaqiyatli yuklandi!")
        except Exception as ex:
            print(ex)
            return None
from ChatstatTikTokApi import ChatstatTikTokApi

with ChatstatTikTokApi() as api:
    sound = api.sound(id="7016547803243022337")

    for video in sound.videos():
        print(video.id)

from ChatstatTikTokApi import ChatstatTikTokApi

with ChatstatTikTokApi() as api:
    for video in api.trending.videos():
        print(video.id)

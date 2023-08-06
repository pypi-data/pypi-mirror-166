from ChatstatTikTokApi import ChatstatTikTokApi

with ChatstatTikTokApi() as api:
    tag = api.hashtag(name="funny")

    print(tag.info())

    for video in tag.videos():
        print(video.id)

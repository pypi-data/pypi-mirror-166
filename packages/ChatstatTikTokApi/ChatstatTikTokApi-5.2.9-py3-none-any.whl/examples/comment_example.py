from ChatstatTikTokApi import ChatstatTikTokApi

with ChatstatTikTokApi() as api:
    tiktok_video_id = 7107272719166901550
    video = api.video(id=tiktok_video_id)

    for comment in video.comments():
        print(comment.text)

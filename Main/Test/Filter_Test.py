from datetime import datetime

# Sample data
data = [
    {
        'kind': 'youtube#searchResult',
        'etag': 'xEIuy2p91bdWMSEsxzlZkcWpd48',
        'id': {'kind': 'youtube#video', 'videoId': 'q55Re22XuEw'},
        'snippet': {
            'publishedAt': '2024-03-29T08:00:23Z',
            'channelId': 'UCBcm-pxUmI5CUnhZSMGbvWQ',
            'title': '(SUB) 오늘도 즐겁게 쓰레기집 청소하러 가볼까 ~♪ | 클린어벤져스',
            'description': '쓰레기집 #니코틴 #클린어벤져스 #특수청소 #cleanavengers #헬프미 #청년 #청소업체 #봉사 청소업체 창업을 도와드립니다 ...',
            'thumbnails': {
                'default': {'url': 'https://i.ytimg.com/vi/q55Re22XuEw/default.jpg', 'width': 120, 'height': 90},
                'medium': {'url': 'https://i.ytimg.com/vi/q55Re22XuEw/mqdefault.jpg', 'width': 320, 'height': 180},
                'high': {'url': 'https://i.ytimg.com/vi/q55Re22XuEw/hqdefault.jpg', 'width': 480, 'height': 360},
            },
            'channelTitle': '클린어벤져스cleanavengers',
            'liveBroadcastContent': 'none',
            'publishTime': '2024-03-29T08:00:23Z'
        }
    },
    {
        'kind': 'youtube#searchResult',
        'etag': '_-7-ahUWUkWaOMcesnSZjEnGgZ0',
        'id': {'kind': 'youtube#video', 'videoId': 'vQm5JbVeQ7A'},
        'snippet': {
            'publishedAt': '2024-04-03T10:15:00Z',  # This date is for testing; it will be considered as "today" in our code
            'channelId': 'UCBcm-pxUmI5CUnhZSMGbvWQ',
            'title': 'Another Video',
            'description': 'Another description',
            'thumbnails': {
                'default': {'url': 'https://i.ytimg.com/vi/vQm5JbVeQ7A/default.jpg', 'width': 120, 'height': 90},
                'medium': {'url': 'https://i.ytimg.com/vi/vQm5JbVeQ7A/mqdefault.jpg', 'width': 320, 'height': 180},
                'high': {'url': 'https://i.ytimg.com/vi/vQm5JbVeQ7A/hqdefault.jpg', 'width': 480, 'height': 360},
            },
            'channelTitle': 'Some Channel',
            'liveBroadcastContent': 'none',
            'publishTime': '2024-04-03T10:15:00Z'
        }
    }
]

# Filter function
def filter_videos_by_date_and_channel(videos, channel_id, date):
    return [
        video for video in videos
        if video['snippet']['channelId'] == channel_id and
           datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').date() == date
    ]

# Setting today's date for filtering
today_date = datetime.now().date()

# Filter videos
filtered_videos = filter_videos_by_date_and_channel(data, 'UCBcm-pxUmI5CUnhZSMGbvWQ', today_date)

filtered_videos
from src.channel import Channel


class Video:

    def __init__(self, video_id):
        self.video_id: str = video_id
        video_info = Channel.get_service().videos().list(part='snippet,statistics', id=self.video_id).execute()
        try:
            self.title: str = video_info['items'][0]['snippet']['title']
        except IndexError:
            self.title: str = None
            self.video_url: str = None
            self.view_count: int = None
            self.like_count: int = None
        else:
            self.video_url: str = 'https://www.youtube.com/watch?v=' + self.video_id
            self.view_count: int = int(video_info['items'][0]['statistics']['viewCount'])
            self.like_count: int = int(video_info['items'][0]['statistics']['likeCount'])

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

import datetime

import isodate

from src.channel import Channel


class PlayList:

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.playlist_info = Channel.get_service().playlists().list(id=self.__playlist_id,
                                                                    part='snippet',
                                                                    ).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    def get_videos_info_from_playlist(self):
        videos = Channel.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        videos_ids: list[str] = [video['contentDetails']['videoId'] for video in videos['items']]
        return Channel.get_service().videos().list(part='contentDetails,statistics',
                                                   id=','.join(videos_ids)
                                                   ).execute()

    @property
    def total_duration(self):
        duration = datetime.timedelta()
        videos = self.get_videos_info_from_playlist()
        for video in videos['items']:
            duration += isodate.parse_duration(video['contentDetails']['duration'])
        return duration

    def show_best_video(self):
        videos = self.get_videos_info_from_playlist()
        max_like = 0
        best_video_url = ''
        for video in videos['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_like:
                max_like = like_count
                best_video_url = 'https://youtu.be/' + video['id']
        return best_video_url
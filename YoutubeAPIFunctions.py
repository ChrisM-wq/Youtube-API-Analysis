def get_channel_stats(youtube, channel_ids):

    """
    Get channel stats
    
    Params:
    -------
    youtube: build object for Youtube API
    channel_ids: list of channel IDs
    
    Returns:
    -------
    A dataframe with all channel stats for each input in the list of channels
    
    """
    
    all_data = []

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)
    )

    response = request.execute()
    for item in response['items']:
        data = {'channelName' : item['snippet']['title'],
                'subscribers' : item['statistics']['subscriberCount'],
                'views' : item['statistics']['viewCount'],
                'totalvideos' : item['statistics']['videoCount'],
                'playlistId' : item['contentDetails']['relatedPlaylists']['uploads']
        }
        all_data.append(data)

    return (pd.DataFrame(all_data))

def get_video_ids(youtube, playlist_id):
    
    """
    Get video IDs
    
    Params:
    -------
    youtube: build object for Youtube API
    channel_ids: list of playlist IDs
    
    Returns:
    -------
    A list of video IDs
    
    """
    
    video_ids = []

    request = youtube.playlistItems().list(
        part = "snippet, contentDetails",
        playlistId = playlist_id,
        maxResults = 50
    )
    response = request.execute()

    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part = "snippet, contentDetails",
            playlistId = playlist_id,
            maxResults = 50,
            pageToken = next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('next_page_token')

    return video_ids

def get_video_details(youtube, video_ids):
    
    """
    Get video details
    
    Params:
    -------
    youtube: build object for Youtube API
    channel_ids: list of video IDs
    
    Returns:
    -------
    A dataframe with all the video stats
    
    """
    
    all_video_info = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for video in response['items']:
            stats_to_keep = {'snippet' : ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                            'statistics' : ['viewCount', 'likeCount', 'favoriteCount', 'commentCount'],
                            'contentDetails' : ['duration', 'definition', 'caption']
                            }
            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None
            
            all_video_info.append(video_info)

    return pd.DataFrame(all_video_info)
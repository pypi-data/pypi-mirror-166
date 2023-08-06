import requests
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


def query_streamer_page_for_vods(streamer_name: str) -> requests:
    uri = 'https://gql.twitch.tv/gql'
    query = 'query{user(login:"' \
            + streamer_name + '"){videos(first:50,after:"") { edges { node { title, id, lengthSeconds, ' \
                              'previewThumbnailURL(height: 180, width: 320), createdAt, viewCount }, cursor }, ' \
                              'pageInfo { hasNextPage, hasPreviousPage }, totalCount }}}'
    try:
        header = {'Client-ID': config['vod_getter_parameters']['twitch_downloader_client_id']}
    except TypeError as TE:
        raise Exception('Invalid config file') from TE

    response = requests.post(uri, json={'query': query}, headers=header)
    if response.status_code != 200:
        raise ConnectionError(f"Unexpected status code returned: {response.status_code}, streamer name in the query "
                              f"was {streamer_name}. It may be invalid")

    return response

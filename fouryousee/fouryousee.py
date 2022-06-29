import json
import time
from typing import List, Any
from pathlib import Path
import requests
from decouple import config

from fouryousee.resources.tools import validate_kwargs_single_media_category, validate_kwargs_player, \
    validate_kwargs_report, brief_player, validate_kwargs_playlist, validate_kwargs_single_media, \
    myme_type, brief_playlist, brief_media


class FouryouseeAPI(object):
    """
    Class allow the communication with the 4YouSee Manager API REST.
    """
    url = 'https://api.4yousee.com.br/v1/'

    def __init__(self, token, name=None, account=None, account_type=None):
        self.name = name
        self.token = token
        self.account = account
        self.account_type = account_type
        self.users = None
        self.user_groups = None
        self.uploads = None
        self.medias = None
        self.media_category = None
        self.players = None
        self.playlists = None
        self.templates = None
        self.news = None
        self.newsources = None
        self.videowall = None
        self.reports = None
        self.playlogs = None
        self.secs_between_call = config('SECS', default=1)

    def get_all(self, resource, spec_id: int = False, **kwargs):
        all_registers = []
        count = 0
        number_page, limit = 1, 1
        while number_page <= limit:
            url = '{base_url}{resource}{end_str}' \
                .format(base_url=FouryouseeAPI.url,
                        resource=resource,
                        end_str=(lambda x: f'/{x}' if x else f'?page={number_page}')(spec_id))
            headers = {
                'Secret-Token': self.token,
                'Content-Type': 'application/json'
            }
            time.sleep(int(self.secs_between_call))
            response = requests.request("GET", url, headers=headers,
                                        params=kwargs)
            if not response.ok:
                raise Exception(response.text)
            data = json.loads(response.text)
            if not data.get('totalPages'):
                if data.get('results') == []:
                    return []
                elif data.get('results'):
                    return data['results']
                else:
                    return data
            limit = data.get('totalPages', 1)
            for item in data.get('results'):
                all_registers.append(item)
                count += 1
                # print(count, medias)
            number_page += 1
        return all_registers

    def get_users(self) -> List[dict]:
        """
        Get the users of the 4YouSee account.
        @return: List of dicts, where every dict, depicts a user.
        """
        self.users = self.get_all('users')
        return self.users

    def get_users_groups(self) -> List[dict]:
        """
        Get the users group of the 4YouSee account.
        @return: List of dicts, where every dict, depicts a users group.
        """
        self.users_groups = self.get_all('users/groups')
        return self.users_groups

    def get_uploads(self, **kwargs) -> List or dict:
        """
        Get the uploads of the 4YouSee account.
        @param kwargs: Dict with the id of a single upload.
        @return: List of dicts, where every dict, depicts a previous upload.
                 If there is not uploads, will return a empty list.
                 If there is an upload with the id, will return a dict.
                 If the upload was not found it'll return an empty list.
        """
        if kwargs:
            if spec_id := kwargs.get('id', False):
                self.uploads = self.get_all('uploads')
                return list(filter(lambda x: x['id'] == spec_id, self.uploads))
            else:
                raise Exception('This function only accepts the id field')
        else:
            self.uploads = self.get_all('uploads')
        return self.uploads

    def get_medias(self, **kwargs) -> List[dict] or dict or Exception:
        """
        Get the medias of the 4YouSee account.
        @param kwargs: dict with the query params. They could be:
        - id: (int, optional) - One and only id of a media
        - name: (str, optional) - Full or part name
        - categoryId: (int, optional) - ID media category.
                    It's not allowed to send a list of categories id
        - metadata: (bool, optional) - set to true to retrieve
                        media metadata (poster, thumbnail, meta-description)
        @return: List of dicts, where every dict depicts a media.
                 If there is an media with the id, will return a dict.
                 If the media was not found it'll raise an exception.

        """
        if kwargs:
            if spec_id := kwargs.get('id', False):
                del kwargs['id']
                return self.get_all('medias/{}'.format(spec_id), **kwargs)
            else:
                return self.get_all('medias', **kwargs)
        else:
            self.medias = self.get_all('medias')
        return self.medias

    def get_media_category(self, **kwargs) -> List[dict] or dict or Exception:
        """
        Get the media categories of the 4YouSee account.
        @param kwargs: Dict with the id of a single category.
        @return: List of dicts, where every dict depicts a media category.
                If there is not media category, will return a empty list
                If there is an category with the id, will return a dict.
                If the category was not found it'll raise an exception.
        """
        if kwargs:
            if spec_id := kwargs.get('id', False):
                del kwargs['id']
                return self.get_all('medias/categories/{}'.format(spec_id))
            else:
                raise Exception('This function only accepts the id field')
        else:
            self.media_category = self.get_all('medias/categories')
        return self.media_category

    def get_players(self, **kwargs) -> List[dict] or dict or Exception:
        """
        Get the players of the 4YouSee account.
        @param kwargs: Dict with the id of a single player.
        @return: List of dicts, where every dict depicts a player.
                 If there is no players, will return a empty list.
                 If there is an player with the id, will return a dict.
                 If the player was not found it'll raise an exception.
        """
        if kwargs:
            if spec_id := kwargs.get('id', False):
                del kwargs['id']
                return self.get_all('players/{}'.format(spec_id))
            else:
                raise Exception('This function only accepts the id field')
        else:
            self.players = self.get_all('players')
        return self.players

    def get_playlists(self, **kwargs) -> List[dict] or dict or Exception:
        """
        Get the playlists of the 4YouSee account.
        @param kwargs: Dict with the id of a single playlist.
        @return: List of dicts, where every dict depicts a playlist.
                 If there is no playlists, will return a empty list.
                 If there is an playlist with the id, will return a dict.
                 If the playlist was not found it'll raise an exception.
        """
        if kwargs:
            if spec_id := kwargs.get('id', False):
                del kwargs['id']
                return self.get_all('playlists/{}'.format(spec_id))
            else:
                raise Exception('This function only accepts the id field')
        else:
            self.playlists = self.get_all('playlists')
        return self.playlists

    def get_templates(self, **kwargs) -> list or dict:
        """
        Get the templates of the 4YouSee account.
        @param kwargs: Dict with the id of a single playlist.
        @return: List of dicts, where every dict, depicts a template.
                 If there is no templates, will return a empty list.
                 If there is an template with the id, will return a dict.
                 If the template was not found it'll return an empty list.
        """
        if kwargs:
            if spec_id := kwargs.get('id', False):
                self.templates = self.get_all('templates')
                return list(filter(lambda x: x['id'] == spec_id, self.templates))
            else:
                raise Exception('This function only accepts the id field')
        else:
            self.templates = self.get_all('templates')
        return self.templates

    def get_newsources(self, **kwargs) -> List:
        """
        Get the newsources (Rss Feeds) of the 4YouSee account.
        @param kwargs: dict with the query params. They could be:
        - id: (int optional) - Id of the newsource.
                Ex.: 31
        - name: (str optional) - Newsource name to search. Ex.: weather
        - template: (int optional) - Template id to search. Ex.: 4
        - insertContentAutomatically: (bool optional) - 0 if search only
                automatic content and 1 for manual. Ex.: 1
        @return: List of dicts, where every dict depicts a newsource.
                 If there is an newsource with the id, will return a
                 list with one dict.
                 If there is no newsources, will return a empty list.
        """
        if kwargs:
            return self.get_all('newsources', **kwargs)
        self.newsources = self.get_all('newsources')
        return self.newsources

    def get_news(self, **kwargs) -> List[dict]:
        """
        Get the medias of the 4YouSee account.
        @param kwargs: dict with the query params. They could be:
        - id: (int optional) -  Id of the specific new.
        - newsourceId: (int optional) - One Newsource id. Example: 34
        - startDate: (str optional) - Start date of the news.
                     Ex.: '2017-03-01' or '2019-09-30 16:33:00'
        - endDate: (str optional) - End date of the news.
                   Ex.: '2019-03-22'  or '2022-06-25 18:33:00'
        - content: (str optional) - Content of the news to search. This
                   is only allowed for news that has variables. A newsource
                   has variables when his content key is a dict and not a str.
                   Ex.: {"product": "Juice"}
        - status: (str optional) - Status of the news. The possible values
                  are: approved, disapproved or, waiting.
                   Ex.: 'waiting'
        @return: List of dicts, where dict depicts a news.
                 If there is no news, will return a empty list.
                 If there is an news with the id, will return a dict.
        """
        if kwargs:
            if spec_id := kwargs.get('id', False):
                del kwargs['id']
                return self.get_all('news/{}'.format(spec_id))
            else:
                self.news = self.get_all('news', **kwargs)
        else:
            self.news = self.get_all('news')
        return self.news

    def get_reports(self, **kwargs) -> List[dict]:
        """
        Get the requested reports of the 4YouSee account.
        @param kwargs: Dict with the id of a single report.
        @return: List of dicts, where dict depicts a requested report.
                 If there is no reports already requested, will
                 return a empty list.
                 If there is an report with the id, will return a dict.
        """
        if kwargs:
            if spec_id := kwargs.get('id', False):
                del kwargs['id']
                return self.get_all('reports/{}'.format(spec_id))
            else:
                raise Exception('This function only accepts the id field')
        else:
            self.reports = self.get_all('reports')
        return self.reports

    def post(self, resource: str, header_type: str = 'application/json',
             files=None, payload=None):
        url = '{base_url}{resource}'.format(
            base_url=FouryouseeAPI.url,
            resource=resource
        )
        headers = {
            'Content-Type': header_type,
            'Secret-Token': self.token
        }
        time.sleep(int(self.secs_between_call))
        response = requests.post(url, headers=headers,
                                 data=payload, files=files)
        if not response.ok:
            raise Exception(response.text)
        # print(json.dumps(data, indent=2))
        return json.loads(response.text)

    def upload_files(self, files: str or list) -> List[dict]:
        """
        Upload a file on the 4YouSee account.
        @param files: str or list: Path of the file(s) locally.
        @return: List of dicts if the file was uploaded.
        Ex.:-> [
                {'id': '1abe4b9dadde1cbc7e3cb6518bca0e0f',
                'filename': 'PIZZA.mp4'},
                ]
            -> Empty list if the file was not uploaded.
        """
        if not files:
            raise Exception('Missing \'files\' field.')
        if isinstance(files, str):
            files = files.split(',')
        if isinstance(files, (list, tuple)):
            payload = {
                'Content-Type':
                    'multipart/form-data;'
            }

            result, multiple_files = [], []
            for file in files:
                file = Path(file)
                if not file.exists():
                    raise Exception(f'File {file} not found.')
                multiple_files.append(
                    (
                        'media',
                        (file.name, open(file, 'rb'),
                         myme_type(file))
                    )
                )
            for file in multiple_files:
                result.append(self.post(resource='uploads', header_type=None,
                                        files=[file], payload=payload)
                              )
            return result

    def post_single_media(self, **kwargs) -> dict:
        """
        Create a new media in the 4yousee account library.
        Obs.: Is not allowed post a html files through the API.
        @param kwargs: dict with the query params. They could be:
        - name (str, optional): Name of the media in the account.
        - file (dict, required) - Upload resource: dict returned from
            upload_files function. Ex:
             {
                "id": "dce17a1a5949768a82dd8bedd2ee525d",
                "filename": "video.mp4"
              }
        - duration (int, required) - duration of Media: used only by html
            or images files.
        - categories (list of ints): List of categories id which this
            media will be associated. If is not given, the function will
            choose one.
            Ex: [1, 2, 3, 4, 5] or '1, 2, 3, 4, 5'
        - schedule (dict, required) - scheduling information.
            Ex:
                {
                "startDate": "2019-01-01",
                "endDate": "2019-12-31",
                "times": [
                            {
                                "startTime": "08:00",
                                "endTime": "11:00",
                                "weekDays": [ 1, 2, 3, 4, 5 ]
                            }
                        ]
            }
        @return: dict that depicts the uploaded media. Ex.:
                {
                    "id": 120,
                    "name": "BURGUER",
                    "file": "https://4usee.com/nameaccount-token
                            /nameaccount/common/videos/i_120.mp4",
                    "duration": 19,
                    "schedule": {
                        "times": []
                        },
                    "categories": [ 1 ]
                 }
        """

        # Validators
        validate_kwargs_single_media(**kwargs)

        file = Path(kwargs.get('file'))
        kwargs['name'] = kwargs.get('name', file.stem)

        # Figure out the category to associate to the media
        categories = kwargs.get('categories')
        if isinstance(categories, str):
            categories = list(map(int, categories.split(',')))
        elif isinstance(categories, int):
            categories = [categories]
        kwargs['categories'] = categories

        file_uploaded = self.upload_files(str(file))
        if file_uploaded:
            kwargs['file'] = file_uploaded[0]
            payload = json.dumps(kwargs, indent=2)
            return self.post(resource='medias', payload=payload)

    def post_media_category(self, **kwargs) -> dict:
        """
        Create a new category in the 4yousee account library.
        :param kwargs: dict with the query params. They could be:
        - name (str, required) Category/subcategory display name
        - description (str) - Detailed category description
        - parent (int) - When informed it creates a subcategory
        - shuffle (int, optional) - True to scramble the order of
                                        contents on the carousel.
        - updateflow (int, optional) - 1: to restart carousel after
                        carousel update; 2: Do not restart after carousel update.
        :return: dict that depicts the media category created.
               Ex: (If it's just passed the name.)
                    {
                      "id": 29,
                      "name": "sample category",
                      "description": null,
                      "parent": null,
                      "children": [],
                      "carouselThumbnail": null,
                      "autoShuffle": false,
                      "updateFlow": "1",
                      "sequence": null
                    }
        """
        # Validators
        validate_kwargs_single_media_category(**kwargs)
        payload = json.dumps(kwargs, indent=2)
        return self.post('medias/categories/', payload=payload)

    def post_player(self, **kwargs) -> dict:
        """
        Create a new player in the 4yousee account.
        :param kwargs: dict with the query params. They could be:
        - name (str, required) player display name.
        - description (str, optional) - Detailed player description.
        - platform (str, required) - Platform where the 4yousee player will
                   be executed:
                   Ex.: 4YOUSEE_PLAYER ou SAMSUNG ou ANDROID ou LG
        - group (int, optional) - Id of a group of players.
        - playlists (dict, required) - 7 keys where every one depicts
                    the number of the they where sunday is 0, and 7
                    values where every one depicts the id of the playlist
                    that the player will play that day.
                        Ex.:
                          {
                            "0": 1,
                            "1": 1,
                            "2": 1,
                            "3": 1,
                            "4": 1,
                            "5": 1,
                            "6": 1
                          }
        - audios (dict, optional) - A dict with "0" as his only key and
                    a value that depicts the id of the audio playlists.
                    Ex.:
                      "audios": {
                                "0": 1
                              }
        :return: dict that depicts the player created.
               Ex: {
                      "id": 6,
                      "name": "Player name example",
                      "description": "Player description example",
                      "platform": "4YOUSEE_PLAYER",
                      "lastContactInMinutes": null,
                      "group": {
                        "id": 1,
                        "name": "Group DEMO"
                      },
                      "playerStatus": {
                        "id": 6,
                        "name": "Never accessed",
                        "time": 0
                      },
                      "playlists": {
                        "0": {
                          "id": 1,
                          "name": "Playlist DEMO"
                        },
                        "1": {
                          "id": 1,
                          "name": "Playlist DEMO"
                        },
                        "2": {
                          "id": 1,
                          "name": "Playlist DEMO"
                        },
                        "3": {
                          "id": 1,
                          "name": "Playlist DEMO"
                        },
                        "4": {
                          "id": 1,
                          "name": "Playlist DEMO"
                        },
                        "5": {
                          "id": 1,
                          "name": "Playlist DEMO"
                        },
                        "6": {
                          "id": 1,
                          "name": "Playlist DEMO"
                        }
                      },
                      "audios": {
                        "0": {
                          "id": 1,
                          "name": "Playlist DEMO"
                        }
                      }
                    }
        """
        # Validators
        validate_kwargs_player(**kwargs)

        if len(kwargs.get('name')) > 50:
            kwargs['name'] = kwargs['name'][:46] + '...'

        kwargs['group'] = kwargs.get('group', 1)

        payload = json.dumps(kwargs, indent=2)
        return self.post('players/', payload=payload)

    def post_playlists(self, **kwargs) -> dict:
        """
        Create a new playlist in the 4yousee account.
        :param kwargs: dict with the query params. They could be:
        - name (str, required) playlist display name.
        - isSubPlaylist (bool, optional) - Default value is False.
        - category (int, optional) - Id of category of playlists.
        - items (list of dicts, required) - Platform where the 4yousee player will
                Ex.:
                    [
                        {
                            "type": "layout",
                            "id": 1
                        },
                        {
                            "type": "videowall",
                            "abortIfError": false,
                            "ignoreLayout": false,
                            "grid": [
                                [
                                    {
                                        "type": "media",
                                        "id": 4
                                    },
                                    {
                                        "type": "media",
                                        "id": 1
                                    }
                                ],
                                [
                                    {
                                        "type": "media",
                                        "id": 2
                                    },
                                    {
                                        "type": "media",
                                        "id": 4
                                    }
                                ]
                            ]
                        },
                        {
                            "type": "media",
                            "id": 5
                        },
                        {
                            "type": "news"
                        }
                    ]
        - sequence (list, required) - Sequence of execution of the items.
                    Ex.: [
                            0,
                            1,
                            2,
                            3
                        ]
        :return: dict that depicts the playlist created.
               Ex: {
                      "id": 40,
                      "name": "Playlist Created via API",
                      "durationInSeconds": 46,
                      "isSubPlaylist": false,
                      "category": null,
                      "items": [
                        {
                          "type": "layout",
                          "id": 1,
                          "name": "Grid 1920x1080 com 1 área",
                          "width": 1920,
                          "height": 1080
                        },
                        {
                          "type": "videoWall",
                          "abortIfError": false,
                          "ignoreLayout": false,
                          "grid": [
                            [
                              {
                                "id": 4,
                                "name": "4YouSee Analyse",
                                "file": "i_4.mp4",
                                "durationInSeconds": 10,
                                "contentSchedule": {
                                  "startDate": "2021-02-01"
                                }
                              },
                              {
                                "id": 1,
                                "name": "4YouSee Play",
                                "file": "i_1.mp4",
                                "durationInSeconds": 10,
                                "contentSchedule": {
                                  "times": [
                                    {
                                      "startTime": "11:00",
                                      "endTime": "19:00",
                                      "weekDays": [
                                        0,
                                        1,
                                        2,
                                        3,
                                        4,
                                        5,
                                        6
                                      ]
                                    }
                                  ]
                                }
                              }
                            ],
                            [
                              {
                                "id": 2,
                                "name": "4YouSee Manage",
                                "file": "i_2.mp4",
                                "durationInSeconds": 10,
                                "contentSchedule": {
                                  "startDate": "2021-02-02",
                                  "endDate": "2021-06-05",
                                  "times": [
                                    {
                                      "startTime": "05:00",
                                      "endTime": "21:00",
                                      "weekDays": [
                                        0,
                                        2,
                                        3,
                                        4,
                                        6
                                      ]
                                    }
                                  ]
                                }
                              },
                              {
                                "id": 4,
                                "name": "4YouSee Analyse",
                                "file": "i_4.mp4",
                                "durationInSeconds": 10,
                                "contentSchedule": {
                                  "startDate": "2021-02-01"
                                }
                              }
                            ]
                          ]
                        },
                        {
                          "type": "media",
                          "id": 5,
                          "name": "Walking",
                          "file": "i_5.mp4",
                          "durationInSeconds": 26,
                          "contentSchedule": {
                            "times": [
                              {
                                "startTime": "00:00",
                                "endTime": "23:59",
                                "weekDays": [
                                  0,
                                  2,
                                  4,
                                  6
                                ]
                              }
                            ]
                          }
                        },
                        {
                          "type": "news",
                          "durationInSeconds": 10
                        }
                      ],
                      "sequence": [
                        0,
                        1,
                        2,
                        3
                      ]
                    }
        """
        # Validators
        validate_kwargs_playlist(**kwargs)

        if len(kwargs.get('name')) > 50:
            kwargs['name'] = kwargs['name'][:46] + '...'

        payload = json.dumps(kwargs, indent=2)
        return self.post('playlists/', payload=payload)

    def post_reports(self, **kwargs) -> dict:
        """
         Create a new request of report in the 4yousee account.
         Once is received the response, through the id will be possible
         to consult if the report is ready.
        :param kwargs: dict with the query params. They could be:
        - type (str, required). Default value is 'detailed'
        - webhook (str, optional) - Web service that may allow the response
                    of the 4yousee servers. THis response will
                    have the result of report.
                    Ex.: 'http://4fc8e5ddf059.ngrok.io'
        - filter: (dict, required) - Interval of time of the desired report.
                    Ex.:
                        {
                            "startDate": "2020-07-26",
                            "startTime": "00:00:00",
                            "endDate": "2020-08-24",
                            "endTime": "23:59:59",
                            "mediaId": [ ],  # List of id medias.
                            "playerId": [ ],  # List of id players.
                            "sort": -1
                            }
        - sort (int, optional) - Default values is -1.
        :return: dict that depicts the playlist created.
               {
                   "id":521356,
                   "type":"detailed",
                   "format":"json",
                   "filter":{
                      "startDate":"2020-07-26",
                      "startTime":"00:00:00",
                      "endDate":"2020-08-24",
                      "endTime":"23:59:59",
                      "mediaId":[],
                      "playerId":[ 2 ],
                      "sort":-1
                   },
                   "status":"waiting",
                   "url":"None",
                   "createdAt":"2022-06-24T21:42:05+00:00",
                   "updatedAt":"2022-06-24T21:42:05+00:00"
                }
        """
        # Validators
        validate_kwargs_report(**kwargs)

        kwargs['filter']['sort'] = kwargs.get('filter').get('sort', -1)
        kwargs['type'] = kwargs.get('type', 'detailed')

        payload = json.dumps(kwargs, indent=2)
        return self.post('reports/', payload=payload)

    def delete(self, resource: str, spec_id: int or str):
        url = '{base_url}{resource}/{spec_id}'.format(
            base_url=FouryouseeAPI.url,
            resource=resource,
            spec_id=spec_id
        )
        headers = {
            'Content-Type': 'application/json',
            'Secret-Token': self.token
        }
        time.sleep(int(self.secs_between_call))
        response = requests.delete(url, headers=headers)
        if not response.ok:
            raise Exception(response.text)
        else:
            return True

    def delete_upload(self, spec_id: str = None) -> bool:
        """
        Delete one upload of the 4YouSee account.
        @param spec_id: int: Id of a single upload.
        @return: True: bool: in case the upload was deleted successfully
        """
        if not spec_id:
            raise Exception('Missing id of the upload.')

        try:
            if self.get_uploads(id=spec_id):
                return self.delete('uploads', spec_id)
        except Exception:
            raise Exception(f'Upload with ID {spec_id} was not found')

    def delete_media(self, spec_id: int = None) -> bool:
        """
        Delete one media of the 4YouSee account.
        @param spec_id: int: Id of a single media.
        @return: True: bool: in case the media was deleted successfully
        """
        if not spec_id:
            raise Exception('Missing id of the media.')

        try:
            if self.get_medias(id=spec_id):
                return self.delete('medias', spec_id)
        except Exception:
            raise Exception(f'Media with ID {spec_id} was not found')

    def delete_player(self, spec_id: int = None) -> bool:
        """
        Delete one player of the 4YouSee account.
        @param spec_id: int: Id of a single player.
        @return: True: bool: in case the player was deleted successfully
        """
        if not spec_id:
            raise Exception('Missing id of the player.')

        try:
            if self.get_players(id=spec_id):
                return self.delete('players', spec_id)
        except Exception:
            raise Exception(f'Player with ID {spec_id} was not found')

    def delete_playlist(self, spec_id: int = None) -> bool:
        """
        Delete one playlist of the 4YouSee account.
        @param spec_id: int: Id of a single playlist.
        @return: True: bool: in case the playlist was deleted successfully
        """
        if not spec_id:
            raise Exception('Missing id of the player.')

        try:
            if self.get_playlists(id=spec_id):
                return self.delete('playlists', spec_id)
        except Exception:
            raise Exception(f'Playlist with ID {spec_id} was not found')

    def edit(self, resource: str, payload=None):
        url = '{base_url}{resource}'.format(
            base_url=FouryouseeAPI.url,
            resource=resource
        )
        headers = {
            'Content-Type': 'application/json',
            'Secret-Token': self.token
        }
        time.sleep(int(self.secs_between_call))
        response = requests.put(url, headers=headers,
                                data=payload)
        if not response.ok:
            raise Exception(response.text)
        # print(json.dumps(data, indent=2))
        return json.loads(response.text)

    def edit_media(self, **kwargs):
        """
        Update an existing media.
        :param kwargs: Same dict that when a player is posted
        - name (str, optional)
        - file (dict, optional) - use only for update file media.
                To update Media file you need to create a Upload
                resource first.
                Ex:
                 {
                    "id": "dce17a1a5949768a82dd8bedd2ee525d",
                    "filename": "video.mp4"
                  }
        - duration (int, optional) - duration of Media, used only
                by zip or images files.
        - categories (list, optional) - list of categories which
                this Media is gonna be associated.
        - schedule (dict, optional) - scheduling information
                Ex.:
                    {
                    "startDate": "2019-01-01",
                    "endDate": "2019-12-31",
                    "times": [
                                {
                                    "startTime": "08:00",
                                    "endTime": "11:00",
                                    "weekDays": [
                                                  1,
                                                  2,
                                                  3,
                                                  4,
                                                  5
                                                ]
                                }
                            ]
                }
        :return: dict that depicts the modified media.
                Ex.:
                {
                  "id": 230,
                  "name": "sample-mp4-file",
                  "file": "https://4usee.com/123456/nameaccount/common/videos/i_230.mp4",
                  "duration": 126,
                  "schedule": {
                    "startDate": null,
                    "endDate": null,
                    "times": []
                  },
                  "categories": [ 22, 23, 24, 25, 26, 27, 31 ]
                }
        """
        if not kwargs:
            raise Exception('Missing Fields')

        spec_id = kwargs.get('id', False)
        if not spec_id:
            raise Exception('Missing ID of the media field.')

        media = self.get_medias(id=spec_id)
        mdia = brief_media(media)

        kwargs['name'] = kwargs.get('name', mdia['name'])
        kwargs['duration'] = kwargs.get('duration', mdia['duration'])
        kwargs['categories'] = kwargs.get('categories', mdia['categories'])
        kwargs['schedule'] = kwargs.get('schedule', mdia['schedule'])

        del kwargs['id']
        payload = json.dumps(kwargs, indent=2)
        return self.edit('medias/{}/'.format(spec_id), payload=payload)

    def edit_category(self, **kwargs):
        """
        It is possible update name, description and/or parent of category.
        :param kwargs: dict with the query params. They could be:
        - name (str, optional) Category/subcategory display name
        - description (str, optional) - Detailed category description
        - parent (int, optional) - When present it convert category
                in subcategory of category informed parent. If the value is
                null, it  converts the subcategory into a first level category.
        :return: dict that depicts the modified media.
                Ex.:
                    {
                      "id": 70,
                      "name": "sample media category",
                      "description": null,
                      "parent": {
                        "id": 1,
                        "name": "DEMO",
                        "description": "",
                        "carouselThumbnail": null,
                        "autoShuffle": false,
                        "updateFlow": "1"
                      },
                      "children": [],
                      "carouselThumbnail": null,
                      "autoShuffle": false,
                      "updateFlow": "1",
                      "sequence": []
                    }
        """
        if not kwargs:
            raise Exception('Missing Fields')

        spec_id = kwargs.get('id', False)
        if not spec_id:
            raise Exception('Missing ID of the category field.')

        del kwargs['id']
        payload = json.dumps(kwargs, indent=2)
        return self.edit('medias/categories/{}'.format(spec_id), payload=payload)

    def edit_multiple_categories(self, *args):
        """
        Update bulk category.
        It is possible to update name, description, parent and sequence for
        multiple categories.
        :param args: list of dicts with every dict could have:
        - name (str, optional) Category display name.
        - description (str, optional) - Detailed category description.
        - parent (int or null, optional) - When present it convert category
            in subcategory of category informed parent. If the value is null,
            it converts the subcategory into a first level category.
        - sequence (list[int], optional) - This array must contain all content
            ids associated to each category in each item. The order of these
            ids in the array is the order they will appear in the carousel.
        Ex.: [
                {
                  "id": 1,
                  "name": "Category #1",
                  "description": "Description for category 1",
                  "parent": 2,
                  "sequence": [ 4, 2, 1, 3 ]
                },
                {
                  "id": 2,
                  "name": "Category #2",
                  "description": "Description for category 2",
                  "sequence": [ 4, 1, 2 ]
                }
             ]
        :return:
            Ex.:
            {
              "carouselItems": [
                                {
                                  "id": 44,
                                  "name": "sample media categoryDEL",
                                  "description": null,
                                  "parent": {
                                    "id": 1,
                                    "name": "DEMO",
                                    "description": "",
                                    "carouselThumbnail": null,
                                    "autoShuffle": false,
                                    "updateFlow": "1"
                                  },
                                  "children": [],
                                  "carouselThumbnail": null,
                                  "autoShuffle": false,
                                  "updateFlow": "1",
                                  "sequence": []
                                },
                                {
                                  "id": 46,
                                  "name": "sample media category DEL",
                                  "description": null,
                                  "parent": {
                                    "id": 1,
                                    "name": "DEMO",
                                    "description": "",
                                    "carouselThumbnail": null,
                                    "autoShuffle": false,
                                    "updateFlow": "1"
                                  },
                                  "children": [],
                                  "carouselThumbnail": null,
                                  "autoShuffle": false,
                                  "updateFlow": "1",
                                  "sequence": []
                                }
                            ]
            }
        """
        if not args:
            raise Exception('Missing Fields')

        for i in args:
            if not isinstance(i, dict):
                raise Exception(f'Invalid dict {i}')

        payload = json.dumps({'carouselItems': args}, indent=2)
        return self.edit('medias/categories/bulk', payload=payload)

    def edit_player(self, **kwargs):
        """
        Update a Player by id.
        When a param is not sent, it will recognize the current values
        of the ayer in the 4yousee account.
        :param kwargs: Same dict that when a player is posted :
        - id (int, required) - Id o the player
        - name (str, optional) - player display name.
        - description (str, optional) - Detailed player description.
        - platform (str, optional) - Platform where the 4yousee player will
                   be executed:
                   Ex.: 4YOUSEE_PLAYER ou SAMSUNG ou ANDROID ou LG
        - group (int, optional) - Id of a group of players.
        - playlists (dict, optional) - 7 keys where every one depicts
                    the number of the they where sunday is 0, and 7
                    values where every one depicts the id of the playlist
                    that the player will play that day.
                        Ex.:
                          {
                            "0": 1,
                            "1": 1,
                            "2": 1,
                            "3": 1,
                            "4": 1,
                            "5": 1,
                            "6": 1
                          }
        - audios (dict, optional) - A dict with "0" as his only key and
                    a value that depicts the id of the audio playlists.
                    Ex.:
                      "audios": {
                                "0": 1
                              }
        Ex.:
            {
              "name": "Player Android",
              "description": "Player Android",
              "group": 1,
              "platform": "ANDROID",
              "playlists": {
                "0": 3,
                "1": 3,
                "2": 3,
                "3": 3,
                "4": 3,
                "5": 3,
                "6": 3
              },
              "audios": {
                "0": 1
              }
            }
        :return:
        """

        # Validators
        spec_id = kwargs.get('id', False)
        if not spec_id:
            raise Exception('Missing ID of the player field.')
        validate_kwargs_player(**kwargs)

        player_existent = self.get_players(id=spec_id)
        plyer = brief_player(player_existent)

        kwargs['name'] = kwargs.get('name', plyer['name'])
        kwargs['description'] = kwargs.get('description', plyer['description'])
        kwargs['group'] = kwargs.get('group', plyer['group'])
        kwargs['platform'] = kwargs.get('platform', plyer['platform'])
        kwargs['playlists'] = kwargs.get('playlists', plyer['playlists'])
        kwargs['audios'] = kwargs.get('audios', plyer['audios'])

        if len(kwargs.get('name')) > 50:
            kwargs['name'] = kwargs['name'][:46] + '...'

        del kwargs['id']
        payload = json.dumps(kwargs, indent=2)
        return self.edit('players/{}'.format(spec_id), payload=payload)

    def edit_playlist(self, **kwargs):
        """
        Update a Playlist by id.
        :param kwargs: Same dict that when a playlist is posted:
        - name (str, required) playlist display name.
        - isSubPlaylist (bool, optional) - Default value is False.
        - category (int, optional) - Id of category of playlists.
        - items (list of dicts, required) - Platform where the 4yousee player will
                Ex.:
                    [
                        {
                            "type": "layout",
                            "id": 1
                        },
                        {
                            "type": "videowall",
                            "abortIfError": false,
                            "ignoreLayout": false,
                            "grid": [
                                       [
                                            { "type": "media", "id": 4 },
                                            { "type": "media", "id": 1 }
                                        ],
                                        [
                                            { "type": "media", "id": 2 },
                                            { "type": "media", "id": 4 }
                                        ]
                                    ]
                        },
                        { "type": "media", "id": 5 },
                        { "type": "news" }
                    ]
        - sequence (list, required) - Sequence of execution of the items.
                    Ex.: [ 0, 1, 2, 3 ]
        :return: dict that depicts the playlist modified.
               Ex: {
                      "id": 40,
                      "name": "Playlist Created via API",
                      "durationInSeconds": 46,
                      "isSubPlaylist": false,
                      "category": null,
                      "items": [
                        {
                          "type": "layout",
                          "id": 1,
                          "name": "Grid 1920x1080 com 1 área",
                          "width": 1920,
                          "height": 1080
                        },
                        {
                          "type": "videoWall",
                          "abortIfError": false,
                          "ignoreLayout": false,
                          "grid": [
                            [
                              {
                                "id": 4,
                                "name": "4YouSee Analyse",
                                "file": "i_4.mp4",
                                "durationInSeconds": 10,
                                "contentSchedule": {
                                  "startDate": "2021-02-01"
                                }
                              },
                              {
                                "id": 1,
                                "name": "4YouSee Play",
                                "file": "i_1.mp4",
                                "durationInSeconds": 10,
                                "contentSchedule": {
                                  "times": [
                                    {
                                      "startTime": "11:00",
                                      "endTime": "19:00",
                                      "weekDays": [
                                        0,
                                        1,
                                        2,
                                        3,
                                        4,
                                        5,
                                        6
                                      ]
                                    }
                                  ]
                                }
                              }
                            ],
                            [
                              {
                                "id": 2,
                                "name": "4YouSee Manage",
                                "file": "i_2.mp4",
                                "durationInSeconds": 10,
                                "contentSchedule": {
                                  "startDate": "2021-02-02",
                                  "endDate": "2021-06-05",
                                  "times": [
                                    {
                                      "startTime": "05:00",
                                      "endTime": "21:00",
                                      "weekDays": [
                                        0,
                                        2,
                                        3,
                                        4,
                                        6
                                      ]
                                    }
                                  ]
                                }
                              },
                              {
                                "id": 4,
                                "name": "4YouSee Analyse",
                                "file": "i_4.mp4",
                                "durationInSeconds": 10,
                                "contentSchedule": {
                                  "startDate": "2021-02-01"
                                }
                              }
                            ]
                          ]
                        },
                        {
                          "type": "media",
                          "id": 5,
                          "name": "Walking",
                          "file": "i_5.mp4",
                          "durationInSeconds": 26,
                          "contentSchedule": {
                            "times": [
                              {
                                "startTime": "00:00",
                                "endTime": "23:59",
                                "weekDays": [
                                  0,
                                  2,
                                  4,
                                  6
                                ]
                              }
                            ]
                          }
                        },
                        {
                          "type": "news",
                          "durationInSeconds": 10
                        }
                      ],
                      "sequence": [
                        0,
                        1,
                        2,
                        3
                      ]
                    }
        """

        # Validators
        spec_id = kwargs.get('id', False)
        if not spec_id:
            raise Exception('Missing ID of the playlist field.')
        validate_kwargs_playlist(**kwargs)

        playlist_existent = self.get_playlists(id=spec_id)
        plist = brief_playlist(playlist_existent)

        kwargs['name'] = kwargs.get('name', plist['name'])
        kwargs['isSubPlaylist'] = kwargs.get('isSubPlaylist', plist['isSubPlaylist'])
        kwargs['category'] = kwargs.get('category', plist['category'])
        kwargs['items'] = kwargs.get('items', plist['items'])
        kwargs['sequence'] = kwargs.get('sequence', plist['sequence'])

        if len(kwargs.get('name')) > 40:
            kwargs['name'] = kwargs['name'][:36] + '...'

        del kwargs['id']
        payload = json.dumps(kwargs, indent=2)
        return self.edit('playlists/{}'.format(spec_id), payload=payload)

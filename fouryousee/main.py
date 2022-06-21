import json
import time
from typing import List
from pathlib import Path
import requests

from fouryousee.resources.tools import filter_id, myme_type


class DataManager:
    """
    Class allow the comunication with the 4YouSee Manager API REST.
    """
    url = 'https://api.4yousee.com.br/v1/'

    def __init__(self, token, name=None, account=None, type=None):
        self.name = name
        self.token = token
        self.account = account
        self.type = type
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

    def get_all(self, resource, spec_id: int = False, **kwargs):
        allResources = []
        count = 0
        number_page, limit = 1, 1
        while number_page <= limit:
            url = '{base_url}{resource}{end_str}' \
                .format(base_url=DataManager.url,
                        resource=resource,
                        end_str=(lambda x: f'/{x}' if x else f'?page={number_page}')(spec_id))
            headers = {
                'Secret-Token': self.token,
                'Content-Type': 'application/json'
            }
            time.sleep(1)
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
                allResources.append(item)
                count += 1
                # print(count, medias)
            number_page += 1
        return allResources

    def get_users(self) -> List[dict]:
        """
        Get the users of the 4YouSee account.
        @param kwargs: dict with the query params. They could be:
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

    def get_uploads(self, upload_id: int = False) -> List[dict]:
        """
        Get the uploads of the 4YouSee account.
        @param upload_id: int. Id of and upload that exists.
        @return: List of dicts, where every dict, depicts a previous upload.
                 If there is not uploads, will return a empty list
        """
        if upload_id:
            if not self.uploads:
                self.uploads = self.get_all('uploads')
            if result := list(
                    filter(lambda x: x['id'] == upload_id, self.uploads)):
                return result[0]
            else:
                return []
        else:
            self.uploads = self.get_all('uploads')
        return self.uploads

    def get_medias(self, **kwargs) -> List[dict]:
        """
        Get the medias of the 4YouSee account.
        @param kwargs: dict with the query params. They could be:
        - id: (int, optional) -
        - name: (str, optional) - Full or part name
        - categoryId: (int, optional) - ID media category.
                    It's not allowed to send a list of categories id
        - metadata: (bool, optional) - set to true to retrieve
                        media metadata (poster, thumbnail, meta-description)
        @return: List of dicts, where every dict depicts a media.
                 If there is not medias, will return a empty list
        """
        if kwargs:
            if spec_id := kwargs.get('id', False):
                del kwargs['id']
                return self.get_all('medias', spec_id, **kwargs)
            else:
                return self.get_all('medias', **kwargs)
        else:
            self.medias = self.get_all('medias')
        return self.medias

    def get_media_category(self, media_category_id: int = None) -> List[dict]:
        """
        Get the media categories of the 4YouSee account.
        @param media_category_id: int: Id of a single category.
        @return: List of dicts, where every dict depicts a media category.
                If there is not media category, will return a empty list
        """
        if media_category_id:
            return self.get_all('medias/categories', media_category_id)
        self.media_category = self.get_all('medias/categories')
        return self.media_category

    def get_players(self, player_id: int = None) -> List[dict]:
        """
        Get the players of the 4YouSee account.
        @param player_id: int: Id of a single player.
        @return: List of dicts, where every dict depicts a player.
                 If there is no players, will return a empty list
        """
        if player_id:
            return self.get_all('players', player_id)
        self.players = self.get_all('players')
        return self.players

    def get_playlists(self, playlist_id: int = None) -> List[dict]:
        """
        Get the playlists of the 4YouSee account.
        @param playlist_id: int: Id of a single playlist.
        @return: List of dicts, where every dict depicts a playlist.
                 If there is no playlists, will return a empty list
        """
        if playlist_id:
            return self.get_all('playlists', playlist_id)
        self.playlists = self.get_all('playlists')
        return self.playlists

    def get_templates(self, template_id: int = None) -> Exception:
        """
        Get the newsources of the 4YouSee account.
        @param template_id: int: Id of a single template.
        @return: List of dicts, where every dict, depicts a template.
                 If there is no templates, will return a empty list
        """
        if template_id:
            if not self.templates:
                self.templates = self.get_all('templates')
            if result := list(
                    filter(lambda x: x['id'] == template_id, self.templates)):
                return result[0]
            else:
                return Exception(
                    f'Template with ID {template_id} was not found')
        else:
            self.templates = self.get_all('templates')
        return self.templates

    def get_newsources(self, **kwargs) -> List[dict]:
        """
        Get the newsources of the 4YouSee account.
        @param kwargs: dict with the query params. They could be:
        - id: One or more comma-separated Newsources ids. Example: 1,2,3
        - name: Newsource name to search. Example: weather
        - template: Template id to search. Examle: 4
        - insertContentAutomatically: 1 if search only automatic content
                                      insertion or 0 for manual. Examples: 1
        @return: List of dicts, where every dict depicts a newsource.
                 If there is no newsources, will return a empty list
        """
        if kwargs:
            return self.get_all('newsources', **kwargs)
        self.newsources = self.get_all('newsources')
        return self.newsources

    def get_news(self, **kwargs) -> List[dict]:
        """
        Get the medias of the 4YouSee account.
        @param kwargs: dict with the query params. They could be:
        - newsourceId: int: One Newsource id. Example: 34
        - startDate: str: Start date of the news.
                     Example 2017-03-01 or '2019-09-30 16:33:00'
        - endDate: str: End date of the news.
                   Example: 2019-03-22  or '2022-06-25 18:33:00'
        - content: str: Content of the news to search.
                   Example {"product": "Juice"}
        - status: str: Status of the news. The possible values are: approved,
                disapproved, waiting. Examples: waiting
        @return: List of dicts, where dict depicts a news.
                 If there is no news, will return a empty list
        """
        if kwargs:
            return self.get_all('news', **kwargs)
        self.news = self.get_all('news')
        return self.news

    def get_reports(self, report_id: int = None) -> List[dict]:
        """
        Get the requested reports of the 4YouSee account.
        @param id: int: Id of a single report.
        @return: List of dicts, where dict depicts a requested report.
                 If there is no reports already requested, will
                 return a empty list
        """
        if report_id:
            return self.get_all('reports', report_id)
        self.reports = self.get_all('reports')
        return self.reports

    def post(self, resource: str, header_type: str = 'application/json',
             files: str = None, payload=None):
        url = '{base_url}{resource}'.format(
            base_url=DataManager.url,
            resource=resource
        )
        headers = {
            'Content-Type': header_type,
            'Secret-Token': self.token
        }
        time.sleep(1)
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
        @return: dict that depicts the uploaded media. Ex.:
                {
                    "id": 120,
                    "name": "BURGUER",
                    "file": "https://4usee.com/alfareiza-3385E2/alfareiza/common/videos/i_120.mp4",
                    "duration": 19,
                    "schedule": {
                        "times": []
                        },
                    "categories": [ 1 ]
                 }
        """

        # Validators
        if not kwargs.get('file'):
            raise Exception('Missing \'file\' field.')

        file = Path(kwargs.get('file'))
        if not file.exists():
            raise Exception('File not found.')

        mimetype = myme_type(file)
        type, extension = mimetype.split('/')

        if mimetype not in ['video/mp4',
                            'image/jpeg',
                            # 'image/gif',
                            'image/png',
                            'application/zip']:
            raise Exception('Invalid file.')

        if mimetype in ['image/jpeg', 'image/png', 'application/zip']:
            if not kwargs.get('duration'):
                raise Exception("Missing 'duration' field. This must "
                                "be an integer that depicts "
                                "the duration of the file in the playlist."
                                )
            elif not isinstance(kwargs.get('duration'), int):
                raise Exception('Invalid duration')

        kwargs['name'] = kwargs.get('name', file.stem)

        if kwargs.get('category'):
            raise Exception('Invalid param must be \'categories\'.')

        # Figure out the category to associate to the media
        if categories := kwargs.get('categories'):
            if isinstance(categories, str):
                categories = list(map(int, categories.split(',')))
            elif isinstance(categories, int):
                categories = [categories]

            kwargs['categories'] = categories

            for category_id in categories:
                if self.media_category:
                    kwargs['categories'] += filter_id(category_id,
                                                      self.media_category)
                elif self.get_media_category(media_category_id=category_id):
                    # If the category doesn't exist in the 4yousee account
                    # it will raise an exception
                    continue

        elif bool(self.get_media_category(media_category_id=1)):
            kwargs['categories'] = [1]
        else:
            self.get_media_category()
            kwargs['categories'] = self.media_category[0]['id']

        file_uploaded = self.upload_files(str(file))
        if file_uploaded:
            kwargs['file'] = file_uploaded[0]
            payload = json.dumps(kwargs, indent=2)
            return self.post(resource='medias', payload=payload)

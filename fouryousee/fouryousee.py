import json
import mimetypes
import time
from pathlib import Path
from typing import List

import requests


class FouryouseeAPI(object):
    """
    Class allow the communication with the 4YouSee Manager API REST.
    """

    url = "https://api.4yousee.com.br/v1/"

    def __init__(self, token, name=None, account=None, account_type=None):
        self.name = name
        self.token = token
        self.account = account
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

    def get_all(self, resource, spec_id: int = False, **kwargs):
        all_registers = []
        count = 0
        number_page, limit = 1, 1
        while number_page <= limit:
            url = "{base_url}{resource}{end_str}".format(
                base_url=FouryouseeAPI.url,
                resource=resource,
                end_str=(lambda x: f"/{x}" if x else f"?page={number_page}")(
                    spec_id
                ),
            )
            headers = {
                "Secret-Token": self.token,
                "Content-Type": "application/json",
            }
            time.sleep(1)
            response = requests.request(
                "GET", url, headers=headers, params=kwargs
            )
            if not response.ok:
                raise Exception(response.text)
            data = json.loads(response.text)
            if not data.get("totalPages"):
                if data.get("results") == []:
                    return []
                elif data.get("results"):
                    return data["results"]
                else:
                    return data
            limit = data.get("totalPages", 1)
            for item in data.get("results"):
                all_registers.append(item)
                count += 1

            number_page += 1

        return all_registers

    def get_users(self) -> List[dict]:
        """Get the users of the 4YouSee account.

        :return: List of dicts, where every dict, depicts a user.
        :rtype: list

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        >>> my.get_users()
        [{'id': 2, 'name': 'foo', 'username': 'foobar', 'email': 'foobar@gmail.com', 'group': {'id': 2, 'name': 'Administrador'}}]

        """
        self.users = self.get_all("users")
        return self.users

    def get_users_groups(self) -> List[dict]:
        """Get the users group of the 4YouSee account.

        :return: List of dicts, where every dict, depicts a users group.
        :rtype: list

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        >>> my.get_users_groups()
        [{'id': 2, 'name': 'Administrador', 'description': 'Administradores do 4YouSee Manager.'}]

        """
        self.users_groups = self.get_all("users/groups")
        return self.users_groups

    def get_uploads(self, **kwargs) -> List or dict:
        """Get the uploads of the 4YouSee account.

        :param id: Id of a single upload.
        :type id: str, optional
        :return: List of dicts, where every dict, depicts a upload.
        :rtype: list

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        Getting all the uploads categories. It will return all the uploads of your account.
        It will be a list of dicts. If there is no uploads will return a empty list.

        >>> my.get_uploads()
        [{'id': '5021b3b7c402468d5b018a8b4a2b448a', 'filename': 'sample-mp4-file.mp4'},
         {'id': 'caf52322a13608e78751573ef1f94bc6', 'filename': 'sample-png-file.png'}]

        If there is no uploads

        >>> my.get_uploads()
        []

        If you know the upload id

        >>> my.get_uploads(id='caf52322a13608e78751573ef1f94bc6')
        [{'id': 'caf52322a13608e78751573ef1f94bc6', 'filename': 'sample-png-file.png'}]

        If the id doesn't exists.

        >>> my.get_uploads(id='123456789abcdefghijklmnopqrstyvwxyz')
        []

        """
        if kwargs:
            if spec_id := kwargs.get("id", False):
                self.uploads = self.get_all("uploads")
                return list(filter(lambda x: x["id"] == spec_id, self.uploads))
            else:
                raise Exception("This function only accepts the id field")
        else:
            self.uploads = self.get_all("uploads")
        return self.uploads

    def get_medias(self, **kwargs):
        """Get the medias of the 4YouSee account.

        :param id: Id of the media to be edited.
        :type id: int, optional
        :param name: Full or part name.
        :type name: str, optional
        :param categoryId: Id of an media category.
        :type categoryId: Int or str, optional
        :return: List of dicts where every dict depicts a media.
        :rtype: list

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        Getting all the medias. It will return all the contents of your account. It will be a
        list of dicts. If there is no content will return a empty list.

        >>> my.get_medias()

        Filtering by id. It will return a dict

        >>> my.get_medias(id=60)
        {
           "id":60,
           "name":"Content_Deck_Vertical",
           "description":"Content_Deck_Vertical",
           "file":"i_60.mp4",
           "durationInSeconds":74,
           "categories":[
              { "id":2, "name":"Sample name via API" }
           ],
           "schedule":{
              "startDate":"None",
              "endDate":"None",
              "times":[ ]
           }
        }

        Filtering by name. It will return a list of dicts, where every one is a match, a media.

        >>> my.get_medias(name='play')
        [
           {
              "id":1,
              "name":"4YouSee Play",
              "description":"4YouSee Play",
              "file":"i_1.mp4",
              "durationInSeconds":10,
              "categories":[
                 { "id":1, "name":"DEMO" },
                 { "id":3, "name":"Imagenes" },
                 { "id":11, "name":"Cliente 1" },
                 { "id":15, "name":"Semanas" },
                 { "id":16, "name":"Semana 1" }
              ],
              "schedule":{
                 "startDate":"2021-06-25",
                 "endDate":"2021-06-30",
                 "times":[
                    {
                       "startTime":"06:00",
                       "endTime":"23:00",
                       "weekDays":[ 0, 2, 3, 5 ]
                    },
                    {
                       "startTime":"09:00",
                       "endTime":"23:00",
                       "weekDays":[ 1, 4, 6 ]
                    }
                 ]
              }
           },
           {
              "id":125,
              "name":"player instalado",
              "description":"player instalado",
              "file":"i_125.gif",
              "durationInSeconds":0,
              "categories":[
                 { "id":1, "name":"DEMO" }
              ],
              "schedule":{
                 "startDate":"None",
                 "endDate":"None",
                 "times":[ ]
              }
           }
        ]

        Filtering by categoryId. It will return a list of dicts,
        where every one is a match, a media. *In case one of the
        categories id doesn't exists, it will be ignored*.

        >>> my.get_medias(categoryId=10)  # If the category doesn't have medias
        []
        >>> my.get_medias(categoryId=15)
        [
           {
              "id":1,
              "name":"Play",
              "description":"4YouSee Play",
              "file":"i_1.mp4",
              "durationInSeconds":10,
              "categories":[
                 { "id":1, "name":"DEMO" },
                 { "id":3, "name":"Imagenes" },
                 { "id":11, "name":"Cliente 1" },
                 { "id":15, "name":"Semanas" },
                 { "id":16, "name":"Semana 1" }
              ],
              "schedule":{
                 "startDate":"2021-06-25",
                 "endDate":"2021-06-30",
                 "times":[
                    {
                       "startTime":"06:00",
                       "endTime":"23:00",
                       "weekDays":[ 0, 2, 3, 5 ]
                    },
                    {
                       "startTime":"09:00",
                       "endTime":"23:00",
                       "weekDays":[ 1, 4, 6 ]
                    }
                 ]
              }
           }
        ]
        >>> my.get_medias(categoryId='1,2,4'))
        [
           {
              "id":1,
              "name":"Play",
              "description":"4YouSee Play",
              "file":"i_1.mp4",
              "durationInSeconds":10,
              "categories":[
                 { "id":1, "name":"DEMO" },
                 { "id":3, "name":"Imagenes" },
                 { "id":11, "name":"Cliente 1" },
                 { "id":15, "name":"Semanas" },
                 { "id":16, "name":"Semana 1" }
              ],
              "schedule":{
                 "startDate":"2021-06-25",
                 "endDate":"2021-06-30",
                 "times":[
                    {
                       "startTime":"06:00",
                       "endTime":"23:00",
                       "weekDays":[ 0, 2, 3, 5 ]
                    },
                    {
                       "startTime":"09:00",
                       "endTime":"23:00",
                       "weekDays":[ 1, 4, 6 ]
                    }
                 ]
              }
           }
        ]

        Mixing filters:
        It will return a list of dicts, where every one is a match, a media that is part of
        `categoryId=1` and has the word `4yousee` inside it.

        >>> my.get_medias(name='4yousee', categoryId=1)

        **Advanced usage**

        - Printing all the medias that has an schedule established.

        >>> my.get_medias()
        >>> import json
        >>> for media in my.medias:
        >>>     if media['schedule']['startDate'] and media['schedule']['endDate']:
        >>>         print(json.dumps(media, indent=2))

        .. warning:: The previous example consider the entire library of contents

        """
        if kwargs:
            if spec_id := kwargs.get("id", False):
                del kwargs["id"]
                return self.get_all("medias/{}".format(spec_id))
            else:
                return self.get_all("medias", **kwargs)
        else:
            self.medias = self.get_all("medias")
        return self.medias

    def get_media_category(self, **kwargs):
        """
        Get the media categories of the 4YouSee account.

        :param id: Id of the media category.
        :type id: int, optional
        :return: List of dicts, where every dict, depicts a media category.
        :rtype: list

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        Getting all media categories. It will return all the media categories of your account.
        It will be a list of dicts. If there is no media category will return a empty list.

        >>> my.get_media_category()

        If you know the media category id

        >>> my.get_media_category(id=108)
        {
           "id":108,
           "name":"sample media category",
           "description":"None",
           "parent":{
              "id":1,
              "name":"DEMO",
              "description":"",
              "carouselThumbnail":"None",
              "autoShuffle":false,
              "updateFlow":"1"
           },
           "children":[ ],
           "carouselThumbnail":"None",
           "autoShuffle":false,
           "updateFlow":"1",
           "sequence":[ ]
        }

        If the id doesn't exists.

        >>> my.get_media_category(id=123_456)
        Exception: {"message":"Category with ID 123456 was not found"}
        
        **Advanced usage**

        - Getting empty media categories.

        >>> my.get_media_category()
        >>> [ mc['id'] for mc in my.media_category if not len(mc['sequence'])]
        [9, 10, 14, 17, 18, 19, 20,]


        """
        if kwargs:
            if spec_id := kwargs.get("id", False):
                del kwargs["id"]
                return self.get_all("medias/categories/{}".format(spec_id))
            else:
                raise Exception("This function only accepts the id field")
        else:
            self.media_category = self.get_all("medias/categories")
        return self.media_category

    def get_players(self, **kwargs):
        """
        Get the players of the 4YouSee account.

        :param id: Id of the player
        :type id: int, optional
        :return: List of dicts, where every dict, depicts a player.
        :rtype: list

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        Getting all players. It will return all the players of your account.
        It will be a list of dicts. If there is no player will return a empty list.

        >>> my.get_players()
        [
           {
              "id":1,
              "name":"Player DEMO",
              "description":"Ponto de demonstração disponibilizado na
                            instalação do 4YouSee Manager.Player demo available
                            on  4YouSee Manager installation.",
              "platform":"ANDROID",
              "lastContactInMinutes":224998,
              "group":{ "id":1, "name":"Group DEMO" },
              "playerStatus":{
                 "id":5,
                 "name":"Local assist needed",
                 "time":9999999
              },
              "playlists":{
                 "0":{ "id":3, "name":"Novo" },
                 "1":{ "id":3, "name":"Novo" },
                 "2":{ "id":3, "name":"Novo" },
                 "3":{ "id":3, "name":"Novo" },
                 "4":{ "id":3, "name":"Novo" },
                 "5":{ "id":3, "name":"Novo" },
                 "6":{ "id":3, "name":"Novo" }
              },
              "audios":{
                 "0":{ "id":1, "name":"Contenido Vertical" }
              },
              "lastLogReceived":"2022-01-26 13:49:28"
           },
           {
              "id":2,
              "name":"Sample name via API",
              "description":"Description from API",
              "platform":"SAMSUNG",
              "lastContactInMinutes":1,
              "group":{ "id":2, "name":"Clientes Barrio Sur" },
              "playerStatus":{
                 "id":1,
                 "name":"Online",
                 "time":10
              },
              "playlists":{
                 "0":{ "id":1, "name":"Contenido Vertical" },
                 "1":{ "id":1, "name":"Contenido Vertical" },
                 "2":{ "id":1, "name":"Contenido Vertical" },
                 "3":{ "id":1, "name":"Contenido Vertical" },
                 "4":{ "id":1, "name":"Contenido Vertical" },
                 "5":{ "id":1, "name":"Contenido Vertical" },
                 "6":{ "id":1, "name":"Contenido Vertical" }
              },
              "audios":{
                 "0":{ "id":1, "name":"Contenido Vertical" }
              },
              "lastLogReceived":"2022-07-01 16:46:33"
           }
        ]

        If you know the player id

        >>> my.get_players(id=1)
        {
           "id":1,
           "name":"Player DEMO",
           "description":"Ponto de demonstração disponibilizado na
                        instalação do 4YouSee Manager.Player demo available on
                        4YouSee Manager installation.",
           "platform":"ANDROID",
           "lastContactInMinutes":224999,
           "group":{ "id":1, "name":"Group DEMO" },
           "playerStatus":{
              "id":5,
              "name":"Local assist needed",
              "time":9999999
           },
           "playlists":{
              "0":{ "id":3, "name":"Novo" },
              "1":{ "id":3, "name":"Novo" },
              "2":{ "id":3, "name":"Novo" },
              "3":{ "id":3, "name":"Novo" },
              "4":{ "id":3, "name":"Novo" },
              "5":{ "id":3, "name":"Novo" },
              "6":{ "id":3, "name":"Novo" }
           },
           "audios":{
              "0":{ "id":1, "name":"Contenido Vertical" }
           },
           "lastLogReceived":"2022-01-26 13:49:28"
        }

        If the id doesn't exists.

        >>> my.get_players(id=123_456)
        Exception: {"message":"Player with ID 123456 was not found"}

        **Advanced Usage**

        - Getting the playlists id's of the players. If two players
            share the same playlist, it will consider just one.

        >>> my.get_players()  # Updating the player attribute
        >>> active_playlists = set()
        >>> for player in my.players:
        ...    active_playlists.add(player['playlists']['0']['id'])
        >>> active_playlists
        {1, 67, 3, 4, 5, 8}

        """
        if kwargs:
            if spec_id := kwargs.get("id", False):
                del kwargs["id"]
                return self.get_all("players/{}".format(spec_id))
            else:
                raise Exception("This function only accepts the id field")
        else:
            self.players = self.get_all("players")
        return self.players

    def get_playlists(self, **kwargs):
        """
        Get the playlists of the 4YouSee account.

        :param id: Id of the playlist.
        :type id: int, optional
        :return: List of dicts, where every dict, depicts a playlist.
        :rtype: list

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        Getting all playlists. It will return all the playlists of your account.
        It will be a list of dicts. If there is no playlist will return a empty list.

        >>> my.get_playlists()
        [
           {
              "id":38,
              "name":"Player DEMO",
              "durationInSeconds":112,
              "isSubPlaylist":false,
              "category":"None",
              "items":[
                 { "type":"news", "durationInSeconds":10 },
                 {
                    "type":"media",
                    "id":55,
                    "name":"samsung_A80",
                    "file":"i_55.mp4",
                    "durationInSeconds":10
                 },
                 {
                    "type":"media",
                    "id":31,
                    "name":"Gopro",
                    "file":"i_31.mp4",
                    "durationInSeconds":30
                 },
                 {
                    "type":"media",
                    "id":56,
                    "name":"audifonos_samsung",
                    "file":"i_56.mp4",
                    "durationInSeconds":10
                 },
                 {
                    "type":"media",
                    "id":51,
                    "name":"pelicula__sello_cinepolis",
                    "file":"i_51.mp4",
                    "durationInSeconds":12
                 },
                 {
                    "type":"media",
                    "id":53,
                    "name":"ubereats",
                    "file":"i_53.mp4",
                    "durationInSeconds":10
                 }
              ],
              "sequence":[ 0, 0, 1, 2, 3, 4, 0, 5 ]
           },
           {
              "id":39,
              "name":"Liva PC",
              "durationInSeconds":112,
              "isSubPlaylist":false,
              "category":"None",
              "items":[
                 { "type":"news", "durationInSeconds":10 },
                 {
                    "type":"media",
                    "id":55,
                    "name":"samsung_A80",
                    "file":"i_55.mp4",
                    "durationInSeconds":10
                 },
                 {
                    "type":"media",
                    "id":31,
                    "name":"Gopro",
                    "file":"i_31.mp4",
                    "durationInSeconds":30
                 },
                 {
                    "type":"media",
                    "id":56,
                    "name":"audifonos_samsung",
                    "file":"i_56.mp4",
                    "durationInSeconds":10
                 },
                 {
                    "type":"media",
                    "id":51,
                    "name":"pelicula__sello_cinepolis",
                    "file":"i_51.mp4",
                    "durationInSeconds":12
                 },
                 {
                    "type":"media",
                    "id":53,
                    "name":"ubereats",
                    "file":"i_53.mp4",
                    "durationInSeconds":10
                 }
              ],
              "sequence":[ 0, 0, 1, 2, 3, 4, 0, 5 ]
           }
        ]

        If you know the playlist id

        >>> my.get_playlists(id=39)
        {
           "id":38,
           "name":"Player DEMO",
           "durationInSeconds":112,
           "isSubPlaylist":false,
           "category":"None",
           "items":[
              { "type":"news", "durationInSeconds":10 },
              {
                 "type":"media",
                 "id":55,
                 "name":"samsung_A80",
                 "file":"i_55.mp4",
                 "durationInSeconds":10
              },
              {
                 "type":"media",
                 "id":31,
                 "name":"Gopro",
                 "file":"i_31.mp4",
                 "durationInSeconds":30
              },
              {
                 "type":"media",
                 "id":56,
                 "name":"audifonos_samsung",
                 "file":"i_56.mp4",
                 "durationInSeconds":10
              },
              {
                 "type":"media",
                 "id":51,
                 "name":"pelicula__sello_cinepolis",
                 "file":"i_51.mp4",
                 "durationInSeconds":12
              },
              {
                 "type":"media",
                 "id":53,
                 "name":"ubereats",
                 "file":"i_53.mp4",
                 "durationInSeconds":10
              }
           ],
           "sequence":[ 0, 0, 1, 2, 3, 4, 0, 5 ]
        }

        If the id doesn't exists.

        >>> my.get_playlists(id=123_456)
        Exception: {"message":"Playlist with ID 123456 was not found"}

        **Advanced Usage**

        - Gettin all the contents of the active playlists

        Let's suppose, we have an iterable with the playlists id, called `active_playlists`

        >>> active_playlists, active_medias = [1, 67, 3, 4, 5, 8], []
        >>> my.get_playlists()
        >>> def active_contents(plist: dict) -> list:
        ...     temp_act_list = []
        ...     for item in plist['items']:
        ...         match item['type']:
        ...             case 'media':
        ...                 temp_act_list += [item['id']]
        ...             case 'carousel':
        ...                 if item['items']:
        ...                     temp_act_list += list(map(lambda x: x['id'], item['items'))
        ...                 else:
        ...                     pass
        ...             case 'videoWall':
        ...                     for rows in item['grid']:
        ...                         temp_act_list += list(map(lambda x: x['id'], rows))
        ...             case 'subPlaylist':
        ...                 temp_act_list += active_contents(item)
        ...     return temp_act_list
        >>> for plist in list(filter(lambda x: x['id'] in active_playlists, my.playlists)):
        ...     active_medias += active_contents(plist)
        >>> print(sorted(list(set(active_medias)))
        [1, 3, 4, 8, 19, 20, 28, 30, 32, 33, 38, 39, 40, 45, 48, 49,
        50, 53, 54, 55, 56, 57, 66, 69, 80, 99, 100, 101]

        """
        if kwargs:
            if spec_id := kwargs.get("id", False):
                del kwargs["id"]
                return self.get_all("playlists/{}".format(spec_id))
            else:
                raise Exception("This function only accepts the id field")
        else:
            self.playlists = self.get_all("playlists")
        return self.playlists

    def get_templates(self, **kwargs):
        """
        Get the templates of the 4YouSee account.

        :param id: Id of the template.
        :type id: int, optional
        :return: List of dicts, where every dict, depicts a template.
        :rtype: list

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        Getting all templates. It will return all the templates of your account.
        It will be a list of dicts. If there is no template will return a empty list.

        >>> my.get_templates()
        [
           {
              "id":35,
              "name":"Barra Logo Horizontal HTML5",
              "width":402,
              "height":100,
              "type":"zip"
           },
           {
              "id":39,
              "name":"Facebook v1 - Área Principal",
              "width":1280,
              "height":720,
              "type":"zip"
           },
           {
              "id":41,
              "name":"Instagram - Área Principal",
              "width":1280,
              "height":720,
              "type":"zip"
           },
           {
              "id":48,
              "name":"Finance: Bovespa-Nasdaq-Nikkei Horizontal HTML5",
              "width":1280,
              "height":720,
              "type":"zip"
           },
           {
              "id":54,
              "name":"CNN - Área Principal",
              "width":1280,
              "height":720,
              "type":"zip"
           },
           {
              "id":55,
              "name":"Yahoo Weather - Área Principal",
              "width":1280,
              "height":720,
              "type":"zip"
           }
        ]

        If you know the template id

        >>> my.get_templates(id=39)
        [
           {
              "id":39,
              "name":"Facebook v1 - Área Principal",
              "width":1280,
              "height":720,
              "type":"zip"
           }
        ]

        If the id doesn't exists.

        >>> my.get_templates(id=123_456)
        []

        """
        if kwargs:
            if spec_id := kwargs.get("id", False):
                self.templates = self.get_all("templates")
                return list(
                    filter(lambda x: x["id"] == spec_id, self.templates)
                )
            else:
                raise Exception("This function only accepts the id field")
        else:
            self.templates = self.get_all("templates")
        return self.templates

    def get_newsources(self, **kwargs) -> List:
        """
        Get the newsources (Rss Feeds) of the 4YouSee account.

        :param id: Id of the newsource.
        :type id: int, optional
        :param name: Newsource name or part of it to search.
        :type name: str, optional
        :param template: Template id to search.
        :type template: int, optional
        :param insertContentAutomatically: 0 if search only
            automatic content and 1 for manual.
        :type insertContentAutomatically: str, optional
        :return: List of dicts, where every dict, depicts a newsource.
        :rtype: list

         **Usage**

        Once "**my**" object has been created. You can execute the next:

        Getting all the newsources. It will return all the newsources
        of your account. It will be a list of dicts. If there is no
        newsources will return a empty list.

        >>> my.get_newsources()
        [
           {
              "id":100,
              "name":"Twitter Revista Semana (Vertical)",
              "url":"/rotinas/canal_obter_rss.php?idcanal=31",
              "template":91,
              "onlyWithImages":"Yes",
              "limit":10,
              "daysToExpire":1,
              "weight":1,
              "variables":"None",
              "approveAutomatically":"Yes",
              "insertContentAutomatically":true
           },
           {
              "id":113,
              "name":"Viajes",
              "url":"/rotinas/canal_obter_rss.php?idcanal=35",
              "template":101,
              "onlyWithImages":"Yes",
              "limit":10,
              "daysToExpire":1,
              "weight":1,
              "variables":"None",
              "approveAutomatically":"Yes",
              "insertContentAutomatically":true
           },
           {
              "id":48,
              "name":"Yahoo Weather Colombia",
              "url":"/rotinas/canal_obter_rss.php?idcanal=14",
              "template":55,
              "onlyWithImages":"No",
              "limit":1,
              "daysToExpire":1,
              "weight":1,
              "variables":"None",
              "approveAutomatically":"Yes",
              "insertContentAutomatically":true
           }
        ]

        If there is no newsources

        >>> my.get_newsources()
        []

        If you know the newsource id

        >>> my.get_newsource(id=100)
        [
           {
              "id":100,
              "name":"Twitter Revista Semana (Vertical)",
              "url":"/rotinas/canal_obter_rss.php?idcanal=31",
              "template":91,
              "onlyWithImages":"Yes",
              "limit":10,
              "daysToExpire":1,
              "weight":1,
              "variables":"None",
              "approveAutomatically":"Yes",
              "insertContentAutomatically":true
           }
        ]

        If the id doesn't exists.

        >>> my.get_newsources(id=123_456)
        []

        Filtering by template

        >>> my.get_newsources(template=91)
        [
           {
              "id":100,
              "name":"Twitter Revista Semana (Vertical)",
              "url":"/rotinas/canal_obter_rss.php?idcanal=31",
              "template":91,
              "onlyWithImages":"Yes",
              "limit":10,
              "daysToExpire":1,
              "weight":1,
              "variables":"None",
              "approveAutomatically":"Yes",
              "insertContentAutomatically":true
           }
        ]

        Filtering by name

        >>> my.get_newsources(name='twit')
        [
           {
              "id":55,
              "name":"Twitter El Espectador",
              "url":"/rotinas/canal_obter_rss.php?idcanal=27",
              "template":63,
              "onlyWithImages":"Yes",
              "limit":7,
              "daysToExpire":1,
              "weight":1,
              "variables":"None",
              "approveAutomatically":"Yes",
              "insertContentAutomatically":true
           },
           {
              "id":8,
              "name":"Twitter El Heraldo",
              "url":"/rotinas/canal_obter_rss.php?idcanal=4",
              "template":89,
              "onlyWithImages":"Yes",
              "limit":7,
              "daysToExpire":1,
              "weight":1,
              "variables":"None",
              "approveAutomatically":"Yes",
              "insertContentAutomatically":true
           },
           {
              "id":53,
              "name":"Twitter Noticias Caracol",
              "url":"/rotinas/canal_obter_rss.php?idcanal=26",
              "template":62,
              "onlyWithImages":"Yes",
              "limit":20,
              "daysToExpire":1,
              "weight":1,
              "variables":"None",
              "approveAutomatically":"Yes",
              "insertContentAutomatically":true
           },
           {
              "id":100,
              "name":"Twitter Revista Semana (Vertical)",
              "url":"/rotinas/canal_obter_rss.php?idcanal=31",
              "template":91,
              "onlyWithImages":"Yes",
              "limit":10,
              "daysToExpire":1,
              "weight":1,
              "variables":"None",
              "approveAutomatically":"Yes",
              "insertContentAutomatically":true
           }
        ]

        Filtering by insertContentAutomatically

        >>> my.get_newsources(insertContentAutomatically=0)  # 0 means False and 1 True
        [
           {
              "id":116,
              "name":"Barra Noticias Manual",
              "url":"",
              "template":103,
              "onlyWithImages":"No",
              "limit":10,
              "daysToExpire":1,
              "weight":1,
              "variables":[
                 "texto"
              ],
              "approveAutomatically":"Yes",
              "insertContentAutomatically":false
           },
           {
              "id":49,
              "name":"Streaming Youtube",
              "url":"",
              "template":58,
              "onlyWithImages":"No",
              "limit":10,
              "daysToExpire":1,
              "weight":1,
              "variables":[
                 "videoURL",
                 "tempo"
              ],
              "approveAutomatically":"Yes",
              "insertContentAutomatically":false
           },
           {
              "id":50,
              "name":"Ticker texto inferior",
              "url":"",
              "template":59,
              "onlyWithImages":"No",
              "limit":10,
              "daysToExpire":1000,
              "weight":1,
              "variables":[
                 "Texto"
              ],
              "approveAutomatically":"Yes",
              "insertContentAutomatically":false
           }
        ]

        """
        if kwargs:
            return self.get_all("newsources", **kwargs)
        self.newsources = self.get_all("newsources")
        return self.newsources

    def get_news(self, **kwargs):
        """
        Get the medias of the 4YouSee account.

        :param id: Id of the specific new.
        :type id: int, optional
        :param newsourceId: Id of the Newsource.
        :type newsourceId: int, optional
        :param startDate: Start date of the news.
        :type startDate: str, optional
        :param endDate: End date of the news.
        :type endDate: str, optional
        :param status: Status of the news. The possible values are approved, disapproved or, waiting.
        :type status: str, optional
        :return: List of dicts, where dict depicts a news.
        :rtype: list

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        Getting all the news. It will return all the news of your news. It will be a
        list of dicts. If there is no news will return a empty list.

        .. note:: Depend of the quantity of news, this execution use to take more than 7 seconds.

        >>> my.get_news()

        If there is no news

        >>> my.get_news()
        []

        If you know the news id

        >>> my.get_news(id=401579)
        {
           "file":"https://4usee.com/****-*****/****/common/imgnews/0.png",
           "approvalDate":"2020-02-19 07:35:28",
           "content":{ "texto":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt" },
           "creationDate":"2020-02-19 07:35:28",
           "startDate":"2020-02-19 00:33:00",
           "endDate":"2033-02-20 07:33:00",
           "status":"approved",
           "image":"0.png",
           "id":401579,
           "newsourceId":116,
           "newsourceName":"Barra Noticias Manual",
           "hash":"None"
        }

        If the id doesn't exists.

        >>> my.get_news(id=123_456)
        Exception: {"error":"C004","message":"Resource not found."}

        Filtering by newsourceId (Feed Rss), status, startDate and endDate

        >>> my.get_news(newsourceId=55)  # If the newsourceId doesn't exist
        []
        >>> my.get_news(newsourceId=125, status='approved',
        ...             startDate='2022-07-01', endDate='2022-07-02 13:02:00')
        [
           {
              "id":501609,
              "content":{
                 "img":"https://cnnespanol.cnn.com/wp-content/uploads/
                 2022/03/GettyImages-1210678056.jpg?quality",
                 "amp;strip":"info",
                 "tag_description":"A partir de marzo de 2022, los pagos del Ingreso
                  solidario son bimensuales y desde julio, los montos cambiarán
                  según la clasificación del Sisbén IV.",
                 "tag_title":"Calendario Ingreso Solidario 2022: cuáles son los
                  fechas de los siguientes pagos en Colombia"
              },
              "creationDate":"2022-07-01 13:01:25",
              "status":"approved",
              "approvalDate":"2022-07-01 13:01:25",
              "startDate":"2022-07-01 13:01:25",
              "endDate":"2022-07-02 13:01:25",
              "newsourceId":47,
              "newsourceName":"CNN",
              "image":"https://4usee.com/.../501609.jpeg"
           }
        ]

        """
        if kwargs:
            if spec_id := kwargs.get("id", False):
                del kwargs["id"]
                return self.get_all("news/{}".format(spec_id))
            else:
                return self.get_all("news", **kwargs)
        else:
            self.news = self.get_all("news")
        return self.news

    def get_reports(self, **kwargs):
        """
        Get the requested reports of the 4YouSee account.

        :param id: Id of the report.
        :type id: int, optional
        :return: List of dicts, where every dict, depicts a report.
        :rtype: list

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        Getting all reports. It will return all the reports of your account.
        It will be a list of dicts. If there is no report will return a empty list.

        >>> my.get_reports()

        If you know the report id

        >>> my.get_reports(id=521546)  # When the report is ready (status = 'success')
        {
           "id":521546,
           "type":"detailed",
           "format":"json",
           "filter":{
              "startDate":"2020-07-26",
              "startTime":"00:00:00",
              "endDate":"2020-08-24",
              "endTime":"23:59:59",
              "mediaId":[ 1, 2, 3 ],
              "playerId":[ 2 ],
              "sort":-1
           },
           "status":"success",
           "url":"https://4yousee-playlogs-reports.s3.amazonaws.com/...62bb067d43ac1.gz",
           "createdAt":"2022-06-28T13:47:36+00:00",
           "updatedAt":"2022-06-28T13:47:41+00:00"
        }

        If the id doesn't exists.

        >>> my.get_reports(id=123_456)
        Exception: {"message":"Report with ID 5215464 was not found"}

        """
        if kwargs:
            if spec_id := kwargs.get("id", False):
                del kwargs["id"]
                return self.get_all("reports/{}".format(spec_id))
            else:
                raise Exception("This function only accepts the id field")
        else:
            self.reports = self.get_all("reports")
        return self.reports

    def post(
        self,
        resource: str,
        header_type: str = "application/json",
        files=None,
        payload=None,
    ):
        url = "{base_url}{resource}".format(
            base_url=FouryouseeAPI.url, resource=resource
        )
        headers = {"Content-Type": header_type, "Secret-Token": self.token}
        time.sleep(1)
        response = requests.post(
            url, headers=headers, data=payload, files=files
        )
        if not response.ok:
            raise Exception(response.text)
        return json.loads(response.text)

    def upload_files(self, files: str or list) -> List[dict]:
        """Upload a file on the 4YouSee account.

        :param files: Path of the file(s) locally.
        :type files: str or list, required
        :return: List of dicts if the file was uploaded.
        :rtype: list

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        Uploading one file

        >>> my.upload_files(files='/home/username/Desktop/sample-mp4-file.mp4')
        [{'id': '5021b3b7c402468d5b018a8b4a2b448a', 'filename': 'sample-mp4-file.mp4'}]

        Uploading multiple files

        >>> my.upload_files(files=['/home/username/Desktop/sample-mp4-file.mp4',
        ...                         '/home/username/Downloads/sample-jpg-file.jpg'])
        [{'id': '5021b3b7c402468d5b018a8b4a2b448a', 'filename': 'sample-mp4-file.mp4'},
        {'id': '9db1ca3bf0b81dd30e40c721323b59a6', 'filename': 'sample-zip-file.zip'}]

        If the file doens't exist, will raise and Exception

        >>> my.upload_files(files='/home/username/Desktop/file.mp4')
        Exception: File /home/username/Desktop/file.mp4 not found.

        """
        if not files:
            raise Exception("Missing 'files' field.")
        if isinstance(files, str):
            files = files.split(",")
        if isinstance(files, (list, tuple)):
            payload = {"Content-Type": "multipart/form-data;"}

            result, multiple_files = [], []

            for file in files:
                file = Path(file)
                if not file.exists():
                    raise Exception(f"File {file} not found.")
                multiple_files.append(
                    ("media", (file.name, open(file, "rb"), myme_type(file)))
                )
            for file in multiple_files:
                result.append(
                    self.post(
                        resource="uploads",
                        header_type=None,
                        files=[file],
                        payload=payload,
                    )
                )
            return result

    def add_media(self, **kwargs) -> dict:
        """Create a new media in the 4yousee account library.
        Obs.: Is not allowed post a html files through the API.

        :param name: Name of the media in the account, default value
                will be the name of the file.
        :type name: str, optional
        :param file: Path of the file(s) locally.
        :type file: str, required
        :param duration: Duration of media.
        :type duration: int, required only for images or zip files
        :param categories: List of id of categories where this media will belong.
        :type categories: list of ints, required
        :param schedule: scheduling information.
        :type schedule: dict, optional
        :return: Dict that depicts the added media.
        :rtype: dict

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        Passing only the required params

        >>> my.add_media(file='/home/username/Desktop/sample-mp4-file.mp4',
        ...             categories=[31])
        {
           "id":422,
           "name":"sample-mp4-file",
           "file":"https://4usee.com/*******/*****/common/videos/i_422.mp4",
           "duration":126,
           "schedule":{
              "times":[ ]
           },
           "categories":[ 31 ]
        }

        Adding a zip file with schedule information

        >>> my.add_media(file='/home/username/Desktop/sample-mp4-file.zip',
        ...               duration=10, categories=[1],
        ...               schedule={
        ...                         "startDate": "2022-06-29",
        ...                         "endDate": "2022-07-31",
        ...                             "times": [
        ...                                         {
        ...                                            "startTime": "08:00",
        ...                                             "endTime": "11:00",
        ...                                             "weekDays": [ 0, 2, 4, 5 ]
        ...                                         }
        ...                                      ]
        ...                         })
        {
           "id":423,
           "name":"sample-zip-file",
           "file":"https://4usee.com/.../.../videos/i_423.zip",
           "duration":10,
           "schedule":{
              "startDate":"2022-06-29",
              "endDate":"2022-07-31",
              "times":[
                 {
                    "startTime":"08:00",
                    "endTime":"11:00",
                    "weekDays":[ 0, 2, 4, 5 ]
                 }
              ]
           },
           "categories":[ 1 ]
        }

        """

        # Validators
        validate_kwargs_single_media(**kwargs)

        file = Path(kwargs.get("file"))
        kwargs["name"] = kwargs.get("name", file.stem)

        # Figure out the category to associate to the media
        categories = kwargs.get("categories")
        if isinstance(categories, str):
            categories = list(map(int, categories.split(",")))
        elif isinstance(categories, int):
            categories = [categories]
        kwargs["categories"] = categories

        file_uploaded = self.upload_files(str(file))
        if file_uploaded:
            kwargs["file"] = file_uploaded[0]
            payload = json.dumps(kwargs, indent=2)
            return self.post(resource="medias", payload=payload)

    def add_media_category(self, **kwargs) -> dict:
        """
        Create a new category in the 4yousee account library.

        :param name: Category/subcategory display name.
        :type name: str, required
        :param description: Detailed category description.
        :type description: str, optional
        :param parent: When informed it creates a subcategory.
        :type parent: int, optional
        :param autoShuffle: True to scramble the order of contents on the carousel.
        :type autoShuffle: bool, optional                .
        :param updateFlow:  1 to restart carousel after carousel update;
                2: Do not restart after carousel update.
        :type updateFlow: int, optional
        :return: Dict that depicts the media category created.
        :rtype: dict

        **Usage**

        Once “**my**” object has been created. You can execute the next:

        Passing only the required params

        >>> my.add_media_category(name='Example category')
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

        Adding a subcategory

        >>> my.add_media_category(name='New category',
        ...                       description='Son of category #143',
        ...                       parent=143, autoShuffle=True)
        {
            'id': 29,
            'name': 'New category',
            'description': 'Son of category #143',
            'parent':
                {
                    'id': 30,
                    'name': 'Example category',
                    'description': None,
                    'carouselThumbnail': None,
                    'autoShuffle': False,
                    'updateFlow': '1'
                },
            'children': [],
            'carouselThumbnail': None,
            'autoShuffle': True,
            'updateFlow': '1',
            'sequence': None
        }

        Adding a category that when is being update, It wont restart his execution inmediately

        >>> my.add_media_category(name='New category', updateFlow=2)
        {
            'id': 31,
            'name': 'New category',
            'description': None,
            'parent': None,
            'children': [],
            'carouselThumbnail': None,
            'autoShuffle': False,
            'updateFlow': '2',
            'sequence': None
        }

        """
        # Validators
        validate_kwargs_single_media_category(**kwargs)
        payload = json.dumps(kwargs, indent=2)
        return self.post("medias/categories/", payload=payload)

    def add_player(self, **kwargs) -> dict:
        """
        Create a new player in the 4yousee account.

        :param name: Display name.
        :type name: str, required
        :param description: Detailed player description.
        :type description: str, optional
        :param platform: Platform where the 4yousee player will be executed.
                They can be **4YOUSEE_PLAYER** or **SAMSUNG** or
                **ANDROID** or **LG**
        :type platform: str, required
        :param group: Id of a group of players.
        :type group: int, optional
        :param playlists: Dict with 7 keys and 7 values. Every key depicts the number
                of the day (starting from 0) and every value the playlist id.
        :type playlists: dict, required
        :param audios: A dict with "0" as his only key and a value that depicts
                the id of the audio playlist
        :type audios: dict, optional
        :return: Dict that depicts the player created.
        :rtype: dict

        **Usage**

        Passing only the required params

        >>> my.add_player(name='Player Example',
        ...               platform='ANDROID',
        ...               playlists={ "0": 1, "1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1 })
        {
          "id": 6,
          "name": "Player name example",
          "description": "Player description example",
          "platform": "ANDROID",
          "lastContactInMinutes": null,
          "group": { "id": 1, "name": "Group DEMO" },
          "playerStatus": { "id": 6, "name": "Never accessed", "time": 0 },
          "playlists": {
            "0": { "id": 1, "name": "Playlist DEMO" },
            "1": { "id": 1, "name": "Playlist DEMO" },
            "2": { "id": 1, "name": "Playlist DEMO" },
            "3": { "id": 1, "name": "Playlist DEMO" },
            "4": { "id": 1, "name": "Playlist DEMO" },
            "5": { "id": 1, "name": "Playlist DEMO" },
            "6": { "id": 1, "name": "Playlist DEMO" }
          },
          "audios": { "0": None }
          "lastLogReceived": None
        }


        Passing all the params

        >>> >>> my.add_player(name='Player Example',
        ...                   description='Extra information for this player',
        ...                   platform='4YOUSEE_PLAYER',
        ...                   playlists={ "0": 24 "1": 24 "2": 24 "3": 24 "4": 24 "5": 24 "6": 24 },
        ...                   group=2,
        ...                   audios={'0': 8}
        {
           "id":25,
           "name":"Player Example",
           "description":"Extra information for this player",
           "platform":"4YOUSEE_PLAYER",
           "lastContactInMinutes":"None",
           "group":{ "id":2, "name":"Clientes Barrio Sur" },
           "playerStatus":{
              "id":6,
              "name":"Never accessed",
              "time":0
           },
           "playlists":{
              "0":{ "id":24, "name":"Player DEMO" },
              "1":{ "id":24, "name":"Player DEMO" },
              "2":{ "id":24, "name":"Player DEMO" },
              "3":{ "id":24, "name":"Player DEMO" },
              "4":{ "id":24, "name":"Player DEMO" },
              "5":{ "id":24, "name":"Player DEMO" },
              "6":{ "id":24, "name":"Player DEMO" }
           },
           "audios":{
              "0":{ "id":8, "name":"Prueba 1" }
           },
           "lastLogReceived":"None"
        }

        """
        # Validators
        validate_kwargs_player(**kwargs)

        if len(kwargs.get("name")) > 50:
            kwargs["name"] = kwargs["name"][:46] + "..."

        kwargs["group"] = kwargs.get("group", 1)

        payload = json.dumps(kwargs, indent=2)
        return self.post("players/", payload=payload)

    def add_playlist(self, **kwargs) -> dict:
        """
        Create a new playlist in the 4yousee account.

        :param name: Playlist display name.
        :type name: str, required
        :param isSubPlaylist: Default value is False.
        :type isSubPlaylist: bool, optional
        :param category: Id of category of playlists.
        :type category: int, optional
        :param items: Items that the playlist will content
        :type items: list of dicts, required
        :param sequence: Sequence of execution of the items.
        :type sequence: list, required
        :return: dict that depicts the playlist created.
        :rtype: dict

        **Usage**

        Once “**my**” object has been created. You can execute the next:

        Passing all the required params

        >>> my.add_playlist(name='New Playlist Example',
        ...                 isSubplaylist=False,
        ...                 category=1,
        ...                 items=[
        ...                            { "type": "layout", "id": 1 },
        ...                            {
        ...                               "type": "videowall",
        ...                                "abortIfError": False,
        ...                                "ignoreLayout": False,
        ...                                "grid": [
        ...                                            [
        ...                                                { "type": "media", "id": 4 },
        ...                                               { "type": "media", "id": 1 }
        ...                                            ],
        ...                                            [
        ...                                                { "type": "media", "id": 2 },
        ...                                                { "type": "media", "id": 4 }
        ...                                            ]
        ...                                        ]
        ...                            },
        ...                            { "type": "media", "id": 5 },
        ...                            { "type": "news" }
        ...                        ],
        ...                 sequence=[ 0, 1, 2, 3])
        {
          "id": 89,
          "name": "New Playlist Example",
          "durationInSeconds": 30,
          "isSubPlaylist": false,
          "category": { "id": 1, "name": "Main Category" },
          "items": [
                    {
                      "type": "layout",
                      "id": 1,
                      "name": "Grid 1920x1080 com 1 \u00e1rea",
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
                            "categories": [
                              { "id": 1, "name": "DEMO" }
                            ]
                          },
                          {
                            "id": 1,
                            "name": "4YouSee Play",
                            "file": "i_1.mp4",
                            "durationInSeconds": 10,
                            "categories": [
                              { "id": 1, "name": "DEMO" },
                              { "id": 3, "name": "Imagenes" },
                              { "id": 11, "name": "Cliente 1" },
                              { "id": 15, "name": "Semanas" },
                              { "id": 16, "name": "Semana 1" }
                            ],
                            "contentSchedule": {
                              "startDate": "2021-06-25",
                              "endDate": "2021-06-30",
                              "times": [
                                {
                                  "startTime": "06:00",
                                  "endTime": "23:00",
                                  "weekDays": [ 0, 2, 3, 5 ]
                                },
                                {
                                  "startTime": "09:00",
                                  "endTime": "23:00",
                                  "weekDays": [ 1, 4, 6 ]
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
                            "categories": [
                              { "id": 1, "name": "DEMO" }
                            ]
                          },
                          {
                            "id": 4,
                            "name": "4YouSee Analyse",
                            "file": "i_4.mp4",
                            "durationInSeconds": 10,
                            "categories": [
                              { "id": 1, "name": "DEMO" }
                            ]
                          }
                        ]
                      ]
                    },
                    {
                      "type": "media",
                      "id": 1,
                      "name": "4YouSee Play",
                      "file": "i_1.mp4",
                      "durationInSeconds": 10,
                      "categories": [
                        { "id": 1, "name": "DEMO" },
                        { "id": 3, "name": "Imagenes" },
                        { "id": 11, "name": "Cliente 1" },
                        { "id": 15, "name": "Semanas" },
                        { "id": 16, "name": "Semana 1" }
                      ],
                      "contentSchedule": {
                        "startDate": "2021-06-25",
                        "endDate": "2021-06-30",
                        "times": [
                          {
                            "startTime": "06:00",
                            "endTime": "23:00",
                            "weekDays": [ 0, 2, 3, 5 ]
                          },
                          {
                            "startTime": "09:00",
                            "endTime": "23:00",
                            "weekDays": [ 1, 4, 6 ]
                          }
                        ]
                      }
                    },
                    {
                      "type": "news",
                      "durationInSeconds": 10
                    }
                  ],
          "sequence": [ 0, 1, 2, 3 ]
        }

        .. note:: The previous playlist has 4 elements inside it.

        """
        # Validators
        validate_kwargs_playlist(**kwargs)

        if len(kwargs.get("name")) > 50:
            kwargs["name"] = kwargs["name"][:46] + "..."

        payload = json.dumps(kwargs, indent=2)
        return self.post("playlists/", payload=payload)

    def request_report(self, **kwargs) -> dict:
        """
         Create a new request of report in the 4yousee account.
         Once is received the response, through the id will be possible
         to consult if the report is ready.

        :param type: Default value is 'detailed'.
        :type type: str, optional
        :param webhook: Web service that may allow the response with the
                report **Ex.**: http://4fc8e5ddf059.ngrok.io
        :type webhook: str, optional
        :param filter: Interval of time of the desired report.
        :type filter: dict, required
        :param sort: Default values is -1.
        :type sort: int, optional
        :return: Dict that depicts the report requested.
        :rtype: dict

        **Usage**

        Once “my” object has been created. You can execute the next:

        Passing only the required params

        >>> my.request_report(filter={
        ...                            "startDate": "2020-07-26",
        ...                            "startTime": "00:00:00",
        ...                            "endDate": "2020-08-24",
        ...                            "endTime": "23:59:59",
        ...                            "mediaId": [ ],  # List of id medias.
        ...                            "playerId": [ ],  # List of id players.
        ...                             "sort": -1 })
        { # Inmediately response
          "id": 522873,
          "type": "detailed",
          "format": "json",
          "filter": {
            "startDate": "2020-07-26",
            "startTime": "00:00:00",
            "endDate": "2020-08-24",
            "endTime": "23:59:59",
            "mediaId": [],
            "playerId": [],
            "sort": -1
          },
          "status": "waiting", # Look, the report wont be ready inmediately
          "url": null,
          "createdAt": "2022-07-02T12:42:05+00:00",
          "updatedAt": "2022-07-02T12:42:05+00:00"
        }

        .. note:: If a webhook url is passed, the report will make a post request to that url when is ready.
                Then you will have to download the file of the url field.

        .. note:: On this repository (Django project), `the view playlog
                <https://github.com/4YouSee-Suporte/4youseewebhook/blob/main/webhook/base/views.py>`_
                shows how to handle the POST sent by 4YouSee.

        """
        # Validators
        validate_kwargs_report(**kwargs)

        kwargs["filter"]["sort"] = kwargs.get("filter").get("sort", -1)
        kwargs["type"] = kwargs.get("type", "detailed")

        payload = json.dumps(kwargs, indent=2)
        return self.post("reports/", payload=payload)

    def delete(self, resource: str):
        url = "{base_url}{resource}".format(
            base_url=FouryouseeAPI.url,
            resource=resource,
        )
        headers = {
            "Content-Type": "application/json",
            "Secret-Token": self.token,
        }
        time.sleep(1)
        response = requests.delete(url, headers=headers)
        if not response.ok:
            raise Exception(response.text)
        else:
            return True

    def delete_upload(self, spec_id: str):
        """
        Delete one upload of the 4YouSee account.

        :param spec_id: Id of a single upload.
        :type spec_id: str, required
        :return: True in case the upload was deleted successfully
                or False in case the upload was not deleted.
        :rtype: bool

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        >>> my.delete_upload('00fa6bba3bb250012278ae03754ad1bb')
        True
        >>> my.delete_upload('123456789abcdefghijklmnopqrstyvwxyz') # If doesn't exists
        False

        """
        if not spec_id:
            raise Exception("Missing id of the upload.")

        try:
            if self.get_uploads(id=spec_id):
                return self.delete("uploads/{}".format(spec_id))
            else:
                raise Exception(f"Upload with ID {spec_id} was not found")
        except Exception:
            raise Exception(f"Upload with ID {spec_id} was not found")

    def delete_media(self, spec_id: int):
        """
        Delete one media of the 4YouSee account.

        :param spec_id: Id of a single media.
        :type spec_id: int, required
        :return: True in case the media was deleted successfully
                or False in case the media was not deleted.
        :rtype: bool

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        >>> my.delete_media(15)
        True
        >>> my.delete_media(123_456)  # If doesn't exists
        False


        **Advanced Usage**

        - Deleting all the zip files of the account

        >>> my.get_medias()
        >>> for media in c.medias:
        ...    if media['file'].endswith('zip'):
        ...        my.delete_media(media['id'])
        """
        if not spec_id:
            raise Exception("Missing id of the media.")

        try:
            if self.get_medias(id=spec_id):
                return self.delete("medias/{}".format(spec_id))
        except Exception:
            raise Exception(f"Media with ID {spec_id} was not found")

    def delete_player(self, spec_id: int):
        """
        Delete one player of the 4YouSee account.

        :param spec_id: Id of a single player.
        :type spec_id: int, required
        :return: True in case the player was deleted successfully
                or False in case the player was not deleted.
        :rtype: bool

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        >>> my.delete_player(15)
        True
        >>> my.delete_player(123_456) # If doesn't exists
        False


        **Advanced Usage**

        >>> my.get_medias(categoryId=10)
        """
        if not spec_id:
            raise Exception("Missing id of the player.")

        try:
            if self.get_players(id=spec_id):
                return self.delete("players/{}".format(spec_id))
        except Exception:
            raise Exception(f"Player with ID {spec_id} was not found")

    def delete_playlist(self, spec_id: int):
        """
        Delete one playlist of the 4YouSee account.

        :param spec_id: Id of a single playlist.
        :type spec_id: int, required
        :return: True in case the playlist was deleted successfully
                or False in case the playlist was not deleted.
        :rtype: bool

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        >>> my.delete_playlist(15)
        True
        >>> my.delete_playlist(123_456) # If doesn't exists
        False


        **Advanced Usage**

        >>> my.get_medias(categoryId=10)
        """
        if not spec_id:
            raise Exception("Missing id of the player.")

        try:
            if self.get_playlists(id=spec_id):
                return self.delete("playlists/{}".format(spec_id))
        except Exception:
            raise Exception(f"Playlist with ID {spec_id} was not found")

    def edit(self, resource: str, payload=None):
        url = "{base_url}{resource}".format(
            base_url=FouryouseeAPI.url, resource=resource
        )
        headers = {
            "Content-Type": "application/json",
            "Secret-Token": self.token,
        }
        time.sleep(1)
        response = requests.put(url, headers=headers, data=payload)
        if not response.ok:
            raise Exception(response.text)
        return json.loads(response.text)

    def edit_media(self, **kwargs):
        """

        Update an existing media.

        :param id: Id of a media.
        :type id: int, required
        :param name: name for the media.
        :type name: str, optional
        :param file: Used only to replace the file media.
                To update the source file of the you need to
                create a upload a file first.
        :type file: dict, optional
        :param duration: duration of Media, used only
                by zip or images files.
        :type duration: int, optional
        :param categories: list of categories which
                this Media is gonna be associated.
        :type categories: list of int, optional
        :param schedule: Scheduling information.
        :type schedule: dict
        :return: Dict that depicts the media edited.
        :rtype: dict

        **Usage**

        Once "**my**" object has been created. You can execute the next:

        Replacing the file media of the content with the `55` id. Only will
        change the param that you send.

        >>> my.edit_media(id=55,
        ...              file={
        ...                     "id": "dce17a1a5949768a82dd8bedd2ee525d",
        ...                     "filename": "video.mp4"
        ...                   })
        {
           "id":55,
           "name":"SEFESO_",
           "file":"https://4usee.com/****-*****/****/common/videos/i_55.mp4",
           "duration":20,
           "schedule":{
              "startDate":"None",
              "endDate":"None",
              "times":[ ]
           },
           "categories":[ 27 ]
        }

        Changing the name of a media, categories and part of the
        schedule information

        >>> my.get_media(id=99)
        {
           "id":99,
           "name":"Noticia museo del carnaval",
           "description":"Noticia museo del carnaval",
           "file":"i_99.mp4",
           "durationInSeconds":15,
           "categories":[
                { "id":2, "name":"Sample name via API" }
           ],
           "schedule":{
              "startDate":"None",
              "endDate":"None",
              "times": [ ]
           }
        }
        >>> my.edit_media(id=99, name='New name',
        ...               categories=[11, 12, 13],
        ...                schedule={'startDate': '2022-05-01', 'endDate': '2022-05-31'})
        {
           "id":99,
           "name":"New name",
           "file":"https://4usee.com/****-*****/****/common/videos/i_99.mp4",
           "duration":15,
           "schedule":{
              "startDate":"2022-05-01",
              "endDate":"2022-05-31",
              "times":[ ]
           },
           "categories":[ 11, 12, 13 ]
        }
        >>> my.get_medias(id=99)
        {
           "id":99,
           "name":"New name",
           "description":"New name",
           "file":"i_99.mp4",
           "durationInSeconds":15,
           "categories":[
              { "id":11, "name":"Cliente 1" },
              { "id":12, "name":"Cliente 2" },
              { "id":13, "name":"Cliente 3" }
           ],
           "schedule":{
              "startDate":"2022-05-01",
              "endDate":"2022-05-31",
              "times":[ ]
           }
        }

        **Advanced Usage**

        - Edit the duration of all the zip files of the account

        >>> my.get_medias()
        >>> for media in c.medias:
        ...    if media['file'].endswith('zip'):
        ...        my.edit_media(id=media['id'], duration=15)
        """
        if not kwargs:
            raise Exception("Missing Fields")

        spec_id = kwargs.get("id", False)
        if not spec_id:
            raise Exception("Missing ID of the media field.")

        media = self.get_medias(id=spec_id)
        mdia = brief_media(media)

        kwargs["name"] = kwargs.get("name", mdia["name"])
        kwargs["duration"] = kwargs.get("duration", mdia["duration"])
        kwargs["categories"] = kwargs.get("categories", mdia["categories"])
        kwargs["schedule"] = kwargs.get("schedule", mdia["schedule"])

        del kwargs["id"]
        payload = json.dumps(kwargs, indent=2)
        return self.edit("medias/{}/".format(spec_id), payload=payload)

    def edit_category(self, **kwargs):
        """
        It is possible update name, description and/or parent of category.

        :param name: Id of the media category to be edited.
        :type name: str, optional
        :param name: Category/subcategory display name.
        :type name: str, optional
        :param description: Detailed category description.
        :type description: str, optional
        :param parent:  When present it convert category in subcategory
                of category informed parent. If the value is
                null, it  converts the subcategory into a first level
                category.
        :type parent: int, optional
        :return: Dict that depicts the modified media.
        :rtype: dict

        **Usage**

        Once “**my**” object has been created. You can execute the next:

        Changing the name and description.

        >>> my.edit_category(id=52, name='Category #52', description='Info of category #52')
        {
          "id": 52,
          "name": "Category #52",
          "description": "Info of category #52",
          "parent": null,
          "children": [],
          "carouselThumbnail": null,
          "autoShuffle": false,
          "updateFlow": "1",
          "sequence": []
        }

        Changing the parent

        >>> my.edit_category(id=52, parent=53)
        {
          "id": 52,
          "name": "Category #52",
          "description": "Info of category #52",
          "parent": {
            "id": 53,
            "name": "sample media category",
            "description": null,
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
            raise Exception("Missing Fields")

        spec_id = kwargs.get("id", False)
        if not spec_id:
            raise Exception("Missing ID of the category field.")

        del kwargs["id"]
        payload = json.dumps(kwargs, indent=2)
        return self.edit(
            "medias/categories/{}".format(spec_id), payload=payload
        )

    def edit_multiple_categories(self, *args):
        """
        Update bulk category.
        It is possible to update name, description, parent and sequence for
        multiple categories. You can pass more than one dict with the
        next params

        :param name: Category display name.
        :type id: int, required
        :param name: Category display name.
        :type name: str, optional
        :param description: Detailed category description.
        :type description: str, optional
        :param parent: When present it convert category in subcategory
                of category informed parent. If the value is null,
                it converts the subcategory into a first level category.
        :type parent: int or null, optional
        :param sequence: This array must contain all content
                ids associated to each category in each item. The order of these
                ids in the array is the order they will appear in the carousel
        :type sequence: list[int], optional
        :return: Dict that depicts the media categories edited
        :rtype: dict

        ***Usage**

        Once “**my**” object has been created. You can execute the next:

        Changing name, description, parent and sequence

        >>> my.edit_multiple_categories({
        ...                                 "id": 11,
        ...                                 "name": "Category #11",
        ...                                 "description": "Description for category 11",
        ...                                 "parent": 10,
        ...                                 "sequence": [ 99, 1, 230 ]
        ...                             },
        ...                             {
        ...                                 "id": 12,
        ...                                 "name": "Category #12",
        ...                                 "description": "Description for category 12",
        ...                                 "sequence": [ 99, 230 ]
        ...                             })
        {
          "carouselItems": [
            {
              "id": 11,
              "name": "Category #11",
              "description": "Description for category 11",
              "parent": {
                "id": 10,
                "name": "Proveedor X",
                "description": "",
                "carouselThumbnail": null,
                "autoShuffle": false,
                "updateFlow": "1"
              },
              "children": [],
              "carouselThumbnail": null,
              "autoShuffle": false,
              "updateFlow": "1",
              "sequence": [ 99, 1, 230 ]
            },
            {
              "id": 12,
              "name": "Category #12",
              "description": "Description for category 12",
              "parent": {
                "id": 10,
                "name": "Proveedor X",
                "description": "",
                "carouselThumbnail": null,
                "autoShuffle": false,
                "updateFlow": "1"
              },
              "children": [],
              "carouselThumbnail": null,
              "autoShuffle": false,
              "updateFlow": "1",
              "sequence": [ 99, 230 ]
            }
          ]
        }

        """
        if not args:
            raise Exception("Missing Fields")

        for i in args:
            if not isinstance(i, dict):
                raise Exception(f"Invalid dict {i}")

        payload = json.dumps({"carouselItems": args}, indent=2)
        return self.edit("medias/categories/bulk", payload=payload)

    def edit_player(self, **kwargs):
        """
        Update a Player by id. When a param is not sent,
         it will recognize the current values of the player
          in the 4yousee account.

        :param id: Id o the player.
        :type id: int, required
        :param name: Player display name.
        :type name: str, optional
        :param description: Detailed player description.
        :type description: str, optional
        :param platform: Platform where the 4yousee player will be
                executed. **Ex**. **4YOUSEE_PLAYER** or **SAMSUNG**
                or **ANDROID** ou **LG**
        :type platform: str, required
        :param group: Id of a group of players.
        :type group: int, optional
        :param playlists: Dict with 7 keys and 7 values. Every key
                depicts the number of the day (starting from 0)
                and every value the playlist id.
        :type playlists: dict, optional
        :param audios: A dict with “0” as his only key and a value
                that depicts the id of the audio playlist.
        :type audios: dict, optional
        :return: Dict that depicts the player edited
        :rtype: dict


        **Usage**

        Once “my” object has been created. You can execute the next:

        Changing the name, platform and playlist

        >>> my.edit_player(id=2, name='New player name',
        ...                platform='SAMSUNG',
        ...                playlists={ "0": 40, "1": 40, "2": 40, "3": 40, "4": 40, "5": 40, "6": 40 })
        {
          "id": 2,
          "name": "New player name",
          "description": "Description from API",
          "platform": "SAMSUNG",
          "lastContactInMinutes": 998,
          "group": { "id": 2, "name": "Clientes Barrio Sur" },
          "playerStatus": {
            "id": 4,
            "name": "Assistance needed",
            "time": 1440
          },
          "playlists": {
            "0": { "id": 40, "name": "Player name example" },
            "1": { "id": 40, "name": "Player name example" },
            "2": { "id": 40, "name": "Player name example" },
            "3": { "id": 40, "name": "Player name example" },
            "4": { "id": 40, "name": "Player name example" },
            "5": { "id": 40, "name": "Player name example" },
            "6": { "id": 40, "name": "Player name example" }
          },
          "audios": {
            "0": { "id": 1, "name": "Contenido Vertical" }
          },
          "lastLogReceived": "2022-07-01 18:00:37"
        }

        .. warning:: It'll raise this exception `Exception: {"message":"Can not
            update an inactive player"}` if the license hasn't been actived.

        """
        # Validators
        spec_id = kwargs.get("id", False)
        if not spec_id:
            raise Exception("Missing ID of the player field.")
        validate_kwargs_player(**kwargs)

        player_existent = self.get_players(id=spec_id)
        plyer = brief_player(player_existent)

        kwargs["name"] = kwargs.get("name", plyer["name"])
        kwargs["description"] = kwargs.get("description", plyer["description"])
        kwargs["group"] = kwargs.get("group", plyer["group"])
        kwargs["platform"] = kwargs.get("platform", plyer["platform"])
        kwargs["playlists"] = kwargs.get("playlists", plyer["playlists"])
        kwargs["audios"] = kwargs.get("audios", plyer["audios"])

        if len(kwargs.get("name")) > 50:
            kwargs["name"] = kwargs["name"][:46] + "..."

        del kwargs["id"]
        payload = json.dumps(kwargs, indent=2)
        return self.edit("players/{}".format(spec_id), payload=payload)

    def edit_playlist(self, **kwargs):
        """
        Update a Playlist by id.

        :param name: Playlist display name.
        :type name: str, required
        :param isSubPlaylist: Default value is False.
        :type isSubPlaylist: bool, optional
        :param category: Id of category of playlists.
        :type category: int, optional
        :param items: Items that the playlist will content
        :type items: list of dicts, required
        :param sequence: Sequence of execution of the items.
        :type sequence: list, required
        :return: Dict that depicts the playlist modified.
        :rtype: dict

        **Usage**

        Once “**my**” object has been created. You can execute the next:

        Changing the name.

        >>> my.edit_playlist(id=75, name='Changing playlist name')
        {
          "id": 75,
          "name": "Changing playlist name",
          "durationInSeconds": 20,
          "isSubPlaylist": false,
          "category": null,
          "items": [
            {
              "type": "media",
              "id": 117,
              "name": "Cielo_Nuevo_",
              "file": "i_117.mp4",
              "durationInSeconds": 20,
              "categories": [
                { "id": 27, "name": "random_" }
              ]
            }
          ],
          "sequence": [ 0 ]
        }

        Adding a item to the playlist

        >>> my.edit_playlist(id=75, items=[
        ...                                 { 'type': 'media', 'id': 117 },
        ...                                 { 'type': 'media', 'id': 228 },
        ...                               ],
        ...                  sequence=[0,1])
        {
          "id": 75,
          "name": "Changing playlist name",
          "durationInSeconds": 146,
          "isSubPlaylist": false,
          "category": null,
          "items": [
                    {
                      "type": "media",
                      "id": 117,
                      "name": "Cielo_Nuevo_",
                      "file": "i_117.mp4",
                      "durationInSeconds": 20,
                      "categories": [
                        { "id": 27, "name": "random_" }
                      ]
                    },
                    {
                      "type": "media",
                      "id": 228,
                      "name": "sample-mp4-file",
                      "file": "i_228.mp4",
                      "durationInSeconds": 126,
                      "categories": [
                        { "id": 1, "name": "DEMO" }
                      ]
                    }
                  ],
          "sequence": [ 0, 1 ]
        }

        Deleting a media of the playlist and adding two carousels

        >>> my.edit_playlist(id=75, items=[
        ...                                 { 'type': 'media', 'id': 117 },
        ...                                 { 'type': 'carousel', 'id': 8 },
        ...                                 { 'type': 'carousel', 'id': 9 },
        ...                               ]
        ...                  sequence=[0,1])
        {
          "id": 75,
          "name": "Changing playlist name",
          "durationInSeconds": 20,
          "isSubPlaylist": false,
          "category": null,
          "items": [
            {
              "type": "media",
              "id": 117,
              "name": "Cielo_Nuevo_",
              "file": "i_117.mp4",
              "durationInSeconds": 20,
              "categories": [
                { "id": 27, "name": "random_" }
              ]
            },
            {
              "type": "carousel",
              "id": 25,
              "name": "Jornada Madrugada 12am-8am",
              "items": [],
              "sequence": []
            },
            {
              "type": "carousel",
              "id": 14,
              "name": "Cliente 4",
              "items": [],
              "sequence": []
            }
          ],
          "sequence": [ 0, 1, 2 ]
        }

        **Advanced Usage**

        - Duplicating a playlist

        >>> existent_plist = my.get_playlists(id=75)
        >>> new_items = [{'type': item['type'], 'id': item['id']} for item in existent_plist['items']]
        >>> my.add_playlist(name=existent_plist['name'], items=new_items, sequence=existent_plist['sequence'])
        {
          "id": 90,
          "name": "Changing playlist name",
          "durationInSeconds": 20,
          "isSubPlaylist": false,
          "category": null,
          "items": [
            {
              "type": "media",
              "id": 117,
              "name": "Cielo_Nuevo_",
              "file": "i_117.mp4",
              "durationInSeconds": 20,
              "categories": [
                { "id": 27, "name": "random_" }
              ]
            },
            {
              "type": "carousel",
              "id": 25,
              "name": "Jornada Madrugada 12am-8am",
              "items": [],
              "sequence": []
            },
            {
              "type": "carousel",
              "id": 14,
              "name": "Cliente 4",
              "items": [],
              "sequence": []
            }
          ],
          "sequence": [ 0, 1, 2 ]
        }
        
        - Removing empty carousels from a playlist
        
        >>> plist = my.get_playlists(id=75)
        >>> empty_car = False
        >>> print(f"Analisando playlist \"{plist['id']} - {plist['name']}\"")
        >>> idx = 0
        >>> while idx <= len(plist['items']):
                try:
                    if plist['items'][idx]['type'] == 'carousel' and not plist['items'][idx]['sequence']:
                        empty_car = True
                        print("\tCarousel excluido : \"{} - {}\"".\
                                                  format(plist['items'][idx]['id'],
                                                         plist['items'][idx]['name']))
                        del plist['items'][idx]
                        plist['sequence'] = list(filter(lambda s: s != idx, plist['sequence']))
                        plist['sequence'] = list(map(lambda seq: seq - 1 if seq > idx else seq, plist['sequence']))
                    else:
                        idx += 1
                except IndexError:
                    break
         >>> if empty_car:
                try:
                    new_items = []
                    for item in plist['items']:
                        if item['type'] in ['videoWall', 'news']:
                            new_items.append(item)
                        else:
                            new_items.append({'type': item['type'], 'id': item['id']})
                    my.edit_playlist(id=plist['id'],
                                     items=new_items,
                                     sequence=plist['sequence'])
                    print(f"\tPlaylist \"{plist['id']} - {plist['name']}\" atualizada!")
                except Exception as e:
                    print(f"\tNão foi possível atualizar playlist \"{plist['id']} - {plist['name']}\"\n\tError : {e}")
            else:
                print(f"\tPlaylist \"{plist['id']} - {plist['name']}\" não tem carroseis vazíos")


        .. warning:: The previous piece of code doesn't consider a playlist with videowalls.

        """

        # Validators
        spec_id = kwargs.get("id", False)
        if not spec_id:
            raise Exception("Missing ID of the playlist field.")
        validate_kwargs_playlist(**kwargs)

        playlist_existent = self.get_playlists(id=spec_id)
        plist = brief_playlist(playlist_existent)

        kwargs["name"] = kwargs.get("name", plist["name"])
        kwargs["isSubPlaylist"] = kwargs.get(
            "isSubPlaylist", plist["isSubPlaylist"]
        )
        kwargs["category"] = kwargs.get("category", plist["category"])
        kwargs["items"] = kwargs.get("items", plist["items"])
        kwargs["sequence"] = kwargs.get("sequence", plist["sequence"])

        if len(kwargs.get("name")) > 40:
            kwargs["name"] = kwargs["name"][:36] + "..."

        del kwargs["id"]
        payload = json.dumps(kwargs, indent=2)
        return self.edit("playlists/{}".format(spec_id), payload=payload)


def myme_type(file: Path) -> str:
    """Retorn mimetypes information"""
    return mimetypes.guess_type(file)[0].replace(
        "application/x-zip-compressed", "application/zip"
    )


def filter_id(input_id: str or int, iterable: list) -> list:
    """Filter a iterable accordding to an input id value"""
    return list(filter(lambda i: i["id"] == input_id, iterable))


def brief_player(player: dict) -> dict:
    """Receive a player object an return the information required
    to the payload"""
    return dict(
        name=player["name"],
        description=player["description"],
        group=player["group"]["id"],
        platform=player["platform"],
        playlists={
            str(k): v["id"] for k, v in enumerate(player["playlists"].values())
        },
        audios={}
        if not player["audios"]["0"]
        else {"0": player["audios"]["0"]["id"]},
    )


def brief_playlist(playlist: dict) -> dict:
    """Receive a playlist object an return the information required
    to the payload"""
    return dict(
        name=playlist["name"],
        isSubPlaylist=playlist["isSubPlaylist"],
        category=playlist["category"]["id"] if playlist["category"] else None,
        items=playlist["items"],
        sequence=playlist["sequence"],
    )


def brief_media(media: dict) -> dict:
    """Receive a media object an return the information required
    to the payload"""
    return dict(
        name=media["name"],
        duration=media["durationInSeconds"],
        categories=[i["id"] for i in media["categories"]],
        schedule=media["schedule"],
    )


def validate_kwargs_single_media(**kwargs) -> Exception or None:
    """Validate the kwargs sent to the post_single_media function"""
    if not kwargs.get("file"):
        raise Exception("Missing 'file' field.")

    if not kwargs.get("categories"):
        raise Exception("Missing 'categories' field.")

    file = Path(kwargs.get("file"))
    if not file.exists():
        raise Exception("File not found.")
    mimetype = myme_type(file)
    type, extension = mimetype.split("/")
    if mimetype not in [
        "video/mp4",
        "image/jpeg",
        # 'image/gif',
        "image/png",
        "application/zip",
    ]:
        raise Exception("Invalid file.")
    if mimetype in ["image/jpeg", "image/png", "application/zip"]:
        if not kwargs.get("duration"):
            raise Exception(
                "Missing 'duration' field. This must "
                "be an integer that depicts "
                "the duration of the file in the playlist."
            )
        elif not isinstance(kwargs.get("duration"), int):
            raise Exception("Invalid duration")
    if kwargs.get("category"):
        raise Exception("Invalid param must be 'categories'.")


def validate_kwargs_single_media_category(**kwargs) -> Exception or None:
    """Validate the kwargs sent to the add_media_category function"""
    if not kwargs.get("name"):
        raise Exception("Missing 'name' field.")

    if parent := kwargs.get("parent"):
        if not isinstance(parent, int):
            raise Exception("Invalid parent, must be an integer")

    if shuffle := kwargs.get("autoShuffle"):
        if not isinstance(shuffle, bool):
            raise Exception("Invalid parent, must be True o False")

    if updateflow := kwargs.get("updateFlow"):
        if updateflow not in [1, 2]:
            raise Exception("Invalid updateFlow, must be 1 or 2")

    if sequence := kwargs.get("sequence"):
        if not isinstance(sequence, list):
            raise Exception("Invalid sequence, must be a list")


def validate_kwargs_player(**kwargs) -> Exception or None:
    """Validate the kwargs sent to the add_player function"""

    if playlists := kwargs.get("playlists"):
        if not isinstance(playlists, dict) and list(playlists.keys()) != [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
        ]:
            raise Exception("Invalid playlists field")

    if platform := kwargs.get("platform"):
        if not isinstance(platform, list) and platform not in [
            "SAMSUNG",
            "WINDOWS",
            "ANDROID",
            "4YOUSEE_PLAYER",
            "LG",
        ]:
            raise Exception("Invalid platform field")

    if audios := kwargs.get("audios"):
        if not isinstance(audios, dict) and list(audios.keys()) != ["0"]:
            raise Exception("Invalid audios field")


def validate_kwargs_playlist(**kwargs) -> Exception or None:
    """Validate the kwargs sent to the add_playlist function"""
    if isSubPlaylist := kwargs.get("isSubPlaylist"):
        if not isinstance(isSubPlaylist, bool):
            raise Exception("Invalid isSubPlaylist field")

    if category := kwargs.get("category"):
        if not isinstance(category, int):
            raise Exception("Invalid category field")

    if items := kwargs.get("items"):
        if not isinstance(items, list):
            raise Exception("Invalid items field")

    if sequence := kwargs.get("sequence"):
        if not isinstance(sequence, list):
            raise Exception("Invalid sequences field")


def validate_kwargs_report(**kwargs) -> Exception or None:
    """Validate the kwargs sent to the request_report function"""
    if filter := kwargs.get("filter"):
        if not isinstance(filter, dict):
            raise Exception("Invalid audios field")

        if mediaId := kwargs.get("mediaId"):
            if not isinstance(mediaId, list):
                raise Exception("Invalid mediaId field")

        if playerId := kwargs.get("playerId"):
            if not isinstance(playerId, list):
                raise Exception("Invalid playerId field")

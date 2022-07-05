<h2 align = 'center'>
Python 4YouSee Manager API Wrapper
</h2>


## <div align = 'center'> <img src="https://badge.fury.io/py/fouryousee.svg" alt="PyPI version"> <img src="https://github.com/Alfareiza/4yousee/workflows/Pytests/badge.svg" /> <img alt="GitHub" src="https://img.shields.io/github/license/Alfareiza/4yousee?label=License">  <img src='https://img.shields.io/pypi/pyversions/fouryousee.svg?label=Python&logo=python&logoColor=white' alt='Compatible Versions' /> <img alt="Codecov" src="https://img.shields.io/codecov/c/github/Alfareiza/4yousee?color=f01f7a&label=Coverage&logo=codecov&logoColor=white&token=LN9T2JYAFN"> <img src='https://readthedocs.org/projects/fouryousee/badge/?version=latest' alt='Documentation Status' target='http://fouryousee.readthedocs.io' /> <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/fouryousee?label=Downloads" target='http://fouryousee.readthedocs.io' /> </div>


This library is a Python wrapper around the [4YouSee](https://docs.4yousee.com/api/) REST API.

Requires Python 3.8 or later.

#### Source code

https://github.com/Alfareiza/4yousee

#### Documentation

https://fouryousee.readthedocs.io/

Getting Started
---------------

To use the Python API, first install it from PyPI using `pip`, then execute:

    pip install fouryousee
    
Once you have it installed, get an API key from [How to get a Token to integrate with the API of 4YouSee Manager](https://suporte.4yousee.com.br/en/support/solutions/articles/72000532960-how-to-get-a-token-to-integrate-with-the-api-of-4yousee-manager). If this link is broken feel free to contact to suporte@4yousee.com.br

    >>> from fouryousee.fouryousee import FouryouseeAPI
    >>> client = FouryouseeAPI(TOKEN_APP_KEY)
    >>> client.get_players()
    [{'id': 1, 'name': 'Player DEMO', 'description': 'Ponto de demonstração disponibilizado na instalação do 4YouSee Manager.Player demo available on  4YouSee Manager installation.', 'platform': 'ANDROID', 'lastContactInMinutes': 210796, 'group': {'id': 1, 'name': 'Group DEMO'}, 'playerStatus': {'id': 5, 'name': 'Local assist needed', 'time': 9999999}, 'playlists': {'0': {'id': 3, 'name': 'Novo'}, '1': {'id': 3, 'name': 'Novo'}, '2': {'id': 3, 'name': 'Novo'}, '3': {'id': 3, 'name': 'Novo'}, '4': {'id': 3, 'name': 'Novo'}, '5': {'id': 3, 'name': 'Novo'}, '6': {'id': 3, 'name': 'Novo'}}, 'audios': {'0': {'id': 1, 'name': 'Contenido Vertical'}}, 'lastLogReceived': '2022-01-26 13:49:28'}, {'id': 2, 'name': '2Outputs', 'description': '', 'platform': '4YOUSEE_PLAYER', 'lastContactInMinutes': 413, 'group': {'id': 3, 'name': 'Clientes Barrio Sur A'}, 'playerStatus': {'id': 4, 'name': 'Assistance needed', 'time': 1440}, 'playlists': {'0': {'id': 70, 'name': 'Test 4uc'}, '1': {'id': 70, 'name': 'Test 4uc'}, '2': {'id': 70, 'name': 'Test 4uc'}, '3': {'id': 70, 'name': 'Test 4uc'}, '4': {'id': 70, 'name': 'Test 4uc'}, '5': {'id': 70, 'name': 'Test 4uc'}, '6': {'id': 70, 'name': 'Test 4uc'}}, 'audios': {'0': None}, 'lastLogReceived': '2022-06-21 13:11:38'}]


Once you have set the user's token, all calls to the API will include that token, as if the user was logged in.

### Advance Usage

#### How to get the actives medias

Active medias are those content who is associated to a player. So, let's suppose, we have an iterable with the playlists id, called `active_playlists`

```pyhon
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
[1, 3, 4, 8, 19, 20, 28, 30, 32, 33, 38, 39, 40, 45, 48, 49, 50, 53, 54, 55, 56, 57, 66, 69, 80, 99, 100, 101]
```





## Author

Alfonso AG - <alfareiza@gmail.com>

New contributers and pull requests are welcome.

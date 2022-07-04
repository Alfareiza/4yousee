<h2 align = 'center'>
Python 4YouSee Manager API Wrapper
</h2>


## <div align = 'center'><img src="https://badge.fury.io/py/fouryousee.svg" alt="PyPI version"> <img alt="GitHub" src="https://img.shields.io/github/license/Alfareiza/4yousee?label=License"> <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/fouryousee?label=Downloads"> <img src='https://readthedocs.org/projects/fouryousee/badge/?version=latest' alt='Documentation Status' /></div>

This library is a Python wrapper around the [4YouSee](https://docs.4yousee.com/api/) REST API.

Requires Python 3.7 or later.


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


## Author

Alfonso AG - <alfareiza@gmail.com>

New contributers and pull requests are welcome.

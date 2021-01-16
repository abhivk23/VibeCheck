
import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests

from exceptions import ResponseException
from secrets import spotify_token, spotify_user_id

class CreatePlaylist:
    def __init__(self):
        
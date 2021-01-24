## vibecheck -- music for the moment

## Quickstart

First fork or 'git clone https://github.com/abhivk23/VibeCheck' to your local system. To set the necessary environment variables at once, navigate to './env/lib/python3.7/site-packages' and create a path file (e.g. '_set_envs.pth'). Edit the file to store API keys in the following format (write everything on the same line):

```python
import os ; os.environ['API_ID_1']='API_KEY_1'; os.environ['API_ID_2']='API_KEY_2'; os.environ['API_ID_2']='API_KEY_2'; ... 
```

Now when the virtual environment is activated, your API keys will be available through your virtual environment variables. Activate the virtual environment from the root with 'source env/bin/activate'. This will install all necessary Python3.7 dependencies. 

Now you should be able to run the application in the virtual environment with 'python3 client.py'.

## Inspiration

As three Spotify (and one Apple Music) lovers, music is deeply personal. Whether it’s a study sesh, a drive downtown, or a good time on a Friday night, we’re always searching for the perfect song, artist, or playlist -- the perfect vibe. We created vibecheck as a fun, simple way to bring our conversations and emotions into a custom, curated playlist fit for any moment. 

vibecheck is an application that converts voice call input into a curated music playlist. Based on the conversation, the application generates text and determines the emotion it holds. vibecheck correlates these sentiments to music by relating emotions like happiness, sadness, or “chill” to music features like beat and danceability. Based on the captured “vibe”, the application generates a playlist fit for the occasion or interaction.

## Successes

## Areas for Improvement

## Featured Tech.

- Audio Input/Processing with Vonage API and Node server
- Sentiment analysis with Google Cloud Speech-to-Text and Natural Language APIs
- Song recommendation and playlist generation with 'SpotiPy' a Spotify Python Web API interface

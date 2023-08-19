#BEFORE RUNNING THIS MAKE SURE TO RUN pip install -r requirements.txt 
#AND GET ALL OF THE REQUIRED API KEYS AND FILES

#CURRENTLY CREATES THE VIDEO IN A FORMAT THAT WILL UPLOAD AS A YOUTUBE SHORT

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from gtts import gTTS
import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from PIL import Image
import numpy as np
import requests
import os


#Keys and function for getting images from Pexels
API_KEY = 'Pexel API key goes here.'
SEARCH_QUERY = 'IMG search query goes here'
PER_PAGE = 4 #Change this number for amount of pictures wanted (be careful for API limits)
URL = f'https://api.pexels.com/v1/search?query={SEARCH_QUERY}&per_page={PER_PAGE}'

headers = {
    'Authorization': API_KEY
}

#Function for getting images
def get_images():
  response = requests.get(URL, headers=headers)
  data = response.json()
  
  # Create a directory to save the images
  if not os.path.exists("downloaded_images"):
      os.makedirs("downloaded_images")

  # Save images to the downloaded_images directory
  for index, photo in enumerate(data['photos']):
      img_url = photo['src']['original']
      response = requests.get(img_url)
      
      with open(f"downloaded_images/image_{index+1}.jpg", "wb") as file:
          file.write(response.content)

# Function for getting the TTS audio file (For changing voice look at gTTS documentation)
def text_to_speech(text, output_audio_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_audio_file)

# Function for creating the video
def create_video_from_images(audio_path, image_paths, output_video):
    audio = AudioFileClip(audio_path)
    img_duration = audio.duration / len(image_paths)
    
    # Resize the images to have a 9:16 aspect ratio for YouTube Shorts
    clips = []
    for img in image_paths:
        pil_image = Image.open(img)

        # Calculate target dimensions while keeping aspect ratio
        base_width, base_height = pil_image.size
        aspect_ratio = base_width / base_height
        target_aspect_ratio = 9 / 16
        
        if aspect_ratio > target_aspect_ratio:
            new_height = 1920
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = 1080
            new_height = int(new_width / aspect_ratio)
        
        pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)

        left_margin = (new_width - 1080) / 2
        top_margin = (new_height - 1920) / 2
        pil_image = pil_image.crop((left_margin, top_margin, left_margin + 1080, top_margin + 1920))

        img_clip = ImageClip(np.array(pil_image)).set_duration(img_duration)
        clips.append(img_clip)
    
    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)
    video.write_videofile(output_video, codec='libx264', fps=24)

# YouTube Upload
#You will need to get the client secrets file (will be a .json) on
#googleapis and a token.pickle file
CLIENT_SECRETS_FILE = "Put Youtube API v3 Client Secrets file path here" 
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    creds = None
    
    # Check if token.pickle exists.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, initiate the OAuth2 flow.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run.
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                
    discovery_service_url = "https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest"
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds, discoveryServiceUrl=discovery_service_url)


#Function for uploading the video
def upload_video(youtube, file_path, title="Put video title here", description="Put video description here", category=22, keywords=[]):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': keywords,
            'categoryId': str(category)
        },
        'status': {
            'privacyStatus': 'unlisted'  
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype='video/*')
    request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if 'id' in response:
            print(f'Video uploaded with ID {response["id"]}')
        else:
            exit(f'The upload failed with an unexpected response: {response}')

if __name__ == '__main__':
    # Convert script to speech
    script = "Put script here."
    audio_output = "audio_output.mp3"
    text_to_speech(script, audio_output)

    #Get images from Pexel based on given query
    get_images()
    
    # Create video
    image_paths = ['downloaded_images/image_1.jpg', 'downloaded_images/image_2.jpg', 'downloaded_images/image_3.jpg', 'downloaded_images/image_4.jpg']
    video_output = 'output_short.mp4'
    create_video_from_images(audio_output, image_paths, video_output)

    # Upload to YouTube
  
    #YOUTUBE ONLY ALLOWS UPLOADS FROM THE API TO BE LISTED AS PUBLIC ON YOUTUBE
    #IF THE APP IS VERFIED THROUGH GOOGLE, SO THIS VIDEO WILL BE UPLOADED AS PRIVATE
    #UNLESS YOU GET VERIFIED BY GOOGLE
  
    youtube = get_authenticated_service()
    upload_video(youtube, video_output, title="Video title here", description="Video description here")
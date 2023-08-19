# youtube-short-creator
Description: This program will attain pictures and a text-to-speech version of an inputted script and create a slideshow video with the provided script overlayed.

Instructions: 
- First, run "pip install -r requirements.txt" to install all required dependencies for the program.
  
- Then, get an API key for Pexels as well as set up a client secrets file through the Youtube API v3 (this will be a .json file).
    Instructions for getting client secrets file:
      Go to the Google Cloud Platform Console: Navigate to https://console.cloud.google.com/.
      Create a new project:
        Click on the project dropdown on the top right corner of the screen.
        Click the New Project button at the top right of the modal that appears.
        Enter a name for your project and select a billing account (if you have one), then click Create.
  
      Enable the YouTube Data API v3:
        In the Dashboard, click on the Navigation menu (three horizontal lines on the top left corner).
        Go to APIs & Services > Library.
        In the API Library, search for "YouTube Data API v3" and select it.
        Click Enable.
  
      Create API Credentials:
        After enabling the API, click on the Create Credentials button at the top.
        Choose OAuth client ID.
        If you haven't configured the OAuth consent screen yet, you'll be prompted to do so. Fill in the required details. For a test application, you can choose the External user type.
        Once the consent screen is set up, go back to creating the OAuth client ID.
        For Application type, select Desktop App.
        Enter a name for the client ID, then click Create.
        Download the generated client_secret_XXXX.json file. This file will contain the credentials you'll use in your application.

- Once you have the API key and client secrets file put them into the required places in the program.

- Input the search query for Pexels, number of photos wanted, and the script into the correct places.

- On first run, you will need to authenticate. Just follow the instructions that are shown during this process. (Read more on this in the notes below)

Notes: 
- Youtube API v3 does not let videos that are uploaded through the API to be set to public or unlisted unless the app being used is verified through Google. This means that any video uploaded through this program will be considered a break of the Youtube terms and policies and will be locked to private. The user can stop the program from uploaded the video to youtube by commenting out the last two lines (162 and 163). This will still create the video as intended, but the user will need to upload the video manually to ensure that it can be listed as public or unlisted.

- On first run of the program, you will be prompted for authentication for the account used to set up and attain the client secrets file mentioned in the instructions. This only needs to be done on the first run or if the token.pickle file attained from the process expires.

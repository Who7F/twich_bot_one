--------------------------------------------------
--CLIENT_ID--

-Go to Twitch Developer Console: 

https://dev.twitch.tv/
You will need two-factor authentication (2FA) enabled.


-Log in

Click the Login button at the top left.
See: clientId0001.jpg


-Register Your Application

Click Register Your Application (middle left of the screen).
(Optional) You can also find Register Your Application under the Applications tab.
See: clientId0002.jpg, (Optional) clientId0002s.jpg
Enter Application Details

Name: Enter the name of your app
OAuth Redirect URLs: http://localhost
Category: Select Chat Bot from the dropdown
Client Type: Select Confidential
See: clientId0003.jpg
📝 Note: You may not need the Client ID for your setup.


--------------------------------------------------
--ACCESS_TOKEN--


-Go to Twitch Token Generator

https://twitchtokengenerator.com/


-Select the necessary permissions

Since this is a chat bot, select:
✅ chat:read
✅ chat:edit
See: accessToken0001.jpg


-Generate Token

Scroll down and click Generate Token
Follow the instructions to link your Twitch account
See: accessToken0002.jpg
Save Your Access Token

Copy the generated access token and keep it safe. You will need this for your .env file.
See: accessToken0003.jpg


--------------------------------------------------
📂 Images are stored in the credentialsHelpImg folder

accessToken0001.jpg
accessToken0002.jpg
accessToken0003.jpg
clientId0001.jpg
clientId0002.jpg
clientId0002s.jpg
clientId0003.jpg


--------------------------------------------------
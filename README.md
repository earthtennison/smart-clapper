Sending Google Assistant Command via REST API

ref https://assistantrelay.com/docs/getting-started/installation

Installation
1. install node.js version 10.13.0 (using nvm)
nvm for window -> https://github.com/coreybutler/nvm-windows
2. install pm2 by $ npm i pm2 -g (using powershell)
3. install assistant relay by download Assistant Relay V3.2.0 release.zip -> https://github.com/greghesp/assistant-relay/releases/download/v3.2.0/release.zip
4. extract the folder and run this command inside that folder $ npm i

Config Google Account
6. Configure Develop Project (step 1 - 6) -> https://developers.google.com/assistant/sdk/guides/service/python/embed/config-dev-project-and-account
7. Go to Google Developer Console -> https://console.developers.google.com/
8. Click on the Credentials link in the left hand menu
9. At the top, click the Create Credentials button and select OAuth Client ID
10. Select Web Application from the dropdown list
11. Give your client ID a name, such as Assistant Relay. Click Create.
12. Click the Download button to download your secret_client json file.

Assistant Relay Setup
13. Modify secret_client by changing "web" key to "installed"
14. Run $ npm run start and open the Assistant Relay webpage on browser
15. Upload secret_client_xxx.json to the webpage, add yout user name and click next.
16. It will pop up the Google Account linking, authorize with your Google Account
17. It will now show the blank white page with some text on it. Copy the code in the url -> http://localhost/?code=**COPYCODEFROMHERE**&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fassistant-sdk-prototype
ref https://github.com/greghesp/assistant-relay/issues/266#issuecomment-1065940698
18. Come back to the Assistant Relay webpage, paste the code.
19. The user is added.

Test with postman
ref https://assistantrelay.com/docs/commands/broadcast
1. POST to , for example, http://192.168.1.157:3000/assistant
with the body of 
{
    "command": "turn on the fan",
    "converse": false,
    "user": "earth"
}
Note: When want to command the Device, "converse" must be false.

# Sending Google Assistant Command via REST API

Ref. [Assistant Relay Installation](https://assistantrelay.com/docs/getting-started/installation)

## Installation
1. Install node.js version 10.13.0 (using nvm)
[nvm for window](https://github.com/coreybutler/nvm-windows)
2. Install PM2 by `$ npm i pm2 -g`  (using powershell)
3. Install Assistant Relay by download [Assistant Relay V3.2.0 release.zip](https://github.com/greghesp/assistant-relay/releases/download/v3.2.0/release.zip)
4. Extract the folder and run `$ npm i` inside that folder <br>


## Config Google Account
5. Configure [Google Develop Project](https://developers.google.com/assistant/sdk/guides/service/python/embed/config-dev-project-and-account) (step 1 - 6)
6. Go to [Google Developer Console](https://console.developers.google.com/)
7. Click on the **Credentials** link in the left hand menu
8. At the top, click the **Create Credentials** button and select **OAuth Client ID**
9. Select **Web Application** from the dropdown list
10. Give your client ID a name, such as **Assistant Relay**. Click **Create**.
11. Click the **Download** button to download your secret_client json file.

## Assistant Relay Setup
12. Modify secret_client_xxx.json by changing "web" key to "installed"
13. Run `$ npm run start` and open the Assistant Relay webpage on browser
14. Upload secret_client_xxx.json to the webpage, add your user name and click next.
15. It will pop up the Google Account linking page, authorize it with your Google Account
16. It will now show the blank white page with some text on it. Copy the code in the url <br>
`http://localhost/?code=**COPYCODEFROMHERE**&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fassistant-sdk-prototype` <br>
Ref. [link](https://github.com/greghesp/assistant-relay/issues/266#issuecomment-1065940698)
17. Come back to the Assistant Relay webpage, and paste the code.
18. The user is added.

## Test with postman
Ref. [Assistant Relay Command Usage](https://assistantrelay.com/docs/commands/broadcast)
1. Command the device <br>
POST to , for example, http://192.168.1.157:3000/assistant, with the body of raw json format <br>
```
{
    "command": "turn on the fan",
    "converse": false,
    "user": "earth"
}
```
Note: When want to command the Device, "converse" must be false. <br>

2. Broadcast to Google Home device
```
{
    "command": "hello world",
    "broadcast": true,
    "user": "earth"
}
```


# Codelab 7: Lamda and API Gateway

### Overview

In this codelab you will gain experience with Lambda and API Gateway by writing a serverless Slack chat bot.
You will also gain experience with both using a third-party REST API and make your own REST endpoint. The required
steps to successfully complete this codelab can be summarized as follows:  

Part 1: Setting Up Slack Chat Bot
You will create a new Slack App and associated Bot. You will additionally generate the Oauth tokens you will need to
save in your API Gateway settings.  

Part 2: Setting Up API Gateway and Lambda  
You will begin a new instance of API Gateway and generate the single resource required to complete this codelab. You
will also drop in some test code in your lamda function to be used in `Part 3` to verify all the API requests are
successfully completing. Finally you will launch your new API endpoint.  

Part 3: Verifying Everything works!  
You will use your new API endpoint to verify a successful connection between your endpoint and Slack.

Part 4: Make your bot says something different that what you messaged it! :)  
Uncomment the code we provided you with and look for the comment that says `TODO:`. This is where you will
add some custom parsing of the message you typed in Slack to send to your bot and will be your Lamda acting in the
role of your bot.

### Due Date

This code is due on *, April  at 11:59:59PM*.

### Setup

Make sure to update your local repo with the remote by executing `git pull`. There is no need to run `pipenv install`
for this codelab.

Part 1. Setting up your Slack Chat Bot  
Open up Slack. I advise you download the desktop app version which is available for Mac, Windows and Linux. Click the plus sign next to `Apps` in the bottom left. This will open the `Browse Apps`window. Click on the wheel on the top left
corner by the `Manage Apps` text. This will open up a browser with the following url in it: `https://api.slack.com/`.
Click the green button in the center that says `Start Building`.

In the next window give your app the name `firstname_lastname_slack_bot`. This is how we will identify your submission for grading purposes. Also select which slack workspace you want this bot to be associated with. It will be one of the following, depending on which one we assigned you to:  `cmsc389lspring2018a`, `cmsc389lspring2018b` or `cmsc389lspring2018c`.

In the next view, under `Add features and functionality`, select `Bots`. Then select `Add a Bot User`.  
On the next view leave the prepopulated fields as they are. Toggle the slider to show your bot as always being online and then click the green `Add Bot User` button.  

We now need to enable event subscription. The way the chat bot will work is the following:

Users send a direct chat message to the chat-bot.  
An event representing that message is published.  
If the bot is subscribed to that type of event, a HTTP POST request, containing information about that chat message, is dispatched to a Web resource living at a given URL.  
That URL can be handled by a Web application that we can easily build using a couple of “serverless” AWS cloud technologies:

An API Gateway resource, at that URL, handles the incoming POST request.
An AWS Lambda function processes the payload of the POST request and takes an appropriate action, such as making a new request to the Slack API (e.g. to reply to the message)
Here’s an interaction diagram that illustrates what will happen each time our bot receives a direct message:  
![Architecture](../../../media/codelabs/codelab-07/codelab07-architecture.png)  

Now select `Event Subscriptions` under `Features` on the left menu. Slide `Enable Events` to `On`.  
Scroll down to `Subscribe to Bot Events`. In the text box type `message.im` and click on the event that is populated below. You should now see that you have added the `message.im` to your bot's subscription events.  

We have created our bot, subscribed it to an event, so what's left? Authorization!  
Click on `Oauth & Permissions`. The next page will ask us to add an app to our workspace. Once you authorize the bot you will receive a set of OAuth Access tokens. Copy the Bot User OAuth Access Token somewhere since you are going to
need it in API Gateway.  




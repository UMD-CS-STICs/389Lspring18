# Codelab 7: Lamda and API Gateway

### Overview

In this codelab you will gain experience with Lambda and API Gateway by writing a serverless Slack chat bot.
You will also gain experience with both using a third-party REST API and make your own REST endpoint. The required
steps to successfully complete this codelab can be summarized as follows:  

Part 1: Setting Up Slack  
You will create a new Slack App and associated Bot. You will additionally generate the Oauth tokens you will need to
save in your API Gateway settings.  

Part 2: Setting Up API Gateway and Lambda  
You will begin a new instance of API Gateway and generate the single resource required to complete this codelab. You
will also drop in some test code in your lamda function to be used in `Part 3` to verify all the API requests are
successfully completing. Finally you will launch your new API endpoint.  

Part 3: Verifying Everything works!  
You will use your new API endpoint to verify a successful connection between your endpoint and Slack.

Part 4: Make your Bot say something different :)  
Uncomment the code we provided you with and look for the comment that says `TODO:`. This is where you will
add some custom parsing of the message you typed in Slack to send to your bot and will be your Lamda acting in the
role of your bot.

### Due Date

This code is due on *, April  at 11:59:59PM*.

### Setup

Make sure to update your local repo with the remote by executing `git pull`. There is no need to run `pipenv install`
for this codelab.

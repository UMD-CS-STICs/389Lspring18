# Codelab 7: Lambda and API Gateway

### Overview

In this codelab you will gain experience with Lambda and API Gateway by writing a serverless Slack chat bot.
You will also gain experience with both using a third-party REST API and make your own REST endpoint. This codelab is based off of an [online tutorial](https://chatbotslife.com/write-a-serverless-slack-chat-bot-using-aws-e2d2432c380e) by Rigel Di Scala at ChatBotsLife. The required steps to successfully complete this codelab can be summarized as follows:  

Part 1: Setting Up Slack Chat Bot
You will create a new Slack App and associated Bot. You will additionally generate the Oauth tokens you will need to
save in your API Gateway settings.  

Part 2: Setting Up API Gateway and Lambda  
You will begin a new instance of API Gateway and generate the single resource required to complete this codelab. You
will also drop in some test code in your lambda function to be used in `Part 3` to verify all the API requests are
successfully completing. Finally you will launch your new API endpoint.  

Part 3: Verifying Everything works!  
You will use your new API endpoint to verify a successful connection between your endpoint and Slack.

Part 4: Make your bot says something different that what you messaged it! :)  
Uncomment the code we provided you with and look for the comment that says `TODO:`. This is where you will
add some custom parsing of the message you typed in Slack to send to your bot and will be your Lamda acting in the
role of your bot.

### Due Date

This code is due on Thursday, April 19th, at 11:59:59PM.

### Setup

Make sure to update your local repo with the remote by executing `git pull`. There is no need to run `pipenv install`
for this codelab.

#### Part 1. Setting up your Slack Chat Bot  
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

We have created our bot, subscribed it to an event, so what's left? Authorization!  
Click on `Oauth & Permissions`. The next page will ask us to add an app to our workspace. Once you authorize the bot you will receive a set of OAuth Access tokens. Copy the Bot User OAuth Access Token somewhere since you are going to
need it in API Gateway.

#### Part 2: Setting Up API Gateway and Lambda  
Sign into your AWS Management Console. We will begin by creating the API Gateway resource, so go to its dashboard.

The only predefined resource is root (/), so we’ll create a new resource named /slack-event-handler. Click on the Actions button and then Create Resource from the drop-down menu.  
![Create Resource](../../../media/codelabs/codelab-07/create-api-resource.png)

Enter "Slack Event Handler” as the Resource Name and “slack-event-handler” as the Resource Path. We don’t need to enable CORS as the client will not be a browser, but rather whatever backend application that Slack runs in order to dispatch these requests. Finally, click on the Create Resource button.  
![Confirm Resource](../../../media/codelabs/codelab-07/generate-api-resource.png)  

Before finalising our new API Gateway resource, we need to create the Lambda function that it will trigger. Click on Services in the top menu and open the Lambda Management Console in another browser tab.  

##### Creating the Lambda function    
Go to the Lambda Dashboard and Create a Lambda function.  

Select Blank Function as the blueprint: we’ll start from scratch, so select "Author from Scratch" on the left.  
![Create Lambda](../../../media/codelabs/codelab-07/create-lambda-function.png)
We’ll write our Lambda function in Python 3 and call it “slackBotEventHandler”. Let’s also create and assign an appropriate role to the function. Scroll down to the Lambda function handler and role section and select Create custom role from the Role dropdown. A browser tab should open and you’ll be able to create a new, very basic role, in this new page:
![Create User Role](../../../media/codelabs/codelab-07/lambda-user-role.png)
Click on Allow and the previous form will auto-fill.  
Finally click on "Create" and you will be taken to a new page where we will actually code-up our lambda function.  
The Lambda function will encode the following process:

1. Handle data originating from an incoming POST request and extract the part relevant to the event
2. Check if the message came from a user
3. Perform some string manipulation on the message to send back to the sender.  
4. Send the text in a response to the user, by submitting a new GET request to the appropriate Slack API resource: chat.postMessage  

Lambda functions behave just like plain old CGI (or WSGI) handlers. The Python Lambda function signature, using Python 3 type annotations, is:

  def lambda_handler(event: dict, context: dict) -> str:
    # TODO implement
    return 'Hello from Lambda'  

Delete what is inside the code editor and copy and past the source we provided you in `lambda_slackbot_function.py`  

In our code we reference an environment variable for the bot OAuth token, so let’s define it under the editor:
![Add environment variables](../../../media/codelabs/codelab-07/add-environment-variables.png)  

That’s it for our Lambda function. Let’s jump back into our API Gateway resource.

#####Linking our API resource with our lamda function
We need to configure the resource so that it handles POST requests. Make sure that you click on "slack-event-handler". Then click on the Actions button again and select Create Method, then click on the new drop down field that has appeared and select POST. Finally, click on the check icon.
![Add Function](../../../media/codelabs/codelab-07/create-post-method.png)  


Select “Lambda Function” as the Integration type, if it isn’t already, and choose the Lambda Region that’s most appropriate for you. Enter “slackBotEventHandler” as the name of Lambda Function.  
Click Save. A pop-up notifying you that you are about to give the API Gateway permission to your new Lambda function will appear. Click "Ok".  
Now you should end up with the following workflow:  
![Final Workflow](../../../media/codelabs/codelab-07/final-workflow.png)  

Deploy the API and it will be made available to through a specific web URL. Click on Actions, and then Deploy API.

We’ll be asked to choose your Deployment stage. Create a new one named “dev” and Deploy!  

Once you do that, we’ll finally get what we really want: the Request URL, here referred to as Invoke URL:  

**Important:** You need the URL of your event-handler resource, not the root resource! Expand the tree and click on the green POST link to get to it.
![Deploy](../../../media/codelabs/codelab-07/deploy-function.png)  
Copy the Link URL.

####Part 3. Verifying Everything Works!  

The AWS part of the equation has been taken care of. Now we need to subscribe the bot to the right type of event, so let's go to the Slack API Event subscriptions page. Click `Event Subscriptions` under `Features` on the left menu. Slide `Enable Events` to `On`.  

Now paste the URL you generated in AWS API into the Request URL field. You should get a warning message almost immediately, saying that the URL didn’t reply correctly to the challenge offered by the Slack API.

So what’s going on? The Slack API prudently sends a one-time challenge request to the new URL you’ve just defined as the Request URL. The challenge consists in a random string of characters, and our API is expected to respond with the same same string in the response. We need to amend the code so that it handles this condition. Go back to the code you pasted in your lambda function editor and uncomment lines 26 and 27.  

That should take care of it. Save the function and go back to the Enable Events page and click on Retry. The verification should now succeed:

![Verified](../../../media/codelabs/codelab-07/verified.png)

Scroll down to the Subscribe to Bot Events section and click on Add Bot User Event. Select message.im as the event type:  

![Subscribe Event](../../../media/codelabs/codelab-07/subscribe-event.png)  

Save your changes and go back to the Slack team channel. The bot should be waiting patiently there:

![Slack Ready](../../../media/codelabs/codelab-07/slack-ready.png)  

####Part 4. Customize your bot!
Now that you have all your api calls working and wired up properly, it's time to play with strings! Go back to your
lambda function editor in AWS and look for the TODO comment at line 45. Make sure you read all the comments we provided as they explain all the parameters that need to be associated with your lambda function to make it a successful round trip transaction. When you have implemented your own version go back to Slack and send a direct message to your bot and see that you get the message back you expect to.

















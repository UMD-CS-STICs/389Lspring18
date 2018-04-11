# Codelab 7: Lambda and API Gateway

### Overview

In this codelab you will gain experience with Lambda and API Gateway by writing a serverless Slack chat bot.
You will also gain experience with both using a third-party REST API and make your own REST endpoint. The required
steps to successfully complete this codelab can be summarized as follows:  

1. **Set Up a Slack Chat Bot**:
You will create a new Slack App and associated Bot. You will additionally generate the OAuth tokens you will need to
save in your API Gateway settings.  
1. **Set Up API Gateway and Lambda**:  
You will begin a new instance of API Gateway and generate the single resource required to complete this codelab. You
will also drop in some test code in your Lambda function to be used in the next part to verify all the API requests are
successfully completing. Finally you will launch your new API endpoint.  
1. **Verify Everything Works**:  
You will use your new API endpoint to verify a successful connection between your endpoint and Slack.
1. **Customize your bot's behavior**:
Modify the Lambda function so that your Slack bot does something fun (up to you!).

### Due Date

This code is due on *Sunday, April 22nd at 11:59:59PM*.

### Setup

Make sure to update your local repo with the remote by executing `git pull`. You won't need to set up your pipenv environment
for this codelab.

### Part 1. Set up your Slack Chat Bot  

You will have received an email inviting you to join a Slack workspace (one of `cmsc389lspring2018{a,b,c}`). Go ahead and accept that invite.

> **Note**: If you would like, you can download the native Slack app (Mac, Windows, Linux) here: https://slack.com/get

Let's create a Slack application. Go ahead and open `https://api.slack.com/` and click the green button in the center that says `Start Building`.

In the next window give your app the name `firstname_lastname_slack_bot`. This is how we will identify your submission for grading purposes. Also select which slack workspace you want this bot to be associated with (one of `cmsc389lspring2018{a,b,c}`).

In the next view, under `Add features and functionality`, select `Bots`. Then select `Add a Bot User`. Leave the pre-populated fields as they are. Toggle the slider to show your bot as always being online and then click the green `Add Bot User` button.  

We now need to enable event subscription. The way the chat bot will work is the following:

1. Users send a direct chat message to the chat-bot.  
1. An event representing that message is published.  
1. If the bot is subscribed to that type of event, a HTTP POST request, containing information about that chat message, is dispatched to a web resource listening on the given URL.  
1. That POST request is handled by a web application that we can easily build using a couple of “serverless” AWS cloud technologies:
  - An API Gateway resource, at that URL, handles the incoming POST request.
  - An AWS Lambda function processes the payload of the POST request and takes an appropriate action, such as making a new request to the Slack API (e.g. to reply to the message)

Here’s an interaction diagram that illustrates what will happen each time our bot receives a direct message:

![Architecture](../../../media/codelabs/codelab-07/codelab07-architecture.png)   

Next, we need to authorize the bot to access our Slack workspace.

Click on `OAuth & Permissions`. The next page will ask us to add an app to our workspace. Once you authorize the bot you will receive a set of OAuth Access tokens. You will need the `Bot User OAuth Access Token` later in API Gateway.

### Part 2: Set Up API Gateway and Lambda

We need to create a new API endpoint, `/slack-event-handler`, that Slack can POST to whenever a message is sent to our bot. Let's go ahead and do that with API Gateway.

Sign into your AWS Management Console, go to the API Gateway dashboard, and create a new regional API.

We will need to create a resource (`slack-event-handler`) with a single method exposed, `POST`. Click on the Actions button to create the resource.

![Create Resource](../../../media/codelabs/codelab-07/create-api-resource.png)

> **Note**: We don’t need to enable CORS as the client will not be a browser, but rather a backend server that Slack runs in order to dispatch these requests.

![Confirm Resource](../../../media/codelabs/codelab-07/generate-api-resource.png)  

However, before creating the method on this resource, we will need to create the Lambda function that it will trigger.

##### Create the Lambda function
Go to the Lambda dashboard and create a Lambda function.  

![Create Lambda](../../../media/codelabs/codelab-07/create-lambda-function.png)

We’ll write our Lambda function in Python 3 and call it `slackBotEventHandler`.

We also need to assign an IAM role to this Lambda function, however it will only need permissions to access CloudWatch to report its logs. If you select `Create a custom role`, it will auto-generate the minimal Lambda role for just that.

![Create User Role](../../../media/codelabs/codelab-07/lambda-user-role.png)

Great, you're done. Go ahead and create the new function. You'll be taken to a new page where we can design our Lambda function.

The Lambda function will encode the following process:

1. Handle data originating from an incoming POST request and extract the part relevant to the Slack message.
2. Check if the message came from a user.
3. Perform some kind of string manipulation on the message.
4. Send the text in a response to the user, by submitting a new `GET` request to the appropriate Slack API resource: [`chat.postMessage`](https://api.slack.com/methods/chat.postMessage).

Lambda functions work by starting execution at a specified handler function. In Python 3, this might look like so:

```
def lambda_handler(event, context):
  # TODO: implement
  return 'Hello from Lambda'  
```

You can delete what is inside the code editor, then copy and paste the source we provided you in `codelabs/codelab-07/lambda_slackbot_function.py`.

In our code we reference an environment variable for the bot OAuth token (`os.environ["BOT_TOKEN"]`), so let’s define it as part of our Lambda environment:

![Add environment variables](../../../media/codelabs/codelab-07/add-environment-variables.png)

Great, that’s it for our Lambda function for now. We just need to finish configuring our API Gateway.

##### Linking our API resource with our Lambda function

We need to configure the resource so that it handles POST requests. Make sure that you click on `slack-event-handler`. Then, create a new `POST` method with the dropdown the appears below your resource.

![Add Function](../../../media/codelabs/codelab-07/create-post-method.png)

Enter “slackBotEventHandler” as the name of Lambda Function, then save it.

Now you should end up with the following workflow:  

![Final Workflow](../../../media/codelabs/codelab-07/final-workflow.png)

Great, now we just need to deploy this API so that API Gateway will assign it a URL. Click on `Actions`, and then `Deploy API`.

You’ll be asked to choose the deployment stage. Go ahead and create a new one called `prod`.

> **Tip**: These deployment stages allow you to create various versions of your API (f.e., `development`, `qa`, `staging`, `production`) so that you can test your APIs without interfering with the production version of your application.

Your API is now available at the specified `Invoke URL`. It will look something like: `https://ne1p41ytol.execute-api.us-east-1.amazonaws.com/prod/`.

Note that you can now access any resource/method combination using this URL. You just append the resource to the end of this URL and submit an HTTP request to it. For example, Slack will hit our endpoint like so:

```
POST https://ne1p41ytol.execute-api.us-east-1.amazonaws.com/prod/slack-event-handler
```

![Deploy](../../../media/codelabs/codelab-07/invoke-url.png)

### Part 3. Verify Everything Works!  

The AWS part of the equation has been taken care of. Now we need to subscribe the bot to the right type of event, so let's go back to the [Slack API](https://api.slack.com/apps/) page. Click `Event Subscriptions` under `Features` on the left menu and turn on `Enable Events` to `On`.

Now, paste in the Invoke URL for the `slack-event-handler` resource.

Scroll down to the `Subscribe to Bot Events` section and click on `Add Bot User Event`. Select `message.im` as the event type:  

![Subscribe Event](../../../media/codelabs/codelab-07/subscribe-event.png)  

Save your changes and go back to the Slack team channel. The bot should be waiting patiently there:

![Slack Ready](../../../media/codelabs/codelab-07/slack-ready.png)  

Go ahead and send your bot user a message. If everything is set up correctly, it should just send your text back to you.

> **Note**: Is it not working? The first place to check would be the [CloudWatch logs](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logs:) for your Lambda function.

### Part 4. Customize your bot!

Now that you have the Slack bot up-and-running, it's time to add your own little flaire to the bot!

Go back to your Lambda function editor in AWS and look for the TODO comment. You can do anything you would like in response to a message from a user, other than a) returning it verbatim or b) reversing it. Some ideas: pig-latin, emoji-ify it, translate it to a different language, or just return sassy responses. Up to you!

### Submission

There is nothing to submit for this codelab. Just leave your bot up-and-running through the deadline and we will check that it functions correctly after the due date.

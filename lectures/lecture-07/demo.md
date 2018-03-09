# Lecture 7 Demo Notes

We will be demoing an AWS SQS queue using the demo in this folder.

Set up your environment by running the following:

```
$ pipenv install
...
$ pipenv shell
...
```

Locally, go ahead and run the message processor:

```
% python process-mesages.py
...
```

### Posting Messages


### Recreating this Demo

You can perform this demo with your own account. You'll need to create a standard SQS queue and then update `add-message.py` and `process-messages.py` with your AWS account id and the name of the queue you created. (You won't have write access to our queue, so you )

# Lecture 7 Demo Notes

We will be demoing an AWS SQS queue using the demo in this folder.

Set up your environment by running the following:

```
$ pipenv install
...
$ pipenv shell
...
```

### Processing Messages

#### No Deletion Request

```
$ python process-mesages.py
...
```

#### With Deletion Requests

```
$ python process-mesages.py --delete
...
```

### Recreating this Demo

If you want, you can recreate this demo outside of class to play around with SQS queues.

You'll need to create a standard SQS queue and then update `add-message.py` and `process-messages.py` with your AWS account id and the name of the queue you created.

Then, you can post messages as follows:

```
$ python add-messages.py
...
```

Or multiple at once:

```
$ python add-messages.py -n=10
...
```

# Codelab 3: AWS + S3 + ClounFront

### Due Date

This is codelab 3, which expands upon ![codelab-02](../../../media/codelabs/codelab-02/README.md) by introducing CloudFront. Both are due on *Thursday, February 15th at 11:59:59PM*.

### Goal

In this codelab, you'll get to play around with ClounFront.
- You'll set up CloudFront via the AWS GUI
- You'll test latency 
- You'll issue an invalidation

### Setting Up

Before starting this codelab, run `git pull` in the `389Lspring18` directory to update your local copy of the class repository.

### Tutorial

**It's a good idea to read/skim the entire codelab first so you have an idea of what you're doing. Keep in mind that you will be submitting screenshots of some command outputs, so make sure to read the submission section (at a minimum) located near the bottom to understand what you will be turning in**

#### Back to buckets

Fist, download the image ![canyon.jpg](../../../media/codelabs/codelab-03/canyon.jpg)

Now, using the [AWS GUI](https://console.aws.amazon.com/console/home?region=us-east-1#), navigate to S3.

From the S3 dashboard, click `Create Bucket`.

In the field labeled *bucket name*, use the format `cmsc389l-<your directory id>-codelab-03`.

In the field labeled *region*, select `Asia Pacific (Sydney)`.

This is what your form should look like.

![create bucket Page](../../../media/codelabs/codelab-03/create-bucket.png)

Click the `Create` button in the lower-left corner. For the purposes of this tutorial, the default properties and permissions are fine. Go ahead and skip past the rest of the configuration screens and create the bucket.

Select your newly-created bucket (you have to click the bucket name itself).

Upload `canyon.jpg` from where you downloaded it on your machine. By default, S3 objects permissions are set to private. We will need to modify those permissions to public.

Click `Next` and select `Grant public read access to this object(s)` from the drop-down menu labeled *Manage public permissions*.

Your form should look similar to this.

![public-read-access Page](../../../media/codelabs/codelab-03/public-read-access.png)

Click the `Upload` button in the lower-left corner.

#### Testing latency

Select your new object (again, you have to click the name itself). This page similarly lets you see some details and configure properties. What we're after is the URL at the bottom of the page, under the label `Link`.

Copy the link and paste it in the URL bar of a new tab in your browser. The canyon should start loading, albeit slowly. Why so slow? Well, we did place it in a region half-way 'round the world. 

Let's try to quantify that speed. Edit the last line in the included shell script `lat-test.sh`, using a command line text editor or IDE, and drop in the copied link. If you haven't already, enter your environment now by running:

```
 $ pipenv shell
```

Make sure you have the proper dependencies from the `Pipfile` with the command:

```
$ pipenv install
```

You may need to make the script executable. While in the same directory as the script is located, run:

```
$ chmod +x lat-test.sh
``` 

Now execute it but running:

```
./lat-test.sh
```

- What is the output?
	- namelookup: The time, in seconds, it took from the start until the name resolving was completed.
	- connect: The time, in seconds, it took from the start until the TCP connect to the remote host (or proxy) was completed.
    - appconnect: The time, in seconds, it took from the start until the SSL/SSH/etc connect/handshake to the remote host was completed.
    - pretransfer: he time, in seconds, it took from the start until the file transfer was just about to begin. This includes all pre-transfer commands and negotiations that are specific to the particular protocol(s) involved.
    - redirect: The time, in seconds, it took for all redirection steps including name lookup, connect, pretransfer and transfer before the final transaction was started. Redirect shows the complete execution time for multiple redirections.
    - starttransfer: The time, in seconds, it took from the start until the first byte was just about to be transferred. This includes time_pretransfer and also the time the server needed to calculate the result.
    - total: The total time, in seconds, that the full operation lasted.

Don't be too surprised if it's several whole seconds. Unlike a ping request which simply tests reachability, this script includes server side time taken. More information about curl may be found on the [manpage](https://curl.haxx.se/docs/manpage.html).

![lat-test-on-canyon-in-s3-sydney Page](../../../media/codelabs/codelab-03/lat-test-on-canyon-in-s3-sydney.png)

For comparison, try some other URLs in the script. If you use the link for the index file from codelab-02, the time should be on the order of .5 seconds (recall we used us-east-1 which is located in northern Virginia).

#### CloudFront

Lets return to using the [AWS GUI](https://console.aws.amazon.com/console/home?region=us-east-1#), this time navigating to CloudFront, which can be found under *Storage & Content Delivery*.

From the CloudFront console, click `Create Distribution`. This will allow us to tell AWS which origin to use for our content. There are two types of delivery CloudFront can use; *web* (suited to static content, like our canyon image) and *RTMP* (suited to dynamic content, like videos). Select the top `Get Started` button under the _Web_ heading.

Now, click into the *Origin Domain Name* text box. You will see a list of possible origins for content. Select the bucket created in the first part of this tutorial. We'll be using the default values for all other fields in this tutorial.

Scroll to the bottom and click the blue `Create Distribution` in the bottom-left. You will then be on a page showing your distributions that will look something like this.

![dist-status-in-progress Page](../../../media/codelabs/codelab-03/dist-status-in-progress.png)

Note that the status is *in progress*, deployment may take several minutes. When complete, the status will change to *deployed*. Then, go ahead and grab the _Domain Name_ (it should end in `.cloudfront.net`).

Now we're ready to test. The new URL of our content will be of the form "http://domainName/objectName". So it should look something like `http://3x4mpl3.cloudfront.net/canyon.jpg`. Try this in your browser.

Edit the shell script again and run it a few times. Does the total time change?

![lat-test-on-canyon-in-cloudfront-sydney Page](../../../media/codelabs/codelab-03/lat-test-on-canyon-in-cloudfront-sydney.png)

Now suppose we want to change the image we're serving. Using the [AWS GUI](https://console.aws.amazon.com/console/home?region=us-east-1#) again, delete the current `canyon.jpg` and replace it with [this one](https://s3.amazonaws.com/cmsc389l-ialock-lab3/canyon.jpg). *Note: make sure the S3 keys are identical* (`canyon.jpg`) 

Verify you can reach it by the S3 link from your browser. Then try to reach it with your CloudFront link... and you might not be able to. So what is happening here? Why is CloudFront serving a stale version of our canyon.jpg image? This is because every object cached by CloudFront has an associated "Time-To-Live" (TTL) which expresses how long a file should be served from an edge location before being considered expired. This defaults to 24 hours -- so if you waited 24 hours and then re-visited this file via the CloudFront distribution, you would get the new version of `canyon.jpg`.

### Assignment

Your assignment for this codelab is to reference the [documentation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AddRemoveReplaceObjects.html) and issue an invalidation via the AWS CLI.

### Submission

You will be submitting:
1. Screenshot of lat_test.sh output on canyon.jpg in Sydney S3
- Two other screenshots of lat_test.sh output on two different images from the internet.
- Screenshot of lat_test.sh output on canyon.jpg in CloudFront
- Screenshot showing the invalidation command you used and its console output
- 3-5 sentences explaining the tradeoff associated with time duration of objects in the cache.

Do this for when the image is hosted in S3 alone AND once it has been deployed in CloudFront. Similarly, capture the command and output for your invalidation. Finally, write your `summary.txt` file.

Submit this assignment to `codelab3` on the submit server. Upload a zipped directory containing the following files:

```
<directory id>.zip
	screenshot1.png 
	screenshot2.png 
	screenshot3.png 
	summary.txt
```
#Codelab 3: AWS + S3 + ClounFront

### Due Date

This codelab comes in two parts, both of which are due on *Thursday, February 15th at 11:59:59PM*. This is codelab-03 (part B) which expands upon what was learned in [codelab-02](https://umd-cs-stics.gitbooks.io/cmsc389l-practical-cloud-computing-spring-2018/content/codelabs/codelab-02/) (part A) and introduces CloudFront.

### Goal

In this codelab, you'll get to play around with ClounFront.
- You'll set up CloudFront via the AWS GUI
- You'll test latency 
- You'll issue an invalidation

### Setting Up

Before starting this codelab, run `git pull` in the `389Lspring18` directory to update your local copy of the class repository.

### Tutorial

<!-- maybe include a summary of what we're going to do -->

#### Back to buckets

Fist, download the image `canyon.jpg` located
[here](https://s3.amazonaws.com/cmsc389l-ialock-lab3/canyon.jpg)

Now, using the [AWS GUI](https://console.aws.amazon.com/console/home?region=us-east-1#), navigate to S3.

From the S3 dashboard, click `Create Bucket`.

In the field labeled *bucket name*, use the format `cmsc389l-#-codelab03`; substituting your directory id for the octothorp(#).

In the field labeled *region*, select `Asia Pacific (Sydney)`.

This is what your form should look like.

![create bucket Page](../../../media/codelabs/codelab-03/create_bucket.png)

Click the `Create` button in the lower-left corner. For the purposes of this tutorial, the default properties and permissions are fine.

Select your new bucket by hovering over its bucket name until highlighted with an underscore; click. This page lets add/view content and configure properties.

Click the blue `Upload` button and `Add files` on the subsequent window. Now select `canyon.jpg` from where you downloaded it on your machine. By default, S3 objects permissions are set to private. We will need to modify those permissions to public.

Click `Next` in the lower-right, and select `Grant public read access to this object(s)` from the drop-down menu labeled *Manage public permissions*.

Your form should look similar to this.

![public_read_access Page](../../../media/codelabs/codelab-03/public_read_access.png)

Click the `Upload` button in the lower-left corner.

#### Testing latency

Select your new object by again hovering over the name until highlighted with an underscore and clicking. This page similarly lets lets you see some details and configure properties. What we're after is the URL at the bottom of the page, under the label `Link`.

Copy the link and paste it in the URL bar of a new tab in your browser. The canyon should start loading, albeit slowly. Why so slow? Well, we did place it in a region half-way 'round the world. 

Lets try to quantify that speed. Edit the last line in the included shell script `lat_test.sh`, using a command line text editor or IDE, and drop in the copied link. If you haven't already, enter your environment now by running:

```
 `$pipenv shell`
```

You may need to make the script executable. While in the same directory as the script is located, run:

```
$ chmod +x lat_test.sh
``` 

Now execute it but running:

```
./lat_test.sh
```

What is the output? Don't be too surprised if it's several whole seconds. Unlike a ping request which simply tests reachability, this script includes server side time taken.

![lat_test_on_canyon_in_s3_sydney Page](../../../media/codelabs/codelab-03/lat_test_on_canyon_in_s3_sydney.png)

For comparison, try some other URLs in the script. If you use the link for the index file from codelab-02, the time should be on the order of .5 seconds (recall we used us-east-1 which is located in northern Virginia).

#### CloudFront

Lets return to using the [AWS GUI](https://console.aws.amazon.com/console/home?region=us-east-1#), this time navigating to CloudFront, which can be found under *Storage & Content Delivery*.

From the S3 CloudFront, click `Create Distribution`. This will allow us to tell AWS which origin to use for our content and configure settings. There are two types of delivery CloudFront can use, *web* and *RTMP*.

Click the top `Get Started` button under the _Web_ heading. This is for static (like our canyon image) and dynamic content. _RTMP_ is best for streaming.

Now, click into the *Origin Domain Name* text box. You will see a list of possible origins for content. Select the bucket created in the first part of this tutorial. We'll be using the default values for all other fields in this tutorial.

Scroll to the bottom and click the blue `Create Distribution` in the bottom-left. You will then be on a page showing your distributions that will look something like this.

![dist_status_in_progress Page](../../../media/codelabs/codelab-03/dist_status_in_progress.png)

Note that the status is *in progress*, deployment may take several minutes. When complete, the status will change to *deployed*. Then, go ahead and grab the _Domain Name_ (it should end in .cloudfront.net).

Now we're ready to test. The new URL of our content will be of the form "http://domainName/objectName". So it should look something like `http://3x4mpl3.cloudfront.net/canyon.jpg`. Try this in your browser.

Edit the shell script again and run it a few times. Does the total time change?

![lat_test_on_canyon_in_cloudfront_sydney Page](../../../media/codelabs/codelab-03/lat_test_on_canyon_in_cloudfront_sydney.png)

### Assignment

Your assignment for this codelab is to see why issuing an invalidation may be used
**Note**:  note

<!-- expand to talk about time-to-live
have students explain the tradeoff associated with time duration of objects in cache -->

Then here are a few examples of the resulting state in S3:

		<!-- 
		swap out an image also named canyon.jpg in the bucket
		load url
		modify TTL via CLI
		load url again
		-->

### Submission

Submit screenshots of your modified `lat_test.sh` script and its output. After editing, run:

```
$ cat lat_test.sh
```

Then execute immediately after thus:

```
./lat_test.sh
```

Make sure to capture both commands and their outputs in the same screenshot. Do this for when the image is hosted in S3 alone AND once it has been deployed in CloudFront. Include a text file `summary.txt` containing 3-5 sentences explaining why the "total time" is different.

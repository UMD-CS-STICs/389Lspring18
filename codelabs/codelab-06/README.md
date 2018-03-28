# Codelab 6: EC2 + ALB

### Overview

Today, you'll be working with EC2 and an Application Load Balancer (ALB) to support scaling a website.

### Due Date

This code is due on *Thursday, April 5th at 11:59:59PM*.

### Setup

Make sure to do a pull on your git repo and then set up your pipenv as usual. This codelab has packaged with it a test utility, [beeswithmachineguns](https://github.com/newsapps/beeswithmachineguns) *"...for arming (creating) many bees (micro EC2 instances) to attack (load test) targets (web applications)"*, which will install with your pipenv shell. We'll also be working heavily from the AWS GUI here, so go ahead and log in with your account.

It's possible to complete this codelab using the IAM user and the key pair, but it's best practice to create new ones. This aids in security (principle of least priviledge), identifying what code is doing what, and solving the problem of your former memorable name not being so memorable.

#### IAM

As in [Codelab 2](codelabs/codelab-02/README.md), add a user in the "IAM" service via the AWS Console. Give it a name that tells you its purpose. Since the user will be Bees (our test utility), "Buzz" might be a good choice. When creating a new group select "EC2FullAccess" instead of administrator. Again, _make sure to save your access keys_ as you will need them later.

![newIAMuser](../../../media/codelabs/codelab-06/newIAMuser.png)

#### EC2

Moving to EC2, under the NETWORK & SECURITY tab, create a new key pair and give it a *memorable* name. Then, after you have it downloaded, move a copy to the `.ssh` folder in your home directory. This is where Bees will look for it.

```
 $ cp ~/Downloads/<bees>.pem ~/.ssh/<bees>.pem
```

While we're here under this tab, take a look at Security Groups and remind yourself of the memorable name you used in [Codelab 4](codelabs/codelab-04/README.md). This is important because Bees will need access to ports 80 and 22.

### Web server

For our server, will use a pre-built AMI from the AWS Marketplace that is similar to the one configured in Codelab 4. Using the EC2 service in the AWS Console, start the Launch Instance wizard. From the AWS Marketplace tab, search for and select "WordPress Certified by Bitnami".

![marketplace](../../../media/codelabs/codelab-06/marketplace.png)

- Instance Type: t2.micro
- Configuration Details: Use the defaults
- Storage: Use the defaults
- Tags: None
- Security Group: Use your codelab 4 security group
- Key Pair: Use your codelab 4 key pair

Verify it comes up using the public DNS in your browser, it should look pretty familiar.

![usersBlog](../../../media/codelabs/codelab-06/usersBlog.png)

### Send in the bees

Moving to your pipenv shell, export your IAM Bees keys

```
$ export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
$ export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

$ bees up -s 1 -g <security group> -k <key.pem>
$ bees attack -n 2000 -c 250 -u http://<public DNS>

![firstTest1instance](../../../media/codelabs/codelab-06/firstTest1instance.png)

### ALB

#### Setup

Using EC2 service in AWS Console
LOAD BALANCING --> Load Balancers --> Create Load Balancer --> Application Load Balancer --> Create

give it a name

- Scheme: Use the defaults
- IP address type: Use the defaults
- Listeners: Use the defaults
- Availability Zones: use the same as your instance
*note: you must pick two AZs*

![mustPickTwo](../../../media/codelabs/codelab-06/mustPickTwo.png)

 --> Configure Security Groups --> Create Security Group

-

#### test *again*



### Wrapping Up

Leave your content up for us to verify. We'll be looking for your post at a DNS name you will submit.

Make sure to let your bees go home with the command `bees down`.

If you are running any other EC2 instances that you are no longer using, be sure to stop
("Actions" > "Instance State" > "Stop")
or terminate
("Actions" > "Instance State" > "Terminate")
them; else they will eat into your free credit.
<!--
Here are some [ideas](http://www.wpbeginner.com/beginners-guide/top-10-most-important-things-to-do-after-installing-wordpress/) for what to do with your site, now that it's up.
-->
### Submission

You will be submitting a text file called `ip.txt` containing only the DNS name of your load balencer.

Submit this assignment to `codelab6` on the submit server. Upload a zipped directory with the file:

```
<directory id>.zip
	dns.txt
```

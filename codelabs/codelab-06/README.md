# Codelab 6: EC2 + ALB

### Overview

Today, you'll be working with EC2 and an Application Load Balancer (ALB) to support scaling a website.

### Due Date

This code is due on *Thursday, April 5th at 11:59:59PM*.

### Setup

Make sure to do a pull on your git repo and then set up your pipenv as usual. This codelab has packaged with it a test utility, [beeswithmachineguns](https://github.com/newsapps/beeswithmachineguns) *"...for arming (creating) many bees (micro EC2 instances) to attack (load test) targets (web applications)"*, which will install with your pipenv shell. We'll also be working heavily from the AWS GUI here, so go ahead and log in with your account.

It's possible to complete this codelab using the IAM user and the key pair you already have, but it's best practice to create new ones. This aids in security (principle of least priviledge), identifying what code is doing what, and solving the problem of your former memorable name not being so memorable.

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

Configure as follows:
- Instance Type: t2.micro
- Configuration Details: Use the default
- Storage: Use the default
- Tags: None
- Security Group: Use your codelab 4 security group
- Key Pair: Use your codelab 4 key pair


Verify it comes up using the public DNS in your browser, it should look pretty familiar.

![usersBlog](../../../media/codelabs/codelab-06/usersBlog.png)

*Note: from the bees README "please keep in mind the following important caveat: they are, more-or-less a distributed denial-of-service attack in a fancy package and, therefore, if you point them at any server you don’t own you will behaving unethically, have your Amazon Web Services account locked-out, and be liable in a court of law for any downtime you cause. You have been warned."*

### Send in the drones

#### Crashcourse on Bees commands

up:
- -s: flag preceeding specified number of instances
- -g: flag preceeding security group name (must have port 22 access)
- -k: flag preceeding key pair filename (omit .pem extension)

attack:
- -n: flag preceeding specified number of requests
- -c: flag preceeding number of requests to send at a time
- -u: flag preceeding url to be attacked

#### On keyboard

Moving to your pipenv shell, first export your IAM Bees keys obtained in setup.

```
$ export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
$ export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Next, it's time to muster the troops. 

```
$ bees up -s 1 -g <security group> -k <key.pem>
```

Then, over the top!

```
$ bees attack -n 2000 -c 250 -u http://<public DNS>
```

You should get output that's something like this.

![firstTest1instance](../../../media/codelabs/codelab-06/firstTest1instance.png)

More information may be found by consulting the [docs](https://github.com/newsapps/beeswithmachineguns) or with `$ ./bees --help`

*Note: i know, i know, bee drones are male and the utiliy uses feminine pronouns for the bees, which means they're prabably workers.. i just think it's a clearer reference as a pun*

### ALB

Let's see if we can improve on those results with a tool to balance the load.

#### Invocation

Using EC2 service in AWS Console, find the LOAD BALANCING tab and click

 --> Load Balancers --> Create Load Balancer --> Application Load Balancer --> Create

Configure as follows:
- Name: give it a memerable one
- Scheme: Use the default (internet-facing)
- IP address type: Use the default (ipv4)
- Listeners: Use the default (HTTP port 80)
- VPC: Use the default (default)
- Availability Zones: use the AZ as you just launched an instance in and an alternate

_You must select two AZs_

![mustPickTwo](../../../media/codelabs/codelab-06/mustPickTwo.png)


 --> Next: Configure Security Settings
 
We will not be using secure listeners in this codelab.


 --> Next: Configure Security Groups --> Create a _new_ Security Group

All defaults here are fine. This will create an inbound rule that allows traffic on the listener we just made (HTTP port 80) and allow all outbound traffic. Optionally you may customize the name or description.


 --> Next: Configure Routing.

- Target group: Use the default (New target group)
- Name: give it a memerable one
- Protocol: Use the default (HTTP)
- Port: Use the default (80)
- Target type: Use the default (instance)
- Protocol: Use the default (HTTP)
- Path: Use the default (/)


 --> Next: Register Targets.

Select the instance you just launched, keeping the default port (80)


 --> Add to registered --> Next: Review --> Create

The ALB will take a few moments to be created. You may check status by clicking "Load Balancers" under the LOAD BALANCING tab. While your there, check the description for the field _DNS name:_. This is what you will be submitting when you're finished. One the ALB is spun up, again verify it loads in your browser.

#### Testing part 2: Electric boogaloo

Order another attack, this time at the ALB

![1instanceBehindALB](../../../media/codelabs/codelab-06/1instanceBehindALB.png)

and try adding instances to see if we can improve.

![2instancesBehindALB](../../../media/codelabs/codelab-06/2instancesBehindALB.png)

### Assignment

Your goal is simple. Given a swarm of 4 bees shooting 10000 requests, 250 at a time, ensure the mean response is within 3 seconds or less.

### Wrapping Up

Leave your content up for us to verify. We'll be looking for your site at a DNS name you will submit.

Make sure to let your bees go home with the command `bees down`.

If you are running any other EC2 instances that you are no longer using, be sure to stop

 --> Actions --> Instance State --> Stop
 
or terminate

 --> Actions --> Instance State --> Terminate
 
them; else they will eat into your free credit.

*Note: Our setup is contrived. Here we will use a turn-key AMI to demonstrate scaling of a static site. In practice, a scalable wordpress website would use stateless servers (which could be spun up/down as needed) that rely on another service for their data (e.g. S3 or EBS).*

### Submission

You will be submitting a text file called `ip.txt` containing only the DNS name of your load balencer.

Submit this assignment to `codelab6` on the submit server. Upload a zipped directory with the file:

```
<directory id>.zip
	dns.txt
```

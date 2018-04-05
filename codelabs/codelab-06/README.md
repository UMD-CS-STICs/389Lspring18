# Codelab 6: EC2 + ALB

### Overview

Today, you'll be working with Application Load Balancers (ALBs) to scale a Wordpress website under load.

### Due Date

This code is due on *Thursday, April 5th at 11:59:59PM*.

### Setup

Make sure to do a pull on your git repo and then set up your pipenv as usual. This codelab has packaged with it a test utility called [Bees With Machine Guns (BWMG)](https://github.com/newsapps/beeswithmachineguns):

> A utility for arming (creating) many bees (small EC2 instances) to attack (load test) targets (web applications).

It is automatically installed in your pipenv shell (`bees --help`).

We'll be working heavily from the AWS GUI here, so go ahead and log in with your account.

### IAM

#### IAM User for Bees

As in [Codelab 2 (AWS/S3)](/codelabs/codelab-02/README.md), add a new IAM user with programmatic access. This user will be used purely for BWMG, so give it a clear name. Bees will only need access to EC2 instances, so attach the `AmazonEC2FullAccess` policy instead of giving it administrator privileges. _Make sure to save your access keys_ as you will need them later.

> **Note**: While it is possible to complete this codelab using the IAM user and the key pair you already have, it is generally a best practice to create a new one. This aids in security by following the principle of least privilege.

![newIAMuser](../../../media/codelabs/codelab-06/newIAMuser.png)

### EC2

#### Key Pair for Bees

Next, we will create a key pair specifically for Bees.

Moving to EC2, under the `Network and Security` tab, create a new key pair and give it a memorable name. Then, after you have it downloaded, move a copy to the `.ssh` folder in your home directory. This is where Bees will look for it.

```
 $ cp ~/Downloads/<bees>.pem ~/.ssh/<bees>.pem
```

#### Security Group for Bees

While you're here, go ahead and create a new security group that opens up SSH and HTTP for Bees.

> **Tip**: It's generally a good idea to create separate security groups for different services, because you can modify the rules in the security group at any time, but you can't change security groups after you've created an EC2 instance. Therefore, if you re-used a security group and Bees needed an extra port opened, then you would have to open that port for all services using that security group.

#### Launch a Wordpress AMI

For our server, will use a pre-built AMI from the AWS Marketplace that is similar to the one you all created in Codelab 4.

> **Note**: You can't use the same server from Codelab 4, because that server hardcodes its IP address, so if we launched it from an AMI then it would be assigned a new IP and you would have to manually update the hardcoded IP -- Bitnami's Wordpress image solves this problem for us.

Go ahead and open the EC Launch Instance wizard. From the AWS Marketplace tab, search for and select "WordPress Certified by Bitnami".

![marketplace](../../../media/codelabs/codelab-06/marketplace.png)

Configure as follows:
- Instance Type: t2.micro
- Configuration Details: Use the default
- Storage: Use the default
- Tags: None
- Security Group: Use the default
- Key Pair: Use your EC2 key pair from previous codelabs

Verify it comes up using the public DNS in your browser, it should look pretty familiar.

![usersBlog](../../../media/codelabs/codelab-06/usersBlog.png)

> **Note** (from the authors of Bees):
>
> "If you decide to use the Bees, please keep in mind the following important caveat: they are, more-or-less a distributed denial-of-service attack in a fancy package and, therefore, if you point them at any server you don’t own you will behaving unethically, have your Amazon Web Services account locked-out, and be liable in a court of law for any downtime you cause.
>
> You have been warned."*

### Send in the drones 🐝

#### How to manage the bee hive

The `bees` command works by launching a set of EC2 instances which then attack a given URL by drowning it with HTTP requests.

There are two commands you will need to know and use (`up` and `attack`). The former launches the servers which will then wait around until directed to attack a URL with the latter command.

```
$ bees up -s NUM_SERVERS -g BEES_SECURITY_GROUP_NAME -k KEY_PAIR_FILENAME
```

- `-s NUM_SERVERS`: The number of Bees servers to run.
- `-g BEES_SECURITY_GROUP_NAME`: The Bees security group from earlier.
- `-k KEY_PAIR_FILENAME`: The name of the Bees key pair you created earlier (without the `.pem` extension).

```
$ bees attack -n NUM_REQUESTS -c NUM_CONCURRENT_REQUESTS -u URL
```

- `-n NUM_REQUESTS`: The number of total connections to make to the target.
- `-c NUM_CONCURRENT_REQUESTS`: The number of concurrent connections to make to the target.
- `-u URL`: URL of the target to attack.

There are a number of other flags we haven't covered (see `bees --help`).

#### Attack your Wordpress server!

Moving to your pipenv shell, first set the environment variables corresponding to the access keys for your IAM Bees user.

```
$ export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
$ export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

If you exit this shell, these variables will be unset. So make sure to store them somewhere.

Next, it's time to muster the troops.

```
$ bees up -s 1 -g <security group> -k <key>
```

Since we're testing the instance directly, make sure to use the IPv4 Public IP for the address. Then, over the top!

```
$ bees attack -n 2000 -c 250 -u http://<address>
```

You should get an output like this. How would you feel accessing a blog post if it took an average of 6.854 seconds to load a page?! Try accessing the blog while Bees is running -- it should be slow to load.

![firstTest1instance](../../../media/codelabs/codelab-06/firstTest1instance.png)

*Note: i know, i know, bee drones are male and the utility uses feminine pronouns for the bees, which means they're probably workers...*

### ALB

Our server is having trouble keeping up with the load. So, let's see if we can improve on those results by balancing the load across more than one instance.

#### Configure the ALB

Go ahead and launch an Application Load Balancer under the `Load Balancing` tab under EC2 in the AWS console.

You are going to use mostly defaults for this ALB. For the AZs, select all of them (you need at least two). On the security group window, create a new one, but use the default security group that it recommends (with port 80 open). On the `Register Targets` page, add the Wordpress server you launched. Then launch!

The ALB will take a few moments to be created. You can see the state of your load balancer in the `Load Balancing` tab. It starts as `provisioning` and will be ready when it gets to `active`. While waiting go ahead and check the description for the field `DNS name:`. This is what you will be submit in a `dns.txt` file when you're finished. Once the ALB is spun up, go ahead and visit the DNS and verify it loads the Wordpress server in your browser.

#### Testing part 2: Electric boogaloo

Order another attack, this time at the ALB, using its DNS name for address. You should get roughly the same latency metrics.

![1instanceBehindALB](../../../media/codelabs/codelab-06/1instanceBehindALB.png)

Then launch a second instance (using the same steps as above) and register it to the ALB's target group. What happens to the latency of your Wordpress server?

![2instancesBehindALB](../../../media/codelabs/codelab-06/2instancesBehindALB.png)

> **Note**: If you add a new instance to the load balancer before it has fully launched, then it might fail the health check from the load balancer. It'll take a few minutes to pass the health check, since it by default will have to pass 5 health checks (performed once per 30s) before being considered healthy. You can increase the health check frequency and reduce the threshold to be considered healthy to speed this up.

> **Note**: You can also double-check that the load balancer is routing you to multiple servers by commenting on a blog post. The blog's state is not replicated across all instances, so each instance has it's own state (comments, posts, etc.).

### Assignment

Your goal is simple. Given a swarm of 4 bees servers shooting 10000 requests, 250 at a time, ensure the mean response (`Time per request`) is under 3 seconds. Launch as many t2.micro instances behind your load balancer as you need to hit that goal, but no more.

### Wrapping Up

Leave the load balancer and the servers set up for us to verify. We'll be testing your site at the DNS name you submit in a `dns.txt` file. We'll post on Piazza when you can shut down these instances.

However, you can shut down your bees servers. Make sure to let your bees go home with the command `bees down`.

If you are running any other EC2 instances that you are no longer using, be sure to terminate them, under `EC2 > Actions > Instance State > Terminate`.

> **Note**: Our setup is contrived. Here we will use a turn-key AMI to demonstrate scaling of a static site. In practice, a scalable Wordpress website would use stateless servers (which could be spun up/down as needed) that rely on a replicated database to store blog data (e.g. MySQL running in RDS) rather than running the database on the server itself.

### Submission

You will be submitting a text file called `dns.txt` containing only the DNS name of your load balancer.

Submit this assignment to `codelab6` on the submit server. Upload a zipped directory with the file:

```
<directory id>.zip
	dns.txt
```

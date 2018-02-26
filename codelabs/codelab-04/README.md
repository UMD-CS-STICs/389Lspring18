# Codelab 4: EC2

### Overview

Today, you'll be working with EC2 to set up and host a full [Wordpress server](https://wordpress.com/)! <!-- You'll be able to view and share it to friends with a domain of your choosing.-->

### Due Date

This code is due on *Thursday, March 1st at 11:59:59PM*.

### Setup

We'll be working heavily from the AWS GUI here, so go ahead and log in with your account.

### Launch an EC2 instance

Launch an Ubuntu Server 16.04 instance on EC2 via the AWS GUI:
- AMI: Ubuntu Server 16.04 LTS 64-bit
- Instance Type: t2.micro
- Configuration Details: Use the defaults
- Storage: **8 GiB** (the default)
- Tags: None
- Security Group: See below
- Key Pair: Use your existing key pair

For the security group, create a new security group and open SSH and HTTP to Anywhere. Go ahead and save this security group with a memorable name, so that you can use it again.

![Security Group](../../../media/codelabs/codelab-04/security-group2.png)

### Elastic IP

So, we now have an instance running on EC2. If we were to stop it from running though, we'd likely be assigned a new pubic IP address from amazon's pool of IP addresses ([they have quite a few](https://ip-ranges.amazonaws.com/ip-ranges.json)). As we talked about in class, internet devices are assigned a Dynamic IP address, because of the limited size of the IPv4 address space. If we want to give a instance a Static IP address (guaranteeing that it won't change), then we can get one using AWS Elastic IP (EIP). After all, we want to have an IP address that we can share (or eventually map a domain name to).

In the [EC2 console](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1), navigate to "Elastic IPs". Click "Allocate new address". Now, right click the EIP and "Associate address", selecting your instance. That's it, you're done. Please note, Elastic IPs are free when associated with devices *in use*, but not if an instance isn't running. To avoid hourly fees, do *release* addresses not in use.

Once you associate the address, notice that the Public IP of your instance has changed to the EIP you just allocated.

Further reading is available [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html).

<!-- NEED TO TRY CONFIGURING MY DOMAIN WITH Route53 BEFORE WRITING
### Your Domain

Register your own domain name at [namecheap.com](https://www.namecheap.com).
-->

### SSH to EC2

Having gotten a static IP address of your EC2 instance, we're ready to advance. Note that you can also use the DNS identifier in place of the IP address ("Public DNS (IPv4)").

![Instance Descriptions](../../../media/codelabs/codelab-04/description.png)

Go ahead and SSH onto your instance. If you run into any problems, see [this section of the EC2 SSH tutorial](../../lectures/lecture-04/ssh.md#common-problems).

```
$ ssh -i <path to keypairName.pem file> ubuntu@<public IPv4 address>
```

There's a lot of useful information here, so take a look around. For example, you can check the rules defined by your security group, get public IP addresses, check which keypair you configured for this instance and you can check on the state of the instance (whether it has finished launching or not, for example).

### Basic LAMP Server on EC2

First thing's first, now that we're on the box let's make sure everything is up to date

```
ubuntu@ip-1-2-3-4:~$ sudo apt-get update
```

We're going to launch a basic LAMP server (Linux, Apache, MySQL, PHP). We're running Ubuntu (a flavor of Linux), but we'll need to install Apache (an HTTP Server), PHP (server-side scripting language), and MySQL (relational DBMS). Run the following command to install all three:

```
ubuntu@ip-1-2-3-4:~$ sudo apt-get install lamp-server^
```

You'll be prompted to create a password for the MySQL root user, do so and write it down; do not leave it blank.

![create-password](../../../media/codelabs/codelab-04/create-password.png)

<!-- TRIED THIS, SEQUEL PRO WORKED BETTER
```
ubuntu@ip-1-2-3-4:~$ sudo apt-get install phpmyadmin
```

![select-apache2](../../../media/codelabs/codelab-04/select-apache2.png)

When prompted, choose the default configuration and create a password

![dbconfig-common](../../../media/codelabs/codelab-04/dbconfig-common.png)

symbolic link
sudo ln -s /usr/share/phpmyadmin /var/www/html/phpmyadmin

sudo apt-get install phpmyadmin php-mbstring php-gettext
sudo service apache2 restart
-->
<!--ubuntu@ip-1-2-3-4:~$ sudo service mysql start-->

Now, let's test to see if our LAMP server is working. Attempt to navigate to your new web server by using either the DNS identifier or public IP address in your browser. You should see a default page stating "It works".

![it-works](../../../media/codelabs/codelab-04/it-works.png)

If you don't see this, then double-check that your security groups opens up port 80.

### Wordpress

Wordpress stores its content in a MySQL database. We now have MySQL installed on your EC2 instance, so let's connect to it using a database client. Depending on your OS, we'd recommend using [Sequel Pro](http://www.sequelpro.com) (Mac OS) and [MySYQL Workbench](http://www.mysql.com/products/workbench/) (Windows/Linux). Both are free.

Create a new connection in your DB client:
- MySQL Host: _127.0.0.1_
- Username: _root_
- Password: _the one you wrote down earlier_
- SSH Host: _the public IP_
- SSH User: _ubuntu_
- SSH Key: _Path to your `your-ssh-key.pem`_

This example is from Sequel Pro

![pro-connection](../../../media/codelabs/codelab-04/sequel-pro.png)

Now you can see the MySQL database running on your EC2 server. Let's create a database for Wordpress to use. You may name it whatever you like, but ensure your encoding is `utf8` and your collation is `utf8_general_ci`.

![Create Database](../../../media/codelabs/codelab-04/create-database.png)

*Note: for security, you generally want to create multiple users on your server, each with limited permissions ("[The Principle of Least Privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)"). In this case, you'd likely have a `mysql` user who is the only user who can access your database, but which can't access anything else on your server. Therefore, if your `mysql` user was compromised, the surface area for an attacker to wreak havoc on your server is limited. We're instead using the root user.*

Now, it's back to the command line to deploy Wordpress. Run the following commands in order. We're loading files into `/var/www/html` because that's where the Wordpress server will host files by default.

```
ubuntu@ip-1-2-3-4:~$ cd /var/www/html
ubuntu@ip-1-2-3-4:~$ sudo wget http://wordpress.org/latest.tar.gz
ubuntu@ip-1-2-3-4:~$ sudo tar -zxvf latest.tar.gz
ubuntu@ip-1-2-3-4:~$ sudo mv wordpress/* .
ubuntu@ip-1-2-3-4:~$ sudo rm -rf wordpress latest.tar.gz index.html
ubuntu@ip-1-2-3-4:~$ sudo service mysql start
ubuntu@ip-1-2-3-4:~$ sudo service apache2 reload
```

Once again we'll, connect to your web server via your browser. You should now see the following Wordpress page! If you still see the "It works" page, try force reloading (`Shift-Cmd-R`, etc.).

![lets-go](../../../media/codelabs/codelab-04/lets-go.png)

Great! Let's set up Wordpress. You nearly have your very own blog running, hosted on EC2.

Click "Let's go" and then fill in the following information. You'll need the name of the database you created earlier and the database password. The username is "root". Everything else you can leave as the default.

![you-will-need](../../../media/codelabs/codelab-04/wordpress-config.png)

Wordpress doesn't have the permissions to write the `wp-config.php` file, so go ahead and create one in `/var/www/html` via the command line.

```
ubuntu@ip-1-2-3-4:~$ cd /var/www/html
ubuntu@ip-1-2-3-4:~$ sudo nano wp-config.php
```

Paste in the provided text.

![copypasta](../../../media/codelabs/codelab-04/copypasta.png)

Go ahead and configure your blog however you like (site name, username, etc.). You'll want to remember that username/password so that you can log into the Wordpress Admin page.

Now, you can go to the Admin page at `http://<your-ip-address>/wp-admin/`) to create posts and manage the blog. You can go to `http://<your-ip-address>/` to view the blog itself.

If everything worked, your page should look something like this!

![wordpress-default-page](../../../media/codelabs/codelab-04/wordpress-default-page.png)

#### First post

While we're here, let's put sometime up to show we can. From the dashboard, navigate to the new post page.

![navigate](../../../media/codelabs/codelab-04/navigate.png)

Use your name as the title, fill the body with arbitrary content, and post.

![new-post](../../../media/codelabs/codelab-04/new-post.png)

View your page; it should now be updated!

![verified-site-example](../../../media/codelabs/codelab-04/verified-site-example.png)

### Amazon Machine Image

That was a lot of work to get our instance just the way we want it!

As instructive as that process is, we probably don't want to have to do that every time we want to launch a Wordpress blog. Is there a way to take a 'snapshot' and save our setup? Yes, with a custom Amazon Machine Image (AMI)! You've already been using custom AMIs, specifically a custom AMI that comes pre-configured with Ubuntu.

Let's make our own. Using the AWS Management Console, navigate to your list of EC2 instances. Select ("Actions" > "Image" > "Create Image")

Configure the new image with a name and description, so that you can tell what the AMI is. AMI creation time will vary, but should only be a few minutes for our task.

Now that you have an AMI created, go ahead and launch it. Navigate to the "AMIs" section here:

![AMI section](../../../media/codelabs/codelab-04/amis.png)

Click "Launch", which will take you to the EC2 launch wizard. Make sure to set the security group to the same security group you used earlier, but otherwise all of the settings should be the same as before.

Once that instance launches, browse to the public IP address of your new instance in your browser. It just works!

You can de-allocate the EIP from your previous instance and allocate it to the new instance. Once you do this, your EIP will now forward traffic to your new instance.

There's a lot of neat things can do with AMIs. You can even sell your AMIs on a marketplace! Feel free to read up more on AMIs [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html).

<!--
if you're not using a static ip, you may can update by modifying the DB

update wp_options set option_value = replace(option_value, 'ec2-<old_ip>', 'ec2-<new_ip>') -->

### Wrapping Up

Leave your content up for us to verify. We'll be looking for your post at an EIP address you will submit.

If you are running any other EC2 instances that you are no longer using, be sure to stop
("Actions" > "Instance State" > "Stop")
or terminate
("Actions" > "Instance State" > "Terminate")
them; else they will eat into your free credit.
<!--
Here are some [ideas](http://www.wpbeginner.com/beginners-guide/top-10-most-important-things-to-do-after-installing-wordpress/) for what to do with your site, now that it's up.
-->
### Submission

You will be submitting a text file called `ip.txt` containing just your Elastic IP address.

Submit this assignment to `codelab4` on the submit server. Upload a zipped directory with the file:

```
<directory id>.zip
	ip.txt
```

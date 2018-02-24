# Codelab 4: EC2

### Overview

Today, you'll be working with EC2 to set up and host a full [Wordpress server](https://wordpress.com/)! You'll be able to view and share it to friends with a domain of your choosing.

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

So, we now have an instance running on EC2. If we were to stop it from running though, we'd likely be assigned a new pubic IP address from amazon's pool of IP addresses ([they have quite a few](https://ip-ranges.amazonaws.com/ip-ranges.json)). As we talked about in class, internet devices are assigned a Dynamic IP address, because of the limited size of the IPv4 address space. If we want to give a instance a Static IP address (guaranteeing that it won't change), then we can get one using AWS EIP (Elastic IP). After all, we want to have an IP address that we can share (or eventually map a domain name to).

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

Make sure to stop ("Actions" > "Instance State" > "Stop") or terminate ("Actions" > "Instance State" > "Terminate") your EC2 instances when you are no longer using them, or else they will eat into your free credit.
<!--
Here are some [ideas](http://www.wpbeginner.com/beginners-guide/top-10-most-important-things-to-do-after-installing-wordpress/) for what to do with your site, now that it's up.
-->
### Submission

There is no submission for this codelab. However, you'll be expected to understand the concepts covered in this codelab (not the commands -- just the concepts).




<!--# LEGACY CODELAB-03

### Webserver on EC2

Let's host a simple website on EC2. On your box, create a simple HTML file. Feel free to put whatever you would like into the file.

```
ec2 ~$ vim index.html
```

```
<html>
	<body>
		<h1>Hello CMSC389L!</h1>
	</body>
</html>
```

Now, start a web server hosted on port 80. This is the default HTTP port, which we opened up in our security group. Python comes with a module which handles all of the networking and web handling necessary to run a simple web server, which we are calling with the `-m` (module) flag.

```

ec2 ~$ sudo python3 -m http.server 80
```

Now, in your browser, go to the public IP or DNS identifier of your EC2 instance, at port 80. If everything went well, you should see your basic website!

You could now go back and edit the security group you created to limit HTTP access to just a specific IP address and you will see that you are no longer able to access this web page.

### EBS Volumes

To see the attached volumes, use the list block devices command:

```
ec2 ~$ lsblk
NAME    MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
xvda    202:0    0   8G  0 disk
└─xvda1 202:1    0   8G  0 part /
xvdb    202:16   0  40G  0 disk
```

As we can see, there are two attached devices (xvda1, xvdb), and one is mounted onto the root directory.

We can mount the root volume again, to look at its contents:

```
ec2 ~$ mkdir ec2-volume
ec2 ~$ sudo mount /dev/xvda1 ~/ec2-volume
ec2 ~$ sudo chown ubuntu ec2-volume
ec2 ~$ ls ec2-volume
bin   dev  home        lib    lost+found  mnt  proc  run   snap  sys  usr  vmlinuz
boot  etc  initrd.img  lib64  media       opt  root  sbin  srv   tmp  var
```

As you can see, this folder now contains the same contents as the root directory, since this volume is now mounted onto both directories.

Go ahead and unmount this volume from that folder:

```
ec2 ~$ sudo umount ~/ec2-volume
```

Let's inspect the contents of that EBS volume (change the device name based on the output of `lsblk`):

```
ec2 ~$ sudo file -s /dev/xvdb
/dev/xvdb: data
```

The output indicates that the volume has not been initialized with a file system, yet.

Let's compare that with the root device:

```
ec2 ~$ sudo file -s /dev/xvda1
/dev/xvda1: Linux rev 1.0 ext4 filesystem data, UUID=3e13556e-d28d-407b-bcc6-97160eafebe1, volume name "cloudimg-rootfs" (needs journal recovery) (extents) (large files) (huge files)
```

This indicates that xvda1 contains an ext4 file system. We want to create something similar on the EBS volume we mounted (xvdb).

```
ec2 ~$ sudo mkfs -t ext4 /dev/xvdb
mke2fs 1.42.13 (17-May-2015)
Creating filesystem with 10485760 4k blocks and 2621440 inodes
Filesystem UUID: dceca987-ea34-43f1-839f-abbb54b7ed8b
Superblock backups stored on blocks:
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
	4096000, 7962624

Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done
ec2 ~$ sudo file -s /dev/xvdb
/dev/xvdb: Linux rev 1.0 ext4 filesystem data, UUID=dceca987-ea34-43f1-839f-abbb54b7ed8b (extents) (large files) (huge files)
```

Now, if we mount this volume we will be able to read and write into it:

```
ec2 ~$ sudo mount /dev/xvdb ~/ec2-volume
ec2 ~$ sudo chown ubuntu ec2-volume
ec2 ~$ ls ec2-volume/
lost+found
ec2 ~$ echo "Hello World! From CMSC389L" > ec2-volume/hello.txt
ec2 ~$ ls ec2-volume/
hello.txt  lost+found
ec2 ~$ more ec2-volume/hello.txt
Hello World! From CMSC389L
```

Let's move this volume onto a new instance. Go ahead and unmount it before exiting:

```
ec2 ~$ sudo umount ~/ec2-volume
ec2 ~$ exit
```

Launch a new instance, with the same settings as above, except without the EBS volume.

In the Management Console, under "Volumes", detach the EBS volume ("Actions" > "Detach Volume") from the first instance. Then attach it to the second instance ("Actions" > "Attach Volume").

SSH onto the box and run `lsblk`. You should see the newly attached volume. Mount the volume, and you will see `hello.txt`!

You could also terminate this instance, and all data in this volume will live on.

Keep at least one instance around.

### IAM Roles

Just like we created an IAM user that we could sign in with to access our AWS account via the CLI, we can create IAM roles to give to EC2 instances.

These IAM roles/users can be given policy documents which specify exactly what permissions they have.

We will create an IAM role for accessing S3 documents, and then assign this role to a new EC2 instance.

First, SSH onto one of your previous EC2 instances. Attempt to look at the list of buckets in S3:

```
ec2 ~$ sudo apt install -y awscli
ec2 ~$ aws s3 ls
Unable to locate credentials. You can configure credentials by running "aws configure".
```

By default, your EC2 instance does not have access to any other AWS resources. We could run `aws configure` and give it the credentials we created for the CLI, however this is a bad practice. If an EC2 instance were to be compromised, an attacker would have access to admin-level credentials and could export them and use them elsewhere. Plus, if we found out, we would have to change the AWS configuration on every single EC2 instance we had running (if we are running a consumer internet company on AWS, that could be in the 100s+!). Instead, AWS roles are managed by AWS and no key is exposed in plaintext on our instance.

Go ahead and create the IAM role via the Management Console. Open the IAM service and go to the "Roles" tab. Select the correct IAM role type: "Create Role" > "AWS Service" > "EC2". On the permissions tab, search for the "AmazonS3ReadOnlyAccess" policy. Go ahead and give it a name and save the new role.

This policy documents looks like this:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*"
            ],
            "Resource": "*"
        }
    ]
}
```

As you can see, it enables the S3 Get and List operations on any AWS resource.

Go and create a new EC2 instance, with the same settings as before (minus the EBS volume), except on the "Configure Instance Details" page, select your s3-read-only policy in the "IAM role" dropdown.

SSH onto this new instance.

```
ec2 ~$ sudo apt install -y awscli
ec2 ~$ aws s3 ls
2017-09-08 12:30:19 cmsc389l
2017-09-12 13:27:27 cmsc389l-colink
2017-09-13 11:53:39 cmsc389l-colink-codelab-02-trail
2017-09-13 16:13:03 cmsc389l-colink-website
...
```

As you can see, your EC2 instance can now access your S3 data, without any form of credentials on the EC2 instance:

```
ec2 ~$ aws configure
AWS Access Key ID [None]:
AWS Secret Access Key [None]:
Default region name [None]:
Default output format [None]:
ec2 ~$ ls ~/.aws
ls: cannot access '/home/ubuntu/.aws': No such file or directory
ec2 ~$ echo $AWS_ACCESS_KEY_ID

ec2 ~$  echo $AWS_ACCESS_SECRET_KEY

```

We can go ahead and use this to sync in everything from the S3 website bucket onto our instance:

```
ec2 ~$ mkdir website
ec2 ~$ aws s3 sync s3://cmsc389l-colink-website website
...
ec2 ~$ ls website
apply.html  assets  catalog.html  CNAME  contact.html  css  faq.html  fwe  index.html  js
```

If you run a Python server in the `website/` directory, and visit the IP address via your browser (`http://<ip address>/website/`), you'll see the STICs website again!
EIP -->

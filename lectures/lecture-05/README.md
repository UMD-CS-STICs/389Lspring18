# Lecture 5 Notes

### Part 1: Setup

Go ahead and launch an EC2 instance and SSH onto it by following the instructions [here](../lecture-04/setup.md).

Make to open up SSH and HTTP to all addresses.

### Part 2: Checking Hardware

SSH onto your new instance:

	$ ssh -i your-ssh-key.pem ubuntu@your-ip-address

Inspect the CPU/memory:

	$ sudo lshw

Inspect the disk storage:

	$ lsblk


### Part 3: Running a Basic Web Server

Create a simple HTML file:

	$ echo "Hello World! From <your name>" > index.html

OR

	$ vim index.html

Now run a Python HTTP server on port 80:

	$ sudo python3 -m http.server 80

Navigate to your IP address via your browser.

Attempt to navigate to my website via the IP address on the board.

### Part 4: Experimenting with Security Groups

Edit your security group to limit HTTP access to just your IP address.

You can double check that it matches your IP address by [googling "What's my IP address"](https://www.google.com/search?q=What%27s+my+IP+address).

Can you access your neighbors site?

Attempt to navigate to my website via the IP address on the board. Does it still work?

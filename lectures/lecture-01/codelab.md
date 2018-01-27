# Codelab 1: Python 101

### Due Date

This codelab is due on *Thursday, Febuary 1st at 11:59:59PM*.

### Goal

In this codelab, you'll learn (or review!) the basics of Python. We will be using Python throughout this class to build projects with AWS. Starting with next week's codelab, we will also be using the [boto3](https://github.com/boto/boto3) library, which is the official AWS SDK for Python.

### Getting Started

##### Environment Setup

To get started, you will need to set up your local development environment. Follow the instructions here: [Environment Setup](https://github.com/UMD-CS-STICs/389Lspring18/env.md).

##### Download Starter Code

For codelabs in this class, you will want to clone the [class repository](https://github.com/UMD-CS-STICs/389Lfall17) from GitHub onto your computer:

	$ git clone https://github.com/UMD-CS-STICs/389Lfall17.git

Each week, when new content is pushed into this repository, you'll need to pull in these changes. All you need to do is run:

	$ git pull

This is a good time to remind you to not publically share any of your solutions to these codelabs. However, you are more than welcome to collaborate with other students in this class.

### Python

#### Learn Python in Y Minutes (Required)

Since you are already familiar with Ruby from CMSC330, then you mostly just need to learn the syntactical differences. 

There's no faster way for that then the "Learn X in Y Minutes" tutorials. Go ahead and read through the Python 3 tutorial here:

https://learnxinyminutes.com/docs/python3/

I would heavily recommend that you open up a Python REPL to experiment with the Python language while reading this tutorial:

	$ python
	Python 3.6.2 (default, Aug 21 2017, 15:27:07)
	[GCC 4.2.1 Compatible Apple LLVM 8.1.0 (clang-802.0.42)] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	>>>

Even if you are already familiar with Python, I'd still recommend that you skim through this tutorial because it contains quite a few useful nuggets that can level up your Python.

### More on Python (Optional)

If you would like to take a deeper dive into the internals of Python, I would recommend checking out the following resources (read: skimming the parts that interest you!):

- [Python Library Reference](https://docs.python.org/3/library/index.html)
- [Python Language Reference](https://docs.python.org/3/reference/index.html)
- [Getting started with Python internals](http://akaptur.com/blog/2014/08/03/getting-started-with-python-internals/)

### Assignment

To give your new Python knowledge a test drive, you're going to write a few simple functions.

For this codelab, we'll be working in `codelabs/codelab-01/`.

`functions.py` contains a few functions that you will need to implement:

1. `foobar_flip(value)`
2. `string_compress(string)`
3. `fibonacci(n)`

`test.py` contains the public tests that you should pass in order to get full credit.

To run the tests:

	$ python tests.py

All of the test cases are independent, so feel free to implement the functions one at a time.

You'll see a message like this when you've passed all of them:

	$ python test.py
	........
	----------------------------------------------------------------------
	Ran 8 tests in 0.002s

	OK

#### Grading

For this codelab, you will get full credit if you complete all the required public tests.

If some codepath is not tested, such as the behavior of `foobar_flip` when a value is provided that is not "foo" or "bar", then you are free to handle it however you would like. Pick something reasonable, like raising a `ValueError`.

#### Submission

To submit this codelab, zip the `codelab-01` folder and upload it to the [submit server](https://submit.cs.umd.edu/).

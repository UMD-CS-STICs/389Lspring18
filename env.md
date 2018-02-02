# Environment Setup

## Instructions

#### Platform Setup

##### macOS

You should be good to go. 🎉

##### Linux

> If you follow these instructions, check in with the TAs to let us know if they do/don't work!

I'm going to give instructions for Ubuntu 16.06.

First update your package repository:

	$ apt-get update

Then install a few packages:

	$ apt-get install -y git zsh make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev tree jq

You should be good to go! Skip ahead to the `Python` installation instructions below.

##### Windows

> If you follow these instructions, check in with the TAs to let us know if they do/don't work!

If you are on Windows 10 and you don't already have the Linux subsystem installed on your computer, go ahead and follow the instructions here: [Install the Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

> **If you are not on Windows 10**, you are going to want to just use Vagrant. There are some instructions [here](https://umd-cs-stics.gitbooks.io/cmsc389l-fall2017/content/lectures/lecture-01/codelab.html), from a previous offering of CMSC389L that used Vagrant.

Once you have the Ubuntu app installed, you can just follow the Linux instructions above. All of the TAs use macOS, so let us know if we can improve these instructions at all. Much appreciated!

#### Python

We will use [`pyenv`](https://github.com/pyenv/pyenv) to manage various versions of Python installed locally. For example, macOS comes with a pre-installed (usually outdated) version of Python. We'll be using Python 3.6.2.

First, install `pyenv`:

	$ curl -sL https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
	
Next, add the following lines to your `~/.bashrc`:

> **If you use Terminal.app on macOS**: Edit `~/.bash_profile` instead as Terminal opens a login shell for every new terminal window. Though you should consider just moving over to [iTerm2](https://www.iterm2.com/).

	export PATH="$HOME/.pyenv/bin:$PATH"
	eval "$(pyenv init -)"
	eval "$(pyenv virtualenv-init -)"

Then, load those changes from your `.bashrc` and verify that `pyenv` is functioning:

	$ source ~/.bashrc
	$ pyenv versions

Now, go ahead and install Python:

	$ pyenv install 3.6.2
	$ pyenv global 3.6.2

You can check that this worked by running:

	$ python --version

Note that whenever you run Python, it will now use this version as the default. However, you can also set a directory-local version using the `pyenv local <python version>` command.

#### Pip

You will also be using [`pipenv`](https://github.com/pypa/pipenv) to manage pip packages.

If you are on macOS, run the following:

	$ brew install pipenv

Otherwise, run the following:

	$ pip install pipenv

To install the packages for a given codelab, run the following:

```
$ pipenv install
```

#### AWS

You will also need to set up the AWS CLI. To install the CLI:

	$ pip install awscli
	$ aws --version

Now, set up your default region and your AWS credentials by running:

	$ aws configure

## Warnings

In the previous offering of this class, we had a few students accidentally commit their AWS credentials to a public GitHub. A variety of automatic scrapers by malicious folks are out there constantly checking GitHub for slip-ups like this. 

So be careful about what you commit!!

Previous groups had hackers rack up $10k+ charges on their account (thankfully AWS support covered these charges for them).

If you make this mistake ([it happens](https://github.com/search?utf8=%E2%9C%93&q=remove+aws+credentials&type=Commits)), change your access credentials and revert the commits. You can temporarily make that repo private in the meantime while you fix the git history.

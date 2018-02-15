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

Once you have the Ubuntu app installed, you'll likely need to create a new non-root user that you will login as. Check out these [instructions](https://www.digitalocean.com/community/tutorials/how-to-add-and-delete-users-on-ubuntu-16-04).

From here, you can just follow the Linux instructions above. All of the TAs use macOS, so let us know if we can improve these instructions at all. Any feedback here is much appreciated!

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

To verify the installation, run:

```
$ pipenv --version
```

##### How does pipenv work?

###### Some Context

Normally in Python, you use a `requirements.txt` file to track your project's dependencies. ([An example](https://github.com/aws/aws-cli/blob/develop/requirements.txt) from `aws-cli`) You would run `pip install -r requirements.txt` to install all dependencies. Easy enough.

However, this doesn't work well when you have multiple Python projects on your system. Some of those packages may collide: for example, possibly you want version `1.4.3` of `package-a` for Project 1, but version `1.5.0` for Project 2. You'd have to pick!

Other package managers solve this by storing your dependencies in the same directory as your project. For example, Node's package manager, `npm`, uses a `node_modules` folder and your packages are accessed from that. Therefore, every package can have its own versions of packages.

In Python, the alternative is to use `virtualenv`. This does something similar to `npm` in that it creates a local environment for every Python project. Once you "activate" that local environment, you can then install your Python packages normally.

This separates **global state** from **local state** and is quite important in setting up a good development environment.

However, managing `virtualenv` can be a pain. It's easy to accidentally forget to activate your environment and accidentally install all of your packages into your global Python environment (not great).

Thus, `pipenv`.

###### Usage

`pipenv` introduces a `Pipfile`. It's a deterministic version of `requirement.txt`, and you can read more about it [here](https://github.com/pypa/pipfile).

All codelabs will ship with a `Pipfile`. You can install the specified packages via:

	$ pipenv install

This creates a local environment for you with all of the packages you need already installed.

To access this environment, run:

	$ pipenv shell

*That's it!*

If you want to install other packages (like `python-magic`), just run:

	$ pipenv install python-magic

If you run these install commands outside of your local environment, `pipenv` is still smart enough to figure out which environment to install that package into (based on the location of the `Pipfile`).

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

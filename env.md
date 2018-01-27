# Environment Setup

## Instructions

#### Python

We will use [`pyenv`](https://github.com/pyenv/pyenv) to manage various versions of Python installed locally. For example, macOS comes with a pre-installed (usually outdated) version of Python. We'll be using Python 3.6.2.

First, install `pyenv`:

> **Note**: You will need to install `curl` and `git` if they aren't already installed on your computer (they probably are).

	$ curl -sL https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
	
Next, add the following lines to your `~/.bashrc` (Note that on OSX, you should edit '~/.bash_profile' instead as Terminal opens a login shell by default)  :

	export PATH="$HOME/.pyenv/bin:$PATH"
	eval "$(pyenv init -)"
	eval "$(pyenv virtualenv-init -)"

Then, load those changes from your `.bashrc` and verify that `pyenv` is functioning:

	$ source ~/.bashrc
	$ pyenv versions

Now, go ahead and install Python:

	$ pyenv install 3.6.2
	$ pyenv global 3.6.2

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

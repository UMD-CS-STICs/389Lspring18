# Environment Setup

## Instructions

We will use `pyenv` to install Python 3.6.2. See: https://github.com/pyenv/pyenv

```bash
$ # You may need to install curl.
$ curl -sL https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
$ # Swap .bashrc with .zshrc, etc. depending on what shell you use.
$ cat >> ~/.bashrc <<'EOL'
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
EOL
$ source ~/.bashrc
$ # Make sure pyenv installed correctly.
$ pyenv --version
$ pyenv install 3.6.2
$ pyenv global 3.6.2
```

You will also be using `pipenv` to manage pip packages.

```
$ TODO
```

To install the packages for a given codelab or project, run the following from within it's directory:

```
$ TODO
```

You will also need to set up the AWS CLI. To install the CLI:

```
$ TODO
$ TODO: configure us-east-1
$ TODO: set up auto-completion
```

Place a file named `aws.credentials` in your `~/.aws` directory with the following contents (change the access key and secret access key):

```
[default]
aws_access_key_id = AIUBG23BWONGOIWEN83N
aws_secret_access_key = oinwgoi2n3th040BIGUEBW4t8h493g3nUUB023jn
```

Add the following to a file called `~/.aws/config`:

```
[default]
region=us-east-1
```

## Warnings

In the previous offering of this class, we had a few students accidentally commit their AWS credentials to a public GitHub. A variety of automatic scrapers by malicious folks are out there constantly checking GitHub for slip-ups like this. 

So be careful about what you commit!!

Previous groups had hackers rack up $10k+ charges on their account (thankfully AWS support covered these charges for them).

If you make this mistake ([it happens](https://github.com/search?utf8=%E2%9C%93&q=remove+aws+credentials&type=Commits)), change your access credentials and revert the commits. You can temporarily make that repo private in the meantime while you fix the git history.

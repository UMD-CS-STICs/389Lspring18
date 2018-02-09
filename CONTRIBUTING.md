# CMSC389L Contributing Guide

You will need to install GitBook: https://github.com/GitbookIO/gitbook/blob/master/docs/setup.md

To run the GitBook server locally, run the following from the root directory of this repo:

```
$ gitbook serve
```

On commit to master, the main GitBook will be updated.

You will need to create an [iFramely](https://iframely.com/) account to test that it properly renders slides.com slides and YouTube videos.

Once you have an API key, you can run the GitBook as follows:

```
$ IFRAMELY_APIKEY=23porgsyum203r0jf02jf gitbook serve
```

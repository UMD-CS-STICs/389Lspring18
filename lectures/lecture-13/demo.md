# Elasticsearch Demo

### Overview

We're going to create a search engine on the UMD CS Professor's course webpages, along with a search engine on their names, using AWS Elasticsearch service.

### Setup

First, open ES: https://console.aws.amazon.com/es/home?region=us-east-1

And make a `git pull` to the 389L repo to get the code files you'll need for this project.

Open a pipenv environment:

```
$ pipenv shell
...
$ pipenv install
...
```

### Elasticsearch Domain

We're going to need an Elasticsearch domain. You can use the default settings, except:

- Step 3
  - **Network Configuration**: Set this to **public access**. This is just for testing, and you should never do this with production data.
  - **Access Policy**: Select a template > Allow open access to the domain. Again, never do this in practice, but this will allow us to easily test our ES domain without worrying about credentials.

This takes about 10m to set up.

### Elasticsearch Demo

Import the following collection into Postman: https://www.getpostman.com/collections/cf3c1415f7039a925b30

You can import it by going to `Import > Import from Link`.

Run through this collection to get a feel for how Elasticsearch works.

### Scrape Faculty Data

Run the following to scrape faculty data from the CS webpage:

```
$ python preprocess-faculty.py
...
$ python scrape.py
...
```

You will now have a `data/faculty-site-data.json` file containing a bulk upload script that can be inserted into Elasticsearch.

### Bulk Insert

Run the following command to insert the faculty data into a new index:

```
$ curl -X POST "<es endpoint>/_bulk" --data-binary "@./data/faculty-site-data.json" -H "Content-Type: application/json"
```

> **Note**: If you need to clear your index, you can run a deletion command as follows: `$ curl -X DELETE "<es endpoint>/umdcs/"`

### Let's search it!

You can use Postman or `curl` from this point forward.

Create a POST endpoint to `/umdcs/faculty/_search` and specify your query as the body of the POST request.

For example:

```
{
    "query": {
        "match" : {
            "text" : {
                "query" : "Cybersecurity",
                "operator" : "and"
            }
        }
    }
}
```

...would search for all Professor's with a research background in cybersecurity!

We can add the `fuzziness` parameter to match misspellings:

```
{
    "query": {
        "match" : {
            "text" : {
                "query" : "Cyberecurity",
                "fuzziness": "AUTO",
                "operator" : "and"
            }
        }
    }
}
```

**Challenge**: Write a query to search for Professor's by name, and create a script (bash, python, etc.) that takes a query as a parameter and prints out a list of

For example:

```
$ python search.py Neil
Neil Spring: http://www.cs.umd.edu/people/nspring/
FooBar Neily: http://www.cs.umd.edu/people/foobar/
...
```

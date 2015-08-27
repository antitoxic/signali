
# Signali
Web app for browsing, rating and commenting contact points of organisations.

** IN ACTIVE DEVELOPMENT. DO NOT USE UNTIL STABLE **

## Related projects
Themes are not bundled. Main theme is located at: [obshtestvo/signali-theme](https://github.com/obshtestvo/signali-theme)

Place the default or your theme in the `themes` directory and set its name as value for `THEME` setting. 

## Setup
### OS

> The following is not made into a script, because it serves educational purposes

 - python3
 - python3 virtualenv
 - postgres
 - redis
 - image manupulation libraries

```sh
# depending on distribution you might want to install 
python-dev, python-devel, or python3-devel libpq-dev
postgresql-devel postgresql-... python3-venv
# for correct mimetypes installing or updating the `mailcap` package on a RedHat-based distribution, or `mime-support` on a Debian distribution.

sudo su - postgres
psql
SHOW hba_file;
vim <the path to hba file>
change `host all all 127.0.0.1/32 ident` to md5

# image manipulation support
# for debian-based: apt-get install libjpeg62 libjpeg62-dev zlib1g-dev

# redis should be smth like: apt-get install redis-server
```

### Project

> The following is not made into a script, because it serves educational purposes
 
```sh
cd <project dir>
# create virtualenv (skip if you already have one)
python3 -m venv ./env/.virtualenv
# activate virtual environment (if not already active)
source env/.virtualenv/bin/activate # (or activate.fish)
# install server requirements
pip install -r env/requirements.txt # (if errors appear, try installing only Django first)
# install client requirements
(cd src/signali.bg-theme && bower install)
# create postgres user & database
sudo su - postgres
createuser -S -D -R -P signali
createdb -O signali signali -E utf-8 -l bg_BG.utf8 -T template0
# set local settings
cp env/.django-sample env/.django
...edit .django to your needs ....
# include src in PYTHONPATH
# for bash shell: export PYTHONPATH=$PWD/src
# for fish shell: set -x PYTHONPATH $PWD/src
# initialise db
python manage.py migrate
# load data seed
bash env/utils/load_dev_fixtures.sh
# run signali
python manage.py runserver
# go to http://127.0.0.1:8000/
```

#### Deployment
You must have a cloned version of the repo on your deployment server and exported sensitive settings as environment variables or
defined as `env/.django` entries.

After this you just simply run:

```
cd env
fab debloy:live,static # or fab deploy:live
```

from your local install.

## Dev hints

### Architecture decisions

#### Conventions
 - This project tries to follow the [12factor](http://12factor.net/) specs with addition of some 
 **REST**ful conventions provided by the [django-restful](https://github.com/obshtestvo-utilities/django-restful) package. 
 Other common good practices are also followed.
 Example conventions followed:
  - not in the way, only use what you want from the conventions, i.e. it can work as standard django install
  - handle all errors in one place
  - all requests and all calls should be as stateless as possible, pass what you need
  - all http methods should be simulatable 
  - response format should be extracted from http header but should also be simulatable
  - template names can be auto-detected based on Controller name and request method, so they should 
  - developers should have full control of data transformation in the template for any format
  - DRY, use single codebase where possible
  - always think modular, extract topical, not simply common logic
  - if requesting html (commonly web) always redirect after anything other than 'GET'
  - let html be html, don't use framework-specific or package-specific html generators (like form-element generators)  
  
#### Specificity
 - Sensitive settings and those specific to deployment are retrieved from ENV variables or `.django` file in the `env`
 directory
 - If you are making a deployment you shouldn't have to modify the `src` directory. The `env` directory holds
   all environment-specific settings. If this is not the case please open an issue or submit a pull request. Changing
   things in `src` should only happen when you want to change the functionality of the project 
 - `env` directory holds settings specific to deployment environment:
  - server settings - debian install script, nginx sample, uwsgi sample, 
  - project dependencies descriptor
  - environment-specific project settings
  - the downloaded project dependencies
 - `src` directory is not "*just API*". It holds all sorts server-code and non-html templates
 - `themes` directory is where you can place your themes
 - The `user` and `security` apps has similar purposes 
   - The main difference between `user` app and `security` app is that `user` app includes the more project-specific 
   user things (like prepping pages and forms for login, profile editing, and making use of `security` app ).
   The `security` app also includes user-related stuff but it limits itself to more generic and security-related 
   logic (auth, validation, tokens, logout). 
   - The logic for the data checkpoint in the signup process is in `user` app instead of `security` app. The logic is closer to
   the security app because it handles required data before the user is allowed to register, **but** that data usually changes
   from project to project which goes against keeping `security` app the more reusable one

#### Database

If you're not familiar with Postgres but you are with Mysql [this article could be useful](http://crashmag.net/mysql-and-postgresql-rosetta-stone).

#### Settings in environment variables
The following will read a `.ini`-like file and export each definition as environment variables.
```
export $(cat ./env/.django | xargs)
```

### Useful packages for debugging
 - Login as another user: [impersonate](https://bitbucket.org/petersanchez/django-impersonate) or [hijack](https://github.com/arteria/django-hijack)
 - Security checkup: https://github.com/carljm/django-secure

### Common scenarios

#### Handling success or error, in a django view:

Example 1:

```python
failure = VerboseException("Error occurred") # prepare for failure
# ... error happens
failure.add_error('password', "Password too long")
failure.add_error('email', "Not a valid email")
raise failure
# ...

```

The code above will render a `error/get` template, *(or other defined by the `RESTFUL_ERROR_TEMPLATE` setting)* and
pass all errors to it.

Example 2:

```python
failure = VerboseHtmlOnlyRedirectException("Error occurred").set_redirect('route-name')
# ...
failure.add_error('password', "Password too long")
failure.add_error('email', "Not a valid email")
raise failure
# ...

```

The code above will behave the same as "Example 1" unless the client requests data in html format (*or doesn't specify format*),
which is the common case for browsers.
If the client requests html response the code above will put all errors in a session variable 
and redirect to `route-name`. Useful when you want to show errors in the same form the input originated from.
 

#### Posting to a page and handling success, in a django view:

Example 1:

```python
return {
  'result': "Successfully created a new user", 
  'user_id': 2, 
}
```

The code above will render a template named the same as the method, located in a directory named the same as the class.
I.e.: Rendering `users/post.html`. 

> **Note:** The file extension is automatically added based on the "Accepted-Type" header.

Example 2:

```python
return HtmlOnlyRedirectSuccessDict({
  'result': "Successfully created a new user", 
  'user_id': 2, 
}).set_redirect('route-name')

```

The code above will behave the same as "Example 1" **unless** the client requests html response. 
If the client requests html response the code above will put all data in a session variable and 
redirect to `route-name`. Useful when you want to redirect users to the page they originated from.
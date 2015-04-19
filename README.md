
# Signali
Web app for browsing, rating and commenting contact points of organisations.

** IN ACTIVE DEVELOPMENT. DO NOT USE UNTIL STABLE **

## Related projects
Themes are not bundled. Main theme is located at: .....

Place the default or your theme in the `themes` directory and set its name as value for `THEME` setting. 

## Setup
### OS

```sh
# depending on distribution you might want to install 
python-dev, python-devel, or python3-devel
postgresql-devel

sudo su - postgres
psql
SHOW hba_file;
vim <the path to hba file>
change `host all all 127.0.0.1/32 ident` to md5
```

### Project

> The following is not made into a script, because it serves educational purposes
 
```sh
cd <project dir>
# create virtualenv (skip if you already have one)
python3 -m venv ./env/.virtualenv
# activate virtual environment (if not already active)
source env/.virtualenv/bin/activate
# install server requirements
pip install -r env/requirements.txt
# install client requirements
(cd src/signali.bg-theme && bower install)
# create postgres user & database
sudo su - postgres
createuser -S -D -R -P signali
createdb -O signali signali -E utf-8 -l bg_BG.utf8 -T template0
# create db
python manage.py migrate
# run app
python manage.py runserver
# go to http://127.0.0.1:8000/
```

#### Production notes:

```
python manage.py collectstatic
```

## Dev hints:

The following will read a `.ini`-like file and export each definition as environment variables.
```
export $(cat path/to/env/file | xargs)
```

### Architecture decisions

 - If you are making a deployment you shouldn't have to modify the `src` directory. The `env` directory holds
   all environment-specific settings. If this is not the case please open an issue or submit a pull request. Changing
   things in `src` should only happen when you want to change the functionality of the project 
 - `env` directory holds settings specific to deployment environment:
  - server settings - debian install script, nginx sample, uwsgi sample, 
  - project dependencies descriptor
  - the actual project dependencies
  - environment-specific project settings
 - `src` directory 
 - `src` directory is not "*just API*". It holds all sorts server-code and non-html templates
 - `themes` directory is where you can place your themes
 
 
### Common scenarios

#### Posting to a page and handling error, in a django view:

Example 1:

```python
failure = VerboseException("Error occurred")
# ...
failure.add_error('password', "Password too long")
failure.add_error('email', "Not a valid email")
raise failure
# ...

```

The code above will render a `error/get` template, *(or other defined by the `RESTFUL_ERROR_TEMPLATE` setting)* and
pass all error to it.

Example 2:

```python
failure = VerboseHtmlOnlyRedirectException("Error occurred").set_redirect('route-name')
# ...
failure.add_error('password', "Password too long")
failure.add_error('email', "Not a valid email")
raise failure
# ...

```

The code above will behave the same as "Example 1" unless the client requests html response.
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
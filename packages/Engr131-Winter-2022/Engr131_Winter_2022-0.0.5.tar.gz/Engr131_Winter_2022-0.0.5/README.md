# ENGR_131_dev

## to build the book

 jupyter-book build ./jupyterbook 

 ## to upload to git pages

 ghp-import -n -p -f jupyterbook/_build/html

 ## Builds the wheel

 python3 jupyterbook/src/setup.py sdist bdist_wheel

0TK706uIobPn
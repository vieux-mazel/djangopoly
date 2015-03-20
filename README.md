# Djangopoly
----
Monopoly implementation in Python and Django. Live demo at: http://djangopoly.shtarkov.net/

Course project for the Web Application Development course at the University of Glasgow.
Developed by Christian Shtarkov, Atanas Penchev and Ian Denev.

## Deployment

You'll need Django 1.7 and Python 2.7+ installed.

    $ git clone https://github.com/cshtarkov/djangopoly.git
    $ cd djangopoly
    $ python manage.py migrate
    $ python manage.py runserver

To use the MySQL backend:

    $ git checkout trans-deployable
    $ python manage.py migrate

The live demo at http://djangopoly.shtarkov.net/ uses the MySQL backend and Apache with mod_wsgi.

## Usage

Visit the home page to create a new private or public game, or to join a random existing public game.
To invite another person to join your game, simply give them the link you have.


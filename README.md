
GraphQL example app
===================================

Python 3.7 implementation of a graphene-django server which allows to query and mutate Users in PostgreSQL 11 database.

About
-----

See ``requirements.txt`` for installed packages and the used versions.

Example guide based on Ubuntu 18.04 installation

Installing PostgreSQL 11
-----

    echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list

    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    
    sudo apt-get update
    
    sudo apt-get install postgresql-11 postgresql-server-dev-11
    
    sudo -u postgres psql postgres
    
    create user user with password 'password';
    
    alter role user set client_encoding to 'utf8';
    
    alter role user set default_transaction_isolation to 'read committed';
    
    alter role user set timezone to 'Asia/Almaty';
    
    create database database owner user;
    

Getting source from the git
---------------------------

Install the required ``requirements.txt`` in the global Python 3
environment or in a virtual Python 3 environment. The latter has the advantage that
the packages are isolated from other projects and also from the system wide
installed global once. If things get messed up, the virtual environment can
just be deleted and created from scratch again.

    cd ~
    mkdir graphql_users
    cd graphql_users
    git clone https://github.com/A-Iskakov/graphql_users.git
    sudo pip3 install -r requirements.txt
    
**Run tests**

    python3 manage.py test --pattern="tests*.py"



**Launch django server**

    python3 manage.py 0.0.0.0:8000
    
**Open browser at localhost:8000/graphql/**

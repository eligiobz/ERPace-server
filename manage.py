#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='psql_repo', url='postgresql://mloki:?!L0k13t0@localhost/mobilerp', debug='False')

# Why Did We Do That (WD2T)?

This is a very simple backend for an idea I had around maintaining decision records.
It was mostly another excuse to try out different approaches to unit testing than I'm
used to and see what FastApi is like as a framework.

I'm used to writing tests that are very much class level tests which I'm not always
convinced are useful and/or targeting the correct unit. In this case I've gone with the
"functionality as the unit" idea.

## To Run

The mongo database is running in docker compose and the actual server as just a python process.
It'd be good to dockerise everything.

1. `docker-compose -p wd2t up -d`
2. `pipenv run uvicorn wd2t.main:app --reload`

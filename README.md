# Electronic-Survey-Delivery

This is an early incarnation of WebSuvey form circa mid 2000.

Written in Perl 5 with a dash of 4 (see &'s in front of a function calls) by
AC to win our first survey job.

No warnings, no strict, no tainting, but at least there are DBI query params.

It originally connected to an MS Access DB so it could be demoed for potential
clients on a laptop with no network connectivity. Sqlite has been substituted
for MS Access, a couple of show stopper bugs fixed, and a few nasty layout
issues have been fixed but it is otherwise it is as it was found.

## Check it out

`docker-compose up --detach --build`

`open http://localhost:8080`

Username: `0001 - 0010`
Passwords:`pw1  - pw10`

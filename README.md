# EM (Engineering Manager)
Engineering manager flywheel for capturing everything that I generally do as an engineering manager.

# APPS
It's a set of command-line apps that share similar interfaces.

## NOTES (general notes for context, optimized for tag search and full-text search)

this could take two options, quick notes and long notes, in a manner similar to git commit. 
quick notes would be a single line, long notes would be a multiline message.

```
em nt 'echo r > /var/run/uwsgi/app.fifo; # restart a uwsgi process' -t uwsgi # for single line quick
em nt # to open up a program for multi-line notes
em nt -m "use xor filters for fast search. it works like a bloom filter. it's a space efficient, fast, probabilistic data structure." -t "full-text-search"
em nt -m "look at meilisearch or tantivy for rust-based full-text search crates" -t "full-text-search" "rust" "search"
em nt -m "don't do this anymore" -t stop-doing
```

## FEEDBACK
Capture feedback for direct reports as it comes up. Inspired by Mark Horstman's book "The Effective Manager".

```
em fb -h
    fb p # gave positive feedback
    fb c # gave constructive feedback
    fb n # took a note of something to discuss later
    fb a # took a note of an accomplishment to be used in a review, for promotion

em fb p -p 'matt.m' -m 'matt was giving wenwen good feedback, really put in the effort to help wenwen grow'
em fb c -p 'matt.m' -m 'matt was late this morning again'
em fb n -m 'had a meeting and wenwen was late' -p wenwen
em fb n -m 'had a meeting and wenwen was late' -p wenwen -t scalability
em fb report -p wenwen # show all feedback for wenwen
```

## TASK TRACKER (Work)
Create tasks and log time on them. time is logged against tasks. time can be bounded or unbounded,
in that you can start a task and end it, and the time duration will be logged automatically, or you 
can just log time against a task without explicitly starting or ending it.

```
em tt 'do a thing' -t 1h # create a task and add 1 hour to it, bounded. if the task already exists, log another hour to it.
em tt -s 'do a thing 2' # start a new task and capture the timestamp for start, unbounded
em tt -p 'do a thing 2' # pause the task and capture the duration of time, bounded
em tt -e 'do a thing 2' # end the task and capture the timestamp for end and the duration of time from start to end
em tt -lo # list open tasks
em tt -lc # list completed tasks
em tt -la # list all tasks
em ttr # show a report of all tasks, time logged, etc.
em ttr -w # show a report scoped to the week
em ttr -m # show a report scoped to the month
```

## REMEMBER/REMINDER
```
em rm -m "get build out" --due today@5pm -w 100 -r 1hr -rb 1hr # remind in one hour to get the build out, remind one hour before it's due, give weight of 100 in todo list (ordered by reverse weight)
em rm -m "read brendan greg article on performance" -r 1d # remind me in one day to read the article
em rm -m "watch the video on the new feature" --due "15/12/2020" -rb 1d # remind me 1 day before the due date
em rm # show all upcoming reminders
em rm "get build out" -b 1d # bump the reminder for "get build out" by one day
```

## TODO (PERSONAL)
```
em td 
    -m "talking to the ceo and he's telling me to read this article: https://www.brendangregg.com/blog/2017-05-09/cpu-utilization-is-wrong.html"
    -a read
    -t "ceo" -t "articles" -t "performance" -t "brendan greg"
    -iw 100 # give it a weight of 100 for sorting index by weight
    -ic 100 # give it a cool factor of 100 for sorting index by cool
    -p person

em td 
    -m "https://www.amazon.com/High-Output-Management-Andrew-Grove/dp/0679762884"
    -a read
    -t books management "andrew grove"

em td 
    -m "watch this movie: https://www.imdb.com/title/tt0111161/"
    -t movies drama prison "stephen king"
    -a watch

em td -it # show list of all todo items sorted by time index
em td -iw # show list of all todo items sorted by weight index
em td -ic # show list of all todo items sorted by cool index
```

## FIND (search through apps)
an interactive search that will search through all apps and return results.
```
em fd nt -t uwsgi # search for notes with tag uwsgi
em fd nt -m uwsgi # search for notes with message that contains the word "uwsgi"
em fd fb -p wenwen -m "refactor" # search through wenwen's feedback for note container work "refactor"
em fd fb -m "refactor" # search through wenwen's feedback for note container work "refactor"
em fd -t wsgi # search through all tags
em fd -m wsgi # search through all messages
em fd # open interactive search that will do live search as you type
```


# DEPENDENCIES
This command line app is built on top of other good apps.

- https://github.com/Textualize/rich-cli
- https://github.com/Textualize/rich
- https://github.com/Textualize/frogmouth
- https://github.com/Textualize/trogon
- https://www.textualize.io/
- https://github.com/Textualize

# BUILD PACKAGE
How to build the package and install it locally.

- `python setup.py sdist bdist_wheel # to build package`
- `pip install dist/em-0.1-py3-none-any.whl # to install package`
- `pip install --force-reinstall dist/em-0.1-py3-none-any.whl # to reinstall package`
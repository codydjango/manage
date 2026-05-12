# EM (Engineering Manager)

Engineering manager flywheel for capturing everything that I generally do as an engineering manager.

## APPS

A set of command-line apps that share similar interfaces.

### NOTES

General notes for context, optimized for tag search and full-text search.

```
em nt 'echo r > /var/run/uwsgi/app.fifo; # restart a uwsgi process' -t uwsgi
em nt
em nt -m "use xor filters for fast search. it works like a bloom filter. it's a space efficient, fast, probabilistic data structure." -t "full-text-search"
em nt -m "look at meilisearch or tantivy for rust-based full-text search crates" -t "full-text-search" "rust" "search"
em nt -m "don't do this anymore" -t stop-doing
```

### QUIZ

Flash-card style quiz to reinforce engineering knowledge. Questions are weighted by frequency and optionally filtered by tag.

```
em qz              # run a full quiz session
em qz -t "networking em"   # filter questions to a specific tag set (space separated)
em qz -l 10        # limit to 10 questions
```

### REMINDER

Defer items to the future, so you don't have to think about them now.

```
em rm -m "get build out" --due today@5pm -w 100 -r 1hr -rb 1hr
em rm -m "read brendan greg article on performance" -r 1d
em rm -m "watch the video on the new feature" --due "15/12/2020" -rb 1d
em rm
em rm "get build out" -b 1d
```

### TODO

General todo list, optimized for productivity.

**Options:**
```
em td
    -m "message"
    -a assign an action type
    -t assign a tag or multiple
    -tw assign a weight for sorting index by weight
    -tp assign points to be recouped on completion
    -ii assign an interesting factor for sorting index by interesting
    -tc to mark as complete
```

**Example Usage:**
```
em td
    -m "https://www.amazon.com/High-Output-Management-Andrew-Grove/dp/0679762884"
    -a read
    -t books management "andrew grove"

em td
    -m "watch this movie: https://www.imdb.com/title/tt0111161/"
    -t movies drama prison "stephen king"
    -a watch

em td -it    # show list of all todo items sorted by time index
em td -iw    # show list of all todo items sorted by weight index
em td -ic    # show list of all todo items sorted by cool index
```

## BACKLOG

Ideas for what's coming next.

### TASK TRACKER

Log time on tasks. Time is logged against tasks and can be bounded or unbounded.

```
em tt 'do a thing' -t 1h    # create a task and add 1 hour to it
em tt -s 'do a thing 2'     # start a new task and capture the start timestamp
em tt -p 'do a thing 2'     # pause the task and capture the duration
em tt -e 'do a thing 2'     # end the task and capture the full duration
em tt -lo                   # list open tasks
em tt -lc                   # list completed tasks
em tt -la                   # list all tasks
em ttr                      # report of all tasks
em ttr -w                   # report scoped to the week
em ttr -m                   # report scoped to the month
```

### FEEDBACK

Capture feedback for direct reports as it comes up. Inspired by Mark Horstman's book *The Effective Manager*.

**Options:**
```
em fb -h
    p    # gave positive feedback
    c    # gave constructive feedback
    n    # took a note of something to discuss later
    a    # took a note of an accomplishment to be used in a review or promotion
```

**Example Usage:**
```
em fb p -p 'matt.m' -m 'matt was giving wenwen good feedback, really put in the effort to help wenwen grow'
em fb c -p 'matt.m' -m 'matt was late this morning again'
em fb n -m 'had a meeting and wenwen was late' -p wenwen
em fb n -m 'had a meeting and wenwen was late' -p wenwen -t scalability
em fb report -p wenwen    # show all feedback for wenwen
```

### FIND

A search that will search through all apps and return results.

```
em fd --in nt -t uwsgi                          # search for notes with tag uwsgi
em fd --in nt -m uwsgi                          # search for notes with message containing "uwsgi"
em fd --in fb -p wenwen -m "refactor"           # search wenwen's feedback for "refactor"
em fd --in fb -m "refactor"                     # search all feedback for "refactor"
em fd -t wsgi                                   # search through all tags
em fd -i                                        # open interactive live search
```

### REPORT

- Daily/weekly/monthly reports on time logged, tasks completed, etc.
- Visualization

### OTHER

- Sync reminders to google calendar
- Encrypt all data at rest
- Automatic local backups using grandfather/father/son backups
- Cloud backups and cloud access
- Sync between devices
- macOS helper app for quick access via hotkey

## DEPENDENCIES

- https://click.palletsprojects.com/en/8.1.x/
- https://whoosh.readthedocs.io/en/latest/intro.html
- https://github.com/Textualize/rich-cli
- https://github.com/Textualize/rich
- https://github.com/Textualize/frogmouth
- https://github.com/Textualize/trogon
- https://www.textualize.io/

## DEV NOTES

- `uv sync` to install dependencies into a local virtualenv
- `uv tool install --editable .` to install `em` to your PATH as a live editable build
- `uv tool update-shell` (once) if `em` is not found after install — ensures `~/.local/bin` is on PATH

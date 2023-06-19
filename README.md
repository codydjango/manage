# manage
Engineering manager flywheel

## Questions
- should it be called `mng` or `em` for engineering manager?

# FEEDBACK
mng fb -h
    fb p # gave positive feedback
    fb c # gave constructive feedback
    fb n # took a note of something to discuss later
    fb a # took a note of an accomplishment to be used in a review, for promotion

mng fb p -p 'matt.m' -m 'matt was giving wenwen good feedback, really put in the effort to help wenwen grow'
mng fb c -p 'matt.m' -m 'matt was late this morning again'
mng fb n -m 'had a meeting and wenwen was late' -p wenwen
mng fb n -m 'had a meeting and wenwen was late' -p wenwen -t scalability
mng fb report -p wenwen # show all feedback for wenwen

# TASK TRACKER (Work)

create tasks and log time on them. time is logged against tasks. time can be bounded or unbounded,
in that you can start a task and end it, and the time duration will be logged automatically, or you 
can just log time against a task without explicitly starting or ending it.

mng tt 'do a thing' -t 1h # create a task and add 1 hour to it, bounded. if the task already exists, log another hour to it.
mng tt -s 'do a thing 2' # start a new task and capture the timestamp for start, unbounded
mng tt -p 'do a thing 2' # pause the task and capture the duration of time, bounded
mng tt -e 'do a thing 2' # end the task and capture the timestamp for end and the duration of time from start to end
mng tt -lo # list open tasks
mng tt -lc # list completed tasks
mng tt -la # list all tasks
mng ttr # show a report of all tasks, time logged, etc.
mng ttr -w # show a report scoped to the week
mng ttr -m # show a report scoped to the month

# REMEMBER/REMINDER
mng rm -m "get build out" --due today@5pm -w 100 -r 1hr -rb 1hr # remind in one hour to get the build out, remind one hour before it's due, give weight of 100 in todo list (ordered by reverse weight)
mng rm -m "read brendan greg article on performance" -r 1d # remind me in one day to read the article
mng rm -m "watch the video on the new feature" --due "15/12/2020" -rb 1d # remind me 1 day before the due date
mng rm # show all upcoming reminders
mng rm "get build out" -b 1d # bump the reminder for "get build out" by one day

# TODO (PERSONAL)
mng td 
    -m "talking to the ceo and he's telling me to read this article: https://www.brendangregg.com/blog/2017-05-09/cpu-utilization-is-wrong.html"
    -a read
    -t "ceo" -t "articles" -t "performance" -t "brendan greg"
    -iw 100 # give it a weight of 100 for sorting index by weight
    -ic 100 # give it a cool factor of 100 for sorting index by cool
    -p person

mng td 
    -m "https://www.amazon.com/High-Output-Management-Andrew-Grove/dp/0679762884"
    -a read
    -t books management "andrew grove"

mng td 
    -m "watch this movie: https://www.imdb.com/title/tt0111161/"
    -t movies drama prison "stephen king"
    -a watch

`mng td -it # show list of all todo items sorted by time index`
`mng td -iw # show list of all todo items sorted by weight index`
`mng td -ic # show list of all todo items sorted by cool index`

# NOTES (general notes for context, optimized for tag search and full-text search)

this could take two options, quick notes and long notes, in a manner similar to git commit. 
quick notes would be a single line, long notes would be a multiline message.

`mng nt 'echo r > /var/run/uwsgi/app.fifo; # restart a uwsgi process' -t uwsgi # for single line quick`
`mng nt # to open up a program for multi-line notes`

`mng fd nt -t uwsgi # search for notes with tag uwsgi`
`mng fd nt -m uwsgi # search for notes with message that contains the word "uwsgi"`
`mng fd fb -p wenwen -m "refactor" # search through wenwen's feedback for note container work "refactor"`
`mng fd fb -m "refactor" # search through wenwen's feedback for note container work "refactor"`
`mng fd -t wsgi # search through all tags`
`mng fd -m wsgi # search through all messages`
`mng fd # open interactive search that will do live search as you type` 


`mng nt -m "use xor filters for fast search. it works like a bloom filter. it's a space efficient, fast, probabilistic data structure." -t "full-text-search"`
`mng nt -m "look at meilisearch or tantivy for rust-based full-text search crates" -t "full-text-search" "rust" "search"`

https://github.com/Textualize/rich-cli
https://github.com/Textualize/rich
https://github.com/Textualize/frogmouth
https://github.com/Textualize/trogon
https://www.textualize.io/
https://github.com/Textualize
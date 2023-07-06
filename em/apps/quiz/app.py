import random
import copy
import click

from collections import Counter
from em.app import App
from typing import List
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table

from .storage import NoteStorage

console = Console()

APPNAME = 'QUIZ'

@dataclass(frozen=True)
class Challenge:
    question: str
    answer: str
    frequency: int = 50
    tags: List[str] = None

    @property
    def get_tags(self):
        return self.tags or []

    def __str__(self):
        return f'{self.question}'

CHALLENGES = [
    Challenge(tags=['em', 'networking'],
              frequency=10,
              question='What are the system design implications for high network bandwidth (ingress/egress)?',
              answer='scalability: capacity planning to avoid bottlenecks \n'
                    'cost: many cdn and cloud providers charge for bandwidth\n'
                    'security: can be an attack vector\n'
                    'performance: understanding pattern and volume of ingress and egress dictate CDN and caching.'),
    Challenge(tags=['em', 'networking'],
              frequency=10,
              question='What are the system design implications for high network CCU?',
              answer='many factors account for CCU -- understanding the requirements will dictate the design. \n'
                     'scalability: webservers can handle 1000 (1024 by default in nginx) and can scale to hundreds '
                     'of thousands. \n'
                     'availability: a surge of connections might make it difficult to scale horizontally, as you need '
                     'time to spin up new instances. \n'
                     'resource management: handling many connections requires substantial cpu, memory, and '
                     'network resources. For stateful websocket servers, the requirements will guide decisions '
                     'about hardware sizing and costs.'),
    Challenge(tags=['em', 'networking'],
              frequency=10,
              question='What is the latency for sending 2k over a 1gbps network?',
              answer='20 microseconds'),
    Challenge(tags=['em', 'networking'],
              frequency=100,
              question='What is the latency for sending a packet round trip within the same datacenter?',
              answer='500 microseconds'),
    Challenge(tags=['em', 'networking'],
              frequency=100,
              question='What is the latency for sending a packet from west coast to europe and back?',
              answer='150 milliseconds'),
    Challenge(tags=['em', 'networking'],
              frequency=100,
              question='What is the latency for reading 1mb sequentially from memory?',
              answer='250 microseconds'),
    Challenge(tags=['em', 'networking'],
              frequency=50,
              question='What is the latency for reading 1mb sequentially from network?',
              answer='10 milliseconds'),
    Challenge(tags=['em', 'networking'],
              frequency=80,
              question='What is the latency for reading 1mb sequentially from disk?',
              answer='30 milliseconds'),
    Challenge(tags=['em', 'networking'],
              question='What is the latency for a disk seek?',
              answer='10 milliseconds'),
    # Challenge(question='What factors into the round trip latency within a datacenter?',
    #           answer='queuing for switches, routers, servers, serialization, transmission (pushing packet bits '
    #                  'to the network link/wire), processing time'),
    # Challenge(question='What is a SMART Story?',
    #           answer='Situation, Metrics/More, Action, Result, Tie-in'),
    Challenge(frequency=20,
              tags=['em', 'interviewing'],
              question='What is a structured way to approach a system design interview? how long should each step take?',
              answer='15 minutes for 1) FR 2) NFR 3) Quantitative Analysis 4) HLD 5) API -> DB Schema 6) Scalability '
                     '7) Fault Tolerance 8) Q&A'),
    Challenge(frequency=10,
              tags=['em', 'databases'],
              question='What is ACID and explain each?',
              answer='atomic, consistent, isolation, durable'),
    Challenge(frequency=10,
              tags=['em', 'distributed-systems', 'scaling', 'databases'],
              question='What are the CAP Theorem and explain each?',
              answer='consistency, availability, partition'),
    Challenge(frequency=10,
              tags=[],
              question='What is the difference between a process and a thread?',
              answer='a process is an instance of '
                                                                                       'a program, a thread is a '
                                                                                       'unit of execution within a '
                                                                                       'process'),
    Challenge(question='What is the difference between a mutex and a semaphore?',
              answer='A mutex is a program object that lets multiple threads share the same resource, but not '
                     'simultaneously. mutex = mutual exclusion. '
                     'It is created on application startup and destroyed on application shutdown. \n'
                     'A semaphore is a program object that lets multiple threads share the same resource to some'
                     'configured limit. It is created on application startup and destroyed on application shutdown.'
                     'Any thread can release a semaphore -- there is no ownership rules with semaphores. A binary '
                     'semaphore is similar to a mutex, but without the ownership rules. A semaphore is a signalling'
                     'mechanism that is useful for syncronizing threads across processes.'),
    Challenge(question='What are RDBMS isolation levels and explain each?',
              answer='read uncommitted: dirty reads, non-repeatable reads, phantom reads \n'
                     'read committed: non-repeatable reads, phantom reads \n'
                     'repeatable read: phantom reads \n'
                     'serializable: no dirty reads, no non-repeatable reads, no phantom reads'),
]

def output(content: List, title=APPNAME.capitalize()):
    table = Table(title=title)
    table.add_column('Question', justify='left', style='cyan', no_wrap=True)
    table.add_column('Attempts', justify='left', style='cyan', no_wrap=True)

    for item in content:
        table.add_row(str(item[0]), item[1])

    console.print(table)

def prompt(challenges) -> None:
    results = []
    attempts = Counter()

    while len(challenges):
        challenge = random.choice(challenges)
        click.echo(challenge.question)
        click.prompt('Answer')
        click.echo(challenge.answer)
        passed = click.confirm('Pass?')

        attempts[challenge.question] += 1

        if passed:
            challenges.remove(challenge)
            results.append((challenge.question, str(attempts[challenge.question])))

    output(title=f'Quiz Results ({len(results)})', content=results)

class Quiz(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        challenges = copy.copy(CHALLENGES)

        if tags:= kwargs.get('tags', None):
            tags = set(tags.split(' '))
            challenges = [c for c in challenges if tags.issubset(c.get_tags)]

        challenges = [c for c in challenges if c.frequency > random.randint(0, 100)]

        random.shuffle(challenges)

        if limit:= kwargs.get('limit', None):
            challenges = challenges[:limit]

        for challenge in challenges:
            click.echo(str(challenge))

        prompt(challenges)






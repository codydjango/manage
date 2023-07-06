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

CHALLENGES = [
    # Challenge(question='What are the system design implications for high network bandwidth (ingress/egress)?',
    #           answer='scalability: capacity planning to avoid bottlenecks \n'
    #                 'cost: many cdn and cloud providers charge for bandwidth\n'
    #                 'security: can be an attack vector\n'
    #                 'performance: understanding pattern and volume of ingress and egress dictate CDN and caching.'),
    # Challenge(question='What are the system design implications for high network CCU?',
    #           answer='many factors account for CCU -- understanding the requirements will dictate the design. \n'
    #                  'scalability: webservers can handle 1000 (1024 by default in nginx) and can scale to hundreds '
    #                  'of thousands. \n'
    #                  'availability: a surge of connections might make it difficult to scale horizontally, as you need '
    #                  'time to spin up new instances. \n'
    #                  'resource management: handling many connections requires substantial cpu, memory, and '
    #                  'network resources. For stateful websocket servers, the requirements will guide decisions '
    #                  'about hardware sizing and costs.'),
    # Challenge(question='What is the latency for sending 2k over a 1gbps network?',
    #           answer='20 microseconds'),
    Challenge(question='What is the latency for sending a packet round trip within the same datacenter?',
              answer='500 microseconds'),
    Challenge(question='What is the latency for sending a packet from west coast to europe and back?',
              answer='150 milliseconds'),
    Challenge(question='What is the latency for reading 1mb sequentially from memory?',
              answer='250 microseconds'),
    # Challenge(question='What is the latency for reading 1mb sequentially from network?',
    #           answer='10 milliseconds'),
    Challenge(question='What is the latency for reading 1mb sequentially from disk?',
              answer='30 milliseconds'),
    Challenge(question='What is the latency for a disk seek?',
              answer='10 milliseconds'),
    # Challenge(question='What factors into the round trip latency within a datacenter?',
    #           answer='queuing for switches, routers, servers, serialization, transmission (pushing packet bits '
    #                  'to the network link/wire), processing time'),
    # Challenge(question='What is a SMART Story?',
    #           answer='Situation, Metrics/More, Action, Result, Tie-in'),
    Challenge(question='What is a structured way to approach a system design interview? how long should each step take?',
              answer='15 minutes for 1) FR 2) NFR 3) Quantitative Analysis 4) HLD 5) API -> DB Schema 6) Scalability '
                     '7) Fault Tolerance 8) Q&A')
]

def output(content: List, title=APPNAME.capitalize()):
    table = Table(title=title)
    table.add_column('Question', justify='left', style='cyan', no_wrap=True)
    table.add_column('Attempts', justify='left', style='cyan', no_wrap=True)

    for item in content:
        table.add_row(str(item[0]), item[1])

    console.print(table)

def prompt() -> None:
    challenges = copy.copy(CHALLENGES)
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
    storage_cls = NoteStorage

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        prompt()






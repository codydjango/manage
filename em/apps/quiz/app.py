import random
import click
from collections import Counter
from em.app import App
from rich.console import Console
from rich.table import Table
from em.apps.quiz import srs

console = Console()

APPNAME = 'QUIZ'


def run_session(questions, state):
    results = []
    attempts = Counter()
    pool = list(questions)

    console.print(f'\n[bold]Quiz — {len(pool)} question(s) due[/bold]\n')

    while pool:
        q = random.choice(pool)
        click.echo(q['question'])
        click.prompt('Answer', prompt_suffix='\n> ')
        click.echo(f'\n{q["answer"]}\n')
        passed = click.confirm('Pass?')

        qid = q['id']
        attempts[qid] += 1
        state[qid] = srs.grade_question(state[qid], passed)

        if passed:
            pool.remove(q)
            results.append((q['question'], str(attempts[qid])))

    return results


def show_results(results):
    table = Table(title=f'Quiz Results ({len(results)})')
    table.add_column('Question', style='cyan')
    table.add_column('Attempts', style='green', justify='right')
    for question, attempts in results:
        table.add_row(question, attempts)
    console.print(table)


def show_list(questions, state):
    from datetime import date
    today = date.today().isoformat()
    table = Table(title='Questions')
    table.add_column('Question', style='cyan', no_wrap=False)
    table.add_column('Tags', style='yellow')
    table.add_column('Active', justify='center')
    table.add_column('Reps', justify='right')
    table.add_column('Interval', justify='right')
    table.add_column('Next Review', justify='right')

    for q in questions:
        s = state.get(q['id'], {})
        active = '[green]✓[/green]' if s.get('active') else '[dim]–[/dim]'
        reps = str(s.get('reps', 0))
        interval = f"{s.get('interval', 1)}d" if s.get('active') else '–'
        next_review = s.get('next_review') or '–'
        if s.get('active') and next_review != '–' and next_review <= today:
            next_review = f'[red]{next_review}[/red]'
        table.add_row(
            q['question'][:70],
            ', '.join(q.get('tags', [])),
            active,
            reps,
            interval,
            next_review,
        )

    console.print(table)


class Quiz(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tag_input = kwargs.get('tags')
        limit = kwargs.get('limit')
        list_mode = kwargs.get('list_mode', False)

        tag_list = tag_input.split() if tag_input else None
        questions = srs.load_questions(tags=tag_list)
        state = srs.load_state()

        srs.ensure_initialized(questions, state)

        if list_mode:
            show_list(questions, state)
            srs.save_state(state)
            return

        due = srs.get_due_questions(questions, state)

        if not due:
            console.print('[yellow]No questions due for review today.[/yellow]')
            new_q = srs.maybe_activate_new(questions, state)
            if new_q:
                console.print(f'[green]Activated new question:[/green] {new_q["question"]}')
                due = [new_q]
            else:
                srs.save_state(state)
                return

        if limit:
            due = due[:limit]

        results = run_session(due, state)

        new_q = srs.maybe_activate_new(questions, state)
        if new_q:
            console.print(f'\n[green]New question added to rotation:[/green] {new_q["question"]}')

        srs.save_state(state)
        show_results(results)

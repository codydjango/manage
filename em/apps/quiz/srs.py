import json
from datetime import date, timedelta
from pathlib import Path
from em.settings import get_database_path

MAX_ACTIVE = 8  # target number of questions in active rotation before graduating


def _state_path():
    return Path(get_database_path()).parent / 'quiz_state.json'


def _questions_path():
    return Path(__file__).parent / 'questions.json'


def load_questions(tags=None):
    with open(_questions_path()) as f:
        questions = json.load(f)
    if tags:
        tag_set = set(tags)
        questions = [q for q in questions if tag_set.issubset(set(q.get('tags', [])))]
    return questions


def load_state():
    path = _state_path()
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def save_state(state):
    _state_path().write_text(json.dumps(state, indent=2, default=str))


def init_question_state(starter=False):
    return {
        'active': starter,
        'ease': 2.5,
        'interval': 1,
        'reps': 0,
        'next_review': date.today().isoformat() if starter else None,
    }


def grade_question(entry, passed: bool):
    today = date.today()
    if passed:
        reps = entry['reps'] + 1
        ease = entry['ease']
        if reps == 1:
            interval = 1
        elif reps == 2:
            interval = 6
        else:
            interval = round(entry['interval'] * ease)
        ease = max(1.3, ease + 0.1)
        next_review = (today + timedelta(days=interval)).isoformat()
        return {**entry, 'reps': reps, 'ease': ease, 'interval': interval, 'next_review': next_review}
    else:
        return {**entry, 'reps': 0, 'interval': 1, 'next_review': today.isoformat()}


def get_due_questions(questions, state):
    today = date.today().isoformat()
    return [
        q for q in questions
        if state.get(q['id'], {}).get('active')
        and state.get(q['id'], {}).get('next_review', '') <= today
    ]


def maybe_activate_new(questions, state):
    """Activate the next inactive question if the active-learning pool has room."""
    active_learning = sum(
        1 for s in state.values()
        if s.get('active') and s.get('interval', 0) < 21
    )
    if active_learning >= MAX_ACTIVE:
        return None
    for q in questions:
        if not state.get(q['id'], {}).get('active', False):
            today = date.today().isoformat()
            base = state.get(q['id'], init_question_state())
            state[q['id']] = {**base, 'active': True, 'next_review': today}
            return q
    return None


def ensure_initialized(questions, state):
    """Add default state for any question not yet seen."""
    for q in questions:
        if q['id'] not in state:
            state[q['id']] = init_question_state(starter=q.get('starter', False))

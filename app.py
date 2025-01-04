# app.py

from flask import Flask, render_template, request, session, redirect, url_for, flash
import random
from game_logic import ChineseWordGame

app = Flask(__name__)
app.secret_key = 'abc123'

# Chinese sentences with hints
SENTENCES = [
    {
        'sentence': '学而时习之，不亦说乎。',
        'hint': "论语中的一句话，关于学习。Hint: A sentence about learning from the Analects of Confucius."
    },
    {
        'sentence': '千里之行，始于足下。',
        'hint': "描述开始做事的谚语。Hint: A proverb describing the start of doing something."
    },
    {
        'sentence': '明月几时有，把酒问青天。',
        'hint': "苏轼的一首诗的开头。Hint: The beginning of a poem by Su Shi."
    },
    {
        'sentence': '春眠不觉晓，处处闻啼鸟。',
        'hint': "描写春天的古诗。Hint: The beginning of a poem describing the spring season."
    },
    {
        'sentence': '天下无难事，只怕有心人。',
        'hint': "关于应对困难的谚语。Hint: A proverb about attitude towards dealing with difficulties."
    },
    {
        'sentence': '床前明月光，疑是地上霜。',
        'hint': "李白的一首诗的开头。Hint: The beginning of a poem by Li Bai."
    }
]


def init_game():
    """Initialize a new game"""
    sentence_data = random.choice(SENTENCES)
    game = ChineseWordGame(sentence_data['sentence'], sentence_data['hint'])
    session['game_state'] = game.get_game_state()
    return game


def load_game():
    """Load game from session or create new one"""
    if 'game_state' not in session:
        return init_game()

    game = ChineseWordGame.from_state(session['game_state'])
    if game is None:
        return init_game()
    return game


@app.route('/')
def index():
    """Main game page"""
    game = load_game()
    game_state = game.get_game_state()
    session['game_state'] = game_state

    return render_template('index.html',
                           display_sentence=game_state['display_sentence'],
                           hint=game_state['hint'],
                           guessed_chars=', '.join(game_state['guessed_chars']) if game_state[
                               'guessed_chars'] else '无',
                           tries_remaining=game_state['tries_remaining'],
                           max_tries=game_state['max_tries'],
                           game_over=game_state['game_over'],
                           won=game_state['won'],
                           sentence=game_state['sentence'] if game_state['game_over'] else None)


@app.route('/guess', methods=['POST'])
def guess():
    """Handle guess submission"""
    game = load_game()
    if not game.game_over:
        guess = request.form.get('guess', '').strip()
        is_valid, is_correct, message = game.make_guess(guess)

        if is_valid:
            flash(message, 'success' if is_correct else 'danger')
        else:
            flash(message, 'warning')

        session['game_state'] = game.get_game_state()

    return redirect(url_for('index'))


@app.route('/new_game')
def new_game():
    """Start a new game"""
    init_game()
    flash('新一轮游戏开始！ Guess another sentence.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
from boggle import Boggle
from flask import Flask, render_template, session, request, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret123'
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/',  methods=["post", 'get'])
def render_board():
    return render_template('board.html', board=session['board'])


@app.route("/check-word")
def check_word():
    """checks word"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route('/restart')
def restart():
    """restarts board"""
    board = boggle_game.make_board()
    session['board'] = board
    return redirect('/')


@app.route("/post-score", methods=["POST"])
def post_score():
    """
    Copied from the solution
    Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)
    return jsonify(brokeRecord=score > highscore)

let words = new Set();
let score = 0;
let timeOut = false;
$wordForm = $('#wordForm');
$info = $('#info');
$score = $('#score');
$timer = $('#timer');
$sumbitScore = $('#sumbitScore');

$wordForm.on('submit', (e) => {
  e.preventDefault();
  word = $('#word').val();
  wordInput = $('#word');
  getWord(word);

  async function getWord(word) {
    if (timeOut) return;
    if (!word) return;
    const resp = await axios.get('/check-word', { params: { word: word } });
    result = resp.data.result;

    if (words.has(word)) {
      $info.html(`The word "${word}" has already guessed`);
      wordInput.val('');
      return;
    }
    if (result === 'ok') {
      words.add(word);
      score += 1;
      wordInput.val('');
      $info.html(`Added word : ${word}`);
      $score.html(`${score}`);
    }
    if (result === 'not-on-board') {
      $info.html("Word isn't on the board");
      wordInput.val('');
    }
    if (result === 'not-word') {
      $info.html('Not a word');
      wordInput.val('');
    }
  }
});
async function postScore() {
  const resp = await axios.post('/post-score', { score: score });
  if (resp.data.brokeRecord) {
    $info.html(`New record: ${score}`);
  } else {
    $info.html(`Final score: ${score}`);
  }
}

function startTimer() {
  $sumbitScore.hide();
  let time = 60;
  let sec = async () => {
    if (time <= 0) {
      $sumbitScore.show();
      clearInterval(timer);
      timeOut = true;
      postScore();
      return;
    } else {
      time -= 1;
      if (time < 15) {
        $timer.html(`<span style="color: red;">${time}</span>`);
      } else {
        $timer.html(`<span>${time}</span>`);
      }
    }
  };
  let timer = setInterval(sec, 1000);
}
$(document).ready(() => {
  startTimer();
  $('#word').focus();
});

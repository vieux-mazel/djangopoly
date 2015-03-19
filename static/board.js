(function($) {
  var TIME_INTERVAL = 800;

  var oldState;
  var $board = $('#board');
  var isAjaxing = false;
  resizeBoard();

  for (var i = 0; i < 40; i++) {
    $board.append('<div id="square' + i + '" class="square"></div>');
  }

  var gameId = document.URL.split('/');
  gameId = gameId[gameId.length - 2];

  function drawBoard() {
    $.getJSON('state/', function(state) {
      isAjaxing = true;
      var i, j, square, player, squareStr, playersStr;
      var $square = $('<div />');
      
      for (i = 0; i < state.squares.length; i++) {
        if (oldState && JSON.stringify(oldState.squares[i]) === JSON.stringify(state.squares[i])) continue;

        square = state.squares[i];
        squareStr = square.title;

        playersStr = '';
        for (j = 0; j < square.players.length; j++) {
          player = square.players[j];
          playersStr += '<div class="person" id="player' + player.joined + '"></div>';
        }
        squareStr = squareStr + playersStr;
        
        document.getElementById('square' + square.position).innerHTML = squareStr;

      } // for

      oldState = state;
      isAjaxing = false;
    });
  }

  function resizeBoard() {
    $board.css({width: $board.height()});
  }

  $('#dice').click(function() {
    $.getJSON('/game/roll', function(data) {
      //console.log('Dice roll:');
      console.log(data);
      //console.log('---');
    });
  });

  $('#end-turn').click(function() {
    $.getJSON('/game/end_turn', function(data){
      //console.log('End turn:');
      console.log(data);
      //console.log('---');
    });
  });

  $('#buy').click(function () {
    var $self = $(this);
    //console.log('About to buy...');
  });

  drawBoard();

  setInterval(function() {
    $.getJSON('state/', function(state) {
      if (!isAjaxing) drawBoard();
    });
  }, TIME_INTERVAL);

  $(window).on('resize', resizeBoard);

})(jQuery);

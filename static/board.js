(function($) {
  var TIME_INTERVAL = 800;

  var oldState;
  var isAjaxing = false;

  var $board = $('#board');
  var $playerList = $('#playerList');

  for (var i = 0; i < 40; i++) {
    $board.append('<div id="square' + i + '" class="square"></div>');
  }
  for (var i = 0; i < 6; i++) {
    $playerList.append('<div id="playerItem' + i + '"></div>');
  }

  var gameId = document.URL.split('/');
  gameId = gameId[gameId.length - 2];


  function drawState() {
    isAjaxing = true;

    $.getJSON('state/', function(state) {
      var i, j, square, player, squareStr, playersStr, playerStr;

      // Main content
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

      // Sidebar
      for (i = 0; i < state.players.length; i++) {
        if (oldState && JSON.stringify(oldState.players[i]) === JSON.stringify(state.players[i])) continue;

        player = state.players[i];
        playerStr = 'Player: ' + player.name;

        document.getElementById('playerItem' + i).innerHTML = playerStr;
      }

      // Reflect new state
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
    $.getJSON('/game/end_turn', function(data) {
      console.log(data);
    });
  });

  $('#buy').click(function () {
    var $self = $(this);
  });

  setInterval(function() {
    $.getJSON('state/', function(state) {
      if (!isAjaxing) drawState();
    });
  }, TIME_INTERVAL);

  $(window).on('resize', resizeBoard);

  resizeBoard();
  drawState();

})(jQuery);

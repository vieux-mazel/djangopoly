(function($) {
  var TIME_INTERVAL = 800;

  var lastState;
  var isAjaxing = false;

  var $board = $('#board');
  var $playerList = $('#players-table-body');
  var $buy = $('#buy');

  for (var i = 0; i < 40; i++) {
    $board.append('<div id="square' + i + '" class="square"></div>');
  }

  for (var i = 0; i < 6; i++) {
    $playerList.append('<tr id="playerItem'+ i +'"></tr>');
  }

  var gameId = document.URL.split('/');
  gameId = gameId[gameId.length - 2];

    

  function drawState() {
    isAjaxing = true;

    $.getJSON('state/', function(state) {
      var i, j, square, player, squareStr, playersStr, playerStr;



      // Main content
      for (i = 0; i < state.squares.length; i++) {
        if (lastState && JSON.stringify(lastState.squares[i]) === JSON.stringify(state.squares[i])) continue;

        square = state.squares[i];
        squareStr = square.title;

        playersStr = '';
        for (j = 0; j < square.players.length; j++) {
          player = square.players[j];
          playersStr += '<div class="person person' + j + '" id="player' + player.joined + '"></div>';
        }
        squareStr = squareStr + playersStr;
        
        document.getElementById('square' + square.position).innerHTML = squareStr;

      } // for

      // Sidebar
      for (i = 0; i < state.players.length; i++) {
        if (lastState && JSON.stringify(lastState.players[i]) === JSON.stringify(state.players[i])) continue;

        player = state.players[i];
        playerStr = '<td>'+ (i + 1) +'</td><td>' + state.players[i].money + '</td>';

        document.getElementById('playerItem' + i).innerHTML = playerStr;
      }

      // Buy action
      if (state.can_be_bought) $buy.addClass('active');
      else $buy.removeClass('active');

      // Reflect new state
      lastState = state;
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

  $buy.click(function() {
    var $self = $(this);
    if (!lastState.can_be_bought) return;
    $.getJSON('/game/buy', function(data) {
      console.log(data);
    });
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

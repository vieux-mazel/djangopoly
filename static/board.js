(function($) {
  var TIME_INTERVAL = 800;

  var lastState;
  var isAjaxing = false;

  var $board = $('#board');
  var $playerList = $('#players-table-body');
  var $dicevis = $('#dice-vis');
  
  var $buy = $('#buy');
  var $mortgage = $('#mortgage');
  var $dice = $('#dice');
  var $endTurn = $('#end-turn');

  for (var i = 0; i < 40; i++) {
    $board.append('<div id="square' + i + '" class="square"></div>');
  }

  for (var i = 0; i < 6; i++) {
    $playerList.append('<tr id="playerItem'+ i +'"></tr>');
  }

  var gameId = document.URL.split('/');
  gameId = gameId[gameId.length - 2];
  function drawState() {
    $.getJSON('state/', function(state) {
      var i, j, square, player, squareStr, playersStr, playerStr, diceRoll;

      // Main content
      for (i = 0; i < state.squares.length; i++) {
        if (
          lastState &&
          JSON.stringify(lastState.squares[i]) === JSON.stringify(state.squares[i])
        ) continue;

        square = state.squares[i];
        squareStr = square.title;

        playersStr = '';
        for (j = 0; j < square.players.length; j++) {
          player = square.players[j];
          playersStr += '<div class="person person' + j + '" id="player' + player.joined + '"></div>';
        }
        squareStr = squareStr + playersStr;
        
        document.getElementById('square' + square.position).innerHTML = squareStr;
      }

      // Sidebar
      for (i = 0; i < state.players.length; i++) {
        if (
          lastState &&
          JSON.stringify(lastState.players[i]) === JSON.stringify(state.players[i])
        ) continue;

        player = state.players[i];
        playerStr = '<td>'+ player.name +'</td><td>' + player.money + '</td>';

        document.getElementById('playerItem' + i).innerHTML = playerStr;
      }

      // Buy and mortgage
      if (state.can_be_bought) $buy.addClass('active');
      else $buy.removeClass('active');
      
      if (state.can_be_mortgaged) $mortgage.addClass('active');
      else $mortgage.removeClass('active');

      // Dice
      if (!state.is_your_turn) {
        $dice.removeClass('active');
        $endTurn.removeClass('active');
      } else if (!state.rolled_this_turn) {
        $dice.addClass('active');
        $endTurn.removeClass('active');
      } else {
        $dice.removeClass('active');
        $endTurn.addClass('active');
      }
      
      // Reflect new state
      lastState = state;
    });
  }

  $dice.click(function() {
    $.getJSON('/game/roll', function(data) {
      console.log(data);

      if (data.success === true) {
        $dice.removeClass('active');
        $endTurn.addClass('active');
        $dicevis.html('<div class="die">'+ data.dice1 +'</div>'+ '<div class="die">'+ data.dice2 +'</div>');
      }
    });
  });

  $endTurn.click(function() {
    $.getJSON('/game/end_turn', function(data) {
      $endTurn.removeClass('active');
    });
  });

  $buy.click(function() {
    if (lastState && !lastState.can_be_bought) return;
    
    $.getJSON('/game/buy', function(data) {
      console.log(data);
    });
  });

  $mortgage.click(function() {
    if (lastState && !lastState.can_be_mortgaged) return;
    
    $.getJSON('/game/mortgage', function(data) {
      console.log(data);
    });
  });

  setInterval(function() {
    $.getJSON('state/', function(state) {
      if (!isAjaxing) drawState();
    });
  }, TIME_INTERVAL);

  function resizeBoard() {
    $board.css({width: $board.height()});
  }
  $(window).on('resize', resizeBoard);
  resizeBoard();

  drawState();

})(jQuery);

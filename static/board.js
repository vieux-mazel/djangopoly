(function($) {
  var oldState;
  var $board = $('#board');
  resizeBoard();

  for (var i = 0; i < 40; i++) {
    $board.append('<div id="square' + i + '"></div>');
  }

  var gameId = document.URL.split('/');
  gameId = gameId[gameId.length - 2];

  function drawBoard() {
    $.getJSON('state/', function(state) {
      //console.log(state);
      //console.log(oldState);
      //console.log('---');

      var size1 = 14;
      var size2 = 8;

      var i, j, classes, styles, distance, square, player;
      
      for (i = 0; i < state.squares.length; i++) {
        square = state.squares[i];
        classes = ['square'];
        styles = [];
       
        if (i % 10 === 0) {
          distance = 0;
          classes.push('big');
        } else {
          classes.push('small');
        }

        if (i < 10) {

          classes.push('bottom');
          styles.push('right:' + distance + '%');
        
        } else if (i < 20) {

          classes.push('left');
          styles.push('bottom: ' + distance + '%');      
        
        } else if (i < 30) {
        
          classes.push('top');
          styles.push('left: ' + distance + '%');
        
        } else {
          
          classes.push('right');
          styles.push('top: ' + distance + '%');
        
        }

        if (i % 10 === 0) distance += size1;
        else distance += size2;

        if (oldState && JSON.stringify(oldState.squares[i]) === JSON.stringify(state.squares[i])) {
          console.log('No news.');
          continue;
        }

        var $square = $('<div id="square' + i + '" class="' + classes.join(' ') + '" style="' + styles.join(';') + '">' + state.squares[i].title + '</div>');
        for (j = 0; j < square.players.length; j++) {
          player = square.players[j];
          $square.append('<div class="person" id="player' + player.joined +'"></div>');
        }
        
        $board.find('#square' + square.position).replaceWith($square);

      } // for

      oldState = state;
      
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
      //console.log('Interval');
      drawBoard();
    });
  }, 1000);

  $(window).on('resize', resizeBoard);

})(jQuery);

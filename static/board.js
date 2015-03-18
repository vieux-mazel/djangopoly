(function($) {
  var oldState = '';
  var $board = $('#board');
  resizeBoard();

  var gameId = document.URL.split('/');
  gameId = gameId[gameId.length - 2];

  function drawBoard(){
    $board.html('');

  $.getJSON('state/', function(state) {
    oldState = state;
    //console.log(state);

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

      var $square = $('<div id="square' + i + '" class="' + classes.join(' ') + '" style="' + styles.join(';') + '">' + state.squares[i].title + '</div>');
      for (j = 0; j < square.players.length; j++) {
        player = square.players[j];
        $square.append('<div class="person" id="player' + player.joined +'"></div>');
        console.log(player);
      }
      
      $board.append($square);
    }
    
  });
  }

  function resizeBoard() {
    $board.css({width: $board.height()});
  }

  $('#dice').click(function(){
    $.getJSON('/game/roll', function(data){
      console.log(data);
      if (data.success === true){
        drawBoard();
      }
    })
  });

  $('#end-turn').click(function(){
    console.log('asdf-click');
    $.getJSON('/game/end_turn', function(data){
      console.log(data);
      if (data.success === true){
        drawBoard();
      }
    })
  });
  drawBoard();

  setInterval(function() {
    $.getJSON('state', function(state) {
      if (JSON.stringify(state) !== JSON.stringify(oldState)) drawBoard();
    });
  }, 1000);

  $(window).on('resize', resizeBoard);

})(jQuery);

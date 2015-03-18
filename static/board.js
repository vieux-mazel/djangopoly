(function($) {
  var $board = $('#board');
  resizeBoard();

  var gameId = document.URL.split('/');
  gameId = gameId[gameId.length - 2];

  $.getJSON('state/', function(state) {
    //console.log(state);

    var size1 = 14;
    var size2 = 8;

    var i, classes, styles, distance, square;
    
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

      var $square = $('<div class="square ' + classes.join(' ')  + '" style="' + styles.join(';') + '"></div>');
      for (j = 0; j < square.players.length; j++) {
        $square.append('<div class="player"></div>');
      }

      $board.append($square);
      //$board.append('<div id="square' + i + '" class="' + classes.join(' ') + '" style="' + styles.join(';') + '">' + state.squares[i].title + '</div>');
    }
    
  });

  function resizeBoard() {
    $board.css({width: $board.height()});
  }

  $(window).on('resize', resizeBoard);

})(jQuery);
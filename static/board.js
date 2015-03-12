(function($) {
  var $board = $('#board');
  resizeBoard();

  $.getJSON('http://localhost:8000/game/1/state/', function(state) {
    //console.log(state);

    var i, e, squares = [];
    for (i = 0; i < state.length; i++) {
      e = state[i];
      if (e.model === 'monopoly.square') {
        squares.push(e);
      }
    }

    var size1 = 14;
    var size2 = 8;

    var classes, styles, distance;

    for (i = 0; i < squares.length; i++) {
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

      $board.append('<div id="square' + i + '" class="' + classes.join(' ') + '" style="' + styles.join(';') + '"></div>');
    }
  });

  function resizeBoard() {
    $board.css({width: $board.height()});
  }

  $(window).on('resize', resizeBoard);

})(jQuery);
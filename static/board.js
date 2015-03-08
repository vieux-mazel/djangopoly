(function($) {
  var $board = $('#board');
  resizeBoard();

  $.getJSON('http://localhost:8000/game/1/state/', function(state) {
    //console.log(state);

    var e, squares = [];
    for (i in state) {
      e = state[i];
      if (e.model === 'monopoly.square') {
        squares.push(e);
      }
    }

    
    var left = 0;
    var right = 0;
    var top = 0;
    var bottom = 0;
    var left = 0;
    for (i in squares) {
      var classes = 'square ';
      var styles = '';
     

      if (i == 0 || i == 10 || i == 20 || i == 30) {
        classes += 'big ';
      } else {
        classes += 'small ';
      }
      
      if (i < 10) {
        
        styles += 'bottom: 0;';
        styles += 'right: ' + right + '%';
        
        if (i == 0) right += 14;
        else right += 8;

      } else if (i >= 10 && i < 20) {

        classes += 'left ';

        styles += 'left: 0;';
        styles += 'bottom: ' + bottom + '%';

        if (i == 10) bottom += 14;
        else bottom += 8;
      
      } else if (i >= 20 && i < 30) {

        classes += 'top';

        styles += 'top: 0;';
        styles += 'left: ' + left + '%';

        if (i == 20) left += 14;
        else left += 8;

      } else {

        classes += 'right';

        styles += 'right: 0;'
        styles += 'top: ' + top + '%';

        if (i == 30) top += 14;
        else top += 8;

      }

      $board.append('<div id="square' + i + '" class="' + classes + '" style="' + styles + '"></div>');
    }
  });

  function resizeBoard() {
    $board.css({width: $board.height()});
  }


  $(window).on('resize', resizeBoard);

})(jQuery);
$(function() {

    var board = makeBoard(5,5);

    $('.tile').click(function() {
        var tile = $(this).index();
        playTile(tile, board, true);
    });
})

var makeBoard = function(width, height) {
    var board = new Array(width * height);
    var html = "";
    for(i = 0; i < board.length; i++) {
        board[i] = {
            graph: [(i - 1), (i + 1), (i + width), (i - width)],
            value: 0
        }
        html += "<a class='tile empty'>" + board[i].value + "</a>";
    }
    html += "<br class='clear'/>";
    $('#board').html(html);
    return board
}

var getNodes = function(board, current, nodes){
    nodes = nodes || new Array();
    nodes.push(current);
    for (i = 0; i < board[current].graph.length; i++) {
        var temp = board[current].graph[i];
        if ( !temp in nodes ) {
            if ( board[current].value === board[temp].value ) {
                var newpath = getNodes(board, temp);
                if ( newpath.length > 0 ) { nodes = nodes + newpath }
            }
        }
    }
    return $.unique(nodes)
}

var playTile = function(tile, board, increment) {
    console.log(tile); 
    console.log(board[tile].graph);
    console.log(increment);
    
    increment = increment || false;

    if (board[tile].value > 0) {
        console.log($('.tile').eq(tile));
        $('.tile').eq(tile).css('background', '#FF0000');
        //$('.tile').eq(tile).animate({background: "#FF0000"}, 750);
        //$('.tile').eq(tile).animate({background: "#EEEEEE"}, 750);
        //$('.tile').eq(tile).attr('class', 'tile empty');
        return false;
    } else {
        board[tile].value++;
        console.log(board[tile].value);
        $('.tile').eq(tile).html(board[tile].value);
        
        /*
        if (increment) {
            return true;

        }
        */
        //var current = parseInt($(this).html());
        //current++;
        //$(this).html(current);

    }
}
$(function() {
    $('.tile').click(function(){
        console.log(parseInt($(this).html()));
        if(parseInt($(this).html()) > 0) {
            $(this).animate({
                background: #FF0000    
            });
            //$(this).attr('class', 'tile taken');
        } else {
            var current = parseInt($(this).html());
            current++;
            $(this).html(current);
        }
    });
})

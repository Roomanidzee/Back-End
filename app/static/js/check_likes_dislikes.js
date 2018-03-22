$('#rating').likeDislike({
    reverseMode: false,
    disabledClass: 'disable',
    click: function (value, l, d, event) {
        var likes = $(this.element).find('.likes');
        var dislikes =  $(this.element).find('.dislikes');

        likes.text(parseInt(likes.text()) + l);
        dislikes.text(parseInt(dislikes.text()) + d);
    }
});
$('#rating2').likeDislike({
    reverseMode: true,
    disabledClass: 'disable',
    click: function (value, l, d, event) {
        var likes = $(this.element).find('.likes');
        var dislikes =  $(this.element).find('.dislikes');

        likes.text(parseInt(likes.text()) + l);
        dislikes.text(parseInt(dislikes.text()) + d);
    }
});
$('#rating3').likeDislike({
    readOnly: true,
    disabledClass: 'disable'
});
$(document).ready(function(){
    var socket = new WebSocket("ws://" + window.location.host + "/chat/");
    var msg = {
        'type': 'connect',
        'text': '',
        'user_name': ''
    };

    socket.onmessage = function(e) {
        console.log(e);
        var data = JSON.parse(e.data);
        var msgType = data.type;
        var user_name = data.user_name;
        var text = data.text;
        if (msgType == 'chat') {
            $('.chat-left').append('<div class="user-msg"><span class="user-name">' + user_name + ':</span>' +
                text + '</div>');
        }
        else if (msgType == 'connect') {
            $('.chat-right').append('<div class="user-name" id="' + user_name + '">'
                + user_name + '</div>');
        }
        else {
            $('#' + user_name).remove();
            // console.log('remove');
        }
    };

    socket.onopen = function() {
        msg.type = 'connect';
        msg.user_name = $('#user-name').val();
        socket.send(JSON.stringify(msg));
    };

    socket.onclose = function() {
        // console.log('disconnect');
        var user_name = $('#user_name').val();
        $('#' + user_name).remove();
    };

    if (socket.readyState == WebSocket.OPEN)
        socket.onopen();

    $('#btn-send').click(function() {
        // console.log(socket);
        msg.type = 'chat';
        msg.text = $('#chat-input').val();
        msg.user_name = $('#user-name').val();
        socket.send(JSON.stringify(msg));
    });
});
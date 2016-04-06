var chat_room_id = undefined;
var last_received = 0;
var initial_scroll = false;
var spy_code = undefined;
var is_commun = false;
/**
 * Initialize chat:
 * - Set the room id
 * - Generate the html elements (chat box, forms & inputs, etc)
 * - Sync with server
 * @param chat_room_id the id of the chatroom
 * @param html_el_id the id of the html element where the chat html should be placed
 * @return
 */
function init_chat(chat_id, html_el_id, spy_hash, is_com=false) {
	chat_room_id = chat_id;
	is_commun = is_com;
	spy_code = spy_hash;
	layout_and_bind(html_el_id);
	if (typeof spy_code === 'undefined' || spy_code == 'false') {
		sync_messages();
		get_messages();
	} else {
		get_spy_messages();
	}
}

var img_dir = "/static/img/";

/**
 * Asks the server which was the last message sent to the room, and stores it's id.
 * This is used so that when joining the user does not request the full list of
 * messages, just the ones sent after he logged in.
 * @return
 */
function sync_messages() {
    $.ajax({
        type: 'POST',
        data: {id:window.chat_room_id, is_commun:window.is_commun},
        url:'/chat/sync/',
		dataType: 'json',
		success: function (json) {
        	last_received = json.last_message_id;
		}
    });

	setTimeout("get_messages()", 2000);
}

/**
 * Generate the Chat box's HTML and bind the ajax events
 * @param target_div_id the id of the html element where the chat will be placed
 */
function layout_and_bind(html_el_id) {
		// layout stuff
		var html = '<div id="chat-messages-container">'+
		'<div id="chat-messages"> </div>'+
		'<div id="chat-last"> </div>'+
		'</div>' ;
		if (typeof spy_code === 'undefined' || spy_code == 'false') {
			html = html + '<form id="chat-form">'+
			'<input name="message" type="text" class="message" />'+
			'<input type="submit" value="Envoyer"/>'+
			'</form>';
		}

		$("#"+html_el_id).append(html);

		// event stuff
		if (typeof spy_code === 'undefined' || spy_code == 'false') {
	    	$("#chat-form").submit( function () {
	            var $inputs = $(this).children('input');
	            var values = {};

	            $inputs.each(function(i,el) {
	            	values[el.name] = $(el).val();
	            });
				values['chat_room_id'] = window.chat_room_id;
				values['is_commun'] = window.is_commun;
	        	$.ajax({
	                data: values,
	                dataType: 'json',
	                type: 'post',
	                url: '/chat/send/'
	            });
	            $('#chat-form .message').val('');
				get_messages()
	            return false;
			});
		}
};

/**
 * Gets the list of messages from the server and appends the messages to the chatbox
 */
function get_messages() {
    $.ajax({
        type: 'POST',
        data: {id:window.chat_room_id, offset: window.last_received, is_commun: window.is_commun},
        url:'/chat/receive/',
		dataType: 'json',
		success: function (json) {


			// first check if we are at the bottom of the div, if we are, we shall scroll once the content is added
			var $containter = $("#chat-messages-container");
			if ($containter.scrollTop() == $containter.attr("scrollHeight") - $containter.height())
				scroll = true;

			// add messages
			$.each(json, function(i,m){
				var timestamp = "<i>" + m.timestamp + "</i> "
				if(m.id != last_received){
					if (m.type == 's')
						$('#chat-messages').append('<div class="system">' + timestamp + replace_emoticons(m.message) + '</div>');
					else if (m.type == 'm')
						$('#chat-messages').append('<div class="message"><div class="author">' + timestamp +m.author+'</div>'+replace_emoticons(m.message) + '</div>');
					else if (m.type == 'j')
						$('#chat-messages').append('<div class="join">' + timestamp +m.author+' has joined</div>');
					else if (m.type == 'l')
						$('#chat-messages').append('<div class="leave">' + timestamp +m.author+' has left</div>');
					last_received = m.id;
					if (initial_scroll){
						var height = 0;
						$('#chat-messages-container div').each(function(i, value){ height += parseInt($(this).height());});
						height += '';
						$('#chat-messages-container').animate({scrollTop: height});
					}
				}
			})
			// scroll to bottom
			if (initial_scroll == false){
				var height = 0;
				$('#chat-messages-container div').each(function(i, value){ height += parseInt($(this).height());});
				height += '';
				$('#chat-messages-container').animate({scrollTop: height});
				initial_scroll = true;
			}
		}

    });
    // wait for next
    setTimeout("get_messages()", 2000);
}

/**
 * Gets the list of messages from the server and appends the messages to the chatbox
 */
function get_spy_messages() {
    $.ajax({
        type: 'POST',
        data: {spycode:window.spy_code, offset: window.last_received},
        url:'/chat/receive_spy/',
		dataType: 'json',
		success: function (json) {

			// first check if we are at the bottom of the div, if we are, we shall scroll once the content is added
			var $containter = $("#chat-messages-container");
			if ($containter.scrollTop() == $containter.attr("scrollHeight") - $containter.height())
				scroll = true;

			// add messages
			if (json == "error"){
				$('#chat-messages').append('<div class="system"> Le code d\'espionnage est incorrecte ! N\'essaie pas de tricher ! </div>');
			}
			$.each(json, function(i,m){
				var timestamp = "<i>" + m.timestamp + "</i> "
				if(m.id != last_received){
					if (m.type == 's')
						$('#chat-messages').append('<div class="system">' + timestamp + replace_emoticons(m.message) + '</div>');
					else if (m.type == 'm')
						$('#chat-messages').append('<div class="message"><div class="author">' + timestamp +m.author+'</div>'+replace_emoticons(m.message) + '</div>');
					else if (m.type == 'j')
						$('#chat-messages').append('<div class="join">' + timestamp +m.author+' has joined</div>');
					else if (m.type == 'l')
						$('#chat-messages').append('<div class="leave">' + timestamp +m.author+' has left</div>');
					last_received = m.id;
					if (initial_scroll){
						var height = 0;
						$('#chat-messages-container div').each(function(i, value){ height += parseInt($(this).height());});
						height += '';
						$('#chat-messages-container').animate({scrollTop: height});
					}
				}
			})
			// scroll to bottom
			if (initial_scroll == false){
				var height = 0;
				$('#chat-messages-container div').each(function(i, value){ height += parseInt($(this).height());});
				height += '';
				$('#chat-messages-container').animate({scrollTop: height});
				initial_scroll = true;
			}
		}

    });
    // wait for next
    setTimeout("get_spy_messages()", 2000);
}

/**
 * Tells the chat app that we are joining
 */
function chat_join() {
	$.ajax({
		async: false,
        type: 'POST',
        data: {chat_room_id:window.chat_room_id, is_commun:window.is_commun},
        url:'/chat/join/',
    });
}

/**
 * Tells the chat app that we are leaving
 */
function chat_leave() {
	$.ajax({
		async: false,
        type: 'POST',
        data: {chat_room_id:window.chat_room_id, is_commun:window.is_commun},
        url:'/chat/leave/',
    });
}

// attach join and leave events
if (typeof spy_code === 'undefined' || spy_code == 'false') {
	$(window).ready(function(){chat_join()});
	$(window).unload(function(){chat_leave()});
}
// emoticons
var emoticons = {
	'>:D' : 'emoticon_evilgrin.png',
	':D' : 'emoticon_grin.png',
	'=D' : 'emoticon_happy.png',
	':\\)' : 'emoticon_smile.png',
	':O' : 'emoticon_surprised.png',
	':P' : 'emoticon_tongue.png',
	':\\(' : 'emoticon_unhappy.png',
	':3' : 'emoticon_waii.png',
	';\\)' : 'emoticon_wink.png',
	'\\(ball\\)' : 'sport_soccer.png'
}

/**
 * Regular expression maddness!!!
 * Replace the above strings for their img counterpart
 */
function replace_emoticons(text) {
	$.each(emoticons, function(char, img) {
		re = new RegExp(char,'g');
		// replace the following at will
		text = text.replace(re, '<img src="'+img_dir+img+'" />');
	});
	return text;
}

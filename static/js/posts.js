
            window.onload = function(){
				
				var chatlist = $('#chat__list');
                var div = $('body');
                height = div.height();
				
				$.post("/respond", {"user_input" : ">!load_page"}, function(jsonData){
                        var x = JSON.stringify(jsonData)
                        x = JSON.parse(x)["response"]
                        console.log(x)
                        var ret = $("<li class=\"chat__list__item chat__list__item-new\"><a target=\"_blank\" href=\"#\" class=\"chat__list__item__author\">Chad</a><a target=\"_blank\" href=\"#\"><img class=\"chat__avatar\" src=\"{{ url_for('static', filename='img/avatar.png') }}\"></a><div class=\"chat__bubble\"><span>" + x + "</span></div></li>")
                        chatlist.append(ret);
                        div.animate({scrollTop: height}, 500);
                        height += div.height();
                    }, "json");
                    $('input[type="text"], textarea').val('');
			}
        
            $(document).ready(function(){
                
                var chatlist = $('#chat__list');
                var div = $('body');
                height = div.height();

                $.ajaxSetup({
                    dataType: "json"
                });
                
                $("form").submit(function(e){
                    e.preventDefault();
                    $.post("/send", $(this).serialize(), function(jsonData){
                        var x = JSON.stringify(jsonData)
                        x = JSON.parse(x)["message"]
                        var ret = "<li class=\"chat__list__item\"><div class=\"chat__bubble chat__bubble-response\"><span>" + x + "</span></div></li>"
                        chatlist.append(ret);
                        div.animate({scrollTop: height}, 500);
                        height += div.height();
                    }, "json");
                    $.post("/respond", $(this).serialize(), function(jsonData){
                        var x = JSON.stringify(jsonData)
                        x = JSON.parse(x)["response"]
                        console.log(x)
                        var ret = $("<li class=\"chat__list__item chat__list__item-new\"><a target=\"_blank\" href=\"#\" class=\"chat__list__item__author\">Chad</a><a target=\"_blank\" href=\"#\"><img class=\"chat__avatar\" src=\"{{ url_for('static', filename='img/avatar.png') }}\"></a><div class=\"chat__bubble\"><span>" + x + "</span></div></li>")
                        chatlist.append(ret);
                        div.animate({scrollTop: height}, 500);
                        height += div.height();
                    }, "json");
                    $('input[type="text"], textarea').val('');
                });
            });
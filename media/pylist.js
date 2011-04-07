var lfmData;
var users;
var userList;
$(document).ready(function(){
    $('#username-form').submit(function(e){
        $('.username-entry').slideUp('slow');
        $('#loading-icon').show();
        e.preventDefault();
        console.log('ajax start');
        $.ajax({
            type: "GET",
            url: "/user",
            data: "username="+"havok07",//$('#username-textbox').val(),
            success: function(data){
                console.log('ajax success');
                var allData = JSON.parse(data);
                lfmData = allData.lfmData;
                users = allData.userHash;
                userList = allData.userList;
                add_to_dom();
                process_user_divs();
                setup_user_palette();
            }
        }); 
        return false;
    });
    $('#username-form').submit();
});
function add_to_dom(){
    var len=lfmData.length;
    var container=$('#toplist-container');
    for (var i=0; i<len; i++){
        var topList = $('#toplist'+String(i));
        topList.show();
        topList.find('.artist-name').append(lfmData[i].artist_name);
        if (lfmData[i].artist_img.length > 0){
            topList.append('<img src="'+lfmData[i].artist_img+'" />');
        }
        var bar = topList.find('.artist-bar');
        for (var j=0; j<lfmData[i].listeners.length; j++){
            bar.append('<div class="user-div"><span class="username"></span></div>');
            bar.children().last().data('index', i);
        };
        
    };
    $('#loading-icon').hide();
    console.log('done');
};
function setup_user_palette(){
    for (var i=0; i<userList.length; i++){
        $('#user-palette').append('<div class="user-color"></div>');
        $('#user-palette').children().last().css('background-color', users[userList[i]]);
    }
    
}
function process_user_divs(){
    var maxWidth;
    var maxSum;
    $('.toplist-item').each(function(i, val){
        $(this).find('.artist-name').click(function(){
            $('.detailed-hud').empty();
            if ($(this).hasClass('selected')){
                $('.selected').removeClass('selected');
                return;
            }
            $(this).addClass('selected');
            var tracks = lfmData[i].tracks;
            for (var ti=0; ti<tracks.length; ti++){
                var track = tracks[ti];
                console.log(track);
                var userDeets = '';
                for (var li=0; li<track.listens.length; li++){
                    console.log(userDeets);
                    console.log(li);
                    userDeets = userDeets + track.listens[li].user + " (" + track.listens[li].playcount+") ";
                }
                $('.detailed-hud').append(
                    '<div class="detail">'+
                        '<div class="playcount">'+
                            String(track.playcount)+
                        '</div>'+
                        '<div class="duration-str">'+
                            String(track.duration)+' Seconds'+
                        '</div>'+
                        '<div class="trackname">'+
                        track.name+
                        '</div>'+
                        '<div class="user-detail">'+
                            userDeets+
                        '</div>'+
                        '<div class="duration-bar"></div>'+
                    '</div>'
                );
                var pct = track.duration / tracks[0].duration * 100;
                $('.detailed-hud').find('.duration-bar').last().css('width', pct + "%")
            }
            
        })
        var sumDuration = 0;
        $(val).find('.user-div').each(function(index, value){
            sumDuration+=lfmData[i].listeners[index].listening_duration;
        });
        $(val).find('.user-div').each(function(index, value){
            
            var listening_duration = lfmData[i].listeners[index].listening_duration;
            var width = parseInt(listening_duration)/sumDuration * 100;
            
            $(value).css('width', width + '%');
            $(value).css('background-color', users[lfmData[i].listeners[index].user]);
            $(value).find('span').append(lfmData[i].listeners[index].user);
            $(value).find('span').each(function(spanI, spanV){
                if ($(value).innerWidth() <= $(spanV).innerWidth()){
                    $(spanV).css('display','none');
                };
            });
            $(value).click(function(){
                $('.detailed-hud').empty();
                if ($(this).hasClass('selected')){
                    $('.selected').removeClass('selected');
                    return;
                }
                $('.selected').removeClass('selected');
                
                $(this).addClass('selected');
                var listens = lfmData[i].listeners[index].listens;
                for (var li=0; li<listens.length; li++){
                    var listen = listens[li];
                    $('.detailed-hud').append(
                        '<div class="detail">'+
                            '<div class="playcount">'+
                                String(listen.playcount)+
                            '</div>'+
                            '<div class="duration-str">'+
                                String(listen.duration)+' Seconds'+
                            '</div>'+
                            '<div class="trackname">'+
                            listen.name+
                            '</div>'+
                            '<div class="duration-bar"></div>'+
                        '</div>'
                    );
                    var pct = listen.duration / listens[0].duration * 100
                    
                    $('.detailed-hud').find('.duration-bar').last().css('width', pct + "%")
                }
            })
            //sumDuration+=$(value).data('data').
        });
        if (i==0){
            maxSum = sumDuration
        }
        
        //$(val).find('.artist-bar').css('width', String(sumDuration/maxSum * 100)+"%")
    });
};
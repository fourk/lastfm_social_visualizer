var youtubeReady = false;
//var videoID = 'Z19zFlPah-o';
var lfmData;
var users;
var userList;
var scrollIndex = 0;
var scrollCounter = 0;
var maxElements = 100;
var savedPlaylists;

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
                setup_nav_buttons();
                setup_playlist_stuff();
                hookEvent('toplist-container', 'mousewheel', printInfo);
            }
        }); 
        return false;
    });
    $('#username-form').submit();
});
function setup_playlist_stuff(){
    $('#playlist-form-close').click(function(){
        $('#playlist-form').hide();
    });
    $('#playlist-load').click(function(){
        $('#youtube-minimize').click();
        $('.playlist-form-contents').hide();
        $('#playlist-form').show();
        if (savedPlaylists === undefined){
            $('#loading-icon').show();
            $.ajax({
                url:'/playlists/load/',
                success: function(data){
                    $('.playlist-form-list').show();
                    savedPlaylists = JSON.parse(data).playlists;
                    $('#loading-icon').hide();
                    for (var i=0; i<savedPlaylists.length; i++){
                        $('.playlist-form-list').append('<div class="playlist-list-item clickable"><div class="playlist-name">'+savedPlaylists[i].name+'</div></div>');
                        $('.playlist-list-item').last().data('tracks', savedPlaylists[i].tracks);
                    }
                    $('.playlist-list-item').click(function(){
                        $('.playlist').append()
                        var tracks = $(this).data('tracks');
                        for (var i=0; i<tracks.length; i++){
                            addToPlaylist(tracks[i]);
                        }
                    })
                }
            });
        }
    });
    $('#playlist-save').click(function(){
        $('#youtube-minimize').click();
        $('.playlist-form-contents').hide();
        $('#playlist-form').show();
        $('.playlist-form-form').show();
    });
    $('#playlist-save-form').submit(function(e){
        e.preventDefault();
        $('#loading-icon').show();
        var playlistContents = [];
        $('.playlist-item').each(function(index, val){
            playlistContents.push($(val).data('id'));
        });
        $.ajax({
            type: 'POST',
            url: '/playlists/save/',
            data: {playlist_name: $('#playlist-textbox').val(),
                playlist: JSON.stringify(playlistContents)},
            success: function(data){
                var resp = JSON.parse(data);
                if(resp.status === 'exists'){
                    alert('pick a new name, that playlist name is taken already');
                }
                else{
                    $('#playlist-form').hide();
                }
                $('#loading-icon').hide();
            }
        })
        
    })
}
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
            bar.append('<div class="user-div clickable"><span class="username"></span></div>');
            bar.children().last().data('index', i);
        };
        bar.after('<div class="clear" />');
    };
    $('#loading-icon').hide();
    console.log('done');
};

var tag = document.createElement('script');
tag.src = "http://www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubePlayerAPIReady(){
    youtubeReady = true;
    $('#youtube-close').click(function(){
        $('#youtube-container').slideUp('fast', function(){
            $('#player').empty();
            $('#toplist-container').slideDown('fast');
        });
        $('#youtube-maximize').css('left','10px')
    });
    $('#youtube-minimize').click(function(){
        $('#youtube-container').slideUp('fast');
        $('#youtube-maximize').css('left','10px')
    });
    $('#youtube-maximize').click(function(){
        $('#youtube-container').slideDown('fast');
        $('#youtube-maximize').css('left','-125px');
    });
}
function youtube(resp){
    var videoID = resp.videoId;
    if (! youtubeReady){
        alert('WAIT IT OUT BRO. Youtube isn\'t ready yet! Or reload if its been a minute.');
        return;
    }
    console.log('made a player, player.');
    addToPlaylist(resp);
}
function addToPlaylist(track){
    if (player === undefined){
        player = new YT.Player('player', {
            height: '540',
            width: '800',
            videoId: track.videoId,
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange
            }
        });
    }
    $('.playlist').append('<div class="playlist-item" title="'+track.displayStr+'"><img src="'+track.image+'"><span class="up64">'+track.displayStr+'</span></div>');
    $('.playlist-item').last().tooltip({position: 'top center'});
    $('.playlist-item').last().data('videoId', track.videoId);
    $('.playlist-item').last().data('id', track.id);
    $('#youtube-maximize').css('left','-125px');
    if ($('.playlist-item').length === 1){
        $('.playlist-item').addClass('current-track');
    }
}
function onPlayerReady(event){
    $('#youtube-container').show();
    event.target.playVideo();
}

function onPlayerStateChange(event){
    console.log(event);
    /* YT.playerState.
    BUFFERING: 3
    CUED: 5
    ENDED: 0
    PAUSED: 2
    PLAYING: 1
    */
    if (event.data == YT.PlayerState.ENDED){
        if ($('.current-track ~ .playlist-item').length > 0){
            var upcoming = $('.current-track ~ .playlist-item');
            var next=upcoming.first();
            $('.current-track').removeClass('current-track');
            next.addClass('current-track');
            player.loadVideoById(next.data('videoId'));
        }
    }
}
function stopVideo(){
    player.stopVideo();
}

function setup_user_palette(){
    for (var i=0; i<userList.length; i++){
        $('#user-palette').append('<div class="user-color clickable"></div>');
        var elem = $('#user-palette').children().last();
        elem.css('background-color', users[userList[i]]);
        elem.data('id', i);
        elem.attr('title', userList[i]);
    }
    function colorFilter(){
        $('.checked').removeClass('checked');
        $(this).addClass('checked');
        if ($(this).data('id') === undefined){
            $('.toplist-item').removeClass('hidden');
            $('.toplist-item').addClass('shown');
            $('.toplist-item').slideDown('fast');
        }
        else{
            var user_name = userList[$(this).data('id')];
            $('.toplist-item').slideUp('fast');
            $('.toplist-item').removeClass('hidden');
            $('.toplist-item').removeClass('shown');
            var elements = $('span:contains('+user_name+')').closest('.toplist-item');
            elements.addClass('shown');
            elements.slideDown('fast');
            scale_user_divs();
        }
    };
    $('.user-color').click(colorFilter);
    $('.user-color').tooltip({position: "center right"});
};
/* ====================================================================================================== */
/*                                          SCROLLING RELATED SHIT                                        */
/* ====================================================================================================== */
function hookEvent(element, eventName, callback)
{
  if(typeof(element) == "string")
    element = document.getElementById(element);
  if(element == null)
    return;
  if(element.addEventListener)
  {
    if(eventName == 'mousewheel')
      element.addEventListener('DOMMouseScroll', callback, false);  
    element.addEventListener(eventName, callback, false);
  }
  else if(element.attachEvent)
    element.attachEvent("on" + eventName, callback);
}

function unhookEvent(element, eventName, callback)
{
  if(typeof(element) == "string")
    element = document.getElementById(element);
  if(element == null)
    return;
  if(element.removeEventListener)
  {
    if(eventName == 'mousewheel')
      element.removeEventListener('DOMMouseScroll', callback, false);  
    element.removeEventListener(eventName, callback, false);
  }
  else if(element.detachEvent)
    element.detachEvent("on" + eventName, callback);
};
function MouseWheel(e)
{
  e = e ? e : window.event;
  var wheelData = e.detail ? e.detail * -1 : e.wheelDelta / 40;
  //do something
  return cancelEvent(e);
}
function cancelEvent(e)
{
        e = e ? e : window.event;
        if(e.stopPropagation){
            e.stopPropagation();
        }
        if(e.preventDefault){
            e.preventDefault();
        }
        e.cancelBubble = true;
        e.cancel = true;
        e.returnValue = false;
        return false;
}
function printInfo(e)
{
    e = e ? e : window.event;
    var raw = e.detail ? e.detail : e.wheelDelta;
    var normal = e.detail ? e.detail * -1 : e.wheelDelta / 40;
    var target;
    if (Math.abs(scrollCounter+normal) < 100){
        scrollCounter+=normal;
    }
    function doScroll(){
        console.log(scrollCounter);
        if(scrollCounter > 0){
            scrollCounter= scrollCounter/2 -1;
            target = $('#nav-up');
        }
        else{
            scrollCounter= scrollCounter/2 +1;
            target = $('#nav-down');
        }
        target.click();
    }
    if (Math.abs(scrollCounter) > 1){
        //for(var i=0; Math.abs(scrollCounter) < 1; i++){
        doScroll();
        //}
    }
    while(Math.abs(scrollCounter) > 5){
        doScroll();
    }
    cancelEvent(e);
}
function setup_nav_buttons(){
    $('#nav-top').click(function(){
        $('.toplist-item').removeClass('hidden');
        $('.toplist-item').addClass('shown');
        $('.toplist-item').slideDown('fast');
        scale_user_divs();
    });
    $('#nav-up').click(function(){
        var elem = $('.hidden').last();
        elem.removeClass('hidden');
        elem.addClass('shown');
        elem.slideDown('fast');
        scale_user_divs();
        //$('.toplist-item:hidden').last().slideDown(100);
    });
    $('#nav-down').click(function(){
        var shown = $('.shown')
        if (shown.length > 1){
            var elem = shown.first();
            elem.addClass('hidden');
            elem.removeClass('shown');
            elem.slideUp('fast');
            scale_user_divs();
        }
        //$('.toplist-item:visible').first().slideUp(100);
    });
    $('#nav-bot').click(function(){
        $('.toplist-item:lt(93)').addClass('hidden');
        $('.toplist-item:lt(93)').slideUp('fast');
        scale_user_divs();
    });
}
function scale_user_divs(){
    var scrollStart = parseInt($('.shown').first().attr('id').split('toplist')[1])
    var scrollTo = Math.min(100,scrollStart+10);
    var elems = $('.shown');
    for (var i=0; i< Math.min(elems.length, 10); i++){
        var index = parseInt($($('.shown')[i]).attr('id').split('toplist')[1]);
        var pct = lfmData[index].sum_duration / lfmData[scrollStart].sum_duration * 92.5; //this means that the calculated width of the first item is 885.
        var artist_bar = $('#toplist'+String(index)).find('.artist-bar');
        artist_bar.stop();
        artist_bar.animate({width: pct+'%'}, 'fast');
    }
}
/* ====================================================================================================== */
/*                                     /END SCROLLING RELATED SHIT                                        */
/* ====================================================================================================== */


function trackClick(){
    if ($(this).data('id') === ''){
        alert('fuck, man. no youtube video available.');
    }
    else{
        console.log('WTB RESP');
        $.ajax({
            url: '/youtube/'+$(this).data('id'),
            success: function(data){
                var resp = JSON.parse(data);
                console.log('GOTRESP');
                console.log(resp);
                if (resp.status === 'error'){
                    alert('Sorry! Couldn\'t find that track on Youtube.');
                }
                else{
                    youtube(resp);
                }
            }
        })
    }
};
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
                $('.detailed-hud').find('.duration-bar').last().css('width', pct + "%");
                $('.trackname').last().data('id', track.id);
            }
            $('.trackname').click(trackClick);
        });
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
                    console.log(listen);
                    $('.trackname').last().data('id', listen.id);
                    $('.detailed-hud').find('.duration-bar').last().css('width', pct + "%")
                }
                $('.trackname').click(trackClick);
            })
            //sumDuration+=$(value).data('data').
        });
        if (i==0){
            maxSum = sumDuration
        }
        
        //$(val).find('.artist-bar').css('width', String(sumDuration/maxSum * 100)+"%")
    });
};
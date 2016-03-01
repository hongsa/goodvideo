$(document).ready(function() {

    var adCallUrl = "http://mtag.mman.kr/interjs.mezzo/makegood/goodvideo/interstitial";
    var currentOS;
    var isMobile = (/iphone|ipad|ipod|android/i.test(navigator.userAgent.toLowerCase()));

    if (isMobile) {
        var _userAgent = navigator.userAgent.toLowerCase();
        if (_userAgent.search("android") > -1)
            currentOS = "3"; //android
        else if ((_userAgent.search("iphone") > -1) || (_userAgent.search("ipod") > -1)
            || (_userAgent.search("ipad") > -1))
            currentOS = "2"; //ios
        else
            currentOS = "6"; //etc
    } else {
        currentOS = "5"; //pc
    }

    adCallUrl = adCallUrl + '?os='+currentOS;
    //console.log(ad);


    $.ajax({
        url: adCallUrl,
        dataType: 'JSON',
        method: 'POST',
        data:{
        },
        success: function (data) {
            if( typeof data !== 'object') return;
            var string1 = '<a href="'+data.click_api+'"'+'target="_blank">'+'<img src="' + data.img_path + '"'
                + 'style="margin: 0 auto;"'+'class="img-responsive ad_big"'+'>'+'</a>';

            $('#mezzo_ad').append(string1);
        },
        error :
            $('#layerpop').modal('hide')

    });

});

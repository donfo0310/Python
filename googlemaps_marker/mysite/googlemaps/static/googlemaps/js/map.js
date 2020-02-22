var map;

function read_json_to_marking() {

    // centerposition and options
    var latlng = new google.maps.LatLng(35.383575, 139.344170);

    var options = {
        zoom: 10,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    // create canvas and read json
    map = new google.maps.Map(document.getElementById("map_canvas"), options);
    map.setCenter(latlng);
    // url: pythonが mysite からdumpするときと documentroot からjsonをreadするときでは当然パスが違う（ハマりポイント）
    jQuery.ajax({
        type: 'GET',
        url: '/static/googlemaps/js/data.json',
        dataType: 'json',
        async: false,
        success: function(data){
            json = data;
        }
    });

    // JSONの要素数分マーカーを作成
    if (json != null){
        for (i = 0; i < json.length; i++) {
            latlng = new google.maps.LatLng(json[i].lat, json[i].lng);
            var marker = new google.maps.Marker({
                position: latlng,
                map: map
            });
        }
    }

}
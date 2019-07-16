var map;

function initialize() {

    // 中心位置を設定
    var latlng = new google.maps.LatLng(35.383575, 139.344170);

    // 地図のオプションを設定
    var options = {
        zoom: 10,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    // キャンパスの要素を取得
    map = new google.maps.Map(document.getElementById("map_canvas"), options);
    map.setCenter(latlng);

    // url: Pythonがローカルへ出力するときと、ブラウザから（Djangoが "効いて"）読み込むときでは当然パスの捉え方が違う（ハマりポイント）
    jQuery.ajax({
        type: 'GET',
        url: '/static/js/data.json',
        dataType: 'json',
        async: false,
        success: function(data){
            json = data;
        }
    });

    //JSONの要素数分マーカーを作成
    for (i = 0; i < json.length; i++) {
        latlng = new google.maps.LatLng(json[i].lat, json[i].lng);
        var marker = new google.maps.Marker({
            position: latlng,
            map: map
        });
    }

}
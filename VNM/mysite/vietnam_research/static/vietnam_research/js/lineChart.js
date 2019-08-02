const LineChart = function (dataset) {

  // 50x50のsvg領域を作る
  var w = 50;
  var h = 50;
  var svg = d3.select("body")
    .append("svg")
    .attr("width", w)
    .attr("height", h);

  // datasetを{x,y}の座標の配列に変換する。
  // X座標は、領域全体を個数で割って全体を使えるようにする。
  // 原点が左上なので、Y座標は最大値から引き算する
  // それぞれ2ずらしているのは、0地点の場合に線が欠けるため。
  var  pathinfo = [];
  var b_x = w / dataset.length;
  for (var i=0; i<dataset.length; i++) {
    pathinfo.push(
      {
        x: b_x * i + 2, 
        y: ((h - 2) - dataset[i] * 10) 
      });
  }

  // 座標データから折れ線グラフ用のコマンドを作るための関数を用意
  var d3line = d3.line()
    .x(function(d){return d.x;})
    .y(function(d){return d.y;})
    .curve(d3.curveLinear); // エッジがシャープな折れ線を指定。
  // 参考 https://www.dashingd3js.com/svg-paths-and-d3js

  // 実際に線を引く。
  svg.append("path")
    .attr("d", d3line(pathinfo))  // さきほどの関数に座標の配列を引数で渡す
    .style("stroke-width", 2)     // 線の太さを決める
    .style("stroke", "#ff5900")   // 色を決める
    .style("fill", "none");

}
const LineChart = function (chart_id, labelset, dataset) {

  var ctx = document.getElementById(chart_id).getContext('2d');

  var chart = new Chart(ctx, {
      // The type of chart we want to create
      type: 'line',

      // The data for our dataset
      data: {
          labels: labelset,
          datasets: dataset
      },

      // Configuration options go here
      options: {
        responsive: false,
        maintainAspectRatio: false
      }
  });

}
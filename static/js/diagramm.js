new Chart(document.getElementById("myDoughnutChart"), {
    type: 'doughnut',
    data: {
      labels: ["Вконтакте", "Ютуб", "Телеграм"],
      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#5181B8","#FE0000","#27A5E7"],
          hoverBorderWidth:10,
          borderColor:"white",

          data: [40,20,15]
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Пример заголовка',
        fontSize:16,
      }
    }
});

var ctx2 = document.getElementById('lineChart').getContext('2d');
var chart = new Chart(ctx2, {
    // The type of chart we want to create
    type: 'bar',
data: {
      labels: ["Вконтакте", "Ютуб", "Телеграм"],
      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#5181B8","#FE0000","#27A5E7"],
          hoverBorderWidth:10,
          borderColor:"white",

          data: [40,20,15]
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Пример заголовка',
        fontSize:16,
      }
    }

















    // The data for our dataset
    // data: {
    //     labels:labels,
    //     datasets: datasets
    // },

    // // Configuration options go here
    // options: {scales: {
    //         xAxes: [{
    //             stacked: true
    //         }],
    //         yAxes: [{
    //             stacked: false
    //         }]

    //     }}
});


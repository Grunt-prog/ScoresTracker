const chartCanvas = document.getElementById('myChart');

    // Create the chart
    const myChart = new Chart(chartCanvas, {
        type: 'line', // Set the chart type
        data: {
            labels: ,
            datasets: [{
                label: 'My Dataset',
                data: [10, 20, 15, 25, 30, 20],
                borderColor: 'blue',
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
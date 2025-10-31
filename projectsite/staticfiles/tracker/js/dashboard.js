// Daily Logs Chart
const dailyLogsCtx = document.getElementById('dailyLogsChart');
if (dailyLogsCtx) {
    const dailyData = JSON.parse(document.getElementById('daily-counts-data').textContent);
    new Chart(dailyLogsCtx, {
        type: 'line',
        data: {
            labels: dailyData.map(d => d.date),
            datasets: [{
                label: 'Meals Logged',
                data: dailyData.map(d => d.count),
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.1,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1 }
                }
            }
        }
    });
}

// Meal Type Chart
const mealTypeCtx = document.getElementById('mealTypeChart');
if (mealTypeCtx) {
    const mealData = JSON.parse(document.getElementById('meal-distribution-data').textContent);
    new Chart(mealTypeCtx, {
        type: 'doughnut',
        data: {
            labels: mealData.map(d => d.meal_type.charAt(0).toUpperCase() + d.meal_type.slice(1)),
            datasets: [{
                data: mealData.map(d => d.count),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}
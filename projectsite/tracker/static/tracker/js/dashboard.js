// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
console.log('Dashboard charts initializing...');

// Common Chart Configuration
Chart.defaults.color = '#e2e8f0';
Chart.defaults.borderColor = 'rgba(102, 126, 234, 0.2)';
Chart.defaults.font.family = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";

const commonOptions = {
    responsive: true,
    maintainAspectRatio: true,
    interaction: {
        mode: 'index',
        intersect: false,
    },
    plugins: {
        legend: {
            labels: {
                color: '#e2e8f0',
                font: {
                    size: 12,
                    weight: '600'
                },
                padding: 15,
                usePointStyle: true
            }
        },
        tooltip: {
            backgroundColor: 'rgba(30, 58, 95, 0.95)',
            titleColor: '#e2e8f0',
            bodyColor: '#cbd5e0',
            borderColor: 'rgba(102, 126, 234, 0.5)',
            borderWidth: 1,
            padding: 12,
            displayColors: true,
            titleFont: {
                size: 14,
                weight: 'bold'
            },
            bodyFont: {
                size: 13
            }
        }
    },
    scales: {
        x: {
            grid: {
                color: 'rgba(102, 126, 234, 0.1)',
                drawBorder: false
            },
            ticks: {
                color: '#cbd5e0',
                font: {
                    size: 11
                }
            }
        },
        y: {
            beginAtZero: true,
            grid: {
                color: 'rgba(102, 126, 234, 0.1)',
                drawBorder: false
            },
            ticks: {
                color: '#cbd5e0',
                font: {
                    size: 11
                }
            }
        }
    }
};

// 1. Main Calorie Chart with Goal Line
const caloriesCtx = document.getElementById('caloriesChart');
const caloriesDataEl = document.getElementById('calories-data');
const calorieGoalEl = document.getElementById('calorie-goal');

if (caloriesCtx && caloriesDataEl && calorieGoalEl) {
    const caloriesData = JSON.parse(caloriesDataEl.textContent);
    const calorieGoal = parseInt(calorieGoalEl.textContent);
    const labels = caloriesData.map(d => d.date);
    const values = caloriesData.map(d => d.calories);
    const goalLine = new Array(labels.length).fill(calorieGoal);

    new Chart(caloriesCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Actual Calories',
                    data: values,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.3)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 5,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#667eea',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointHoverBackgroundColor: '#764ba2',
                    pointHoverBorderColor: '#fff',
                },
                {
                    label: 'Goal',
                    data: goalLine,
                    borderColor: '#f093fb',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    borderDash: [10, 5],
                    tension: 0,
                    fill: false,
                    pointRadius: 0,
                    pointHoverRadius: 0
                }
            ]
        },
        options: {
            ...commonOptions,
            plugins: {
                ...commonOptions.plugins,
                legend: {
                    ...commonOptions.plugins.legend,
                    position: 'top',
                },
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(0) + ' kcal';
                        }
                    }
                }
            },
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: function(value) {
                            return value.toFixed(0) + ' kcal';
                        }
                    }
                }
            }
        }
    });
}

// 2. Combined Macronutrients Chart
const macrosComboCtx = document.getElementById('macrosComboChart');
const proteinDataEl2 = document.getElementById('protein-data');
const carbsDataEl2 = document.getElementById('carbs-data');
const fatDataEl2 = document.getElementById('fat-data');

if (macrosComboCtx && proteinDataEl2 && carbsDataEl2 && fatDataEl2) {
    const proteinData = JSON.parse(proteinDataEl2.textContent);
    const carbsData = JSON.parse(carbsDataEl2.textContent);
    const fatData = JSON.parse(fatDataEl2.textContent);
    
    new Chart(macrosComboCtx, {
        type: 'line',
        data: {
            labels: proteinData.map(d => d.date),
            datasets: [
                {
                    label: 'Protein',
                    data: proteinData.map(d => d.value),
                    borderColor: '#11998e',
                    backgroundColor: 'rgba(17, 153, 142, 0.1)',
                    borderWidth: 2.5,
                    tension: 0.4,
                    fill: false,
                    pointRadius: 3,
                    pointHoverRadius: 6
                },
                {
                    label: 'Carbs',
                    data: carbsData.map(d => d.value),
                    borderColor: '#4facfe',
                    backgroundColor: 'rgba(79, 172, 254, 0.1)',
                    borderWidth: 2.5,
                    tension: 0.4,
                    fill: false,
                    pointRadius: 3,
                    pointHoverRadius: 6
                },
                {
                    label: 'Fat',
                    data: fatData.map(d => d.value),
                    borderColor: '#fa709a',
                    backgroundColor: 'rgba(250, 112, 154, 0.1)',
                    borderWidth: 2.5,
                    tension: 0.4,
                    fill: false,
                    pointRadius: 3,
                    pointHoverRadius: 6
                }
            ]
        },
        options: {
            ...commonOptions,
            plugins: {
                ...commonOptions.plugins,
                legend: {
                    ...commonOptions.plugins.legend,
                    position: 'top',
                },
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(1) + 'g';
                        }
                    }
                }
            },
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: function(value) {
                            return value.toFixed(0) + 'g';
                        }
                    }
                }
            }
        }
    });
}

// 3. Nutrient Distribution Chart (Today's Macros)
const nutrientDistCtx = document.getElementById('nutrientDistributionChart');
const proteinDataEl = document.getElementById('protein-data');
const carbsDataEl = document.getElementById('carbs-data');
const fatDataEl = document.getElementById('fat-data');

if (nutrientDistCtx && proteinDataEl && carbsDataEl && fatDataEl) {
    const proteinData = JSON.parse(proteinDataEl.textContent);
    const carbsData = JSON.parse(carbsDataEl.textContent);
    const fatData = JSON.parse(fatDataEl.textContent);
    
    console.log('Protein Data:', proteinData);
    console.log('Carbs Data:', carbsData);
    console.log('Carbs Data Detail:', JSON.stringify(carbsData, null, 2));
    console.log('Fat Data:', fatData);
    
  
    const todayProtein = proteinData.length > 0 ? proteinData[proteinData.length - 1].value : 0;
    const todayCarbs = carbsData.length > 0 ? carbsData[carbsData.length - 1].value : 0;
    const todayFat = fatData.length > 0 ? fatData[fatData.length - 1].value : 0;
    
    console.log('Today Protein:', todayProtein);
    console.log('Today Carbs:', todayCarbs);
    console.log('Today Fat:', todayFat);
    
    if (todayCarbs === 0 && (todayProtein > 0 || todayFat > 0)) {
        console.warn('⚠️ Carbohydrates are 0 but other macros exist. Check if nutrition_data has carbohydrates_total_g field.');
    }
    
    const totalMacros = parseFloat(todayProtein) + parseFloat(todayCarbs) + parseFloat(todayFat);
    
    console.log('Total Macros:', totalMacros);
    
    if (totalMacros > 0) {
        // Ensure all values are valid numbers
        const chartData = [
            parseFloat(todayProtein) || 0,
            parseFloat(todayCarbs) || 0,
            parseFloat(todayFat) || 0
        ];
        
        console.log('Chart Data Array:', chartData);
        
        new Chart(nutrientDistCtx, {
            type: 'doughnut',
            data: {
                labels: ['Protein', 'Carbohydrates', 'Fat'],
                datasets: [{
                    data: chartData,
                    backgroundColor: [
                        'rgba(17, 153, 142, 0.9)',
                        'rgba(79, 172, 254, 0.9)',
                        'rgba(250, 112, 154, 0.9)'
                    ],
                    borderColor: [
                        '#11998e',
                        '#4facfe',
                        '#fa709a'
                    ],
                    borderWidth: 2,
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#e2e8f0',
                            font: {
                                size: 12,
                                weight: '600'
                            },
                            padding: 15,
                            usePointStyle: true,
                            generateLabels: function(chart) {
                                const data = chart.data;
                                return data.labels.map((label, i) => {
                                    const value = data.datasets[0].data[i];
                                    const total = data.datasets[0].data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return {
                                        text: `${label}: ${value.toFixed(1)}g (${percentage}%)`,
                                        fillStyle: data.datasets[0].backgroundColor[i],
                                        hidden: false,
                                        index: i
                                    };
                                });
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(30, 58, 95, 0.95)',
                        titleColor: '#e2e8f0',
                        bodyColor: '#cbd5e0',
                        borderColor: 'rgba(102, 126, 234, 0.5)',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return context.label + ': ' + value.toFixed(1) + 'g (' + percentage + '%)';
                            }
                        }
                    }
                }
            }
        });
    } else {
        // Show message if no data
        nutrientDistCtx.parentElement.innerHTML = '<p style="text-align: center; color: #cbd5e0; padding: 50px 0;">No nutrient data for today</p>';
    }
}

}); // End DOMContentLoaded
// Get the data from the HTML script tag
var dailyExpensesData = JSON.parse(document.getElementById('dailyExpensesData').textContent);

// Prepare data for the chart
var labels = dailyExpensesData.map(function(item) { 
    // Format each date as 'Month Name Day' (e.g., 'March 5')
    var date = new Date();
    date.setDate(item.day); // Set the day from the data
    var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var monthName = monthNames[date.getMonth()];
    return monthName + ' ' + item.day; 
});
var expenses = dailyExpensesData.map(function(item) { return item.total; });

// Use Chart.js (or any other charting library) to plot the data
var ctx = document.getElementById('dailyExpenseChart').getContext('2d');
var dailyExpenseChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,  // Month and Day
        datasets: [{
            label: 'Daily Expenses',
            data: expenses,  // Expense amounts
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false
        }]
    },
    options: {
        scales: {
            y: {
                min: 0,  // Set the minimum value of y-axis to 0
                ticks: {
                    // Add $ sign to each tick value
                    callback: function(value) {
                        return '$' + value.toFixed(2);  // Format the value as currency
                    }
                }
            }
        }
    }
});

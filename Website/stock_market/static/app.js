document.addEventListener('DOMContentLoaded', () => {
    let series; // Declare series here
    let chart; // Declare chart here
    let socket; // WebSocket variable
    let dataPoints = []; // Store data points here

    if (typeof LightweightCharts === 'undefined') {
        console.error('LightweightCharts is not defined');
    } else {
        console.log('LightweightCharts is available');
    }

    // Initialize TradingView chart
    function initializeChart() {
        if (!chart) {
            chart = LightweightCharts.createChart(document.getElementById('candlestick-chart'), {
                width: 600,
                height: 400,
                layout: {
                    textColor: '#000',
                    background: { type: 'solid', color: '#FFF' }
                },
                grid: {
                    vertLines: { color: '#eee' },
                    horzLines: { color: '#eee' }
                },
                crossHair: { mode: 0 },
                priceScale: { borderColor: '#aaa' },
                timeScale: { borderColor: '#aaa' }
            });

            series = chart.addCandlestickSeries({
                upColor: '#4fff8a',
                borderUpColor: '#4fff8a',
                wickUpColor: '#4fff8a',
                color: '#ff4976',
                borderColor: '#ff4976',
                wickColor: '#ff4976',
            });

            // Initialize the chart with some data if available
            if (dataPoints.length > 0) {
                series.setData(dataPoints);
            }
        }
    }

    // Initialize WebSocket connection
    function initializeWebSocket() {
        socket = new WebSocket('ws://localhost:8765');

        socket.onopen = function() {
            console.log('WebSocket connection opened.');
        };

        socket.onclose = function(event) {
            console.log('WebSocket connection closed:', event);
            // Attempt to reconnect if needed
            setTimeout(() => {
                initializeWebSocket(); // Reinitialize WebSocket
            }, 1000);
        };

        socket.onerror = function(error) {
            console.error('WebSocket error:', error);
        };

        socket.onmessage = function(event) {
            const price = parseFloat(event.data);
            console.log(`Received price: ${price}`);
            document.getElementById('price').innerText = `Current Price: $${price}`;

            const now = Math.floor(new Date().getTime() / 1000); // Convert to Unix timestamp
            const dataPoint = {
                time: now,
                open: price,
                high: price + 1,
                low: price - 1,
                close: price
            };

            // Add new data point and keep only the last `maxDataPoints` points
            dataPoints.push(dataPoint);
            if (series) {
                series.setData(dataPoints); // Update the series with the fixed-size data buffer
            } else {
                console.error('Series is not initialized.');
            }
        };
    }

    initializeChart(); // Initialize the chart
    initializeWebSocket(); // Initialize WebSocket connection

    // Fetch transactions initially and then every 5 seconds
    function fetchTransactions() {
        fetch('/transactions')
            .then(response => response.json())
            .then(data => {
                const transactionsList = document.getElementById('transactions-list');
                transactionsList.innerHTML = ''; // Clear any existing content

                if (data.transactions && data.transactions.length > 0) {
                    data.transactions.forEach(transaction => {
                        const listItem = document.createElement('li');
                        listItem.className = 'text-lg';
                        listItem.textContent = `${transaction.quantity} shares at $${transaction.price}`;
                        transactionsList.appendChild(listItem);
                    });
                } else {
                    const emptyMessage = document.createElement('li');
                    emptyMessage.className = 'text-lg';
                    emptyMessage.textContent = 'No transactions available.';
                    transactionsList.appendChild(emptyMessage);
                }
            })
            .catch(error => console.error('Error fetching transactions:', error));
    }
    
    fetchTransactions();
    setInterval(fetchTransactions, 5000); // Update transactions every 5 seconds
});

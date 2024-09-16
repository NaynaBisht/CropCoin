document.addEventListener('DOMContentLoaded', () => {
    let series; // Declare series here
    let chart; // Declare chart here
    let socket; // WebSocket variable
    let historicalData = []; // Store historical data here
    let liveData = []; // Store live data here
    let lastUpdate = Date.now();

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

            // Initialize the chart with historical data if available
            if (historicalData.length > 0) {
                series.setData(historicalData);
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
            const liveDataPoint = {
                time: now,
                open: price,
                high: price,
                low: price,
                close: price
            };

            liveData.push(liveDataPoint);

            // Add live data to the chart
            if (series) {
                series.update(liveDataPoint);
            } else {
                console.error('Series is not initialized.');
            }

            // Aggregate historical data to 1-minute intervals
            historicalData = aggregateDataToMinute(liveData);
            if (series) {
                series.setData(historicalData); // Update historical data on the chart
            }
        };
    }

    // Function to aggregate data to 1-minute intervals
    function aggregateDataToMinute(dataPoints) {
        const aggregated = [];
        let currentMinute = Math.floor(dataPoints[0].time / 60) * 60;
        let open = dataPoints[0].open;
        let high = dataPoints[0].high;
        let low = dataPoints[0].low;
        let close = dataPoints[0].close;

        dataPoints.forEach(point => {
            const minute = Math.floor(point.time / 60) * 60;
            if (minute !== currentMinute) {
                aggregated.push({ time: currentMinute, open, high, low, close });
                currentMinute = minute;
                open = point.open;
                high = point.high;
                low = point.low;
                close = point.close;
            } else {
                high = Math.max(high, point.high);
                low = Math.min(low, point.low);
                close = point.close;
            }
        });

        // Push the last interval data
        aggregated.push({ time: currentMinute, open, high, low, close });

        return aggregated;
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
    setInterval(fetchTransactions, 2000); // Update transactions every 2 seconds
});

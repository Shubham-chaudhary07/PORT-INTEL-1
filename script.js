let attackChart, severityChart;
let logs = [];
let honeypotInterval = null;

// Map severity to impact
const severityImpact = { LOW: 1, MEDIUM: 3, HIGH: 5 };

// Function to generate a simulated attack
function generateAttack() {
    const severities = ['LOW', 'MEDIUM', 'HIGH'];
    const services = ['SSH', 'FTP', 'HTTP', 'MySQL'];
    const severity = severities[Math.floor(Math.random() * severities.length)];
    const service = services[Math.floor(Math.random() * services.length)];
    const timestamp = new Date().toLocaleTimeString();

    const log = {
        timestamp,
        severity,
        source_ip: `192.168.${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}`,
        source_port: Math.floor(Math.random()*65535),
        destination_port: service === 'SSH' ? 22 : service === 'FTP' ? 21 : service === 'HTTP' ? 80 : 3306
    };

    logs.push(log);
    if (logs.length > 100) logs.shift(); // keep last 100 attacks
    updateDashboard(log);
}

// Function to update logs and charts
function updateDashboard(latestLog = null) {
    const logBox = document.getElementById('logBox');
    logBox.innerHTML = "";
    logs.slice().reverse().forEach(l => {
        const div = document.createElement('div');
        div.className = `log-entry ${l.severity}`;
        div.textContent =
            `[${l.timestamp}] ${l.source_ip}:${l.source_port} → ${l.destination_port} | ${l.severity}`;
        logBox.appendChild(div);
    });

    // Update impact box
    if (latestLog) {
        document.getElementById('impactBox').textContent =
            `Impact: ${severityImpact[latestLog.severity]} (${latestLog.severity})`;
    }

    // Weighted frequency based on severity for zigzag
    const attackLabels = logs.map(l => l.timestamp);
    let cumulativeValue = 0;
    const attackData = logs.map(l => {
        const value = severityImpact[l.severity];
        cumulativeValue += value;
        return cumulativeValue;
    });

    if (attackChart) attackChart.destroy();
    attackChart = new Chart(document.getElementById("attackChart"), {
        type: "line",
        data: {
            labels: attackLabels,
            datasets: [{
                label: "Attack Frequency",
                data: attackData,
                borderColor: "#38bdf8",
                backgroundColor: "rgba(56, 189, 248,0.3)",
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            animation: false,
            scales: {
                x: { title: { display: true, text: 'Time' } },
                y: { title: { display: true, text: 'Frequency' }, beginAtZero: true }
            }
        }
    });

    // Update severity chart
    const count = { LOW: 0, MEDIUM: 0, HIGH: 0 };
    logs.forEach(l => count[l.severity]++);
    if (severityChart) severityChart.destroy();
    severityChart = new Chart(document.getElementById("severityChart"), {
        type: 'doughnut',
        data: {
            labels: ["LOW", "MEDIUM", "HIGH"],
            datasets: [{
                data: [count.LOW, count.MEDIUM, count.HIGH],
                backgroundColor: ["#4ade80", "#facc15", "#f87171"]
            }]
        },
        options: { responsive: true, animation: false }
    });
}

// Honeypot control functions
function startHoneypot() {
    if (honeypotInterval) return;
    honeypotInterval = setInterval(generateAttack, 1000);
}

function stopHoneypot() {
    clearInterval(honeypotInterval);
    honeypotInterval = null;
}

function simulateAttack() {
    generateAttack();
}

console.log("SCRIPT LOADED");

async function loadSentiment() {
    const res = await fetch("/api/sentiment");
    const data = await res.json();

    console.log("Sentiment data:", data);

    new Chart(document.getElementById("sentimentChart"), {
        type: "bar",
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: "Reviews",
                data: Object.values(data),
                backgroundColor: ["#4CAF50", "#FFC107", "#F44336"]
            }]
        }
    });
}

async function loadKeywords() {
    const res = await fetch("/api/keywords");
    const data = await res.json();

    console.log("Keyword data:", data);

    const labels = data.map(r => r.keyword);
    const values = data.map(r => r.frequency);

    new Chart(document.getElementById("keywordChart"), {
        type: "bar",
        data: {
            labels: labels.slice(0, 10),
            datasets: [{
                label: "Keyword Frequency",
                data: values.slice(0, 10),
                backgroundColor: "#2196F3"
            }]
        }
    });
}

loadSentiment();
loadKeywords();

document.getElementById("status").innerText = "Dashboard loaded";

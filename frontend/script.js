const API_BASE = "http://127.0.0.1:8000";

async function fetchScore() {
    const sbd = document.getElementById("sbdInput").value.trim();
    if (!sbd) return;
    const res = await fetch(`${API_BASE}/score/${sbd}`);
    if (res.ok) {
        const data = await res.json();
        document.getElementById("scoreResult").textContent = JSON.stringify(data, null, 2);
    } else {
        document.getElementById("scoreResult").textContent = "Không tìm thấy SBD";
    }
}

async function fetchStats() {
    const res = await fetch(`${API_BASE}/stats`);
    const stats = await res.json();
    const labels = Object.keys(stats);
    const datasets = [
        { label: ">=8", data: labels.map(subj => stats[subj][">=8"]) },
        { label: "6-8", data: labels.map(subj => stats[subj]["6-8"]) },
        { label: "4-6", data: labels.map(subj => stats[subj]["4-6"]) },
        { label: "<4", data: labels.map(subj => stats[subj]["<4"]) }
    ];
    new Chart(document.getElementById("statsChart"), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets.map((d, i) => ({
                ...d,
                backgroundColor: `hsl(${i*90}, 70%, 50%)`
            }))
        },
        options: { responsive: true }
    });
}

async function fetchTop10() {
    const res = await fetch(`${API_BASE}/top10`);
    const data = await res.json();
    const tbody = document.querySelector("#top10Table tbody");
    tbody.innerHTML = "";
    data.forEach(st => {
        const total = (st.toan||0) + (st.vat_li||0) + (st.hoa_hoc||0);
        tbody.innerHTML += `<tr>
            <td>${st.sbd}</td>
            <td>${st.toan||""}</td>
            <td>${st.vat_li||""}</td>
            <td>${st.hoa_hoc||""}</td>
            <td>${total.toFixed(2)}</td>
        </tr>`;
    });
}

fetchStats();
fetchTop10();

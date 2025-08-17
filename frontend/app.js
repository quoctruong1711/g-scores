const API_URL = "http://127.0.0.1:8000";  // backend FastAPI

function getSubjectLabel(subject) {
  const map = {
    toan: "Toán",
    ngu_van: "Ngữ văn",
    ngoai_ngu: "Ngoại ngữ",
    vat_li: "Vật lí",
    hoa_hoc: "Hóa học",
    sinh_hoc: "Sinh học",
    lich_su: "Lịch sử",
    dia_li: "Địa lí",
    gdcd: "GDCD",
    ma_ngoai_ngu: "Mã ngoại ngữ",
  };
  return map[subject] || subject;
}

async function loadStats() {
  try {
    const res = await fetch(`${API_URL}/stats`);
    const data = await res.json();

    const container = document.getElementById("stats-result");
    container.innerHTML = "";

    for (const [subject, stats] of Object.entries(data)) {
      const card = document.createElement("div");

      if (subject === "ngoai_ngu") {
        card.innerHTML = `<h3>Ngoại ngữ (theo mã)</h3>`;
        for (const [code, subStats] of Object.entries(stats)) {
          card.innerHTML += `
            <p><b>Mã ${code}</b></p>
            <ul>
              <li>&gt;= 8: ${subStats[">=8"]}</li>
              <li>6 - 8: ${subStats["6-8"]}</li>
              <li>4 - 6: ${subStats["4-6"]}</li>
              <li>&lt; 4: ${subStats["<4"]}</li>
            </ul>
          `;
        }
      } else {
        card.innerHTML = `
          <h3>${getSubjectLabel(subject)}</h3>
          <ul>
            <li>&gt;= 8: ${stats[">=8"]}</li>
            <li>6 - 8: ${stats["6-8"]}</li>
            <li>4 - 6: ${stats["4-6"]}</li>
            <li>&lt; 4: ${stats["<4"]}</li>
          </ul>
        `;
      }

      container.appendChild(card);
    }
  } catch (err) {
    alert("Lỗi khi tải stats: " + err);
  }
}

async function loadTop10() {
  try {
    const res = await fetch(`${API_URL}/top10`);
    const data = await res.json();

    const tbody = document.querySelector("#top10-table tbody");
    tbody.innerHTML = "";

    data.forEach(student => {
      const total = (student.toan || 0) + (student.vat_li || 0) + (student.hoa_hoc || 0);
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${student.sbd}</td>
        <td>${student.toan ?? "-"}</td>
        <td>${student.vat_li ?? "-"}</td>
        <td>${student.hoa_hoc ?? "-"}</td>
        <td>${total}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    alert("Lỗi khi tải top10: " + err);
  }
}

async function lookupScore(sbd) {
  const resultBox = document.getElementById("lookup-result");
  resultBox.style.display = "block";
  resultBox.innerHTML = "⏳ Đang tra cứu...";

  try {
    const res = await fetch(`${API_URL}/score/${sbd}`);
    if (!res.ok) throw new Error("not found");
    const data = await res.json();

    let html = `<h3>Kết quả cho SBD: ${data.sbd}</h3><table class="styled-table"><tbody>`;
    for (const [subject, value] of Object.entries(data)) {
      if (subject !== "sbd") {
        html += `<tr><td>${getSubjectLabel(subject)}</td><td>${value ?? "-"}</td></tr>`;
      }
    }
    html += "</tbody></table>";

    resultBox.className = "result-box";
    resultBox.innerHTML = html;
  } catch (err) {
    resultBox.className = "result-box error";
    resultBox.innerHTML = "❌ Không tìm thấy SBD này!";
  }
}

// Gắn sự kiện
document.getElementById("lookup-form").addEventListener("submit", e => {
  e.preventDefault();
  const sbd = document.getElementById("sbd-input").value.trim();
  if (sbd) lookupScore(sbd);
});


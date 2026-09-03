async function submitComplaint() {
  const text = document.getElementById("complaintText").value.trim();
  if (!text) { alert("Please enter a complaint."); return; }

  const res = await fetch("/api/complaints", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  const resultDiv = document.getElementById("result");
  resultDiv.style.display = "block";

  if (!res.ok) {
    const err = await res.json();
    resultDiv.innerHTML = `<p style="color:#b8433a">${err.detail}</p>`;
    return;
  }

  const data = await res.json();
  resultDiv.innerHTML = `
    <div class="ticket-id">Complaint #${data.id}</div>
    <div class="ticket-row">
      <span><span class="label">Category</span>${data.category}</span>
      <span><span class="label">Priority</span><span class="pill ${data.priority}">${data.priority}</span></span>
      <span><span class="label">Status</span>${data.status}</span>
    </div>
  `;
  document.getElementById("complaintText").value = "";
}

async function loadComplaints() {
  const res = await fetch("/api/complaints");
  const complaints = await res.json();

  renderStats(complaints);

  const tbody = document.querySelector("#complaintsTable tbody");
  tbody.innerHTML = "";

  complaints.forEach(c => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${c.id}</td>
      <td>${c.complaint_text}</td>
      <td>${c.category}</td>
      <td><span class="pill ${c.priority}">${c.priority}</span></td>
      <td>
        <select onchange="changeStatus(${c.id}, this.value)">
          <option ${c.status === "Pending" ? "selected" : ""}>Pending</option>
          <option ${c.status === "In Progress" ? "selected" : ""}>In Progress</option>
          <option ${c.status === "Resolved" ? "selected" : ""}>Resolved</option>
        </select>
      </td>
      <td>${c.created_at}</td>
    `;
    tbody.appendChild(tr);
  });
}

function renderStats(complaints) {
  const counts = { Pending: 0, "In Progress": 0, Resolved: 0 };
  complaints.forEach(c => { if (counts[c.status] !== undefined) counts[c.status]++; });

  const statsDiv = document.getElementById("stats");
  statsDiv.innerHTML = Object.entries(counts).map(([label, count]) => `
    <div class="stat-card">
      <div class="count">${count}</div>
      <div class="stat-label">${label}</div>
    </div>
  `).join("");
}

async function changeStatus(id, status) {
  await fetch(`/api/complaints/${id}/status`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status })
  });
  loadComplaints();
}

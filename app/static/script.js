async function submitComplaint() {
  const text = document.getElementById("complaintText").value.trim();
  if (!text) { alert("Please enter a complaint."); return; }

  const res = await fetch("/api/complaints", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  const resultDiv = document.getElementById("result");
  if (!res.ok) {
    const err = await res.json();
    resultDiv.style.display = "block";
    resultDiv.innerHTML = `<p style="color:red">${err.detail}</p>`;
    return;
  }

  const data = await res.json();
  resultDiv.style.display = "block";
  resultDiv.innerHTML = `
    <p><strong>Complaint ID:</strong> ${data.id}</p>
    <p><strong>Category:</strong> ${data.category}</p>
    <p><strong>Priority:</strong> <span class="${data.priority}">${data.priority}</span></p>
    <p><strong>Status:</strong> ${data.status}</p>
  `;
  document.getElementById("complaintText").value = "";
}

async function loadComplaints() {
  const res = await fetch("/api/complaints");
  const complaints = await res.json();
  const tbody = document.querySelector("#complaintsTable tbody");
  tbody.innerHTML = "";

  complaints.forEach(c => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${c.id}</td>
      <td>${c.complaint_text}</td>
      <td>${c.category}</td>
      <td class="${c.priority}">${c.priority}</td>
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

async function changeStatus(id, status) {
  await fetch(`/api/complaints/${id}/status`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status })
  });
}

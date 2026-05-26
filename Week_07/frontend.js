// Example of Asynchronous Fetch and DOM Update

async function loadStudentData(studentId) {
    const statusEl = document.getElementById('status');
    const resultEl = document.getElementById('result');

    statusEl.textContent = "Loading...";

    try {
        // Fetching data from an API endpoint
        const response = await fetch(`/api/students/${studentId}`);
        
        if (!response.ok) throw new Error("Student not found");

        const student = await response.json();

        // Update the DOM with the received data
        resultEl.innerHTML = `
            <div class="card">
                <h3>${student.name}</h3>
                <p>Hostel: ${student.hostel}</p>
            </div>
        `;
        statusEl.textContent = "Data loaded successfully.";

    } catch (error) {
        statusEl.textContent = "Error: " + error.message;
        resultEl.innerHTML = "";
    }
}

// Usage: Call this function when a button is clicked
// loadStudentData(101);

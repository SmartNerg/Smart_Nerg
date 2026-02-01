// ===== Step Navigation =====
let currentStep = 1;
const totalSteps = document.querySelectorAll('.form-step').length;

function changeStep(direction) {
    const steps = document.querySelectorAll('.form-step');
    const progressSteps = document.querySelectorAll('.progress-step');

    // Hide current step
    steps[currentStep - 1].classList.remove('active');

    // Update step number
    currentStep += direction;

    if (currentStep < 1) currentStep = 1;
    if (currentStep > totalSteps) currentStep = totalSteps;

    // Show new step
    steps[currentStep - 1].classList.add('active');

    // Update progress circles
    progressSteps.forEach((step, index) => {
        if (index < currentStep) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    });

    // Toggle buttons
    document.getElementById('prevBtn').style.display = currentStep === 1 ? 'none' : 'inline-flex';
    document.getElementById('nextBtn').style.display = currentStep === totalSteps ? 'none' : 'inline-flex';
    document.getElementById('submitBtn').style.display = currentStep === totalSteps ? 'inline-flex' : 'none';
}

// ===== Add / Remove Rooms =====
function addRoom() {
    const container = document.getElementById('roomsContainer');
    const newRoom = document.createElement('div');
    newRoom.classList.add('room-input-group');
    newRoom.innerHTML = `
        <div class="input-group">
            <label class="input-label">Room Type</label>
            <input type="text" class="input-field room-type" required>
        </div>
        <div class="input-group">
            <label class="input-label">Number of Rooms</label>
            <input type="number" class="input-field room-count" min="1" required>
        </div>
        <button type="button" class="btn-remove" onclick="removeRoom(this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
        </button>
    `;
    container.appendChild(newRoom);
}

function removeRoom(button) {
    button.parentElement.remove();
}

// ===== Add / Remove Time Periods =====
function addPeriod() {
    const container = document.getElementById('periodsContainer');
    const newPeriod = document.createElement('div');
    newPeriod.classList.add('period-input-group');
    newPeriod.innerHTML = `
        <div class="input-group">
            <label class="input-label">Time Period</label>
            <input type="text" placeholder="Morning, Afternoon, Evening" class="input-field period-name" required>
        </div>
        <div class="input-group">
            <label class="input-label">Electricity Cost (₦/kWh)</label>
            <input type="number" class="input-field period-cost" min="0" step="0.01" required>
        </div>
        <div class="input-group">
            <label class="input-label">Available Power (kWh)</label>
            <input type="number" class="input-field period-power" min="0" step="0.01" required>
        </div>
        <button type="button" class="btn-remove" onclick="removePeriod(this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
        </button>
    `;
    container.appendChild(newPeriod);
}

function removePeriod(button) {
    button.parentElement.remove();
}

// ===== Optional: Submit Form =====
function submitForm() {
    // Optional: you can gather form data here
    window.location.href = "results.html";
}


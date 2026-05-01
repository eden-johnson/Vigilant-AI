// Core design tokens mapped to JS variables for logic
const COLORS = {
  primary: '#39FF14',
  warning: '#FFB300',
  critical: '#FF3B30'
};

// Elements
const fatigueGauge = document.getElementById('fatigueGaugeProgress');
const fatigueValueEl = document.getElementById('fatigueValue');
const fatigueLabelEl = document.getElementById('fatigueLabel');
const fatigueStatusDot = document.getElementById('fatigueStatusDot');

const attentionGauge = document.getElementById('attentionGaugeProgress');
const attentionValueEl = document.getElementById('attentionValue');

const sensitivitySlider = document.getElementById('sensitivitySlider');
const sensitivityValue = document.getElementById('sensitivityValue');

const testAlertBtn = document.getElementById('testAlertBtn');
const alertOverlay = document.getElementById('alertOverlay');
const dismissAlertBtn = document.getElementById('dismissAlertBtn');

const sensorFeed = document.getElementById('sensorFeed');

// Gauge Math (radius 70 => circumference = 2 * Math.PI * 70 ≈ 440)
const CIRCUMFERENCE = 440;

// Set initial gauge states
fatigueGauge.style.strokeDasharray = CIRCUMFERENCE;
attentionGauge.style.strokeDasharray = CIRCUMFERENCE;

function updateGauge(gaugeEl, value, isReversed = false) {
  // value is 0-100
  const progress = isReversed ? (100 - value) : value;
  const offset = CIRCUMFERENCE - (progress / 100) * CIRCUMFERENCE;
  gaugeEl.style.strokeDashoffset = offset;
}

function getFatigueColorAndLabel(value) {
  if (value <= 30) return { color: COLORS.primary, label: 'Optimal' };
  if (value <= 70) return { color: COLORS.warning, label: 'Caution' };
  return { color: COLORS.critical, label: 'Danger' };
}

function setFatigueLevel(value) {
  updateGauge(fatigueGauge, value);
  fatigueValueEl.textContent = `${value}%`;
  
  const { color, label } = getFatigueColorAndLabel(value);
  fatigueGauge.style.stroke = color;
  fatigueLabelEl.textContent = label;
  fatigueLabelEl.style.color = color;
  fatigueStatusDot.style.backgroundColor = color;
  fatigueStatusDot.style.boxShadow = `0 0 8px ${color}`;

  // Log to feed (throttled to avoid spam)
  const now = Date.now();
  if (!window.lastLogTime) window.lastLogTime = 0;
  if (!window.lastLoggedFatigue) window.lastLoggedFatigue = -1;
  
  if (Math.abs(value - window.lastLoggedFatigue) >= 5 || (now - window.lastLogTime > 2000)) {
    window.lastLoggedFatigue = value;
    window.lastLogTime = now;
    logToFeed(`> Fatigue index updated: ${value}% [${label.toUpperCase()}]`);
  }
}

function setAttentionLevel(value) {
  updateGauge(attentionGauge, value);
  attentionValueEl.textContent = `${value}%`;
}

function logToFeed(msg) {
  sensorFeed.innerHTML += `${msg}<br>`;
  sensorFeed.scrollTop = sensorFeed.scrollHeight;
}

// Clock
setInterval(() => {
  const now = new Date();
  document.getElementById('currentTime').textContent = now.toLocaleTimeString('en-US', { hour12: false });
}, 1000);

// Slider Interactivity
sensitivitySlider.addEventListener('input', (e) => {
  sensitivityValue.textContent = `${e.target.value}%`;
  // Update slider thumb visual logic if needed, but CSS handles it
});

let currentFatigue = 0;
let currentAttention = 100;

// Real-time telemetry from Python
window.updateTelemetry = function(ear, mar, status, alert_message, frame_b64) {
  if (frame_b64) {
    document.getElementById('videoFeed').src = "data:image/jpeg;base64," + frame_b64;
  }

  // 1. Calculate Target Fatigue
  // Map EAR from 0.28 (awake) to 0.20 (closed)
  let targetFatigue = 0;
  if (ear < 0.28) {
    targetFatigue = ((0.28 - ear) / 0.08) * 100;
  }
  targetFatigue = Math.max(0, Math.min(100, targetFatigue));

  // If system explicitly detects drowsy status, force fatigue high
  if (status === "DROWSY!") {
    targetFatigue = 100;
  } else if (status === "NO FACE") {
    targetFatigue = currentFatigue; // Pause fatigue index when no face detected
  }

  // 2. Smooth the Fatigue (prevent blink spikes)
  if (targetFatigue > currentFatigue) {
    // Increase slowly so a quick blink doesn't max it out
    currentFatigue += 2.0; 
  } else {
    // Decrease very slowly so fatigue persists a bit
    currentFatigue -= 0.5;
  }
  currentFatigue = Math.max(0, Math.min(100, currentFatigue));

  // 3. Calculate Target Attention
  let targetAttention = 100;
  if (status === "YAWNING!") {
    targetAttention = 20;
  } else if (currentFatigue > 50) {
    targetAttention = 100 - currentFatigue;
  }
  
  // 4. Smooth Attention
  if (targetAttention < currentAttention) {
    currentAttention -= 3.0; // Drop relatively fast
  } else {
    currentAttention += 1.0; // Recover slower
  }
  currentAttention = Math.max(0, Math.min(100, currentAttention));

  setFatigueLevel(Math.round(currentFatigue));
  setAttentionLevel(Math.round(currentAttention));

  // Handle alerts triggered by Python
  if (alert_message && !alertOverlay.classList.contains('active')) {
    triggerAlert();
    logToFeed(`<span style="color: ${COLORS.critical}">> [SYSTEM] ${alert_message}</span>`);
  }
};

// Alerts
function triggerAlert() {
  alertOverlay.classList.add('active');
  logToFeed(`<span style="color: ${COLORS.critical}">> CRITICAL ALERT TRIGGERED</span>`);
}

function dismissAlert() {
  alertOverlay.classList.remove('active');
  currentFatigue = 0; // Reset smoothed fatigue on awake
  setFatigueLevel(0);
  currentAttention = 100;
  setAttentionLevel(100);
  logToFeed(`> Driver acknowledged alert. System reset to optimal.`);
}

testAlertBtn.addEventListener('click', triggerAlert);
dismissAlertBtn.addEventListener('click', dismissAlert);

// Initial paint
setFatigueLevel(0);
setAttentionLevel(100);
logToFeed('> Telemetry stream connected.');

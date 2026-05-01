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

  // Log to feed
  if(Math.random() > 0.7) {
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

// Real-time telemetry from Python
window.updateTelemetry = function(ear, mar, status, alert_message) {
  // Convert EAR (threshold ~0.25) to a fatigue percentage
  // If EAR > 0.30, fatigue is 0. If EAR < 0.20, fatigue is 100
  let fatigue = 0;
  if (ear < 0.30) {
    fatigue = ((0.30 - ear) / 0.10) * 100;
  }
  fatigue = Math.max(0, Math.min(100, Math.round(fatigue)));

  // Convert MAR (threshold ~0.60) to a metric (optional, we can just use status)
  let attention = 100 - fatigue;
  if (mar > 0.60) {
    attention -= 20; // Yawning reduces attention
  }
  attention = Math.max(0, Math.min(100, Math.round(attention)));

  setFatigueLevel(fatigue);
  setAttentionLevel(attention);

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
  simFatigue = 0; // Reset fatigue on awake
  setFatigueLevel(0);
  simAttention = 100;
  setAttentionLevel(100);
  logToFeed(`> Driver acknowledged alert. System reset to optimal.`);
}

testAlertBtn.addEventListener('click', triggerAlert);
dismissAlertBtn.addEventListener('click', dismissAlert);

// Initial paint
setFatigueLevel(0);
setAttentionLevel(100);
logToFeed('> Telemetry stream connected.');

/**
 * Nuclear Blast Detection & Life-Saving Alert System Engine
 * Dynamic REST API Integration, Canvas Blast Visualizer, & Audio Siren Synthesizer
 */

// Application State
const state = {
  optical: 150000,
  emp: 25.0,
  seismic: 5.2,
  gamma: 120.0,
  yieldKt: 100.0,
  distanceKm: 10.0,
  location: "City Center Sector 4",
  autoSim: false,
  sirenMuted: false,
  apiOnline: false,
  lastAnalysis: null,
  autoSimInterval: null,
  shockwaveProgress: 0,
};

// DOM Element Selectors
const elements = {
  opticalInput: document.getElementById("opticalInput"),
  opticalVal: document.getElementById("opticalVal"),
  empInput: document.getElementById("empInput"),
  empVal: document.getElementById("empVal"),
  seismicInput: document.getElementById("seismicInput"),
  seismicVal: document.getElementById("seismicVal"),
  gammaInput: document.getElementById("gammaInput"),
  gammaVal: document.getElementById("gammaVal"),
  yieldInput: document.getElementById("yieldInput"),
  yieldVal: document.getElementById("yieldVal"),
  distanceInput: document.getElementById("distanceInput"),
  distanceVal: document.getElementById("distanceVal"),
  locationInput: document.getElementById("locationInput"),
  btnAnalyze: document.getElementById("btnAnalyzeTelemetry"),
  autoSimCheck: document.getElementById("autoSimCheck"),
  
  // Presets
  btnPresetNormal: document.getElementById("btnPresetNormal"),
  btnPresetSuspicious: document.getElementById("btnPresetSuspicious"),
  btnPresetCritical: document.getElementById("btnPresetCritical"),

  // Output Displays
  confidenceGauge: document.getElementById("confidenceGauge"),
  confidenceNum: document.getElementById("confidenceNum"),
  threatStatusText: document.getElementById("threatStatusText"),
  indicatorsList: document.getElementById("indicatorsList"),
  
  // Radar Legend Labels
  lblFireball: document.getElementById("lblFireball"),
  lblHeavy: document.getElementById("lblHeavy"),
  lblModerate: document.getElementById("lblModerate"),
  lblThermal: document.getElementById("lblThermal"),
  lblLight: document.getElementById("lblLight"),
  warningTimeNum: document.getElementById("warningTimeNum"),
  alertInstructionsText: document.getElementById("alertInstructionsText"),
  emergencyAlertBox: document.getElementById("emergencyAlertBox"),

  // Table & Stats
  eventsTableBody: document.getElementById("eventsTableBody"),
  btnRefreshLogs: document.getElementById("btnRefreshLogs"),
  btnClearLogs: document.getElementById("btnClearLogs"),
  btnExportCSV: document.getElementById("btnExportCSV"),
  statTotalEvents: document.getElementById("statTotalEvents"),
  statCriticalThreats: document.getElementById("statCriticalThreats"),
  statSuspiciousEvents: document.getElementById("statSuspiciousEvents"),
  statAvgConfidence: document.getElementById("statAvgConfidence"),

  // Header
  apiStatusBadge: document.getElementById("apiStatusBadge"),
  apiStatusText: document.getElementById("apiStatusText"),
  clockDisplay: document.getElementById("clockDisplay"),
  sirenMuteBtn: document.getElementById("sirenMuteBtn"),
  canvas: document.getElementById("blastCanvas"),
};

// Canvas 2D Context
const ctx = elements.canvas ? elements.canvas.getContext("2d") : null;

// Initialize Application
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
  startClock();
  checkApiHealth();
  triggerAnalysis();
  fetchEventsHistory();
  startCanvasAnimation();
});

// Clock UTC Display
function startClock() {
  setInterval(() => {
    const now = new Date();
    elements.clockDisplay.textContent = now.toUTCString().split(" ")[4] + " UTC";
  }, 1000);
}

// Setup Event Listeners
function setupEventListeners() {
  elements.opticalInput.addEventListener("input", (e) => {
    state.optical = parseFloat(e.target.value);
    elements.opticalVal.textContent = state.optical.toLocaleString() + " lux";
    triggerAnalysis();
  });

  elements.empInput.addEventListener("input", (e) => {
    state.emp = parseFloat(e.target.value);
    elements.empVal.textContent = state.emp.toFixed(1) + " kV/m";
    triggerAnalysis();
  });

  elements.seismicInput.addEventListener("input", (e) => {
    state.seismic = parseFloat(e.target.value);
    elements.seismicVal.textContent = state.seismic.toFixed(1) + " Richter";
    triggerAnalysis();
  });

  elements.gammaInput.addEventListener("input", (e) => {
    state.gamma = parseFloat(e.target.value);
    elements.gammaVal.textContent = state.gamma.toFixed(1) + " µSv/hr";
    triggerAnalysis();
  });

  elements.yieldInput.addEventListener("input", (e) => {
    state.yieldKt = parseFloat(e.target.value);
    elements.yieldVal.textContent = state.yieldKt.toLocaleString() + " KT";
    triggerAnalysis();
  });

  elements.distanceInput.addEventListener("input", (e) => {
    state.distanceKm = parseFloat(e.target.value);
    elements.distanceVal.textContent = state.distanceKm.toFixed(1) + " km";
    triggerAnalysis();
  });

  elements.locationInput.addEventListener("input", (e) => {
    state.location = e.target.value;
  });

  elements.btnAnalyze.addEventListener("click", () => {
    triggerAnalysis(true);
  });

  // Presets
  elements.btnPresetNormal.addEventListener("click", () => applyPreset(450, 0.2, 1.4, 0.15));
  elements.btnPresetSuspicious.addEventListener("click", () => applyPreset(120000, 12.5, 2.1, 1.2));
  elements.btnPresetCritical.addEventListener("click", () => applyPreset(150000, 25.0, 5.2, 120.0));

  // Auto Simulation Toggle
  elements.autoSimCheck.addEventListener("change", (e) => {
    state.autoSim = e.target.checked;
    if (state.autoSim) {
      state.autoSimInterval = setInterval(() => {
        const noise = (Math.random() - 0.5) * 2000;
        state.optical = Math.max(0, Math.min(250000, state.optical + noise));
        elements.opticalInput.value = state.optical;
        elements.opticalVal.textContent = Math.round(state.optical).toLocaleString() + " lux";
        triggerAnalysis();
      }, 1500);
    } else {
      clearInterval(state.autoSimInterval);
    }
  });

  // Siren Audio Toggle
  elements.sirenMuteBtn.addEventListener("click", () => {
    state.sirenMuted = !state.sirenMuted;
    elements.sirenMuteBtn.textContent = state.sirenMuted ? "🔇 Siren Sound: OFF" : "🔊 Siren Sound: ON";
  });

  // Table buttons
  elements.btnRefreshLogs.addEventListener("click", fetchEventsHistory);
  elements.btnClearLogs.addEventListener("click", clearDatabaseLogs);
  elements.btnExportCSV.addEventListener("click", exportTableToCSV);
}

function applyPreset(optical, emp, seismic, gamma) {
  state.optical = optical;
  state.emp = emp;
  state.seismic = seismic;
  state.gamma = gamma;

  elements.opticalInput.value = optical;
  elements.opticalVal.textContent = optical.toLocaleString() + " lux";
  elements.empInput.value = emp;
  elements.empVal.textContent = emp.toFixed(1) + " kV/m";
  elements.seismicInput.value = seismic;
  elements.seismicVal.textContent = seismic.toFixed(1) + " Richter";
  elements.gammaInput.value = gamma;
  elements.gammaVal.textContent = gamma.toFixed(1) + " µSv/hr";

  triggerAnalysis(true);
}

// API Health Check
async function checkApiHealth() {
  try {
    const res = await fetch("/api/health");
    if (res.ok) {
      state.apiOnline = true;
      elements.apiStatusBadge.style.color = "var(--accent-green)";
      elements.apiStatusText.textContent = "BACKEND ONLINE (200 OK)";
    } else {
      throw new Error();
    }
  } catch (err) {
    state.apiOnline = false;
    elements.apiStatusBadge.style.color = "var(--accent-amber)";
    elements.apiStatusText.textContent = "STANDALONE CLIENT MODE";
  }
}

// Core Analysis Engine
async function triggerAnalysis(forceSave = false) {
  const payload = {
    optical_lux: state.optical,
    emp_kvm: state.emp,
    seismic_magnitude: state.seismic,
    gamma_usv: state.gamma,
    yield_kt: state.yieldKt,
    distance_km: state.distanceKm,
    location: state.location,
  };

  let analysis = null;

  if (state.apiOnline && forceSave) {
    try {
      const res = await fetch("/api/telemetry/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        analysis = await res.json();
        fetchEventsHistory();
      }
    } catch (e) {
      console.warn("API Call failed, falling back to client logic", e);
    }
  }

  if (!analysis) {
    analysis = calculateClientSideAnalysis(payload);
  }

  state.lastAnalysis = analysis;
  renderAnalysisResults(analysis);
}

// In-Browser Client Fallback Physics Engine
function calculateClientSideAnalysis(p) {
  let score = 0;
  const reasons = [];

  if (p.optical_lux > 100000) { score += 30; reasons.push("Extreme optical flash spike detected (Double-pulse signature)"); }
  if (p.emp_kvm > 10.0) { score += 25; reasons.push("High-voltage Electromagnetic Pulse (EMP) burst detected"); }
  if (p.gamma_usv > 50.0) { score += 25; reasons.push("Severe Gamma radiation ionization spike detected"); }
  if (p.seismic_magnitude > 4.0) { score += 20; reasons.push("Shallow epicentral acoustic/seismic shockwave detected"); }

  let threatLevel = "NORMAL - NO NUCLEAR THREAT DETECTED";
  if (score >= 75) threatLevel = "CRITICAL - DETONATION CONFIRMED";
  else if (score >= 40) threatLevel = "WARNING - SUSPICIOUS EVENT";

  const scale = Math.pow(p.yield_kt, 1 / 3);
  const fireball = Math.round(0.07 * scale * 100) / 100;
  const heavy = Math.round(0.35 * scale * 100) / 100;
  const moderate = Math.round(0.85 * scale * 100) / 100;
  const thermal = Math.round(1.35 * scale * 100) / 100;
  const light = Math.round(2.20 * scale * 100) / 100;
  const warningTime = Math.round(Math.max(0, p.distance_km / 0.34) * 10) / 10;

  const impact = {
    yield_kt: p.yield_kt,
    distance_km: p.distance_km,
    fireball_km: fireball,
    heavy_damage_km: heavy,
    moderate_damage_km: moderate,
    thermal_burn_km: thermal,
    light_damage_km: light,
    warning_time_sec: warningTime,
  };

  let directives = [
    "Remain indoors and seal doors/windows against fallout dust.",
    "Tune into emergency communication broadcasts."
  ];

  if (p.distance_km <= fireball) {
    directives = [
      "GROUND ZERO DETONATION ZONE - IMMEDIATE VAPORIZATION RISK.",
      "If sheltered underground, remain stationary and protect head/airway.",
      "Do NOT look at flash. Seal eyes and face immediately."
    ];
  } else if (p.distance_km <= heavy) {
    directives = [
      "DO NOT LOOK AT THE FLASH. Close eyes and cover face immediately.",
      "Lie flat on the ground facing AWAY from blast center.",
      "Take immediate shelter inside underground basements or reinforced structures."
    ];
  } else if (p.distance_km <= light) {
    directives = [
      "Move away from all windows immediately to avoid shattered glass.",
      "Take cover behind solid walls or heavy furniture.",
      "Stay indoors to prevent fallout radiation exposure."
    ];
  }

  return {
    confidence_percentage: score,
    threat_level: threatLevel,
    detected_indicators: reasons,
    impact: impact,
    directives: directives,
  };
}

// Render Results on UI
function renderAnalysisResults(res) {
  elements.confidenceNum.textContent = res.confidence_percentage + "%";
  elements.threatStatusText.textContent = res.threat_level;

  if (res.confidence_percentage >= 75) {
    elements.confidenceGauge.style.borderColor = "var(--accent-red)";
    elements.threatStatusText.style.color = "var(--accent-red)";
    elements.emergencyAlertBox.className = "alert-box critical";
    playSirenSound();
  } else if (res.confidence_percentage >= 40) {
    elements.confidenceGauge.style.borderColor = "var(--accent-amber)";
    elements.threatStatusText.style.color = "var(--accent-amber)";
    elements.emergencyAlertBox.className = "alert-box warning";
  } else {
    elements.confidenceGauge.style.borderColor = "var(--accent-green)";
    elements.threatStatusText.style.color = "var(--accent-green)";
    elements.emergencyAlertBox.className = "alert-box normal";
  }

  // Render Indicators
  elements.indicatorsList.innerHTML = "";
  if (res.detected_indicators.length === 0) {
    elements.indicatorsList.innerHTML = "<li>No abnormal nuclear signatures detected. System baseline stable.</li>";
  } else {
    res.detected_indicators.forEach((ind) => {
      const li = document.createElement("li");
      li.textContent = ind;
      elements.indicatorsList.appendChild(li);
    });
  }

  // Render Radii Labels
  if (res.impact) {
    elements.lblFireball.textContent = res.impact.fireball_km + " km";
    elements.lblHeavy.textContent = res.impact.heavy_damage_km + " km";
    elements.lblModerate.textContent = res.impact.moderate_damage_km + " km";
    elements.lblThermal.textContent = res.impact.thermal_burn_km + " km";
    elements.lblLight.textContent = res.impact.light_damage_km + " km";
    elements.warningTimeNum.textContent = res.impact.warning_time_sec + "s";
  }

  // Render Directives
  if (res.directives) {
    elements.alertInstructionsText.innerHTML = res.directives.map((d, i) => `<p>${i + 1}. ${d}</p>`).join("");
  }
}

// Web Audio API Emergency Alarm Siren Synthesizer
let audioCtx = null;
function playSirenSound() {
  if (state.sirenMuted) return;
  try {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = "sawtooth";
    osc.frequency.setValueAtTime(440, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.5);
    gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.5);
  } catch (e) {
    // Silent fail if audio autoplay restricted
  }
}

// 2D Canvas Blast Radar Animation Renderer
function startCanvasAnimation() {
  if (!ctx) return;

  function drawRadar() {
    const width = elements.canvas.width;
    const height = elements.canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;

    ctx.clearRect(0, 0, width, height);

    // Background Grid
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(centerX, centerY, 40, 0, Math.PI * 2);
    ctx.arc(centerX, centerY, 80, 0, Math.PI * 2);
    ctx.arc(centerX, centerY, 120, 0, Math.PI * 2);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(centerX, 0); ctx.lineTo(centerX, height);
    ctx.moveTo(0, centerY); ctx.lineTo(width, centerY);
    ctx.stroke();

    if (state.lastAnalysis && state.lastAnalysis.impact) {
      const imp = state.lastAnalysis.impact;
      const maxRadiusKm = Math.max(imp.light_damage_km, 1.0);
      const scalePixelPerKm = 120 / maxRadiusKm;

      // Draw Blast Rings
      const rings = [
        { radius: imp.light_damage_km, color: "rgba(0, 255, 102, 0.25)" },
        { radius: imp.thermal_burn_km, color: "rgba(0, 204, 255, 0.35)" },
        { radius: imp.moderate_damage_km, color: "rgba(255, 204, 0, 0.45)" },
        { radius: imp.heavy_damage_km, color: "rgba(255, 102, 0, 0.6)" },
        { radius: imp.fireball_km, color: "rgba(255, 0, 0, 0.85)" },
      ];

      rings.forEach((r) => {
        ctx.fillStyle = r.color;
        ctx.beginPath();
        ctx.arc(centerX, centerY, r.radius * scalePixelPerKm, 0, Math.PI * 2);
        ctx.fill();
      });

      // Animated Expanding Shockwave Ring
      state.shockwaveProgress = (state.shockwaveProgress + 1.5) % 130;
      ctx.strokeStyle = "rgba(255, 255, 255, 0.8)";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(centerX, centerY, state.shockwaveProgress, 0, Math.PI * 2);
      ctx.stroke();

      // Draw Epicenter Dot
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(centerX, centerY, 4, 0, Math.PI * 2);
      ctx.fill();
    }

    requestAnimationFrame(drawRadar);
  }

  requestAnimationFrame(drawRadar);
}

// Fetch SQLite Events Log
async function fetchEventsHistory() {
  if (!state.apiOnline) return;

  try {
    const res = await fetch("/api/events?limit=25");
    if (res.ok) {
      const events = await res.json();
      renderEventsTable(events);
      fetchStats();
    }
  } catch (e) {
    console.warn("Failed to fetch SQLite events", e);
  }
}

// Render SQLite Table
function renderEventsTable(events) {
  elements.eventsTableBody.innerHTML = "";
  if (events.length === 0) {
    elements.eventsTableBody.innerHTML = "<tr><td colspan='12' style='text-align:center;'>No historical detection events logged in database.</td></tr>";
    return;
  }

  events.forEach((ev) => {
    const tr = document.createElement("tr");
    const threatClass = ev.confidence_percentage >= 75 ? "critical" : ev.confidence_percentage >= 40 ? "warning" : "normal";
    tr.innerHTML = `
      <td>#${ev.id}</td>
      <td>${ev.timestamp}</td>
      <td>${ev.location}</td>
      <td><span class="legend-item ${threatClass}">${ev.threat_level}</span></td>
      <td><b>${ev.confidence_percentage}%</b></td>
      <td>${ev.yield_kt} KT</td>
      <td>${ev.distance_km} km</td>
      <td>${ev.warning_time_sec}s</td>
      <td>${ev.optical_lux.toLocaleString()} lux</td>
      <td>${ev.emp_kvm} kV/m</td>
      <td>${ev.seismic_magnitude}</td>
      <td>${ev.gamma_usv} µSv</td>
    `;
    elements.eventsTableBody.appendChild(tr);
  });
}

// Fetch Stats
async function fetchStats() {
  if (!state.apiOnline) return;
  try {
    const res = await fetch("/api/stats");
    if (res.ok) {
      const s = await res.json();
      elements.statTotalEvents.textContent = s.total_events;
      elements.statCriticalThreats.textContent = s.critical_threats;
      elements.statSuspiciousEvents.textContent = s.suspicious_events;
      elements.statAvgConfidence.textContent = s.average_confidence + "%";
    }
  } catch (e) {}
}

// Clear Database Logs
async function clearDatabaseLogs() {
  if (!confirm("Are you sure you want to clear all historical detection records from SQLite database?")) return;
  if (state.apiOnline) {
    await fetch("/api/events", { method: "DELETE" });
    fetchEventsHistory();
  }
}

// Export CSV
function exportTableToCSV() {
  const rows = [["ID", "Timestamp", "Location", "Threat Level", "Confidence", "Yield KT", "Distance KM", "Warning Sec"]];
  const trs = elements.eventsTableBody.querySelectorAll("tr");
  trs.forEach((tr) => {
    const tds = tr.querySelectorAll("td");
    if (tds.length >= 8) {
      const row = Array.from(tds).map((td) => `"${td.textContent.trim()}"`);
      rows.push(row);
    }
  });

  const csvContent = "data:text/csv;charset=utf-8," + rows.map((e) => e.join(",")).join("\n");
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "nuclear_detonation_events_log.csv");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

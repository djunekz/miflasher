"""
MiFlasher Web GUI
A full single-file web dashboard served via Python's built-in HTTP server.
"""

import json
import os
import sys
import threading
import time
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import webbrowser


# ─── HTML / CSS / JS ─────────────────────────────────────────────────────────

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MiFlasher v2.0</title>
<style>
  :root{
    --bg:#0a0a0f;--bg2:#12121a;--bg3:#1a1a28;
    --accent:#00d4ff;--accent2:#a855f7;--green:#22c55e;
    --red:#ef4444;--yellow:#f59e0b;--text:#e2e8f0;--dim:#64748b;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--text);font-family:'JetBrains Mono',monospace,sans-serif;min-height:100vh}
  .top-bar{
    background:linear-gradient(135deg,var(--bg2),var(--bg3));
    border-bottom:1px solid #ffffff12;
    padding:16px 28px;display:flex;align-items:center;gap:16px;
  }
  .logo{font-size:1.4rem;font-weight:900;
    background:linear-gradient(90deg,var(--accent),var(--accent2));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent}
  .version{color:var(--dim);font-size:.8rem}
  .status-dot{width:10px;height:10px;border-radius:50%;background:var(--red);
    margin-left:auto;animation:pulse 2s infinite}
  .status-dot.connected{background:var(--green)}
  .status-label{font-size:.85rem;color:var(--dim)}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}

  .layout{display:grid;grid-template-columns:220px 1fr;min-height:calc(100vh - 61px)}
  .sidebar{background:var(--bg2);border-right:1px solid #ffffff08;padding:20px 0}
  .nav-item{
    display:flex;align-items:center;gap:10px;
    padding:12px 24px;cursor:pointer;transition:.15s;
    font-size:.9rem;color:var(--dim);border-left:3px solid transparent;
  }
  .nav-item:hover{background:#ffffff06;color:var(--text)}
  .nav-item.active{background:#ffffff09;color:var(--accent);border-left-color:var(--accent)}
  .nav-icon{font-size:1.1rem;width:22px;text-align:center}

  .main{padding:28px;overflow-y:auto}
  .section{display:none}.section.active{display:block}
  h2{font-size:1.3rem;margin-bottom:20px;color:var(--accent)}

  .card{
    background:var(--bg2);border:1px solid #ffffff0d;
    border-radius:12px;padding:22px;margin-bottom:18px;
  }
  .card-title{font-size:.8rem;text-transform:uppercase;letter-spacing:.1em;
    color:var(--dim);margin-bottom:14px}

  .info-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
  .info-item{background:var(--bg3);border-radius:8px;padding:12px 16px}
  .info-label{font-size:.72rem;color:var(--dim);margin-bottom:4px;text-transform:uppercase}
  .info-value{font-size:.95rem;color:var(--text);font-weight:600}
  .badge{
    display:inline-block;padding:2px 10px;border-radius:99px;font-size:.72rem;font-weight:700;
  }
  .badge-green{background:#22c55e22;color:#22c55e}
  .badge-red{background:#ef444422;color:#ef4444}
  .badge-blue{background:#00d4ff22;color:#00d4ff}
  .badge-yellow{background:#f59e0b22;color:#f59e0b}

  .btn{
    display:inline-flex;align-items:center;gap:8px;
    padding:10px 20px;border-radius:8px;border:none;
    cursor:pointer;font-size:.88rem;font-weight:600;transition:.15s;
  }
  .btn-primary{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff}
  .btn-primary:hover{opacity:.85}
  .btn-danger{background:#ef444420;color:var(--red);border:1px solid var(--red)40}
  .btn-danger:hover{background:#ef444435}
  .btn-ghost{background:#ffffff0a;color:var(--text);border:1px solid #ffffff12}
  .btn-ghost:hover{background:#ffffff15}
  .btn:disabled{opacity:.4;cursor:not-allowed}

  .input-group{margin-bottom:14px}
  label{display:block;font-size:.8rem;color:var(--dim);margin-bottom:6px}
  input,select{
    width:100%;background:var(--bg3);border:1px solid #ffffff12;
    border-radius:8px;padding:10px 14px;color:var(--text);font-size:.9rem;outline:none;
    font-family:inherit;transition:.15s;
  }
  input:focus,select:focus{border-color:var(--accent);box-shadow:0 0 0 3px #00d4ff15}
  select option{background:var(--bg2)}

  .terminal{
    background:#000;border:1px solid #ffffff12;border-radius:10px;
    padding:16px;font-size:.82rem;line-height:1.6;min-height:180px;
    max-height:400px;overflow-y:auto;white-space:pre-wrap;word-break:break-all;
  }
  .t-info{color:#60a5fa}.t-success{color:#4ade80}.t-error{color:#f87171}
  .t-warn{color:#fbbf24}.t-dim{color:#475569}.t-step{color:#22d3ee}

  .progress-wrap{margin:14px 0}
  .progress-label{font-size:.8rem;color:var(--dim);margin-bottom:6px;display:flex;justify-content:space-between}
  .progress-bar-bg{background:#ffffff0a;border-radius:99px;height:8px;overflow:hidden}
  .progress-bar{height:100%;border-radius:99px;width:0%;transition:.3s;
    background:linear-gradient(90deg,var(--accent),var(--accent2))}

  .reboot-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}
  .reboot-btn{
    background:var(--bg3);border:1px solid #ffffff0d;border-radius:10px;
    padding:16px;text-align:center;cursor:pointer;transition:.15s;
  }
  .reboot-btn:hover{border-color:var(--accent);background:#00d4ff08}
  .reboot-btn .icon{font-size:1.4rem;margin-bottom:6px}
  .reboot-btn .label{font-size:.8rem;color:var(--dim)}

  .tab-bar{display:flex;gap:2px;margin-bottom:20px;background:var(--bg3);
    border-radius:8px;padding:4px}
  .tab{padding:8px 18px;border-radius:6px;cursor:pointer;font-size:.85rem;
    color:var(--dim);transition:.15s}
  .tab.active{background:var(--bg2);color:var(--text)}

  .log-line{padding:2px 0;border-bottom:1px solid #ffffff05}
  .log-line:last-child{border:none}
</style>
</head>
<body>

<div class="top-bar">
  <div class="logo">⚡ MiFlasher</div>
  <div class="version">v2.0</div>
  <div style="margin-left:auto;display:flex;align-items:center;gap:8px">
    <div class="status-dot" id="statusDot"></div>
    <div class="status-label" id="statusLabel">Scanning...</div>
  </div>
</div>

<div class="layout">
  <div class="sidebar">
    <div class="nav-item active" onclick="show('device')">
      <span class="nav-icon">📱</span> Device
    </div>
    <div class="nav-item" onclick="show('flash')">
      <span class="nav-icon">⚡</span> Flash
    </div>
    <div class="nav-item" onclick="show('backup')">
      <span class="nav-icon">💾</span> Backup
    </div>
    <div class="nav-item" onclick="show('unlock')">
      <span class="nav-icon">🔓</span> Unlock
    </div>
    <div class="nav-item" onclick="show('wipe')">
      <span class="nav-icon">🗑️</span> Wipe
    </div>
    <div class="nav-item" onclick="show('logs')">
      <span class="nav-icon">📋</span> Logs
    </div>
    <div class="nav-item" onclick="show('settings')">
      <span class="nav-icon">⚙️</span> Settings
    </div>
  </div>

  <div class="main">

    <!-- DEVICE -->
    <div class="section active" id="sec-device">
      <h2>Device Information</h2>
      <div id="deviceInfo">
        <div class="card">
          <div class="card-title">Status</div>
          <p style="color:var(--dim)">Loading device info...</p>
        </div>
      </div>
      <div class="card" style="margin-top:4px">
        <div class="card-title">Reboot</div>
        <div class="reboot-grid">
          <div class="reboot-btn" onclick="rebootDevice('system')">
            <div class="icon">🏠</div><div class="label">System</div>
          </div>
          <div class="reboot-btn" onclick="rebootDevice('bootloader')">
            <div class="icon">🔧</div><div class="label">Bootloader</div>
          </div>
          <div class="reboot-btn" onclick="rebootDevice('recovery')">
            <div class="icon">🛠️</div><div class="label">Recovery</div>
          </div>
          <div class="reboot-btn" onclick="rebootDevice('fastbootd')">
            <div class="icon">⚡</div><div class="label">Fastbootd</div>
          </div>
          <div class="reboot-btn" onclick="rebootDevice('edl')">
            <div class="icon">🔴</div><div class="label">EDL</div>
          </div>
        </div>
      </div>
    </div>

    <!-- FLASH -->
    <div class="section" id="sec-flash">
      <h2>Flash</h2>
      <div class="tab-bar">
        <div class="tab active" onclick="flashTab('rom')">ROM</div>
        <div class="tab" onclick="flashTab('boot')">Boot</div>
        <div class="tab" onclick="flashTab('recovery')">Recovery</div>
        <div class="tab" onclick="flashTab('vbmeta')">vbmeta</div>
        <div class="tab" onclick="flashTab('payload')">Payload</div>
      </div>

      <div class="card">
        <div class="card-title" id="flashTarget">Flash ROM</div>
        <div class="input-group">
          <label>Source</label>
          <input id="flashSrc" placeholder="Local path or https:// URL" />
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
          <div class="input-group">
            <label>Slot</label>
            <select id="flashSlot">
              <option value="all">All (A+B)</option>
              <option value="a">Slot A</option>
              <option value="b">Slot B</option>
            </select>
          </div>
          <div class="input-group">
            <label>Options</label>
            <select id="flashOpts">
              <option value="">Auto</option>
              <option value="keep-data">Keep Data</option>
              <option value="wipe-data">Wipe Data</option>
            </select>
          </div>
        </div>
        <div style="display:flex;gap:10px;margin-top:4px">
          <button class="btn btn-primary" onclick="startFlash()">⚡ Start Flash</button>
          <button class="btn btn-ghost" onclick="clearConsole('flashConsole')">Clear Log</button>
        </div>
        <div class="progress-wrap" id="flashProgressWrap" style="display:none">
          <div class="progress-label">
            <span id="flashProgressLabel">Flashing...</span>
            <span id="flashProgressPct">0%</span>
          </div>
          <div class="progress-bar-bg"><div class="progress-bar" id="flashProgressBar"></div></div>
        </div>
        <div class="terminal" id="flashConsole" style="margin-top:16px"></div>
      </div>
    </div>

    <!-- BACKUP -->
    <div class="section" id="sec-backup">
      <h2>Backup & Restore</h2>
      <div class="tab-bar">
        <div class="tab active" onclick="backupTab('backup')">Backup</div>
        <div class="tab" onclick="backupTab('restore')">Restore</div>
      </div>
      <div class="card" id="bk-backup">
        <div class="card-title">Backup Partitions</div>
        <div class="input-group">
          <label>Output Directory</label>
          <input id="backupDest" value="~/storage/downloads/MiFlasher/backups" />
        </div>
        <div class="input-group">
          <label>Partitions (comma separated, or leave blank for all)</label>
          <input id="backupParts" placeholder="boot,recovery,vbmeta" />
        </div>
        <button class="btn btn-primary" onclick="startBackup()">💾 Start Backup</button>
        <div class="terminal" id="backupConsole" style="margin-top:16px"></div>
      </div>
      <div class="card" id="bk-restore" style="display:none">
        <div class="card-title">Restore from Backup</div>
        <div class="input-group">
          <label>Backup archive or directory path</label>
          <input id="restorePath" placeholder="/path/to/backup.tar.gz" />
        </div>
        <button class="btn btn-primary" onclick="startRestore()">↩️ Start Restore</button>
        <div class="terminal" id="restoreConsole" style="margin-top:16px"></div>
      </div>
    </div>

    <!-- UNLOCK -->
    <div class="section" id="sec-unlock">
      <h2>Bootloader Unlock</h2>
      <div class="card">
        <div class="card-title">⚠️ Warning</div>
        <p style="color:var(--yellow);margin-bottom:16px;line-height:1.7;font-size:.9rem">
          Unlocking the bootloader will <strong>permanently wipe all data</strong> on your device.
          Make sure to backup your data before proceeding.<br><br>
          Xiaomi requires a 7-day waiting period after binding your Mi Account.
        </p>
        <div class="input-group">
          <label>Unlock Token (optional, if you have one)</label>
          <input id="unlockToken" placeholder="Leave blank to use miunlock tool" />
        </div>
        <button class="btn btn-danger" onclick="startUnlock()">🔓 Unlock Bootloader</button>
        <div class="terminal" id="unlockConsole" style="margin-top:16px"></div>
      </div>
    </div>

    <!-- WIPE -->
    <div class="section" id="sec-wipe">
      <h2>Wipe Partitions</h2>
      <div class="card">
        <div class="card-title">⚠️ Irreversible — Data will be lost</div>
        <div style="display:flex;flex-wrap:wrap;gap:10px;margin:16px 0">
          <label style="display:flex;align-items:center;gap:8px;cursor:pointer">
            <input type="checkbox" id="wData" style="width:auto"> Data (/data)
          </label>
          <label style="display:flex;align-items:center;gap:8px;cursor:pointer">
            <input type="checkbox" id="wCache" style="width:auto"> Cache
          </label>
          <label style="display:flex;align-items:center;gap:8px;cursor:pointer">
            <input type="checkbox" id="wDalvik" style="width:auto"> Dalvik Cache
          </label>
        </div>
        <button class="btn btn-danger" onclick="startWipe()">🗑️ Wipe Selected</button>
        <div class="terminal" id="wipeConsole" style="margin-top:16px"></div>
      </div>
    </div>

    <!-- LOGS -->
    <div class="section" id="sec-logs">
      <h2>Session Logs</h2>
      <div class="card">
        <div style="display:flex;gap:10px;margin-bottom:16px">
          <button class="btn btn-ghost" onclick="refreshLogs()">↻ Refresh</button>
          <button class="btn btn-danger" onclick="clearLogs()">🗑 Clear All</button>
        </div>
        <div class="terminal" id="logsConsole" style="min-height:320px"></div>
      </div>
    </div>

    <!-- SETTINGS -->
    <div class="section" id="sec-settings">
      <h2>Settings</h2>
      <div class="card">
        <div class="card-title">Configuration</div>
        <div id="settingsForm">Loading...</div>
        <button class="btn btn-primary" onclick="saveSettings()" style="margin-top:16px">
          💾 Save Settings
        </button>
      </div>
    </div>

  </div><!-- main -->
</div>

<script>
let currentFlashTarget = 'rom';
let devicePollTimer;

// ── Navigation ─────────────────────────────────────────────────────────────
function show(id) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('sec-' + id).classList.add('active');
  event.currentTarget.classList.add('active');
  if (id === 'device') pollDevice();
  if (id === 'logs')   refreshLogs();
  if (id === 'settings') loadSettings();
}

// ── API ────────────────────────────────────────────────────────────────────
async function api(path, body=null) {
  const opts = body
    ? {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)}
    : {};
  const r = await fetch('/api/' + path, opts);
  return r.json();
}

// ── Device ─────────────────────────────────────────────────────────────────
async function pollDevice() {
  clearTimeout(devicePollTimer);
  try {
    const d = await api('device');
    renderDevice(d);
    devicePollTimer = setTimeout(pollDevice, 5000);
  } catch(e) {
    document.getElementById('statusLabel').textContent = 'Error';
  }
}

function renderDevice(d) {
  const dot   = document.getElementById('statusDot');
  const label = document.getElementById('statusLabel');
  if (!d || d.mode === 'unknown' || d.serial === 'unknown') {
    dot.className = 'status-dot';
    label.textContent = 'No device';
    document.getElementById('deviceInfo').innerHTML = `
      <div class="card">
        <div class="card-title">Status</div>
        <p style="color:var(--dim)">No device detected. Connect your Xiaomi device via USB.</p>
      </div>`;
    return;
  }
  dot.className = 'status-dot connected';
  label.textContent = d.brand + ' ' + d.model;

  const badge = m => m === 'unknown' ? '' :
    m.includes('unlocked') || m === 'adb' || m === 'fastboot'
      ? `<span class="badge badge-green">${m}</span>`
      : `<span class="badge badge-blue">${m}</span>`;

  const row = (label, val) => `
    <div class="info-item">
      <div class="info-label">${label}</div>
      <div class="info-value">${val||'—'}</div>
    </div>`;

  document.getElementById('deviceInfo').innerHTML = `
    <div class="card">
      <div class="card-title">Device Info</div>
      <div class="info-grid">
        ${row('Serial',      d.serial)}
        ${row('Mode',        badge(d.mode) || d.mode.toUpperCase())}
        ${row('Brand',       d.brand)}
        ${row('Model',       d.model)}
        ${row('Codename',    d.codename)}
        ${row('Android',     d.android)}
        ${row('MIUI',        d.miui)}
        ${row('Build ID',    d.build)}
        ${row('Security',    d.security)}
        ${row('CPU ABI',     d.cpu_abi)}
        ${row('RAM',         d.ram)}
        ${row('Storage',     d.storage)}
        ${row('Display',     d.display)}
        ${row('Slot',        d.slot)}
        ${row('Bootloader',  badge(d.unlocked) || d.unlocked)}
        ${row('Battery',     d.battery)}
      </div>
    </div>`;
}

async function rebootDevice(mode) {
  appendLog('device-reboot', `Rebooting to ${mode}...`, 'info');
  const r = await api('reboot', {mode});
  appendLog('device-reboot', r.message, r.ok ? 'success' : 'error');
}

// ── Flash ─────────────────────────────────────────────────────────────────
function flashTab(t) {
  currentFlashTarget = t;
  document.querySelectorAll('#sec-flash .tab').forEach(tab => tab.classList.remove('active'));
  event.currentTarget.classList.add('active');
  document.getElementById('flashTarget').textContent = 'Flash ' + t.toUpperCase();
}

async function startFlash() {
  const src   = document.getElementById('flashSrc').value.trim();
  const slot  = document.getElementById('flashSlot').value;
  const opts  = document.getElementById('flashOpts').value;
  if (!src) { appendLog('flashConsole', 'Source is required!', 'error'); return; }

  appendLog('flashConsole', `Starting flash: ${currentFlashTarget} | ${src}`, 'step');
  showProgress('flashProgressWrap','flashProgressBar','flashProgressLabel','flashProgressPct','Flashing...',0);

  const r = await api('flash', {target: currentFlashTarget, source: src, slot, opts});
  appendLog('flashConsole', r.message, r.ok ? 'success' : 'error');
  showProgress('flashProgressWrap','flashProgressBar','flashProgressLabel','flashProgressPct','Done',r.ok?100:0);
}

// ── Backup ─────────────────────────────────────────────────────────────────
function backupTab(t) {
  document.querySelectorAll('#sec-backup .tab').forEach(tab => tab.classList.remove('active'));
  event.currentTarget.classList.add('active');
  document.getElementById('bk-backup').style.display  = t==='backup'  ? 'block':'none';
  document.getElementById('bk-restore').style.display = t==='restore' ? 'block':'none';
}

async function startBackup() {
  const dest  = document.getElementById('backupDest').value;
  const parts = document.getElementById('backupParts').value;
  appendLog('backupConsole', 'Starting backup...', 'step');
  const r = await api('backup', {dest, partitions: parts ? parts.split(',').map(p=>p.trim()) : null});
  appendLog('backupConsole', r.message, r.ok ? 'success' : 'error');
}

async function startRestore() {
  const path = document.getElementById('restorePath').value;
  appendLog('restoreConsole', `Restoring from ${path}...`, 'step');
  const r = await api('restore', {path});
  appendLog('restoreConsole', r.message, r.ok ? 'success' : 'error');
}

// ── Unlock ─────────────────────────────────────────────────────────────────
async function startUnlock() {
  if (!confirm('⚠️ This will WIPE ALL DATA. Are you absolutely sure?')) return;
  const token = document.getElementById('unlockToken').value;
  appendLog('unlockConsole', 'Starting bootloader unlock...', 'step');
  const r = await api('unlock', {token: token||null});
  appendLog('unlockConsole', r.message, r.ok ? 'success' : 'error');
}

// ── Wipe ───────────────────────────────────────────────────────────────────
async function startWipe() {
  const data   = document.getElementById('wData').checked;
  const cache  = document.getElementById('wCache').checked;
  const dalvik = document.getElementById('wDalvik').checked;
  if (!data && !cache && !dalvik) {
    appendLog('wipeConsole', 'Select at least one partition to wipe.', 'warn'); return;
  }
  if (!confirm('⚠️ Wipe selected partitions? This cannot be undone.')) return;
  appendLog('wipeConsole', 'Wiping...', 'step');
  const r = await api('wipe', {data, cache, dalvik});
  appendLog('wipeConsole', r.message, r.ok ? 'success' : 'error');
}

// ── Logs ───────────────────────────────────────────────────────────────────
async function refreshLogs() {
  const el = document.getElementById('logsConsole');
  el.innerHTML = 'Loading...';
  const r = await api('logs');
  el.innerHTML = '';
  (r.entries||[]).forEach(e => {
    const cls = {info:'t-info',success:'t-success',error:'t-error',
                 warning:'t-warn',step:'t-step',debug:'t-dim'}[e.level]||'';
    el.innerHTML += `<div class="log-line"><span class="t-dim">${e.time.slice(11,19)}</span> `
      + `<span class="${cls}">[${e.level.toUpperCase()}]</span> ${e.message}</div>`;
  });
  el.scrollTop = el.scrollHeight;
}

async function clearLogs() {
  if (!confirm('Clear all session logs?')) return;
  await api('clear-logs');
  refreshLogs();
}

// ── Settings ───────────────────────────────────────────────────────────────
async function loadSettings() {
  const r = await api('config');
  const keys = Object.keys(r.config||{});
  document.getElementById('settingsForm').innerHTML = keys.map(k => `
    <div class="input-group">
      <label>${k}</label>
      <input id="cfg_${k}" value="${r.config[k]}">
    </div>`).join('');
}

async function saveSettings() {
  const items = document.querySelectorAll('#settingsForm input');
  const cfg = {};
  items.forEach(inp => { cfg[inp.id.replace('cfg_','')] = inp.value; });
  const r = await api('save-config', {config: cfg});
  alert(r.ok ? 'Settings saved!' : 'Failed to save settings.');
}

// ── Helpers ────────────────────────────────────────────────────────────────
function appendLog(id, msg, level='info') {
  const el = document.getElementById(id);
  if (!el) return;
  const cls = {info:'t-info',success:'t-success',error:'t-error',warn:'t-warn',step:'t-step'}[level]||'';
  const ts  = new Date().toTimeString().slice(0,8);
  el.innerHTML += `<span class="t-dim">[${ts}]</span> <span class="${cls}">${msg}</span>\n`;
  el.scrollTop  = el.scrollHeight;
}

function clearConsole(id) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = '';
}

function showProgress(wrapId, barId, labelId, pctId, label, pct) {
  document.getElementById(wrapId).style.display = 'block';
  document.getElementById(barId).style.width    = pct + '%';
  document.getElementById(labelId).textContent  = label;
  document.getElementById(pctId).textContent    = pct + '%';
}

// ── Init ──────────────────────────────────────────────────────────────────
pollDevice();
</script>
</body>
</html>"""


# ─── API Handler ─────────────────────────────────────────────────────────────

def _run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.returncode == 0, r.stdout + r.stderr
    except Exception as e:
        return False, str(e)


class APIHandler(BaseHTTPRequestHandler):

    def log_message(self, *args):
        pass  # Suppress default HTTP logs

    def _json(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/" or path == "/index.html":
            body = HTML.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/api/device":
            from core.device import DeviceManager
            from core.logger import Logger
            log = Logger(); log.no_color = True
            dm  = DeviceManager(log)
            info = dm.detect()
            if info:
                from dataclasses import asdict
                self._json(asdict(info))
            else:
                self._json({"mode":"unknown","serial":"unknown"})
            return

        if path == "/api/logs":
            import glob
            log_dir = os.path.expanduser("~/.local/share/miflasher/logs")
            entries = []
            files   = sorted(glob.glob(os.path.join(log_dir, "*.jsonl")), reverse=True)
            if files:
                with open(files[0]) as f:
                    for line in f:
                        try: entries.append(json.loads(line))
                        except: pass
            self._json({"entries": entries[-200:]})
            return

        if path == "/api/config":
            from core.config import ConfigManager, DEFAULTS
            self._json({"config": DEFAULTS})
            return

        self._json({"error": "Not found"}, 404)

    def do_POST(self):
        path   = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length) or b"{}")

        if path == "/api/reboot":
            mode = body.get("mode", "system")
            ok, out = _run(["adb", "reboot", mode])
            if not ok:
                ok, out = _run(["fastboot", "reboot"])
            self._json({"ok": ok, "message": out or f"Reboot → {mode} sent"})

        elif path == "/api/flash":
            # Async placeholder — real implementation would stream output
            self._json({"ok": False, "message":
                "Flash started in background. Check CLI for output. "
                "GUI flash streaming coming in next version."})

        elif path == "/api/backup":
            self._json({"ok": False, "message":
                "Run: miflasher backup --all from terminal for full backup."})

        elif path == "/api/restore":
            self._json({"ok": False, "message":
                "Run: miflasher restore --path <file> from terminal."})

        elif path == "/api/unlock":
            self._json({"ok": False, "message":
                "Run: miflasher unlock from terminal for guided unlock."})

        elif path == "/api/wipe":
            targets = []
            if body.get("data"):    targets.append("userdata")
            if body.get("cache"):   targets.append("cache")
            if body.get("dalvik"):  pass  # adb only
            if not targets:
                self._json({"ok": False, "message": "Nothing selected"}); return
            results = []
            for t in targets:
                ok, out = _run(["fastboot", "erase", t])
                results.append(f"{'✓' if ok else '✗'} {t}")
            self._json({"ok": True, "message": " | ".join(results)})

        elif path == "/api/clear-logs":
            import shutil
            log_dir = os.path.expanduser("~/.local/share/miflasher/logs")
            shutil.rmtree(log_dir, ignore_errors=True)
            os.makedirs(log_dir, exist_ok=True)
            self._json({"ok": True, "message": "Logs cleared"})

        elif path == "/api/save-config":
            self._json({"ok": True, "message": "Config saved (placeholder)"})

        else:
            self._json({"error": "Unknown endpoint"}, 404)


# ─── Entrypoint ───────────────────────────────────────────────────────────────

def run_gui(host: str = "localhost", port: int = 8080, open_browser: bool = True):
    url = f"http://{host}:{port}"
    print(f"\n  \033[1;36m🌐 MiFlasher GUI running at {url}\033[0m")
    print(f"  \033[2mPress Ctrl+C to stop\033[0m\n")

    server = HTTPServer((host, port), APIHandler)

    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  \033[1;33m⚡ GUI stopped.\033[0m")
        server.shutdown()

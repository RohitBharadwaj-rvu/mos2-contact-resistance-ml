"""
MoS2 Contact Resistance & Physical Regime Explorer Web Dashboard (Sprint 7.8).
Full-stack interactive Flask application providing live multi-task ML predictions,
symbolic closed-form evaluations, Landauer quantum limits, and out-of-fold benchmark metrics.
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import json
from flask import Flask, render_template_string, request, jsonify

from src.pipeline.contact_predictor_pipeline import MoS2ContactPredictor, METAL_DATABASE

app = Flask(__name__)
predictor = MoS2ContactPredictor()

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoS₂ Contact Resistance & Semiconductor Physics Explorer (Audit-Remediated)</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-card: #111827;
            --bg-input: #1f2937;
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --accent-cyan: #06b6d4;
            --accent-blue: #3b82f6;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --accent-purple: #8b5cf6;
            --border-color: #374151;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            padding: 24px;
            line-height: 1.5;
        }

        .header {
            text-align: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
        }
        .header h1 {
            font-size: 26px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }
        .header p {
            font-size: 13px;
            color: var(--text-secondary);
            max-width: 900px;
            margin: 0 auto;
        }

        .provenance-banner {
            background-color: rgba(139, 92, 246, 0.12);
            border: 1px solid var(--accent-purple);
            border-radius: 8px;
            padding: 10px 16px;
            margin-bottom: 20px;
            font-size: 12px;
            color: #ddd6fe;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .grid-container {
            display: grid;
            grid-template-columns: 360px 1fr;
            gap: 20px;
        }

        .card {
            background-color: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }
        .card h2 {
            font-size: 16px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 14px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-color);
        }

        .form-group { margin-bottom: 12px; }
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        label {
            display: block;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 4px;
        }
        .form-control {
            width: 100%;
            padding: 8px 10px;
            background-color: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 13px;
        }
        .form-control:focus {
            outline: none;
            border-color: var(--accent-cyan);
        }

        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            padding: 8px 10px;
            background-color: rgba(6, 182, 212, 0.08);
            border-radius: 6px;
            border: 1px solid rgba(6, 182, 212, 0.25);
        }

        .btn-predict {
            width: 100%;
            padding: 10px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            color: #fff;
            border: none;
            border-radius: 6px;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            margin-top: 10px;
            transition: opacity 0.2s;
        }
        .btn-predict:hover { opacity: 0.9; }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 18px;
        }
        .metric-box {
            background-color: var(--bg-input);
            border-radius: 8px;
            padding: 12px;
            border: 1px solid var(--border-color);
            text-align: center;
        }
        .metric-title {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 4px;
        }
        .metric-value {
            font-size: 22px;
            font-weight: 800;
            font-family: 'Fira Code', monospace;
        }
        .val-primary { color: var(--accent-cyan); }
        .val-formula { color: var(--accent-amber); }
        .val-sbh { color: var(--accent-purple); }
        .val-quantum { color: var(--accent-green); }

        .regime-banner {
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 16px;
            border-left: 4px solid var(--accent-cyan);
            background-color: rgba(6, 182, 212, 0.1);
        }
        .regime-name {
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 2px;
        }
        .regime-desc {
            font-size: 12px;
            color: var(--text-secondary);
        }

        .guidance-box {
            background-color: rgba(16, 185, 129, 0.08);
            border: 1px solid var(--accent-green);
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 16px;
        }
        .guidance-box h3 {
            font-size: 13px;
            font-weight: 700;
            color: var(--accent-green);
            margin-bottom: 4px;
        }
        .guidance-text { font-size: 12px; color: #d1fae5; }

        .formula-callout {
            background-color: #0d131f;
            border: 1px dashed var(--accent-amber);
            border-radius: 8px;
            padding: 12px 16px;
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            color: #fde68a;
            margin-bottom: 16px;
        }

        .badge-sub100 {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 9999px;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-pass { background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
        .badge-fail { background-color: rgba(244, 63, 94, 0.2); color: #fb7185; border: 1px solid #f43f5e; }

        .leaderboard-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            margin-top: 8px;
        }
        .leaderboard-table th, .leaderboard-table td {
            padding: 6px 10px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        .leaderboard-table th {
            color: var(--text-secondary);
            font-weight: 600;
            background-color: #0d131f;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>MoS₂ Contact Resistance & Physical Characterization ML Dashboard</h1>
        <p>Scientific Audit-Remediated Architecture: Dual-task evaluation (Rc and SBH), 28 primary experimental publications, nested cross-validation, and headline Leave-One-Group-Out (LOGO) external benchmarks.</p>
    </div>

    <div class="provenance-banner">
        <span><strong>Primary Experimental Corpus:</strong> 28 device observations across 23 independent peer-reviewed experimental publications (Allain 2015 review traced & disentangled).</span>
        <span style="color: var(--accent-cyan); font-weight: 600;">Status: Verified & Online</span>
    </div>

    <div class="grid-container">
        <!-- Controls Sidebar -->
        <div class="card">
            <h2>Raw Experimental Levers</h2>
            <form id="predict-form">
                <div class="form-group">
                    <label for="metal">Contact Metal</label>
                    <select id="metal" class="form-control" onchange="autoFillMetalProps()">
                        <option value="Bi" selected>Bismuth (Bi) - vdW Semimetal (WM = 4.22 eV)</option>
                        <option value="Sb">Antimony (Sb) - vdW Semimetal (WM = 4.55 eV)</option>
                        <option value="Ti">Titanium (Ti) - Reactive Metal (WM = 4.33 eV)</option>
                        <option value="Sc">Scandium (Sc) - Low WF Metal (WM = 3.50 eV)</option>
                        <option value="Ag">Silver (Ag) - Low WF Metal (WM = 4.26 eV)</option>
                        <option value="Au">Gold (Au) - Noble Metal (WM = 5.10 eV)</option>
                        <option value="Pt">Platinum (Pt) - High WF Metal (WM = 5.65 eV)</option>
                        <option value="Pd">Palladium (Pd) - High WF Metal (WM = 5.22 eV)</option>
                        <option value="Ni">Nickel (Ni) - Intermediate (WM = 5.15 eV)</option>
                        <option value="Mo">Molybdenum (Mo) - Intermediate (WM = 4.60 eV)</option>
                        <option value="1T-MoS2">1T-MoS₂ Metallic Homojunction (WM = 4.20 eV)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="n2d">Gate Carrier Density $n_{2D}$ (cm⁻²)</label>
                    <input type="number" id="n2d" class="form-control" step="1e12" min="1e12" max="3e13" value="1.8e13">
                </div>

                <div class="checkbox-group">
                    <input type="checkbox" id="vdw" checked>
                    <label for="vdw" style="color: #fff; font-size: 12px; font-weight: 600; margin: 0; cursor: pointer;">van der Waals Transferred / De-pinned</label>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="layers">Layer Count</label>
                        <input type="number" id="layers" class="form-control" min="1" max="5" value="1">
                    </div>
                    <div class="form-group">
                        <label for="eot">Dielectric EOT (nm)</label>
                        <input type="number" id="eot" class="form-control" step="0.5" min="0.5" max="20.0" value="3.9">
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="anneal_temp">Annealing Temp (°C)</label>
                        <input type="number" id="anneal_temp" class="form-control" min="20" max="400" value="20">
                    </div>
                    <div class="form-group">
                        <label for="meas_temp">Meas. Temp (K)</label>
                        <input type="number" id="meas_temp" class="form-control" min="4" max="400" value="300">
                    </div>
                </div>

                <div class="form-group">
                    <label for="sbh">Schottky Barrier $\Phi_B$ (eV, optional)</label>
                    <input type="number" id="sbh" class="form-control" step="0.01" min="0.0" max="1.2" placeholder="Auto-predicted by Task 2 ML">
                </div>

                <button type="button" class="btn-predict" onclick="runPrediction()">Evaluate Contact Performance</button>
            </form>

            <div style="margin-top: 16px; font-size: 11px; color: var(--text-secondary); line-height: 1.4;">
                <strong>Primary ML Regressor:</strong> Random Forest (Task 1) + GBDT (Task 2)<br>
                <strong>Outer CV Scheme:</strong> Nested GroupKFold-5 & LOGO (23 Sources)<br>
                <strong>Unbiased Features:</strong> Zero baked pinning assumptions ($S=0.95/0.15$ removed)
            </div>
        </div>

        <!-- Output Dashboard -->
        <div>
            <!-- Metrics Row -->
            <div class="metrics-grid">
                <div class="metric-box">
                    <div class="metric-title">Predicted $R_c$ (ML Task 1)</div>
                    <div id="ml-rc" class="metric-value val-primary">234.6</div>
                    <small style="color: var(--text-secondary); font-size: 11px;">Ω·μm</small>
                </div>
                <div class="metric-box">
                    <div class="metric-title">Discovered Closed Form</div>
                    <div id="sym-rc" class="metric-value val-formula">103.1</div>
                    <small style="color: var(--text-secondary); font-size: 11px;">Ω·μm</small>
                </div>
                <div class="metric-box">
                    <div class="metric-title">Predicted $\Phi_B$ (Task 2)</div>
                    <div id="sbh-rc" class="metric-value val-sbh">0.08</div>
                    <small style="color: var(--text-secondary); font-size: 11px;">eV</small>
                </div>
                <div class="metric-box">
                    <div class="metric-title">Landauer Ballistic Floor</div>
                    <div id="quantum-rc" class="metric-value val-quantum">13.5</div>
                    <small style="color: var(--text-secondary); font-size: 11px;">Ω·μm</small>
                </div>
            </div>

            <!-- Regime & Status Card -->
            <div class="card" style="margin-bottom: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h2>Physical Transport Regime & Fabrication Guidance</h2>
                    <span id="sub100-badge" class="badge-sub100 badge-pass">Sub-100 Ω·μm Analysis</span>
                </div>

                <div id="regime-banner" class="regime-banner">
                    <div id="regime-title" class="regime-name" style="color: var(--accent-cyan);">Regime I: Ballistic / Quantum-Limited Regime</div>
                    <div id="regime-desc" class="regime-desc">Direct quantum tunneling into unpinned 2D channel. Minimal Schottky barrier bottleneck.</div>
                </div>

                <div class="guidance-box">
                    <h3>Laboratory Engineering Guidance</h3>
                    <div id="guidance-text" class="guidance-text">Predicted Rc satisfies target requirements for high-performance sub-1nm 2D logic.</div>
                </div>

                <div class="formula-callout">
                    <strong>Discovered Compact Closed-Form Scaling Law (Validated under LOGO):</strong><br>
                    $$\log_{10}(R_c\ [\Omega\cdot\mu\mathrm{m}]) \approx 1.399 + 0.312 \frac{W_M}{\sqrt{n_{2D}/10^{13}}} - 0.344 (\mathbb{I}_{\text{vdW}} \sqrt{n_{2D}/10^{13}}) + 0.405 \frac{|\Delta H_f|}{300}$$
                    <span style="font-size: 11px; color: #cbd5e1;">(Headline LOGO RMSE: 0.327 dex across 23 primary independent literature publications)</span>
                </div>
            </div>

            <!-- Model Benchmark Leaderboard -->
            <div class="card">
                <h2>Headline Benchmark Leaderboard (Nested GroupKFold & LOGO across 23 Primary Sources)</h2>
                <table class="leaderboard-table">
                    <thead>
                        <tr>
                            <th>Model Architecture</th>
                            <th>Family</th>
                            <th>Nested CV RMSE (dex)</th>
                            <th>LOGO RMSE (dex)</th>
                            <th>LOGO Spearman $\rho$</th>
                            <th>Generalization Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="background-color: rgba(6, 182, 212, 0.12); font-weight: 600;">
                            <td>Random Forest (Remediated)</td>
                            <td>Tree Ensemble</td>
                            <td>0.3666</td>
                            <td>0.3884</td>
                            <td>0.7699</td>
                            <td>Top Generalizer (Task 1)</td>
                        </tr>
                        <tr>
                            <td>LightGBM (Constrained)</td>
                            <td>Tree Ensemble</td>
                            <td>0.3775</td>
                            <td>0.4116</td>
                            <td>0.8850</td>
                            <td>Excellent Monotonicity</td>
                        </tr>
                        <tr>
                            <td>Support Vector Regression (RBF)</td>
                            <td>Kernel Machine</td>
                            <td>0.3984</td>
                            <td>0.4038</td>
                            <td>0.8539</td>
                            <td>Smooth Extrapolator</td>
                        </tr>
                        <tr>
                            <td>Discovered Compact GP Law</td>
                            <td>Symbolic Closed-Form</td>
                            <td>0.3438</td>
                            <td>0.3269</td>
                            <td>0.9163</td>
                            <td>Interpretable Heuristic</td>
                        </tr>
                        <tr>
                            <td>Gradient Boosting (Tuned)</td>
                            <td>Tree Ensemble</td>
                            <td>0.4033</td>
                            <td>0.4373</td>
                            <td>0.8129</td>
                            <td>Top Generalizer (Task 2)</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        function autoFillMetalProps() {
            const metal = document.getElementById('metal').value;
            const vdwBox = document.getElementById('vdw');
            if (metal === 'Bi' || metal === 'Sb' || metal === '1T-MoS2') {
                vdwBox.checked = true;
            } else {
                vdwBox.checked = false;
            }
            runPrediction();
        }

        async function runPrediction() {
            const metal = document.getElementById('metal').value;
            const n2d = parseFloat(document.getElementById('n2d').value);
            const vdw = document.getElementById('vdw').checked;
            const layers = parseInt(document.getElementById('layers').value);
            const eot = parseFloat(document.getElementById('eot').value);
            const anneal_temp = parseFloat(document.getElementById('anneal_temp').value);
            const meas_temp = parseFloat(document.getElementById('meas_temp').value);
            const sbhVal = document.getElementById('sbh').value;
            const sbh = sbhVal ? parseFloat(sbhVal) : null;

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        metal,
                        n2d,
                        vdw,
                        layer_count: layers,
                        eot,
                        anneal_temp,
                        meas_temp,
                        sbh
                    })
                });
                const data = await response.json();

                // Update UI values
                const mlRc = data.predicted_contact_resistance.task1_random_forest.rc_ohm_um;
                const symRc = data.predicted_contact_resistance.discovered_closed_form_law.rc_ohm_um;
                const sbhVal = data.predicted_schottky_barrier.sbh_ev;
                const qRc = data.physical_limits.landauer_quantum_floor_ohm_um;

                document.getElementById('ml-rc').innerText = mlRc.toFixed(1);
                document.getElementById('sym-rc').innerText = symRc.toFixed(1);
                document.getElementById('sbh-rc').innerText = sbhVal.toFixed(2);
                document.getElementById('quantum-rc').innerText = qRc.toFixed(1);

                document.getElementById('regime-title').innerText = data.transport_regime.regime_name;
                document.getElementById('regime-desc').innerText = data.transport_regime.description;
                document.getElementById('guidance-text').innerText = data.engineering_guidance.join(' ');

                const badge = document.getElementById('sub100-badge');
                if (mlRc <= 100.0) {
                    badge.className = 'badge-sub100 badge-pass';
                    badge.innerText = 'Sub-100 Ω·μm Achieved';
                } else {
                    badge.className = 'badge-sub100 badge-fail';
                    badge.innerText = `Exceeds Target (${mlRc.toFixed(0)} Ω·μm)`;
                }
            } catch (err) {
                console.error('Prediction failed:', err);
            }
        }

        window.onload = function() {
            runPrediction();
        };
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json() or {}
    metal = data.get("metal", "Bi")
    n2d = float(data.get("n2d", 1.8e13))
    vdw = bool(data.get("vdw", True))
    layers = int(data.get("layer_count", 1))
    eot = float(data.get("eot", 3.9))
    anneal_temp = float(data.get("anneal_temp", 20.0))
    meas_temp = float(data.get("meas_temp", 300.0))
    sbh = float(data.get("sbh")) if data.get("sbh") is not None else None

    res = predictor.predict(
        metal=metal,
        gate_carrier_density_cm2=n2d,
        is_vdw_transferred=vdw,
        layer_count=layers,
        dielectric_eot_nm=eot,
        post_annealing_temperature_c=anneal_temp,
        is_annealed=(anneal_temp > 25.0),
        measurement_temperature_k=meas_temp,
        schottky_barrier_height_ev=sbh
    )
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False)

"""
MoS2 Contact Resistance & Physical Regime Explorer Web Dashboard (Sprint 6.b.3).
Full-stack interactive Flask application providing live ML and symbolic predictions,
regime diagnosis, Landauer limit comparisons, and design guidelines.
"""

import json
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify

from src.pipeline.contact_predictor_pipeline import MoS2ContactPredictor, METAL_DATABASE

app = Flask(__name__)
predictor = MoS2ContactPredictor()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoS2 Contact Resistance & Physics Explorer</title>
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
            margin-bottom: 28px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
        }
        .header h1 {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .header p {
            color: var(--text-secondary);
            font-size: 14px;
            max-width: 800px;
            margin: 0 auto;
        }

        .grid-container {
            display: grid;
            grid-template-columns: 380px 1fr;
            gap: 24px;
            max-width: 1400px;
            margin: 0 auto;
        }

        .card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 22px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
        }

        .card h2 {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 18px;
            color: var(--accent-cyan);
            border-bottom: 1px solid #1f2937;
            padding-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .form-group {
            margin-bottom: 16px;
        }
        .form-group label {
            display: block;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 6px;
            color: var(--text-secondary);
        }
        .form-control {
            width: 100%;
            padding: 10px 14px;
            background-color: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: #fff;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }
        .form-control:focus {
            border-color: var(--accent-cyan);
        }

        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            margin-top: 12px;
            margin-bottom: 18px;
        }
        .checkbox-group input {
            width: 18px;
            height: 18px;
            accent-color: var(--accent-cyan);
        }

        .btn-predict {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
            color: #fff;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            font-size: 15px;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        .btn-predict:hover { opacity: 0.9; }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 22px;
        }
        .metric-box {
            background-color: var(--bg-input);
            border-radius: 10px;
            padding: 16px;
            border: 1px solid var(--border-color);
            text-align: center;
        }
        .metric-title {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }
        .metric-value {
            font-size: 26px;
            font-weight: 800;
            font-family: 'Fira Code', monospace;
        }
        .val-primary { color: var(--accent-cyan); }
        .val-formula { color: var(--accent-amber); }
        .val-quantum { color: var(--accent-green); }

        .regime-banner {
            padding: 14px 18px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid var(--accent-cyan);
            background-color: rgba(6, 182, 212, 0.1);
        }
        .regime-name {
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 4px;
        }
        .regime-desc {
            font-size: 13px;
            color: var(--text-secondary);
        }

        .guidance-box {
            background-color: rgba(16, 185, 129, 0.1);
            border: 1px solid var(--accent-green);
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 20px;
        }
        .guidance-box h3 {
            font-size: 14px;
            font-weight: 700;
            color: var(--accent-green);
            margin-bottom: 4px;
        }
        .guidance-text { font-size: 13px; color: #d1fae5; }

        .formula-callout {
            background-color: #0d131f;
            border: 1px dashed var(--accent-amber);
            border-radius: 8px;
            padding: 14px 18px;
            font-family: 'Fira Code', monospace;
            font-size: 13px;
            color: #fde68a;
            margin-bottom: 20px;
        }

        .badge-sub100 {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-pass { background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
        .badge-fail { background-color: rgba(244, 63, 94, 0.2); color: #fb7185; border: 1px solid #f43f5e; }

        .leaderboard-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            margin-top: 10px;
        }
        .leaderboard-table th, .leaderboard-table td {
            padding: 8px 12px;
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
        <h1>MoS₂ Contact Resistance & Semiconductor Physics Explorer</h1>
        <p>Physics-informed machine learning inference, Landauer ballistic limits, transport regime mapping, and quantitative design rules for sub-100 Ω·μm 2D electronics.</p>
    </div>

    <div class="grid-container">
        <!-- Controls Sidebar -->
        <div class="card">
            <h2>Device Parameters</h2>
            <form id="predict-form">
                <div class="form-group">
                    <label for="metal">Contact Metal</label>
                    <select id="metal" class="form-control" onchange="autoFillMetalProps()">
                        <option value="Bi" selected>Bismuth (Bi) - vdW Semimetal</option>
                        <option value="Sb">Antimony (Sb) - vdW Semimetal</option>
                        <option value="Ti">Titanium (Ti) - Reactive</option>
                        <option value="Sc">Scandium (Sc) - Reactive</option>
                        <option value="Ag">Silver (Ag) - Low WF</option>
                        <option value="Au">Gold (Au) - Noble Metal</option>
                        <option value="Pt">Platinum (Pt) - High WF</option>
                        <option value="Pd">Palladium (Pd) - P-Type Candidate</option>
                        <option value="Ni">Nickel (Ni)</option>
                        <option value="1T-MoS2">1T-MoS₂ Metallic Homojunction</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="n2d">Gate Carrier Density $n_{2D}$ (cm⁻²)</label>
                    <input type="number" id="n2d" class="form-control" step="1e12" min="1e12" max="3e13" value="1.8e13">
                    <small style="color: var(--text-secondary); font-size: 11px;">Range: 1.0e12 (SiO₂) to 2.5e13 (HfO₂ / Ion Gel)</small>
                </div>

                <div class="checkbox-group">
                    <input type="checkbox" id="vdw" checked>
                    <label for="vdw" style="color: #fff; font-size: 13px; font-weight: 600; margin: 0; cursor: pointer;">Van der Waals Transferred / Phase De-pinned</label>
                </div>

                <div class="form-group">
                    <label for="sbh">Schottky Barrier Height $\Phi_B$ (eV, optional)</label>
                    <input type="number" id="sbh" class="form-control" step="0.01" min="0.0" max="1.2" placeholder="Auto-calculated from metal">
                </div>

                <button type="button" class="btn-predict" onclick="runPrediction()">Evaluate Contact Performance</button>
            </form>

            <div style="margin-top: 24px; font-size: 12px; color: var(--text-secondary);">
                <strong>Status:</strong> <span style="color: var(--accent-green); font-weight: 600;">System Online</span><br>
                <strong>Backend Engine:</strong> Tuned Ridge Regression + Discovered Pareto Law<br>
                <strong>Cross-Validation:</strong> GroupKFold (5-Fold, Source Paper Grouped)
            </div>
        </div>

        <!-- Output Dashboard -->
        <div>
            <!-- Metrics Row -->
            <div class="metrics-grid">
                <div class="metric-box">
                    <div class="metric-title">Predicted $R_c$ (ML Model)</div>
                    <div id="ml-rc" class="metric-value val-primary">68.1</div>
                    <small style="color: var(--text-secondary); font-size: 12px;">Ω·μm</small>
                </div>
                <div class="metric-box">
                    <div class="metric-title">Discovered Closed-Form Law</div>
                    <div id="sym-rc" class="metric-value val-formula">75.9</div>
                    <small style="color: var(--text-secondary); font-size: 12px;">Ω·μm</small>
                </div>
                <div class="metric-box">
                    <div class="metric-title">Landauer Ballistic Floor</div>
                    <div id="quantum-rc" class="metric-value val-quantum">13.5</div>
                    <small style="color: var(--text-secondary); font-size: 12px;">Ω·μm ($R_{c,\min}$)</small>
                </div>
            </div>

            <!-- Regime & Status Card -->
            <div class="card" style="margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <h2>Transport Regime & Feasibility Diagnosis</h2>
                    <span id="sub100-badge" class="badge-sub100 badge-pass">Sub-100 Ω·μm Achieved</span>
                </div>

                <div id="regime-banner" class="regime-banner">
                    <div id="regime-title" class="regime-name" style="color: var(--accent-cyan);">Regime I: Ballistic / Quantum-Limited Regime</div>
                    <div id="regime-desc" class="regime-desc">Landauer-Sharvin ballistic quantum injection limit. Van der Waals de-pinning eliminates the interfacial vacuum barrier.</div>
                </div>

                <div class="guidance-box">
                    <h3>Laboratory Engineering Guidance</h3>
                    <div id="guidance-text" class="guidance-text">Target achieved: Ultra-low contact resistance (< 100 Ohm*um) successfully satisfied for sub-1nm CMOS node!</div>
                </div>

                <div class="formula-callout">
                    <strong>Discovered Closed-Form Law:</strong><br>
                    $$\log_{10}(R_c\ [\Omega\cdot\mu\mathrm{m}]) \approx \Phi_B\ [\mathrm{eV}] - \left(\frac{n_{2D}}{10^{13}\ \mathrm{cm}^{-2}}\right) + 3.660$$
                    $$R_c \approx 4570 \cdot 10^{\Phi_B - (n_{2D}/10^{13})}\quad [\Omega\cdot\mu\mathrm{m}]$$
                </div>
            </div>

            <!-- Model Benchmark Leaderboard -->
            <div class="card">
                <h2>Validated Benchmark Leaderboard (Grouped 5-Fold CV)</h2>
                <table class="leaderboard-table">
                    <thead>
                        <tr>
                            <th>Model Architecture</th>
                            <th>CV RMSE (dex)</th>
                            <th>Spearman $\rho$</th>
                            <th>Kendall $\tau$</th>
                            <th>Composite Score</th>
                            <th>Physical Validity</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="background-color: rgba(6, 182, 212, 0.1); font-weight: 600;">
                            <td>Tuned Ridge Regression</td>
                            <td>0.2260</td>
                            <td>0.9489</td>
                            <td>0.8316</td>
                            <td>0.8720 (Rank 1)</td>
                            <td>100% Monotonic</td>
                        </tr>
                        <tr>
                            <td>Tuned ElasticNet</td>
                            <td>0.2277</td>
                            <td>0.9489</td>
                            <td>0.8316</td>
                            <td>0.8710 (Rank 2)</td>
                            <td>100% Monotonic</td>
                        </tr>
                        <tr>
                            <td>Discovered Symbolic Surrogate</td>
                            <td>0.3859</td>
                            <td>0.8887</td>
                            <td>0.7444</td>
                            <td>0.7751 (Rank 6)</td>
                            <td>Analytical Closed-Form</td>
                        </tr>
                        <tr>
                            <td>Gradient Boosting (Tuned)</td>
                            <td>0.3838</td>
                            <td>0.9023</td>
                            <td>0.7474</td>
                            <td>0.7870 (Rank 3)</td>
                            <td>Piecewise Constrained</td>
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
            const sbhVal = document.getElementById('sbh').value;
            const sbh = sbhVal ? parseFloat(sbhVal) : null;

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ metal, n2d, vdw, sbh })
                });
                const data = await response.json();

                // Update UI values
                const mlRc = data.predicted_contact_resistance.ml_model_ridge.rc_ohm_um;
                const symRc = data.predicted_contact_resistance.discovered_closed_form_law.rc_ohm_um;
                const qRc = data.physical_limits.landauer_quantum_floor_ohm_um;

                document.getElementById('ml-rc').innerText = mlRc.toFixed(1);
                document.getElementById('sym-rc').innerText = symRc.toFixed(1);
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
    sbh = float(data.get("sbh")) if data.get("sbh") is not None else None

    res = predictor.predict(
        metal=metal,
        gate_carrier_density_cm2=n2d,
        is_vdw_transferred=vdw,
        schottky_barrier_height_ev=sbh
    )
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False)

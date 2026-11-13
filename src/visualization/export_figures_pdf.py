"""Export all project structural and analytical graphs into a single formatted PDF atlas."""

from __future__ import annotations

from pathlib import Path
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
ARTIFACT_DASHBOARD = Path(
    r"C:\Users\rohit\.gemini\antigravity\brain\40351c3a-3e08-415f-8617-d9dac2b5ded1\dashboard_live_verification.png"
)
OUTPUT_PDF = Path(r"C:\Users\rohit\Downloads\MoS2_Contact_Resistance_ML_Figures_Atlas.pdf")


SECTIONS = [
    (
        "1. Structural Graphs, Decision Trees & Flowchart Networks",
        [
            (
                "1.1 Literature Citation Network Graph",
                FIGURES_DIR / "citation_network_graph.png",
                "NetworkX directed graph mapping citation and intellectual dependencies across foundational solid-state theories (Landauer-Buttiker, Bardeen, Heine, Tersoff), landmark primary experimental studies (Kappera 2014, Liu 2018, Shen 2019, Wang 2019), review syntheses (Allain 2015), and cross-validation benchmark folds.",
            ),
            (
                "1.2 Random Forest Decision Tree Graph",
                FIGURES_DIR / "random_forest_decision_tree_graph.png",
                "Tree topology of an individual estimator from the production Random Forest ensemble. Each node displays the physical split threshold (such as metal work function, carrier density, or de-pinning indicator), sample count, and MSE impurity reduction.",
            ),
            (
                "1.3 Experimental Hierarchy Decision Flowchart Graph",
                FIGURES_DIR / "experimental_decision_flowchart_graph.png",
                "Directed laboratory optimization flowchart translating the ML model's top feature sensitivities into a 4-step fabrication hierarchy for realizing sub-100 Ohm*um ohmic contacts on monolayer and few-layer MoS2.",
            ),
            (
                "1.4 Observational Mediation Path DAG",
                FIGURES_DIR / "mediation_path_analysis.png",
                "Directed acyclic path diagram decomposing direct versus mediated contact resistance mechanisms. Observational path analysis indicates that 94.7% of resistance reduction in de-pinned architectures is statistically mediated through Schottky barrier height reduction.",
            ),
            (
                "1.5 Confounding & Partial Correlation Matrix",
                FIGURES_DIR / "confounding_partial_correlation_matrix.png",
                "Gaussian Graphical Model and partial correlation matrix isolating direct conditional dependencies between fabrication variables, electronic descriptors, and contact resistance from spurious bivariate correlations.",
            ),
        ],
    ),
    (
        "2. Literature Dataset & Exploratory Data Analysis",
        [
            (
                "2.1 Univariate Physical Property Distributions",
                FIGURES_DIR / "univariate_distributions.png",
                "Histograms and kernel density estimates for primary targets (log10 Rc, measured Schottky barrier height Phi_B) and key experimental inputs (2D carrier density n_2D, metal work function W_M) across the curated primary corpus.",
            ),
            (
                "2.2 Bivariate Physical Relationships",
                FIGURES_DIR / "bivariate_physical_relationships.png",
                "Bivariate scatter plots comparing contact resistance against metal work function, channel carrier density, and interfacial chemical reactivity, highlighting the separation between conventional evaporated and van der Waals transferred contacts.",
            ),
            (
                "2.3 Multi-Feature Correlation Heatmap",
                FIGURES_DIR / "feature_correlation_heatmap.png",
                "Pairwise Pearson and Spearman rank correlation heatmaps identifying dominant linear and monotonic relationships across all experimental, structural, and electronic features.",
            ),
            (
                "2.4 Dataset Sparsity & Measurement Gaps Radar",
                FIGURES_DIR / "dataset_sparsity_and_gaps_radar.png",
                "Radar chart auditing reporting completeness across experimental dimensions—such as annealing ambient, measurement temperature, dielectric stack, and extraction method—in published MoS2 FET literature.",
            ),
            (
                "2.5 Inter-Paper Experimental Variance Analysis",
                FIGURES_DIR / "inter_paper_variance_analysis.png",
                "Per-publication boxplots and ANOVA variance breakdown quantifying systematic laboratory-to-laboratory scatter across independent research groups.",
            ),
        ],
    ),
    (
        "3. Cross-Validation & Machine Learning Benchmarks",
        [
            (
                "3.1 Nested GroupKFold-5 vs. Headline LOGO Comparison",
                FIGURES_DIR / "nested_vs_logo_validation_comparison.png",
                "Generalization comparison between 5-fold Nested GroupKFold and Leave-One-Group-Out (LOGO) cross-validation across independent papers. Strict inner-loop tuning prevents selection optimism and benchmarks out-of-publication accuracy.",
            ),
            (
                "3.2 Dual-Task Model Suite Nested Benchmark",
                FIGURES_DIR / "model_suite_nested_benchmark.png",
                "Multi-architecture leaderboard comparing Linear (Ridge, ElasticNet), Kernel (SVR), Bayesian (Gaussian Process), and Tree Ensembles (Random Forest, XGBoost, LightGBM, HistGradientBoosting) across Task 1 (Rc prediction) and Task 2 (Phi_B prediction).",
            ),
            (
                "3.3 Residual Parity Plot",
                FIGURES_DIR / "residual_parity_plot.png",
                "Out-of-fold parity plot comparing experimentally measured vs. ML-predicted log10 Rc, overlaid with +/-0.5 dex uncertainty bounds to visualize calibration across 4 orders of magnitude.",
            ),
            (
                "3.4 Residual Error Diagnostics & Normality",
                FIGURES_DIR / "residual_diagnostics.png",
                "Residual distribution histogram and normal Q-Q diagnostic plot verifying approximate normality and homoscedasticity of out-of-fold prediction errors.",
            ),
            (
                "3.5 Out-of-Fold Permutation Feature Importance",
                FIGURES_DIR / "permutation_importance_oof.png",
                "Out-of-fold permutation importance ranking showing that gate-modulated carrier density (n_2D) and de-pinned interface architecture carry the highest predictive signal on unseen papers.",
            ),
        ],
    ),
    (
        "4. Symbolic Regression & Physical Scaling Laws",
        [
            (
                "4.1 Symbolic Regression Cross-Validated Pareto Frontier",
                FIGURES_DIR / "symbolic_cross_validated_frontier.png",
                "Pareto frontier plotting expression complexity against held-out cross-validated RMSE for candidate analytical contact resistance laws discovered via symbolic regression.",
            ),
            (
                "4.2 ML Predictions vs. Theoretical Ballistic Limits",
                FIGURES_DIR / "ml_vs_theoretical_models.png",
                "Comparison of empirical ML predictions against the Landauer quantum ballistic limit (R_Q ~ 33 Ohm*um) and classical thermionic/tunneling transport bounds across carrier densities.",
            ),
        ],
    ),
    (
        "5. Model Interpretability & SHAP Attributions",
        [
            (
                "5.1 Out-of-Fold SHAP Importance Summary",
                FIGURES_DIR / "oof_shap_summary.png",
                "Mean absolute SHAP feature attributions computed strictly out-of-fold using fold-specific models, preventing in-sample explanation leakage.",
            ),
            (
                "5.2 SHAP Summary Beeswarm Plot",
                FIGURES_DIR / "shap_summary_beeswarm.png",
                "Device-level SHAP beeswarm plot illustrating both magnitude and directionality—showing how higher carrier density and vdW/semimetal de-pinning systematically drive Rc downward.",
            ),
            (
                "5.3 Cross-Architecture SHAP Comparison",
                FIGURES_DIR / "shap_cross_architecture_comparison.png",
                "Consistency check comparing SHAP attribution rankings across Random Forest, Gradient Boosting, and Linear architectures to verify physical stability.",
            ),
            (
                "5.4 1D Partial Dependence & ICE Curves",
                FIGURES_DIR / "pdp_ice_curves.png",
                "Partial Dependence (PDP) and Individual Conditional Expectation (ICE) curves revealing the non-linear inflection near n_2D ~ 3e12 cm^-2 where transport transitions from barrier-limited to tunneling-dominated.",
            ),
            (
                "5.5 2D Partial Dependence Interaction Surface",
                FIGURES_DIR / "pdp_2d_interaction_surface.png",
                "Two-dimensional interaction surface mapping the joint effect of metal work function (W_M) and carrier density (n_2D) on predicted contact resistance.",
            ),
        ],
    ),
    (
        "6. Physical Transport Regime Phase Diagrams",
        [
            (
                "6.1 2D Contact Resistance Transport Regime Phase Diagram",
                FIGURES_DIR / "regime_phase_diagram_2d.png",
                "2D transport phase diagram delineating Thermionic Emission, Thermionic-Field Emission, Tunneling / Field Emission, and Quantum Ballistic regimes across carrier density and contact resistance.",
            ),
            (
                "6.2 Work Function vs. Barrier Height (Pinning vs. Schottky-Mott Map)",
                FIGURES_DIR / "regime_phase_diagram_workfunction.png",
                "Phase map contrasting Fermi-level-pinned conventional evaporated contacts (pinning factor S ~ 0.13) against de-pinned van der Waals and semimetal contacts approaching the ideal Schottky-Mott limit (S ~ 0.95).",
            ),
        ],
    ),
    (
        "7. Physical Decoupling & Experimental Optimization",
        [
            (
                "7.1 Out-of-Fold Variance Decomposition with Bootstrap CIs",
                FIGURES_DIR / "oof_variance_decomposition_bootstrap.png",
                "Out-of-fold variance decomposition with 1,000 bootstrap confidence intervals attributing total Rc variance to intrinsic electronic factors (63.4%), extrinsic processing conditions (10.6%), and inter-lab/device residual variance (26.6%).",
            ),
            (
                "7.2 Sequential Intrinsic vs. Extrinsic Decomposition",
                FIGURES_DIR / "intrinsic_vs_extrinsic_decomposition.png",
                "Sequential regression breakdown quantifying incremental R^2 explained by intrinsic band-alignment features versus extrinsic fabrication and interface cleanliness modifiers.",
            ),
            (
                "7.3 Experimental Parameter Return-on-Investment (ROI) Ranking",
                FIGURES_DIR / "experimental_parameter_roi_ranking.png",
                "Sensitivity ranking scoring controllable fabrication levers by their expected impact on driving contact resistance toward the IRDS sub-100 Ohm*um benchmark.",
            ),
        ],
    ),
    (
        "8. Live Interactive Web Dashboard",
        [
            (
                "8.1 Verified Full-Stack Flask Dashboard Interface",
                ARTIFACT_DASHBOARD if ARTIFACT_DASHBOARD.exists() else FIGURES_DIR / "dashboard_live_screenshot.png",
                "Live Playwright capture of the Flask web dashboard (http://127.0.0.1:5050), providing interactive multi-task Rc and Phi_B predictions, symbolic law evaluation, and transport regime classification.",
            ),
        ],
    ),
]


def _add_page_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(
        doc.leftMargin,
        0.38 * inch,
        "MoS2 Contact Resistance & Schottky Barrier Height ML — Visual Atlas",
    )
    canvas.drawRightString(
        letter[0] - doc.rightMargin,
        0.38 * inch,
        f"Page {doc.page}",
    )
    canvas.restoreState()


def build_pdf(output_path: Path = OUTPUT_PDF) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.6 * inch,
        title="MoS2 Contact Resistance ML - Complete Figures Atlas",
        author="MoS2 Contact Resistance ML Pipeline",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "AtlasTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=27,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=10,
    )
    subtitle_style = ParagraphStyle(
        "AtlasSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=17,
        textColor=colors.HexColor("#334155"),
        spaceAfter=18,
    )
    section_badge_style = ParagraphStyle(
        "SectionBadge",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1D4ED8"),
        spaceAfter=3,
    )
    fig_title_style = ParagraphStyle(
        "FigTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=8,
    )
    explainer_style = ParagraphStyle(
        "ExplainerText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1E293B"),
    )
    toc_section_style = ParagraphStyle(
        "TOCSection",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=5,
        spaceAfter=2,
    )
    toc_item_style = ParagraphStyle(
        "TOCItem",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        leftIndent=12,
        textColor=colors.HexColor("#475569"),
    )

    story = []

    # Cover Page
    story.append(Spacer(1, 0.35 * inch))
    story.append(
        Paragraph(
            "MoS<sub>2</sub> Contact Resistance &amp; Schottky Barrier Height ML",
            title_style,
        )
    )
    story.append(
        Paragraph(
            "Complete Visual Atlas of Structural Graphs, Cross-Validation Benchmarks, Symbolic Scaling Laws, SHAP Interpretability &amp; Transport Regime Phase Maps",
            subtitle_style,
        )
    )

    total_figs = sum(len(figs) for _, figs in SECTIONS)
    summary_data = [
        ["Repository", "RohitBharadwaj-rvu/mos2-contact-resistance-ml"],
        ["Validation Protocol", "Nested GroupKFold-5 & Leave-One-Group-Out (LOGO)"],
        ["Total Figures Included", f"{total_figs} Figures (Structural Graphs + Analytical Plots)"],
        ["Prediction Tasks", "Task 1: log10(Rc) [Ohm*um] | Task 2: Schottky Barrier Phi_B [eV]"],
    ]
    summary_table = Table(summary_data, colWidths=[1.8 * inch, 5.5 * inch])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EFF6FF")),
                ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#F8FAFC")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#0F172A")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Contents", ParagraphStyle("TOCHdr", parent=styles["Heading3"], fontSize=12, spaceAfter=4)))

    for section_name, figs in SECTIONS:
        story.append(Paragraph(section_name, toc_section_style))
        for fig_title, _, _ in figs:
            story.append(Paragraph(f"• {fig_title}", toc_item_style))

    # Figure Pages (1 figure + explainer per page)
    max_width = 7.35 * inch
    max_height = 7.25 * inch

    for section_name, figs in SECTIONS:
        for fig_title, img_path, explainer in figs:
            if not img_path.exists():
                raise FileNotFoundError(f"Missing figure image: {img_path}")

            story.append(PageBreak())
            story.append(Paragraph(section_name.upper(), section_badge_style))
            story.append(Paragraph(fig_title, fig_title_style))

            explainer_box = Table(
                [[Paragraph(explainer, explainer_style)]],
                colWidths=[max_width],
            )
            explainer_box.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
                        ("LINEBEFORE", (0, 0), (0, -1), 3, colors.HexColor("#2563EB")),
                        ("PADDING", (0, 0), (-1, -1), 8),
                    ]
                )
            )
            story.append(explainer_box)
            story.append(Spacer(1, 0.18 * inch))

            with PILImage.open(img_path) as pil_img:
                w_px, h_px = pil_img.size

            scale = min(max_width / float(w_px), max_height / float(h_px))
            draw_w = w_px * scale
            draw_h = h_px * scale

            img_flowable = Image(str(img_path), width=draw_w, height=draw_h)
            img_flowable.hAlign = "CENTER"
            story.append(img_flowable)

    doc.build(story, onFirstPage=_add_page_footer, onLaterPages=_add_page_footer)
    return output_path


if __name__ == "__main__":
    out = build_pdf()
    print(f"Successfully exported {sum(len(f) for _, f in SECTIONS)} figures to: {out}")

# Comprehensive Execution Roadmap: $\text{MoS}_2$ Contact Resistance & Schottky Barrier Height ML Project

This roadmap outlines the procedural workflow for your project. Every step is framed purely as an investigative or execution task, without pre-selecting any specific tools, techniques, metrics, or modeling choices upfront.

---

## 1. Data Aggregation & Curation

### a. Finding All Sources for Papers, Databases, and Other Resources
1. **Survey Scientific Literature Indexes:** Research and compile a list of academic search engines, publisher portals, and citation indexes that cover condensed matter physics, materials science, and nanoelectronics.
2. **Investigate Existing Material Property Databases:** Search for open-access computational and experimental materials databases that contain baseline elemental and material properties for contact metals and 2D semiconductors.
3. **Locate Pre-Existing Benchmark Compilations:** Search the literature for recent review articles, meta-analyses, or supplementary data repositories on 2D transistor contacts that have aggregated tables of experimental results.
4. **Evaluate Source Accessibility and Coverage:** Assess which of the identified databases and indexes you have access to, and determine which ones offer the best export tools for metadata or citation tracking.

### b. Mining Said Sources for All Relevant Papers, Databases, and Resources
1. **Develop and Test Search Taxonomies:** Research and test combinations of keywords, synonyms, and search operators related to your material, target metrics, and fabrication variables to maximize relevance and minimize noise.
2. **Execute Literature Searches:** Run your finalized queries across the selected search engines and log the raw list of returned articles, reviews, and datasets.
3. **Perform Citation Tracing:** Inspect the bibliographies of highly relevant papers and examine newer papers that cite them to capture studies missed by initial searches.
4. **Extract Elemental & Material Reference Data:** Query the material property databases found in Step 1a to gather intrinsic physical constants for the candidate contact metals and semiconductor layers.
5. **Organize Raw Collected Sources:** Set up a tracking system to catalog all mined files, supplementary documents, and database exports, assigning a unique identifier to each source.

### c. Removing Low-Quality Papers, Databases, and Other Resources
1. **Research Valid Characterization Standards:** Investigate the semiconductor characterization literature to understand how contact resistance and Schottky barrier height are measured experimentally, and identify which measurement methods are reliable versus error-prone.
2. **Define Inclusion and Exclusion Criteria:** Establish a formal checklist to filter your mined sources based on study type, experimental validity, and reporting completeness.
3. **Screen Titles and Abstracts:** Perform an initial pass over your raw source list to remove papers that are off-topic, focus on the wrong material system, or do not report electrical contact metrics.
4. **Audit Full Texts for Methodological Quality:** Read the experimental and characterization sections of the remaining papers to verify that their measurement conditions and parameter extraction techniques meet your quality criteria.
5. **Audit Data Completeness and Consistency:** Discard or quarantine sources where the reported data is contradictory, uncalibrated, or missing too many input variables to be useful for modeling.

### d. Extracting All Usable Data
1. **Design the Raw Data Extraction Schema:** Research and determine every piece of information you need to record from each paper—including source metadata, material attributes, processing recipes, measurement conditions, and target values—and build a structured data entry template.
2. **Extract Tabular and Textual Values:** Systematically go through the accepted papers and their supplementary information to record all explicitly stated numerical values and categorical descriptions into your template.
3. **Identify and Digitize Graphical Data:** Locate relevant plots and figures in the papers where raw numbers are not provided in text, research tools for extracting data from figures, and record the underlying values.
4. **Record Data Provenance and Context:** For every extracted row, log the source identifier, location within the source, and any unique experimental notes so that every data point can be audited later.

### e. Filtering, Cleaning, and Engineering Data
1. **Audit and Standardize Units:** Inspect all numerical columns across your extracted dataset, identify discrepancies in how different authors report units for the same physical quantity, and determine the mathematical conversions needed to bring every column to a single standard unit.
2. **Establish Categorical Taxonomies:** Review the raw text descriptions of fabrication steps and material attributes, and group synonymous or overlapping descriptions into standardized categories.
3. **Investigate Missing Data Patterns:** Analyze which columns have missing values, research whether default experimental assumptions can be safely inferred from domain norms, and decide on a strategy for handling remaining gaps.
4. **Research Domain-Specific Feature Engineering:** Study the physics of metal-semiconductor interfaces to hypothesize new composite features, combinations, or external descriptors that could better represent the underlying contact mechanisms than the raw inputs alone.
5. **Evaluate Target Variable Transformations:** Check the numerical range and scaling of your target variables and determine if mathematical transformations are required for regression modeling.

### f. Performing Exploratory Data Analysis (EDA) to Guide ML and Physical Deductions
1. **Analyze Univariate Distributions:** Plot the distributions of all input features and target variables to understand dataset coverage, class imbalances in categorical variables, skewness, and potential outliers.
2. **Investigate Bivariate Physical Relationships:** Plot key input variables against your targets to visually inspect whether expected physical trends appear in the raw data or if they are obscured by other variables.
3. **Assess Feature Collinearity and Redundancy:** Compute statistical associations across all input variables to identify redundant features or confounding relationships where multiple fabrication choices co-occur.
4. **Analyze Inter-Paper Variance and Lab Bias:** Group and visualize the data by source paper to investigate how much variance comes from lab-to-lab systematic differences versus actual material and processing changes.
5. **Synthesize EDA Findings for Modeling:** Document what the data distributions, sample size, missingness, and noise levels imply for how you should structure your machine learning pipeline and what physical questions the dataset is capable of answering.

---

## 2. Identify Candidate Models, Architectures & ML Paradigms

### a. Formulate the Learning Tasks
1. **Define Target Formulations:** Decide how to structure the prediction tasks for your target variables and whether to treat them independently or jointly.
2. **Assess Sample-to-Feature Ratios:** Evaluate how the number of usable rows and features in your curated dataset constrains the complexity of models you can realistically train without overfitting.

### b. Research and Select Baseline Models
1. **Define Naive Statistical Baselines:** Research and choose simple reference predictors to establish the floor of predictive performance.
2. **Define Simple Parametric Baselines:** Research standard low-complexity regression models that can represent simple baseline relationships to serve as a benchmark for more complex models.

### c. Evaluate Non-Linear Tabular ML Architectures
1. **Investigate Tree-Based Ensemble Methods:** Research decision-tree ensemble and boosting frameworks to understand how they handle mixed categorical and numerical features, non-linear interactions, and missing values.
2. **Investigate Alternative Regression Paradigms:** Explore other families of machine learning algorithms to see if they offer advantages for your specific dataset structure and size.
3. **Select Final Candidate Architectures:** Compare the strengths and weaknesses of the researched models against your EDA findings and shortlist the specific algorithms you will implement.

### d. Research Symbolic Regression Paradigms
1. **Survey Symbolic Regression Algorithms and Tools:** Research how symbolic regression algorithms operate and evaluate available software libraries.
2. **Determine Mathematical Search Spaces:** Investigate which mathematical operators, complexity penalties, and physical constraints should be allowed when searching for closed-form equations describing your targets.

### e. Research Interpretability and Feature Attribution Frameworks
1. **Study Post-Hoc Explanation Methods:** Research feature attribution and model explanation frameworks to understand how they compute feature contributions and interaction effects.
2. **Design the Decoupling Analysis Framework:** Formulate a methodological plan for how you will use model explanations to mathematically or visually separate intrinsic metal properties from extrinsic processing and defect effects.

---

## 3. Design Validation Strategy & Experimental Protocol

### a. Design the Paper-Wise Validation Scheme
1. **Analyze Data Leakage Risks:** Investigate how standard train/test splitting fails when multiple rows originate from the same published study or experimental batch.
2. **Research Grouped Cross-Validation Methods:** Explore grouped splitting strategies to ensure all data points from a single paper stay together in either the training or validation split.
3. **Configure the Splitting Protocol:** Test different splitting configurations and grouping rules on your dataset to ensure each validation fold has a representative distribution of inputs and target values.

### b. Select Evaluation Metrics
1. **Research Regression Error Metrics:** Evaluate standard regression error metrics to determine which ones best capture prediction quality across the numerical scales of your targets.
2. **Research Rank and Trend Metrics:** Investigate correlation and ranking metrics to assess whether a model correctly orders contact performance even when absolute values shift between papers.
3. **Establish Model Selection Criteria:** Define the exact combination of validation metrics you will use to declare one model or feature set superior to another.

---

## 4. Model Implementation, Training & Optimization

### a. Build the Preprocessing Pipeline
1. **Implement Categorical Encoding Strategies:** Research and test methods for encoding categorical variables strictly within training folds so no validation information leaks.
2. **Implement Scaling and Imputation:** Set up feature scaling and missing-value handling rules tailored to the mathematical requirements of each candidate model family.

### b. Train Baseline and Non-Linear Models
1. **Execute Baseline Runs:** Train your statistical and simple parametric baselines across the paper-wise validation splits and record their benchmark scores.
2. **Train Default Candidate Models:** Run your shortlisted non-linear models with default settings on the grouped splits to verify pipeline functionality and establish initial performance.

### c. Perform Hyperparameter Tuning and Regularization
1. **Identify Key Hyperparameters:** Research which parameters in your chosen models control model capacity, structural complexity, subsampling, and regularization penalties.
2. **Design and Run the Tuning Search:** Research and execute a systematic hyperparameter optimization strategy evaluated strictly over your paper-wise cross-validation folds to prevent overfitting.
3. **Experiment with Domain Constraints:** Investigate whether your chosen modeling libraries allow you to enforce directional or physical constraints on specific inputs, and test whether applying them improves cross-paper generalization.

### d. Execute Symbolic Regression Discovery
1. **Select Input Variables for Equation Search:** Determine which subset of physical features and engineered variables should be fed into the symbolic regression algorithm.
2. **Run Symbolic Search Across Complexity Levels:** Execute the symbolic regression algorithm to generate a spectrum of candidate mathematical formulas across varying levels of complexity.
3. **Evaluate the Accuracy-Complexity Trade-off:** Analyze the resulting equations by comparing validation error against mathematical complexity, and select candidate formulas that balance accuracy with physical interpretability.

### e. Conduct Error and Residual Analysis
1. **Inspect Out-of-Fold Residuals:** Plot predicted versus actual values across all validation folds to identify systematic biases, poorly predicted regimes, or extreme outlier papers.
2. **Trace High-Error Predictions Back to Literature:** Examine the specific papers and experimental conditions responsible for the largest prediction errors to determine if they stem from data entry mistakes, unique unmodeled physics, or noisy characterization.

---

## 5. Interpretability, Decoupling Analysis & Regime Mapping

### a. Compute Global and Local Feature Attributions
1. **Generate Feature Attributions:** Run your chosen interpretability analysis on your best-performing validated model to calculate the contribution of every input feature to every prediction.
2. **Rank Global Feature Importance:** Aggregate the attribution scores to identify which material and interface variables have the strongest overall association with low contact resistance and low Schottky barrier height.

### b. Separate Intrinsic Metal Effects from Extrinsic Processing Effects
1. **Categorize Features by Physical Origin:** Group your model inputs into distinct physical domains separating intrinsic metal properties from extrinsic interface, defect, phase, and processing variables.
2. **Quantify Relative Domain Contributions:** Analyze the aggregated attribution scores and variance explained by each group to determine the relative weight of the metal itself versus how the contact is fabricated.
3. **Analyze Feature Interactions:** Examine multi-variable interaction plots to see how extrinsic processing conditions modify or override the effect of intrinsic metal properties.

### c. Construct the Interpretable Regime Map
1. **Select Axes for the Regime Map:** Based on your attribution and interaction analysis, choose the primary intrinsic variable(s) and primary extrinsic/processing variable(s) that best span the contact performance space.
2. **Generate Model Response Surfaces:** Evaluate your trained ML model and/or symbolic equations across a grid of these variables to map out predicted contact resistance and barrier height regimes.
3. **Overlay Experimental Data and Identify Regimes:** Plot the literature data points over your response surface, delineate distinct physical operating regimes, and verify that the map is intuitive and physically sound.

---

## 6. Synthesis, Validation of Insights & Final Deliverables

### a. Connect ML Findings Back to Semiconductor Characterization & Physics
1. **Compare ML Trends Against Theoretical Models:** Contrast your feature attributions, regime maps, and symbolic equations with established semiconductor contact theories to see where the literature data supports or contradicts textbook assumptions.
2. **Formulate Actionable Experimental Recommendations:** Deduce what your findings imply for experimentalists—identifying which variables are worth optimizing in the lab and which variables have negligible impact.
3. **Document Limitations and Dataset Gaps:** Critically evaluate where the literature dataset is sparse, biased, or inconsistent, and specify what future characterization experiments are needed to fill those gaps.

### b. Finalize Project Deliverables
1. **Package the Benchmark Dataset:** Clean and format the final extracted dataset along with a complete data dictionary and source reference list so it can serve as a reusable benchmark for the 2D electronics community.
2. **Organize Reproducible Code:** Clean, comment, and structure all data processing, validation, modeling, symbolic regression, and visualization scripts.
3. **Compile Final Report / Presentation:** Synthesize your methodology, EDA insights, paper-wise validation metrics, symbolic equations, and interpretable regime maps into your final semester submission.
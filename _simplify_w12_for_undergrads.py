from pathlib import Path
import re

path = Path(r"2026\Fall\Research Method of Data Science\W12\W12_RMDS.Rmd")
source = path.read_text(encoding="utf-8")

css_anchor = ".interpret-item p { margin:4px 0; }"
css_addition = """
.plot.compact img { max-height:315px; }
.plot-reading { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; margin:8px 0; }
.plot-reading .item { min-width:0; border-top:5px solid #851a10; background:#f8f5f3; padding:9px 13px; font-size:19px; line-height:1.25; }
.plot-reading .item.alt { border-top-color:#3a7188; background:#f3f7f8; }
.plot-reading h3 { margin:0 0 5px; color:#851a10; font-size:23px; }
.plot-reading .alt h3 { color:#2e6579; }
.plain-steps { counter-reset:plainstep; margin:8px 0; }
.plain-step { counter-increment:plainstep; display:grid; grid-template-columns:40px 1fr; gap:10px; align-items:start; border-bottom:1px solid #d7dcde; padding:9px 4px; font-size:23px; line-height:1.25; }
.plain-step::before { content:counter(plainstep); display:flex; align-items:center; justify-content:center; width:32px; height:32px; border-radius:50%; background:#851a10; color:white; font-weight:700; }
""".strip()
if ".plot-reading {" not in source:
    source = source.replace(css_anchor, css_anchor + "\n" + css_addition)


def replace_visible(title, new_title=None, body=None):
    global source
    title_re = re.escape(title)
    pattern = re.compile(rf"(?ms)(^# {title_re}\s*$)(.*?)(?=^\?\?\?\s*$)")
    match = pattern.search(source)
    if not match:
        raise RuntimeError(f"Slide not found: {title}")
    heading = f"# {new_title or title}"
    source = source[:match.start()] + heading + "\n\n" + body.strip() + "\n\n" + source[match.end():]


replace_visible(
    "Agenda",
    body="""
**Tuesday - Meeting 1**

1. Turn a research question into a regression comparison
2. Understand what changes when controls are added
3. Check patterns the model did not explain
4. Compare prediction methods on new records
5. Connect the lesson to your own project

Appendix: optional advanced models and software references.

<div class="student-note">The lesson starts with a question, builds a model, checks its weaknesses, and then asks whether it predicts new cases well.</div>
""",
)

replace_visible(
    "1. From a research question to OLS",
    new_title="1. From a research question to a regression line",
    body='<div class="section-subtitle">We begin with the outcome and comparison, then use OLS to draw the straight line that best summarizes the observed pattern.</div>',
)

replace_visible(
    "OLS turns a question into a fitted comparison",
    new_title="OLS draws the best-fitting straight line",
    body="""
**Question:** how does average MPG differ as vehicle weight changes?

**OLS** stands for *ordinary least squares*. It chooses the straight line that makes the overall prediction mistakes as small as possible.

<div class="split">
  <div class="split-panel"><h2>Fitted value</h2><p>The MPG predicted by the line for one vehicle.</p></div>
  <div class="split-panel alt"><h2>Residual</h2><p>Actual MPG minus predicted MPG. It is the vertical gap from a point to the line.</p></div>
</div>

<div class="student-note"><strong>Weight unit:</strong> the model records weight in 1,000 lb, so a change of 0.5 means 500 lb.</div>
""",
)

replace_visible(
    "2. Specification, interpretation and uncertainty",
    new_title="2. Adding controls and measuring uncertainty",
    body='<div class="section-subtitle">Adding variables changes the comparison. Confidence intervals show how precisely the adjusted comparison is estimated.</div>',
)

replace_visible(
    "A specification states the comparison",
    new_title="Adding controls changes the question",
    body="""
**Simple model:** compare MPG across vehicle weights.

**Adjusted model:** compare vehicle weights while also accounting for recorded horsepower, model year, and origin.

<div class="split">
  <div class="split-panel"><h2>What “holding fixed” means</h2><p>The model compares vehicles at the same recorded values of the included controls.</p></div>
  <div class="split-panel alt"><h2>What it does not mean</h2><p>The vehicles are not identical, and adding controls does not automatically create a causal comparison.</p></div>
</div>

<div class="student-note">The technical name for the chosen variables and equation is the <strong>model specification</strong>.</div>
""",
)

replace_visible(
    "3. Diagnostics and threats to validity",
    new_title="3. Checking model problems and research limits",
    body='<div class="section-subtitle">Model checks show patterns left unexplained. Research design determines whether the final claim is descriptive, associational, predictive, or causal.</div>',
)

replace_visible(
    "A diagnostic asks what the model missed",
    new_title="Model checks ask what the regression missed",
    body="""
| Check | Plain-language question |
|---|---|
| Residuals versus predictions | Do the mistakes form a pattern instead of a random cloud? |
| Q-Q plot of residuals | Are there unusually large mistakes in the tails? |
| Unusual predictor values (leverage) | Is a vehicle far from most others in its recorded characteristics? |
| Influence (Cook's distance) | Does one vehicle noticeably change the fitted model? |
| Data and design documentation | Could selection, missing data, or related records affect the claim? |

<div class="student-note">A warning sign tells us what to investigate. No single graph gives the entire regression a pass or fail.</div>
""",
)

replace_visible(
    "Curvature can change the fitted comparison",
    new_title="A curved line can describe the pattern better",
    body="""
<div class="plot compact"><img alt="Adjusted straight and curved fits with their residual plots" src=""" + re.search(r'(?s)# Curvature can change the fitted comparison.*?<img[^>]+src="([^"]+)"', source).group(1) + """" /></div>

<div class="plot-reading">
  <div class="item">
    <h3>Left: fitted MPG</h3>
    <p>The straight line assumes the same weight-MPG change everywhere. The curved line allows the pattern to flatten or bend for lighter and heavier vehicles.</p>
  </div>
  <div class="item alt">
    <h3>Right: prediction mistakes</h3>
    <p>A good residual plot looks like a loose cloud around zero. A visible curve means the model is still missing a systematic pattern.</p>
  </div>
</div>

<div class="student-note"><strong>Interpretation:</strong> the curved model follows the training pattern better, but this alone does not prove a causal effect or guarantee good prediction for new vehicles.</div>
""",
)

replace_visible(
    "A quadratic has a changing slope",
    new_title="A curved model has no single weight effect",
    body="""
<div class="split">
  <div class="split-panel">
    <h2>Straight-line model</h2>
    <p>Uses one weight slope for every vehicle. An additional 1,000 lb has the same fitted MPG difference across the entire graph.</p>
  </div>
  <div class="split-panel alt">
    <h2>Curved model</h2>
    <p>The fitted MPG difference depends on the starting weight. We therefore report the slope at a specific weight.</p>
  </div>
</div>

<div class="result-band"><strong>Near 3,000 lb:</strong> an additional 1,000 lb is associated with about <strong>6.50 fewer MPG</strong>, after accounting for horsepower, model year, and origin.</div>

<div class="student-note"><strong>“Local slope” means near that weight.</strong> It should not be presented as one universal effect for every light and heavy vehicle.</div>
""",
)

replace_visible(
    "HC3 changes uncertainty, not coefficients",
    new_title="HC3 gives safer uncertainty when the scatter is uneven",
    body="""
Regression mistakes may be tightly grouped for some vehicles and widely spread for others. Ordinary standard errors can then be too optimistic.

<div class="split">
  <div class="split-panel">
    <h2>What stays the same</h2>
    <p>The coefficient estimates and the fitted regression line or curve.</p>
  </div>
  <div class="split-panel alt">
    <h2>What HC3 recalculates</h2>
    <p>Standard errors, confidence intervals, t-statistics, and p-values.</p>
  </div>
</div>

<div class="caution"><strong>HC3 cannot fix the research design.</strong> It does not solve missing important variables, reverse causality, related observations, or the wrong curve.</div>

<div class="student-note">Think of HC3 as a more cautious way to report uncertainty when the residual plot has uneven spread.</div>
""",
)

replace_visible(
    "Common threats begin in the research design",
    new_title="Regression can mislead for reasons beyond the equation",
    body="""
| Possible problem | Why it matters |
|---|---|
| Important factor is missing | Weight may stand in for another vehicle characteristic that also affects MPG |
| Measurement is imperfect | Recorded horsepower or MPG may not fully represent the concept of interest |
| Available records are selected | Historical vehicles may differ from modern vehicles or the population we want to discuss |
| Some records are related | Similar models from one manufacturer may not provide fully independent evidence |
| The line has the wrong shape | A straight line may hide curvature or other patterns |

<div class="student-note">Better software cannot remove these problems automatically. Researchers must use subject knowledge, documentation, and careful claims.</div>
""",
)

replace_visible(
    "Influence challenge — pairs, 4 minutes",
    new_title="Which vehicle strongly affects the fitted model?",
    body="""
""" + re.search(r'(?s)# Influence challenge — pairs, 4 minutes(.*?)(?=<div class="student-note">)', source).group(1).strip() + """

<div class="plot-reading">
  <div class="item"><h3>Farther right</h3><p>The vehicle has an unusual combination of recorded predictors. This is called <strong>high leverage</strong>.</p></div>
  <div class="item alt"><h3>Larger bubble</h3><p>The vehicle changes the fitted model more strongly. Bubble size represents <strong>Cook's distance</strong>.</p></div>
</div>

<div class="student-note">Investigate the original record and context. An influential vehicle can be valid evidence that the model is too simple.</div>
""",
)

replace_visible(
    "A robustness check has a specific purpose",
    new_title="A sensitivity check asks whether one record drives the result",
    body="""
At 3,000 lb, the curved model gives:

| Analysis | Estimated local slope |
|---|---:|
| Use all 294 training vehicles | -6.50 MPG per 1,000 lb |
| Temporarily leave out the most influential vehicle | -6.59 MPG per 1,000 lb |

The estimate changes very little, so this one vehicle does not drive the result.

<div class="student-note">This answers one narrow question about sensitivity to one record. It does not prove that the model, sample, or causal interpretation is correct.</div>
""",
)

replace_visible(
    "4. Prediction, Ridge and Lasso",
    new_title="4. Predicting new vehicles",
    body='<div class="section-subtitle">Prediction asks how close the model comes to actual MPG for vehicles that were not used to build or tune it.</div>',
)

replace_visible(
    "Many related features can overfit",
    new_title="A model can learn the training data too closely",
    body="""
Weight, engine size, cylinder count, and horsepower are related.

Adding many squared terms and combinations makes the model more flexible. It can then learn small quirks of the training records instead of a pattern that repeats.

<div class="definition"><strong>Overfitting:</strong> very good performance on the training data but weaker prediction for new records.</div>

<div class="student-note"><strong>Regularization</strong> is a method that limits extreme complexity so predictions can be more stable.</div>
""",
)

replace_visible(
    "OLS, Ridge and Lasso use different penalties",
    new_title="Three ways to control model complexity",
    body="""
| Method | Plain-language idea | What students should remember |
|---|---|---|
| OLS | Fits the training data without a penalty | Clear baseline, but flexible versions may overfit |
| Ridge | Pulls large coefficients toward zero | Often stabilizes prediction when predictors overlap |
| Lasso | Pulls coefficients toward zero and can set some exactly to zero | Produces a simpler selected set of features |

<div class="student-note">Ridge and Lasso need predictors on comparable scales. Their selected coefficients support prediction, not automatic causal importance.</div>
""",
)

replace_visible(
    "Validation separates tuning from evaluation",
    new_title="Choose the model without looking at the final test answers",
    body="""
<div class="plain-steps">
  <div class="plain-step">Keep 100 test vehicles aside.</div>
  <div class="plain-step">Use only the training vehicles to compare settings through repeated train-and-check splits. This is <strong>cross-validation</strong>.</div>
  <div class="plain-step">Choose one model and fit it using all training vehicles.</div>
  <div class="plain-step">Open the test set once for the final prediction check.</div>
</div>

<div class="student-note">All data preparation must be learned separately inside each training split. This prevents <strong>data leakage</strong>, where the model indirectly sees validation answers.</div>
""",
)

replace_visible(
    "Lasso makes a visible choice",
    new_title="Cross-validation chooses the Lasso setting",
    body="""
""" + re.search(r'(?s)# Lasso makes a visible choice(.*?)(?=<div class="student-note">)', source).group(1).strip() + """

<div class="plot-reading">
  <div class="item"><h3>Horizontal axis</h3><p>Penalty strength, called <strong>alpha</strong>. Moving right applies stronger shrinkage.</p></div>
  <div class="item alt"><h3>Vertical axis</h3><p>Average prediction error in training cross-validation. Lower RMSE is better.</p></div>
</div>

<div class="student-note">The dashed line marks the alpha with the lowest cross-validation error in this grid. A nearby value may perform almost the same.</div>
""",
)

replace_visible(
    "5. Your project and Thursday preparation",
    new_title="5. Connect regression to your project",
    body='<div class="section-subtitle">Choose a method only after defining your outcome, unit of observation, research aim, and main limitation.</div>',
)

replace_visible(
    "The research question selects the evidence",
    new_title="Different questions need different evidence",
    body="""
| Your aim | Evidence to report |
|---|---|
| Describe an adjusted association | Coefficient or predicted contrast, interval, and model checks |
| Predict new cases | Training/test plan, a simple baseline, prediction errors, and limitations |
| Explain a cause | A credible reason why groups differ in X but not in other causes, plus estimation and uncertainty |
| Understand experiences or meanings | Themes, supporting evidence, interpretation, and trustworthiness |

<div class="student-note">More controls, more equations, or a higher R-squared do not automatically make a causal claim credible.</div>
""",
)

replace_visible(
    "3. Functional form and residuals — 12 minutes",
    new_title="3. Check the curve and prediction mistakes - 12 minutes",
    body="""
Run notebook **3**.

Compare the straight and curved fitted lines, then inspect the residual plots.

1. Describe one remaining visual pattern in plain language.
2. Explain the fitted weight-MPG relationship near **3,000 lb**.
3. State what HC3 changes and one research problem it cannot fix.

Compare your observations with a neighbour.

<div class="student-note">A residual is actual MPG minus predicted MPG. Look for a random cloud around zero rather than a curve or widening funnel.</div>
""",
)

replace_visible(
    "4. Influence and robustness — 10 minutes",
    new_title="4. Investigate an influential vehicle - 10 minutes",
    body="""
Run notebook **4**.

Find the vehicle with the largest Cook's distance and inspect its original values and name.

Compare the estimate using all records with the estimate after temporarily leaving out this one vehicle.

**Write:** “This check tells us ... It cannot prove ...”

Keep a valid unusual record in the main analysis unless source evidence supports a correction.

<div class="student-note">The goal is not to remove inconvenient data. The goal is to understand why a record matters and whether the conclusion depends on it.</div>
""",
)

replace_visible(
    "5. Prediction pipelines — 18 minutes",
    new_title="5. Compare prediction methods - 18 minutes",
    body="""
Run notebook **5**.

Use training cross-validation to compare the mean baseline, OLS, Ridge, and Lasso.

Before opening the test results, record:

- which model has the lowest training cross-validation error
- the Lasso penalty setting and number of retained features
- where missing values and scaling are learned

Explain why a retained Lasso feature is useful for prediction but not proof of causality.

<div class="student-note">The notebook uses a <strong>pipeline</strong>: an ordered set of preparation and modelling steps repeated correctly inside each training split.</div>
""",
)

replace_visible(
    "The full lab comparison in numbers",
    new_title="Test results compare prediction accuracy",
    body="""
| Model | RMSE | MAE | Test R² |
|---|---:|---:|---:|
| Mean baseline | 7.985 | 6.371 | -0.056 |
| Linear OLS | 3.635 | 2.863 | 0.781 |
| Expanded OLS | 3.077 | 2.275 | 0.843 |
| Ridge | 3.027 | 2.295 | 0.848 |
| Lasso | 3.028 | 2.293 | 0.848 |

<div class="plot-reading">
  <div class="item"><h3>MAE</h3><p>Average absolute miss in MPG. A value near 2.3 means predictions miss by about 2.3 MPG on average.</p></div>
  <div class="item alt"><h3>RMSE</h3><p>Also measures MPG error but gives extra weight to large misses. Lower is better.</p></div>
</div>

<div class="student-note">Lasso was selected using training cross-validation. Ridge is only 0.001 lower on this test RMSE, far too small for a strong claim that it is universally better.</div>
""",
)

replace_visible(
    "Lasso coefficients need careful interpretation",
    new_title="Lasso coefficients describe a prediction system",
    body="""
""" + re.search(r'(?s)# Lasso coefficients need careful interpretation(.*?)(?=<div class="student-note">)', source).group(1).strip() + """

<div class="student-note">The model created squares and interactions, then rescaled them. A large bar means the feature contributes to this prediction formula; it does not rank scientific importance or establish a cause.</div>
""",
)

replace_visible(
    "A log outcome changes the scale",
    new_title="Optional: logging MPG changes the meaning of coefficients",
    body="""
Taking the logarithm of MPG changes the question from an MPG difference to an approximate percentage difference.

**Simple interpretation for a small coefficient:** a one-unit increase in X is associated with roughly **100 × b percent** change in fitted MPG, holding other included variables fixed.

For larger changes, software should calculate the exact percentage using the exponential transformation.

<div class="student-note">Use a log outcome only when a percentage interpretation fits the research question. Do not choose it simply because it looks more technical.</div>
""",
)

replace_visible(
    "Interactions allow a changing association",
    new_title="Optional: an interaction allows the slope to change",
    body="""
The model allows the weight-MPG association to differ by model year.

| Model year | Fitted MPG difference for 1,000 lb greater weight |
|---|---:|
| 1972 | -3.84 MPG |
| 1976 | -5.65 MPG |
| 1980 | -7.47 MPG |

<div class="student-note"><strong>Interaction:</strong> the association of one variable depends on another variable. Interpret the combined slope at meaningful values, not one coefficient by itself.</div>
""",
)

replace_visible(
    "Elastic Net combines two penalties",
    new_title="Optional: Elastic Net blends Ridge and Lasso",
    body="""
Elastic Net combines the two regularization ideas:

- Ridge-style shrinkage can stabilize groups of related predictors.
- Lasso-style shrinkage can set some coefficients to zero.

Training cross-validation chooses both the overall penalty strength and the balance between the two styles.

<div class="student-note">Elastic Net is another prediction option, not evidence that selected variables are causal.</div>
""",
)

replace_visible(
    "Three meanings of “robust”",
    new_title="The word “robust” can mean different things",
    body="""
| Term | Plain-language meaning |
|---|---|
| HC3 robust standard errors | Keep the OLS estimates but report uncertainty that better handles uneven residual spread |
| Huber robust regression | Fit the line while reducing the effect of very large residuals |
| Robustness or sensitivity check | Change one reasonable analysis choice and see whether the conclusion changes |

<div class="student-note">Always name the specific problem being addressed. “Robust” never means that every research problem has been solved.</div>
""",
)

replace_visible(
    "Other outcomes call for other models",
    new_title="The outcome type guides the model choice",
    body="""
| Outcome | Possible starting model |
|---|---|
| Yes/no event | Logistic regression |
| Number of events | A count model such as Poisson regression |
| Typical or median outcome | Quantile regression |
| Repeated observations of countries or firms | A model that accounts for repeated records and dependence |

<div class="student-note">These are starting points, not automatic choices. Students should justify the model using the outcome, research design, and claim.</div>
""",
)

path.write_text(source, encoding="utf-8")

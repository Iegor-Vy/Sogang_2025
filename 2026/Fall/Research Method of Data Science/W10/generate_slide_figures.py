"""Regenerate all Week 10 figures from the notebook's embedded WDI snapshot."""
from pathlib import Path
import json, os
os.environ.setdefault("MPLBACKEND", "Agg")

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "slide_figures"
OUT.mkdir(exist_ok=True)
nb_path = ROOT / "W10_RMDS_Preparation_and_EDA.ipynb"
ns = {"__name__": "__slide_figure_generation__"}
for cell in json.loads(nb_path.read_text(encoding="utf-8"))["cells"]:
    if cell.get("cell_type") != "code": continue
    source = "".join(cell.get("source", []))
    exec(compile(source, nb_path.name, "exec"), ns)
    if "Internet use in six selected countries" in source: break

np, pd, plt, sns = (ns[x] for x in ("np", "pd", "plt", "sns"))
panel, latest, complete, endpoints = (ns[x] for x in ("panel", "latest", "complete", "endpoints"))
YEARS, VALUES, SHORT, report = (ns[x] for x in ("YEARS", "VALUES", "SHORT", "report_2023"))
BURGUNDY, TEAL, GRAY, GRID = "#851a10", "#3a7188", "#9aa3a8", "#d9d9d9"

plt.rcParams.update({"font.size": 13, "axes.titlesize": 18, "axes.titleweight": "bold",
 "axes.labelsize": 14, "xtick.labelsize": 12, "ytick.labelsize": 12,
 "legend.fontsize": 12, "figure.titlesize": 20})

def finish(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight", facecolor="white", dpi=180)
    plt.close(fig)

def style(ax, xpad=16, ypad=12, grid=True):
    ax.xaxis.labelpad, ax.yaxis.labelpad = xpad, ypad
    if grid:
        ax.grid(True, color=GRID, linewidth=.8); ax.set_axisbelow(True)

# 1. Korea time series
kor = panel.loc[panel.country_code.eq("KOR")].set_index("year").reindex(YEARS)
fig, ax = plt.subplots(figsize=(9, 4.4))
ax.plot(YEARS, kor.internet_pct, color=BURGUNDY, linewidth=2.8, marker="o", markersize=4)
for x, y, offset, align in [(YEARS[0], kor.internet_pct.iloc[0], (8, 8), "left"),
                             (YEARS[-1], kor.internet_pct.iloc[-1], (-8, -18), "right")]:
    ax.annotate(f"{y:.1f}%", (x, y), xytext=offset, textcoords="offset points",
                fontsize=13, ha=align, color=BURGUNDY, weight="bold")
ax.set(title="Internet use in Korea, 2000-2023", xlabel="Year",
       ylabel="Individuals using the internet (%)", ylim=(0, 100)); style(ax)
fig.subplots_adjust(bottom=.24)
fig.text(.12, .025, "Source: World Bank WDI, IT.NET.USER.ZS; retrieved 31 Oct 2026.", fontsize=10)
finish(fig, "01_korea_internet.png")

# 2. Country bars
codes = ["KOR", "VNM", "UKR", "USA", "IND", "ZAF"]
focus = latest.loc[latest.country_code.isin(codes), ["country_code", "country", "life_expectancy"]].dropna().sort_values("life_expectancy")
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.barh(focus.country, focus.life_expectancy, color=[BURGUNDY if x == "KOR" else TEAL for x in focus.country_code])
for i, (value, code) in enumerate(zip(focus.life_expectancy, focus.country_code)):
    ax.text(value + .6, i, f"{value:.1f}", va="center", fontsize=12, weight="bold" if code == "KOR" else "normal")
ax.set(xlabel="Life expectancy at birth (years)", title=f"Life expectancy in selected countries, 2023 (n={len(focus)})", xlim=(0, 100)); style(ax)
fig.subplots_adjust(bottom=.24)
fig.text(.12, .025, "Source: World Bank WDI, SP.DYN.LE00.IN; retrieved 31 Oct 2026.", fontsize=10)
finish(fig, "02_life_bars.png")

# 3. GDP histograms
gdp = latest.gdp_pc_ppp.dropna(); fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
axes[0].hist(gdp, bins=7, color=TEAL, edgecolor="white")
axes[0].set(xlabel="GDP per capita, PPP\n(constant 2021 international $)", ylabel="Country count", title=f"Original scale (n={len(gdp)})")
axes[1].hist(np.log(gdp), bins=7, color=TEAL, edgecolor="white")
axes[1].set(xlabel="Natural log of GDP per capita, PPP", ylabel="Country count", title="Transformed scale")
for ax in axes: style(ax, xpad=18)
fig.text(.5, .91, "natural-log transformation  ->", color=BURGUNDY, ha="center", fontsize=13, weight="bold")
fig.suptitle("GDP per capita distribution, selected countries, 2023", y=1.04, weight="bold"); fig.tight_layout()
finish(fig, "03_gdp_histograms.png")

# 4. GDP-life expectancy scatterplot
d = latest.dropna(subset=["gdp_pc_ppp", "life_expectancy"]); hi = d.country_code.isin(["KOR", "VNM", "UKR", "USA", "IND", "AFG"])
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(d.loc[~hi, "gdp_pc_ppp"], d.loc[~hi, "life_expectancy"], color=GRAY, s=52, alpha=.75, label="Other selected countries")
ax.scatter(d.loc[hi, "gdp_pc_ppp"], d.loc[hi, "life_expectancy"], color=BURGUNDY, s=70, alpha=.9, label="Labelled examples")
for _, row in d.loc[hi].iterrows(): ax.annotate(row.country_code, (row.gdp_pc_ppp, row.life_expectancy), xytext=(5, 5), textcoords="offset points", fontsize=12, color=BURGUNDY, weight="bold")
ax.set_xscale("log"); ax.set(xlabel="GDP per capita, PPP\n(constant 2021 international $, log axis)", ylabel="Life expectancy at birth (years)", title=f"GDP and life expectancy, selected countries, 2023 (n={len(d)})")
ax.legend(frameon=False, loc="lower right"); style(ax, xpad=18); fig.tight_layout()
finish(fig, "04_gdp_life_scatter.png")

# 5. Small multiples
names = latest.set_index("country_code").country.to_dict(); fig, axes = plt.subplots(2, 3, figsize=(11, 6.3), sharex=True, sharey=True)
for ax, code in zip(axes.flat, codes):
    d = panel.loc[panel.country_code.eq(code)].set_index("year").reindex(YEARS)
    ax.plot(YEARS, d.internet_pct, color=TEAL, linewidth=2.4); ax.set(title=f"{code} - {names[code]}", ylim=(0, 100)); style(ax)
fig.supxlabel("Year", y=.01); fig.supylabel("Internet use (% of population)", x=.01)
fig.suptitle("Internet use in six selected countries, 2000-2023\nCommon 0-100 scale in every panel", y=1.04, weight="bold"); fig.tight_layout()
finish(fig, "07_small_multiples.png")

# 6. Correlation heatmap
corr, n = report["correlation"], report["pairwise_n"]; labels = corr.copy().astype(object)
for r in corr.index:
    for c in corr.columns: labels.loc[r, c] = f"{corr.loc[r,c]:.2f}\nN={n.loc[r,c]}" if pd.notna(corr.loc[r,c]) else ""
fig, ax = plt.subplots(figsize=(7.5, 5.5)); mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(corr, mask=mask, annot=labels, fmt="", cmap="vlag", vmin=-1, vmax=1, center=0, xticklabels=[SHORT[x] for x in VALUES], yticklabels=[SHORT[x] for x in VALUES], ax=ax, linewidths=1, linecolor="white", annot_kws={"fontsize": 13})
ax.set(title="Pairwise Pearson correlations\nSelected countries, 2023"); ax.tick_params(axis="x", rotation=25, pad=8); ax.tick_params(axis="y", rotation=0); fig.tight_layout()
finish(fig, "05_correlation_heatmap.png")

# 7. Missingness map
miss = panel.pivot(index="country_code", columns="year", values="internet_pct").isna().astype(int)
fig, ax = plt.subplots(figsize=(11, 7)); sns.heatmap(miss, cmap=["#eef3f5", BURGUNDY], vmin=0, vmax=1, cbar=False, ax=ax)
ax.set(title="Internet-use data availability, 2000-2023\nBurgundy cells indicate missing values", xlabel="Year", ylabel="Country code")
ax.set_xticks(np.arange(.5, len(YEARS), 4), labels=YEARS[::4], rotation=0); style(ax, xpad=18, grid=False); fig.tight_layout()
finish(fig, "06_missingness_map.png")

# 8. Scatterplot matrix
d = complete[VALUES].copy(); d["Log GDP per capita"] = np.log(d.pop("gdp_pc_ppp")); d = d.rename(columns={"life_expectancy":"Life expectancy", "internet_pct":"Internet use (%)"})
g = sns.pairplot(d, diag_kind="hist", height=3, plot_kws={"alpha":.8, "s":55, "color":TEAL}, diag_kws={"bins":7, "color":TEAL})
for ax in g.axes.flat:
    if ax is not None: style(ax, xpad=14, grid=False)
g.fig.suptitle(f"Relationships among 2023 measures\nComplete-case countries (n={len(d)})", y=1.04, weight="bold"); g.fig.tight_layout()
finish(g.fig, "08_pairplot.png")

# 9. Endpoint change and ECDF
chg = endpoints["change_pp_2000_2023"].dropna().sort_values(); fig, axes = plt.subplots(1, 2, figsize=(12, 7))
axes[0].barh(chg.index, chg.values, color=TEAL); axes[0].set(title=f"Internet-use change, 2000-2023\nBoth endpoints observed (n={len(chg)})", xlabel="Change (percentage points)")
sns.ecdfplot(data=latest, x="gdp_pc_ppp", ax=axes[1], color=BURGUNDY, linewidth=2.5)
axes[1].set(title=f"GDP per capita distribution, 2023\nObserved countries (n={latest.gdp_pc_ppp.notna().sum()})", xlabel="GDP per capita, PPP\n(constant 2021 international $)", ylabel="Share of observed countries")
for ax in axes: style(ax, xpad=18)
fig.tight_layout(w_pad=3); finish(fig, "09_changes_ecdf.png")
print("Generated", len(list(OUT.glob("*.png"))), "slide figures in", OUT)

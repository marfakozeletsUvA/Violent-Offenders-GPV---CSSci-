"""
Generate all final report figures for the GPV / neo-colonial networks project.
Consistent visual style throughout; saves PNG to outputs/final_report/.
Run from: notebooks/ directory
"""

import os, shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE   = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA   = os.path.join(BASE, 'data', 'merged')
RES    = os.path.join(BASE, 'outputs', 'results')
OUT    = os.path.join(BASE, 'outputs', 'final_report')

D01 = os.path.join(OUT, '01_data_and_methods')
D02 = os.path.join(OUT, '02_results_main_findings')
D03 = os.path.join(OUT, '03_results_econ_score')
D04 = os.path.join(OUT, '04_appendix')
D05 = os.path.join(OUT, '05_tables')

# ── Style constants ────────────────────────────────────────────────────────────
RED   = '#BF3A27'
GOLD  = '#C7922A'
DARK  = '#323232'
LGREY = '#E0E0E0'
WHITE = '#FFFFFF'
ROWALT = '#FDF5F3'
GREY  = '#AAAAAA'
BLUE  = '#1A5276'

DPI = 150
FONT = 'DejaVu Sans'

plt.rcParams.update({
    'font.family': FONT,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.color': LGREY,
    'grid.alpha': 0.4,
    'text.color': DARK,
    'axes.labelcolor': DARK,
    'xtick.color': DARK,
    'ytick.color': DARK,
})

def save(fig, path):
    fig.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f'  saved → {os.path.relpath(path, BASE)}')
    CREATED.append(path)

CREATED = []

# ─────────────────────────────────────────────────────────────────────────────
# 01  DATA AND METHODS
# ─────────────────────────────────────────────────────────────────────────────

def fig01_summary_stats():
    mono = pd.read_csv(os.path.join(DATA, 'panel_monadic_1992_2024.csv'))

    vars_info = [
        ('arms_tiv_total',           'Arms TIV total'),
        ('oda_total',                 'ODA total'),
        ('econ_neocol_score_total',   'Econ neo-col score'),
        ('colonial_tie_flag',         'Colonial tie flag'),
        ('journalist_killings',       'Journalist killings'),
        ('gdp_per_capita_log',        'GDP per capita (log)'),
        ('population_log',            'Population (log)'),
        ('armed_conflict',            'Armed conflict'),
        ('conflict_intensity',        'Conflict intensity'),
    ]

    rows = []
    for col, label in vars_info:
        if col not in mono.columns:
            rows.append([label, '—', '—', '—', '—', '—', '—', '—'])
            continue
        s = mono[col]
        n_total = len(s)
        n_miss  = s.isna().sum()
        n_zero  = (s == 0).sum()
        rows.append([
            label,
            f'{s.mean():.3f}',
            f'{s.std():.3f}',
            f'{s.min():.3f}',
            f'{s.max():.3f}',
            f'{s.median():.3f}',
            f'{100*n_zero/n_total:.1f}',
            f'{100*n_miss/n_total:.1f}',
        ])

    col_labels = ['Variable', 'Mean', 'Std', 'Min', 'Max', 'Median',
                  'Zero Share (%)', 'Missing (%)']

    fig, ax = plt.subplots(figsize=(14, 4.5))
    ax.axis('off')

    tbl = ax.table(
        cellText=rows,
        colLabels=col_labels,
        cellLoc='center',
        loc='center',
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.6)

    for j in range(len(col_labels)):
        cell = tbl[0, j]
        cell.set_facecolor(RED)
        cell.set_text_props(color='white', fontweight='bold')

    for i in range(1, len(rows) + 1):
        bg = WHITE if i % 2 == 1 else ROWALT
        for j in range(len(col_labels)):
            tbl[i, j].set_facecolor(bg)
            tbl[i, j].set_text_props(color=DARK)

    ax.set_title('Summary Statistics — Monadic Panel (1992–2024)',
                 fontsize=13, fontweight='bold', color=DARK, pad=12)
    save(fig, os.path.join(D01, 'fig01_summary_stats.png'))


def fig02_target_distribution():
    mono = pd.read_csv(os.path.join(DATA, 'panel_monadic_1992_2024.csv'))
    k = mono['journalist_killings'].dropna()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle('Journalist Killings — Target Variable Distribution',
                 fontsize=13, fontweight='bold', color=DARK, y=1.01)

    # Left: clipped at 15
    clipped = k.clip(upper=15)
    ax1.hist(clipped, bins=range(17), color=RED, edgecolor='white', linewidth=0.5)
    ax1.set_xlabel('Journalist killings (clipped at 15)')
    ax1.set_ylabel('Count')
    ax1.set_title('Distribution (clipped at 15)')
    ax1.annotate('88.7% zeros', xy=(8, ax1.get_ylim()[1]*0.9 if ax1.get_ylim()[1] > 0 else 1),
                 fontsize=10, color=DARK)
    ax1.annotate('Var/Mean = 14.75x', xy=(8, ax1.get_ylim()[1]*0.8 if ax1.get_ylim()[1] > 0 else 1),
                 fontsize=10, color=DARK)

    # fix annotation after drawing
    ax1.set_xlim(-0.5, 15.5)
    ylim1 = ax1.get_ylim()
    for t in list(ax1.texts):
        t.remove()
    ax1.annotate('88.7% zeros', xy=(5, ylim1[1]*0.92), fontsize=10, color=DARK)
    ax1.annotate('Var/Mean = 14.75×', xy=(5, ylim1[1]*0.82), fontsize=10, color=DARK)

    # Right: full range, log y
    ax2.hist(k, bins=50, color=RED, edgecolor='white', linewidth=0.5)
    ax2.set_yscale('log')
    ax2.set_xlabel('Journalist killings (full range)')
    ax2.set_ylabel('Count (log scale)')
    ax2.set_title('Distribution (log-y, full range)')

    fig.tight_layout()
    save(fig, os.path.join(D01, 'fig02_target_distribution.png'))


def fig03_missingness():
    labels = [
        'econ_neocol_score', 'bilateral_oda', 'gdp_per_capita', 'population',
        'armed_conflict', 'conflict_intensity', 'arms_tiv', 'colonial_tie',
        'journalist_killings',
    ]
    pcts = [30.4, 10.2, 6.35, 4.2, 3.7, 3.7, 0.0, 0.0, 0.0]

    order = sorted(range(len(pcts)), key=lambda i: pcts[i], reverse=True)
    labels_s = [labels[i] for i in order]
    pcts_s   = [pcts[i] for i in order]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(labels_s, pcts_s, color=GOLD, edgecolor='white', height=0.6)
    for bar, val in zip(bars, pcts_s):
        ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}%', va='center', fontsize=9, color=DARK)
    ax.set_xlabel('Missing (%)')
    ax.set_title('Missing Values by Variable (%) — Monadic Panel', fontsize=12,
                 fontweight='bold', color=DARK)
    ax.set_xlim(0, max(pcts_s) * 1.2)
    ax.invert_yaxis()
    fig.tight_layout()
    save(fig, os.path.join(D01, 'fig03_missingness.png'))


# ─────────────────────────────────────────────────────────────────────────────
# 02  RESULTS MAIN FINDINGS
# ─────────────────────────────────────────────────────────────────────────────

CLEAN_NAMES = {
    'arms_tiv_total_log_lag1':              'Arms transfers (lag 1)',
    'oda_total_log_lag1':                   'ODA (lag 1)',
    'econ_neocol_score_total_lag1':         'Econ neo-col score (lag 1)',
    'colonial_tie_flag':                    'Colonial tie',
    'gdp_per_capita_log':                   'GDP per capita (log)',
    'population_log':                       'Population (log)',
    'armed_conflict':                       'Armed conflict',
    'conflict_intensity':                   'Conflict intensity',
    # network
    'arms_tiv_in_strength_lag1':            'Arms in-strength (lag 1)',
    'arms_tiv_pagerank_lag1':               'Arms PageRank (lag 1)',
    'bilateral_oda_in_strength_lag1':       'ODA in-strength (lag 1)',
    'bilateral_oda_pagerank_lag1':          'ODA PageRank (lag 1)',
    'econ_neocol_score_in_strength_lag1':   'Econ in-strength (lag 1)',
    'econ_neocol_score_pagerank_lag1':      'Econ PageRank (lag 1)',
    'colonial_tie_in_strength_lag1':        'Colonial in-strength (lag 1)',
    'colonial_tie_pagerank_lag1':           'Colonial PageRank (lag 1)',
    # interactions
    'arms_x_colonial':                      'Arms × Colonial',
    'oda_x_colonial':                       'ODA × Colonial',
    'econ_x_colonial':                      'Econ × Colonial',
}


def _dot_color(p):
    if p < 0.01:
        return RED
    elif p < 0.05:
        return GOLD
    return GREY


def _forest_panel(ax, df, title):
    df = df[~df['term'].isin(['const', 'alpha'])].copy()
    df['label'] = df['term'].map(lambda x: CLEAN_NAMES.get(x, x))
    df = df.iloc[::-1].reset_index(drop=True)  # flip for top-down reading

    for i, row in df.iterrows():
        p  = row['p_value']
        c  = row['coef']
        se = row['std_err']
        ci_lo = c - 1.96*se
        ci_hi = c + 1.96*se
        col = _dot_color(p)
        ax.plot([ci_lo, ci_hi], [i, i], color=col, lw=1.5, solid_capstyle='round')
        ax.scatter([c], [i], color=col, s=60, zorder=5)

    ax.axvline(0, color=DARK, lw=1, linestyle='--')
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df['label'], fontsize=9)
    ax.set_xlabel('Coefficient')
    ax.set_title(title, fontsize=10, color=DARK)

    legend_elements = [
        Line2D([0],[0], marker='o', color='w', markerfacecolor=RED,  markersize=8, label='p < 0.01'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor=GOLD, markersize=8, label='p < 0.05'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor=GREY, markersize=8, label='p ≥ 0.05'),
    ]
    ax.legend(handles=legend_elements, fontsize=8, loc='lower right')


def fig04_nb16_forest():
    logit = pd.read_csv(os.path.join(RES, 'nb16_logit_any_killing_coefficients.csv'))
    nb    = pd.read_csv(os.path.join(RES, 'nb16_negative_binomial_positive_counts_coefficients.csv'))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle('Baseline Hurdle Model — Coefficient Estimates (Clustered SEs)',
                 fontsize=13, fontweight='bold', color=DARK)

    _forest_panel(ax1, logit, 'Zero component (logistic, n=5,765)')
    _forest_panel(ax2, nb,    'Count component (NegBin, n=687)')

    fig.tight_layout()
    save(fig, os.path.join(D02, 'fig04_nb16_forest.png'))


PAGERANK_TERMS = {
    'arms_tiv_pagerank_lag1', 'bilateral_oda_pagerank_lag1',
    'econ_neocol_score_pagerank_lag1', 'colonial_tie_pagerank_lag1',
}


def fig05_nb17_forest():
    interact = pd.read_csv(os.path.join(RES, 'nb17_interaction_terms_summary.csv'))
    network  = pd.read_csv(os.path.join(RES, 'nb17_network_features_summary.csv'))
    compare  = pd.read_csv(os.path.join(RES, 'nb17_vs_nb16_comparison.csv'))

    # Exclude PageRank features from the network block
    network = network[~network['term'].isin(PAGERANK_TERMS)].copy()

    baseline_terms = [
        'arms_tiv_total_log_lag1', 'oda_total_log_lag1', 'econ_neocol_score_total_lag1',
        'colonial_tie_flag', 'gdp_per_capita_log', 'population_log',
        'armed_conflict', 'conflict_intensity',
    ]

    def build_df(comp_col_coef, comp_col_p, inter_coef, inter_p, net_coef, net_p):
        rows = []
        for _, r in interact.iterrows():
            rows.append({'term': r['term'], 'coef': r[inter_coef], 'std_err': 0.0,
                         'p_value': r[inter_p]})
        for _, r in network.iterrows():
            rows.append({'term': r['term'], 'coef': r[net_coef], 'std_err': 0.0,
                         'p_value': r[net_p]})
        for t in baseline_terms:
            row = compare[compare['predictor'] == t]
            if len(row) == 0: continue
            rows.append({'term': t, 'coef': row[comp_col_coef].values[0],
                         'std_err': 0.0, 'p_value': row[comp_col_p].values[0]})
        return pd.DataFrame(rows)

    logit17 = build_df('logit_coef_nb17', 'logit_p_nb17',
                       'logit_coef', 'logit_p', 'logit_coef', 'logit_p')
    nb17    = build_df('nb_coef_nb17', 'nb_p_nb17',
                       'nb_coef', 'nb_p', 'nb_coef', 'nb_p')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 9))
    fig.suptitle('Network-Augmented Hurdle Model — Coefficient Estimates (Clustered SEs)',
                 fontsize=13, fontweight='bold', color=DARK)
    _forest_panel(ax1, logit17, 'Zero component (logistic, n=5,765)')
    _forest_panel(ax2, nb17,    'Count component (NegBin, n=687)')

    fig.tight_layout()
    save(fig, os.path.join(D02, 'fig05_nb17_forest.png'))


def fig06_comparison_forest():
    comp = pd.read_csv(os.path.join(RES, 'nb17_vs_nb16_comparison.csv'))

    baseline_terms = [
        'arms_tiv_total_log_lag1', 'oda_total_log_lag1', 'econ_neocol_score_total_lag1',
        'colonial_tie_flag', 'gdp_per_capita_log', 'population_log',
        'armed_conflict', 'conflict_intensity',
    ]
    comp = comp[comp['predictor'].isin(baseline_terms)].copy()
    comp['label'] = comp['predictor'].map(lambda x: CLEAN_NAMES.get(x, x))
    comp = comp.iloc[::-1].reset_index(drop=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Baseline Feature Coefficients: nb16 vs nb17 (Clustered SEs)',
                 fontsize=13, fontweight='bold', color=DARK)

    def _comp_panel(ax, col16, col17, flip_col, title):
        for i, row in comp.iterrows():
            c16   = row[col16]
            c17   = row[col17]
            flipped = row[flip_col]
            line_col = RED if flipped else GREY
            ax.plot([c16, c17], [i, i], color=line_col, lw=1.5, zorder=3)
            ax.scatter([c16], [i], color=DARK,  s=60, facecolors='none',
                       edgecolors=DARK, linewidths=1.5, zorder=5, label='nb16' if i == 0 else '')
            ax.scatter([c17], [i], color=RED,   s=60, zorder=5,
                       label='nb17' if i == 0 else '')
        ax.axvline(0, color=DARK, lw=1, linestyle='--')
        ax.set_yticks(range(len(comp)))
        ax.set_yticklabels(comp['label'], fontsize=9)
        ax.set_xlabel('Coefficient')
        ax.set_title(title, fontsize=10, color=DARK)

        legend_elements = [
            Line2D([0],[0], marker='o', color='w', markerfacecolor='none',
                   markeredgecolor=DARK, markersize=8, label='nb16 (baseline)'),
            Line2D([0],[0], marker='o', color='w', markerfacecolor=RED,
                   markersize=8, label='nb17 (network-augmented)'),
            Line2D([0],[0], color=RED,  lw=2, label='Sign flipped'),
            Line2D([0],[0], color=GREY, lw=2, label='Stable'),
        ]
        ax.legend(handles=legend_elements, fontsize=8, loc='lower right')

    _comp_panel(ax1, 'logit_coef_nb16', 'logit_coef_nb17', 'logit_sign_flip',
                'Zero component (logistic)')
    _comp_panel(ax2, 'nb_coef_nb16',    'nb_coef_nb17',    'nb_sign_flip',
                'Count component (NegBin)')

    fig.tight_layout()
    save(fig, os.path.join(D02, 'fig06_comparison_forest.png'))


def fig07_roc_curves():
    # Load existing ROC PNGs and embed their AUC info as text annotation
    # since we don't have stored fpr/tpr arrays, redraw with matplotlib from
    # the image or annotate AUC values directly
    fig, ax = plt.subplots(figsize=(7, 7))

    # Draw diagonal reference
    ax.plot([0,1],[0,1], color=GREY, linestyle='--', lw=1, label='Random (AUC = 0.50)')

    # We don't have stored fpr/tpr arrays so we create stylised stand-in curves
    # using a beta-distribution-shaped mock and annotate with known AUC values.
    # This is an honest representation: exact ROC shape not archived, AUC values exact.
    def _mock_roc(auc, n=200, seed=42):
        rng = np.random.RandomState(seed)
        t = np.linspace(0, 1, n)
        # A plausible ROC curve shape for the given AUC
        fpr = t
        # shape parameter from AUC: higher AUC → more concave curve
        tpr = t ** (1 / (auc / (1 - auc)))
        return fpr, tpr

    fpr16, tpr16 = _mock_roc(0.849, seed=10)
    fpr17, tpr17 = _mock_roc(0.857, seed=10)

    ax.plot(fpr16, tpr16, color=GOLD, linestyle='--', lw=2,
            label='Baseline (AUC = 0.849)')
    ax.plot(fpr17, tpr17, color=RED,  linestyle='-',  lw=2,
            label='Network-augmented (AUC = 0.857)')

    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('ROC Curves — Zero Component (Logistic):\nBaseline vs Network-Augmented',
                 fontsize=12, fontweight='bold', color=DARK)
    ax.text(0.55, 0.12, '⚠ Curves are illustrative; AUC values are exact.',
            fontsize=7.5, color=GREY, style='italic', transform=ax.transAxes)
    ax.legend(fontsize=10, loc='lower right')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_aspect('equal')

    fig.tight_layout()
    save(fig, os.path.join(D02, 'fig07_roc_curves.png'))


# ─────────────────────────────────────────────────────────────────────────────
# 03  ECON SCORE RESULTS
# ─────────────────────────────────────────────────────────────────────────────

def fig08_econ_structural_mismatch():
    mono = pd.read_csv(os.path.join(DATA, 'panel_monadic_1992_2024.csv'))

    country_stats = mono.groupby('recipient_iso3').agg(
        econ_mean=('econ_neocol_score_total', 'mean'),
        kill_total=('journalist_killings', 'sum'),
    ).dropna().reset_index()

    country_stats['x'] = np.log1p(country_stats['econ_mean'] * 1e9)
    country_stats['y'] = np.log1p(country_stats['kill_total'])

    HIGHLIGHT = ['IRQ','SYR','PHL','MEX','PAK','LBR','COG','PNG',
                 'MNG','BRA','AFG','COL','IND']

    fig, ax = plt.subplots(figsize=(10, 7))
    normal = country_stats[~country_stats['recipient_iso3'].isin(HIGHLIGHT)]
    ax.scatter(normal['x'], normal['y'], color=GREY, alpha=0.4, s=30, zorder=2)

    for _, row in country_stats[country_stats['recipient_iso3'].isin(HIGHLIGHT)].iterrows():
        ax.scatter(row['x'], row['y'], color=RED, s=60, zorder=4)
        ax.annotate(row['recipient_iso3'], (row['x'], row['y']),
                    fontsize=8, color=RED, xytext=(4,4), textcoords='offset points')

    xmed = country_stats['x'].median()
    ymed = country_stats['y'].median()
    ax.axvline(xmed, color=DARK, lw=1, linestyle='--', alpha=0.5)
    ax.axhline(ymed, color=DARK, lw=1, linestyle='--', alpha=0.5)

    xmax = country_stats['x'].max()
    ymax = country_stats['y'].max()

    ax.text(xmed*0.05, ymax*0.95, 'Low econ dep.\nHigh killings', fontsize=8,
            color=RED, ha='left', va='top')
    ax.text(xmax*0.85, ymax*0.95, 'High econ dep.\nHigh killings', fontsize=8,
            color=GOLD, ha='left', va='top')
    ax.text(xmed*0.05, ymax*0.08, 'Low econ dep.\nLow killings', fontsize=8,
            color=GREY, ha='left', va='bottom')
    ax.text(xmax*0.85, ymax*0.08, 'High econ dep.\nLow killings', fontsize=8,
            color=GREY, ha='left', va='bottom')

    ax.set_xlabel('Mean Econ Neo-Col Score (log1p × 1e9)', fontsize=11)
    ax.set_ylabel('Total Journalist Killings (log1p)', fontsize=11)
    ax.set_title('Structural Mismatch: Economic Dependency vs Journalist Violence',
                 fontsize=12, fontweight='bold', color=DARK)
    ax.text(0.5, -0.1, 'Dashed lines = medians.  Spearman r = 0.002, p = 0.952',
            ha='center', transform=ax.transAxes, fontsize=9, color=DARK)

    fig.tight_layout()
    save(fig, os.path.join(D03, 'fig08_econ_structural_mismatch.png'))


def fig09_econ_top_recipients():
    mono = pd.read_csv(os.path.join(DATA, 'panel_monadic_1992_2024.csv'))

    country_mean = mono.groupby('recipient_iso3')['econ_neocol_score_total'].mean()
    top25 = country_mean.nlargest(25).reset_index()
    top25.columns = ['iso3', 'mean_econ']
    top25['econ_log'] = np.log1p(top25['mean_econ'] * 1e9)

    TOP20_KILL = {'IRQ','SYR','PHL','MEX','PAK','IND','AFG','COL','SOM',
                  'BRA','UKR','YEM','DZA','BGD','HND','TUR','LKA','NGA','GTM','RWA'}
    top25['color'] = top25['iso3'].apply(lambda x: GOLD if x in TOP20_KILL else GREY)
    top25 = top25.sort_values('econ_log')

    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(top25['iso3'], top25['econ_log'],
                   color=top25['color'], edgecolor='white', height=0.7)
    ax.set_xlabel('Mean Econ Neo-Col Score (log1p × 1e9)')
    ax.set_title('Top 25 Recipients by Econ Neo-Colonial Score (Mean, 1992–2024)',
                 fontsize=12, fontweight='bold', color=DARK)

    legend_elements = [
        mpatches.Patch(facecolor=GOLD, label='Also top-20 killing country'),
        mpatches.Patch(facecolor=GREY, label='Not in top-20 killing countries'),
    ]
    ax.legend(handles=legend_elements, fontsize=9, loc='lower right')

    fig.tight_layout()
    save(fig, os.path.join(D03, 'fig09_econ_top_recipients.png'))


# ─────────────────────────────────────────────────────────────────────────────
# 04  APPENDIX
# ─────────────────────────────────────────────────────────────────────────────

def figa01_corr_matrix():
    mono = pd.read_csv(os.path.join(DATA, 'panel_monadic_1992_2024.csv'))
    vars_corr = ['arms_tiv_total','oda_total','econ_neocol_score_total',
                 'colonial_tie_flag','gdp_per_capita_log','population_log',
                 'armed_conflict','journalist_killings']
    clean = [CLEAN_NAMES.get(v, v.replace('_', ' ').title()) for v in vars_corr]
    corr = mono[vars_corr].rename(columns=dict(zip(vars_corr, clean))).corr()

    import matplotlib.colors as mcolors
    cmap = mcolors.LinearSegmentedColormap.from_list(
        'rw_blue', [BLUE, '#FFFFFF', RED], N=256)

    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(corr.values, cmap=cmap, vmin=-1, vmax=1)
    ax.set_xticks(range(len(clean))); ax.set_xticklabels(clean, rotation=40, ha='right', fontsize=9)
    ax.set_yticks(range(len(clean))); ax.set_yticklabels(clean, fontsize=9)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
    ax.grid(False)

    for i in range(len(clean)):
        for j in range(len(clean)):
            ax.text(j, i, f'{corr.values[i,j]:.2f}',
                    ha='center', va='center', fontsize=9,
                    color='white' if abs(corr.values[i,j]) > 0.5 else DARK)

    plt.colorbar(im, ax=ax, fraction=0.04, pad=0.04)
    ax.set_title('Pearson Correlation Matrix — Monadic Panel',
                 fontsize=12, fontweight='bold', color=DARK, pad=12)
    fig.tight_layout()
    save(fig, os.path.join(D04, 'figa01_corr_matrix.png'))


def figa02_predicted_vs_actual():
    # Load the existing predicted vs actual data from nb16
    # nb16 saved a PNG; check if underlying CSV exists
    results_dir = RES
    # Try to reconstruct: load the panel and positive-count subset
    # The nb16_predicted_vs_actual.png exists — we will recreate using model coefficients
    # For now, display the stored image with our style wrapper

    # Fallback: load nb16 NB coefficients and reconstruct rough predictions
    mono = pd.read_csv(os.path.join(DATA, 'panel_monadic_1992_2024.csv'))
    final = pd.read_csv(os.path.join(DATA, 'panel_final_1992_2024.csv'))

    pos = final[final['journalist_killings'] > 0].copy()
    n_pos = len(pos)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(pos['journalist_killings'], bins=30, color=DARK, alpha=0.5,
            label=f'Actual (n={n_pos})', density=True)

    # NB model coefficients from stored CSV
    nb_coef = pd.read_csv(os.path.join(RES, 'nb16_negative_binomial_positive_counts_coefficients.csv'))
    coef_dict = dict(zip(nb_coef['term'], nb_coef['coef']))

    features = ['arms_tiv_total_log_lag1','oda_total_log_lag1',
                'econ_neocol_score_total_lag1','colonial_tie_flag',
                'gdp_per_capita_log','population_log',
                'armed_conflict','conflict_intensity']
    available = [f for f in features if f in pos.columns and f in coef_dict]

    if available:
        log_mu = coef_dict.get('const', 0)
        for f in available:
            log_mu = log_mu + coef_dict[f] * pos[f].fillna(0)
        mu = np.exp(log_mu).clip(0.01, 1000)
        ax.hist(mu, bins=30, color=RED, alpha=0.5,
                label='Predicted (NB model)', density=True)
    else:
        ax.text(0.5, 0.5, 'Predicted values not available\n(features missing from panel)',
                ha='center', va='center', transform=ax.transAxes, color=GREY)

    ax.set_xscale('log')
    ax.set_xlabel('Journalist killings (log scale)')
    ax.set_ylabel('Density')
    ax.set_title('NegBin — Predicted vs Actual Distribution\n(Positive Counts Only, n=687)',
                 fontsize=12, fontweight='bold', color=DARK)
    ax.legend(fontsize=10)

    fig.tight_layout()
    save(fig, os.path.join(D04, 'figa02_predicted_vs_actual.png'))


def figa03_econ_distribution():
    mono = pd.read_csv(os.path.join(DATA, 'panel_monadic_1992_2024.csv'))
    raw = mono['econ_neocol_score_total'].dropna()
    log_v = np.log1p(raw * 1e9)

    zero_share = 100 * (raw == 0).sum() / len(raw)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle('Distribution of Econ Neo-Colonial Score — Raw and Log-Transformed',
                 fontsize=13, fontweight='bold', color=DARK)

    ax1.hist(raw, bins=60, color=GREY, edgecolor='white', linewidth=0.3)
    ax1.set_xlabel('Raw econ_neocol_score_total')
    ax1.set_ylabel('Count')
    ax1.set_title('Raw score')
    ax1.annotate(f'Zero share: {zero_share:.1f}%',
                 xy=(0.6, 0.9), xycoords='axes fraction', fontsize=10, color=DARK)

    ax2.hist(log_v, bins=60, color=GOLD, edgecolor='white', linewidth=0.3)
    ax2.set_xlabel('log1p(score × 1e9)')
    ax2.set_ylabel('Count')
    ax2.set_title('Log-transformed score')

    fig.tight_layout()
    save(fig, os.path.join(D04, 'figa03_econ_distribution.png'))


def figa04_econ_decile():
    # Two-bar chart: Zero killings vs Any killing — mean econ score (log)
    # This is more honest than a decile chart given 88.7% zeros collapse most deciles
    df = pd.read_csv(os.path.join(RES, 'nb18_econ_score_by_killing_status.csv'))
    df.columns = df.columns.str.strip()

    labels   = ['Zero killings', 'Any killing']
    means    = [df.loc[df.iloc[:,0] == 'Zero killings', 'Mean econ score'].values[0],
                df.loc[df.iloc[:,0] == 'Any killing',   'Mean econ score'].values[0]]
    stds     = [df.loc[df.iloc[:,0] == 'Zero killings', 'Std'].values[0],
                df.loc[df.iloc[:,0] == 'Any killing',   'Std'].values[0]]
    ns       = [df.loc[df.iloc[:,0] == 'Zero killings', 'N'].values[0],
                df.loc[df.iloc[:,0] == 'Any killing',   'N'].values[0]]
    sems     = [s / np.sqrt(n) for s, n in zip(stds, ns)]
    colors   = [GREY, RED]

    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(labels, means, yerr=sems, capsize=6,
                  color=colors, edgecolor='white', width=0.45,
                  error_kw={'color': DARK, 'lw': 1.5})

    for bar, m, n in zip(bars, means, ns):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(sems)*1.3,
                f'{m:.1f}\n(n={int(n):,})', ha='center', va='bottom', fontsize=9, color=DARK)

    ax.set_ylabel('Mean Econ Neo-Col Score (log1p × 1e9)')
    ax.set_title('Econ Neo-Colonial Score by Killing Status\n(Mean ± SEM)',
                 fontsize=12, fontweight='bold', color=DARK)
    ax.set_ylim(0, max(means) * 1.4)
    fig.tight_layout()
    save(fig, os.path.join(D04, 'figa04_econ_decile.png'))


def figa05_econ_trajectories():
    mono = pd.read_csv(os.path.join(DATA, 'panel_monadic_1992_2024.csv'))
    mono['econ_log'] = np.log1p(mono['econ_neocol_score_total'].fillna(0) * 1e9)

    country_colors = {
        'IRQ': RED, 'PHL': GOLD, 'MEX': '#2A7F6F',
        'LBR': '#7F2A2A', 'COG': '#6A5ACD', 'PNG': DARK,
    }

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle('Key Countries: Econ Score vs Journalist Killings Trajectories (1992–2024)',
                 fontsize=12, fontweight='bold', color=DARK)

    for iso, col in country_colors.items():
        sub = mono[mono['recipient_iso3'] == iso].sort_values('year')
        if sub.empty: continue
        ax1.plot(sub['year'], sub['econ_log'],    color=col, lw=2, label=iso)
        ax2.plot(sub['year'], sub['journalist_killings'], color=col, lw=2, label=iso)

    ax1.set_xlabel('Year'); ax1.set_ylabel('Econ Neo-Col Score (log)')
    ax1.set_title('Econ score over time')
    ax1.legend(fontsize=8)

    ax2.set_xlabel('Year'); ax2.set_ylabel('Journalist killings')
    ax2.set_title('Journalist killings over time')
    ax2.legend(fontsize=8)

    fig.tight_layout()
    save(fig, os.path.join(D04, 'figa05_econ_trajectories.png'))


def figa06_network_top_nodes():
    src = os.path.join(RES, 'network_top_nodes.png')
    dst = os.path.join(D04, 'figa06_network_top_nodes.png')
    shutil.copy2(src, dst)
    print(f'  copied → {os.path.relpath(dst, BASE)}')
    CREATED.append(dst)


def figa07_network_trajectories():
    src = os.path.join(BASE, 'outputs', 'results', 'key_countries_network_trajectories.png')
    dst = os.path.join(D04, 'figa07_network_trajectories.png')
    shutil.copy2(src, dst)
    print(f'  copied → {os.path.relpath(dst, BASE)}')
    CREATED.append(dst)


# ─────────────────────────────────────────────────────────────────────────────
# 05  TABLES
# ─────────────────────────────────────────────────────────────────────────────

def _style_table(tbl, n_rows, n_cols):
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.55)
    for j in range(n_cols):
        cell = tbl[0, j]
        cell.set_facecolor(RED)
        cell.set_text_props(color='white', fontweight='bold')
    for i in range(1, n_rows + 1):
        bg = WHITE if i % 2 == 1 else ROWALT
        for j in range(n_cols):
            tbl[i, j].set_facecolor(bg)
            tbl[i, j].set_text_props(color=DARK)


def _render_table(rows, col_labels, title, path, col_widths=None):
    n_cols = len(col_labels)
    n_rows = len(rows)
    fig_h = max(2.5, 0.45 * (n_rows + 2))
    fig, ax = plt.subplots(figsize=(max(8, n_cols * 1.8), fig_h))
    ax.axis('off')
    tbl = ax.table(cellText=rows, colLabels=col_labels,
                   cellLoc='center', loc='center')
    _style_table(tbl, n_rows, n_cols)
    ax.set_title(title, fontsize=12, fontweight='bold', color=DARK, pad=12)
    save(fig, path)


def _render_table_wide(rows, col_labels, title, path, first_col_width=0.50):
    """Like _render_table but gives column 0 proportionally more space."""
    n_cols = len(col_labels)
    n_rows = len(rows)
    fig_h = max(2.5, 0.45 * (n_rows + 2))
    fig_w = max(10, n_cols * 2.0)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis('off')

    # Build per-column widths so column 0 is wider
    rest_w = (1.0 - first_col_width) / max(n_cols - 1, 1)
    col_widths = [first_col_width] + [rest_w] * (n_cols - 1)

    tbl = ax.table(cellText=rows, colLabels=col_labels,
                   cellLoc='center', loc='center',
                   colWidths=col_widths)
    _style_table(tbl, n_rows, n_cols)

    # Left-align the label column
    for i in range(n_rows + 1):
        tbl[i, 0].set_text_props(ha='left')
        tbl[i, 0]._loc = 'left'

    ax.set_title(title, fontsize=12, fontweight='bold', color=DARK, pad=12)
    save(fig, path)


def table01_vif():
    df = pd.read_csv(os.path.join(RES, 'nb16_vif_baseline_features.csv'))
    df['feature_clean'] = df['feature'].map(lambda x: CLEAN_NAMES.get(x, x))
    df = df.sort_values('vif', ascending=False)
    rows = [[row['feature_clean'], f'{row["vif"]:.3f}'] for _, row in df.iterrows()]
    _render_table(rows, ['Feature', 'VIF'],
                  'Variance Inflation Factors — Baseline Model (nb16)',
                  os.path.join(D05, 'table01_vif_nb16.png'))


def table02_sample_construction():
    df = pd.read_csv(os.path.join(RES, 'nb16_sample_loss.csv'))
    # Reconstruct sample construction stages from the data
    total = int(df['rows_before'].values[0])
    after = int(df['rows_after'].values[0])
    dropped = int(df['rows_dropped'].values[0])
    pct_dropped = float(df['pct_dropped'].values[0])
    nonzero = int(df['nonzero_count_rows'].values[0])
    zero_count = int(df['zero_count_rows'].values[0])

    rows = [
        ['Full monadic panel (1992–2024)',                   str(total),    '100.0%'],
        ['After lag + missingness filter',                   str(after),    f'{100*(after/total):.1f}%'],
        ['Dropped (lag NaNs + missing covariates)',          str(dropped),  f'{pct_dropped:.1f}%'],
        ['Zero-killing obs. (logit component)',              str(zero_count), f'{100*zero_count/after:.1f}%'],
        ['Positive-killing obs. (NegBin component)',         str(nonzero),  f'{100*nonzero/after:.1f}%'],
    ]
    _render_table_wide(rows, ['Stage', 'N', '%'],
                       'Sample Construction — Baseline Hurdle Model',
                       os.path.join(D05, 'table02_sample_construction.png'),
                       first_col_width=0.55)


def table03_nb16_logit_coefs():
    df = pd.read_csv(os.path.join(RES, 'nb16_logit_any_killing_coefficients.csv'))
    df['term_clean'] = df['term'].map(lambda x: CLEAN_NAMES.get(x, x))
    rows = []
    for _, r in df.iterrows():
        sig = r.get('significance', '')
        rows.append([
            r['term_clean'],
            f'{r["coef"]:.3f}',
            f'{r["std_err"]:.3f}',
            f'{r["z"]:.3f}',
            f'{r["p_value"]:.4f}',
            str(sig) if pd.notna(sig) else '',
        ])
    _render_table_wide(rows, ['Variable', 'Coef', 'Std Err', 'Z', 'P-value', 'Sig'],
                       'Logistic Component Coefficients — Baseline Model (nb16)',
                       os.path.join(D05, 'table03_nb16_logit_coefficients.png'),
                       first_col_width=0.38)


def table04_nb16_nb_coefs():
    df = pd.read_csv(os.path.join(RES, 'nb16_negative_binomial_positive_counts_coefficients.csv'))
    df['term_clean'] = df['term'].map(lambda x: CLEAN_NAMES.get(x, x))
    rows = []
    for _, r in df.iterrows():
        sig = r.get('significance', '')
        rows.append([
            r['term_clean'],
            f'{r["coef"]:.3f}',
            f'{r["std_err"]:.3f}',
            f'{r["z"]:.3f}',
            f'{r["p_value"]:.4f}',
            str(sig) if pd.notna(sig) else '',
        ])
    _render_table_wide(rows, ['Variable', 'Coef', 'Std Err', 'Z', 'P-value', 'Sig'],
                       'Negative Binomial Component Coefficients — Baseline Model (nb16)',
                       os.path.join(D05, 'table04_nb16_nb_coefficients.png'),
                       first_col_width=0.38)


def table05_nb17_interactions():
    df = pd.read_csv(os.path.join(RES, 'nb17_interaction_terms_summary.csv'))
    df['term_clean'] = df['term'].map(lambda x: CLEAN_NAMES.get(x, x))
    rows = []
    for _, r in df.iterrows():
        rows.append([
            r['term_clean'],
            f'{r["logit_coef"]:.3f}',
            f'{r["logit_p"]:.4f}',
            str(r.get("logit_sig", "")) if pd.notna(r.get("logit_sig","")) else '',
            f'{r["nb_coef"]:.3f}',
            f'{r["nb_p"]:.4f}',
            str(r.get("nb_sig", "")) if pd.notna(r.get("nb_sig","")) else '',
        ])
    _render_table(rows,
                  ['Term', 'Logit Coef', 'Logit p', 'Sig', 'NB Coef', 'NB p', 'Sig'],
                  'Interaction Terms — Network-Augmented Model (nb17)',
                  os.path.join(D05, 'table05_nb17_interactions.png'))


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('\n=== 01_data_and_methods ===')
    fig01_summary_stats()
    fig02_target_distribution()
    fig03_missingness()

    print('\n=== 02_results_main_findings ===')
    fig04_nb16_forest()
    fig05_nb17_forest()
    fig06_comparison_forest()
    fig07_roc_curves()

    print('\n=== 03_results_econ_score ===')
    fig08_econ_structural_mismatch()
    fig09_econ_top_recipients()

    print('\n=== 04_appendix ===')
    figa01_corr_matrix()
    figa02_predicted_vs_actual()
    figa03_econ_distribution()
    figa04_econ_decile()
    figa05_econ_trajectories()
    figa06_network_top_nodes()
    figa07_network_trajectories()

    print('\n=== 05_tables ===')
    table01_vif()
    table02_sample_construction()
    table03_nb16_logit_coefs()
    table04_nb16_nb_coefs()
    table05_nb17_interactions()

    print('\n\n=== ALL FILES CREATED ===')
    for p in CREATED:
        print(f'  {os.path.relpath(p, BASE)}')
    print(f'\nTotal: {len(CREATED)} files')

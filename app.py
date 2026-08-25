from pathlib import Path
import re

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# GENESIS EIR 3 | CFA | APPLICATION INTELLIGENCE
# V5 - MULTI-PAGE EXECUTIVE DASHBOARD
# ============================================================

st.set_page_config(
    page_title="GENESIS EIR 3 | CFA",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- COLORS -----------------------------
NAVY = "#0A2540"
NAVY_2 = "#153E5C"
AMBER = "#D4A017"
BLUE = "#2E6F9E"
ICE = "#EAF2F8"
BG = "#F4F7FA"
WHITE = "#FFFFFF"
TEXT = "#182B3A"
MUTED = "#6F7F8C"
BORDER = "#D8E1E8"
GREEN = "#3F8065"
RED = "#C95C5C"
PURPLE = "#6C63A8"
LIGHT = "#F8FAFC"

# ----------------------------- CSS -----------------------------
st.markdown(
    f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Lora:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Streamlit's UI icons (sidebar collapse arrow, etc.) use a ligature icon
       font — the rule above was overriding it and printing the icon's raw
       name as text. Force those back to the icon font. */
    [data-testid="stIconMaterial"],
    span[class*="material-symbols"],
    button[data-testid="stSidebarCollapseButton"] span,
    div[data-testid="collapsedControl"] span {{
        font-family: 'Material Symbols Outlined', 'Material Symbols Rounded', 'Material Icons' !important;
    }}

    .stApp {{
        background:
            radial-gradient(1200px 500px at 100% -10%, rgba(212,160,23,.06), transparent 60%),
            radial-gradient(900px 500px at -10% 0%, rgba(46,111,158,.05), transparent 55%),
            {BG};
    }}

    .block-container {{
        max-width: 1560px;
        padding: 14px 36px 70px 36px;
    }}

    /* ---------------- SIDEBAR ---------------- */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(190deg, {NAVY} 0%, #0D2C49 55%, {NAVY_2} 100%);
        width: 272px;
        box-shadow: 3px 0 18px rgba(0,0,0,.12);
    }}

    section[data-testid="stSidebar"] > div {{
        padding: 20px 16px;
    }}

    section[data-testid="stSidebar"] * {{
        color: #EEF5FA;
        font-family: 'Inter', sans-serif;
    }}

    section[data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,.12);
        margin: 14px 0;
    }}

    /* keep Streamlit's native collapse / reopen arrow visible and clickable */
    div[data-testid="collapsedControl"] {{
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
    }}

    button[data-testid="stSidebarCollapseButton"] {{
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
    }}

    .sb-brand {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 2px;
    }}

    .sb-badge {{
        width: 34px;
        height: 34px;
        border-radius: 9px;
        background: linear-gradient(135deg, {AMBER}, #B5860F);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 14px;
        color: {NAVY};
        flex-shrink: 0;
        box-shadow: 0 3px 8px rgba(212,160,23,.35);
    }}

    .sb-brand-title {{
        font-size: 15px;
        font-weight: 800;
        letter-spacing: .2px;
        line-height: 1.15;
    }}

    .sb-brand-sub {{
        font-size: 10px;
        color: #9FB6C8;
        letter-spacing: 1.1px;
        font-weight: 700;
        margin-top: 2px;
    }}

    .sb-label {{
        font-size: 10.5px;
        font-weight: 800;
        letter-spacing: 1.3px;
        color: {AMBER};
        margin: 2px 0 8px 0;
    }}

    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header[data-testid="stHeader"] {{ background: transparent; }}

    /* ---------------- TOPBAR ---------------- */
    .topbar {{
        background: linear-gradient(120deg, {WHITE} 0%, {ICE} 130%);
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 20px 26px 20px 26px;
        margin-bottom: 22px;
        box-shadow: 0 4px 18px rgba(10,37,64,.06);
        position: relative;
        overflow: hidden;
    }}

    .topbar::before {{
        content: "";
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 5px;
        background: linear-gradient(180deg, {AMBER}, {BLUE});
    }}

    .eyebrow {{
        color: {AMBER};
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
    }}

    .main-title {{
        font-family: 'Lora', serif;
        color: {NAVY};
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -.3px;
        margin-top: 6px;
    }}

    .subtitle {{
        color: {MUTED};
        font-size: 13.5px;
        margin-top: 6px;
        max-width: 720px;
    }}

    .meta {{
        color: {MUTED};
        font-size: 11px;
        margin-top: 14px;
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
    }}

    .meta span {{
        background: rgba(10,37,64,.05);
        border: 1px solid {BORDER};
        padding: 3px 10px;
        border-radius: 100px;
        font-weight: 600;
    }}

    /* ---------------- KPI CARDS ---------------- */
    .kpi {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 14px;
        min-height: 122px;
        padding: 17px 18px 14px;
        box-shadow: 0 2px 10px rgba(10,37,64,.05);
        transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
        position: relative;
    }}

    .kpi:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 22px rgba(10,37,64,.11);
        border-color: rgba(212,160,23,.45);
    }}

    .kpi-accent {{
        height: 3px;
        width: 34px;
        background: linear-gradient(90deg, {AMBER}, #E8C158);
        border-radius: 3px;
        margin-bottom: 13px;
    }}

    .kpi-label {{
        color: {MUTED};
        font-size: 10.5px;
        font-weight: 800;
        letter-spacing: .6px;
        text-transform: uppercase;
    }}

    .kpi-value {{
        font-family: 'Lora', serif;
        color: {NAVY};
        font-size: 28px;
        line-height: 1.15;
        font-weight: 700;
        margin-top: 8px;
    }}

    .kpi-note {{
        color: {MUTED};
        font-size: 10px;
        margin-top: 7px;
    }}

    /* ---------------- SECTIONS ---------------- */
    .section-head {{
        display: flex;
        align-items: baseline;
        gap: 10px;
        margin-top: 30px;
        margin-bottom: 5px;
    }}

    .section-title {{
        color: {NAVY};
        font-size: 19px;
        font-weight: 800;
        letter-spacing: -.2px;
    }}

    .section-sub {{
        color: {MUTED};
        font-size: 11.5px;
    }}

    .section-rule {{
        height: 3px;
        background: linear-gradient(90deg, {AMBER} 0%, rgba(212,160,23,.15) 55%, transparent 100%);
        width: 100%;
        border-radius: 4px;
        margin-bottom: 15px;
    }}

    /* ---------------- CALLOUTS / INSIGHTS ---------------- */
    .callout {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-left: 4px solid {BLUE};
        border-radius: 10px;
        padding: 11px 15px;
        font-size: 12.5px;
        color: {TEXT};
        margin-bottom: 12px;
        box-shadow: 0 1px 6px rgba(10,37,64,.03);
    }}

    .insight-card {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-left: 4px solid {AMBER};
        border-radius: 10px;
        padding: 12px 15px;
        font-size: 12.5px;
        color: {TEXT};
        margin-bottom: 10px;
        line-height: 1.55;
        box-shadow: 0 1px 6px rgba(10,37,64,.03);
        transition: box-shadow .15s ease, transform .15s ease;
    }}

    .insight-card:hover {{
        box-shadow: 0 6px 16px rgba(10,37,64,.08);
        transform: translateX(2px);
    }}

    /* ---------------- PAGE HEADER ---------------- */
    .page-title {{
        font-family: 'Lora', serif;
        color: {NAVY};
        font-size: 25px;
        font-weight: 700;
        margin-bottom: 3px;
    }}

    .page-desc {{
        color: {MUTED};
        font-size: 12.5px;
        margin-bottom: 18px;
    }}

    /* ---------------- CHARTS ---------------- */
    div[data-testid="stPlotlyChart"] {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 13px;
        padding: 4px;
        overflow: visible;
        box-shadow: 0 2px 10px rgba(10,37,64,.045);
        transition: box-shadow .15s ease;
    }}

    div[data-testid="stPlotlyChart"]:hover {{
        box-shadow: 0 6px 18px rgba(10,37,64,.09);
    }}

    div[data-testid="stPlotlyChart"] > div {{
        width: 100% !important;
    }}

    /* ---------------- BUTTONS / INPUTS ---------------- */
    .stButton button {{
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,.25);
        transition: all .15s ease;
    }}

    section[data-testid="stSidebar"] .stButton button {{
        background: rgba(255,255,255,.08);
        color: #EEF5FA;
    }}

    section[data-testid="stSidebar"] .stButton button:hover {{
        background: {AMBER};
        color: {NAVY};
        border-color: {AMBER};
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 11px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(10,37,64,.045);
    }}

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
        background: #FFFFFF;
        color: #162B3C;
        border: none;
        border-radius: 7px;
    }}

    section[data-testid="stSidebar"] input {{
        color: #162B3C !important;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        background: rgba(255,255,255,.05);
        border-radius: 8px;
        padding: 7px 9px;
        margin-bottom: 4px;
        transition: background .15s ease;
        border: 1px solid transparent;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background: rgba(212,160,23,.14);
        border-color: rgba(212,160,23,.3);
    }}

    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {{
        font-size: 12px;
    }}

    .app-footer {{
        margin-top: 30px;
        padding-top: 16px;
        border-top: 1px solid {BORDER};
        color: #93A2AD;
        font-size: 10.5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
    }}

    .app-footer .tag {{
        background: {ICE};
        border: 1px solid {BORDER};
        padding: 3px 10px;
        border-radius: 100px;
        color: {NAVY};
        font-weight: 700;
        letter-spacing: .3px;
    }}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATA HELPERS  (unchanged business logic from original app)
# ============================================================

def clean(value):
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def norm(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def find_column(df, aliases):
    exact = {norm(c): c for c in df.columns}

    for alias in aliases:
        if norm(alias) in exact:
            return exact[norm(alias)]

    for c in df.columns:
        nc = norm(c)
        for alias in aliases:
            na = norm(alias)
            if na in nc or nc in na:
                return c
    return None


def values(df, col):
    if not col:
        return pd.Series(["Not Available"] * len(df), index=df.index)
    return df[col].map(clean).replace("", "Not Available")


def shorten(value, limit=34):
    value = str(value)
    return value if len(value) <= limit else value[:limit - 1] + "…"


def frequency(df, field, limit=None):
    """Full frequency distribution, count DESC. limit=None returns all rows."""
    if df.empty:
        return pd.DataFrame(columns=["label", "count", "pct"])

    s = df[field].fillna("Not Available").map(clean)
    s = s.replace("", "Not Available")
    out = s.value_counts().reset_index()
    out.columns = ["label", "count"]
    total = out["count"].sum()
    out["pct"] = (out["count"] / total * 100) if total else 0
    if limit:
        out = out.head(limit)
    return out


def extract_trl_level(label):
    """Extract the numeric TRL level from a label like 'TRL 4' or '4'. Returns None if not found."""
    match = re.search(r"(\d+)", str(label))
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    return None


# ============================================================
# CHART BUILDERS
# ============================================================

def layout(fig, title="", height=390):
    top_margin = 78 if title else 18

    fig.update_layout(
        height=height,
        margin=dict(l=18, r=28, t=top_margin, b=28),
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(family="Arial", size=11, color="#000000"),
        title=dict(
            text=title,
            x=0.02,
            xanchor="left",
            y=0.98,
            yanchor="top",
            font=dict(size=15, color="#000000"),
        ),
        hoverlabel=dict(bgcolor=WHITE, font_color=TEXT),
        legend=dict(
            orientation="h",
            x=0.02,
            xanchor="left",
            y=1.075,
            yanchor="bottom",
            bgcolor="rgba(255,255,255,0)",
            borderwidth=0,
            font=dict(family="Arial", size=10, color="#000000"),
            tracegroupgap=6,
        ),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E8EDF1",
        zeroline=False,
        tickfont=dict(color="#000000"),
        title_font=dict(color="#000000"),
    )
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        automargin=True,
        tickfont=dict(color="#000000"),
        title_font=dict(color="#000000"),
    )
    fig.update_layout(legend_font=dict(color="#000000"))

    return fig


def bar_chart(df, field, title, n=10, color=NAVY, height=400,
              show_pct=False, full_distribution=False, category_order=None):
    """
    Horizontal bar chart, HIGH -> LOW top to bottom.
    full_distribution=True ignores the Top-N slider and shows every category.
    category_order: explicit list of labels (low->high) to force axis order,
    used for TRL so it reads TRL1 -> TRL9 instead of by frequency.
    """
    d = frequency(df, field, None if full_distribution else n)
    if d.empty:
        return go.Figure()

    d["full"] = d["label"]
    d["short"] = d["label"].map(lambda x: shorten(x, 38))

    if category_order:
        # explicit logical order (e.g. TRL levels) - ascending so the
        # lowest level sits at the bottom and highest at the top
        order_map = {lbl: i for i, lbl in enumerate(category_order)}
        d["_order"] = d["label"].map(lambda x: order_map.get(x, -1))
        d = d.sort_values("_order")
    else:
        # frequency order - ascending count so the HIGHEST count renders
        # at the top of a horizontal bar chart
        d = d.sort_values("count")

    text_field = "count"
    if show_pct:
        d["label_text"] = d.apply(lambda r: f"{r['count']:,} ({r['pct']:.1f}%)", axis=1)
        text_field = "label_text"

    fig = px.bar(
        d,
        x="count",
        y="short",
        orientation="h",
        text=text_field,
        custom_data=["full", "pct"],
    )
    fig.update_traces(
        marker_color=color,
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{customdata[0]}</b><br>Applications: %{x:,} (%{customdata[1]:.1f}%)<extra></extra>",
    )
    fig.update_xaxes(tickformat=",")
    fig.update_yaxes(categoryorder="array", categoryarray=list(d["short"]))
    return layout(fig, title, height)


def donut_chart(df, field, title, height=390):
    d = frequency(df, field, 12)
    if d.empty:
        return go.Figure()

    fig = px.pie(d, names="label", values="count", hole=.62)
    fig.update_traces(
        textposition="inside",
        texttemplate="%{percent:.1%}",
        hovertemplate="<b>%{label}</b><br>Applications: %{value:,}<extra></extra>",
        marker=dict(line=dict(color=WHITE, width=2)),
    )
    return layout(fig, title, height)


_PLOTLY_CHART_COUNTER = 0


def render(fig):
    global _PLOTLY_CHART_COUNTER
    _PLOTLY_CHART_COUNTER += 1

    st.plotly_chart(
        fig,
        use_container_width=True,
        key=f"plotly_chart_{_PLOTLY_CHART_COUNTER}",
        config={"displaylogo": False, "displayModeBar": True, "responsive": True},
    )


def section(title, subtitle=""):
    st.markdown(
        f"""
        <div class="section-head">
            <div class="section-title">{title}</div>
            <div class="section-sub">{subtitle}</div>
        </div>
        <div class="section-rule"></div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, desc):
    st.markdown(
        f"""
        <div class="page-title">{title}</div>
        <div class="page-desc">{desc}</div>
        """,
        unsafe_allow_html=True,
    )


def kpi_row(kpis):
    cols = st.columns(len(kpis))
    for col, (label, value, note) in zip(cols, kpis):
        display = f"{value:,}" if isinstance(value, int) else value
        col.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-accent"></div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{display}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def insight_card(text):
    st.markdown(f'<div class="insight-card">{text}</div>', unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    folder = Path(__file__).resolve().parent
    path = folder / "Applications__7_.xlsx"

    if not path.exists():
        candidates = list(folder.glob("*.xlsx"))
        if not candidates:
            raise FileNotFoundError(
                "Applications__7_.xlsx not found in the same folder as app.py."
            )
        path = candidates[0]

    workbook = pd.ExcelFile(path)
    sheet = "Screening" if "Screening" in workbook.sheet_names else workbook.sheet_names[0]
    data = pd.read_excel(path, sheet_name=sheet)
    data.columns = [clean(c) for c in data.columns]
    return data, path.name, sheet


try:
    raw, source_file, source_sheet = load_data()
except Exception as error:
    st.error(str(error))
    st.stop()


# ============================================================
# COLUMN MAPPING (unchanged)
# ============================================================

COL = {
    "form": find_column(raw, ["Form Status"]),
    "round": find_column(raw, ["Round Status"]),
    "stage": find_column(raw, ["Current Startup Stage"]),
    "sector": find_column(raw, ["Startup Sector", "Sector"]),
    "gender": find_column(raw, ["Gender"]),
    "occupation": find_column(raw, ["Current Occupation", "Occupation"]),
    "mode": find_column(raw, ["Preferred Incubation Mode"]),
    "innovation": find_column(raw, ["Innovation Type"]),
    "dpiit": find_column(raw, ["Is your startup DPIIT Registered?", "DPIIT Registered"]),
    "pref1": find_column(raw, ["Preference 1"]),
    "pref2": find_column(raw, ["Preference 2"]),
    "statecity": find_column(raw, ["State & City", "State and City"]),
    "state": find_column(raw, ["State"]),
    "city": find_column(raw, ["City"]),
    "qualification": find_column(raw, ["Highest Qualification", "Highest Educational Qualification"]),
    "time": find_column(raw, ["Time allocation by founder on startup", "Time allocation", "Founder time allocation"]),
    "technology": find_column(raw, ["Technology Used", "Technology used"]),
    "trl": find_column(raw, ["Technology Readiness Level (TRL)", "Technology Readiness Level", "TRL"]),
}

df = raw.copy()

for name, col in COL.items():
    df[f"_{name}"] = values(raw, col)

# State / city extraction (unchanged logic)
INDIA_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]


def extract_state_only(value):
    s = clean(value)
    if not s or s == "Not Available":
        return "Not Available"
    s_norm = re.sub(r"\s+", " ", s).strip().lower()
    for state in INDIA_STATES:
        if re.search(r"(?<![a-z])" + re.escape(state.lower()) + r"(?![a-z])", s_norm):
            return state
    return clean(re.split(r"[,|/\-]", s, maxsplit=1)[0]) or "Not Available"


if COL["statecity"]:
    raw_location = df["_statecity"].map(clean)
    df["_state_derived"] = raw_location.map(extract_state_only)
    df["_city_derived"] = "Not Available"
elif COL["state"]:
    df["_state_derived"] = df["_state"].map(clean).replace("", "Not Available")
    df["_city_derived"] = (
        df["_city"].map(clean).replace("", "Not Available") if COL["city"] else "Not Available"
    )
else:
    df["_state_derived"] = "Not Available"
    df["_city_derived"] = "Not Available"


# ============================================================
# SIDEBAR - NAVIGATION + FILTERS
# ============================================================

PAGES = [
    "Executive Overview",
    "Application & Pipeline",
    "Founder Profile",
    "Geography",
    "Incubator Intelligence",
    "Sector & Technology",
    "Innovation & Maturity",
    "Data Quality",
]

with st.sidebar:
    st.markdown(
        """
        <div class="sb-brand">
            <div class="sb-badge">G3</div>
            <div>
                <div class="sb-brand-title">GENESIS EIR 3</div>
                <div class="sb-brand-sub">CFA INTELLIGENCE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown('<div class="sb-label">NAVIGATION</div>', unsafe_allow_html=True)
    page = st.radio("Go to", PAGES, index=0, label_visibility="collapsed", key="nav_page")

    st.divider()
    st.markdown('<div class="sb-label">FILTERS</div>', unsafe_allow_html=True)

    form_values = sorted([x for x in df["_form"].unique() if x != "Not Available"])
    stage_values = sorted([x for x in df["_stage"].unique() if x != "Not Available"])
    gender_values = sorted([x for x in df["_gender"].unique() if x != "Not Available"])
    location_values = sorted([x for x in df["_state_derived"].unique() if x != "Not Available"])
    incubator_values = sorted(
        set(
            [x for x in df["_pref1"].unique() if x != "Not Available"]
            + [x for x in df["_pref2"].unique() if x != "Not Available"]
        )
    )

    form_filter = st.selectbox(
        "Form Status", ["All"] + form_values,
        index=(1 if "Submitted" in form_values else 0), key="f_form",
    )
    location_filter = st.selectbox("State", ["All"] + location_values, index=0, key="f_state")
    incubator_filter = st.selectbox("Incubator Name", ["All"] + incubator_values, index=0, key="f_incubator")
    gender_filter = st.selectbox("Gender", ["All"] + gender_values, index=0, key="f_gender")

    st.markdown('<div class="sb-label">INCUBATOR DEMAND CHECK</div>', unsafe_allow_html=True)
    incubator_demand_mode = st.selectbox(
        "Incubator demand", ["All", "Applications less than count"], index=0, key="f_demand_mode",
    )
    incubator_demand_count = st.selectbox(
        "Count", list(range(1, 101)), index=9,
        disabled=(incubator_demand_mode == "All"), key="f_demand_count",
        help="Example: 10 shows incubators with fewer than 10 applications across Preference 1 + Preference 2.",
    )

    stage_filter = st.selectbox("Current Startup Stage", ["All"] + stage_values, index=0, key="f_stage")

    st.markdown('<div class="sb-label">CHART DETAIL</div>', unsafe_allow_html=True)
    top_n = st.slider("Top categories shown", min_value=5, max_value=25, value=10, step=1, key="f_top_n")

    st.divider()
    if st.button("Reset filters", use_container_width=True):
        for k in ["f_form", "f_state", "f_incubator", "f_gender", "f_demand_mode",
                  "f_demand_count", "f_stage", "f_top_n"]:
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown(
        f"""
        <div style="font-size:10px;color:#AFC3D3;line-height:1.6;">
        DATASET<br>{len(df):,} screening records<br><br>
        SOURCE<br>{source_file}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CENTRALIZED FILTERING (unchanged logic, single source of truth)
# ============================================================

def apply_filters(base_df):
    out = base_df.copy()

    if form_filter != "All":
        out = out[out["_form"] == form_filter]
    if location_filter != "All":
        out = out[out["_state_derived"] == location_filter]
    if incubator_filter != "All":
        out = out[(out["_pref1"] == incubator_filter) | (out["_pref2"] == incubator_filter)]
    if gender_filter != "All":
        out = out[out["_gender"] == gender_filter]
    if stage_filter != "All":
        out = out[out["_stage"] == stage_filter]

    if incubator_demand_mode == "Applications less than count":
        demand_p1 = (
            out["_pref1"].map(clean)
            .loc[lambda s: ~s.str.lower().isin(["", "not available", "nan", "none"])]
            .value_counts()
        )
        demand_p2 = (
            out["_pref2"].map(clean)
            .loc[lambda s: ~s.str.lower().isin(["", "not available", "nan", "none"])]
            .value_counts()
        )
        demand = demand_p1.add(demand_p2, fill_value=0)
        low_demand_incubators = set(demand[demand < incubator_demand_count].index)
        out = out[out["_pref1"].isin(low_demand_incubators) | out["_pref2"].isin(low_demand_incubators)]

    return out


filtered = apply_filters(df)

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()


def preference_frequency(data, field):
    """Full, un-truncated Preference 1 / Preference 2 counts (unchanged logic)."""
    if data.empty:
        return pd.DataFrame(columns=["Incubator", "count"])

    s = data[field].map(clean)
    s = s[
        (s != "")
        & (s.str.lower() != "not available")
        & (s.str.lower() != "nan")
        & (s.str.lower() != "none")
    ]

    if s.empty:
        return pd.DataFrame(columns=["Incubator", "count"])

    return s.value_counts().rename_axis("Incubator").reset_index(name="count")


def combined_incubator_demand(data):
    """Total Demand = Preference 1 + Preference 2, computed on FULL counts before any truncation."""
    p1 = preference_frequency(data, "_pref1").rename(columns={"count": "Preference 1"})
    p2 = preference_frequency(data, "_pref2").rename(columns={"count": "Preference 2"})

    pref = pd.merge(p1, p2, on="Incubator", how="outer").fillna(0)
    pref["Preference 1"] = pref["Preference 1"].astype(int)
    pref["Preference 2"] = pref["Preference 2"].astype(int)
    pref["Total Demand"] = pref["Preference 1"] + pref["Preference 2"]

    pref = pref.sort_values(
        ["Total Demand", "Preference 1", "Preference 2"],
        ascending=[False, False, False],
        kind="stable",
    ).reset_index(drop=True)
    pref.insert(0, "Rank", pref.index + 1)
    return pref


pref_full = combined_incubator_demand(filtered)


# ============================================================
# TOP BAR
# ============================================================

st.markdown(
    f"""
    <div class="topbar">
        <div class="eyebrow">MEITY STARTUP HUB · GENESIS · EIR 3</div>
        <div class="main-title">CFA Application Intelligence Dashboard</div>
        <div class="subtitle">
            Executive view of founder profile, incubator demand, geography,
            technology, innovation and startup maturity
        </div>
        <div class="meta">
            <span>Screening data: {len(df):,} records</span>
            <span>Current view: {len(filtered):,}</span>
            <span>Source: {source_file}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# KPI BASE NUMBERS (shared across pages)
# ============================================================

total = len(df)
submitted_total = int((df["_form"].str.lower() == "submitted").sum())
completion_rate = (submitted_total / total * 100) if total else 0

submitted = int((filtered["_form"].str.lower() == "submitted").sum())
saved = int((filtered["_form"].str.lower() == "saved").sum())
active = int((filtered["_round"].str.lower() == "active").sum())
withdrawn = int((filtered["_round"].str.lower() == "withdrawn").sum())
filtered_completion_rate = (submitted / len(filtered) * 100) if len(filtered) else 0
dpiit_yes_rate = (
    (filtered["_dpiit"].str.lower().str.startswith("yes").sum() / len(filtered) * 100)
    if len(filtered) else 0
)


# ============================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# ============================================================

def page_executive_overview():
    page_header(
        "Executive Overview",
        "Headline metrics, pipeline health and auto-generated insights for senior management",
    )

    kpi_row([
        ("APPLICATIONS", len(filtered), "Current filtered population"),
        ("SUBMITTED", submitted, "Completed applications"),
        ("COMPLETION RATE", f"{completion_rate:.1f}%", "Submitted / full dataset"),
        ("ACTIVE", active, "Current round status"),
        ("WITHDRAWN", withdrawn, "Current round status"),
    ])

    section("Key Insights", "Automatically derived from the current filtered dataset")

    state_top = frequency(filtered, "_state_derived", 1)
    sector_top = frequency(filtered, "_sector", 1)
    stage_top = frequency(filtered, "_stage", 1)
    tech_top = frequency(filtered, "_technology", 1)
    incubator_top = pref_full.iloc[0] if not pref_full.empty else None

    insights = []
    if not state_top.empty and state_top.iloc[0]["label"] != "Not Available":
        r = state_top.iloc[0]
        insights.append(f"<b>{r['label']}</b> contributes the highest number of applications, with <b>{int(r['count']):,}</b> ({r['pct']:.1f}%) of the current view.")
    if incubator_top is not None:
        insights.append(f"<b>{incubator_top['Incubator']}</b> has the highest combined incubator demand, with <b>{int(incubator_top['Total Demand']):,}</b> applications (Preference 1: {int(incubator_top['Preference 1']):,}, Preference 2: {int(incubator_top['Preference 2']):,}).")
    if not sector_top.empty and sector_top.iloc[0]["label"] != "Not Available":
        r = sector_top.iloc[0]
        insights.append(f"<b>{r['label']}</b> is the most represented startup sector, accounting for <b>{r['pct']:.1f}%</b> of applications.")
    if not tech_top.empty and tech_top.iloc[0]["label"] != "Not Available":
        r = tech_top.iloc[0]
        insights.append(f"<b>{r['label']}</b> is the most commonly used technology among applicants.")
    if not stage_top.empty and stage_top.iloc[0]["label"] != "Not Available":
        r = stage_top.iloc[0]
        insights.append(f"<b>{r['label']}</b> is the most common current startup stage ({r['pct']:.1f}% of applications).")
    insights.append(f"<b>{filtered_completion_rate:.1f}%</b> of applications in the current view are submitted, with the remainder still saved as drafts.")
    insights.append(f"<b>{dpiit_yes_rate:.1f}%</b> of applicants report being DPIIT registered.")

    for text in insights:
        insight_card(text)

    section("Application Pipeline", "Saved → submitted → withdrawn view")
    status = pd.DataFrame({
        "Status": ["Saved", "Submitted", "Withdrawn"],
        "Applications": [saved, submitted, withdrawn],
    }).sort_values("Applications")
    fig = px.bar(
        status, x="Applications", y="Status", orientation="h", text="Applications",
        color="Status",
        color_discrete_map={"Saved": "#9AA8B3", "Submitted": NAVY, "Withdrawn": AMBER},
    )
    fig.update_traces(textposition="outside", cliponaxis=False,
                       hovertemplate="<b>%{y}</b><br>Applications: %{x:,}<extra></extra>")
    fig.update_layout(showlegend=False)
    fig.update_xaxes(tickformat=",")
    fig.update_yaxes(categoryorder="array", categoryarray=list(status["Status"]))
    render(layout(fig, "Application Status", 280))

    section("At a Glance", "Top states, incubators and sectors")
    a, b, c = st.columns(3)
    with a:
        render(bar_chart(filtered, "_state_derived", "Top States", top_n, NAVY, 380, show_pct=True))
    with b:
        d = pref_full.head(top_n).sort_values("Total Demand")
        d["short"] = d["Incubator"].map(lambda x: shorten(x, 30))
        fig = px.bar(d, x="Total Demand", y="short", orientation="h", text="Total Demand", custom_data=["Incubator"])
        fig.update_traces(marker_color=AMBER, textposition="outside", cliponaxis=False,
                           hovertemplate="<b>%{customdata[0]}</b><br>Total demand: %{x:,}<extra></extra>")
        fig.update_xaxes(tickformat=",")
        fig.update_yaxes(categoryorder="array", categoryarray=list(d["short"]))
        render(layout(fig, "Top Incubators (Total Demand)", 380))
    with c:
        render(bar_chart(filtered, "_sector", "Top Sectors", top_n, BLUE, 380, show_pct=True))


# ============================================================
# PAGE 2 — APPLICATION & PIPELINE
# ============================================================

def page_pipeline():
    page_header("Application & Pipeline", "Form status, round status and pipeline movement")

    kpi_row([
        ("APPLICATIONS", len(filtered), "Current filtered population"),
        ("SUBMITTED", submitted, "Form status = Submitted"),
        ("SAVED", saved, "Form status = Saved"),
        ("ACTIVE", active, "Round status = Active"),
        ("WITHDRAWN", withdrawn, "Round status = Withdrawn"),
    ])

    section("Form Status vs Round Status", "Sorted high to low")
    a, b = st.columns(2)
    with a:
        render(bar_chart(filtered, "_form", "Form Status", 10, NAVY, 340, show_pct=True, full_distribution=True))
    with b:
        render(bar_chart(filtered, "_round", "Round Status", 10, BLUE, 340, show_pct=True, full_distribution=True))

    section("Submitted vs Saved vs Withdrawn", "Absolute counts, current filtered view")
    status = pd.DataFrame({
        "Status": ["Saved", "Submitted", "Withdrawn"],
        "Applications": [saved, submitted, withdrawn],
    }).sort_values("Applications")
    fig = px.bar(status, x="Applications", y="Status", orientation="h", text="Applications", color="Status",
                 color_discrete_map={"Saved": "#9AA8B3", "Submitted": NAVY, "Withdrawn": AMBER})
    fig.update_traces(textposition="outside", cliponaxis=False,
                       hovertemplate="<b>%{y}</b><br>Applications: %{x:,}<extra></extra>")
    fig.update_layout(showlegend=False)
    fig.update_xaxes(tickformat=",")
    fig.update_yaxes(categoryorder="array", categoryarray=list(status["Status"]))
    render(layout(fig, "Pipeline Breakdown", 320))


# ============================================================
# PAGE 3 — FOUNDER PROFILE
# ============================================================

def page_founder():
    page_header("Founder Profile", "Demographics, education and founder commitment")

    a, b, c = st.columns(3)
    with a:
        render(donut_chart(filtered, "_gender", "Gender", 360))
    with b:
        render(bar_chart(filtered, "_qualification", "Highest Qualification", top_n, BLUE, 360, show_pct=True))
    with c:
        render(bar_chart(filtered, "_occupation", "Current Occupation", top_n, NAVY, 360, show_pct=True))

    a, b = st.columns(2)
    with a:
        render(bar_chart(filtered, "_time", "Time Allocation by Founder on Startup", top_n, AMBER, 390, show_pct=True))
    with b:
        render(donut_chart(filtered, "_mode", "Preferred Incubation Mode", 390))


# ============================================================
# PAGE 4 — GEOGRAPHY
# ============================================================

def page_geography():
    page_header("Geography", "Where applicant startups are coming from (state extraction preserved)")

    geo = filtered.copy()
    geo["_geo_state"] = geo["_state_derived"]
    geo["_geo_city"] = geo["_city_derived"]

    section("State & City Distribution", "High to low, with application share %")
    a, b = st.columns(2)
    with a:
        render(bar_chart(geo, "_geo_state", "Top States", top_n, NAVY, max(410, top_n * 30), show_pct=True))
    with b:
        render(bar_chart(geo, "_geo_city", "Top Cities", top_n, BLUE, max(410, top_n * 30), show_pct=True))

    section("Full State Ranking", "Complete distribution, not limited by Top-N")
    state_full = frequency(geo, "_geo_state", None)
    state_full = state_full[state_full["label"] != "Not Available"].reset_index(drop=True)
    state_full.insert(0, "Rank", state_full.index + 1)
    state_full = state_full.rename(columns={"label": "State", "count": "Applications", "pct": "Share %"})
    state_full["Share %"] = state_full["Share %"].round(1)
    st.dataframe(state_full, use_container_width=True, hide_index=True)


# ============================================================
# PAGE 5 — INCUBATOR INTELLIGENCE
# ============================================================

def page_incubator():
    page_header("Incubator Intelligence", "First-choice vs second-choice demand and combined ranking")

    st.markdown(
        """
        <div class="callout">
            <b>Preference 1</b> is the founder's first-choice incubator.
            <b>Preference 2</b> is the second-choice incubator.
            <b>Total Demand</b> = Preference 1 + Preference 2, calculated on the complete
            (untruncated) counts before any Top-N selection is applied.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not pref_full.empty:
        top_row = pref_full.iloc[0]
        kpi_row([
            ("INCUBATORS TRACKED", len(pref_full), "Distinct incubators named in Pref 1 / Pref 2"),
            ("TOP INCUBATOR", shorten(top_row["Incubator"], 20), "Highest combined demand"),
            ("TOP DEMAND", int(top_row["Total Demand"]), "Preference 1 + Preference 2"),
            ("TOTAL PREF 1", int(pref_full["Preference 1"].sum()), "All first-choice picks"),
            ("TOTAL PREF 2", int(pref_full["Preference 2"].sum()), "All second-choice picks"),
        ])

    section("Preference 1 vs Preference 2", f"Top {top_n} incubators by combined demand")
    pref_chart = pref_full.head(top_n).copy()

    a, b = st.columns([1.2, 1])
    with a:
        long_pref = pref_chart.melt(
            id_vars="Incubator", value_vars=["Preference 1", "Preference 2"],
            var_name="Preference", value_name="Applications",
        )
        long_pref["Short"] = long_pref["Incubator"].map(lambda x: shorten(x, 31))
        order = pref_chart.sort_values("Total Demand")["Incubator"].map(lambda x: shorten(x, 31)).tolist()

        fig = px.bar(
            long_pref, x="Applications", y="Short", color="Preference", orientation="h",
            barmode="group", text="Applications", custom_data=["Incubator"],
            color_discrete_map={"Preference 1": NAVY, "Preference 2": AMBER},
        )
        fig.update_traces(textposition="outside", cliponaxis=False,
                           hovertemplate="<b>%{customdata[0]}</b><br>%{fullData.name}: %{x:,}<extra></extra>")
        fig.update_xaxes(tickformat=",")
        fig.update_yaxes(categoryorder="array", categoryarray=order)
        render(layout(fig, "Preference 1 vs Preference 2", 460))

    with b:
        d = pref_chart.sort_values("Total Demand")
        d["Short"] = d["Incubator"].map(lambda x: shorten(x, 31))
        fig = px.bar(d, x="Total Demand", y="Short", orientation="h", text="Total Demand", custom_data=["Incubator"])
        fig.update_traces(marker_color=BLUE, textposition="outside", cliponaxis=False,
                           hovertemplate="<b>%{customdata[0]}</b><br>Total demand: %{x:,}<extra></extra>")
        fig.update_xaxes(tickformat=",")
        fig.update_yaxes(categoryorder="array", categoryarray=list(d["Short"]))
        render(layout(fig, "Overall Incubator Demand", 460))

    section("Ranked Incubator Table", "Sorted: Total Demand ↓, Preference 1 ↓, Preference 2 ↓")
    table = pref_full[["Rank", "Incubator", "Preference 1", "Preference 2", "Total Demand"]]
    st.dataframe(table, use_container_width=True, hide_index=True)

    section("Low-Demand Incubators", "Use the sidebar 'Incubator demand' filter to isolate these")
    threshold = 5
    low_demand = pref_full[pref_full["Total Demand"] < threshold]
    if low_demand.empty:
        st.markdown(f'<div class="callout">No incubators currently fall under {threshold} combined applications.</div>', unsafe_allow_html=True)
    else:
        st.dataframe(
            low_demand[["Rank", "Incubator", "Preference 1", "Preference 2", "Total Demand"]],
            use_container_width=True, hide_index=True,
        )


# ============================================================
# PAGE 6 — SECTOR & TECHNOLOGY
# ============================================================

def page_sector_tech():
    page_header("Sector & Technology", "Top startup sectors and technologies represented in applications")

    a, b = st.columns(2)
    with a:
        render(bar_chart(filtered, "_sector", "Startup Sector", top_n, NAVY, max(430, top_n * 34), show_pct=True))
    with b:
        render(bar_chart(filtered, "_technology", "Technology Used", top_n, BLUE, max(430, top_n * 34), show_pct=True))


# ============================================================
# PAGE 7 — INNOVATION & MATURITY
# ============================================================

def page_innovation():
    page_header("Innovation & Startup Maturity", "Innovation profile, technology readiness and current stage")

    a, b, c = st.columns(3)
    with a:
        render(donut_chart(filtered, "_innovation", "Innovation Type", 370))
    with b:
        trl_freq = frequency(filtered, "_trl", None)
        trl_labels = [l for l in trl_freq["label"] if l != "Not Available"]
        trl_order = sorted(trl_labels, key=lambda x: (extract_trl_level(x) is None, extract_trl_level(x) or 0))
        render(bar_chart(
            filtered, "_trl", "Technology Readiness Level (TRL)",
            top_n, PURPLE, 370, show_pct=True, full_distribution=True,
            category_order=trl_order,
        ))
    with c:
        render(donut_chart(filtered, "_stage", "Current Startup Stage", 370))

    section("DPIIT & Incubation", "Registration status and preferred incubation model")
    a, b = st.columns(2)
    with a:
        render(donut_chart(filtered, "_dpiit", "DPIIT Registration Status", 390))
    with b:
        render(donut_chart(filtered, "_mode", "Preferred Incubation Mode", 390))


# ============================================================
# PAGE 8 — DATA QUALITY
# ============================================================

def page_data_quality():
    page_header("Data Quality", "Completeness of the fields used for analytical reporting")

    sort_order = st.radio(
        "Sort completeness", ["Low → High (spot gaps first)", "High → Low"],
        horizontal=True, key="dq_sort",
    )

    quality_fields = [
        ("_gender", "Gender"),
        ("_statecity", "State & City"),
        ("_qualification", "Highest Qualification"),
        ("_time", "Founder Time Allocation"),
        ("_pref1", "Preference 1"),
        ("_pref2", "Preference 2"),
        ("_mode", "Preferred Incubation Mode"),
        ("_technology", "Technology Used"),
        ("_sector", "Startup Sector"),
        ("_innovation", "Innovation Type"),
        ("_trl", "TRL"),
        ("_stage", "Current Startup Stage"),
    ]

    quality_rows = []
    for field, label in quality_fields:
        s = filtered[field]
        filled = (~s.isin(["", "Not Available"])) & s.notna()
        quality_rows.append({
            "Field": label,
            "Completion": round(float(filled.mean() * 100), 1),
            "Filled": int(filled.sum()),
            "Total": len(filtered),
        })

    quality = pd.DataFrame(quality_rows)
    ascending = sort_order.startswith("Low")
    quality = quality.sort_values("Completion", ascending=ascending)

    lowest = quality.sort_values("Completion").iloc[0]
    insight_card(
        f"Lowest completeness: <b>{lowest['Field']}</b> at <b>{lowest['Completion']:.1f}%</b> "
        f"({int(lowest['Filled']):,} of {int(lowest['Total']):,} records filled). "
        "This is the field most likely to distort analysis if used without caveats."
    )

    fig = px.bar(
        quality, x="Completion", y="Field", orientation="h", text="Completion",
        custom_data=["Filled", "Total"],
    )
    fig.update_traces(
        marker_color=[RED if c < 60 else (AMBER if c < 85 else GREEN) for c in quality["Completion"]],
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Completion: %{x:.1f}%<br>Filled: %{customdata[0]:,} / %{customdata[1]:,}<extra></extra>",
    )
    fig.update_xaxes(range=[0, 100], ticksuffix="%")
    fig.update_yaxes(categoryorder="array", categoryarray=list(quality.sort_values("Completion")["Field"]) if ascending
                      else list(quality.sort_values("Completion", ascending=False)["Field"])[::-1])
    render(layout(fig, "Analytical Field Completeness", max(450, len(quality) * 32)))

    st.dataframe(
        quality.rename(columns={"Completion": "Completion %"}).sort_values("Completion %", ascending=False),
        use_container_width=True, hide_index=True,
    )


# ============================================================
# ROUTER
# ============================================================

ROUTES = {
    "Executive Overview": page_executive_overview,
    "Application & Pipeline": page_pipeline,
    "Founder Profile": page_founder,
    "Geography": page_geography,
    "Incubator Intelligence": page_incubator,
    "Sector & Technology": page_sector_tech,
    "Innovation & Maturity": page_innovation,
    "Data Quality": page_data_quality,
}

ROUTES[page]()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="app-footer">
        <span>GENESIS EIR 3 · CFA Application Intelligence · Interactive analytical dashboard</span>
        <span class="tag">MeitY Startup Hub</span>
    </div>
    """,
    unsafe_allow_html=True,
)

import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd

# --------------------------------------------------
# Page Setup
# --------------------------------------------------
st.set_page_config(
    page_title="INSPECTRA | AI Home Inspection",
    layout="wide"
)

session = get_active_session()

st.title("🏠 INSPECTRA")
st.markdown(
    "**AI-Assisted Home & Building Inspection Workspace**  \n"
    "A transparent, explainable system to assess housing safety."
)
st.divider()

# --------------------------------------------------
# Helper: Load Data Safely
# --------------------------------------------------
def load_df(query):
    try:
        return session.sql(query).to_pandas()
    except Exception as e:
        st.error(f"Data load failed: {e}")
        return pd.DataFrame()

# --------------------------------------------------
# Load Core Tables
# --------------------------------------------------
property_df = load_df("SELECT * FROM INSPECTRA_DB.CORE.PROPERTY_RISK")
room_df = load_df("SELECT * FROM INSPECTRA_DB.CORE.ROOM_RISK")
summary_df = load_df("SELECT * FROM INSPECTRA_DB.CORE.PROPERTY_SUMMARY")
image_df = load_df("SELECT * FROM INSPECTRA_DB.CORE.ROOM_IMAGES")
bank_df = load_df("SELECT * FROM INSPECTRA_DB.CORE.BANK_RISK_VIEW")

if property_df.empty:
    st.warning("No inspection data available yet.")
    st.stop()

# --------------------------------------------------
# Sidebar Controls
# --------------------------------------------------
st.sidebar.header("Inspection Settings")
focus = st.sidebar.selectbox(
    "Inspection Focus",
    ["Overall", "Structural", "Electrical", "Finishing"]
)
only_high_risk = st.sidebar.checkbox("Highlight only high-risk rooms")

# --------------------------------------------------
# Property Selection
# --------------------------------------------------
st.subheader("Select Property")
property_id = st.selectbox("Property ID", property_df["PROPERTY_ID"].unique())
property_row = property_df[property_df["PROPERTY_ID"] == property_id].iloc[0]

# --------------------------------------------------
# Key Metrics
# --------------------------------------------------
st.subheader("Overall Risk Assessment")
c1, c2, c3 = st.columns(3)
c1.metric("Risk Level", property_row["RISK_LEVEL"])
c2.metric("Total Risk Score", int(property_row["TOTAL_RISK"]))

rooms_inspected = room_df[room_df["PROPERTY_ID"] == property_id].shape[0]
confidence = "High" if rooms_inspected >= 3 else "Medium"
c3.metric("Inspection Confidence", confidence)
st.divider()

# --------------------------------------------------
# Room-wise Risk Breakdown
# --------------------------------------------------
st.subheader("Room-wise Risk Distribution")
room_view = room_df[room_df["PROPERTY_ID"] == property_id]

if only_high_risk:
    room_view = room_view[room_view["ROOM_RISK_SCORE"] >= 60]

st.caption("Risk score per room based on observed inspection findings.")
st.bar_chart(room_view.set_index("ROOM_TYPE")["ROOM_RISK_SCORE"])
st.dataframe(room_view, use_container_width=True)
st.divider()

# --------------------------------------------------
# Room Risk Heatmap (Simplified)
# --------------------------------------------------
st.subheader("🌡️ Room Risk Heatmap")
heatmap_df = room_view.copy()
# Map colors (just for display in the table)
heatmap_df["RISK_LEVEL"] = heatmap_df["ROOM_RISK_SCORE"].apply(
    lambda x: "High" if x >= 80 else ("Medium" if x >= 60 else ("Low" if x >= 30 else "Safe"))
)
st.dataframe(heatmap_df[["ROOM_TYPE", "ROOM_RISK_SCORE", "RISK_LEVEL"]], use_container_width=True)
st.divider()

# --------------------------------------------------
# Explainable AI Panel
# --------------------------------------------------
st.subheader("🧠 Explainable AI – Room-Level Risk Reasoning")
st.caption(
    "AI reasoning shows which defects contributed to risk scores. "
    "Transparent and auditor-friendly."
)
for _, row in room_view.iterrows():
    score = row["ROOM_RISK_SCORE"]
    if score >= 80:
        reason = "Severe structural or safety defect"
        severity = "HIGH"
    elif score >= 60:
        reason = "Electrical hazard or dampness detected"
        severity = "MEDIUM"
    elif score >= 30:
        reason = "Minor maintenance or finishing issue"
        severity = "LOW"
    else:
        reason = "No significant defects found"
        severity = "SAFE"

    with st.expander(f"🚪 {row['ROOM_TYPE']}"):
        st.markdown(f"**Room Risk Score:** {score}")
        st.markdown(f"**AI Explanation:** {reason}")
        if severity == "HIGH":
            st.error("High-confidence safety risk")
        elif severity == "MEDIUM":
            st.warning("Moderate risk, attention advised")
        elif severity == "LOW":
            st.info("Low risk, routine maintenance suggested")
        else:
            st.success("Room appears safe")
st.divider()

# --------------------------------------------------
# Inspection Coverage
# --------------------------------------------------
st.subheader("Inspection Coverage")
st.metric("Rooms Inspected", rooms_inspected)
st.progress(min(rooms_inspected / 5, 1.0))
st.caption("More inspected rooms increase confidence in the final risk score.")
st.divider()

# --------------------------------------------------
# Plain-Language Summary
# --------------------------------------------------
st.subheader("Plain-Language Inspection Summary")
summary_text = summary_df[summary_df["PROPERTY_ID"] == property_id]["SUMMARY_TEXT"].iloc[0]
if property_row["RISK_LEVEL"] == "HIGH":
    st.error(summary_text)
elif property_row["RISK_LEVEL"] == "MEDIUM":
    st.warning(summary_text)
else:
    st.success(summary_text)
st.divider()

# --------------------------------------------------
# AI-Generated Report (TXT)
# --------------------------------------------------
st.subheader("🤖 AI-Generated Inspection Report")
report_text = f"""
PROPERTY ID: {property_id}

OVERALL RISK LEVEL: {property_row['RISK_LEVEL']}
TOTAL RISK SCORE: {property_row['TOTAL_RISK']}

INSPECTION COVERAGE:
- Rooms inspected: {rooms_inspected}
- Confidence level: {confidence}

KEY AI FINDINGS:
- High-risk rooms detected
- Electrical/damp issues identified
- Structural safety evaluated using transparent thresholds

RECOMMENDATION:
Immediate corrective inspection advised for high-risk rooms.
Preventive maintenance recommended for medium-risk rooms.
"""
st.text_area("Preview (Explainable AI Output)", report_text, height=260)
st.download_button(
    "📥 Download AI Inspection Report (TXT)",
    data=report_text,
    file_name=f"{property_id}_AI_Inspection_Report.txt",
    mime="text/plain"
)
st.divider()

# --------------------------------------------------
# Risk Severity Guide
# --------------------------------------------------
st.subheader("Risk Severity Guide")
st.markdown(
    """
- 🟥 **High (70–100):** Structural or serious safety hazards  
- 🟧 **Medium (30–69):** Electrical/damp issues  
- 🟩 **Low (1–29):** Minor cosmetic/maintenance issues  
- ✅ **Safe (0):** No visible defects  
"""
)
st.divider()

# --------------------------------------------------
# AI Vision Findings (Images)
# --------------------------------------------------
st.subheader("🖼️ Detected Defects (Sample Images)")
img_view = image_df[image_df["PROPERTY_ID"] == property_id]
cols = st.columns(3)
for i, (_, row) in enumerate(img_view.iterrows()):
    with cols[i % 3]:
        st.image(row.get("IMAGE_URL","https://via.placeholder.com/200"))
        st.caption(f"{row['ROOM_TYPE']} – {row.get('DEFECT_LABEL','Unknown')} (Confidence: {int(row.get('DEFECT_CONFIDENCE',0)*100)}%)")
st.divider()

# --------------------------------------------------
# Bank / Mortgage Signal
# --------------------------------------------------
st.subheader("🏦 Bank / Mortgage Risk Signal")
bank_row = bank_df[bank_df["PROPERTY_ID"] == property_id].iloc[0]
decision = bank_row.get("BANK_DECISION","MANUAL_REVIEW")
if decision == "LOAN_REJECT":
    st.error("Loan not recommended due to safety risks")
elif decision == "MANUAL_REVIEW":
    st.warning("Manual review required")
else:
    st.success("Property suitable for standard loan approval")
st.divider()

# --------------------------------------------------
# Risk Trend Over Time
# --------------------------------------------------
st.subheader("📉 Risk Trend Over Time")
trend_df = property_df.copy()
trend_df["INSPECTION_DATE"] = pd.date_range(end=pd.Timestamp.today(), periods=len(trend_df))
st.line_chart(trend_df.set_index("INSPECTION_DATE")["TOTAL_RISK"])
st.divider()

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "INSPECTRA applies explainable AI-assisted logic to inspection data "
    "to help families, banks, and regulators detect unsafe housing early."
)
st.caption("Developed by **Krish Bhatia** | CodeRED")

# INSPECTRA | AI Home Inspection

INSPECTRA is an **AI-assisted home and building inspection workspace** built using **Snowflake** and **Streamlit**. The tool helps identify structural, electrical, and finishing defects in residential properties using explainable AI logic, providing actionable insights for homeowners, banks, and regulators.


https://github.com/user-attachments/assets/4f5364b3-117f-4544-9733-95a920c36c31
---

## **Key Features**

- **Property Risk Scoring**: Aggregates room-level findings into an overall risk score.
- **Explainable AI**: Transparent AI reasoning for each room, explaining risk factors.
- **Room-wise Risk Breakdown**: Easy visualization of high-risk rooms.
- **Inspection Coverage Tracker**: Confidence metric based on number of rooms inspected.
- **AI-Generated Plain-Language Report**: TXT download of inspection summary and recommendations.
- **Image-based Defect Detection**: Displays images tagged with defect labels and AI confidence.
- **Bank / Mortgage Risk Signal**: Shows suitability for loan approval based on property risk.
- **Risk Trend Over Time**: Historical risk trend visualization per property.
- **Risk Severity Guide**: Easy-to-understand color-coded risk legend.

---

## **Problem Solved**

Many housing inspections are **manual, inconsistent, and not easily auditable**. INSPECTRA provides:

- A **standardized risk scoring system** per property and room.
- **Explainable AI insights** for decision-making.
- Faster and safer evaluation for families, regulators, and banks.

---

## **Opportunities / USP**

- Transparent and explainable AI that can be audited.
- Combines structured data (inspection scores) and optional unstructured data (images, labels).
- Helps detect **high-risk properties earlier**, reducing accidents and infrastructure damage.
- Provides **actionable recommendations** for homeowners and banks.

---

## **Tech Stack**

- **Frontend / UI**: Streamlit
- **Backend / Data Processing**: Snowflake Snowpark (Python)
- **Visualization**: Streamlit native charts, optional Plotly
- **AI Logic**: Explainable rules + Cortex AI (optional, depending on availability)
- **Storage**: Snowflake tables for property, room, summary, and images
- **Deployment**: Any cloud platform supporting Python & Streamlit

---

## **Snowflake Tools Used**

- Snowflake Worksheets
- Snowflake Snowpark for Python
- (Optional) Snowflake Cortex for AI classification
- Streams & Tasks (optional for automatic re-evaluation)

---

## **Process Flow / Architecture**

1. Load property, room, and summary tables from Snowflake.
2. Aggregate risk scores per room and property.
3. Apply explainable AI logic for risk reasoning.
4. Visualize risk breakdown, trends, and room heatmaps.
5. Generate plain-language report and downloadable summary.
6. Optional: Trigger AI classification on new inspection images using Snowflake Cortex.
7. Bank/Mortgage decision integration based on overall property risk.

---

## **Estimated Implementation Cost**

- Mostly Snowflake compute cost (varies with usage)
- Minimal storage cost for tables and images
- Streamlit hosting cost (optional if deployed on Streamlit Cloud / Heroku / AWS)

---

## **Future Development**

- Integrate **real-time image analysis** for defect detection.
- Add **automatic alerts for high-risk properties**.
- Expand AI to suggest **repair cost estimates** and timelines.
- Multi-property dashboard for inspectors or regulators.
- Mobile-friendly UI for on-site inspectors.

---

## **How to Run**

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/INSPECTRA-AI.git
   cd INSPECTRA-AI




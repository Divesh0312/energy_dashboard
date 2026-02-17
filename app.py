import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Campus Energy Utility Dashboard",
    layout="wide"
)

st.title("⚡ VIT Campus Energy Utility & Sustainability Dashboard")

# ---------------- MOCK DATA ---------------- #
np.random.seed(7)

areas = [
    "M Block - Classrooms",
    "M Block - Labs",
    "M Block - Auditorium",
    "Old Building - A Block",
    "Old Building - B Block",
    "Old Building - C Block",
    "Old Building - D Block",
    "Old Building - E Block",
    "Old Building - F Block",
    "Old Building - G Block",
    "Old Building - Lower Floor Labs",
    "Canteens",
    "Common Areas"
]

data = pd.DataFrame({
    "Area": areas,
    "Daily Energy (kWh)": np.random.randint(250, 900, len(areas)),
    "Solar Contribution (%)": np.random.randint(20, 55, len(areas)),
    "Occupancy (%)": np.random.randint(35, 95, len(areas))
})

data["Grid Energy (kWh)"] = data["Daily Energy (kWh)"] * (1 - data["Solar Contribution (%)"] / 100)
data["Solar Energy (kWh)"] = data["Daily Energy (kWh)"] * (data["Solar Contribution (%)"] / 100)
data["CO₂ Emissions (kg)"] = data["Grid Energy (kWh)"] * 0.82

# ---------------- SIDEBAR ---------------- #
st.sidebar.header("🎛️ Campus Filters")

selected_areas = st.sidebar.multiselect(
    "Select Campus Areas",
    options=data["Area"].tolist(),
    default=data["Area"].tolist()   # ✅ ALL selected by default
)

occupancy_filter = st.sidebar.slider(
    "Minimum Occupancy (%)",
    0, 100, 20
)

filtered = data[
    (data["Area"].isin(selected_areas)) &
    (data["Occupancy (%)"] >= occupancy_filter)
]

# ---------------- EMPTY CHECK ---------------- #
if filtered.empty:
    st.warning("⚠️ No data available for selected filters. Please adjust filters.")
    st.stop()

# ---------------- KPI STRIP ---------------- #
col1, col2, col3, col4 = st.columns(4)

total_energy = filtered["Daily Energy (kWh)"].sum()
solar_energy = filtered["Solar Energy (kWh)"].sum()

col1.metric("🔋 Total Energy (kWh/day)", int(total_energy))
col2.metric("☀️ Solar Share (%)", f"{int((solar_energy / total_energy) * 100)}%")
col3.metric("🌍 CO₂ Emissions (kg/day)", int(filtered["CO₂ Emissions (kg)"].sum()))
col4.metric("👥 Avg Occupancy", f"{int(filtered['Occupancy (%)'].mean())}%")

st.divider()

# ---------------- VISUALS ROW 1 ---------------- #
c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 Energy Consumption by Area")
    fig_bar = px.bar(
        filtered,
        x="Area",
        y="Daily Energy (kWh)",
        color="Daily Energy (kWh)",
        height=320
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("☀️ Solar vs Grid Energy Split")
    energy_split = pd.DataFrame({
        "Source": ["Solar", "Grid"],
        "Energy (kWh)": [
            filtered["Solar Energy (kWh)"].sum(),
            filtered["Grid Energy (kWh)"].sum()
        ]
    })

    fig_pie = px.pie(
        energy_split,
        names="Source",
        values="Energy (kWh)",
        hole=0.45,
        height=320
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------- VISUALS ROW 2 ---------------- #
b1, b2 = st.columns(2)

with b1:
    st.subheader("📈 Occupancy vs Energy Demand")
    fig_scatter = px.scatter(
        filtered,
        x="Occupancy (%)",
        y="Daily Energy (kWh)",
        size="Daily Energy (kWh)",
        color="Area",
        height=300
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with b2:
    st.subheader("🌱 CO₂ Emissions by Area")
    fig_co2 = px.bar(
        filtered,
        x="Area",
        y="CO₂ Emissions (kg)",
        color="CO₂ Emissions (kg)",
        height=300
    )
    st.plotly_chart(fig_co2, use_container_width=True)

# ---------------- INSIGHTS ---------------- #
st.divider()
st.subheader("🧠 Key Insights & Sustainability Actions")

st.success(
    "• M Block labs and auditorium show higher energy demand due to equipment and events.\n"
    "• Lower-floor labs consume steady power throughout the day.\n"
    "• Solar contribution significantly reduces grid dependency.\n"
    "• Old building blocks can benefit from energy-efficient retrofits."
)

st.info(
    "📌 Long-Term Sustainability Plan:\n"
    "• Rooftop solar expansion on M Block & Old Building\n"
    "• Smart energy meters per floor\n"
    "• AI-based HVAC scheduling\n"
    "• Sensor-based lighting in washrooms and corridors\n"
    "• Target: Net-zero energy campus by 2035"
)

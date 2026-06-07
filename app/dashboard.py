import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Dashboard Académico TUP", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/student_learning_trajectory_noisy.csv")

    df.columns = df.columns.str.lower().str.strip()
    df["study_hours"] = pd.to_numeric(df["study_hours"], errors="coerce")
    df["student_id"] = df["student_id"].astype("Int64").astype(str)
    df["week"] = df["week"].astype("Int64")

    numeric_cols = [
        "study_hours",
        "sleep_hours",
        "stress_level",
        "attendance_rate",
        "screen_time_hours",
        "caffeine_intake",
        "learning_efficiency",
        "fatigue_index",
        "quiz_score",
        "assignment_score",
        "performance_index",
    ]
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    df["real_fatigue"] = df["stress_level"] / (df["sleep_hours"] + 1)
    df["risk_level"] = (
        (df["real_fatigue"] > 0.9)
        & (df["sleep_hours"] < 6.3)
        & (df["stress_level"] > 6.8)
    ).astype(int)

    q1 = df["performance_index"].quantile(0.25)
    q2 = df["performance_index"].quantile(0.50)
    q3 = df["performance_index"].quantile(0.75)

    def categorize_student(row):
        if row["performance_index"] >= q3:
            return "Excelente"
        if row["performance_index"] >= q2:
            return "Alto"
        if row["performance_index"] >= q1:
            return "Medio"
        return "Bajo"

    df["student_profile"] = df.apply(categorize_student, axis=1)
    return df


st.title("Panel de Control: Análisis de Desempeño")
st.markdown(
    "Explorá el rendimiento académico con filtros dinámicos y métricas clave.")

df = load_data()

st.sidebar.header("Filtros")

# Contador de reinicio: al cambiarlo, todos los sliders se crean de nuevo
if "reset_n" not in st.session_state:
    st.session_state.reset_n = 0

week_min, week_max = int(df["week"].min()), int(df["week"].max())
week_range = st.sidebar.slider(
    "Semana", week_min, week_max, (week_min, week_max),
    key=f"reset_week_{st.session_state.reset_n}")

perf_min, perf_max = float(df["performance_index"].min()), float(
    df["performance_index"].max())
perf_range = st.sidebar.slider(
    "Performance Index",
    perf_min,
    perf_max,
    (perf_min, perf_max),
    key=f"reset_perf_{st.session_state.reset_n}",
)

stress_min, stress_max = float(
    df["stress_level"].min()), float(df["stress_level"].max())
stress_range = st.sidebar.slider(
    "Nivel de estrés",
    stress_min,
    stress_max,
    (stress_min, stress_max),
    key=f"reset_stress_{st.session_state.reset_n}",
)

sleep_min, sleep_max = float(
    df["sleep_hours"].min()), float(df["sleep_hours"].max())
sleep_range = st.sidebar.slider(
    "Horas de sueño",
    sleep_min,
    sleep_max,
    (sleep_min, sleep_max),
    key=f"reset_sleep_{st.session_state.reset_n}",
)

attendance_min, attendance_max = float(
    df["attendance_rate"].min()), float(df["attendance_rate"].max())
attendance_range = st.sidebar.slider(
    "Asistencia",
    attendance_min,
    attendance_max,
    (attendance_min, attendance_max),
    key=f"reset_attendance_{st.session_state.reset_n}",
)

st.sidebar.markdown("---")
if st.sidebar.button("Restablecer filtros", use_container_width=True):
    st.session_state.reset_n += 1
    st.rerun()

df_filtered = df[
    (df["week"].between(week_range[0], week_range[1]))
    & (df["performance_index"].between(perf_range[0], perf_range[1]))
    & (df["stress_level"].between(stress_range[0], stress_range[1]))
    & (df["sleep_hours"].between(sleep_range[0], sleep_range[1]))
    & (df["attendance_rate"].between(attendance_range[0], attendance_range[1]))
]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Registros filtrados", len(df_filtered))
with col2:
    st.metric("Promedio rendimiento", round(
        df_filtered["performance_index"].mean(), 2))
with col3:
    risk_pct = (df_filtered["risk_level"].mean()
                * 100) if len(df_filtered) else 0
    st.metric("% en riesgo", f"{risk_pct:.1f}%")
with col4:
    st.metric("Promedio estrés", round(df_filtered["stress_level"].mean(), 2))

st.divider()

# Gráfico 1: Histograma de rendimiento
st.subheader("Distribución del Performance Index")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.histplot(df_filtered["performance_index"], bins=20,
             kde=True, color="steelblue", ax=ax1)
ax1.set_xlabel("Performance Index")
ax1.set_ylabel("Cantidad de registros")
st.pyplot(fig1)

# Gráfico 2: Estrés vs rendimiento
st.subheader("Estrés vs Rendimiento")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.scatterplot(data=df_filtered, x="stress_level",
                y="performance_index", alpha=0.4, ax=ax2)
sns.regplot(data=df_filtered, x="stress_level",
            y="performance_index", scatter=False, color="red", ax=ax2)
ax2.set_xlabel("Nivel de estrés")
ax2.set_ylabel("Performance Index")
st.pyplot(fig2)

# Gráfico 3: Sueño vs rendimiento
st.subheader("Sueño vs Rendimiento")
fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.scatterplot(data=df_filtered, x="sleep_hours",
                y="performance_index", alpha=0.4, ax=ax3)
sns.regplot(data=df_filtered, x="sleep_hours",
            y="performance_index", scatter=False, color="green", ax=ax3)
ax3.set_xlabel("Horas de sueño")
ax3.set_ylabel("Performance Index")
st.pyplot(fig3)

# Gráfico 4: Boxplot por perfil
st.subheader("Rendimiento por perfil de estudiante")
fig4, ax4 = plt.subplots(figsize=(8, 4))
sns.boxplot(data=df_filtered, x="student_profile",
            order=["Bajo", "Medio", "Alto", "Excelente"],
            y="performance_index", palette="viridis", ax=ax4)
ax4.set_xlabel("Perfil")
ax4.set_ylabel("Performance Index")
ax4.grid(True, alpha=0.3, axis="y")
st.pyplot(fig4)

# Gráfico 5: Evolución semanal
st.subheader("Evolución semanal de estrés y sueño")
fig5, axes = plt.subplots(1, 2, figsize=(14, 4))
sns.lineplot(data=df_filtered, x="week", y="stress_level", errorbar=None,
             marker="o", color="coral", label="Estrés promedio", ax=axes[0])
axes[0].set_title("Evolución del nivel de estrés")
axes[0].set_xlabel("Semana")
axes[0].set_ylabel("Nivel de estrés promedio")
axes[0].legend()
axes[0].grid(True, alpha=0.3)
sns.lineplot(data=df_filtered, x="week", y="sleep_hours", errorbar=None,
             marker="o", color="steelblue", label="Sueño promedio", ax=axes[1])
axes[1].set_title("Evolución de horas de sueño")
axes[1].set_xlabel("Semana")
axes[1].set_ylabel("Horas de sueño promedio")
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig5)

st.divider()
st.subheader("Vista previa de datos")
st.dataframe(df_filtered.head(50), use_container_width=True)

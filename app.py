import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Automotive Data Explorer",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2. IDENTIDADE VISUAL
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #F5F7FB;
    }

    [data-testid="stSidebar"] {
        background-color: #17243A;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    .main-title {
        font-size: 34px;
        font-weight: 750;
        color: #17243A;
        margin-bottom: 0;
    }

    .subtitle {
        color: #64748B;
        font-size: 15px;
        margin-bottom: 25px;
    }

    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E5EAF1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .kpi-label {
        color: #64748B;
        font-size: 13px;
        font-weight: 600;
    }

    .kpi-value {
        color: #17243A;
        font-size: 27px;
        font-weight: 750;
        margin-top: 7px;
    }

    .section-title {
        color: #17243A;
        font-size: 21px;
        font-weight: 700;
        margin-top: 20px;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3. CARREGAMENTO DOS DADOS
# --------------------------------------------------

@st.cache_data
def load_data():
    data = pd.read_csv("vehicles.csv")

    data["date_posted"] = pd.to_datetime(
        data["date_posted"], errors="coerce"
    )

    numeric_columns = [
        "price", "model_year", "odometer",
        "cylinders", "days_listed"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )

    return data


try:
    car_data = load_data()
except Exception as error:
    st.error(f"Não foi possível carregar os dados: {error}")
    st.stop()

# --------------------------------------------------
# 4. CABEÇALHO
# --------------------------------------------------

st.markdown(
    '<p class="main-title">🚗 AUTOMOTIVE DATA EXPLORER</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Interactive analytics of the used vehicle market</p>',
    unsafe_allow_html=True
)

st.markdown("---")

# --------------------------------------------------
# 5. FILTROS LATERAIS
# --------------------------------------------------

st.sidebar.title("⚙️ Filtros")
st.sidebar.caption("Personalize sua análise")

filtered_data = car_data.copy()


def category_filter(data, column, label):
    options = sorted(
        data[column].dropna().astype(str).unique().tolist()
    )

    selected = st.sidebar.multiselect(
        label,
        options=options,
        default=[]
    )

    if selected:
        return data[data[column].astype(str).isin(selected)]

    return data


filtered_data = category_filter(
    filtered_data, "type", "Tipo de veículo"
)

filtered_data = category_filter(
    filtered_data, "condition", "Condição"
)

filtered_data = category_filter(
    filtered_data, "fuel", "Combustível"
)

filtered_data = category_filter(
    filtered_data, "transmission", "Transmissão"
)

# Filtro de preço
price_min = int(car_data["price"].min())
price_max = int(car_data["price"].max())

price_range = st.sidebar.slider(
    "Faixa de preço (US$)",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max),
    step=500
)

filtered_data = filtered_data[
    filtered_data["price"].between(
        price_range[0], price_range[1]
    )
]

# Filtro de ano
year_min = int(car_data["model_year"].min())
year_max = int(car_data["model_year"].max())

year_range = st.sidebar.slider(
    "Ano do veículo",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

filtered_data = filtered_data[
    filtered_data["model_year"].between(
        year_range[0], year_range[1]
    )
]

st.sidebar.markdown("---")
st.sidebar.caption(
    f"Anúncios após os filtros: {len(filtered_data):,}"
)

# --------------------------------------------------
# 6. INDICADORES PRINCIPAIS
# --------------------------------------------------

st.markdown(
    '<p class="section-title">Indicadores do mercado</p>',
    unsafe_allow_html=True
)

if filtered_data.empty:
    st.warning("Nenhum anúncio encontrado para os filtros selecionados.")
    st.stop()

total_ads = len(filtered_data)
median_price = filtered_data["price"].median()
median_year = filtered_data["model_year"].median()
median_odometer = filtered_data["odometer"].median()

kpis = [
    ("TOTAL DE ANÚNCIOS", f"{total_ads:,}"),
    ("PREÇO MEDIANO", f"US$ {median_price:,.0f}"),
    ("ANO MEDIANO", f"{median_year:.0f}"),
    ("ODÔMETRO MEDIANO", f"{median_odometer:,.0f}")
]

columns = st.columns(4)

for column, (label, value) in zip(columns, kpis):
    with column:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# 7. DISTRIBUIÇÃO DOS PREÇOS
# --------------------------------------------------

st.markdown(
    '<p class="section-title">Análise de preços</p>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    fig_price = px.histogram(
        filtered_data,
        x="price",
        nbins=50,
        title="Distribuição dos preços",
        labels={"price": "Preço (US$)", "count": "Anúncios"},
        color_discrete_sequence=["#2563EB"]
    )

    fig_price.update_layout(
        template="plotly_white",
        showlegend=False
    )

    st.plotly_chart(fig_price, width="stretch")

with col2:
    price_by_condition = (
        filtered_data.groupby("condition", observed=True)["price"]
        .median()
        .reset_index()
        .sort_values("price", ascending=True)
    )

    fig_condition = px.bar(
        price_by_condition,
        x="price",
        y="condition",
        orientation="h",
        title="Preço mediano por condição",
        labels={
            "price": "Preço mediano (US$)",
            "condition": "Condição"
        },
        color="price",
        color_continuous_scale="Blues"
    )

    fig_condition.update_layout(
        template="plotly_white",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_condition, width="stretch")

# --------------------------------------------------
# 8. PREÇO E CARACTERÍSTICAS DOS VEÍCULOS
# --------------------------------------------------

st.markdown(
    '<p class="section-title">Preço e características dos veículos</p>',
    unsafe_allow_html=True
)

col3, col4 = st.columns(2)

with col3:
    fig_odometer = px.scatter(
        filtered_data,
        x="odometer",
        y="price",
        color="type",
        opacity=0.55,
        title="Preço versus leitura do odômetro",
        labels={
            "odometer": "Leitura do odômetro",
            "price": "Preço (US$)",
            "type": "Tipo"
        },
        hover_data=["model", "model_year"]
    )

    fig_odometer.update_layout(template="plotly_white")
    st.plotly_chart(fig_odometer, width="stretch")

with col4:
    year_price = (
        filtered_data.groupby("model_year")["price"]
        .median()
        .reset_index()
        .sort_values("model_year")
    )

    fig_year = px.line(
        year_price,
        x="model_year",
        y="price",
        markers=True,
        title="Preço mediano por ano de fabricação",
        labels={
            "model_year": "Ano de fabricação",
            "price": "Preço mediano (US$)"
        }
    )

    fig_year.update_traces(line_color="#2563EB")
    fig_year.update_layout(template="plotly_white")
    st.plotly_chart(fig_year, width="stretch")

# --------------------------------------------------
# 9. ANÁLISE POR CATEGORIA
# --------------------------------------------------

st.markdown(
    '<p class="section-title">Perfil dos anúncios</p>',
    unsafe_allow_html=True
)

col5, col6 = st.columns(2)

with col5:
    fuel_data = (
        filtered_data["fuel"]
        .value_counts()
        .reset_index()
    )

    fuel_data.columns = ["fuel", "quantity"]

    fig_fuel = px.pie(
        fuel_data,
        names="fuel",
        values="quantity",
        hole=0.48,
        title="Distribuição por combustível"
    )

    fig_fuel.update_layout(template="plotly_white")
    st.plotly_chart(fig_fuel, width="stretch")

with col6:
    type_data = (
        filtered_data.groupby("type")
        .size()
        .reset_index(name="quantity")
        .sort_values("quantity", ascending=True)
    )

    fig_type = px.bar(
        type_data,
        x="quantity",
        y="type",
        orientation="h",
        title="Anúncios por tipo de veículo",
        labels={
            "quantity": "Quantidade de anúncios",
            "type": "Tipo de veículo"
        },
        color="quantity",
        color_continuous_scale="Blues"
    )

    fig_type.update_layout(
        template="plotly_white",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_type, width="stretch")

# --------------------------------------------------
# 10. EVOLUÇÃO DOS ANÚNCIOS
# --------------------------------------------------

st.markdown(
    '<p class="section-title">Evolução temporal</p>',
    unsafe_allow_html=True
)

date_data = filtered_data.dropna(
    subset=["date_posted"]
).copy()

if not date_data.empty:
    date_data["month"] = (
        date_data["date_posted"].dt.to_period("M").astype(str)
    )

    monthly_data = (
        date_data.groupby("month")
        .size()
        .reset_index(name="quantity")
    )

    fig_month = px.bar(
        monthly_data,
        x="month",
        y="quantity",
        title="Quantidade de anúncios por mês",
        labels={
            "month": "Mês",
            "quantity": "Quantidade de anúncios"
        },
        color_discrete_sequence=["#2563EB"]
    )

    fig_month.update_layout(template="plotly_white")
    st.plotly_chart(fig_month, width="stretch")

# --------------------------------------------------
# 11. TABELA DE ANÚNCIOS
# --------------------------------------------------

st.markdown(
    '<p class="section-title">Explorar anúncios</p>',
    unsafe_allow_html=True
)

available_columns = [
    "price", "model_year", "model", "condition",
    "cylinders", "fuel", "odometer",
    "transmission", "type", "paint_color",
    "date_posted", "days_listed"
]

display_columns = [
    column for column in available_columns
    if column in filtered_data.columns
]

st.dataframe(
    filtered_data[display_columns]
    .sort_values("price", ascending=False),
    width="stretch",
    hide_index=True
)

# --------------------------------------------------
# 12. RODAPÉ
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Automotive Data Explorer | Data analysis with "
    "Python, Pandas, Plotly and Streamlit"
)

# Import the libraries we need
import plotly.express as px
import pandas as pd
import plotly.io as pio
pio.renderers.default = "browser"

# Load the data
df = pd.read_csv("Gender_StatsCSV.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Identify year columns (World Bank style)
year_cols = [c for c in df.columns if c.isdigit()]

# Convert from wide to long
df_long = df.melt(
    id_vars=["Country Name", "Indicator Name"],
    value_vars=year_cols,
    var_name="Year",
    value_name="Value"
)

# Fix types
df_long["Year"] = pd.to_numeric(df_long["Year"], errors="coerce")
df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")

# Filter for specific countries, years, and indicators
countries = ["United States", "Honduras", "Philippines"]
years = [2020, 2021, 2022]

indicator_keywords = [
    "A woman can be \"head of household\" in the same way as a man",
    "Decision maker about a woman's own health care: mainly wife"
]

mask_ind = False
for kw in indicator_keywords:
    mask_ind |= df_long["Indicator Name"].str.contains(kw, case=False, na=False)

df_filtered = df_long[
    df_long["Country Name"].isin(countries)
    & df_long["Year"].isin(years)
    & mask_ind
].copy()

# Create the bar chart
fig = px.bar(
    df_filtered,
    x="Country Name",
    y="Value",
    color="Indicator Name",
    barmode="group",
    facet_col="Year",
    title="Gender & Development Indicators Across Countries and Years"
)

fig.write_html("gender_indicators.html")
print("Saved chart to gender_indicators.html")



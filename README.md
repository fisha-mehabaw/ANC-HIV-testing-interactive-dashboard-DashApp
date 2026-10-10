# ANC HIV Testing — Interactive Data Dashboard

An interactive **public-health data visualization dashboard** built with **Python, Dash, Plotly, and Pandas** to explore HIV testing indicators among pregnant women attending antenatal care (ANC). The application provides country-level trends, comparisons between countries, continent-level summaries, and a geographic visualization.

> **Purpose:** Exploratory visualization of ANC HIV-testing indicators. This dashboard is not a clinical decision-support tool or a validated epidemiological reporting system.

## Features

- **Country trends:** Select a country and indicator to view annual changes in a Plotly line chart.
- **Country comparisons:** Select multiple countries to compare the same indicator over time.
- **Continent summaries:** Use a year slider to view continent-level totals in a bar chart and a pie chart.
- **Geographic visualization:** Explore a choropleth map associated with continent-level HIV-testing totals.
- **Interactive controls:** Searchable dropdown menus and a year slider update visualizations through Dash callbacks.

## Indicators

The dataset contains two related indicators:

1. **Number of pregnant women presenting at ANC who were tested for HIV or already knew their HIV-positive status.**
2. **Percentage of pregnant women presenting at ANC who were tested for HIV or already knew their HIV-positive status.**

These indicators capture both testing and already-known positive status. The percentage should not be interpreted simply as the proportion of women receiving a new HIV test during the visit.

## Tech Stack

| Component | Technology |
| --- | --- |
| Programming language | Python |
| Interactive web dashboard | Dash |
| Layout and styling | Dash Bootstrap Components (LUMEN theme) |
| Charts and geographic visualization | Plotly Express |
| Data manipulation | Pandas and NumPy |

The source also imports Matplotlib, although the displayed charts are implemented with Plotly.

## Repository Structure

```text
ANC-HIV-testing-interactive-dashboard-DashApp/
├── dashApp.py                  # Application, preprocessing, layout, callbacks
└── HIV_ANC_Testing_2024.csv    # Input data
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/fisha-mehabaw/ANC-HIV-testing-interactive-dashboard-DashApp.git
cd ANC-HIV-testing-interactive-dashboard-DashApp
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install dash dash-bootstrap-components pandas numpy plotly matplotlib
```

> The repository currently does not provide a pinned `requirements.txt`. The command above installs the libraries imported by `dashApp.py`; exact package versions have not been verified.

### 4. Run the application

```bash
python dashApp.py
```

Open the local address printed in the terminal (typically `http://127.0.0.1:8050/`). The CSV must remain alongside `dashApp.py`, because the source loads it using a relative file path.

## How to Use

1. **Country analysis:** Choose a country and select the number or percentage indicator. Inspect the yearly line chart.
2. **Country comparison:** Choose multiple countries and an indicator. Compare trajectories on a shared chart.
3. **Continent analysis:** Move the year slider to update continent-level bar and pie charts.
4. **Geographic view:** Inspect the choropleth for the selected year, keeping its aggregation limitation in mind (see below).

## Data

The included file, `HIV_ANC_Testing_2024.csv`, contains columns for:

- `ISO3`, `Type`, `Country/Region`, and `UNICEF Region`
- `Indicator` and `Data source`
- `Year` and `Value`

The rows identify **Global AIDS Monitoring** and **Global AIDS Monitoring and UNAIDS 2024 estimates** as data sources, depending on the indicator. The CSV filename contains “2024,” but this does **not** mean all observations are from 2024; the visible records include historical years.

The app standardizes indicator labels, converts the `Value` column to numeric, and assigns countries to continents using predefined lookup sets.

## Data Processing and Interpretation Caveats

The code currently applies the following transformations to reported values:

- Strings with commas are converted into numeric values.
- Values containing `<1` and values equal to `.` are converted to `0.0`.
- Values containing `>95` are replaced by a random choice among `96`, `97`, `98`, and `99`.
- Countries not found in the manually maintained continent mapping are categorized as `Unknown`.

**Important:** Converting suppressed or missing values to zero, and randomly replacing bounded percentages, can misrepresent source data and make results non-reproducible. A stronger analytical version should preserve these values as missing or censored, record the original text, and apply a documented handling policy.

The continent charts sum the count indicator by mapped continent. The choropleth then assigns each country its **continent's aggregate value**, rather than a country-specific value. It should therefore not be interpreted as a country-level testing map.

The code also has a possible callback error when the country or indicator dropdown is empty: its empty-state branch returns two chart objects although the callback declares one output. The normal selected-country path returns one chart.

## Potential Improvements

- Correct the handling of missing, suppressed, and bounded source values.
- Replace the continent-aggregate choropleth with country-level values, or change the visualization/labels to make the aggregate geography explicit.
- Add a pinned `requirements.txt` and automated tests for preprocessing and callbacks.
- Improve empty-selection handling and validate the country-to-continent mapping.
- Add documentation for data provenance, coverage, and update frequency.
- Add dashboard screenshots and a hosted demo link if deployed.

## Project Skills Demonstrated

**Data preprocessing · Interactive dashboards · Exploratory data analysis · Time-series visualization · Geographic visualization · Python · Pandas · Plotly · Dash · Public-health indicators**

## Author

**Fisha Mehabaw Alemayoh**  
[GitHub: fisha-mehabaw](https://github.com/fisha-mehabaw)

## Disclaimer

This is a portfolio and exploratory analytics project. Indicator definitions, missing-data treatment, geographic aggregations, and source revisions should be validated before using any output for research, program evaluation, or policy decisions.

## License

No license file is currently visible in the repository. Reuse permissions have therefore not been specified.

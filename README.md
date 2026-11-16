# AI-Powered EDA & Dashboard Generator

Public repository: [abhishekgb1/ai-eda-dashboard](https://github.com/abhishekgb1/ai-eda-dashboard)

An intelligent exploratory data analysis tool that uses **Google Gemini** to decide _what_ to analyse, while computing every number from the real data in Python — **zero hallucinated numbers**.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Smart Analysis** | Upload CSV/Excel → Gemini designs KPIs, charts & insights |
| **Data Copilot** | Ask follow-up questions using aggregate dataset statistics and validated analysis results |
| **Data Quality Report** | Check completeness, missing values, duplicates, constant columns, and potential IQR outliers |
| **Sample Dataset** | Explore the dashboard immediately with the included sales dataset |
| **Filtered CSV Export** | Download the rows selected by the sidebar filters |
| **No Hallucinated Numbers** | Every KPI and chart is computed from real data via pandas/Plotly |
| **Interactive Charts** | Dark-themed Plotly charts with zoom, hover, and export |
| **10 Chart Types** | Bar, line, scatter, histogram, box, pie, heatmap, treemap, sunburst, funnel |
| **Dynamic Filters** | Sidebar filter widgets auto-generated from your data |
| **KPI Deltas** | Up/down indicators comparing mean vs median, etc. |
| **Tabbed Layout** | Clean result organisation: KPIs → Charts → Insights → Code → Image |
| **Auto-Retry** | Exponential backoff on transient API errors (429/500/502/503) |
| **Analysis Caching** | Same prompt on the same file returns instantly without re-calling Gemini |
| **Smart Date Handling** | Auto-detects date columns and resamples line charts appropriately |
| **EDA Code Export** | One-click Python script generation (pandas + matplotlib) |
| **Dashboard Mockup** | AI-generated stylised dashboard image (Gemini image model) |

---

## 🔐 Data and privacy

Uploads are processed by the Streamlit app in memory for analysis and filtering. When you run an AI analysis, Gemini receives a dataset profile that includes column names, summary statistics, category counts, and a small sample of rows. Data Copilot sends aggregate profile statistics and the chat questions, without raw rows. Do not upload confidential or personal data. The app does not save uploaded files or generated scripts to disk.

## 📁 Project Structure

```
ai-eda-dashboard/
├── app.py                          # Streamlit UI + orchestration
├── config.py                       # API key & model config (secrets + .env)
├── requirements.txt
├── .env.example                    # Template for local development
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example        # Template for Streamlit Cloud
├── utils/
│   ├── __init__.py
│   ├── data_loader.py              # File loading, date parsing, profiling
│   ├── prompts.py                  # Prompt templates for Gemini tasks
│   ├── gemini_client.py            # Gemini client with retry + profile trimming
│   ├── eda_engine.py               # Validation, KPIs, charts (10 types)
│   ├── filters.py                  # Dynamic sidebar filter builder
│   └── data_quality.py             # Deterministic quality checks
└── outputs/
    ├── generated_code/             # Saved EDA scripts (gitignored)
    └── generated_images/           # Saved dashboard images (gitignored)
```

---

## 🚀 Local Setup

### 1. Install Python dependencies

Use Python 3.10 or newer. Open a terminal in the project folder (the folder containing `app.py`) and run:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Configure API key

Copy `.env.example` to `.env` and add your [Google AI Studio API key](https://aistudio.google.com/apikey). Do not overwrite an existing `.env` file.

```powershell
Copy-Item .env.example .env
# Edit .env and set GEMINI_API_KEY=your-key
```

### 3. Run

```powershell
python -m streamlit run app.py
```

The app opens at `http://localhost:8501`. Uploading and exploring data works without an API key; Gemini-powered analysis and generation require `GEMINI_API_KEY`.

---

## ☁️ Streamlit Community Cloud Deployment

1. Connect this GitHub repository on [Streamlit Community Cloud](https://share.streamlit.io/) and choose `main` and `app.py`.
2. Add your Gemini key in the app's **Settings → Secrets** panel:

   ```toml
    GEMINI_API_KEY = "your-gemini-api-key-here"
   ```

3. Deploy. `config.py` reads `st.secrets` first, so the key stays out of the repository.

---

## 🔒 How "No Hallucinated Numbers" Works

```
User request  ──►  Build data profile (pandas)
                        │
                        ▼
               Send profile to Gemini  ──►  Gemini returns a PLAN (JSON)
                                               │
                                               ▼
                                     Validate plan in Python
                                     (drop bad columns / types)
                                               │
                                               ▼
                                     Compute KPIs  ← pandas (real data)
                                     Build charts  ← Plotly  (real data)
                                               │
                                               ▼
                                     Display results in Streamlit
```

Gemini **never** computes or states a numeric value. It only decides _what_ to compute. Every number on screen comes from `pandas` running against the real DataFrame.

---

## 🔄 Resilience Features

- **Auto-retry** with exponential backoff (1s → 2s → 4s) for status codes 429, 500, 502, 503, 504
- **Token budget guard** automatically trims large profiles to prevent context-window overflows
- **Malformed JSON handling** — catches JSONDecodeError and prompts the user to retry
- **Column validation** — silently drops any Gemini suggestion referencing non-existent columns
- **Analysis caching** — re-running the same prompt on the same file uses cached results

---

## 📝 License

MIT

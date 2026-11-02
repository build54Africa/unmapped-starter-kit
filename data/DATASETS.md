# Unmapped starter datasets

These files are open, need no account or API key, and were checked on 2 November 2026. Each "What's missing" note is a gap you could close during Unmapped. Start from the sample for your area, or bring your own data.

Every sample opens in the [starter notebook](https://colab.research.google.com/github/build54Africa/unmapped-starter-kit/blob/main/notebooks/unmapped_starter.ipynb) with two settings: DATA_SOURCE = "sample" and your SAMPLE_AREA. To load one yourself, start with import pandas as pd. When you publish an improved copy, list the source and its licence in your [data card](../templates/DATA_CARD.md).

## Health

**Start here: [Rwanda Healthsites](https://data.humdata.org/dataset/rwanda-healthsites)** — a small list of mapped health facilities with coordinates and service fields.

```python
df = pd.read_csv("https://data.humdata.org/dataset/67ca8390-678a-4eb0-8c06-a12d86df1033/resource/752482cc-e7a0-4898-8653-113d0373fba6/download/rwanda.csv")
```

- **Format:** CSV, about 247 KB. **Licence:** [Open Data Commons ODbL v1.0](https://opendatacommons.org/licenses/odbl/1-0/).
- **What's missing:** Many facilities have blank fields for beds, staffing, opening hours, electricity, water, accessibility and services, and community-mapped places may be incomplete or stale.

### More health data

- [Kenya Healthsites](https://data.humdata.org/dataset/kenya-healthsites) — mapped health facilities across Kenya; CSV, about 513 KB; [ODbL v1.0](https://opendatacommons.org/licenses/odbl/1-0/). **What's missing:** Staffing, stock-outs, prices, queues and even operating status are often absent or unevenly maintained.
- [Nigeria Healthsites](https://data.humdata.org/dataset/nigeria-healthsites) — mapped health facilities across Nigeria; CSV, about 1.32 MB; [ODbL v1.0](https://opendatacommons.org/licenses/odbl/1-0/). **What's missing:** Rural facilities and details about staff, costs, medicines and waiting times can be missing.

## Food and farming

**Start here: [Kenya - Food Prices](https://data.humdata.org/dataset/wfp-food-prices-for-kenya)** — monthly prices for foods and other essentials in selected markets from 2006 to 2026.

```python
df = pd.read_csv("https://data.humdata.org/dataset/e0d3fba6-f9a2-45d7-b949-140c455197ff/resource/517ee1bf-2437-4f8c-aa1b-cb9925b9d437/download/wfp_food_prices_ken.csv")
```

- **Format:** CSV, about 3.69 MB. **Licence:** [CC BY 3.0 IGO](https://creativecommons.org/licenses/by/3.0/igo/).
- **What's missing:** Selected markets can miss farm-gate prices, remote markets, informal trading and household transport costs.

### More food and farming data

- [Nigeria - Food Prices](https://data.humdata.org/dataset/wfp-food-prices-for-nigeria) — market prices from 2002 to 2026; CSV, about 10.78 MB; [CC BY 3.0 IGO](https://creativecommons.org/licenses/by/3.0/igo/). **What's missing:** Coverage is uneven across states and time, with no direct measure of storage losses or trader margins.
- [Rwanda - Food Prices](https://data.humdata.org/dataset/wfp-food-prices-for-rwanda) — market prices from 2000 to 2026; CSV, about 20.03 MB; [CC BY 3.0 IGO](https://creativecommons.org/licenses/by/3.0/igo/). **What's missing:** Not every market is observed every month, and local farm-gate, storage and transport conditions are not measured.

## Climate

**Start here: [NASA POWER daily weather near Nairobi](https://power.larc.nasa.gov/docs/services/api/temporal/daily/)** — daily maximum temperature and precipitation for one modeled grid cell near Nairobi, 2000–2025.

```python
df = pd.read_csv("https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M_MAX,PRECTOTCORR&community=AG&longitude=36.817&latitude=-1.286&start=20000101&end=20251231&format=CSV", skiprows=10)
```

- **Format:** CSV, about 195 KB. **Licence:** [NASA Earth Science Data and Information Policy](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-information-guidance), free and unrestricted use.
- **What's missing:** One modeled grid cell cannot show neighborhood heat, flash flooding or weather across Kenya's varied terrain.

### More climate data

- [NASA POWER daily weather near Lagos](https://power.larc.nasa.gov/docs/services/api/temporal/daily/) — daily maximum temperature and precipitation for 2000–2025; CSV, about 195 KB; [NASA data policy](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-information-guidance). **What's missing:** One grid cell misses drainage, coastal exposure, informal-settlement heat and conditions across Nigeria.
- [NASA POWER daily weather near Kigali](https://power.larc.nasa.gov/docs/services/api/temporal/daily/) — daily maximum temperature and precipitation for 2000–2025; CSV, about 196 KB; [NASA data policy](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-information-guidance). **What's missing:** The coarse cell misses hill-by-hill rain, landslide exposure, drainage failures and household impacts.

## Learning

**Start here: [Primary school completion rate](https://ourworldindata.org/grapher/school-completion)** — annual modeled completion rates for every country, including Nigeria, Kenya and Rwanda, from 1981 to 2025. The notebook keeps just those three.

```python
df = pd.read_csv("https://ourworldindata.org/grapher/school-completion.csv?v=1&csvType=full&useColumnShortNames=false", storage_options={"User-Agent": "Mozilla/5.0"})
```

- **Format:** CSV, about 177 KB. **Licence:** [CC BY 3.0 IGO](https://databrowser.uis.unesco.org/terms-and-conditions).
- **What's missing:** Completion does not show whether pupils learned, repeated grades, faced disability barriers or lacked devices and data; many values are modeled.

### More learning data

- [Children one year before primary school who are out of school](https://ourworldindata.org/grapher/children-not-in-school) — national out-of-school rates for every country, with few years for Nigeria, Kenya and Rwanda; CSV, about 81 KB; [CC BY 3.0 IGO](https://databrowser.uis.unesco.org/terms-and-conditions). **What's missing:** National averages and sparse years hide district, disability, gender, displacement and household-cost barriers.
- [Adult literacy rate](https://ourworldindata.org/grapher/literacy) — basic adult literacy observations for every country, including the three; CSV, about 59 KB; [CC BY 3.0 IGO](https://databrowser.uis.unesco.org/terms-and-conditions). **What's missing:** Surveys are rare and inconsistent, and basic literacy does not show practical, digital or language-specific skills.

## Money and work

**Start here: [Mobile money account usage](https://ourworldindata.org/grapher/mobile-money-account-usage)** — a small Global Findex file with national survey waves of mobile money use for every country that has them, including Nigeria, Kenya and Rwanda.

```python
df = pd.read_csv("https://ourworldindata.org/grapher/mobile-money-account-usage.csv?v=1&csvType=full&useColumnShortNames=false", storage_options={"User-Agent": "Mozilla/5.0"})
```

- **Format:** CSV, about 8 KB. **Licence:** [CC BY 4.0](https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets).
- **What's missing:** A few survey waves cannot show agent reliability, fees, failed transactions, gender gaps or people who share phones and accounts.

### More money and work data

- [Share of workers in vulnerable employment](https://ourworldindata.org/grapher/share-in-vulnerable-employment) — annual ILO and World Bank modeled estimates for every country, 1991–2025; CSV, about 205 KB; [CC BY 4.0](https://datacatalog.worldbank.org/search/dataset/0037712/World-Development-Indicators). **What's missing:** National estimates cannot reveal daily earnings, unpaid work, job security, seasonal shocks or local forms of informality.
- [Employment-to-population ratio](https://ourworldindata.org/grapher/employment-to-population-ratio) — annual modeled employment rates for every country, 1991–2025; CSV, about 188 KB; [CC BY 4.0](https://datacatalog.worldbank.org/search/dataset/0037712/World-Development-Indicators). **What's missing:** Being employed says nothing about hours, income, safety, benefits, unpaid family work or whether a job is formal.

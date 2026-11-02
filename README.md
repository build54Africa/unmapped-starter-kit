# Unmapped starter kit

**If it isn't in the data, AI can't see it.**

Unmapped is a one-week Build54 challenge with [Adaption](https://adaptionlabs.ai) for builders in Nigeria, Kenya and Rwanda. Pick an impact area, map a real problem with data, and ship a product that puts that data in someone's hands. Then Build54 votes.

This kit has what you need for each day. No code is needed, and if you do code, the starters are ready to run.

## What's inside

| Day | Task | Use |
|---|---|---|
| Monday | Find it: your problem brief | [Problem brief template](templates/PROBLEM_BRIEF.md) |
| Tuesday | Map it: your adapted dataset | [Starter datasets](data/DATASETS.md) and the [data card template](templates/DATA_CARD.md) |
| Tuesday | Run it through the API | [Starter notebook](notebooks/unmapped_starter.ipynb), or [open it in Colab](https://colab.research.google.com/github/build54Africa/unmapped-starter-kit/blob/main/notebooks/unmapped_starter.ipynb) |
| Wednesday and Thursday | Find the insight, then build it | Adaption Visualize, and the [product starter](product/README.md) |
| Friday | Ship it: the reality check | [Reality check template](templates/REALITY_CHECK.md) |

## Before you start

- **Credits.** Adaption adds $800 in API credits to the Adaption account that uses your registration email. When you register on [Build54](https://build54.com/challenges), tick "Share my registration details with event partners" so we can send your email to Adaption, then sign up to Adaption with the same email.
- **Your API key.** Create it in Adaption under Settings, then API keys. Keep it in Colab secrets or an environment variable. Never paste it into code, a chat or a screenshot.
- **No personal data.** Datasets, products and write-ups must not include names, phone numbers, exact home locations or ID numbers of private people.

## Impact areas

- **Health:** where care doesn't reach, such as distance to clinics, stock-outs, costs and waiting times.
- **Food and farming:** what the harvest depends on, such as prices, rainfall, pests, storage and market access.
- **Climate:** who the weather hits first, through floods, heat, air and water.
- **Learning:** who school leaves behind, through access, outcomes, dropout, devices and data.
- **Money and work:** the economy nobody counts, such as informal work, incomes, prices and mobile money.

## Run your data through Adaption

1. [Open the notebook in Colab](https://colab.research.google.com/github/build54Africa/unmapped-starter-kit/blob/main/notebooks/unmapped_starter.ipynb) and save a copy to your Google Drive (File, then Save a copy in Drive).
2. Add your API key as a Colab secret called `ADAPTION_API_KEY`: click the key icon on the left.
3. Run the cells from top to bottom. The notebook checks your data, shows the credit estimate first, and spends credits only when you switch it on.
4. Share your copy (Share, then "Anyone with the link") and paste that link into the Build54 task.

## Build your product

Click **Use this template** at the top of this page to get your own copy of the kit, then follow the [product starter](product/README.md). It covers a web app, a Telegram bot and a no-code route.

## For maintainers

- `python notebooks/test_notebook.py` runs every notebook cell with a fake Adaption SDK that mirrors adaption 0.17.1. It makes no API calls.
- `python notebooks/check_samples.py` loads every sample dataset through the notebook's own code.
- `python data/verify_datasets.py` rechecks every dataset link.
- `python -m pytest -q product/tests` tests the product starter.

The datasets keep their own licences, listed in [DATASETS.md](data/DATASETS.md). Everything else here is MIT licensed.

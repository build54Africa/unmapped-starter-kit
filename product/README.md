# Product starter

Build it on Wednesday and Thursday: a product that puts your adapted data in someone's hands. It has to be live, work without you, and use your data. Pick one of three ways.

## 1. A web app (Streamlit)

[app.py](app.py) is a working web app. It searches your data, adds a filter for every column with a few repeated values, draws a map when your data has coordinates, compares a number across groups and lets people download what they found.

1. Put your adapted dataset in this folder as `data.csv`. Excel and JSON work too; change `DATA_FILE` in app.py.
2. Change the four settings at the top of app.py: the title, a one-line introduction, the file name and the note about where the data comes from.
3. Try it on your computer:

   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

4. Put it online for free. Get your own copy of the kit with **Use this template** on its GitHub page, commit your `data.csv` and settings to it, then sign in at [share.streamlit.io](https://share.streamlit.io) with GitHub, create an app from your repository and set the main file to `product/app.py`. You get a public link to paste into Build54.

## 2. A Telegram bot

[bot.py](bot.py) answers messages with matching rows from `data.csv`, using the same search as the web app. The steps are at the top of the file: get a token from @BotFather, save it as `TELEGRAM_BOT_TOKEN`, then run `python bot.py`. The bot answers while the program runs, so keep it on a server, or a free host, for the vote weekend.

WhatsApp bots need a Meta business account and approval, which rarely fits into one week. Telegram is the quick route.

## 3. No code

No code is needed. Either of these counts, as long as the product is live and uses your data.

- **An AI app builder.** Copy the prompt below, fill in the brackets and attach your adapted CSV.
- **A spreadsheet app.** Put your data in Google Sheets and connect it to a no-code app builder that reads sheets. Most offer a free plan with a public link.

Prompt for an AI app builder:

> Build a simple, mobile-friendly web app called [name] for [who it's for] in [place]. It uses the attached CSV of [what the data is], with these columns: [columns]. People should be able to search by [column], filter by [column], see the results on a map using the [latitude] and [longitude] columns, and see [the number that matters] for each row. Show where the data comes from at the bottom: [source and a link to your data card]. Keep the words short and plain. Do not ask people for personal details.

## Before you share it

- Your app shows your adapted data, not the example rows in data.csv.
- The data note at the bottom names your source and links your data card.
- Nothing in it reveals personal details, and no API key or token is in your code.

## Tests

`pip install pytest`, then `python -m pytest -q tests` checks the search, filters, map columns, bot replies and the web app itself.

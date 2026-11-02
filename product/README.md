# Product starter

Build it on Wednesday and Thursday: a product that puts your adapted data in someone's hands. It has to be live, work without you, and use your data. The web app is the quickest route to a public link that stays up through the vote, and it works entirely in your browser.

## 1. A web app, all in your browser

[app.py](app.py) is a working web app. It searches your data, adds a filter for every column with a few repeated values, draws a map when your data has coordinates, compares a number across groups and lets people download what they found. You change a few lines of settings; no installs.

1. On the kit's GitHub page, click **Use this template**, then **Create a new repository**. You now have your own copy.
2. In your copy, open the `product` folder, click **Add file**, then **Upload files**, and upload your adapted dataset named `data.csv`. It replaces the example rows.
3. Open `product/app.py`, click the pencil icon and change the settings at the top: the title, a one-line introduction, the note about where the data comes from, and `SHOW_COLUMNS`, the columns people may see. Click **Commit changes**.
4. Sign in at [share.streamlit.io](https://share.streamlit.io) with GitHub, create an app from your repository and set the main file path to `product/app.py`. After a few minutes you get a public link. Paste it into Build54 as your live link.

To change the app later, edit the files on GitHub; the live app updates on its own.

## 2. The same web app on your computer

For trying changes quickly. You need Python 3.10 or newer.

```bash
cd product
pip install -r requirements.txt
streamlit run app.py
```

## 3. A Telegram bot

[bot.py](bot.py) answers messages with matching rows from `data.csv`, using the same search as the web app. The steps are at the top of the file: get a token from @BotFather, save it as `TELEGRAM_BOT_TOKEN`, then run it:

```bash
cd product
pip install -r requirements.txt
python bot.py
```

The bot only answers while that program runs, so voters can try it only if a computer keeps running it through the vote weekend. If your team has no computer that can stay on, build the web app instead. WhatsApp bots need a Meta business account and approval, which rarely fits into one week.

## 4. No code

AI app builders and no-code tools count too, as long as the product is live, uses your adapted data and has a public link that stays up through the vote weekend. Check the free plan before you start. To use an AI app builder, copy this prompt, fill in the brackets and attach your adapted CSV:

> Build a simple, mobile-friendly web app called [name] for [who it's for] in [place]. It uses the attached CSV of [what the data is], with these columns: [columns]. People should be able to search by [column], filter by [column], see the results on a map using the [latitude] and [longitude] columns, and see [the number that matters] for each row. Show only these columns: [columns]. Show where the data comes from at the bottom: [source and a link to your data card]. Keep the words short and plain. Do not ask people for personal details.

## Before you share it

- Your product shows your adapted data, not the example rows in data.csv.
- `SHOW_COLUMNS` lists only what people need, and nothing reveals personal details.
- The note at the bottom names your source and links your data card.
- No API key or token is written in your code.

## Tests

```bash
cd product
pip install -r requirements.txt pytest
python -m pytest -q tests
```

They check the search, filters, map columns, bot replies and the web app itself.

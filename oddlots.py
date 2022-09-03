# -*- encoding: utf-8 -*-

import os
import shutil
from datetime import date, timedelta
import secedgar.cik_lookup
from secedgar import filings
from secedgar.exceptions import EDGARQueryError
from discord_webhook import DiscordWebhook

# Change these accordingly
SEC_USER_AGENT = os.environ.get("SEC_USER_AGENT", "Your Name (me@example.com)")
TMP_FOLDER_NAME = os.environ.get("TMP_FOLDER_NAME", "tmp")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "REPLACE WITH DISCORD WEBHOOK URL")

def get_all_filings(date_to_download: date):
    """
    Downloads all filings from the given date
    :param date_to_download:
    :return:
    """
    daily_filings = filings(start_date=date_to_download,
                            end_date=date_to_download,
                            user_agent=SEC_USER_AGENT,
                            entry_filter=lambda f: any(
                                x in f.form_type.lower() for x in ("sc to", "sc13e4", "sc14d", "424b3"))
                            )
    try:
        daily_filings.save(TMP_FOLDER_NAME,
                           dir_pattern="{cik}")
    except EDGARQueryError:
        print("Keine Filings für den gegebenen Tag!")

def get_ticker(cik: str) -> str:
    """
    Returns the ticker to the given CIK
    :param cik: cik to get ticker from
    :return: ticker
    """
    result = [k for k, v in secedgar.cik_lookup.get_cik_map().get("ticker").items() if v == cik]
    return result[0] if (len(result)) > 0 else "einen unbekannten Ticker"

def find_odd_lots():
    """
    Searches through all previously downloaded files and finds all documents mentioning "odd lots"
    """
    if not os.path.exists(TMP_FOLDER_NAME):
        return
    for root, dirs, files in os.walk(TMP_FOLDER_NAME, topdown=False):
        for name in files:
            with open(os.path.join(root, name)) as f:
                if "odd lot" in f.read().lower():
                    send_message_to_discord(os.path.basename(root))
    shutil.rmtree(TMP_FOLDER_NAME)

def send_message_to_discord(cik: str):
    """
    Sends a message to the given Discord channel
    :param cik: CIK of the company where an odd lots arbitrage has been found
    """
    ticker = get_ticker(cik)
    webhook = DiscordWebhook(
        url=DISCORD_WEBHOOK_URL,
        content=f"Eine neue Odd Lots Arbritage wurde für **{ticker}** gefunden. "
                f"Hier gehts zu den Filings: https://www.sec.gov/edgar/search/#/entityName={int(cik):010}")
    webhook.execute()

if __name__ == "__main__":
    get_all_filings(date.today() - timedelta(1))
    find_odd_lots()

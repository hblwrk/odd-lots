# Odd Lots

A script to find odd lots arbitrage opportunities by scanning SEC filings. 

## Setup

1. Install python and the required dependencies
2. Change the constants in `oddlots.py` or set them as environment variables to run the script
   1. `SEC_USER_AGENT` is a custom user agent. See https://www.sec.gov/os/webmaster-faq#developers for further details.
   2. `TMP_FOLDER_NAME` is the path of the folder where the filings will be downloaded to. The script auto-deletes the folder each run.
   3. `DISCORD_WEBHOOK_URL` is the webhook url of the channel to send the messages to if any odd lots filings are found.

## Usage

`python oddlots.py` to run the script. As it checks the filings of the previous day, it is advised to run it in an automated cronjob to check for all filings from yesterday.

### Container

If you prefer using a OCI container, run `docker build .`. Environment variables need to be injected when launching the container, for example `docker run -e SEC_USER_AGENT=... -e DISCORD_WEBHOOK_URL=... containername`.

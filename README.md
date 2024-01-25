# SeedBot2000
## About
This silly little robot rolls random flagsets for FF6WC, as well as some other fun little extra things. You can see SeedBot in action on the [FF6WC Discord](https://discord.gg/5MPeng5). You can also invite SeedBot to your own server by [clicking here](https://discord.com/api/oauth2/authorize?client_id=892560638969278484&permissions=1494917180496&scope=bot).

If you want to run your own instance of SeedBot, read below.

## Installation
* Clone this repository
* Create a .env file in the main directory with the following:
    * DISCORD_TOKEN='Your Discord bot token'
    * new_api_key='Your API key for api.ff6worldscollide.com'
    * dev_api_key='Your API key for devapi.ff6worldscollide.com'
* Initialize and update the submodules with:
    * ```git submodule init```
    * ```git submodule update --recursive```
* Add the folder `\seeds` to `\WorldsCollide`
* Add your FF6 rom named `ff3.smc` to `\WorldsCollide`
* If you want to utilize the seed-writing function(s), enable them by uncommenting the following lines at the bottom of the `parse_commands.py` file:
    * JSON metric file (local): `functions.update_metrics(m)`
    * Google Sheets (additional setup required): `write_gsheets(m)`
        * For Google Sheets integration, you'll need to set up a service account with Google to enable SeedBot to write to your Google Sheet. Lots of information on the web about setting this up. Replace the `service_file` in `db\metric_writer.py` with your key file.
* Run `bot.py` and enjoy!

DiscordCoronaBotNL

Discord bot created to scrape the data from https://github.com/J535D165/CoronaWatchNL twice a day (to prevent flooding) and collect the number of hospitalized people per municipality.

When user in discord writes !corona <municipality(gemeente)> the bot will respond with number of hospitalized cases..

Also implemented is !corona <municipality> <days in history> to show differences between now and days specified.
And we have !corona graphs to show graphs as a .png on discord.

To use the bot for yourself you need to create an account to get a secret key store this in your .env file.

https://pypi.org/project/pbwrap/ library explanation on keycreation and pastebin for python use https://realpython.com/how-to-make-a-discord-bot-python/ has a nice description on how-to set discord up.

--disclaimer-- It is still work in progress
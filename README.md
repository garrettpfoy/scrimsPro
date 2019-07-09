# ScrimsPro
Discord Bot made to handle scrims, and private games hosted via discord.

Commands:
- !help (Bring up help menu)
- !website (Shows website info)
- !email (Presents business email)
- !discord (Retrieves discord invite link)
- !admin (Brings up admin menu)
- !admin broadcast (Sends an announcement from the bot)
- !admin push (Sends an update, formatted, from the bot)
- !ticket (Creates a private ticket, used to get help from admins)
- !admin mark [w-, p-, r-] (Marks a ticket as Waiting, Pending, or Resolved)
- !participation check (Sends a message in a config'd channel polling whether or not there are enough players to start a scrim)
- !admin prefix [Prefix] (Sets a new prefix, default is !)
- !queue start (Starts a queue, kicks off a bunch of methods)
- !admin status [New Status] (Changes the status of the bot, AKA the playing message)
- !admin close (Closes a ticket)


About:
To start a queue, use the !queue start. Once this is done, the following steps happen

1) The Queue is announced, and a latancy-adjusted countdown begins.

2) Once the countdown is finished, the channel is unlocked, and users can enter in their game codes

3) Once the time for game-code entry is finished, the bot deletes all the messages, and creates an embed with all of the teams, and codes

4) If the requeue requests become more then entries, the queue starts over.

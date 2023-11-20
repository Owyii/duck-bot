# duck-bot
A small project to get some experience and telegram scraper bot. Develop is slow and im bad at coding so you are warned.

It use a plugin structure, so every supported site will have a plugin.py file that implement all the logics.

## USAGE
### Python lib
Install the required lib with:   
`pip install -r requirements.txt`
### Telegram information
Fill the example.env file with the information needed for the telegram bot  
and rename it into `.env`  

**API_ID** = The id give by the botfather bot  
You can get the next two here: https://my.telegram.org/apps  
**API_HASH** = App api_hash  
**BOT_TOKEN** = App api_id

Creating an app is needed to overcome the upload limits.
### How to use
Simply paste a link into the chat of the bot, if it is supported it will dowload the media correlated

## PLUGIN PROGRESS
1. `https://bunkrr.su/` Kinda work, some error with the album part 

## TODO
1. Fixing README
2. Create and mantaining requirement.txt
3. Clear the old crawler and develop them into the new system
4. Automate the plugin template to show an example
5. Explain how to install the bot and how tu put credentials


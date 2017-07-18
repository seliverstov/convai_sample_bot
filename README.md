# Sample bot for convai.io challenge
Bot demonstrates how to use RouterBot API to communicate with telegram users. Currently bot works only with dedicated instance of RouterBot (see BOT_URL) and has fixed id (see BOT_ID). Do not run many instances of bot. Bot support only one dialogue at a time. 

## Clone repo
```sh
git clone https://github.com/seliverstov/convai_sample_bot/
cd convai_sample_bot
```
## Edit bot.py and enter your bot token (id)
```python
def main():
    """
    !!!!!!! Put your bot token (id) here !!!!!!!
    """
    BOT_ID = None
```
## Run bot (python 3 required)
```sh
python bot.py
```
## Start chattings
Open telegram client, find @ConvaiBot (convai-bot), send "/test PUT_YOUR_BOT_ID_HERE" to start chatting with your own bot

>**WARNING:** if you start chatting with command / begin @ConvaiBot will connect your with random bot or human. To evaluate your own bot you should use the command /test with your bot id

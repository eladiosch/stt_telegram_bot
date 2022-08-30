# 1. Introduction

This is a simple Telegram bot that receives audio files and converts them to text using the Google speech recognition.

The libraries used are `python-telegram-bot` for the bot creation, `SpeechRecognition` for the speech to text conversion and `ffmpy` to convert the audio to `wav`.

# 2. Configuration and language support

To make this bot work, you need to set a `TOKEN` variable in the `bot_config.py` file. Get this token creating a telegram bot with [@BotFather](https://t.me/BotFather).

In the `bot_config.py` file, you can set the language that the bot will use to convert the audio to text. This will also be the language that the bot will use to reply to the user. By default there's `es-ES` for Spanish and `en-US` for English. If you use a different one, Google will probably recognise it, but the bot will still reply in english unless you create a new texts file for the language.

# 3. Limitations

Since this is using the Google speech recognition service, their limitations apply. There's a 20 MB limit for the audio files (after conversion to `wav`) so if they're longer than 2 minutes it probably won't work.
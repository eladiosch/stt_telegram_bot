import logging

from bot_config import TOKEN
from functools import wraps
from stt import process_audio
from telegram import (
    ChatAction,
    Update,
)
from telegram.ext import (
    Filters,
    MessageHandler,
    Updater,
)

from texts_manager import get_text, init_texts

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TEXTS = None

def send_typing_action(func):
    """
    This decorator will act as the bot is typing while processing request
    """

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

def help(update, context):
    """ Shows some text to explain the user how to use the bot """
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_text('help'), parse_mode='html')

@send_typing_action
def audio_manager(update: Update, context) -> None:
    """Manages an audio file."""
    logger.info('Audio file received')
    if update.message.voice:
        logger.info('Voice received')
        file = update.message.voice.get_file()
    elif update.message.audio:
        logger.info('Audio received')
        file = update.message.audio.get_file()
    else:
        logger.info('Unknown audio received')
        context.bot.send_message(chat_id=update.effective_chat.id, text=get_text('unrecognised_audio'), reply_to_message_id=update.message.message_id)
        return

    context.bot.send_message(chat_id=update.effective_chat.id, text=get_text('processing'))
    audio_text = process_audio(file)
    if not audio_text:
        audio_text = get_text('empty_audio')
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'{get_text("result")}{audio_text}', reply_to_message_id=update.message.message_id)

def main():
    """ Controls the flow of the bot """

    init_texts()

    logger.info('Bot starts!')

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text | Filters.command, help))
    dispatcher.add_handler(MessageHandler(Filters.voice | Filters.audio, audio_manager))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
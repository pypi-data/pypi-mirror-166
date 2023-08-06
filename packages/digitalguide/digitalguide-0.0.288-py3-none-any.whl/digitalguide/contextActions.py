from telegram import (Update)
from telegram.ext import (CallbackContext)

from digitalguide.twilio.TwilioUpdate import TwilioUpdate


def telegram_default_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.from_user.first_name


def twilio_default_name(client, update: TwilioUpdate, context):
    context["name"] = update.ProfileName


def telegram_save_text_to_context(update: Update, context: CallbackContext, key):
    context.user_data[key] = update.message.text


def twilio_save_text_to_context(client, update: TwilioUpdate, context, key):
    context[key] = update.Body


def telegram_save_value_to_context(update: Update, context: CallbackContext, key, value):
    context.user_data[key] = value


def twilio_save_value_to_context(client, update: TwilioUpdate, context, key, value):
    context[key] = value


telegram_action_functions = {"default_name": telegram_default_name,
                             "save_text_to_context": telegram_save_text_to_context,
                             "save_value_to_context": telegram_save_value_to_context
                             }

twilio_action_functions = {"default_name": twilio_default_name,
                             "save_text_to_context": twilio_save_text_to_context,
                             "save_value_to_context": twilio_save_value_to_context
                             }

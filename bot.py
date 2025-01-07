import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from database import get_user_points, add_points, subtract_points, save_user_info

# تنظیمات لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# دستور شروع ربات
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    save_user_info(user_id)  # ذخیره اطلاعات اولیه کاربر
    welcome_message = """سلام به ARTA خوش آمدید! لطفاً از دکمه‌های زیر استفاده کنید تا تجربه بهتری داشته باشید."""

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("چالش‌های روزانه", callback_data='daily_challenges')],
        [InlineKeyboardButton("مشاهده امتیازات", callback_data='view_points')],
        [InlineKeyboardButton("دریافت انیمیشن خوش‌آمدگویی", callback_data='send_gif')]
    ])
    
    update.message.reply_text(welcome_message, reply_markup=reply_markup)

# ارسال انیمیشن
def send_gif(update: Update, context: CallbackContext):
    update.message.reply_animation(animation="https://example.com/your_animation.gif")

# مشاهده امتیازات
def view_points(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    points = get_user_points(user_id)
    update.callback_query.answer()
    update.callback_query.edit_message_text(f"مجموع امتیازات شما: {points} امتیاز")

# چالش‌های روزانه
def handle_challenges(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text(
        "چالش روزانه: دعوت 3 نفر به ربات! امتیاز دریافتی: 1000 امتیاز"
    )

# مدیریت امتیازات و جوایز
def claim_rewards(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    points = get_user_points(user_id)
    if points >= 5000:
        update.callback_query.answer()
        update.callback_query.edit_message_text("شما جایزه ویژه دریافت کردید!")
        subtract_points(user_id, 5000)
    else:
        update.callback_query.answer()
        update.callback_query.edit_message_text("برای دریافت جایزه به امتیاز بیشتری نیاز دارید.")

# اجرای ربات
def main():
    updater = Updater("YOUR_BOT_API_KEY", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(handle_challenges, pattern='daily_challenges'))
    dispatcher.add_handler(CallbackQueryHandler(view_points, pattern='view_points'))
    dispatcher.add_handler(CallbackQueryHandler(claim_rewards, pattern='claim_rewards'))
    dispatcher.add_handler(CallbackQueryHandler(send_gif, pattern='send_gif'))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

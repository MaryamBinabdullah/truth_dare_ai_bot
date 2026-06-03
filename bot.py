import os
import random
import requests
import html
from dotenv import load_dotenv
from telegram.error import BadRequest
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, InlineQueryHandler, ContextTypes
from uuid import uuid4

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

LOCAL_TRUTHS = [
    "What is the most embarrassing thing you have ever Googled at 3 a.m.?",
    "What is a secret you have never told your parents?",
    "Have you ever faked being sick to get out of a social plan?",
    "What is the most childish habit you still have?",
    "Have you ever accidentally sent a text about someone to that exact person?",
    "What is the most embarrassing song or artist on your playlist?",
    "Have you ever stalked an ex on social media from a fake account?",
    "What is the grossest food combination that you secretly love?",
    "What is the biggest lie you have ever told without getting caught?",
    "What is the cheapest or worst gift you have ever given someone?",
    "Have you ever lied about your age online?",
    "What is the most awkward thing that has ever happened to you on a date?",
    "What movie or TV show is your ultimate guilty pleasure?",
    "What is an irrational fear or phobia that you still hold on to?",
    "Have you ever cried during a movie that wasn't supposed to be sad?",
    "Who is the most surprising person to ever slide into your DMs?",
    "Have you ever developed a crush on a coworker or classmate you can't stand?",
    "If you had to delete everyone in this chat from your life except one, who stays?",
    "What is your absolute biggest relationship dealbreaker?",
    "Have you ever ghosted someone because of a completely petty reason?",
    "Who in this chat do you think is the most stylish?",
    "Have you ever told someone 'I love you' without actually meaning it?",
    "Who is one person you pretend to like but secretly cannot stand?",
    "If you could swap lives with one person in this chat for a day, who would it be?",
    "What was your very first impression of me when we first met?",
    "Have you ever dated or liked two people at the exact same time?",
    "Who do you think is the most attractive person currently in this chat?",
    "What is the meanest thing you have ever said behind a close friend's back?",
    "Have you ever stayed in a friendship purely because you were lonely?",
    "If you had to marry an ex, which one would you choose?",
    "What is the pettiest reason you have ever stopped talking to someone?",
    "Who is the first person you look for when you open your chat apps?",
    "Have you ever been caught talking to yourself out loud?",
    "What is something you are deeply jealous of regarding someone else's life?",
    "What is the biggest professional or academic mistake you have ever made?",
    "If you were guaranteed to never get caught, what minor crime would you commit?",
    "What is the most useless, random talent that you possess?",
    "If you could change one physical feature about yourself, what would it be?",
    "What is the single biggest regret you have about your past?",
    "If you won $10 million tomorrow, what is the very first thing you would buy?",
    "Do you believe in ghosts, aliens, or any supernatural entities?",
    "What is a popular opinion or trend that you think is completely overrated?",
    "If you had to change your first name, what name would you choose?",
    "What is something you are deeply insecure about that people wouldn't guess?",
    "If a movie was made about your life, which celebrity would play you?",
    "What is the hardest lesson you have ever had to learn?",
    "What is one goal on your bucket list that you are terrified you won't achieve?",
    "If you could see into the future, what is the one thing you'd want to know?",
    "What is the most impulsive thing you have ever spent money on?",
    "What do you think is the biggest misconception people have about you?",
    "If you had to live in a different country for the rest of your life, where would you go?",
    "What is the best piece of advice you have ever ignored and regretted?",
    "When was the last time you actually cried, and what caused it?",
    "Have you ever taken the blame for something someone else did?",
    "What is something you love to do that your friends would find uncool?",
    "What is the most stubborn thing you have ever done just to prove a point?",
    "Have you ever looked through someone's phone without their permission?",
    "What is the biggest lie you have ever told on a resume or job interview?",
    "Have you ever been kicked out of a venue, bar, or establishment?",
    "Have you ever pretended to know a lot about a topic just to impress a crush?",
    "What is the single most defining moment of your life so far?",
    "If you could remove one person from your past entirely, who would it be?",
    "What is something you are proud of but never bring up because it sounds like bragging?",
    "Have you ever broken a major promise to someone who trusted you?",
    "What is the weirdest dream you can still vividly remember?",
    "Have you ever run away from a situation instead of facing confrontation?",
    "What is a habit you have that you desperately wish you could break?",
    "If you could read minds, whose mind would you want to look into first?",
    "What is the lowest you have ever come to getting in serious trouble?",
    "Have you ever blamed a mistake you made on a pet or a younger sibling?",
    "What is the worst piece of relationship advice you have ever given someone?",
    "Do you talk or walk in your sleep?",
    "What is your go-to excuse when you want to cancel plans at the last minute?",
    "Are you a morning person or an absolute night owl?",
    "What app on your phone currently has the highest screen time?",
    "Do you save text conversations or delete them immediately?",
    "Have you ever tried to look up your own house on Google Maps?",
    "What is the most money you have ever lost or misplaced?",
    "Do you believe in soulmates or is love just timing?",
    "Have you ever fallen asleep in a completely inappropriate public place?",
    "What is the worst haircut or hairstyle you have ever had?",
    "Do you believe that people can truly change, or do they stay the same?",
    "What is your absolute favorite comfort food when you are sad?",
    "Have you ever gotten a tattoo or a piercing that you heavily regret?",
    "Do you check your horoscope or astrology signs regularly?",
    "What is the last thing you bought that was a total waste of cash?",
    "What's the longest you have ever gone without sleeping?",
    "Have you ever ignored a message on purpose and then blamed it on being busy?",
    "What's the absolute worst text message you've ever sent by mistake?",
    "If you could mute one person in this group chat in real life, who would it be?",
    "What's your most useless expensive purchase?",
    "Have you ever created a fake social media account to spy on someone?",
    "What's something you're glad your family doesn't know about you?",
    "What is the most ridiculous rumor you've ever heard about yourself?",
    "Have you ever lied in this game tonight?",
    "What's the most childish thing you still do when nobody is looking?",
    "What's your biggest guilty pleasure song that you'd hide from friends?",
    "Have you ever pretended to be broke to avoid spending money with friends?",
    "What's the worst advice you've ever taken from a friend?",
    "Have you ever re-gifted something that was given to you?",
    "What is the most annoying text habit someone can have?",
    "What's the longest you've gone without checking your phone notifications?",
    "Have you ever un-liked a post because your crush didn't like it?",
    "What is the first thing you notice about someone online?",
    "If your internet history was public, how cooked would you be?"
]

LOCAL_DARES = [
    "Send a random emoji to the 3rd person in your recent private chats.",
    "Post a completely blank story/status on your social media with no context.",
    "Send a 10-second audio note to this chat singing the chorus of your favorite song.",
    "Change your Telegram profile bio to 'I am a secret agent' for the next hour.",
    "Text a close friend 'I know your secret' and post a screenshot of their reaction here.",
    "Send a voice note to this chat speaking in a British accent for the 60 seconds.",
    "Share a screenshot of your screen time breakdown from your settings.",
    "Direct message a random celebrity a paragraph detailing your love for breakfast cereal.",
    "Type out the alphabet backward in this chat as fast as you can in one single message.",
    "Change your Telegram theme or wallpaper to something chosen by the group and proof it with a screenshot.",
    "Send a voice note trying to recite a famous movie monologue from memory.",
    "Send an accidental-looking gibberish text to a family member and show the chat their reply.",
    "Text your best friend 'I'm moving to Mars' out of nowhere and show their reaction.",
    "Send a 15-second voice note of you laughing hysterically for absolutely no reason.",
    "Give a passionate 1-minute text description of why pineapples belong on pizza.",
    "Use only emojis to communicate in this group for the next two rounds.",
    "Send a voice note whispering everything you say for the next minute.",
    "Give a dramatic backhanded compliment to the person who played before you.",
    "Send a text message entirely in rhymes for your next three turns.",
    "Change your Telegram profile picture to a funny meme chosen by the group for the next 24 hours.",
    "Send a voice note imitating a broken record repeating the last word three times.",
    "Send a voice note reciting a popular children's nursery rhyme in an opera voice.",
    "Drop your current top 3 most used emojis into the chat right now.",
    "Send a voice note of your best impression of a chicken laying an egg.",
    "Text a random contact a completely out-of-context movie quote and share the results.",
    "Like the oldest post of a random person on your timeline right now.",
    "Leave an extremely detailed 5-star review for an ordinary item (like a pencil) on Amazon and share the text.",
    "Send a voice note explaining a simple concept (like how water is wet) in a highly dramatic way.",
    "Change your name on Telegram to 'Mystery Player' for the remainder of this game.",
    "Send a voice note mimicking a robot whose batteries are running out.",
    "Text your parents 'I just won the lottery!' and share the screenshot of their response.",
    "Send a funny voice note doing your best impression of a cartoon character.",
    "Type a message to the chat using only your chin or your nose.",
    "Send a link to the most embarrassing YouTube video you can think of.",
    "Send an audio note singing a pop song but replace all the lyrics with the word 'meow'.",
    "Share a screenshot of your phone's home screen configuration.",
    "Write a short, bad poem about the person sitting above you in the chat list.",
    "Send a voice note giving a highly enthusiastic fake review of an imaginary product.",
    "Send a text message to this group where every single word must start with the letter 'S'.",
    "Send a sticker that perfectly describes your current mood without explanation.",
    "Change your Telegram bio to 'DM me for life advice' for the next two hours.",
    "Send a voice note trying to whistle your favorite song completely through.",
    "Confess your deepest, funniest unverified conspiracy theory to the group.",
    "Rate the profile pictures of the last three people who texted in this chat out of 10.",
    "Send a text explaining what you ate for breakfast using only sound effects (onomatopoeias).",
    "Send a voice note explaining your favorite hobby but make it sound illegal.",
    "Text a contact 'Are you mad at me?' out of nowhere and share what they say.",
    "Send a random GIF into the chat and let the group interpret its meaning.",
    "Send a voice note speaking entirely in slow motion for one minute.",
    "Change your text capitalization style to tHiS for the next three rounds.",
    "Send a screenshot of the oldest photo currently stored on your phone.",
    "Type a 30-word story in the chat about a heroic squirrel.",
    "Send a voice note explaining your day entirely through animal noises.",
    "Text a friend 'I found it.' and do not explain what 'it' is for 10 minutes.",
    "Send a link to your absolute favorite meme of all time.",
    "Send a voice note trying to make the sound of a sports car revving its engine.",
    "Use a translator app to translate a phrase into 5 different languages and paste the weird result here.",
    "Compliment the person you talk to the least in this group chat.",
    "Send a text message explaining your favorite movie using absolutely no nouns.",
    "Send a 10-second voice note of you trying to speak while holding your nose shut.",
    "Describe your dream partner using only corporate or business jargon.",
    "Text a random contact 'Quick, hide the evidence!' and post the screenshot.",
    "Send a voice note singing the alphabet song as fast as you humanly can.",
    "Rate your own cooking skills out of 10 and justify it in one sentence.",
    "Send a message entirely in UPPERCASE for the next two rounds.",
    "Share a screenshot of your most frequently used app list from settings.",
    "Send a voice note explaining how to make coffee but pretend you're a mad scientist.",
    "Text a friend 'Where are you? I'm outside' when you are actually home, and share their response.",
    "Send an emoji that you have never used before in your life.",
    "Send a voice note trying to mimic the noise of an old dial-up internet connection.",
    "Create a custom nickname for everyone in this group chat right now.",
    "Send a text detailing your ideal superhero superpower and your ridiculous weakness.",
    "Send a voice note in a whisper explaining why you love sleep.",
    "Share the title of the last Wikipedia article you read.",
    "Text a sibling or friend 'I lost my phone' and post their reaction when they reply.",
    "Send a GIF that represents what you think the year 3000 looks like.",
    "Send a voice note explaining your favorite video game using only bad descriptions.",
    "Send a message using zero spaces between your words for the next round.",
    "Text a friend 'Can I borrow your cat?' and show the chat their response.",
    "Send an audio note listing 5 items within arm's reach of you right now in a auctioneer voice.",
    "Change your profile status text to 'Loading...' for the next hour.",
    "Send a text describing your absolute worst fashion choice from your childhood.",
    "Send a voice note explaining why aliens definitely exist or definitely don't.",
    "Rank the top 3 best movies of all time in the chat right now.",
    "Send a text message using only punctuation marks to describe your mood.",
    "Text a contact 'Happy New Year!' out of context right now and show the screenshot.",
    "Send a voice note counting to 20 but skip all numbers that have a 3 or 7 in them.",
    "Describe the color blue to a blind person using text in the chat.",
    "Send a GIF of your favorite dance move.",
    "Text a friend 'Do you want to build a snowman?' and share their response.",
    "Send a voice note reading the latest news headline in a dramatic radio host voice.",
    "Give a 1-minute text tutorial on how to breathe properly.",
    "Send a screenshot of your phone's battery percentage right now.",
    "Text a contact 'I'm a wizard, Harry' and see what they say.",
    "Send a voice note talking while yawning throughout the entire thing.",
    "Describe your morning routine using only action movie vocabulary.",
    "Send a text detailing the weirdest dream you remember having this week.",
    "Text a random friend 'I'm buying a goat' and share the screenshot.",
    "Send a voice note explaining why water is the best beverage on earth.",
    "Send a GIF that represents your exact reaction if you won a million dollars.",
    "Describe your favorite food using only adjectives.",
    "Text a friend 'Are you awake?' at this exact second and show the screenshot response.",
    "Send a voice note saying the tongue twister 'Peter Piper picked a peck of pickled peppers' three times fast.",
    "Send a text message in all lowercase with no punctuation for the next two rounds.",
    "Share a link to a song that makes you feel like a main character."
]

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes button presses and edits the message in place safely using HTML."""
    query = update.callback_query
    await query.answer() 
    
    user = query.from_user
    user_name = html.escape(user.first_name)
    player_html = f'<a href="tg://user?id={user.id}">{user_name}</a>'
    
    try:
        if query.data == "get_truth":
            truth_text = generate_truth()
            await query.edit_message_text(
                text=f"❓ {player_html} <b>chose Truth:</b>\n\n<i>{html.escape(truth_text)}</i>\n\nSelect the next turn:",
                reply_markup=get_game_keyboard(),
                parse_mode="HTML"
            )
            
        elif query.data == "get_dare":
            dare_text = generate_dare()
            await query.edit_message_text(
                text=f"🎲 {player_html} <b>chose Dare:</b>\n\n<i>{html.escape(dare_text)}</i>\n\nSelect the next turn:",
                reply_markup=get_game_keyboard(),
                parse_mode="HTML"
            )
            
        elif query.data == "get_menu":
            await query.edit_message_text(
                text="🎲 <b>AI Truth or Dare Game</b>\n\nSelect an option below to play:",
                reply_markup=get_game_keyboard(),
                parse_mode="HTML"
            )
            
    except BadRequest as e:
        if "Message is not modified" in str(e):
            pass
        else:
            raise e

def generate_ai_text(prompt, fallback_pool):
    url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"
    headers = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
    formatted_prompt = (
        f"<|im_start|>system\nYou are a group party game assistant. Generate one completely unique, "
        f"creative text item. Max 80 characters. It MUST be fully playable online via text or voice note. "
        f"Do NOT generate physical real-life actions. Output ONLY the response text itself, no quotes.\n<|im_end|>\n"
        f"<|im_start|>user\n{prompt} (Seed: {random.randint(1, 100000)})\n<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )
    payload = {"inputs": formatted_prompt, "parameters": {"max_new_tokens": 40, "temperature": 0.95, "return_full_text": False}}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=8)
        if response.status_code == 200:
            result = response.json()
            return result[0]['generated_text'].strip().strip('"').strip("'").split('\n')[0]
        return random.choice(fallback_pool)
    except:
        return random.choice(fallback_pool)

def generate_dare():
    return generate_ai_text("Give me a brand new, hilarious dare playable entirely via Telegram text or voice note.", LOCAL_DARES)

def generate_truth():
    return generate_ai_text("Give me an interesting, creative truth question playable over a chat application.", LOCAL_TRUTHS)

def get_game_keyboard():
    keyboard = [
        [InlineKeyboardButton("❓ Truth", callback_data="get_truth"), InlineKeyboardButton("🎲 Dare", callback_data="get_dare")],
        [InlineKeyboardButton("🔄 Reset Menu", callback_data="get_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 <b>Welcome to AI Truth or Dare!</b> 🔥\n\n"
        "Ready to spice up the chat? You can play right here, "
        "or bring the game into <i>any</i> conversation with your friends!\n\n"
        "🎮 <b>How to play right now:</b>\n"
        "Tap <b>Truth</b> or <b>Dare</b> below to get an instant, AI-generated prompt!\n\n"
        "🚀 <b>How to play in other chats:</b>\n"
        "Type <code>@truth_dare_ai_bot truth</code> or <code>@truth_dare_ai_bot dare</code> "
        "in any chat box and watch the magic happen!",
        reply_markup=get_game_keyboard(),
        parse_mode="HTML"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ <b>How to Play:</b>\n\n"
        "1. <b>In this Chat:</b> Use /start and click the interactive menu buttons.\n"
        "2. <b>In Friends' DMs (Inline Mode):</b> Type <code>@YourBotName truth</code> or <code>@YourBotName dare</code> in any chat window, wait 1 second, and tap the pop-up to send a prompt!",
        parse_mode="HTML"
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    user_name = html.escape(user.first_name)
    player_html = f'<a href="tg://user?id={user.id}">{user_name}</a>'
    
    if query.data == "get_truth":
        truth_text = generate_truth()
        await query.edit_message_text(
            text=f"❓ {player_html} <b>chose Truth:</b>\n\n<i>{html.escape(truth_text)}</i>\n\nSelect the next turn:",
            reply_markup=get_game_keyboard(), parse_mode="HTML"
        )
    elif query.data == "get_dare":
        dare_text = generate_dare()
        await query.edit_message_text(
            text=f"🎲 {player_html} <b>chose Dare:</b>\n\n<i>{html.escape(dare_text)}</i>\n\nSelect the next turn:",
            reply_markup=get_game_keyboard(), parse_mode="HTML"
        )
    elif query.data == "get_menu":
        await query.edit_message_text(
            text="🎲 <b>AI Truth or Dare Game</b>\n\nSelect an option below to play:",
            reply_markup=get_game_keyboard(), parse_mode="HTML"
        )

async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes search queries typed into the message box across any chat."""
    query = update.inline_query.query.lower().strip()
    user_name = html.escape(update.inline_query.from_user.first_name)
    
    results = []

    if not query or "truth" in query:
        truth_prompt = generate_truth()
        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="❓ Share a Truth Prompt",
                description=f"Generate an instant truth for your chat.",
                input_message_content=InputTextMessageContent(
                    message_text=f"❓ <b>{user_name} picked TRUTH:</b>\n\n<i>{html.escape(truth_prompt)}</i>",
                    parse_mode="HTML"
                )
            )
        )

    if not query or "dare" in query:
        dare_prompt = generate_dare()
        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="🎲 Share a Dare Prompt",
                description=f"Generate an instant text/voice dare.",
                input_message_content=InputTextMessageContent(
                    message_text=f"🎲 <b>{user_name} picked DARE:</b>\n\n<i>{html.escape(dare_prompt)}</i>",
                    parse_mode="HTML"
                )
            )
        )

    await update.inline_query.answer(results, cache_time=0)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(InlineQueryHandler(handle_inline_query)) 
    
    print("🤖 Bot with Inline Mode is running successfully!")
    app.run_polling()

if __name__ == "__main__":
    main()
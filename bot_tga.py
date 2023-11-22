import os
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from .env

TOKEN = os.getenv("TELEGRAM_TOKEN")

import sqlite3
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging


# Initialize database
conn = sqlite3.connect("game_awards.db")
cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS user_choices
                  (user_id INTEGER PRIMARY KEY, category TEXT, nominee TEXT)"""
)
conn.commit()

# Define categories and nominees
categories = [
    {
        "category": "Game of the Year",
        "nominees": [
            "Alan Wake 2 (Remedy Entertainment/Epic Games Publishing)",
            "Baldur’s Gate 3 (Larian Studios)",
            "Marvel’s Spider-Man 2 (Insomniac Games/SIE)",
            "Resident Evil 4 (Capcom)",
            "Super Mario Bros. Wonder (Nintendo EPD/Nintendo)",
            "The Legend of Zelda: Tears of the Kingdom (Nintendo EPD/Nintendo)",
        ],
    },
    {
        "category": "Best Game Direction",
        "nominees": [
            "Alan Wake 2 (Remedy Entertainment/Epic Games Publishing)",
            "Baldur’s Gate 3 (Larian Studios)",
            "Marvel’s Spider-Man 2(Insomniac Games/SIE)",
            "Super Mario Bros. Wonder (Nintendo EPD/Nintendo)",
            "The Legend of Zelda: Tears of the Kingdom (Nintendo EPD/Nintendo)",
        ],
    },
    {
        "category": "Best Adaptation",
        "nominees": [
            "Castlevania: Nocturne (Powerhouse Animation/Netflix)",
            "Gran Turismo (PlayStation Productions/Sony Pictures)",
            "The Last of Us (PlayStation Productions/HBO)",
            "The Super Mario Bros. Movie (Illumination/Nintendo/Universal Pictures)",
            "Twisted Metal (PlayStation Productions/Peacock)",
        ],
    },
    {
        "category": "Best Narrative",
        "nominees": [
            "Alan Wake 2 (Remedy Entertainment/Epic Games Publishing)",
            "Baldur’s Gate 3 (Larian Studios)",
            "Cyberpunk 2077: Phantom Liberty (CD Projekt Red)",
            "Final Fantasy XVI (Square Enix)",
            "Marvel’s Spider-Man 2 (Insomniac Games/SIE)",
        ],
    },
    {
        "category": "Best Art Direction",
        "nominees": [
            "Alan Wake 2 (Remedy Entertainment/Epic Games Publishing)",
            "Hi-Fi Rush (Tango Gameworks/Bethesda Softworks)",
            "Lies of P (Round8 Studio/Neowiz Games)",
            "Super Mario Bros. Wonder (Nintendo EPD/Nintendo)",
            "The Legend of Zelda: Tears of the Kingdom (Nintendo EPD/Nintendo)",
        ],
    },
    {
        "category": "Best Score and Music",
        "nominees": [
            "Alan Wake 2, Composer Petri Alanko (Remedy Entertainment/Epic Games Publishing)",
            "Baldur’s Gate 3, Composer Borislav Slavov (Larian Studios)",
            "Final Fantasy XVI, Composer Masayoshi Soken (Square Enix)",
            "Hi-Fi Rush, Audio Director Shuichi Kobori (Tango Gameworks/Bethesda Softworks)",
            "The Legend of Zelda: Tears of the Kingdom, Composed by Nintendo Sound Team (Nintendo EPD/Nintendo)",
        ],
    },
    {
        "category": "Best Audio Design",
        "nominees": [
            "Alan Wake 2 (Remedy Entertainment/Epic Games Publishing)",
            "Dead Space (Motive Studio/EA)",
            "Hi-Fi Rush (Tango Gameworks/Bethesda Softworks)",
            "Marvel’s Spider-Man 2 (Insomniac Games/SIE)",
            "Resident Evil 4 (Capcom)",
        ],
    },
    {
        "category": "Best Performance",
        "nominees": [
            "Ben Starr, Final Fantasy XVI",
            "Cameron Monaghan, STAR WARS Jedi: Survivor",
            "Idris Elba, Cyberpunk 2077: Phantom Liberty",
            "Melanie Liburd, Alan Wake 2",
            "Neil Newbon, Baldur’s Gate 3",
            "Yuri Lowenthal, Marvel’s Spider-Man 2",
        ],
    },
    {
        "category": "Innovation in Accessibility",
        "nominees": [
            "Diablo IV (Blizzard Entertainment)",
            "Forza Motorsport (Turn 10 Studios/Xbox Game Studios)",
            "Hi-Fi Rush (Tango Gameworks/Bethesda Softworks)",
            "Marvel’s Spider-Man 2 (Insomniac Games/SIE)",
            "Mortal Kombat 1 (NetherRealm Studios/WB Games)",
            "Street Fighter 6 (Capcom)",
        ],
    },
    {
        "category": "Games for Impact",
        "nominees": [
            "A Space for the Unbound (Mojiken Studio/Toge Productions/Chorus)",
            "Chants of Sennaar (Rundisc/Focus Entertainment)",
            "Goodbye Volcano High (KO_OP)",
            "Tchia (Awaceb/Kepler Interactive)",
            "Terra Nil (Free Lives/Devolver Digital/Netflix)",
            "Venba (Visai Games)",
        ],
    },
    {
        "category": "Best Ongoing Game",
        "nominees": [
            "Apex Legends (Respawn Entertainment/EA)",
            "Cyberpunk 2077 (CD Projekt Red)",
            "Final Fantasy XIV (Square Enix)",
            "Fortnite (Epic Games)",
            "Genshin Impact (HoYoverse)",
        ],
    },
    {
        "category": "Best Community Support",
        "nominees": [
            "Baldur’s Gate 3 (Larian Studios)",
            "Cyberpunk 2077 (CD Projekt Red)",
            "Destiny 2 (Bungie)",
            "Final Fantasy XIV (Square Enix)",
            "No Man’s Sky (Hello Games)",
        ],
    },
    {
        "category": "Best Independent Game",
        "nominees": [
            "Cocoon (Geometric Interactive/Annapurna Interactive)",
            "Dave the Diver (MINTROCKET)",
            "Dredge (Black Salt Games/Team 17)",
            "Sea of Stars (Sabotage Studio)",
            "Viewfinder (Sad Owl Studios/Thunderful Publishing)",
        ],
    },
    {
        "category": "Best Debut Indie Game",
        "nominees": [
            "Cocoon (Geometric Interactive/Annapurna Interactive)",
            "Dredge (Black Salt Games/Team 17)",
            "Pizza Tower (Tour de Pizza)",
            "Venba (Visai Games)",
            "Viewfinder (Sad Owl Studios/Thunderful Publishing)",
        ],
    },
    {
        "category": "Best Mobile Game",
        "nominees": [
            "Final Fantasy VII: Ever Crisis (Applibot/Square Enix)",
            "Honkai: Star Rail (HoYoverse)",
            "Hello Kitty Island Adventure (Sunblink Entertainment)",
            "Monster Hunter Now (Niantic/Capcom)",
            "Terra Nil (Free Lives/Devolver/Netflix)",
        ],
    },
    {
        "category": "Best VR/AR Game",
        "nominees": [
            "Gran Turismo 7 (Polyphony Digital/SIE)",
            "Humanity (tha LTD/Enhance Games)",
            "Horizon Call of the Mountain (Guerrilla Games/Firesprite/SIE)",
            "Resident Evil Village VR Mode (Capcom)",
            "Synapse (nDreams)",
        ],
    },
    {
        "category": "Best Action Game",
        "nominees": [
            "Armored Core VI: Fires of Rubicon (FromSoftware/Bandai Namco)",
            "Dead Island 2 (Dambuster Studios/Deep Silver)",
            "Ghostrunner 2 (One More Level/505 Games)",
            "Hi-Fi Rush (Tango Gameworks/Bethesda Softworks)",
            "Remnant 2 (Gunfire Games/Gearbox Publishing)",
        ],
    },
    {
        "category": "Best Action/Adventure Game",
        "nominees": [
            "Alan Wake 2 (Remedy Entertainment/Epic Games Publishing)",
            "Marvel’s Spider-Man 2 (Insomniac Games/SIE)",
            "Resident Evil 4 (Capcom)",
            "Star Wars Jedi: Survivor (Respawn Entertainment/EA)",
            "The Legend of Zelda: Tears of the Kingdom (Nintendo EPD/Nintendo)",
        ],
    },
    {
        "category": "Best RPG",
        "nominees": [
            "Baldur’s Gate 3 (Larian Studios)",
            "Final Fantasy XVI (Square Enix)",
            "Lies of P (Round8 Studio/Neowiz Games)",
            "Sea of Stars (Sabotage Studio)",
            "Starfield (Bethesda Game Studios/Bethesda Softworks)",
        ],
    },
    {
        "category": "Best Fighting Game",
        "nominees": [
            "God of Rock (Modus Studios Brazil/Modus Games)",
            "Mortal Kombat 1 (NetherRealm Studios/WB Games)",
            "Nickelodeon All-Star Brawl 2 (Ludosity/Fair Play Labs/GameMill Entertainment)",
            "Pocket Bravery (Statera Studio/PQube)",
            "Street Fighter 6 (Capcom)",
        ],
    },
    {
        "category": "Best Family Game",
        "nominees": [
            "Disney Illusion Island (Dlala Studios/Disney)",
            "Party Animals (Recreate Games)",
            "Pikmin 4 (Nintendo EPD/Nintendo)",
            "Sonic Superstars (Arzest/Sonic Team/Sega)",
            "Super Mario Bros. Wonder (Nintendo EPD/Nintendo)",
        ],
    },
    {
        "category": "Best Sim/Strategy Game",
        "nominees": [
            "Advance Wars 1+2: Re-Boot Camp (WayForward/Nintendo)",
            "Cities: Skylines II (Colossal Order/Paradox Interactive)",
            "Company of Heroes 3 (Relic Entertainment/Sega)",
            "Fire Emblem Engage (Intelligent Systems/Nintendo)",
            "Pikmin 4 (Nintendo EPD/Nintendo)",
        ],
    },
    {
        "category": "Best Sports/Racing",
        "nominees": [
            "EA Sports FC 24 (EA Vancouver/EA Romania/EA Sports)",
            "F1 23 (Codemasters/EA Sports)",
            "Forza Motorsport (Turn 10 Studios/Xbox Game Studios)",
            "Hot Wheels Unleashed 2: Turbocharged (Milestone)",
            "The Crew Motorfest (Ubisoft Ivory Tower/Ubisoft)",
        ],
    },
    {
        "category": "Best Multiplayer Presented by Discord",
        "nominees": [
            "Baldur’s Gate 3 (Larian Studios)",
            "Diablo IV (Blizzard Entertainment)",
            "Party Animals (Recreate Games)",
            "Street Fighter 6 (Capcom)",
            "Super Mario Bros. Wonder (Nintendo EPD/Nintendo)",
        ],
    },
    {
        "category": "Most Anticipated Game",
        "nominees": [
            "Final Fantasy VII Rebirth (Square Enix)",
            "Hades II (Supergiant Games)",
            "Like A Dragon: Infinite Wealth (Ryu Ga Gotoku Studio/Sega)",
            "Star Wars Outlaws (Massive Entertainment/Ubisoft)",
            "Tekken 8 (Bandai Namco/Arika)",
        ],
    },
    {
        "category": "Content Creator of the Year",
        "nominees": ["IronMouse", "PeopleMakeGames", "Quackity", "Spreen", "SypherPK"],
    },
    {
        "category": "Best Esports Game",
        "nominees": [
            "Counter-Strike 2 (Valve)",
            "Dota 2 (Valve)",
            "League of Legends (Riot Games)",
            "PUBG Mobile (LightSpeed Studios/Tencent Games)",
            "Valorant (Riot Games)",
        ],
    },
    {
        "category": "Best Esports Athlete",
        "nominees": [
            "Lee “Faker” Sang-hyeok (League of Legends)",
            "Mathieu “ZywOo” Herbaut (CS:GO)",
            "Max “Demon1” Mazanov (Valorant)",
            "Paco “HyDra” Rusiewiez (Call of Duty)",
            "Park “Ruler” Jae-hyuk (League of Legends)",
            "Phillip ”ImperialHal” Dosen (Apex Legends)",
        ],
    },
    {
        "category": "Best Esports Team",
        "nominees": [
            "Evil Geniuses (Valorant)",
            "Fnatic (Valorant)",
            "Gaimin Gladiators (Dota 2)",
            "JD Gaming (League of Legends)",
            "Team Vitality (Counter-Strike)",
        ],
    },
    {
        "category": "Best Esports Coach",
        "nominees": [
            "Christine “potter” Chi (Evil Geniuses – Valorant)",
            "Danny “zonic” Sorensen (Team Falcons – Counter-Strike)",
            "Jordan “Gunba” Graham (Florida Mayhem – Overwatch)",
            "Remy “XTQZZZ” Quoniam (Team Vitality – Counter-Strike)",
            "Yoon “Homme” Sung-young (JD Gaming – League of Legends)",
        ],
    },
    {
        "category": "Best Esports Event",
        "nominees": [
            "2023 League of Legends World Championship",
            "Blast.tv Paris Major 2023",
            "EVO 2023",
            "The International Dota 2 Championships 2023",
            "Valorant Champions 2023",
        ],
    },
]

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update, context):
    """Send the first category when the command /start is issued."""
    user = update.message.from_user
    context.user_data[user.id] = {"current_category": 0, "selections": {}}
    await send_category(update, context, user.id)


async def send_category(update, context, user_id):
    current_category = context.user_data[user_id]["current_category"]
    category = categories[current_category]

    # Simplifying the nominees' names and creating buttons with one nominee per row
    keyboard = [
        [InlineKeyboardButton(nominee.split(" (")[0], callback_data=str(i))]
        for i, nominee in enumerate(category["nominees"])
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f'Category: {category["category"]}', reply_markup=reply_markup
    )


async def button(update, context):
    """Handle button press."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    current_category = context.user_data[user_id]["current_category"]
    category_name = categories[current_category]["category"]
    selected_nominee_index = int(query.data)
    selected_nominee = categories[current_category]["nominees"][
        selected_nominee_index
    ].split(" (")[0]

    # Save the user's choice to the database
    cursor.execute(
        "INSERT OR REPLACE INTO user_choices (user_id, category, nominee) VALUES (?, ?, ?)",
        (user_id, category_name, selected_nominee_index),
    )
    conn.commit()

    # Update the message to show only the selected option with a checkmark
    keyboard = [
        [InlineKeyboardButton(f"{selected_nominee} ✅", callback_data="selected")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"Category: {category_name}\n\nSelected: {selected_nominee} ✅",
        reply_markup=reply_markup,
    )

    # Move to the next category
    context.user_data[user_id]["current_category"] += 1
    if context.user_data[user_id]["current_category"] < len(categories):
        await send_category(query, context, user_id)
    else:
        await query.edit_message_text(text="Thank you for your selections!")


def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Register handlers directly with the Application object
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    application.run_polling()


if __name__ == "__main__":
    main()

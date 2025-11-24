import asyncio
import logging
import random
import re
from collections import Counter
from datetime import date

from aiogram import Bot, F, Router
from aiogram.exceptions import (
    TelegramAPIError,
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNotFound,
    TelegramRetryAfter,
)
from aiogram.filters import CommandObject, CommandStart
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold
from openai import AsyncOpenAI
from sqlalchemy import select

from database import User, get_or_create_user, session_scope
from tviyastrogid_keyboard import (
    architips_partner_kb,
    architips_q1_kb,
    architips_q2_kb,
    architips_q3_kb,
    architips_q4_kb,
    architips_q5_kb,
    architips_start_kb,
    archetype_test_kb,
    daily_bonus_kb,
    explanation_cards_taro_y_or_n,
    kwiz_question2_inline,
    main_keyboard,
    music_q10_kb,
    music_q11_kb,
    music_q12_kb,
    music_q13_kb,
    music_q14_kb,
    music_q15_kb,
    music_q1_kb,
    music_q2_kb,
    music_q3_kb,
    music_q4_kb,
    music_q5_kb,
    music_q6_kb,
    music_q7_kb,
    music_q8_kb,
    music_q9_kb,
    taro_question1,
    zodiac_keyboard,
)
from config import OPENAI_API_KEY

router = Router()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)
logger = logging.getLogger(__name__)


async def ask_openai(prompt: str, *, temperature: float = 0.7, max_tokens: int = 600) -> str:
    """Uniform wrapper around OpenAI calls for consistent handling."""
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()


ZODIAC_MAP = {
    "zodiac_Овен": "Овен",
    "zodiac_Телець": "Телець",
    "zodiac_Близнюки": "Близнюки",
    "zodiac_Рак": "Рак",
    "zodiac_Лев": "Лев",
    "zodiac_Діва": "Діва",
    "zodiac_Терези": "Терези",
    "zodiac_Скорпіон": "Скорпіон",
    "zodiac_Стрілець": "Стрілець",
    "zodiac_Козеріг": "Козеріг",
    "zodiac_Водолій": "Водолій",
    "zodiac_Риби": "Риби",
}

# ===== States =====
class ProblemState(StatesGroup):
    waiting_for_problem = State()

class DreamState(StatesGroup):
    waiting_for_dream = State()

class ArchetypeTest(StatesGroup):
    person = State()
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()

class ZodiacCompatibility(StatesGroup):
    your_sign = State()
    partner_sign = State()

class regist(StatesGroup):
    name = State()
    zodiak_callback = State()
    zodiak_callback1 = State()

class taro_answer(StatesGroup):
    come_question1 = State()
    answer1 = State()

class AstroChat(StatesGroup):
    waiting_for_question = State()


def spend_cards_if_possible(user_id: int, amount: int) -> bool:
    with session_scope() as session:
        user = session.get(User, user_id)
        if not user or (user.cards or 0) < amount:
            return False
        user.cards = (user.cards or 0) - amount
        return True


def extract_inviter_id(command: CommandObject | None) -> int | None:
    """Extract inviter id from the deep link payload if it contains digits."""
    if not command or not command.args:
        return None
    match = re.search(r"\d+", command.args)
    if not match:
        return None
    try:
        return int(match.group())
    except ValueError:
        return None


@router.message(CommandStart())
async def unified_start_handler(message: Message, command: CommandObject, state: FSMContext):
    user_id = message.from_user.id

    # ===== Визначаємо інвайтера =====
    inviter_id = extract_inviter_id(command)
    logger.info(f"Invited By: {inviter_id}")

    # Забороняємо рефералити себе
    if inviter_id == user_id:
        inviter_id = None

    # Логіка через БД
    with session_scope() as session:
        user = session.get(User, user_id)
        is_new_user = user is None

        if not user:
            # новий юзер
            user = User(id=user_id, cards=50, invited_by=inviter_id)
            session.add(user)
        else:
            # існує, але нема інвайтера і він є в deep link
            if inviter_id and not user.invited_by:
                user.invited_by = inviter_id

        # Інвайтеру нараховуємо тільки якщо юзер новий
        if inviter_id and is_new_user:
            inviter = get_or_create_user(session, inviter_id)
            inviter.cards = (inviter.cards or 0) + 25

    # ===== Привітання =====
    photo = "AgACAgIAAxkBAAIFRGgUnhBhg0pqMszswBANaZYpsCuOAAIb-jEbbpihSGn8T3t5wVOcAQADAgADeQADNgQ"

    await message.answer_photo(
        photo=photo,
        caption="Привіт, це твій персональний АстроГід 🌌\nЯ допоможу тобі дізнатися твою долю."
    )

    zodiac_msg = await message.answer("Обери свій знак зодіаку!", reply_markup=zodiac_keyboard)
    await state.update_data(zodiac_msg_id=zodiac_msg.message_id)
    await state.set_state(regist.zodiak_callback1)


# ===== Zodiac select =====
@router.callback_query(StateFilter(regist.zodiak_callback1))
async def zodiac_callback_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    zodiac_msg_id = data.get("zodiac_msg_id")
    if zodiac_msg_id:
        try:
            await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=zodiac_msg_id)
        except:
            pass

    zodiak = ZODIAC_MAP.get(callback.data)
    if not zodiak:
        await callback.message.answer("Щось пішло не так. Знак не знайдено.")
        await callback.answer()
        return

    user_id = callback.from_user.id
    with session_scope() as session:
        user = get_or_create_user(session, user_id)
        user.zodiac_sign = zodiak

    await callback.message.answer(f"🔮 Прекрасно! Ви обрали знак {zodiak}.")
    await callback.message.answer("Оберіть що вас інтересує в меню знизу", reply_markup=main_keyboard)
    await state.clear()
    await callback.answer()


# ===== Tarot Q&A =====
@router.message(F.text == "🔮 Розклад Таро на запитання – 10🃏")
async def quastion_text(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not spend_cards_if_possible(user_id, 10):
        await message.answer("❌ У вас недостатньо карт! Потрібно 10 🃏.")
        return
    await message.answer("🃏 Напиши своє запитання — і я зроблю розклад, що відкриє приховану суть.")
    await state.set_state(taro_answer.come_question1)

@router.message(StateFilter(taro_answer.come_question1))
async def tarot_reading(message: Message, state: FSMContext):
    await message.answer_photo(
        photo="AgACAgIAAxkBAAIFS2gUn8yWzRsY15lVroUlZOMdLYF_AAL76zEbNX-oSLSquGiNbVxoAQADAgADeQADNgQ",
        caption="🔮 Я розкладаю карти… приготуйся."
    )
    await asyncio.sleep(4)
    await message.answer("✨ Ще трохи…")
    await asyncio.sleep(2)
    tarot_cards = [
        "0. Дурак","I. Маг","II. Верховна Жриця","III. Імператриця","IV. Імператор",
        "V. Ієрофант","VI. Закохані","VII. Колісниця","VIII. Сила","IX. Відлюдник",
        "X. Колесо Фортуни","XI. Справедливість","XII. Повішений","XIII. Смерть",
        "XIV. Уміреність","XV. Диявол","XVI. Вежа","XVII. Зірка","XVIII. Місяць",
        "XIX. Сонце","XX. Суд","XXI. Світ",
        "Туз Жезлів","2 Жезлів","3 Жезлів","4 Жезлів","5 Жезлів","6 Жезлів",
        "7 Жезлів","8 Жезлів","9 Жезлів","10 Жезлів","Паж Жезлів","Лицар Жезлів",
        "Королева Жезлів","Король Жезлів",
        "Туз Кубків","2 Кубків","3 Кубків","4 Кубків","5 Кубків","6 Кубків",
        "7 Кубків","8 Кубків","9 Кубків","10 Кубків","Паж Кубків","Лицар Кубків",
        "Королева Кубків","Король Кубків",
        "Туз Мечів","2 Мечів","3 Мечів","4 Мечів","5 Мечів","6 Мечів",
        "7 Мечів","8 Мечів","9 Мечів","10 Мечів","Паж Мечів","Лицар Мечів",
        "Королева Мечів","Король Мечів",
        "Туз Пентаклів","2 Пентаклів","3 Пентаклів","4 Пентаклів","5 Пентаклів","6 Пентаклів",
        "7 Пентаклів","8 Пентаклів","9 Пентаклів","10 Пентаклів","Паж Пентаклів","Лицар Пентаклів",
        "Королева Пентаклів","Король Пентаклів"
    ]
    random_cards = random.sample(tarot_cards, 3)
    await state.update_data(drawn_cards=random_cards, user_question=message.text)
    await message.answer("🃏 Твій розклад Таро:\n\n" + "\n".join(random_cards),
                         reply_markup=explanation_cards_taro_y_or_n)

@router.callback_query(F.data == "explanation_cards")
async def explanation_cards_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if not spend_cards_if_possible(user_id, 7):
        await callback.message.answer("❌ У вас недостатньо карт! Потрібно 7 🃏.")
        await callback.answer()
        return

    data = await state.get_data()
    cards = data.get("drawn_cards", [])
    question = (data.get("user_question") or "").strip()
    if not cards:
        await callback.message.answer("⚠️ Помилка: карти не знайдено.")
        await callback.answer()
        return
    if not question:
        await callback.message.answer("⚠️ Помилка: не збережено запитання.")
        await callback.answer()
        return

    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    await asyncio.sleep(0.8)

    prompt = (
        "Ти — досвідчений таролог. Людина запитує:\n"
        f"«{question}»\n"
        f"Карти: {', '.join(cards)}.\n"
        "Дай лаконічну, але глибоку відповідь саме на питання. "
        "Не описуй карти окремо — поясни спільний сенс у контексті. "
        "Українською, до 100 слів."
    )

    try:
        result = await ask_openai(prompt, temperature=0.7, max_tokens=600)
        await callback.message.answer(f"📖 Пояснення розкладу:\n\n{result}")
        await state.clear()
    except Exception as e:
        print(f"explanation_cards_handler error: {e}")
        await callback.message.answer("⚠️ Сталася помилка під час пояснення. Спробуй ще раз.")
    finally:
        await callback.answer()


# ===== Palm reading =====
@router.message(F.text == "✋ Гадання на лодоні – 30🃏")
async def scan_palm(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not spend_cards_if_possible(user_id, 30):
        await message.answer("❌ У вас недостатньо карт! Потрібно 30 🃏.")
        return

    await message.answer_photo(
        photo="AgACAgIAAxkBAAIFs2gUu7wz1RWhx5cJsvj4AAEpCFLQ3gACtPQxG26YqUh2OwHmU7Ra2gEAAwIAA3kAAzYE",
        caption="🤲 Прикладіть руку до руки нашої Астрологині... Відбувається сканування ліній долоні..."
    )
    await asyncio.sleep(12)
    await message.answer("✨ З'єднання встановлено. Ваша долоня зберігає унікальний код долі... ")
    await asyncio.sleep(6)

    life_line    = random.choice(["довга", "коротка", "ламається", "нечітка"])
    heart_line   = random.choice(["глибока", "розірвана", "довга", "тонка"])
    mind_line    = random.choice(["пряма", "вигнута", "нечітка", "довга"])
    fate_line    = random.choice(["чітка", "відсутня", "ламається", "пряма"])
    sun_line     = random.choice(["виражена", "коротка", "відсутня", "розірвана"])
    mercury_line = random.choice(["довга", "вигнута", "нечітка", "відсутня"])
    health_line  = random.choice(["пряма", "розірвана", "коротка", "хвиляста"])

    palm_lines_display = (
        "🔮 *Результат магічного аналізу долоні*:\n"
        f"⏳ Лінія життя: {life_line}  \n"
        f"💓 Лінія серця: {heart_line}  \n"
        f"🧠 Лінія розуму: {mind_line}  \n"
        f"⚖️ Лінія долі: {fate_line}  \n"
        f"🌞 Лінія Сонця: {sun_line}  \n"
        f"🪄 Лінія Меркурія: {mercury_line}  \n"
        f"🩺 Лінія здоров’я: {health_line}"
    )
    await message.answer(palm_lines_display, parse_mode="Markdown")

    palm_lines = (
        f"- Лінія життя: {life_line}\n"
        f"- Лінія серця: {heart_line}\n"
        f"- Лінія розуму: {mind_line}\n"
        f"- Лінія долі: {fate_line}\n"
        f"- Лінія Сонця: {sun_line}\n"
        f"- Лінія Меркурія: {mercury_line}\n"
        f"- Лінія здоров’я: {health_line}"
    )

    prompt = f"""
Ти — провидець і хіромант. Для кожної з поданих ліній дай чітке тлумачення саме цієї форми.
Не вигадуй нових ліній, не додавай зайвого. Пиши українською, впевнено і лаконічно.
Ось лінії:
{palm_lines}
"""

    try:
        await message.bot.send_chat_action(message.chat.id, "typing")
        result = await ask_openai(prompt, temperature=0.7, max_tokens=600)
        await message.answer(result)
    except Exception as e:
        print(f"scan_palm error: {e}")
        await message.answer("⚠️ Сталася помилка під час тлумачення долоні. Спробуй ще раз трохи згодом.")


# ===== Ask Astrologer =====
@router.message(F.text == "🌟 Запитати Астрологиню – 15🃏")
async def q_to_astrolog(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not spend_cards_if_possible(user_id, 15):
        await message.answer("❌ У вас недостатньо карт! Потрібно 15 🃏.")
        return
    await message.answer(
        "✨ Сформулюйте своє запитання максимально чітко та зрозуміло — саме від цього залежатиме, якою буде відповідь Астрологині.\n\n"
        "📩 Надішліть повідомлення просто сюди, одним текстом."
    )
    await state.set_state(AstroChat.waiting_for_question)

@router.message(StateFilter(AstroChat.waiting_for_question))
async def process_astro_question(message: Message, state: FSMContext):
    user_question = (message.text or "").strip()
    if not user_question:
        await message.answer("Будь ласка, сформулюй запитання для Астрологині.")
        return

    await message.bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1.0)

    prompt = f"""Уяви, що ти — Містична Астрологиня, провидиця, яка говорить з людиною від імені зірок.
Твоя мова — тепла, мудра, образна, але конкретна.

Відповідь повинна містити:
1) короткий образний вступ (1 речення),
2) конкретні поради/спостереження, які можна застосувати,
3) енергетичне завершення — духовне напуття однією фразою.

Пиши українською. Уникай порожніх фраз на кшталт «у тебе все вийде» — будь предметною.
Ось питання користувача:

{user_question}
"""

    try:
        answer = await ask_openai(prompt, temperature=0.7, max_tokens=700)
        await message.answer(f"🔮 Відповідь Астрологині:\n\n{answer}")
        await state.clear()
    except Exception as e:
        print(f"process_astro_question error: {e}")
        await message.answer("⚠️ Вибач, сталася помилка під час відповіді. Спробуй ще раз трохи згодом.")


# ===== Archetype compatibility =====
@router.message(F.text == "❤️‍🔥 Дізнатись сумісність душ – 25🃏")
async def start_compatibility(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not spend_cards_if_possible(user_id, 25):
        await message.answer("❌ У вас недостатньо карт! Потрібно 25 🃏.")
        return
    await message.answer("🔮 Спершу обери свій знак Зодіаку:", reply_markup=zodiac_keyboard)
    await state.set_state(ZodiacCompatibility.your_sign)

@router.callback_query(StateFilter(ZodiacCompatibility.your_sign))
async def choose_your_sign(callback: CallbackQuery, state: FSMContext):
    if not callback.data or not callback.data.startswith("zodiac_"):
        await callback.answer("Невірний вибір.", show_alert=True)
        return
    user_sign = callback.data.replace("zodiac_", "", 1)
    await state.update_data(your_sign=user_sign)
    await callback.message.answer(
        "🧿 Тепер обери знак партнера або людини, з якою хочеш перевірити сумісність:",
        reply_markup=zodiac_keyboard
    )
    await state.set_state(ZodiacCompatibility.partner_sign)
    await callback.answer()

@router.callback_query(StateFilter(ZodiacCompatibility.partner_sign))
async def choose_partner_sign(callback: CallbackQuery, state: FSMContext):
    if not callback.data or not callback.data.startswith("zodiac_"):
        await callback.answer("Невірний вибір.", show_alert=True)
        return

    partner_sign = callback.data.replace("zodiac_", "", 1)

    data = await state.get_data()
    your_sign = data.get("your_sign")
    if not your_sign:
        await callback.message.answer("⚠️ Спочатку обери свій знак.")
        await callback.answer()
        return

    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    await asyncio.sleep(0.8)

    prompt = f"""
Ти — мудрий астролог, що бачить глибокі взаємозв’язки між знаками зодіаку.
Дано два знаки: {your_sign} і {partner_sign}.

Зроби три частини:
1) Яку енергію створює їхній союз (можна алегоріями).
2) Сильні та слабкі сторони поєднання (чесно, але красиво й конкретно).
3) Завершення: один короткий поетичний афоризм/пророцтво.

Пиши українською, образно, але без води. До ~120–150 слів.
"""

    try:
        answer = await ask_openai(prompt, temperature=0.8, max_tokens=500)

        await callback.message.answer(f"🔮 Відповідь Астрологині:\n\n{answer}")
        await callback.message.answer(
            "✨ Хочеш дізнатися глибшу сумісність — *сумісність душ*?\n"
            "Пройди короткий архетипний тест:",
            reply_markup=archetype_test_kb,
            parse_mode="Markdown"
        )
        await state.clear()
    except Exception as e:
        print(f"choose_partner_sign error: {e}")
        await callback.message.answer("⚠️ Сталася помилка під час розрахунку сумісності. Спробуй ще раз.")
    finally:
        await callback.answer()

@router.callback_query(F.data == "start_archetype_test")
async def ask_who_first(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIFU2gUoTefcGZ0po2z4W6FC_HcMNBvAAJB-jEbbpihSAqF0HHBk3poAQADAgADeQADNgQ")
    await callback.message.answer("✨ Для кого проходимо тест спочатку?", reply_markup=architips_start_kb)

@router.callback_query(F.data.in_(["person_you", "person_partner"]))
async def start_test(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ArchetypeTest.q1)
    await state.update_data(person=callback.data)
    await callback.message.answer("❓ Як ти зазвичай реагуєш на труднощі?", reply_markup=architips_q1_kb)
    await callback.answer()

@router.callback_query(StateFilter(ArchetypeTest.q1, ArchetypeTest.q2, ArchetypeTest.q3, ArchetypeTest.q4, ArchetypeTest.q5))
async def next_question(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    current_state = await state.get_state()

    answers = state_data.get("answers", [])
    answers.append(callback.data)
    await state.update_data(answers=answers)

    if current_state == ArchetypeTest.q1.state:
        await state.set_state(ArchetypeTest.q2)
        await callback.message.answer("❓ Що ти найбільше цінуєш у житті?", reply_markup=architips_q2_kb)

    elif current_state == ArchetypeTest.q2.state:
        await state.set_state(ArchetypeTest.q3)
        await callback.message.answer("❓ У тебе вільний день. Що робиш?", reply_markup=architips_q3_kb)

    elif current_state == ArchetypeTest.q3.state:
        await state.set_state(ArchetypeTest.q4)
        await callback.message.answer("❓ Який твій головний страх?", reply_markup=architips_q4_kb)

    elif current_state == ArchetypeTest.q4.state:
        await state.set_state(ArchetypeTest.q5)
        await callback.message.answer("❓ Як ти сприймаєш інших людей?", reply_markup=architips_q5_kb)

    elif current_state == ArchetypeTest.q5.state:
        most_common = Counter(answers).most_common(1)[0][0]
        person = state_data["person"]
        await state.update_data(**{person: most_common}, answers=[])

        if person == "person_you":
            await callback.message.answer(
                "✅ Твій архетип визначено. Тепер пройди тест для партнера:",
                reply_markup=architips_partner_kb
            )
        else:
            data = await state.get_data()
            you = data.get("person_you")
            partner = data.get("person_partner")

            await callback.message.answer(f"🔮 Ти — {you}, партнер — {partner}\nСкоро я скажу, як взаємодіють ваші душі...")
            await callback.bot.send_chat_action(callback.message.chat.id, "typing")
            await asyncio.sleep(0.8)

            prompt = f"""
Уяви, що ти — мудра душа, яка відчуває енергетику стосунків. Дано два архетипи: {you} і {partner}.
Опиши їхню сумісність одним цілісним текстом:
- що між ними відчувається (притягнення, напруга, гармонія чи виклик),
- де їхнє світло і де тінь (чесно, але тепло),
- заверш з однією короткою фразою-пророцтвом, яка запам’ятається.
Пиши українською, щиро й конкретно, без списків і води (≈ 120–160 слів).
"""
            try:
                answer = await ask_openai(prompt, temperature=0.8, max_tokens=600)
                await callback.message.answer(f"🔮 Відповідь Астрологині:\n\n{answer}")
                await state.clear()
            except Exception as e:
                print(f"Archetype compatibility error: {e}")
                await callback.message.answer("⚠️ Сталася помилка під час аналізу сумісності. Спробуй ще раз.")
    await callback.answer()


# ===== Dream reading =====
@router.message(F.text == "💤 Мені наснився сон – 10🃏")
async def start_dream(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not spend_cards_if_possible(user_id, 10):
        await message.answer("❌ У вас недостатньо карт! Потрібно 10 🃏.")
        return
    await message.answer_photo(
        photo="AgACAgIAAxkBAAIFqGgUucN9O7420zzAQTsBq8oHsc_CAAKk9DEbbpipSLh5NoLFH6U6AQADAgADeQADNgQ",
        caption="🌙 Напиши свій сон одним повідомленням. Я відчую, що в ньому заховано..."
    )
    await state.set_state(DreamState.waiting_for_dream)

@router.message(StateFilter(DreamState.waiting_for_dream))
async def interpret_dream(message: Message, state: FSMContext):
    person_dream = (message.text or "").strip()
    if not person_dream:
        await message.answer("Будь ласка, опиши свій сон одним повідомленням.")
        return

    await message.bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(0.8)

    prompt = f"""
Ти — тлумач снів. Прочитай сон і дай цілісне, щире тлумачення без списків:
- яку потребу/емоцію він озвучує,
- де в ньому тінь і світло,
- заверши однією короткою фразою-резюме (без пояснень).
Сон: {person_dream}
"""

    try:
        answer = await ask_openai(prompt, temperature=0.7, max_tokens=700)
        await message.answer(f"🔮 Тлумачення сну:\n{answer}")
        await state.clear()
    except Exception as e:
        print(f"interpret_dream error: {e}")
        await message.answer("⚠️ Сталася помилка під час тлумачення. Спробуй ще раз.")


# ===== Photo util =====
@router.message(F.photo)
async def get_photo_id(message: Message):
    photo = message.photo[-1]
    await message.answer(f"file_id: {photo.file_id}")


# ===== Daily habit =====
@router.message(F.text == "🌙 Астральна звичка дня – 3🃏")
async def astral_habit(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not spend_cards_if_possible(user_id, 3):
        await message.answer("❌ У вас недостатньо карт! Потрібно 3 🃏.")
        return

    await message.answer("🌕 Твоя астральна звичка дня:")
    await message.bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(0.8)

    prompt = (
        "Вигадай одну унікальну астральну звичку на сьогодні (до 20 слів). "
        "Без пояснень, лише текст звички. Формат: [текст]"
    )

    try:
        answer = await ask_openai(prompt, temperature=0.9, max_tokens=60)
        await message.answer(answer)
        await state.clear()
    except Exception as e:
        print(f"astral_habit error: {e}")
        await message.answer("⚠️ Сталася помилка під час генерації звички. Спробуй ще раз трохи згодом.")


# ===== Daily bonus (callback) =====
@router.callback_query(F.data == "daily_bonus")
async def daily_bonus_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    amount = 5  # or random.choice([3,5,7])

    await callback.bot.send_chat_action(callback.message.chat.id, "typing")

    today_str = date.today().isoformat()
    already_claimed = False

    try:
        with session_scope() as session:
            user = get_or_create_user(session, user_id)
            if user.last_gift == today_str:
                already_claimed = True
            else:
                user.cards = (user.cards or 0) + amount
                user.last_gift = today_str
    except Exception as e:
        print(f"daily_bonus_handler error: {e}")
        await callback.message.answer("⚠️ Сталася помилка під час нарахування бонусу. Спробуй пізніше.")
        await callback.answer()
        return

    if already_claimed:
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass
        await callback.message.answer("🔔 Ти вже забирав щоденний бонус сьогодні. Повертайся завтра! 😊")
        await callback.answer()
        return

    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await callback.message.answer(f"🎉 Ти отримав +{amount} 🃏. Завітай завтра ще!")
    await callback.answer()


# ===== Horoscope + broadcast =====
async def generate_daily_horoscope(sign: str) -> str:
    prompt = f"""
Ти — астролог і поет. Напиши короткий (до 70 слів) персональний гороскоп на сьогодні для знаку {sign}.
Будь теплим, мудрим і натхненним. Уникай шаблонів і повторів, пиши українською.
Не використовуй фразу «день буде складним» — заміни її м'якою метафорою.
"""
    return await ask_openai(prompt, temperature=0.8, max_tokens=160)

HOROSCOPE_MAX_RETRIES = 3
BROADCAST_MAX_RETRIES = 3
BROADCAST_DELAY_SECONDS = 0.08


async def _generate_horoscope_with_retry(sign: str) -> str:
    """Generate horoscope text with retry logic to shield against transient errors."""
    delay = 1.0
    for attempt in range(1, HOROSCOPE_MAX_RETRIES + 1):
        try:
            return await generate_daily_horoscope(sign)
        except Exception as exc:
            logger.warning(
                "Failed to generate horoscope for %s (attempt %s/%s): %s",
                sign,
                attempt,
                HOROSCOPE_MAX_RETRIES,
                exc,
            )
            if attempt == HOROSCOPE_MAX_RETRIES:
                break
            await asyncio.sleep(delay)
            delay = min(delay * 2, 15)
    return f"Sogodni zori movchat dlya {sign}. Zajdi trochi piznishe, my poprobuemo znovu."


async def _build_horoscope_cache(signs: set[str]) -> dict[str, str]:
    cache: dict[str, str] = {}
    for sign in signs:
        cache[sign] = await _generate_horoscope_with_retry(sign)
    return cache


async def _send_broadcast_message(bot: Bot, user_id: int, sign: str, horoscope: str) -> None:
    delay = BROADCAST_DELAY_SECONDS
    for attempt in range(1, BROADCAST_MAX_RETRIES + 1):
        try:
            await bot.send_message(
                chat_id=user_id,
                text=f"Daily horoscope for {sign}:\n\n{horoscope}",
                reply_markup=daily_bonus_kb,
            )
            await asyncio.sleep(BROADCAST_DELAY_SECONDS)
            return
        except TelegramRetryAfter as exc:
            wait_time = exc.retry_after + 1
            logger.info("Flood wait for %s. Sleeping %.2fs", user_id, wait_time)
            await asyncio.sleep(wait_time)
        except (TelegramForbiddenError, TelegramNotFound):
            logger.info("Broadcast skipped for %s: bot blocked or user not found", user_id)
            return
        except TelegramBadRequest as exc:
            logger.warning("Bad request while broadcasting to %s: %s", user_id, exc)
            return
        except TelegramAPIError as exc:
            logger.warning(
                "Telegram API error for %s (attempt %s/%s): %s",
                user_id,
                attempt,
                BROADCAST_MAX_RETRIES,
                exc,
            )
        except Exception as exc:
            logger.exception("Unexpected error while sending broadcast to %s: %s", user_id, exc)
        await asyncio.sleep(delay)
        delay = min(delay * 2, 5)
    logger.error("Failed to deliver broadcast to %s after %s attempts", user_id, BROADCAST_MAX_RETRIES)


async def daily_broadcast(bot: Bot):
    with session_scope() as session:
        users = session.execute(
            select(User.id, User.zodiac_sign).where(User.zodiac_sign.is_not(None))
        ).all()

    if not users:
        logger.info("No users with zodiac signs to broadcast to.")
        return

    signs = {sign for _, sign in users if sign}
    horoscope_cache = await _build_horoscope_cache(signs) if signs else {}

    for user_id, sign in users:
        if not sign:
            continue
        horoscope = horoscope_cache.get(sign)
        if not horoscope:
            logger.warning("No horoscope text for sign %s, skipping user %s", sign, user_id)
            continue
        await _send_broadcast_message(bot, user_id, sign, horoscope)

# ===== Invite & Cards =====
@router.message(F.text == "🤝 Запросити друга")
async def invite_friend(message: Message):
    bot_username = "tviyAstrogid_bot"
    ref_link = f"https://t.me/{bot_username}?start={message.from_user.id}"
    await message.answer(
        f"💌 Надішли це посилання другу:\n\n{hbold(ref_link)}\n\n"
        "🃏 Якщо він запустить бота — ти отримаєш 25 карт!"
    )

@router.message(F.text == "🛒Мої карти")
async def my_cards(message: Message):
    user_id = message.from_user.id
    with session_scope() as session:
        user = session.get(User, user_id)
        cards = int(user.cards) if user and user.cards else 0
    await message.answer(f"💳 Баланс: {cards} 🃏")

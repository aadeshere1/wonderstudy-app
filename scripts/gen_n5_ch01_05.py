#!/usr/bin/env python3
"""Generate JLPT N5 lesson files for Minna no Nihongo chapters 1-5."""
import json, os, random

OUT = "/sessions/festive-blissful-meitner/mnt/wonderstudy-app/data/classes/jlpt/n5"
os.makedirs(OUT, exist_ok=True)

DIFFICULTY_VOCAB = "beginner"
DIFFICULTY_GRAMMAR = "beginner"
DIFFICULTY_EXAMPLES = "beginner"

def make_vocab_lesson(num, jp_title, en_title, icon, teach_cards, vocab_items, grammar_preview=""):
    """vocab_items: list of (question_jp, answer_en, [option1,option2,option3]) """
    practice = []
    challenge = []
    for (q, ans, others) in vocab_items:
        opts = [ans] + others[:3]
        random.shuffle(opts)
        practice.append({"question": q, "answer": ans, "options": opts})
    # challenge = reversed direction (English → Japanese) for first 15
    for (q, ans, others) in vocab_items[:15]:
        jp_opts = [q] + [x[0] for x in vocab_items if x[0] != q][:3]
        random.shuffle(jp_opts)
        challenge.append({"question": f"How do you say '{ans}' in Japanese?", "answer": q, "options": jp_opts})
    return {
        "id": f"ch{num:02d}-vocabulary",
        "meta": {
            "title": f"Lesson {num}: {jp_title} — Vocabulary",
            "subject": "japanese", "class": None,
            "lesson": f"ch{num:02d}-vocabulary",
            "subtopic": en_title,
            "description": f"Vocabulary for Minna no Nihongo Lesson {num}: {en_title}",
            "icon": icon, "difficulty": DIFFICULTY_VOCAB
        },
        "teach": {"type": "flashcard", "items": teach_cards},
        "practice": {"gameType": "vocab", "config": {"answerMode": "mcq", "optionsCount": 4, "timeLimit": 20, "questionsCount": min(15, len(practice))}, "items": practice},
        "challenge": {"gameType": "vocab", "config": {"answerMode": "mcq", "optionsCount": 4, "timeLimit": 10, "questionsCount": min(15, len(challenge))}, "items": challenge},
    }

def make_grammar_lesson(num, jp_title, en_title, icon, teach_cards, practice_items, challenge_items=None):
    return {
        "id": f"ch{num:02d}-grammar",
        "meta": {
            "title": f"Lesson {num}: {jp_title} — Grammar",
            "subject": "japanese", "class": None,
            "lesson": f"ch{num:02d}-grammar",
            "subtopic": en_title,
            "description": f"Grammar patterns for Minna no Nihongo Lesson {num}: {en_title}",
            "icon": icon, "difficulty": DIFFICULTY_GRAMMAR
        },
        "teach": {"type": "flashcard", "items": teach_cards},
        "practice": {"gameType": "mcq-facts", "config": {"shuffleOptions": True, "timeLimit": 25, "questionsCount": min(15, len(practice_items))}, "items": practice_items},
        "challenge": {"gameType": "mcq-facts", "config": {"shuffleOptions": True, "timeLimit": 12, "questionsCount": min(15, len(challenge_items or practice_items))}, "items": challenge_items or practice_items},
    }

def make_examples_lesson(num, jp_title, en_title, icon, teach_cards, practice_items):
    return {
        "id": f"ch{num:02d}-examples",
        "meta": {
            "title": f"Lesson {num}: {jp_title} — Dialogue & Examples",
            "subject": "japanese", "class": None,
            "lesson": f"ch{num:02d}-examples",
            "subtopic": en_title,
            "description": f"Practical dialogues and sentences for Lesson {num}: {en_title}",
            "icon": icon, "difficulty": DIFFICULTY_EXAMPLES
        },
        "teach": {"type": "flashcard", "items": teach_cards},
        "practice": {"gameType": "mcq-facts", "config": {"shuffleOptions": True, "timeLimit": 25, "questionsCount": min(15, len(practice_items))}, "items": practice_items},
        "challenge": {"gameType": "mcq-facts", "config": {"shuffleOptions": True, "timeLimit": 12, "questionsCount": min(15, len(practice_items))}, "items": practice_items},
    }

def write(lesson):
    path = os.path.join(OUT, lesson["id"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(lesson, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {lesson['id']}.json")

# ══════════════════════════════════════════════════════════════
# CHAPTER 1: はじめまして — Nice to Meet You
# ══════════════════════════════════════════════════════════════
ch1_vocab = [
    ("わたし (私)", "I / me", ["you", "he/she", "they"]),
    ("あなた", "you", ["I / me", "he/she", "we"]),
    ("このかた (この方)", "this person (polite)", ["that person", "everyone", "who?"]),
    ("〜さん", "Mr. / Ms. (honorific suffix)", ["teacher", "friend", "colleague"]),
    ("せんせい (先生)", "teacher", ["student", "doctor", "engineer"]),
    ("がくせい (学生)", "student", ["teacher", "company employee", "researcher"]),
    ("かいしゃいん (会社員)", "company employee", ["doctor", "teacher", "student"]),
    ("いしゃ (医者)", "doctor / physician", ["teacher", "engineer", "student"]),
    ("けんきゅうしゃ (研究者)", "researcher", ["teacher", "doctor", "student"]),
    ("エンジニア", "engineer", ["doctor", "researcher", "company employee"]),
    ("にほん (日本)", "Japan", ["China", "America", "Korea"]),
    ("アメリカ", "America / USA", ["Japan", "France", "Germany"]),
    ("イギリス", "United Kingdom", ["France", "Germany", "Australia"]),
    ("ちゅうごく (中国)", "China", ["Japan", "Korea", "America"]),
    ("かんこく (韓国)", "South Korea", ["Japan", "China", "America"]),
    ("フランス", "France", ["Germany", "Italy", "Spain"]),
    ("ドイツ", "Germany", ["France", "Italy", "UK"]),
    ("〜じん (〜人)", "person from ~ / nationality suffix", ["language suffix", "job suffix", "place suffix"]),
    ("〜ご (〜語)", "language of ~", ["nationality suffix", "job suffix", "country suffix"]),
    ("なんさい (何歳)", "how old?", ["how many?", "what time?", "how much?"]),
    ("よろしくおねがいします", "pleased to meet you / nice to meet you", ["goodbye", "excuse me", "thank you"]),
    ("はじめまして", "how do you do / nice to meet you (first meeting)", ["goodbye", "good morning", "thank you"]),
]

ch1_vocab_teach = [
    {"front": "わたし", "back": "I / me (私)\nFormal in speech; use in all polite situations.\nExample: わたしは田中です。= I am Tanaka."},
    {"front": "せんせい / がくせい", "back": "先生 = teacher\n学生 = student\nThese are the two most common roles in MNN Lesson 1."},
    {"front": "かいしゃいん / いしゃ", "back": "会社員 = company employee\n医者 = doctor\nCommon occupations introduced in Lesson 1."},
    {"front": "〜じん vs 〜ご", "back": "〜人 (じん) = nationality\n日本人 (にほんじん) = Japanese person\n\n〜語 (ご) = language\n日本語 (にほんご) = Japanese language"},
    {"front": "〜さん", "back": "A polite suffix used after names.\nNever use it with your own name!\n田中さん = Mr./Ms. Tanaka"},
    {"front": "はじめまして", "back": "Said when meeting someone for the first time.\nAlways followed by よろしくおねがいします.\nMeans: 'How do you do' / 'Nice to meet you'"},
    {"front": "Nationalities", "back": "日本 → 日本人 (Japanese)\nアメリカ → アメリカ人 (American)\nイギリス → イギリス人 (British)\nちゅうごく → ちゅうごく人 (Chinese)\nフランス → フランス人 (French)"},
    {"front": "よろしくおねがいします", "back": "Used at the end of self-introductions.\nMeans: 'I'm in your care' / 'Please treat me well'\nEssential phrase for first meetings!"},
]

ch1_grammar_teach = [
    {"front": "Pattern: NはNです", "back": "N は N です — N is N\nわたしは田中です。= I am Tanaka.\nは (wa) marks the topic; です = polite 'is'."},
    {"front": "Pattern: NもNです", "back": "N も N です — N is also N\nサントスさんもブラジル人です。\n= Mr. Santos is also Brazilian.\nも (mo) replaces は to mean 'also/too'."},
    {"front": "Pattern: NはNじゃありません", "back": "Negative: N is not N\nわたしは学生じゃありません。\n= I am not a student.\nじゃありません = polite negative of です."},
    {"front": "Pattern: NのN", "back": "N の N — N's N (possession/affiliation)\nIMCのミラーさん = Mr. Miller of IMC\nわたしの本 = my book\nの connects owner → object."},
    {"front": "Making questions: 〜ですか", "back": "Add か to any statement to make a question.\n学生ですか。= Are you a student?\nアメリカ人ですか。= Are you American?\nAnswer: はい (yes) or いいえ (no)."},
    {"front": "Responding: はい/いいえ", "back": "はい、そうです。= Yes, that's right.\nいいえ、ちがいます。= No, that's different/wrong.\nいいえ、〜じゃありません。= No, I'm not ~."},
    {"front": "Asking age: 〜さいですか", "back": "なんさいですか。= How old are you?\n〜さいです。= I am ~ years old.\n23さい → にじゅうさんさい\n(Numbers review: いち、に、さん、し、ご...)"},
    {"front": "Asking occupation", "back": "おしごとは？= What is your job?\nしごとはなんですか。= What do you do for work?\n→ 〜です。(I am a ~)"},
]

ch1_grammar_q = [
    {"question": "わたし ___ 田中です。(I am Tanaka.)", "answer": "は", "options": ["は", "が", "を", "も"], "explanation": "は (wa) is the topic marker. NはNです = 'N is N'."},
    {"question": "サントスさん ___ ブラジル人です。(Mr. Santos is also Brazilian.)", "answer": "も", "options": ["も", "は", "が", "で"], "explanation": "も (mo) means 'also/too' and replaces は in this pattern."},
    {"question": "わたしは学生 ___ ありません。(I am not a student.)", "answer": "じゃ", "options": ["じゃ", "では", "が", "は"], "explanation": "じゃありません is the polite negative of です. (でもありません is also correct but less common in speech.)"},
    {"question": "これはIMC ___ ミラーさんです。(This is Mr. Miller of IMC.)", "answer": "の", "options": ["の", "は", "が", "を"], "explanation": "の connects two nouns: company の person = person of the company."},
    {"question": "がくせい ___ (Are you a student?)", "answer": "ですか", "options": ["ですか", "ですね", "でしょう", "ですよ"], "explanation": "か at the end of a です sentence makes it a yes/no question."},
    {"question": "ミラーさんはアメリカ___ です。(Mr. Miller is American.)", "answer": "じん (人)", "options": ["じん (人)", "ご (語)", "さん", "の"], "explanation": "〜人 (じん) is the nationality suffix. アメリカ人 = American person."},
    {"question": "にほん___ はにほんごです。(The language of Japan is Japanese.)", "answer": "ご (語)", "options": ["ご (語)", "じん (人)", "の", "は"], "explanation": "〜語 (ご) is the language suffix. 日本語 = Japanese language."},
    {"question": "はい、___ です。(Yes, that's right.)", "answer": "そう", "options": ["そう", "これ", "どれ", "だれ"], "explanation": "はい、そうです = Yes, that's right. そう = 'so/that way'."},
    {"question": "わたしはかいしゃいんじゃ ___ 。(I am not a company employee.)", "answer": "ありません", "options": ["ありません", "います", "です", "ません"], "explanation": "じゃありません = polite negative. じゃ + ありません (not exist/be)."},
    {"question": "Q: おしごとは？A: ___ です。(I am a teacher.)", "answer": "せんせい", "options": ["せんせい", "がくせい", "かいしゃいん", "エンジニア"], "explanation": "せんせい (先生) = teacher. おしごとは = what is your job?"},
    {"question": "田中さん ___ ちゅうごく人ですか。(Is Mr. Tanaka Chinese?)", "answer": "は", "options": ["は", "も", "が", "の"], "explanation": "は marks 田中さん as the topic of this question."},
    {"question": "A: フランス人ですか。B: いいえ、___ 。", "answer": "ちがいます", "options": ["ちがいます", "そうです", "います", "あります"], "explanation": "ちがいます = 'that's different/wrong'. Used to politely deny something."},
    {"question": "なんさいですか → ___ さいです。(I am 25 years old.)", "answer": "にじゅうご (25)", "options": ["にじゅうご (25)", "じゅうに (12)", "さんじゅう (30)", "よんじゅう (40)"], "explanation": "25 = にじゅうご. に (2) + じゅう (10) + ご (5) = 25."},
    {"question": "はじめまして, followed by what phrase?", "answer": "よろしくおねがいします", "options": ["よろしくおねがいします", "ありがとうございます", "すみません", "おやすみなさい"], "explanation": "はじめまして always pairs with よろしくおねがいします at the end of a first introduction."},
    {"question": "〜さん is used after:", "answer": "Other people's names (not your own)", "options": ["Other people's names (not your own)", "Your own name", "Place names", "Job titles only"], "explanation": "〜さん is a respectful suffix. Never attach it to your own name — that's considered rude."},
]

ch1_examples_teach = [
    {"front": "Self-introduction formula", "back": "1. はじめまして。\n2. (name)です。\n3. (country/company)の(name)です。\n4. よろしくおねがいします。\n\nExample:\nはじめまして。IMCのミラーです。よろしくおねがいします。"},
    {"front": "Asking nationality", "back": "Q: 〜さんは___人ですか。\nA: はい、___人です。\n   いいえ、___人じゃありません。___人です。\n\nExample:\nA: ミラーさんはアメリカ人ですか。\nB: はい、そうです。"},
    {"front": "Asking occupation", "back": "Q: おしごとは？/ しごとはなんですか。\nA: 〜です。\n\nExample:\nA: おしごとは？\nB: エンジニアです。ABCのエンジニアです。"},
    {"front": "Business card exchange", "back": "When exchanging 名刺 (めいし = business card):\n1. Hand with both hands + slight bow\n2. はじめまして。(name)でございます。\n3. よろしくおねがいいたします。\nForever remember: never write on or stuff a card in pocket immediately!"},
    {"front": "Key Lesson 1 dialogue", "back": "ミラー：はじめまして。IMCのミラーです。よろしく。\n山田：山田です。よろしく。ミラーさんはアメリカ人ですか。\nミラー：はい、そうです。山田さんは？\n山田：わたしは日本人です。"},
    {"front": "Polite vs casual", "back": "Polite (です/ます): Use with strangers, superiors\nわたしは学生です。\n\nCasual (drop です): Use with close friends\nわたしは学生。\n\nAlways use polite form in Lesson 1 situations!"},
]

ch1_examples_q = [
    {"question": "Someone says はじめまして to you. What do you say back?", "answer": "はじめまして。よろしくおねがいします。", "options": ["はじめまして。よろしくおねがいします。", "ありがとうございます。", "おはようございます。", "さようなら。"], "explanation": "はじめまして is reciprocal — you say it back, then add よろしくおねがいします."},
    {"question": "Mr. Miller works at IMC. How does he introduce himself?", "answer": "IMCのミラーです。", "options": ["IMCのミラーです。", "ミラーのIMCです。", "IMCはミラーです。", "ミラーがIMCです。"], "explanation": "Company/affiliation comes first with の: [company]の[name]です."},
    {"question": "How do you ask 'Are you a teacher?'", "answer": "せんせいですか。", "options": ["せんせいですか。", "せんせいですね。", "せんせいでしょう。", "せんせいですよ。"], "explanation": "Add か to a です statement to make a yes/no question."},
    {"question": "Someone asks あなたはちゅうごく人ですか。You're Japanese. What do you say?", "answer": "いいえ、ちがいます。日本人です。", "options": ["いいえ、ちがいます。日本人です。", "はい、そうです。", "いいえ、日本人じゃありません。", "はい、ちがいます。"], "explanation": "いいえ、ちがいます or いいえ、〜じゃありません are both correct polite denials."},
    {"question": "Your colleague is also from France. Which sentence is correct?", "answer": "マリーさんもフランス人です。", "options": ["マリーさんもフランス人です。", "マリーさんはフランス人です。", "マリーさんがフランス人です。", "マリーさんのフランス人です。"], "explanation": "も (also) replaces は when adding 'also/too'. 〜さんも〜です."},
    {"question": "What does よろしくおねがいします mean in a first meeting?", "answer": "Pleased to meet you / I'm in your care", "options": ["Pleased to meet you / I'm in your care", "Thank you very much", "Excuse me", "Goodbye"], "explanation": "よろしくおねがいします literally means 'please treat me well' — the standard phrase ending introductions."},
    {"question": "Karina is Indonesian. Which nationality sentence is correct?", "answer": "カリナさんはインドネシア人です。", "options": ["カリナさんはインドネシア人です。", "カリナさんはインドネシアごです。", "カリナさんのインドネシア人です。", "カリナさんがインドネシアです。"], "explanation": "〜人 (じん) is used for nationality. Country + 人 = person from that country."},
    {"question": "How do you say 'I am not a researcher'?", "answer": "わたしはけんきゅうしゃじゃありません。", "options": ["わたしはけんきゅうしゃじゃありません。", "わたしはけんきゅうしゃです。", "わたしがけんきゅうしゃじゃありません。", "わたしのけんきゅうしゃじゃありません。"], "explanation": "NはNじゃありません = N is not N. は marks topic; じゃありません = negative of です."},
    {"question": "A person hands you their business card (名刺). What are they doing?", "answer": "Introducing themselves / exchanging business cards", "options": ["Introducing themselves / exchanging business cards", "Giving you a present", "Asking for directions", "Requesting help"], "explanation": "名刺 (めいし) exchange is an important Japanese business introduction ritual."},
    {"question": "What is the correct Japanese for 'Japanese language'?", "answer": "にほんご (日本語)", "options": ["にほんご (日本語)", "にほんじん (日本人)", "にほん (日本)", "にほんさん"], "explanation": "〜語 (ご) = language. 日本語 = Japanese language. 日本人 = Japanese person."},
]

write(make_vocab_lesson(1, "はじめまして", "Nice to Meet You", "👋", ch1_vocab_teach, ch1_vocab))
write(make_grammar_lesson(1, "はじめまして", "Nice to Meet You", "👋", ch1_grammar_teach, ch1_grammar_q))
write(make_examples_lesson(1, "はじめまして", "Nice to Meet You", "👋", ch1_examples_teach, ch1_examples_q))

# ══════════════════════════════════════════════════════════════
# CHAPTER 2: これはなんですか — What Is This?
# ══════════════════════════════════════════════════════════════
ch2_vocab = [
    ("これ", "this (near speaker)", ["that (near you)", "that (far away)", "which one?"]),
    ("それ", "that (near listener)", ["this (near me)", "that (far away)", "which one?"]),
    ("あれ", "that (far from both)", ["this (near me)", "that (near you)", "which one?"]),
    ("どれ", "which one?", ["this", "that", "those"]),
    ("ほん (本)", "book", ["dictionary", "magazine", "notebook"]),
    ("じしょ (辞書)", "dictionary", ["book", "magazine", "notebook"]),
    ("ざっし (雑誌)", "magazine", ["book", "dictionary", "newspaper"]),
    ("しんぶん (新聞)", "newspaper", ["magazine", "book", "dictionary"]),
    ("ノート", "notebook", ["book", "dictionary", "magazine"]),
    ("てちょう (手帳)", "pocket planner / organiser", ["notebook", "magazine", "book"]),
    ("えんぴつ (鉛筆)", "pencil", ["ballpoint pen", "key", "eraser"]),
    ("ボールペン", "ballpoint pen", ["pencil", "marker", "key"]),
    ("かぎ (鍵)", "key", ["watch", "umbrella", "bag"]),
    ("とけい (時計)", "watch / clock", ["key", "umbrella", "bag"]),
    ("かさ (傘)", "umbrella", ["key", "watch", "bag"]),
    ("かばん (鞄)", "bag", ["umbrella", "key", "watch"]),
    ("めいし (名刺)", "business card", ["card", "book", "notebook"]),
    ("テレビ", "television", ["computer", "radio", "camera"]),
    ("パソコン", "computer / laptop", ["television", "radio", "camera"]),
    ("だれ (誰)", "who?", ["what?", "where?", "when?"]),
    ("〜の", "apostrophe-s / belonging marker", ["topic marker", "object marker", "direction marker"]),
    ("なん / なに (何)", "what?", ["who?", "where?", "when?"]),
]

ch2_vocab_teach = [
    {"front": "これ / それ / あれ / どれ", "back": "これ = this (near ME)\nそれ = that (near YOU)\nあれ = that (far from BOTH of us)\nどれ = which one?\n\nTip: Think of the distance between speakers!"},
    {"front": "Stationery vocabulary", "back": "えんぴつ = pencil\nボールペン = ballpoint pen\nノート = notebook\nてちょう = pocket planner\nじしょ = dictionary"},
    {"front": "Everyday objects", "back": "かぎ = key\nとけい = watch/clock\nかさ = umbrella\nかばん = bag\nめいし = business card"},
    {"front": "Reading material", "back": "ほん (本) = book\nざっし (雑誌) = magazine\nしんぶん (新聞) = newspaper\nじしょ (辞書) = dictionary"},
    {"front": "Question words", "back": "なん / なに = what?\nだれ = who?\nどれ = which one?\nいくら = how much?\n\nAll question words go where the answer would be!"},
    {"front": "〜の (possession)", "back": "〜の connects owner to object:\nわたしの かばん = my bag\nせんせいの ほん = the teacher's book\nIMCの ミラーさん = Mr. Miller of IMC"},
    {"front": "そうです / そうじゃありません", "back": "そうです = Yes, that's right\nそうじゃありません = That's not right\n\nUsed to confirm or deny identity:\nA: これはとけいですか。\nB: はい、そうです。"},
    {"front": "Asking 'whose'", "back": "これはだれのNですか。\n= Whose N is this?\n\nA: これはだれのかさですか。\nB: それはわたしのかさです。"},
]

ch2_grammar_teach = [
    {"front": "これ/それ/あれ は N です", "back": "This/that is N.\nこれは ほんです。= This is a book.\nそれは かぎですか。= Is that a key?\nあれは なんですか。= What is that?"},
    {"front": "N は N の N です", "back": "This is [owner]'s [object].\nこれはわたしのかばんです。\n= This is my bag.\n\nOwner + の + Object = possession"},
    {"front": "Asking 'what is this?'", "back": "これはなんですか。= What is this?\nそれはなんですか。= What is that?\nあれはなんですか。= What is that over there?\n\nなん = what (before consonants)\nなに = what (before vowels/particles)"},
    {"front": "Confirming / Denying", "back": "はい、そうです。= Yes, that's right.\nいいえ、そうじゃありません。= No, that's not right.\nいいえ、それはNです。= No, it's N.\n\nExample: A: かぎですか。B: いいえ、とけいです。"},
    {"front": "Asking 'whose?'", "back": "だれのNですか。= Whose N is it?\nこれはだれのかさですか。\n= Whose umbrella is this?\nAnswer: わたしの(かさ)です。= It's mine."},
    {"front": "〜は〜のです", "back": "N は [owner] のです。\n= The N is [owner]'s.\nこれはわたしのです。= This is mine.\n\nCan drop the noun when clear from context!"},
]

ch2_grammar_q = [
    {"question": "A: ___ はなんですか。(What is this?)", "answer": "これ", "options": ["これ", "それ", "あれ", "どれ"], "explanation": "これ = this (near the speaker). Use これ when pointing at something near you."},
    {"question": "A: ___ はなんですか。(What is that? — object near the listener)", "answer": "それ", "options": ["それ", "これ", "あれ", "どれ"], "explanation": "それ = that (near the listener). Use when the object is closer to the other person."},
    {"question": "これはわたし ___ かばんです。(This is my bag.)", "answer": "の", "options": ["の", "は", "が", "を"], "explanation": "の marks possession. わたしのかばん = my bag (I's bag)."},
    {"question": "A: これはとけいですか。B: はい、___ 。(Yes, that's right.)", "answer": "そうです", "options": ["そうです", "ちがいます", "ありません", "いません"], "explanation": "はい、そうです = Yes, that's right. Used to confirm identity."},
    {"question": "A: これはだれのかさですか。B: ___ のかさです。(It's the teacher's.)", "answer": "せんせい", "options": ["せんせい", "わたし", "あなた", "がくせい"], "explanation": "だれの = whose? The answer replaces だれ: せんせいのかさ = teacher's umbrella."},
    {"question": "これはえんぴつじゃ___ 。ボールペンです。(This is not a pencil. It's a pen.)", "answer": "ありません", "options": ["ありません", "います", "です", "ません"], "explanation": "じゃありません = polite negative of です. Not a pencil → じゃありません."},
    {"question": "あれは なん ___ か。(What is that over there?)", "answer": "です", "options": ["です", "ます", "でした", "ました"], "explanation": "なんですか = What is it? です before か makes a polite question."},
    {"question": "A: それはミラーさんのですか。B: はい、___ 。", "answer": "わたしのです", "options": ["わたしのです", "あなたのです", "このです", "それのです"], "explanation": "When asked if something belongs to you, reply: はい、わたしのです (Yes, it's mine)."},
    {"question": "___ はどれですか。(Which one is the dictionary?)", "answer": "じしょ", "options": ["じしょ", "ざっし", "しんぶん", "ノート"], "explanation": "じしょ (辞書) = dictionary. The question asks which object is the dictionary."},
    {"question": "How do you ask 'Is this a newspaper?'", "answer": "これはしんぶんですか。", "options": ["これはしんぶんですか。", "これにしんぶんですか。", "これがしんぶんですか。", "これをしんぶんですか。"], "explanation": "これはNですか = Is this N? は marks これ as the topic."},
    {"question": "A: これはだれのめいしですか。B: それは___のめいしです。(It's Mr. Miller's.)", "answer": "ミラーさん", "options": ["ミラーさん", "わたし", "あなた", "せんせい"], "explanation": "Owner + の + object = possession. ミラーさんのめいし = Mr. Miller's business card."},
    {"question": "Which word means 'which one?' (choosing from several)", "answer": "どれ", "options": ["どれ", "これ", "それ", "あれ"], "explanation": "どれ = which one? Used when asking someone to choose from 3+ options. (どちら = which of two)"},
]

ch2_examples_teach = [
    {"front": "Identifying objects", "back": "A: これはなんですか。\nB: それはじしょです。\n\nA: What is this?\nB: That is a dictionary.\n\nNote: これ (A's side) → それ (B's reference)"},
    {"front": "Lost & Found conversation", "back": "A: すみません、これはだれのかばんですか。\nB: あ、それはわたしのです。ありがとうございます。\n\nA: Excuse me, whose bag is this?\nB: Ah, that's mine. Thank you."},
    {"front": "Shopping: What is that?", "back": "A: すみません、あれはなんですか。\nB: あれはてちょうです。\nA: いくらですか。\nB: 500円です。\n\nいくら = how much?"},
    {"front": "Correcting someone", "back": "A: それはかさですか。\nB: いいえ、そうじゃありません。これはかさじゃありません。てんびんです。\n\nA: Is that an umbrella?\nB: No, that's not right. This isn't an umbrella. It's a scale."},
    {"front": "Whose is it? — Confirming ownership", "back": "A: このノートはだれのですか。\nB: わたしのです。\nA: そうですか。はい、どうぞ。\nB: ありがとうございます。\n\nどうぞ = here you go / please (offering something)"},
    {"front": "Key phrases for Lesson 2", "back": "• これはなんですか。= What is this?\n• だれのNですか。= Whose N is it?\n• いくらですか。= How much is it?\n• はい、そうです。= Yes, that's right.\n• いいえ、ちがいます。= No, that's wrong."},
]

ch2_examples_q = [
    {"question": "Someone near you points at something far away. Which word should they use?", "answer": "あれ", "options": ["あれ", "これ", "それ", "どれ"], "explanation": "あれ = that (far from both speaker and listener). これ = near speaker, それ = near listener."},
    {"question": "You find an umbrella. How do you ask 'Whose umbrella is this?'", "answer": "これはだれのかさですか。", "options": ["これはだれのかさですか。", "これはなんのかさですか。", "これはどれのかさですか。", "これにだれのかさですか。"], "explanation": "だれの = whose? + の connects to the noun: だれのかさ = whose umbrella."},
    {"question": "In a shop you see something far away. How do you ask 'What is that?'", "answer": "あれはなんですか。", "options": ["あれはなんですか。", "これはなんですか。", "それはなんですか。", "どれはなんですか。"], "explanation": "あれ is used for things far from both you and the shopkeeper."},
    {"question": "You want to say 'That pen is not mine.' Which is correct?", "answer": "そのボールペンはわたしのじゃありません。", "options": ["そのボールペンはわたしのじゃありません。", "そのボールペンはわたしのです。", "そのボールペンにわたしのじゃありません。", "そのボールペンがわたしじゃありません。"], "explanation": "NはNじゃありません = N is not N. Using の to show it's 'mine/not mine'."},
    {"question": "The shopkeeper asks: どれがいいですか。What are they asking?", "answer": "Which one would you like?", "options": ["Which one would you like?", "What is this?", "Whose is it?", "How much is it?"], "explanation": "どれ = which one? どれがいいですか = Which one is good/do you want?"},
    {"question": "A: それはテレビですか。B: いいえ、___。(No, it's a computer.)", "answer": "パソコンです", "options": ["パソコンです", "テレビです", "かぎです", "かさです"], "explanation": "When denying, say いいえ + the correct identity. パソコン = computer/laptop."},
    {"question": "How do you say 'This is the teacher's dictionary'?", "answer": "これはせんせいのじしょです。", "options": ["これはせんせいのじしょです。", "これはじしょのせんせいです。", "これにせんせいのじしょです。", "これがせんせいじしょのです。"], "explanation": "Owner + の + Object: せんせいの + じしょ = teacher's dictionary."},
    {"question": "You want to ask 'Is this a magazine?' How do you ask?", "answer": "これはざっしですか。", "options": ["これはざっしですか。", "これにざっしですか。", "これのざっしですか。", "これがざっしです。"], "explanation": "これはNですか = Is this N? Simple question pattern with は and か."},
]

write(make_vocab_lesson(2, "これはなんですか", "What Is This?", "📦", ch2_vocab_teach, ch2_vocab))
write(make_grammar_lesson(2, "これはなんですか", "What Is This?", "📦", ch2_grammar_teach, ch2_grammar_q))
write(make_examples_lesson(2, "これはなんですか", "What Is This?", "📦", ch2_examples_teach, ch2_examples_q))

# ══════════════════════════════════════════════════════════════
# CHAPTER 3: ここはどこですか — Where Is This Place?
# ══════════════════════════════════════════════════════════════
ch3_vocab = [
    ("ここ", "here / this place", ["there", "over there", "where?"]),
    ("そこ", "there / that place (near you)", ["here", "over there", "where?"]),
    ("あそこ", "over there (far from both)", ["here", "there", "where?"]),
    ("どこ", "where?", ["here", "there", "over there"]),
    ("こちら", "this way / here (polite)", ["that way", "over there", "which way?"]),
    ("そちら", "that way / there (polite)", ["this way", "over there", "which way?"]),
    ("あちら", "that way over there (polite)", ["this way", "that way", "which way?"]),
    ("どちら", "which way? / where? (polite)", ["this way", "that way", "over there"]),
    ("デパート", "department store", ["supermarket", "restaurant", "hospital"]),
    ("スーパー", "supermarket", ["department store", "restaurant", "hospital"]),
    ("レストラン", "restaurant", ["supermarket", "hospital", "library"]),
    ("しょくどう (食堂)", "cafeteria / dining hall", ["restaurant", "library", "hospital"]),
    ("びょういん (病院)", "hospital", ["pharmacy", "clinic", "library"]),
    ("ゆうびんきょく (郵便局)", "post office", ["bank", "hospital", "library"]),
    ("ぎんこう (銀行)", "bank", ["post office", "hospital", "library"]),
    ("としょかん (図書館)", "library", ["school", "hospital", "bank"]),
    ("〜かい (〜階)", "floor / story (counter)", ["〜本", "〜枚", "〜個"]),
    ("なんかい (何階)", "which floor?", ["how many?", "how much?", "what time?"]),
    ("うえ (上)", "above / up / top", ["below", "left", "right"]),
    ("した (下)", "below / down / bottom", ["above", "left", "right"]),
    ("いくら", "how much?", ["how many?", "which floor?", "what time?"]),
    ("えん (円)", "yen (Japanese currency)", ["dollar", "euro", "pound"]),
]

ch3_vocab_teach = [
    {"front": "Location words: ここ / そこ / あそこ / どこ", "back": "ここ = here (near me)\nそこ = there (near you)\nあそこ = over there (far from both)\nどこ = where?\n\nPolite versions: こちら / そちら / あちら / どちら"},
    {"front": "Shops & Places", "back": "デパート = department store\nスーパー = supermarket\nレストラン = restaurant\nしょくどう (食堂) = cafeteria\nびょういん (病院) = hospital"},
    {"front": "Public facilities", "back": "ゆうびんきょく (郵便局) = post office\nぎんこう (銀行) = bank\nとしょかん (図書館) = library\nがっこう (学校) = school\nびょういん (病院) = hospital"},
    {"front": "〜かい (〜階) = floor", "back": "いっかい = 1st floor\nにかい = 2nd floor\nさんかい / さんがい = 3rd floor\nよんかい = 4th floor\nなんかい = which floor?\nちかいっかい = basement 1"},
    {"front": "いくら = how much?", "back": "いくらですか。= How much is it?\n〜えん (〜円) = ~ yen\n\n500円 → ごひゃくえん\n1000円 → せんえん\n2000円 → にせんえん"},
    {"front": "Direction words", "back": "うえ (上) = above / top\nした (下) = below / bottom\nみぎ (右) = right\nhidari (左) = left\nまえ (前) = front / before\nうしろ (後ろ) = behind"},
    {"front": "Asking location: Nはどこですか", "back": "Nはどこですか。= Where is N?\nトイレはどこですか。= Where is the restroom?\nデパートはどこですか。= Where is the department store?\n\nAnswer: 〜にあります / 〜です"},
    {"front": "Existence: あります vs います", "back": "あります = there is (non-living things)\nエレベーターはあそこにあります。\n= The elevator is over there.\n\nいます = there is (living things — covered in L4!)"},
]

ch3_grammar_q = [
    {"question": "トイレは ___ ですか。(Where is the restroom?)", "answer": "どこ", "options": ["どこ", "ここ", "そこ", "どちら"], "explanation": "どこ = where? Used in questions about location. どちら is the polite version."},
    {"question": "エレベーターはあそこ ___ あります。(The elevator is over there.)", "answer": "に", "options": ["に", "で", "は", "を"], "explanation": "に marks the location of existence (where something is). あります = exists (non-living things)."},
    {"question": "デパートは ___ かいですか。(Which floor is the department store on?)", "answer": "なん", "options": ["なん", "どこ", "いくら", "なに"], "explanation": "なんかい = which floor? なん + かい (floor counter) = which floor?"},
    {"question": "レストランはにかいです。Where is the restaurant?", "answer": "2nd floor", "options": ["2nd floor", "1st floor", "3rd floor", "basement"], "explanation": "にかい = 2nd floor. に = 2, かい = floor counter. いっかい = 1F, さんかい/さんがい = 3F."},
    {"question": "これはいくら ___ か。(How much is this?)", "answer": "です", "options": ["です", "ます", "でした", "でしょう"], "explanation": "いくらですか = How much is it? です + か = polite question."},
    {"question": "500円は ___ ですか。(How do you say 500 yen?)", "answer": "ごひゃくえん", "options": ["ごひゃくえん", "いつえん", "ごじゅうえん", "ごひゃくえんです"], "explanation": "500 = ごひゃく (5 × 100). 百 = ひゃく. 500円 = ごひゃくえん."},
    {"question": "ゆうびんきょくはどこですか → ___にあります。(It's in front of the bank.)", "answer": "ぎんこうのまえ", "options": ["ぎんこうのまえ", "ぎんこうのうしろ", "びょういんのまえ", "デパートのなか"], "explanation": "まえ = front/before. ぎんこうのまえ = in front of the bank. の connects place to direction."},
    {"question": "エレベーターはあります。What does this sentence lack to be complete?", "answer": "A location (にあります)", "options": ["A location (にあります)", "A subject marker", "A question mark", "Nothing — it's complete"], "explanation": "あります needs a location: Nは[place]にあります. Without the location, the sentence is incomplete."},
    {"question": "どちらへどうぞ。What does this phrase mean?", "answer": "This way, please.", "options": ["This way, please.", "Where are you going?", "Please wait here.", "Which floor?"], "explanation": "どちらへどうぞ = 'Please go this way.' どちら = polite 'which way/where', へ = direction particle, どうぞ = please."},
    {"question": "こちら = ?", "answer": "This way / here (polite)", "options": ["This way / here (polite)", "That way (near you, polite)", "Over there (polite)", "Which way? (polite)"], "explanation": "こちら is the polite form of ここ/こっち. Used in formal or service situations."},
    {"question": "としょかんはなんかいですか → ___ かいです。(It's on the 4th floor.)", "answer": "よん", "options": ["よん", "し", "よ", "ふ"], "explanation": "4th floor = よんかい. よん is preferred over し for floor numbers to avoid confusion."},
    {"question": "The food hall is in the basement. How do you say 'basement 1'?", "answer": "ちかいっかい", "options": ["ちかいっかい", "したかい", "いちかい", "ちかわん"], "explanation": "ちか (地下) = underground/basement. ちかいっかい = B1 (basement 1st floor)."},
]

ch3_examples_teach = [
    {"front": "Asking directions inside a building", "back": "A: すみません、エレベーターはどこですか。\nB: あちらです。\n\nA: Excuse me, where is the elevator?\nB: It's over there. (polite)"},
    {"front": "Department store floor guide", "back": "B1 = ちかいっかい (food hall / しょくひんかん)\n1F = いっかい (accessories / accessories)\n2F = にかい (women's clothing)\n3F = さんかい (men's clothing)\n4F = よんかい (furniture)"},
    {"front": "Asking price", "back": "A: すみません、これはいくらですか。\nB: それは3,500円です。\n\nA: Excuse me, how much is this?\nB: That's 3,500 yen.\n(さんぜんごひゃくえん)"},
    {"front": "Location dialogue", "back": "A: ゆうびんきょくはどこですか。\nB: ぎんこうのとなりです。\n\nA: Where is the post office?\nB: It's next to the bank.\n\nとなり = next to / neighbor"},
    {"front": "Key location phrases", "back": "〜はどこですか。= Where is ~?\nNは〜にあります。= N is at ~.\nこちらへどうぞ。= Please come this way.\nすぐそこです。= It's right there."},
    {"front": "Numbers & Money", "back": "100円 = ひゃくえん\n500円 = ごひゃくえん\n1,000円 = せんえん\n5,000円 = ごせんえん\n10,000円 = いちまんえん\n\nお金 (おかね) = money"},
]

ch3_examples_q = [
    {"question": "You're in a department store. How do you ask where the restroom is?", "answer": "すみません、トイレはどこですか。", "options": ["すみません、トイレはどこですか。", "すみません、トイレがどこですか。", "すみません、トイレをどこですか。", "すみません、どこはトイレですか。"], "explanation": "NはどこですかWhere is N? は marks the topic (what you're asking about)."},
    {"question": "Something costs 1,500 yen. How do you say this?", "answer": "せんごひゃくえん", "options": ["せんごひゃくえん", "ひゃくごじゅうえん", "いちごひゃくえん", "せんいつえん"], "explanation": "1500 = せん (1000) + ごひゃく (500) = せんごひゃくえん."},
    {"question": "The elevator is on the right. How do you tell someone?", "answer": "エレベーターはみぎにあります。", "options": ["エレベーターはみぎにあります。", "エレベーターでみぎにあります。", "エレベーターをみぎにあります。", "エレベーターがみぎにあります。"], "explanation": "Location with あります: Nは[place]にあります. に marks location of existence."},
    {"question": "A staff member says こちらへどうぞ。What should you do?", "answer": "Follow them in the direction they indicate", "options": ["Follow them in the direction they indicate", "Wait where you are", "Say thank you and leave", "Ask for the price"], "explanation": "こちらへどうぞ = Please come this way. Staff use this to guide customers."},
    {"question": "You want to find the bank. What do you ask?", "answer": "ぎんこうはどこですか。", "options": ["ぎんこうはどこですか。", "ぎんこうがどこですか。", "ぎんこうにどこですか。", "ぎんこうをどこですか。"], "explanation": "Nはどこですか = Where is N? Simple and direct question for location."},
    {"question": "The library is on the 3rd floor. Which is correct?", "answer": "としょかんはさんかいにあります。", "options": ["としょかんはさんかいにあります。", "としょかんはさんかいであります。", "としょかんをさんかいにあります。", "としょかんにさんかいあります。"], "explanation": "Nは[floor]にあります = N is on [floor]. に marks the location."},
    {"question": "How do you say 'It's right over there'?", "answer": "あそこです。/ すぐあそこです。", "options": ["あそこです。/ すぐあそこです。", "ここです。", "そこです。", "どこです。"], "explanation": "あそこ = over there (far from both speakers). すぐ = immediately/right (すぐあそこ = right over there)."},
    {"question": "A: レストランはなんかいですか。B: ___かいです。(6th floor)", "answer": "ろく", "options": ["ろく", "ご", "なな", "はち"], "explanation": "6th floor = ろっかい (or ろくかい). ろく = 6."},
]

write(make_vocab_lesson(3, "ここはどこですか", "Where Is This Place?", "🏢", ch3_vocab_teach, ch3_vocab))
write(make_grammar_lesson(3, "ここはどこですか", "Where Is This Place?", "🏢", ch3_vocab_teach, ch3_grammar_q))
write(make_examples_lesson(3, "ここはどこですか", "Where Is This Place?", "🏢", ch3_examples_teach, ch3_examples_q))

# ══════════════════════════════════════════════════════════════
# CHAPTER 4: 毎日何時に起きますか — What Time Do You Get Up?
# ══════════════════════════════════════════════════════════════
ch4_vocab = [
    ("なんじ (何時)", "what time?", ["how many?", "which floor?", "how much?"]),
    ("〜じ (〜時)", "o'clock (time counter)", ["floor counter", "minute counter", "day counter"]),
    ("〜ふん/ぷん (〜分)", "minutes", ["hours", "seconds", "days"]),
    ("ごぜん (午前)", "AM / morning", ["PM / afternoon", "evening", "midnight"]),
    ("ごご (午後)", "PM / afternoon", ["AM / morning", "evening", "midnight"]),
    ("おきます (起きます)", "to wake up / get up", ["to sleep", "to eat", "to go"]),
    ("ねます (寝ます)", "to sleep / go to bed", ["to wake up", "to eat", "to work"]),
    ("はたらきます (働きます)", "to work", ["to study", "to sleep", "to play"]),
    ("やすみます (休みます)", "to rest / take a day off", ["to work", "to study", "to wake up"]),
    ("べんきょうします (勉強します)", "to study", ["to work", "to rest", "to eat"]),
    ("たべます (食べます)", "to eat", ["to drink", "to sleep", "to study"]),
    ("のみます (飲みます)", "to drink", ["to eat", "to sleep", "to work"]),
    ("みます (見ます)", "to watch / see / look", ["to listen", "to read", "to speak"]),
    ("ききます (聞きます)", "to listen / hear / ask", ["to watch", "to read", "to speak"]),
    ("まいにち (毎日)", "every day", ["every week", "every month", "sometimes"]),
    ("から", "from (starting point)", ["to (ending point)", "and", "because"]),
    ("まで", "until / to (ending point)", ["from", "and", "but"]),
    ("ごろ", "around / about (approximate time)", ["exactly", "before", "after"]),
    ("なんじかん (何時間)", "how many hours?", ["how many minutes?", "how many days?", "what time?"]),
    ("はん (半)", "half (30 minutes)", ["quarter", "full hour", "minute"]),
]

ch4_vocab_teach = [
    {"front": "Telling time: 〜じ〜ふん", "back": "〜時 (じ) = o'clock\n〜分 (ふん/ぷん) = minutes\n\n3:00 = さんじ\n3:30 = さんじはん (half past 3)\n3:15 = さんじじゅうごふん\n\nごぜん = AM, ごご = PM"},
    {"front": "Tricky minute readings", "back": "1分 = いっぷん\n3分 = さんぷん\n4分 = よんぷん\n6分 = ろっぷん\n8分 = はっぷん\n10分 = じゅっぷん\n\nRule: ふん changes to ぷん after certain numbers!"},
    {"front": "Daily activity verbs", "back": "起きます (おきます) = wake up\n寝ます (ねます) = sleep\n食べます (たべます) = eat\n飲みます (のみます) = drink\n働きます (はたらきます) = work\n休みます (やすみます) = rest"},
    {"front": "Study verbs", "back": "勉強します (べんきょうします) = study\n見ます (みます) = watch / see\n聞きます (ききます) = listen / hear\n読みます (よみます) = read\n書きます (かきます) = write"},
    {"front": "Time particles", "back": "〜に = at (specific time)\n毎朝7時に起きます。= I wake up at 7 every morning.\n\nから = from\nまで = until\n9時から5時まで = from 9 to 5\n\nごろ = around\n7時ごろ = around 7 o'clock"},
    {"front": "まいにち / まいあさ / まいばん", "back": "毎日 (まいにち) = every day\n毎朝 (まいあさ) = every morning\n毎晩 (まいばん) = every evening\n毎週 (まいしゅう) = every week\n\nNote: These words do NOT use the に particle!"},
    {"front": "はん = half past", "back": "〜時はん = half past ~\n3時半 = さんじはん = 3:30\n\nCompare:\n3時15分 = さんじじゅうごふん (3:15)\n3時30分 = さんじさんじっぷん = さんじはん (3:30)\n3時45分 = さんじよんじゅうごふん (3:45)"},
    {"front": "Asking what time", "back": "何時ですか。= What time is it?\n何時に〜しますか。= At what time do you ~?\n\nA: 何時に起きますか。\nB: 7時に起きます。\n\nA: What time do you wake up?\nB: I wake up at 7."},
]

ch4_grammar_q = [
    {"question": "毎朝7時 ___ 起きます。(I wake up at 7 every morning.)", "answer": "に", "options": ["に", "で", "は", "を"], "explanation": "に marks specific time points. 7時に = at 7 o'clock. Note: まいあさ does not take に, but the clock time does."},
    {"question": "9時 ___ 5時まで働きます。(I work from 9 to 5.)", "answer": "から", "options": ["から", "まで", "に", "で"], "explanation": "から = from. まで = until/to. 9時から5時まで = from 9 o'clock to 5 o'clock."},
    {"question": "3:30 in Japanese is:", "answer": "さんじはん", "options": ["さんじはん", "さんじさんじゅっぷん", "さんじごふん", "さんじよんじゅうごふん"], "explanation": "はん = half. 3時半 (さんじはん) = 3:30. You can also say さんじさんじゅっぷん."},
    {"question": "毎日 ___ テレビを見ます。Does 毎日 need a particle?", "answer": "No particle needed after 毎日", "options": ["No particle needed after 毎日", "に after 毎日", "で after 毎日", "を after 毎日"], "explanation": "Time words like 毎日、毎朝、毎晩 do NOT take the に particle. Just use them directly before the verb."},
    {"question": "7時 ___ 起きます。(I wake up around 7.)", "answer": "ごろに", "options": ["ごろに", "ごろ", "ごろで", "にごろ"], "explanation": "ごろ = around/approximately. 7時ごろに = around 7 o'clock. ごろ comes AFTER the time, に comes after ごろ."},
    {"question": "What time is ごぜん11じ?", "answer": "11 AM", "options": ["11 AM", "11 PM", "23:00", "1 AM"], "explanation": "ごぜん = AM (morning). ごご = PM (afternoon). ごぜん11じ = 11 o'clock in the morning."},
    {"question": "How do you say '1 minute' in Japanese?", "answer": "いっぷん", "options": ["いっぷん", "いちふん", "いちぷん", "いっふん"], "explanation": "1分 = いっぷん. Special reading! 1/3/6/8/10 change ふん to ぷん (いっぷん、さんぷん、ろっぷん、はっぷん、じゅっぷん)."},
    {"question": "A: 何時間べんきょうしますか。B: ___じかんです。(3 hours)", "answer": "さん", "options": ["さん", "み", "みっ", "みつ"], "explanation": "Hours: 何時間 = how many hours. さんじかん = 3 hours. (1時間=いちじかん, 2時間=にじかん, 3時間=さんじかん)"},
    {"question": "シュミットさんは ___ 働きますか。(When does Schmidt-san work?)", "answer": "なんじから なんじまで", "options": ["なんじから なんじまで", "なんじに", "どこで", "なんじごろ"], "explanation": "To ask 'from what time to what time', use なんじから なんじまで."},
    {"question": "毎晩 ___ 寝ますか。(What time do you go to bed every night?)", "answer": "何時に", "options": ["何時に", "何時から", "何時まで", "何時ごろ"], "explanation": "Asking for a specific time uses なんじに. Answer: 11時に寝ます (I sleep at 11)."},
    {"question": "6:00 in Japanese:", "answer": "ろくじ", "options": ["ろくじ", "むじ", "むっつじ", "ろっじ"], "explanation": "6:00 = ろくじ. Numbers for hours: 1=いち, 2=に, 3=さん, 4=よ, 5=ご, 6=ろく, 7=しち, 8=はち, 9=く, 10=じゅう, 11=じゅういち, 12=じゅうに."},
]

ch4_examples_teach = [
    {"front": "Talking about daily schedule", "back": "毎朝6時に起きます。= I wake up at 6 every morning.\n7時から8時まで勉強します。= I study from 7 to 8.\nごご5時まで働きます。= I work until 5 PM."},
    {"front": "Asking about someone's schedule", "back": "A: 毎朝何時に起きますか。\nB: 6時半に起きます。\n\nA: What time do you wake up every morning?\nB: I wake up at 6:30."},
    {"front": "Japanese time format", "back": "Japan uses 24-hour and 12-hour formats.\nごぜん (午前) = AM\nごご (午後) = PM\n\n13:00 = ごご1じ (1 PM)\n18:30 = ごご6じはん (6:30 PM)\n\nOfficial notices often use 13時, 18時 etc."},
    {"front": "Verb dictionary form → ます form", "back": "おきる → おきます (wake up)\nねる → ねます (sleep)\nたべる → たべます (eat)\nのむ → のみます (drink)\nはたらく → はたらきます (work)\n\nます form = polite present/habitual tense"},
    {"front": "Negative: 〜ません", "back": "Replace ます with ません for negative.\n起きます → 起きません (don't wake up)\n食べます → 食べません (don't eat)\n\nExample: あさごはんを食べません。\n= I don't eat breakfast."},
    {"front": "Key question: 何時間〜ますか", "back": "A: 毎日何時間べんきょうしますか。\nB: ２時間べんきょうします。\n\nA: How many hours do you study every day?\nB: I study for 2 hours.\n\n〜時間 (じかん) = ~ hours"},
]

ch4_examples_q = [
    {"question": "How do you say 'I wake up at 6:30 every morning'?", "answer": "毎朝6時半に起きます。", "options": ["毎朝6時半に起きます。", "毎朝6時半で起きます。", "毎朝に6時半起きます。", "毎朝6時半から起きます。"], "explanation": "Specific time uses に: 6時半に起きます. まいあさ doesn't need に, but the clock time does."},
    {"question": "You work from 9AM to 6PM. How do you say this?", "answer": "ごぜん9時からごご6時まではたらきます。", "options": ["ごぜん9時からごご6時まではたらきます。", "ごぜん9時にごご6時まではたらきます。", "ごぜん9時からごご6時にはたらきます。", "ごぜん9時ごろごご6時まではたらきます。"], "explanation": "から〜まで = from〜to. ごぜん = AM, ごご = PM."},
    {"question": "A: 毎晩何時に寝ますか。B: 11時ごろに寝ます。What does ごろ mean here?", "answer": "Around / approximately", "options": ["Around / approximately", "Exactly", "Before", "After"], "explanation": "ごろ = around/approximately. 11時ごろに = around 11 o'clock (not exactly)."},
    {"question": "You don't eat breakfast. How do you say this?", "answer": "あさごはんを食べません。", "options": ["あさごはんを食べません。", "あさごはんが食べません。", "あさごはんは食べません。", "あさごはんで食べません。"], "explanation": "を marks the direct object of eating. Negative: 食べません. (Note: は can also be used for contrast.)"},
    {"question": "What time is 7:15?", "answer": "しちじじゅうごふん", "options": ["しちじじゅうごふん", "ななじじゅうごふん", "しちじごじゅっぷん", "ごじじゅうなな"], "explanation": "7:15 = しちじじゅうごふん. Hours use しち (7), minutes use regular numbers + ふん."},
    {"question": "How do you ask 'How many hours do you work?'", "answer": "なんじかんはたらきますか。", "options": ["なんじかんはたらきますか。", "なんじにはたらきますか。", "なんじまではたらきますか。", "なんじからはたらきますか。"], "explanation": "何時間 (なんじかん) = how many hours? This asks duration, not the clock time."},
    {"question": "You study from 8PM to 10PM. How do you express this?", "answer": "ごご8時から10時まで勉強します。", "options": ["ごご8時から10時まで勉強します。", "ごご8時に10時まで勉強します。", "ごご8時から10時に勉強します。", "ごご8時まで10時から勉強します。"], "explanation": "から = from, まで = until/to. 8時から10時まで = from 8 to 10."},
    {"question": "What does まいばん mean?", "answer": "Every evening / every night", "options": ["Every evening / every night", "Every morning", "Every week", "Every day"], "explanation": "毎晩 (まいばん) = every evening/night. 毎朝 (まいあさ) = every morning. 毎日 (まいにち) = every day."},
]

write(make_vocab_lesson(4, "毎日何時に起きますか", "What Time Do You Get Up?", "⏰", ch4_vocab_teach, ch4_vocab))
write(make_grammar_lesson(4, "毎日何時に起きますか", "What Time Do You Get Up?", "⏰", ch4_vocab_teach, ch4_grammar_q))
write(make_examples_lesson(4, "毎日何時に起きますか", "What Time Do You Get Up?", "⏰", ch4_examples_teach, ch4_examples_q))

# ══════════════════════════════════════════════════════════════
# CHAPTER 5: 誕生日はいつですか — When Is Your Birthday?
# ══════════════════════════════════════════════════════════════
ch5_vocab = [
    ("いつ", "when?", ["where?", "who?", "what?"]),
    ("たんじょうび (誕生日)", "birthday", ["holiday", "anniversary", "wedding"]),
    ("〜がつ (〜月)", "month (counter)", ["year counter", "day counter", "week counter"]),
    ("〜にち/か (〜日)", "day of the month (counter)", ["month counter", "year counter", "week counter"]),
    ("なんがつ (何月)", "which month?", ["which day?", "which year?", "when?"]),
    ("なんにち (何日)", "which day of the month?", ["which month?", "which year?", "how many?"]),
    ("きょう (今日)", "today", ["yesterday", "tomorrow", "the day after tomorrow"]),
    ("きのう (昨日)", "yesterday", ["today", "tomorrow", "the day before"]),
    ("あした (明日)", "tomorrow", ["today", "yesterday", "next week"]),
    ("あさって", "the day after tomorrow", ["yesterday", "today", "tomorrow"]),
    ("せんしゅう (先週)", "last week", ["this week", "next week", "last month"]),
    ("こんしゅう (今週)", "this week", ["last week", "next week", "this month"]),
    ("らいしゅう (来週)", "next week", ["this week", "last week", "next month"]),
    ("せんげつ (先月)", "last month", ["this month", "next month", "last year"]),
    ("こんげつ (今月)", "this month", ["last month", "next month", "this year"]),
    ("らいげつ (来月)", "next month", ["this month", "last month", "next year"]),
    ("きょねん (去年)", "last year", ["this year", "next year", "two years ago"]),
    ("ことし (今年)", "this year", ["last year", "next year", "the year before"]),
    ("らいねん (来年)", "next year", ["this year", "last year", "in two years"]),
    ("〜ねん (〜年)", "year (counter)", ["month counter", "day counter", "week counter"]),
]

ch5_vocab_teach = [
    {"front": "Months (〜月)", "back": "1月 = いちがつ (January)\n2月 = にがつ (February)\n3月 = さんがつ (March)\n4月 = しがつ (April)\n5月 = ごがつ (May)\n6月 = ろくがつ (June)\n7月 = しちがつ (July)\n8月 = はちがつ (August)\n9月 = くがつ (September)\n10月 = じゅうがつ (October)\n11月 = じゅういちがつ (November)\n12月 = じゅうにがつ (December)"},
    {"front": "Tricky dates (1st–10th)", "back": "1日 = ついたち\n2日 = ふつか\n3日 = みっか\n4日 = よっか\n5日 = いつか\n6日 = むいか\n7日 = なのか\n8日 = ようか\n9日 = ここのか\n10日 = とおか\n14日 = じゅうよっか\n20日 = はつか\n24日 = にじゅうよっか"},
    {"front": "Relative time: days", "back": "おととい = the day before yesterday\nきのう (昨日) = yesterday\nきょう (今日) = today\nあした (明日) = tomorrow\nあさって = the day after tomorrow"},
    {"front": "Relative time: weeks/months/years", "back": "せんしゅう / こんしゅう / らいしゅう = last/this/next week\nせんげつ / こんげつ / らいげつ = last/this/next month\nきょねん / ことし / らいねん = last/this/next year"},
    {"front": "Asking about dates", "back": "いつですか。= When is it?\n何月何日ですか。= What is the month and day?\n何曜日ですか。= What day of the week?\n\nExample:\nA: たんじょうびはいつですか。\nB: 4月14日です。(しがつじゅうよっかです)"},
    {"front": "Days of the week", "back": "月曜日 (げつようび) = Monday\n火曜日 (かようび) = Tuesday\n水曜日 (すいようび) = Wednesday\n木曜日 (もくようび) = Thursday\n金曜日 (きんようび) = Friday\n土曜日 (どようび) = Saturday\n日曜日 (にちようび) = Sunday"},
    {"front": "Saying the year", "back": "2024年 = にせんにじゅうよねん\n1990年 = せんきゅうひゃくきゅうじゅうねん\n\nJapanese era years (令和/Reiwa):\n令和6年 = れいわろくねん = 2024\n\nGenerally use Western years in conversation."},
    {"front": "Birthday conversation", "back": "A: たんじょうびはいつですか。\nB: 5月3日です。\nA: そうですか。もうすぐですね！\n\nA: When is your birthday?\nB: May 3rd.\nA: Is that so. It's coming up soon!"},
]

ch5_grammar_q = [
    {"question": "たんじょうびは ___ ですか。(When is your birthday?)", "answer": "いつ", "options": ["いつ", "なに", "どこ", "だれ"], "explanation": "いつ = when? Used to ask about time/dates. (なに = what, どこ = where, だれ = who)"},
    {"question": "How do you say 'May 3rd'?", "answer": "ごがつみっか", "options": ["ごがつみっか", "ごがつさんにち", "ごがつさんか", "ごがつみか"], "explanation": "5月 = ごがつ. 3日 = みっか (irregular reading). These special date readings must be memorized!"},
    {"question": "How do you say 'January 1st'?", "answer": "いちがつついたち", "options": ["いちがつついたち", "いちがつちいたち", "いちがついちにち", "いちがつひとにち"], "explanation": "1月 = いちがつ. 1日 = ついたち (irregular — must memorize!). Not いちにち."},
    {"question": "How do you say 'next month'?", "answer": "らいげつ", "options": ["らいげつ", "こんげつ", "せんげつ", "つぎつき"], "explanation": "来月 (らいげつ) = next month. 今月 (こんげつ) = this month. 先月 (せんげつ) = last month."},
    {"question": "What day is 20日?", "answer": "はつか", "options": ["はつか", "にじゅうにち", "はっか", "にじゅうか"], "explanation": "20日 = はつか. Irregular reading — must memorize! 14日 = じゅうよっか, 24日 = にじゅうよっか are also irregular."},
    {"question": "What is the month for 9月?", "answer": "September", "options": ["September", "July", "October", "August"], "explanation": "9月 = くがつ = September. Months in order: 1=Jan, 4=Apr, 7=Jul, 9=Sep, 12=Dec."},
    {"question": "How do you say 'What month and day is it?'", "answer": "なんがつなんにちですか", "options": ["なんがつなんにちですか", "なんじなんぷんですか", "なんようびですか", "いつですか"], "explanation": "何月何日ですか = What month and day is it? なんがつ = which month, なんにち = which day."},
    {"question": "きょう is 月曜日. What day is らいしゅうの月曜日?", "answer": "Next Monday", "options": ["Next Monday", "Last Monday", "This Monday", "Yesterday's Monday"], "explanation": "来週 (らいしゅう) = next week. 来週の月曜日 = next Monday (Monday of next week)."},
    {"question": "How do you say 'the day after tomorrow'?", "answer": "あさって", "options": ["あさって", "あした", "きのう", "おととい"], "explanation": "あさって = the day after tomorrow. あした = tomorrow. きのう = yesterday. おととい = the day before yesterday."},
    {"question": "What is 14日 read as?", "answer": "じゅうよっか", "options": ["じゅうよっか", "じゅうしにち", "じゅうよんにち", "じゅうよにち"], "explanation": "14日 = じゅうよっか. The よっ (4) part is irregular in dates. Also applies to 24日 = にじゅうよっか."},
    {"question": "How do you say 'August 8th'?", "answer": "はちがつようか", "options": ["はちがつようか", "はちがつはちにち", "はちがつようにち", "はちがつはちか"], "explanation": "8月 = はちがつ. 8日 = ようか (irregular). Both 8月 and 8日 have special readings."},
    {"question": "What year is にせんにじゅうよねん?", "answer": "2024", "options": ["2024", "2014", "2004", "2040"], "explanation": "2000 = にせん, 2024 = にせんにじゅうよ. に(2) + せん(000) + に(2) + じゅう(10) + よ(4) = 2024."},
]

ch5_examples_teach = [
    {"front": "Birthday conversation", "back": "A: ミラーさんのたんじょうびはいつですか。\nB: 9月18日です。\nA: そうですか。何曜日ですか。\nB: 火曜日です。\n\nA: When is your birthday, Miller-san?\nB: September 18th.\nA: Is that so. What day of the week?\nB: Tuesday."},
    {"front": "Planning: 'What day is convenient?'", "back": "A: 来週のいつがいいですか。\nB: 水曜日はどうですか。\nA: いいですね。\n\nA: When is good next week?\nB: How about Wednesday?\nA: That's good!"},
    {"front": "Japanese holidays", "back": "1月1日 = お正月 (New Year)\n2月11日 = けんこくきねんびNational Foundation Day\n3月21日ごろ = しゅんぶんのひ (Spring Equinox)\n5月3日 = けんぽうきねんび (Constitution Day)\n8月11日 = やまのひ (Mountain Day)\n11月3日 = ぶんかのひ (Culture Day)"},
    {"front": "Asking the date today", "back": "A: 今日は何月何日ですか。\nB: 4月14日です。\nA: 何曜日ですか。\nB: 月曜日です。\n\nA: What is today's date?\nB: April 14th.\nA: What day is it?\nB: Monday."},
    {"front": "Giving relative time expressions", "back": "今日は火曜日です。\n昨日は月曜日でした。\n明日は水曜日です。\n\nToday is Tuesday.\nYesterday was Monday.\nTomorrow is Wednesday.\n\nPast → でした (was/were)"},
    {"front": "Using でした (past of です)", "back": "たんじょうびは先週でした。\n= My birthday was last week.\n\nです → でした (past)\nじゃありません → じゃありませんでした (past negative)\n\nExample:\nきのうはいいてんきでした。\n= Yesterday was good weather."},
]

ch5_examples_q = [
    {"question": "How do you ask 'When is your birthday?'", "answer": "たんじょうびはいつですか。", "options": ["たんじょうびはいつですか。", "たんじょうびはなんですか。", "たんじょうびはどこですか。", "たんじょうびはだれですか。"], "explanation": "いつ = when? Used for dates and times. たんじょうびはいつですか = When is the birthday?"},
    {"question": "Today is April 14th. How do you say this?", "answer": "今日はしがつじゅうよっかです。", "options": ["今日はしがつじゅうよっかです。", "今日はよんがつじゅうよんにちです。", "今日はしがつじゅうしにちです。", "今日はよんがつよんにちです。"], "explanation": "4月 = しがつ. 14日 = じゅうよっか (irregular). Both readings are important to know!"},
    {"question": "Your friend's birthday is next month. Which phrase describes this?", "answer": "らいげつ", "options": ["らいげつ", "こんげつ", "せんげつ", "きょねん"], "explanation": "来月 (らいげつ) = next month. こんげつ = this month. せんげつ = last month."},
    {"question": "Someone says 先週の金曜日. What does this mean?", "answer": "Last Friday", "options": ["Last Friday", "Next Friday", "This Friday", "Last Saturday"], "explanation": "先週 (せんしゅう) = last week. 金曜日 = Friday. 先週の金曜日 = last Friday."},
    {"question": "How do you say 'My birthday was yesterday'?", "answer": "たんじょうびはきのうでした。", "options": ["たんじょうびはきのうでした。", "たんじょうびはきのうです。", "たんじょうびにきのうです。", "たんじょうびはきのうでしたか。"], "explanation": "でした = past tense of です. きのう = yesterday. たんじょうびはきのうでした = Birthday was yesterday."},
    {"question": "What is 水曜日?", "answer": "Wednesday", "options": ["Wednesday", "Monday", "Friday", "Saturday"], "explanation": "水曜日 (すいようび) = Wednesday. 水 = water. Days: 月=Mon, 火=Tue, 水=Wed, 木=Thu, 金=Fri, 土=Sat, 日=Sun."},
    {"question": "A: 今日は何曜日ですか。B: ___です。(It's Thursday.)", "answer": "木曜日 (もくようび)", "options": ["木曜日 (もくようび)", "水曜日 (すいようび)", "金曜日 (きんようび)", "土曜日 (どようび)"], "explanation": "木曜日 (もくようび) = Thursday. 木 = tree/wood (木星 = Jupiter, Thor's planet!)."},
    {"question": "How do you say 'How many months until your birthday?'", "answer": "たんじょうびまでなんかげつですか。", "options": ["たんじょうびまでなんかげつですか。", "たんじょうびになんかげつですか。", "たんじょうびからなんかげつですか。", "たんじょうびでなんかげつですか。"], "explanation": "まで = until/to. なんかげつ = how many months. 〜までなんかげつ = how many months until ~."},
]

write(make_vocab_lesson(5, "誕生日はいつですか", "When Is Your Birthday?", "🎂", ch5_vocab_teach, ch5_vocab))
write(make_grammar_lesson(5, "誕生日はいつですか", "When Is Your Birthday?", "🎂", ch5_vocab_teach, ch5_grammar_q))
write(make_examples_lesson(5, "誕生日はいつですか", "When Is Your Birthday?", "🎂", ch5_examples_teach, ch5_examples_q))

print("\n✅ Chapters 1–5 complete (15 files generated)")

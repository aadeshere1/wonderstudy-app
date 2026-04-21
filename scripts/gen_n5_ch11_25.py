#!/usr/bin/env python3
"""Generate JLPT N5 lesson files for Minna no Nihongo chapters 11-25."""
import json, os, random

OUT = "/sessions/festive-blissful-meitner/mnt/wonderstudy-app/data/classes/jlpt/n5"

def make_vocab_lesson(num, jp_title, en_title, icon, teach_cards, vocab_items):
    practice, challenge = [], []
    for (q, ans, others) in vocab_items:
        opts = [ans] + others[:3]; random.shuffle(opts)
        practice.append({"question": q, "answer": ans, "options": opts})
    for (q, ans, others) in vocab_items[:15]:
        jp_opts = [q] + [x[0] for x in vocab_items if x[0] != q][:3]; random.shuffle(jp_opts)
        challenge.append({"question": f"How do you say '{ans}' in Japanese?", "answer": q, "options": jp_opts})
    return {"id": f"ch{num:02d}-vocabulary", "meta": {"title": f"Lesson {num}: {jp_title} — Vocabulary", "subject": "japanese", "class": None, "lesson": f"ch{num:02d}-vocabulary", "subtopic": en_title, "description": f"Vocabulary for Minna no Nihongo Lesson {num}: {en_title}", "icon": icon, "difficulty": "beginner"}, "teach": {"type": "flashcard", "items": teach_cards}, "practice": {"gameType": "vocab", "config": {"answerMode": "mcq", "optionsCount": 4, "timeLimit": 20, "questionsCount": min(15, len(practice))}, "items": practice}, "challenge": {"gameType": "vocab", "config": {"answerMode": "mcq", "optionsCount": 4, "timeLimit": 10, "questionsCount": min(15, len(challenge))}, "items": challenge}}

def make_grammar_lesson(num, jp_title, en_title, icon, teach_cards, practice_items):
    return {"id": f"ch{num:02d}-grammar", "meta": {"title": f"Lesson {num}: {jp_title} — Grammar", "subject": "japanese", "class": None, "lesson": f"ch{num:02d}-grammar", "subtopic": en_title, "description": f"Grammar patterns for Minna no Nihongo Lesson {num}: {en_title}", "icon": icon, "difficulty": "beginner"}, "teach": {"type": "flashcard", "items": teach_cards}, "practice": {"gameType": "mcq-facts", "config": {"shuffleOptions": True, "timeLimit": 25, "questionsCount": min(15, len(practice_items))}, "items": practice_items}, "challenge": {"gameType": "mcq-facts", "config": {"shuffleOptions": True, "timeLimit": 12, "questionsCount": min(15, len(practice_items))}, "items": practice_items}}

def make_examples_lesson(num, jp_title, en_title, icon, teach_cards, practice_items):
    return {"id": f"ch{num:02d}-examples", "meta": {"title": f"Lesson {num}: {jp_title} — Dialogue & Examples", "subject": "japanese", "class": None, "lesson": f"ch{num:02d}-examples", "subtopic": en_title, "description": f"Practical dialogues and sentences for Lesson {num}: {en_title}", "icon": icon, "difficulty": "beginner"}, "teach": {"type": "flashcard", "items": teach_cards}, "practice": {"gameType": "mcq-facts", "config": {"shuffleOptions": True, "timeLimit": 25, "questionsCount": min(15, len(practice_items))}, "items": practice_items}, "challenge": {"gameType": "mcq-facts", "config": {"shuffleOptions": True, "timeLimit": 12, "questionsCount": min(15, len(practice_items))}, "items": practice_items}}

def write(lesson):
    path = os.path.join(OUT, lesson["id"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(lesson, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {lesson['id']}.json")

# ══════════════════════════════════════════════════════════════
# CHAPTER 11: どこかへ行きましたか — Did You Go Anywhere?
# ══════════════════════════════════════════════════════════════
ch11_vocab = [
    ("どこか", "somewhere / anywhere", ["nowhere", "everywhere", "here"]),
    ("なにか (何か)", "something / anything", ["nothing", "everything", "what?"]),
    ("だれか (誰か)", "someone / anyone", ["no one", "everyone", "who?"]),
    ("どこも〜ない", "nowhere (with negative)", ["somewhere", "everywhere", "anywhere"]),
    ("なにも〜ない (何も〜ない)", "nothing (with negative)", ["something", "everything", "anything"]),
    ("だれも〜ない (誰も〜ない)", "no one (with negative)", ["someone", "everyone", "anyone"]),
    ("きました (来ました)", "came (past of 来ます)", ["went", "returned", "stayed"]),
    ("いきました (行きました)", "went (past of 行きます)", ["came", "returned", "stayed"]),
    ("かえりました (帰りました)", "returned home (past)", ["went out", "came", "stayed"]),
    ("あいました (会いました)", "met (past of 会います)", ["separated", "called", "saw"]),
    ("みました (見ました)", "watched/saw (past)", ["heard", "bought", "ate"]),
    ("たべました (食べました)", "ate (past of 食べます)", ["drank", "bought", "cooked"]),
    ("のみました (飲みました)", "drank (past of 飲みます)", ["ate", "bought", "cooked"]),
    ("かいました (買いました)", "bought (past of 買います)", ["sold", "borrowed", "returned"]),
    ("おわります (終わります)", "to end / finish", ["to start", "to continue", "to rest"]),
    ("はじまります (始まります)", "to begin / start (intransitive)", ["to end", "to continue", "to pause"]),
    ("〜ました", "past tense (positive)", ["present tense", "negative past", "negative present"]),
    ("〜ませんでした", "past tense (negative)", ["past tense positive", "present negative", "present positive"]),
    ("しゅうまつ (週末)", "weekend", ["weekday", "holiday", "vacation"]),
    ("やすみ (休み)", "holiday / day off / rest", ["working day", "overtime", "busy day"]),
]

ch11_teach_vocab = [
    {"front": "Indefinite pronouns: どこか / なにか / だれか", "back": "どこか = somewhere / anywhere\nなにか = something / anything\nだれか = someone / anyone\n\nUsed in POSITIVE sentences:\nどこかへ行きましたか。= Did you go somewhere?\nなにかたべましたか。= Did you eat something?"},
    {"front": "Negative indefinite: どこも / なにも / だれも", "back": "どこも〜ない = nowhere\nなにも〜ない = nothing\nだれも〜ない = no one\n\nUsed with NEGATIVE verbs:\nどこもいきませんでした。= I didn't go anywhere.\nなにもたべませんでした。= I didn't eat anything."},
    {"front": "Past tense: 〜ました / 〜ませんでした", "back": "Present: 食べます (eat)\nPast positive: 食べました (ate)\nPast negative: 食べませんでした (didn't eat)\n\nPresent: 行きます (go)\nPast positive: 行きました (went)\nPast negative: 行きませんでした (didn't go)"},
    {"front": "Weekend conversation starters", "back": "しゅうまつはどうでしたか。= How was your weekend?\nどこかへ行きましたか。= Did you go somewhere?\nなにをしましたか。= What did you do?\n\nつまらなかったです。= It was boring.\nたのしかったです。= It was fun."},
    {"front": "Movement verbs — past tense", "back": "行きます → 行きました (went)\n来ます → 来ました (came)\n帰ります → 帰りました (returned)\n会います → 会いました (met)\n\nToday: 行きます\nYesterday: 行きました\nLast week: 先週行きました"},
    {"front": "週末の活動 (Weekend activities)", "back": "映画を見ました = watched a movie\n友達に会いました = met a friend\n家で休みました = rested at home\nどこもいきませんでした = didn't go anywhere\nゆっくりしました = relaxed / took it easy"},
]

ch11_grammar_q = [
    {"question": "しゅうまつにどこか ___ か。(Did you go somewhere on the weekend?)", "answer": "へ行きました", "options": ["へ行きました", "へ行きます", "に行きました", "で行きました"], "explanation": "へ marks direction of movement. どこかへ行きましたか = Did you go somewhere? Past = 〜ました."},
    {"question": "いいえ、どこ ___ いきませんでした。(No, I didn't go anywhere.)", "answer": "も", "options": ["も", "か", "が", "を"], "explanation": "どこも (with negative) = nowhere. どこもいきませんでした = I didn't go anywhere."},
    {"question": "なにか ___ ましたか。(Did you eat something?)", "answer": "たべ", "options": ["たべ", "のみ", "かい", "み"], "explanation": "なにかたべましたか = Did you eat something? なにか in questions = something/anything."},
    {"question": "A: だれかに会いましたか。B: いいえ、___ に会いませんでした。", "answer": "だれも", "options": ["だれも", "だれか", "なにも", "どこも"], "explanation": "だれも (with negative) = no one. だれにも会いませんでした = I didn't meet anyone."},
    {"question": "先週のしゅうまつはどうでしたか → とても ___ 。(It was very fun.)", "answer": "たのしかったです", "options": ["たのしかったです", "たのしいです", "たのしくないです", "たのしかった"], "explanation": "い-adjective past: たのしい → たのしかった + です. Polite past = たのしかったです."},
    {"question": "映画を ___ ましたか。(Did you watch a movie?)", "answer": "み", "options": ["み", "たべ", "のみ", "かい"], "explanation": "見ます (みます) → 見ました (みました). み + ましたか = did you watch?"},
    {"question": "家で ___ 。(I rested at home.)", "answer": "やすみました", "options": ["やすみました", "はたらきました", "べんきょうしました", "たべました"], "explanation": "休みます (やすみます) → 休みました (やすみました). Past of 'rest' = やすみました."},
    {"question": "友達と ___ 映画を見ました。(I watched a movie with a friend.)", "answer": "いっしょに", "options": ["いっしょに", "ひとりで", "ふたりで", "みんなで"], "explanation": "一緒に (いっしょに) = together (with someone). いっしょに + action = doing it together."},
    {"question": "なにもしませんでした。What does this mean?", "answer": "I didn't do anything.", "options": ["I didn't do anything.", "I did something.", "I did nothing special.", "I did everything."], "explanation": "なにも (with negative) = nothing. なにもしませんでした = didn't do anything."},
    {"question": "How do you say 'I bought a souvenir in Kyoto'?", "answer": "京都でおみやげをかいました。", "options": ["京都でおみやげをかいました。", "京都におみやげをかいました。", "京都からおみやげをかいました。", "京都がおみやげをかいました。"], "explanation": "で marks location of action. 京都で = in Kyoto. を marks object. かいました = bought (past)."},
]

ch11_examples_q = [
    {"question": "A: しゅうまつはどこかへ行きましたか。B: ___ 。(No, I stayed home.)", "answer": "いいえ、どこもいきませんでした。うちにいました。", "options": ["いいえ、どこもいきませんでした。うちにいました。", "はい、どこもいきました。", "いいえ、どこかいきませんでした。", "はい、どこかいませんでした。"], "explanation": "Negative answer uses どこも (nowhere) + ませんでした. うちにいました = was at home (いました = was there, for living things)."},
    {"question": "You ate sushi last night. How do you say this?", "answer": "昨日の夜、すしをたべました。", "options": ["昨日の夜、すしをたべました。", "昨日の夜、すしをたべます。", "昨日の夜、すしをたべませんでした。", "明日の夜、すしをたべました。"], "explanation": "Past positive: 食べます → 食べました. 昨日の夜 = last night."},
    {"question": "Someone asks なにかのみましたか. You had nothing. What do you say?", "answer": "いいえ、なにものみませんでした。", "options": ["いいえ、なにものみませんでした。", "いいえ、なにかのみませんでした。", "はい、なにものみました。", "いいえ、どこものみませんでした。"], "explanation": "なにも (nothing) + negative verb. なにものみませんでした = didn't drink anything."},
    {"question": "You met a colleague yesterday. How do you say this?", "answer": "昨日、どうりょうに会いました。", "options": ["昨日、どうりょうに会いました。", "昨日、どうりょうと会いました。", "昨日、どうりょうで会いました。", "昨日、どうりょうを会いました。"], "explanation": "会います (to meet) takes に: 〜に会います = meet someone. Past: 会いました."},
    {"question": "How do you ask about someone's weekend?", "answer": "しゅうまつはどうでしたか。", "options": ["しゅうまつはどうでしたか。", "しゅうまつはなにをしましたか。", "しゅうまつはどこへいきましたか。", "All of the above are natural"], "explanation": "All three are natural ways to ask. どうでしたか = how was it? なにをしましたか = what did you do? どこへいきましたか = where did you go?"},
]

write(make_vocab_lesson(11, "どこかへ行きましたか", "Did You Go Anywhere?", "🗓️", ch11_teach_vocab, ch11_vocab))
write(make_grammar_lesson(11, "どこかへ行きましたか", "Did You Go Anywhere?", "🗓️", ch11_teach_vocab, ch11_grammar_q))
write(make_examples_lesson(11, "どこかへ行きましたか", "Did You Go Anywhere?", "🗓️", ch11_teach_vocab, ch11_examples_q))

# ══════════════════════════════════════════════════════════════
# CHAPTER 12: もう昼ごはんを食べましたか — Already/Not Yet
# ══════════════════════════════════════════════════════════════
ch12_vocab = [
    ("もう", "already / soon", ["not yet", "just", "never"]),
    ("まだ", "not yet / still", ["already", "soon", "just"]),
    ("〜ていません", "have not done ~ yet (negative progressive)", ["have already done", "was doing", "will do"]),
    ("〜てあります", "has been done (resultant state)", ["is being done", "will be done", "hasn't been done"]),
    ("〜ておきます", "to do in advance / for later", ["to undo", "to forget", "to delay"]),
    ("じゅんびします (準備します)", "to prepare", ["to finish", "to cancel", "to rest"]),
    ("かきます (書きます)", "to write", ["to read", "to speak", "to listen"]),
    ("よみます (読みます)", "to read", ["to write", "to listen", "to speak"]),
    ("はなします (話します)", "to speak / talk", ["to listen", "to write", "to read"]),
    ("わかります (分かります)", "to understand / know", ["to not know", "to forget", "to remember"]),
    ("おぼえます (覚えます)", "to memorise / remember", ["to forget", "to understand", "to study"]),
    ("わすれます (忘れます)", "to forget", ["to remember", "to understand", "to know"]),
    ("ちゅうしょく (昼食) / ひるごはん", "lunch", ["breakfast", "dinner", "snack"]),
    ("ちょうしょく / あさごはん (朝ごはん)", "breakfast", ["lunch", "dinner", "snack"]),
    ("ゆうしょく / ばんごはん (晩ごはん)", "dinner / evening meal", ["breakfast", "lunch", "snack"]),
    ("レポート", "report / essay", ["test", "homework", "textbook"]),
    ("しゅくだい (宿題)", "homework", ["test", "textbook", "report"]),
    ("テスト", "test / exam", ["homework", "essay", "textbook"]),
    ("けっか (結果)", "result / outcome", ["process", "beginning", "plan"]),
    ("しめきり (締め切り)", "deadline", ["result", "beginning", "extension"]),
]

ch12_teach = [
    {"front": "もう vs まだ", "back": "もう + positive verb = already done\nもうたべました。= I already ate.\n\nまだ + 〜ていません = not yet\nまだたべていません。= I haven't eaten yet.\n\nKey: もう with positive past; まだ with 〜ていません!"},
    {"front": "〜ていません (not yet / haven't done)", "back": "て-form + いません = have not done\n(negative of て-form + います)\n\nまだたべていません。= Haven't eaten yet.\nまだかいていません。= Haven't written yet.\nまだよんでいません。= Haven't read yet.\n\nFor ongoing 'not yet' situations."},
    {"front": "Q&A: もう〜ましたか", "back": "Q: もう〜ましたか。= Have you already ~?\n\nA (yes): はい、もう〜ました。= Yes, already.\nA (not yet): いいえ、まだです。= No, not yet.\n   or: いいえ、まだ〜ていません。= No, haven't yet."},
    {"front": "〜てあります (done in preparation)", "back": "て-form + あります = has been done (in preparation)\n\nきっぷを買ってあります。\n= The ticket has been bought (in readiness).\n\nNote: てあります focuses on the resulting state,\noften implying someone did it intentionally."},
    {"front": "〜ておきます (do in advance)", "back": "て-form + おきます = do in advance / for a purpose\n\nパーティーの前にりょうりをしておきます。\n= I'll cook in advance of the party.\n\nImplication: doing now to be ready later."},
    {"front": "Common 'have you done' questions", "back": "もうしゅくだいをしましたか。= Have you done homework?\nもうレポートをかきましたか。= Have you written the report?\nもうばんごはんをたべましたか。= Have you eaten dinner?\n\nUse もう to ask if someone has ALREADY done something."},
]

ch12_grammar_q = [
    {"question": "もう昼ごはんを食べ ___ か。(Have you already eaten lunch?)", "answer": "ました", "options": ["ました", "ます", "ていません", "ていた"], "explanation": "もう + ました = already done. もう食べましたか = Have you already eaten?"},
    {"question": "いいえ、___ たべていません。(No, I haven't eaten yet.)", "answer": "まだ", "options": ["まだ", "もう", "ぜんぜん", "あまり"], "explanation": "まだ + negative (〜ていません) = not yet. まだたべていません = haven't eaten yet."},
    {"question": "しゅくだいをしましたか → はい、___ しました。(Yes, already done.)", "answer": "もう", "options": ["もう", "まだ", "まだ〜ていません", "ぜんぜん"], "explanation": "はい、もう〜ました = Yes, I've already done it. もう with positive past tense."},
    {"question": "A: もうレポートをかきましたか。B: いいえ、___。(No, not yet.)", "answer": "まだです", "options": ["まだです", "もうです", "もうしました", "ぜんぜんです"], "explanation": "Short answer for 'not yet': いいえ、まだです. (まだ = not yet, as a standalone response)"},
    {"question": "切符を買っ ___ 。(The ticket has been bought [in preparation].)", "answer": "てあります", "options": ["てあります", "ています", "ておきます", "てください"], "explanation": "〜てあります = has been done (resultant state, intentional). 買ってあります = it's been bought."},
    {"question": "パーティーの前に、りょうりをし ___ 。(I'll cook in advance for the party.)", "answer": "ておきます", "options": ["ておきます", "てあります", "ています", "てください"], "explanation": "〜ておきます = do in advance for a future purpose. しておきます = will do (it) in preparation."},
    {"question": "I haven't read the textbook yet. Which is correct?", "answer": "まだきょうかしょをよんでいません。", "options": ["まだきょうかしょをよんでいません。", "もうきょうかしょをよんでいません。", "まだきょうかしょをよみませんでした。", "もうきょうかしょをよんでいません。"], "explanation": "まだ + 〜ていません = haven't done yet. よむ → よんで (て-form) + いません."},
    {"question": "A: もうかきましたか。B: いいえ、まだかいて ___。(No, I haven't written yet.)", "answer": "いません", "options": ["いません", "います", "ました", "ありません"], "explanation": "まだ〜ていません = haven't done yet. かいて + いません (negative of ています)."},
    {"question": "What does まだです mean when answering もう〜ましたか?", "answer": "Not yet", "options": ["Not yet", "Already", "Never", "Sometimes"], "explanation": "まだです as a short answer = 'not yet'. Full form: まだ〜ていません."},
]

ch12_examples_q = [
    {"question": "You've already done your homework. How do you reply to もうしゅくだいをしましたか?", "answer": "はい、もうしました。", "options": ["はい、もうしました。", "いいえ、まだです。", "はい、まだしました。", "いいえ、もうしました。"], "explanation": "はい + もう + ました = Yes, I've already done it."},
    {"question": "You haven't made a reservation yet. How do you say this?", "answer": "まだよやくをしていません。", "options": ["まだよやくをしていません。", "もうよやくをしていません。", "まだよやくをしました。", "もうよやくをしました。"], "explanation": "まだ + 〜ていません = not yet done. よやく (予約) = reservation."},
    {"question": "Before a trip, you prepare clothes in advance. Which phrase describes this?", "answer": "ふくをじゅんびしておきます。", "options": ["ふくをじゅんびしておきます。", "ふくをじゅんびしてあります。", "ふくをじゅんびしています。", "ふくをじゅんびしてください。"], "explanation": "〜ておきます = do in advance for future use. じゅんびしておきます = prepare in advance."},
    {"question": "The room has been cleaned (by someone, now it's ready). How do you say this?", "answer": "へやをそうじしてあります。", "options": ["へやをそうじしてあります。", "へやをそうじしています。", "へやをそうじしておきます。", "へやをそうじしてください。"], "explanation": "〜てあります = has been done (resultant state, someone did it intentionally). そうじしてあります = has been cleaned."},
]

write(make_vocab_lesson(12, "もう昼ごはんを食べましたか", "Already / Not Yet", "⌚", ch12_teach, ch12_vocab))
write(make_grammar_lesson(12, "もう昼ごはんを食べましたか", "Already / Not Yet", "⌚", ch12_teach, ch12_grammar_q))
write(make_examples_lesson(12, "もう昼ごはんを食べましたか", "Already / Not Yet", "⌚", ch12_teach, ch12_examples_q))

# ══════════════════════════════════════════════════════════════
# CHAPTERS 13-25: Condensed but complete
# ══════════════════════════════════════════════════════════════

CHAPTERS_13_25 = [
    {   "num": 13, "jp": "先週映画を見ました", "en": "Last Week I Watched a Movie", "icon": "🎬",
        "vocab": [
            ("せんしゅう (先週)", "last week", ["this week", "next week", "yesterday"]),
            ("せんげつ (先月)", "last month", ["this month", "next month", "last year"]),
            ("きょねん (去年)", "last year", ["this year", "next year", "last month"]),
            ("〜まえに (〜前に)", "before ~ / ~ ago", ["after ~", "during ~", "since ~"]),
            ("〜あとで (〜後で)", "after doing ~", ["before ~", "during ~", "while ~"]),
            ("えいが (映画)", "movie / film", ["drama", "anime", "documentary"]),
            ("えんそう (演奏)", "musical performance", ["movie", "lecture", "drama"]),
            ("しゃしん (写真)", "photo / photograph", ["picture (drawing)", "poster", "movie"]),
            ("たびをします (旅をします)", "to travel", ["to stay", "to return", "to rest"]),
            ("かんこうします (観光します)", "to sightsee", ["to travel", "to stay", "to shop"]),
            ("おみやげ", "souvenir", ["gift", "letter", "money"]),
            ("かぶき (歌舞伎)", "Kabuki (traditional Japanese theatre)", ["Noh", "opera", "ballet"]),
            ("びじゅつかん (美術館)", "art museum", ["library", "science museum", "movie theater"]),
            ("こうえん (公園)", "park", ["garden", "museum", "square"]),
            ("はくぶつかん (博物館)", "museum (general)", ["art museum", "library", "zoo"]),
        ],
        "grammar_teach": [
            {"front": "Time reference: 〜まえに vs 〜あとで", "back": "〜まえに = before ~ (noun/verb dictionary form)\nたべるまえに = before eating\nじゅぎょうのまえに = before class\n\n〜あとで = after ~ (verb た-form/noun)\nたべたあとで = after eating\nじゅぎょうのあとで = after class"},
            {"front": "Past tense review", "back": "Group 1 (u-verbs): 〜った / 〜んだ / 〜いた\n飲む → 飲んだ\n書く → 書いた\n\nGroup 2 (ru-verbs): 〜た\n食べる → 食べた\n\nPolite past: + です → ました\nたべる → たべました"},
            {"front": "Past time expressions", "back": "昨日 (きのう) = yesterday\n先週 (せんしゅう) = last week\n先月 (せんげつ) = last month\n去年 (きょねん) = last year\n〜日前 (〜にちまえ) = ~ days ago\n〜週間前 (〜しゅうかんまえ) = ~ weeks ago"},
        ],
        "grammar_q": [
            {"question": "たべる ___ 、歯を磨いてください。(Before eating, brush your teeth.)", "answer": "まえに", "options": ["まえに", "あとで", "ながら", "てから"], "explanation": "〜まえに = before. Verb dictionary form + まえに: たべるまえに = before eating."},
            {"question": "じゅぎょうの ___ 、コーヒーを飲みます。(After class, I drink coffee.)", "answer": "あとで", "options": ["あとで", "まえに", "ながら", "から"], "explanation": "〜あとで = after. Noun + のあとで: じゅぎょうのあとで = after class."},
            {"question": "先週、どこかへ行き ___ か。(Did you go somewhere last week?)", "answer": "ました", "options": ["ました", "ます", "ました", "ていません"], "explanation": "Past question: 〜ましたか. 先週 (last week) indicates past time."},
            {"question": "先月、おみやげを ___ 。(Last month, I bought souvenirs.)", "answer": "かいました", "options": ["かいました", "かいます", "かっています", "かっていました"], "explanation": "先月 (last month) + かいました (bought, past) = last month I bought."},
            {"question": "How do you say '3 days ago'?", "answer": "みっかまえ", "options": ["みっかまえ", "さんにちまえ", "みっかあとで", "さんにちあとで"], "explanation": "〜日前 = ~ days ago. 3日前 = みっかまえ (using the special reading for 3 days: みっか)."},
        ],
        "examples_teach": [
            {"front": "Talking about a past trip", "back": "A: 先週はどこかへ行きましたか。\nB: はい、京都へ行きました。\nA: どうでしたか。\nB: とても楽しかったです！お寺がきれいでした。\n\nA: Did you go anywhere last week?\nB: Yes, I went to Kyoto.\nA: How was it?\nB: It was very fun! The temples were beautiful."},
            {"front": "Before and after activities", "back": "ねるまえに、はをみがきます。\n= Before sleeping, I brush my teeth.\n\nたべたあとで、さんぽします。\n= After eating, I take a walk.\n\nしごとのまえに、コーヒーをのみます。\n= Before work, I drink coffee."},
            {"front": "Souvenir shopping", "back": "A: どこでおみやげをかいましたか。\nB: 浅草でかいました。\nA: なにをかいましたか。\nB: ようかんとせんべいをかいました。\n\nようかん = sweet bean jelly\nせんべい = rice crackers"},
        ],
        "examples_q": [
            {"question": "A: 先月どこへ行きましたか。B: ___ へ行きました。(To Osaka.)", "answer": "大阪", "options": ["大阪", "東京", "京都", "北海道"], "explanation": "大阪 (おおさか) = Osaka. 先月大阪へ行きました = I went to Osaka last month."},
            {"question": "Before sleeping, I read a book. Which is correct?", "answer": "ねるまえに、本をよみます。", "options": ["ねるまえに、本をよみます。", "ねたあとで、本をよみます。", "ねながら、本をよみます。", "ねてから、本をよみます。"], "explanation": "〜まえに = before. ねる (dictionary form) + まえに = before sleeping."},
            {"question": "I went sightseeing in Kyoto last year. How do you say this?", "answer": "きょねん、京都でかんこうしました。", "options": ["きょねん、京都でかんこうしました。", "らいねん、京都でかんこうします。", "きょねん、京都にかんこうしました。", "せんしゅう、京都でかんこうしました。"], "explanation": "去年 (きょねん) = last year. で = location of action. かんこうしました = went sightseeing (past)."},
        ],
    },
    {   "num": 14, "jp": "今何をしていますか", "en": "What Are You Doing Now?", "icon": "📞",
        "vocab": [
            ("〜ています", "is doing ~ (progressive/ongoing)", ["did ~", "will do ~", "has done ~"]),
            ("いまなにを (今何を)", "what are you doing now?", ["what did you do?", "what will you do?", "what did you want to do?"]),
            ("でんわ (電話)", "telephone / phone call", ["email", "letter", "fax"]),
            ("でんわします", "to make a phone call", ["to email", "to write", "to fax"]),
            ("もしもし", "hello? (phone greeting)", ["goodbye", "excuse me", "sorry"]),
            ("しばらく", "for a while / it's been a while", ["immediately", "forever", "sometimes"]),
            ("ちょっとまってください", "please wait a moment", ["please come in", "please sit down", "please start"]),
            ("かけます (掛けます)", "to make a call / hang (something)", ["to receive", "to put down", "to write"]),
            ("うけます / でます (出ます)", "to answer (the phone) / to come out", ["to call", "to hang up", "to hold"]),
            ("おかけします", "I'll put you through / I'll connect you", ["please hold", "goodbye", "I'll call back"]),
            ("りょうりします (料理します)", "to cook", ["to eat", "to clean", "to shop"]),
            ("そうじします (掃除します)", "to clean (a room)", ["to cook", "to wash", "to decorate"]),
            ("せんたくします (洗濯します)", "to do laundry / wash clothes", ["to clean", "to iron", "to fold"]),
            ("うたいます (歌います)", "to sing", ["to dance", "to play (instrument)", "to listen"]),
            ("おどります (踊ります)", "to dance", ["to sing", "to play", "to watch"]),
        ],
        "grammar_teach": [
            {"front": "〜ています — Progressive", "back": "て-form + います = is doing (right now)\n\n今なにをしていますか。= What are you doing now?\n→ テレビをみています。= I'm watching TV.\n→ ごはんをたべています。= I'm eating.\n\nUse for ongoing actions happening right now."},
            {"front": "〜ています — Habitual state", "back": "〜ています also expresses habits or ongoing situations:\n\n東京にすんでいます。= I live in Tokyo.\n(ongoing state of living)\n\nかいしゃにつとめています。= I work at a company.\n(ongoing job situation)\n\nThis is different from present progressive!"},
            {"front": "Phone conversation phrases", "back": "もしもし = hello? (phone)\nAのBでございます。= This is B from A. (formal)\nAさんはいらっしゃいますか。= Is Mr./Ms. A there?\nしょうしょうおまちください。= Please hold a moment. (formal)\nまたあとでおかけします。= I'll call back later."},
        ],
        "grammar_q": [
            {"question": "今なにをし ___ か。(What are you doing now?)", "answer": "ていますか", "options": ["ていますか", "ましたか", "ますか", "てありますか"], "explanation": "〜ています = progressive (ongoing action). 今 = now. していますか = are you doing?"},
            {"question": "テレビをみ ___ 。(I'm watching TV.)", "answer": "ています", "options": ["ています", "ました", "ます", "てありました"], "explanation": "〜ています = is doing (right now). みています = am watching."},
            {"question": "東京にすん ___ 。(I live in Tokyo.)", "answer": "でいます", "options": ["でいます", "でいました", "でいません", "でおきます"], "explanation": "すんでいます = am living (ongoing state). 住む (すむ) → 住んで + います."},
            {"question": "でんわで ___ 。(I'm talking on the phone.)", "answer": "はなしています", "options": ["はなしています", "きいています", "かいています", "よんでいます"], "explanation": "でんわで = on the phone (by means of phone). はなしています = am talking/speaking."},
            {"question": "Phone answer: もしもし、___ です。(Hello, this is Tanaka.)", "answer": "田中", "options": ["田中", "はじめまして", "よろしく", "おはよう"], "explanation": "もしもし、[name]です = Hello, this is [name]. Standard phone greeting."},
            {"question": "〜に住んでいます means:", "answer": "I live in ~ (ongoing state)", "options": ["I live in ~ (ongoing state)", "I went to ~", "I visited ~", "I am going to ~"], "explanation": "住む (すむ) + でいます = ongoing state of living. 〜に住んでいます = live in ~."},
        ],
        "examples_q": [
            {"question": "You call a friend and they answer. What is the first thing said?", "answer": "もしもし", "options": ["もしもし", "はじめまして", "おはようございます", "よろしくおねがいします"], "explanation": "もしもし = hello? (used only on the phone, not in person)."},
            {"question": "Your friend is eating when you call. How do they describe what they're doing?", "answer": "ごはんをたべています。", "options": ["ごはんをたべています。", "ごはんをたべました。", "ごはんをたべます。", "ごはんをたべていました。"], "explanation": "〜ています = ongoing action. たべています = am eating (right now)."},
            {"question": "You want to ask 'Do you live in Tokyo?' How do you ask?", "answer": "東京にすんでいますか。", "options": ["東京にすんでいますか。", "東京にすみますか。", "東京でたんでいますか。", "東京をすんでいますか。"], "explanation": "に marks location for living: 〜に住んでいます. すんでいますか = do you live?"},
        ],
    },
    {   "num": 15, "jp": "少し疲れました", "en": "I'm a Little Tired", "icon": "😴",
        "vocab": [
            ("つかれました (疲れました)", "I'm tired / got tired", ["I'm energetic", "I'm fine", "I'm busy"]),
            ("〜てしまいました", "ended up doing ~ / unfortunately did ~", ["will do ~", "am doing ~", "haven't done ~"]),
            ("〜てしまいます", "end up doing ~ (habitual unfortunate)", ["will do ~", "am doing ~", "haven't done ~"]),
            ("〜なければなりません", "must ~ / have to ~", ["don't have to ~", "want to ~", "can ~"]),
            ("〜なくてもいいです", "don't have to ~ / it's OK not to ~", ["must ~", "have to ~", "can't ~"]),
            ("かぜをひきます", "to catch a cold", ["to recover", "to feel well", "to go to hospital"]),
            ("ねつがあります", "to have a fever", ["to have no fever", "to feel cold", "to feel hot"]),
            ("あたまがいたいです", "to have a headache", ["to have a stomachache", "to feel fine", "to be tired"]),
            ("はがいたいです", "to have a toothache", ["to have a headache", "to feel fine", "to have a cold"]),
            ("いたい (痛い)", "painful / it hurts", ["feels good", "comfortable", "fine"]),
            ("びょうきです (病気です)", "to be sick / ill", ["to be well", "to be fine", "to be busy"]),
            ("くすり (薬)", "medicine", ["injection", "hospital", "doctor"]),
            ("のみます (薬を飲みます)", "to take medicine", ["to give medicine", "to get an injection", "to rest"]),
            ("やすみます (休みます)", "to rest / take time off", ["to work", "to study", "to play"]),
            ("〜てもいいです", "it's okay to ~ / you may ~", ["must not ~", "must ~", "can't ~"]),
        ],
        "grammar_teach": [
            {"front": "〜てしまいました — Regret or completion", "back": "〜てしまいました = unfortunately did / ended up doing\n\nかぎをわすれてしまいました。\n= I unfortunately forgot my key.\n\nお金をぜんぶつかってしまいました。\n= I ended up spending all my money.\n\nExpresses regret or that something is completely done (sometimes unwanted)."},
            {"front": "〜なければなりません — Must / Have to", "back": "〜なければなりません = must do (obligation)\n\nVerb negative stem + なければなりません\n行く → 行かなければなりません\n= must go\n\nShort form (spoken): 〜なきゃ\n行かなきゃ = I gotta go"},
            {"front": "〜なくてもいいです — Don't have to", "back": "〜なくてもいいです = don't have to do\n\nVerb neg て-form + もいいです\n行かなくてもいいです = don't have to go\n\nCompare:\n〜なければなりません = MUST do\n〜なくてもいいです = DON'T have to"},
        ],
        "grammar_q": [
            {"question": "まいにちくすりを飲ま ___ ならない。(I must take medicine every day.)", "answer": "なければ", "options": ["なければ", "なくて", "ないで", "なくても"], "explanation": "〜なければなりません = must do. Verb neg. stem: 飲む → 飲まない → 飲まなければなりません."},
            {"question": "あしたはこなく ___ いいです。(You don't have to come tomorrow.)", "answer": "ても", "options": ["ても", "ては", "てから", "てきて"], "explanation": "〜なくてもいいです = don't have to. こない → こなくても + いいです."},
            {"question": "かぎをわすれて ___ 。(I unfortunately forgot my key.)", "answer": "しまいました", "options": ["しまいました", "ください", "もいいです", "おきました"], "explanation": "〜てしまいました = unfortunately did / ended up doing (with regret)."},
            {"question": "かぜをひい ___ 。(I caught a cold.)", "answer": "てしまいました", "options": ["てしまいました", "てください", "てもいいです", "ておきます"], "explanation": "かぜをひく → ひいてしまいました. てしまいました expresses the unwanted result (catching a cold)."},
            {"question": "Which means 'You don't have to eat'?", "answer": "たべなくてもいいです", "options": ["たべなくてもいいです", "たべなければなりません", "たべてはいけません", "たべてください"], "explanation": "〜なくてもいいです = don't have to do. たべなくても = even without eating."},
        ],
        "examples_q": [
            {"question": "You forgot your umbrella. How do you express this with regret?", "answer": "かさをわすれてしまいました。", "options": ["かさをわすれてしまいました。", "かさをわすれました。", "かさをわすれてください。", "かさをわすれなければなりません。"], "explanation": "〜てしまいました expresses the regret of forgetting. Plain ました is just stating a fact."},
            {"question": "You have a headache. How do you say 'I have a headache'?", "answer": "あたまがいたいです。", "options": ["あたまがいたいです。", "はがいたいです。", "ねつがあります。", "つかれました。"], "explanation": "あたまがいたいです = my head hurts (headache). いたい = painful/hurts."},
            {"question": "Doctor says you don't have to rest today. How does the doctor say this?", "answer": "きょうはやすまなくてもいいです。", "options": ["きょうはやすまなくてもいいです。", "きょうはやすまなければなりません。", "きょうはやすんでください。", "きょうはやすんではいけません。"], "explanation": "〜なくてもいいです = don't have to. やすむ → やすまない → やすまなくてもいいです."},
        ],
    },
    {   "num": 16, "jp": "荷物を送りたいんですが", "en": "I'd Like to Send Some Luggage", "icon": "📦",
        "vocab": [
            ("〜たい", "want to do ~", ["don't want to do ~", "must do ~", "can do ~"]),
            ("〜たいと思っています", "I'm thinking I'd like to ~", ["I decided to ~", "I have to ~", "I don't want to ~"]),
            ("〜んですが", "it's that ~ / (giving background context)", ["because ~", "if ~", "although ~"]),
            ("おくります (送ります)", "to send", ["to receive", "to return", "to carry"]),
            ("にもつ (荷物)", "luggage / baggage / package", ["letter", "parcel only", "envelope"]),
            ("こづつみ (小包)", "parcel / package", ["letter", "luggage", "envelope"]),
            ("てがみ (手紙)", "letter", ["parcel", "email", "postcard"]),
            ("はがき (葉書)", "postcard", ["letter", "parcel", "envelope"]),
            ("きって (切手)", "postage stamp", ["envelope", "postcard", "letter"]),
            ("ふうとう (封筒)", "envelope", ["stamp", "postcard", "letter"]),
            ("ゆうびんきょく (郵便局)", "post office", ["bank", "hospital", "library"]),
            ("とどきます (届きます)", "to arrive / be delivered", ["to send", "to leave", "to return"]),
            ("〜ほど", "approximately ~ / about ~", ["exactly ~", "more than ~", "less than ~"]),
            ("いじょう (以上)", "more than ~ / that's all", ["less than ~", "exactly ~", "not enough"]),
            ("かかります", "to take (time/money) / to cost", ["to save", "to give", "to spend"]),
        ],
        "grammar_teach": [
            {"front": "〜たい — Want to do", "back": "Verb stem + たい = want to do ~\n\n食べたい = want to eat\n行きたい = want to go\n見たい = want to see\n\nPolite: 〜たいです\nNegative: 〜たくないです\nPast: 〜たかったです"},
            {"front": "〜たいと思っています", "back": "〜たい + と思っています = am thinking of ~ing / I'm planning to ~\n\n日本語を勉強したいと思っています。\n= I'm thinking of studying Japanese.\n\nMore tentative than たいです. Often used for future plans."},
            {"front": "〜んですが — Context giving", "back": "〜んですが = It's that ~ (giving background before a request)\n\n荷物を送りたいんですが...\n= I'd like to send luggage... (so could you help?)\n\nImplies that what follows is a request or question.\nVery natural and polite in Japanese!"},
        ],
        "grammar_q": [
            {"question": "にほんへ行き ___ です。(I want to go to Japan.)", "answer": "たい", "options": ["たい", "ます", "ました", "ています"], "explanation": "Verb stem + たい = want to do. 行く → 行き + たい = want to go."},
            {"question": "にほんごをべんきょうし ___ と思っています。(I'm thinking of studying Japanese.)", "answer": "たい", "options": ["たい", "て", "ます", "ました"], "explanation": "〜たいと思っています = am thinking of ~ing. たい + と思っています."},
            {"question": "てがみをおく ___ んですが。(It's that I'd like to send a letter.)", "answer": "りたい", "options": ["りたい", "ります", "りました", "っています"], "explanation": "送る + たい = 送りたい. + んですが adds context/background before a request."},
            {"question": "〜んですが is used to:", "answer": "Give context before making a request", "options": ["Give context before making a request", "Deny something", "Ask a direct question", "Give a reason with から"], "explanation": "〜んですが sets up background information, implying a request follows. Very natural in service situations."},
            {"question": "I don't want to go. Which is correct?", "answer": "行きたくないです", "options": ["行きたくないです", "行きたいじゃないです", "行きたないです", "行きくないです"], "explanation": "Negative of たい: たい → たくない + です. 行きたくないです = don't want to go."},
        ],
        "examples_q": [
            {"question": "At the post office, you want to send a parcel. How do you start?", "answer": "こづつみをおくりたいんですが。", "options": ["こづつみをおくりたいんですが。", "こづつみをおくってください。", "こづつみをおくりますか。", "こづつみをおくりたいから。"], "explanation": "〜たいんですが = I'd like to ~ (polite request opener). Natural at the post office counter."},
            {"question": "You want to buy 5 stamps. What do you say?", "answer": "きってを5枚ください。", "options": ["きってを5枚ください。", "きってを5本ください。", "きってを5個ください。", "きってを5冊ください。"], "explanation": "Stamps are flat → use 枚 (まい). きって (切手) = stamp. 5枚 = ごまい."},
            {"question": "How long does this package take to arrive?", "answer": "このこづつみはどのくらいでとどきますか。", "options": ["このこづつみはどのくらいでとどきますか。", "このこづつみはどのくらいかかりますか。", "このこづつみはいつにとどきますか。", "All of these are natural"], "explanation": "All three are natural! どのくらいでとどきますか = how long until it arrives? とどきます = to be delivered."},
        ],
    },
    {   "num": 17, "jp": "ちょっと待ってください", "en": "Please Wait a Moment", "icon": "✋",
        "vocab": [
            ("〜ていただけませんか", "could you please ~ (very polite)", ["please do ~", "may I ~", "let's ~"]),
            ("〜てくれませんか", "won't you ~ for me? (less formal)", ["please don't ~", "may I ~", "let's ~"]),
            ("もうすこし", "a little more", ["a lot more", "a little less", "enough"]),
            ("もう一度 (もういちど)", "one more time / again", ["for the first time", "sometimes", "always"]),
            ("ゆっくり", "slowly", ["quickly", "quietly", "loudly"]),
            ("はっきり", "clearly / distinctly", ["vaguely", "quietly", "slowly"]),
            ("おおきいこえで", "in a loud voice", ["quietly", "softly", "slowly"]),
            ("ちいさいこえで", "in a quiet voice", ["loudly", "clearly", "quickly"]),
            ("にほんごで", "in Japanese", ["in English", "in Chinese", "in Korean"]),
            ("えいごで", "in English", ["in Japanese", "in Chinese", "in French"]),
            ("かんじ (漢字)", "kanji (Chinese characters)", ["hiragana", "katakana", "romaji"]),
            ("ひらがな", "hiragana (Japanese script)", ["katakana", "kanji", "romaji"]),
            ("かたかな", "katakana (Japanese script)", ["hiragana", "kanji", "romaji"]),
            ("けいご (敬語)", "polite/formal Japanese", ["casual Japanese", "written Japanese", "dialect"]),
            ("くだけたことば", "casual/informal speech", ["polite speech", "formal speech", "written language"]),
        ],
        "grammar_teach": [
            {"front": "Polite requests: 〜ていただけませんか", "back": "Very polite request: could you please ~?\n\nもう一度言っていただけませんか。\n= Could you please say it one more time?\n\nゆっくり話していただけませんか。\n= Could you please speak slowly?\n\nMore formal than 〜てください"},
            {"front": "〜てくれませんか (friendly request)", "back": "Friendly/casual request: won't you ~ for me?\n\nちょっと待ってくれませんか。\n= Won't you wait a moment?\n\nLess formal than 〜ていただけませんか\nMore personal/direct"},
            {"front": "Communication adverbs", "back": "ゆっくり = slowly\nはっきり = clearly\nもう一度 = one more time\nもう少し = a little more\n大きい声で = in a loud voice\n小さい声で = in a quiet voice\n日本語で = in Japanese"},
        ],
        "grammar_q": [
            {"question": "もう一度言っていただけ ___ か。(Could you please say it one more time?)", "answer": "ません", "options": ["ません", "ます", "ましょう", "てください"], "explanation": "〜ていただけませんか = Could you please ~? Very polite request form."},
            {"question": "ゆっくり話してくれ ___ か。(Won't you please speak slowly?)", "answer": "ません", "options": ["ません", "ます", "ましょう", "ていただけ"], "explanation": "〜てくれませんか = won't you ~ (for me)? Less formal than いただけませんか."},
            {"question": "Which is more polite?", "answer": "〜ていただけませんか", "options": ["〜ていただけませんか", "〜てくれませんか", "〜てください", "〜て (plain form)"], "explanation": "Politeness scale: 〜ていただけませんか > 〜てくれませんか > 〜てください > plain て-form."},
            {"question": "はっきり話してください means:", "answer": "Please speak clearly.", "options": ["Please speak clearly.", "Please speak slowly.", "Please speak quietly.", "Please speak in Japanese."], "explanation": "はっきり = clearly/distinctly. はっきり話す = speak clearly."},
            {"question": "How do you ask someone to write in Japanese?", "answer": "日本語でかいていただけませんか。", "options": ["日本語でかいていただけませんか。", "日本語をかいていただけませんか。", "日本語にかいていただけませんか。", "日本語からかいていただけませんか。"], "explanation": "で marks the means/language: 日本語で = in Japanese. かいて + いただけませんか = could you write?"},
        ],
        "examples_q": [
            {"question": "In a meeting, you didn't understand. What do you say?", "answer": "もう一度言っていただけませんか。", "options": ["もう一度言っていただけませんか。", "もう一度いってください。", "もう一度いいですか。", "わかりません。"], "explanation": "〜ていただけませんか is the most polite way to request repetition in formal settings."},
            {"question": "A friend is speaking too fast. What do you ask?", "answer": "もう少しゆっくり話してくれませんか。", "options": ["もう少しゆっくり話してくれませんか。", "もう少しゆっくり話していただけませんか。", "もう少しゆっくり話してください。", "All are possible depending on relationship"], "explanation": "All three work! くれませんか = casual (with friends), いただけませんか = formal, ください = neutral."},
            {"question": "What does はっきり言ってください mean?", "answer": "Please say it clearly.", "options": ["Please say it clearly.", "Please say it slowly.", "Please say it again.", "Please say it quietly."], "explanation": "はっきり = clearly/distinctly. はっきり言う = say clearly. はっきり言ってください = please say it clearly."},
        ],
    },
    {   "num": 18, "jp": "来週パーティーをするんですが", "en": "I'm Having a Party Next Week", "icon": "🎉",
        "vocab": [
            ("パーティー", "party", ["meeting", "gathering", "dinner"]),
            ("〜んですが", "it's that ~ (context setting)", ["because ~", "although ~", "if ~"]),
            ("〜から", "because ~ (giving reason)", ["although ~", "if ~", "when ~"]),
            ("きます (来ます)", "to come", ["to go", "to return", "to stay"]),
            ("つれてきます (連れてきます)", "to bring (a person)", ["to take away", "to send", "to leave behind"]),
            ("もってきます (持ってきます)", "to bring (a thing)", ["to take away", "to send", "to leave behind"]),
            ("もっていきます (持っていきます)", "to take (a thing) somewhere", ["to bring here", "to send", "to leave"]),
            ("つれていきます (連れていきます)", "to take (a person) somewhere", ["to bring here", "to send", "to leave"]),
            ("しょうたい (招待)", "invitation", ["refusal", "visit", "gathering"]),
            ("よてい (予定)", "schedule / plan", ["result", "past", "decision"]),
            ("よていがあります", "to have plans", ["to have no plans", "to be free", "to cancel"]),
            ("つごうがいい (都合がいい)", "convenient / good timing", ["inconvenient", "busy", "impossible"]),
            ("つごうがわるい (都合が悪い)", "inconvenient / bad timing", ["convenient", "free", "possible"]),
            ("ぜひ", "by all means / definitely", ["never", "maybe", "perhaps"]),
            ("きかい (機会)", "opportunity / chance", ["result", "plan", "difficulty"]),
        ],
        "grammar_teach": [
            {"front": "〜から — Giving reasons", "back": "〜から = because ~ (reason)\n\n[reason sentence]から、[result]\n\nつかれたから、はやく寝ます。\n= Because I'm tired, I'll sleep early.\n\n〜から can come in the middle or at end:\nはやく寝ます。つかれたから。\n= I'll sleep early. Because I'm tired."},
            {"front": "Bringing things: きます/いきます", "back": "〜てきます = come/go and bring back:\n→ きます: action done and come back here\nかってきます = go buy and come back\n\n〜ていきます = go and do:\n→ いきます: action done while going\nもっていきます = take (to go)\n\nもってきます = bring (here)\nもっていきます = take (there)"},
            {"front": "Inviting and scheduling", "back": "つごうはどうですか。= How's your schedule?\nよていはありますか。= Do you have plans?\nこんどのどようびはどうですか。= How about this Saturday?\n\nぜひきてください。= Please do come.\nぜひ！= By all means!"},
        ],
        "grammar_q": [
            {"question": "あたまがいたい ___ 、かいしゃをやすみます。(Because I have a headache, I'll take the day off.)", "answer": "から", "options": ["から", "ので", "が", "でも"], "explanation": "〜から = because (subjective reason). あたまがいたいから = because my head hurts."},
            {"question": "パーティーに ___ てきてください。(Please bring your friend to the party.)", "answer": "ともだちをつれ", "options": ["ともだちをつれ", "ともだちをもっ", "ともだちとき", "ともだちにき"], "explanation": "つれてきます = to bring (a person). ともだちをつれてくる = to bring a friend."},
            {"question": "What does もっていきます mean?", "answer": "To take (something) to another place", "options": ["To take (something) to another place", "To bring (something) here", "To send (something)", "To buy (something)"], "explanation": "持っていきます = take (thing) away (away from here). Contrast: 持ってきます = bring (here)."},
            {"question": "しゅうまつはつごうがいい ___ 。(The weekend works for me.)", "answer": "です", "options": ["です", "ました", "ます", "ています"], "explanation": "都合がいいです = it's convenient / works for me. A common scheduling expression."},
            {"question": "A: パーティーにきませんか。B: ___！(By all means!)", "answer": "ぜひ", "options": ["ぜひ", "ちょっと", "また今度", "すみません"], "explanation": "ぜひ = by all means / definitely! The most enthusiastic way to accept an invitation."},
        ],
        "examples_q": [
            {"question": "You're planning a party and inviting a friend. How do you start?", "answer": "らいしゅうパーティーをするんですが、きませんか。", "options": ["らいしゅうパーティーをするんですが、きませんか。", "らいしゅうパーティーをします。きてください。", "らいしゅうパーティーがありますから、きませんか。", "らいしゅうパーティーをするから、きてください。"], "explanation": "〜んですが + request = natural way to make invitations. Sets up context before the invitation."},
            {"question": "You're going on a picnic. What do you bring?", "answer": "ピクニックにおべんとうをもっていきます。", "options": ["ピクニックにおべんとうをもっていきます。", "ピクニックにおべんとうをもってきます。", "ピクニックにおべんとうをつれていきます。", "ピクニックにおべんとうをつれてきます。"], "explanation": "もっていきます = take (something) to another place. Bringing food TO the picnic = もっていく."},
            {"question": "Why can't you come to the party? Give a reason using から.", "answer": "よていがあるから、いけません。", "options": ["よていがあるから、いけません。", "よていがあるので、いけません。", "よていがあるが、いけません。", "よていがあるけど、いけません。"], "explanation": "〜から = because. よていがあるから = because I have plans. Natural reason for declining."},
        ],
    },
    {   "num": 19, "jp": "旅行はどうでしたか", "en": "How Was Your Trip?", "icon": "✈️",
        "vocab": [
            ("どうでしたか", "how was it?", ["how is it?", "what is it?", "where is it?"]),
            ("〜かったです", "was ~ (い-adjective past positive)", ["is ~", "was not ~", "will be ~"]),
            ("〜くなかったです", "was not ~ (い-adj past negative)", ["was ~", "is ~", "will be ~"]),
            ("〜でした", "was ~ (noun/な-adj past positive)", ["is ~", "was not ~", "will be ~"]),
            ("〜じゃなかったです", "was not ~ (noun/な-adj past negative)", ["was ~", "is ~", "will be ~"]),
            ("りょこう (旅行)", "trip / travel", ["stay", "commute", "walk"]),
            ("かんそう (感想)", "impression / thoughts", ["schedule", "plan", "result"]),
            ("たのしかった (楽しかった)", "was fun / enjoyable (past)", ["is fun", "will be fun", "not fun"]),
            ("すばらしかった (素晴らしかった)", "was wonderful / magnificent", ["was ordinary", "was bad", "was boring"]),
            ("きれいでした", "was beautiful / clean (past)", ["is beautiful", "was dirty", "will be beautiful"]),
            ("にぎやかでした", "was lively / bustling (past)", ["was quiet", "was beautiful", "was fun"]),
            ("しずかでした (静かでした)", "was quiet / peaceful (past)", ["was noisy", "was lively", "was busy"]),
            ("てんきがよかった (天気がよかった)", "the weather was good", ["the weather was bad", "the weather was hot", "the weather was cold"]),
            ("たべもの (食べ物)", "food", ["drink", "dessert", "snack"]),
            ("おもいで (思い出)", "memory / recollection", ["plan", "schedule", "future"]),
        ],
        "grammar_teach": [
            {"front": "い-adjective past tense", "back": "Positive past: drop い + かった + です\nおいしい → おいしかったです (was delicious)\nたのしい → たのしかったです (was fun)\n\nNegative past: drop い + くなかった + です\nたかい → たかくなかったです (was not expensive)\n\nException: いい → よかったです (was good)"},
            {"front": "な-adjective / noun past tense", "back": "Positive past: Nでした / な-adjadj + でした\nきれいでした (was beautiful)\nしずかでした (was quiet)\n\nNegative past: じゃなかったです / ではなかったです\nきれいじゃなかったです (was not beautiful)\n\nNoun: 学生でした (was a student)"},
            {"front": "Talking about past experiences", "back": "どうでしたか = how was it?\n→ とてもよかったです！= It was very good!\n→ まあまあでした。= It was so-so.\n→ あまりよくなかったです。= Not very good.\n\nかんそうはどうですか = What are your thoughts?"},
        ],
        "grammar_q": [
            {"question": "旅行はどうでし ___ か。(How was the trip?)", "answer": "た", "options": ["た", "ます", "ました", "て"], "explanation": "どうでしたか = how was it? です past = でした. でした + か = でしたか (question)."},
            {"question": "ホテルはきれい ___ 。(The hotel was beautiful.)", "answer": "でした", "options": ["でした", "かったです", "でありました", "じゃなかったです"], "explanation": "きれい is a な-adjective. Past = きれいでした (not きれいかった!)."},
            {"question": "たべものはおいし ___ 。(The food was delicious.)", "answer": "かったです", "options": ["かったです", "でした", "くなかったです", "じゃなかったです"], "explanation": "おいしい is an い-adjective. Past = おいしかったです (drop い + かった + です)."},
            {"question": "てんきはあまりよく ___ 。(The weather was not very good.)", "answer": "なかったです", "options": ["なかったです", "かったです", "じゃなかったです", "ありませんでした"], "explanation": "いい → negative past: よくなかったです (not いくなかった!). いい is irregular."},
            {"question": "にぎやかじゃ ___ です。(It was not lively.)", "answer": "なかった", "options": ["なかった", "くなかった", "ありませんでした", "いません"], "explanation": "な-adjective negative past: 〜じゃなかったです. にぎやか (lively) is な-adjective → じゃなかったです."},
        ],
        "examples_q": [
            {"question": "Your trip to Kyoto was wonderful. How do you express this?", "answer": "京都の旅行はすばらしかったです！", "options": ["京都の旅行はすばらしかったです！", "京都の旅行はすばらしいでした！", "京都の旅行はすばらしくなかったです！", "京都の旅行はすばらしでした！"], "explanation": "すばらしい is an い-adjective. Past = すばらしかったです (drop い + かった + です)."},
            {"question": "The hotel was not quiet. How do you say this?", "answer": "ホテルはしずかじゃなかったです。", "options": ["ホテルはしずかじゃなかったです。", "ホテルはしずかくなかったです。", "ホテルはしずかでした。", "ホテルはしずかじゃないです。"], "explanation": "しずか is a な-adjective. Past negative = じゃなかったです. (not くなかった!)"},
            {"question": "Someone asks どうでしたか about your holiday. You say 'It was very fun!'", "answer": "とてもたのしかったです！", "options": ["とてもたのしかったです！", "とてもたのしいでした！", "とてもたのしくなかったです！", "とてもたのしいです！"], "explanation": "Past of い-adjective: たのしい → たのしかったです. とても = very."},
        ],
    },
    {   "num": 20, "jp": "道を教えてください", "en": "Please Tell Me the Way", "icon": "🗺️",
        "vocab": [
            ("みちをおしえます (道を教えます)", "to give directions", ["to ask for directions", "to get lost", "to walk"]),
            ("まっすぐ", "straight ahead", ["turn right", "turn left", "turn back"]),
            ("みぎ (右)", "right", ["left", "straight", "back"]),
            ("ひだり (左)", "left", ["right", "straight", "back"]),
            ("まがります (曲がります)", "to turn", ["to go straight", "to stop", "to cross"]),
            ("わたります (渡ります)", "to cross", ["to turn", "to stop", "to walk"]),
            ("しんごう (信号)", "traffic light", ["crosswalk", "corner", "bridge"]),
            ("かど (角)", "corner", ["traffic light", "intersection", "bridge"]),
            ("こうさてん (交差点)", "intersection", ["corner", "bridge", "tunnel"]),
            ("はし (橋)", "bridge", ["tunnel", "corner", "intersection"]),
            ("ちかい (近い)", "near / close", ["far", "long", "short"]),
            ("とおい (遠い)", "far / distant", ["near", "short", "long"]),
            ("〜メートル", "~ metres", ["~ kilometres", "~ steps", "~ floors"]),
            ("〜キロ", "~ kilometres", ["~ metres", "~ miles", "~ steps"]),
            ("むこう (向こう)", "over there / the other side", ["this side", "here", "nearby"]),
        ],
        "grammar_teach": [
            {"front": "Giving directions with て-form", "back": "Chain directions with て-form:\nまっすぐ行って、\n= Go straight, then\nかどを右に曲がって、\n= turn right at the corner, then\nはしをわたると、右手にあります。\n= cross the bridge and it's on the right."},
            {"front": "〜と、〜 (when you do X, Y happens)", "back": "[action] + と + [result/discovery]\n\nこのみちをまっすぐ行くと、えきがあります。\n= If you go straight on this road, you'll find the station.\n\nかどを曲がると、すぐ見えます。\n= When you turn the corner, you can see it right away."},
            {"front": "Directional phrases", "back": "Right side: みぎ / 右て (みぎて)\nLeft side: ひだり / 左て (ひだりて)\nStraight: まっすぐ\nOver there: むこう\n\nDistance:\n〜メートル先 = ~ metres ahead\n〜分ぐらい = about ~ minutes (walking)"},
        ],
        "grammar_q": [
            {"question": "まっすぐ行っ ___ 、右に曲がってください。(Go straight, then turn right.)", "answer": "て", "options": ["て", "から", "まで", "に"], "explanation": "て-form chains instructions: 行って = go (and then). て connects sequential directions."},
            {"question": "このみちをまっすぐ行く ___ 、えきがあります。(If you go straight, there's the station.)", "answer": "と", "options": ["と", "から", "ので", "から"], "explanation": "〜と = when/if (natural sequence). 行くと = when you go. Used for directional 'when you do X, Y happens'."},
            {"question": "えきはここから ___ ですか。(Is the station near here?)", "answer": "ちかい", "options": ["ちかい", "とおい", "おおきい", "あたらしい"], "explanation": "ちかい = near/close. とおい = far. 〜からちかいですか = is it close from ~?"},
            {"question": "しんごうを ___ 、ひだりに曲がります。(Cross the traffic light, then turn left.)", "answer": "わたって", "options": ["わたって", "まがって", "とまって", "きって"], "explanation": "わたる → わたって (て-form). を marks the thing being crossed: しんごうをわたる = cross the traffic light."},
            {"question": "Directions: '3rd traffic light, turn right' — what is 3rd?", "answer": "みっつめの", "options": ["みっつめの", "さんばんめの", "さんこめの", "さんにちめの"], "explanation": "〜つめ counts ordinal things: ひとつめ (1st), ふたつめ (2nd), みっつめ (3rd). みっつめのしんごう = the 3rd traffic light."},
        ],
        "examples_q": [
            {"question": "Someone asks you where the station is. Give directions: 'Go straight and turn left at the corner.'", "answer": "まっすぐ行って、かどをひだりに曲がってください。", "options": ["まっすぐ行って、かどをひだりに曲がってください。", "まっすぐ行って、かどをみぎに曲がってください。", "まっすぐ行きます、かどをひだりに曲がります。", "かどをひだりに曲がって、まっすぐ行ってください。"], "explanation": "Te-form chain: 行って + 曲がってください. Left = ひだり. を marks what you turn at."},
            {"question": "How do you ask 'Is it far from here?'", "answer": "ここからとおいですか。", "options": ["ここからとおいですか。", "ここにとおいですか。", "ここでとおいですか。", "ここをとおいですか。"], "explanation": "から marks starting point. ここから = from here. とおいですか = is it far?"},
            {"question": "The bank is 200 metres from the station. How do you describe this?", "answer": "えきから200メートルのところにぎんこうがあります。", "options": ["えきから200メートルのところにぎんこうがあります。", "えきに200メートルのところにぎんこうがあります。", "えきで200メートルのところにぎんこうがあります。", "えきまで200メートルのところにぎんこうがあります。"], "explanation": "から marks distance from a point. 〜のところに = at the place of ~. あります = there is."},
        ],
    },
    {   "num": 21, "jp": "誰でも利用できます", "en": "Anyone Can Use It", "icon": "✅",
        "vocab": [
            ("できます", "can do / is possible", ["cannot do", "must do", "want to do"]),
            ("〜ができます", "can ~ / is able to ~", ["cannot ~", "must ~", "wants to ~"]),
            ("〜られます (Group 2 potential)", "can ~ (ru-verb potential)", ["must ~", "wants to ~", "has to ~"]),
            ("〜える (Group 1 potential)", "can ~ (u-verb potential)", ["must ~", "wants to ~", "has to ~"]),
            ("だれでも", "anyone / everyone", ["no one", "someone", "who?"]),
            ("なんでも", "anything / everything", ["nothing", "something", "what?"]),
            ("どこでも", "anywhere / everywhere", ["nowhere", "somewhere", "where?"]),
            ("いつでも", "anytime / always", ["never", "sometimes", "when?"]),
            ("じゆうに (自由に)", "freely / as you like", ["restrictedly", "carefully", "slowly"]),
            ("りようします (利用します)", "to use / make use of", ["to avoid", "to stop", "to buy"]),
            ("つかいます (使います)", "to use (a thing)", ["to avoid", "to stop", "to repair"]),
            ("プール", "swimming pool", ["gym", "park", "court"]),
            ("えいご (英語)", "English (language)", ["Japanese", "Chinese", "French"]),
            ("にほんご (日本語)", "Japanese (language)", ["English", "Chinese", "French"]),
            ("スポーツ", "sport(s)", ["art", "music", "study"]),
        ],
        "grammar_teach": [
            {"front": "Potential form — Group 2 (ru-verbs)", "back": "Replace る with られる:\n食べる → 食べられる (can eat)\n見る → 見られる (can see)\n起きる → 起きられる (can wake up)\n\nPolite: 食べられます (can eat)\nNegative: 食べられません (cannot eat)"},
            {"front": "Potential form — Group 1 (u-verbs)", "back": "Replace the u-sound with e-sound + る:\n書く (ku) → 書ける (keru) = can write\n読む (mu) → 読める (meru) = can read\n飲む → 飲める (can drink)\n話す → 話せる (can speak)\n\nPolite: 書けます (can write)"},
            {"front": "Irregular potential forms", "back": "する → できる (can do)\n来る → 来られる (korareru, can come)\n\nNote: できる is the most common!\n日本語ができます = can do Japanese = can speak Japanese\nスポーツができます = can do sports"},
        ],
        "grammar_q": [
            {"question": "日本語 ___ 話せます。(I can speak Japanese.)", "answer": "が", "options": ["が", "を", "は", "で"], "explanation": "Potential verbs often take が for the object: 日本語が話せます. (を is also acceptable in modern usage.)"},
            {"question": "食べる → potential form is:", "answer": "食べられます", "options": ["食べられます", "食べれます", "食べます", "食べえます"], "explanation": "Group 2 potential: 食べる → 食べられる → 食べられます. Replace る with られる."},
            {"question": "書く → potential form is:", "answer": "書けます", "options": ["書けます", "書かれます", "書きます", "書られます"], "explanation": "Group 1 potential: k(u) → k(e)ru. 書く → 書ける → 書けます."},
            {"question": "する → potential form is:", "answer": "できます", "options": ["できます", "されます", "しられます", "しえます"], "explanation": "する is irregular. Potential = できる → できます. 日本語ができます = can speak Japanese."},
            {"question": "だれでも ___ できます。(Anyone can use it.)", "answer": "りよう", "options": ["りよう", "しよう", "りよ", "よう"], "explanation": "利用できます = can use / is available for use. だれでも = anyone. だれでも利用できます."},
        ],
        "examples_q": [
            {"question": "How do you say 'I can read kanji'?", "answer": "漢字が読めます。", "options": ["漢字が読めます。", "漢字を読めます。", "漢字が読まれます。", "漢字が読みます。"], "explanation": "読む → 読める (potential, Group 1). 漢字が読めます = can read kanji. が marks the object of potential."},
            {"question": "What does だれでも入れます mean?", "answer": "Anyone can enter.", "options": ["Anyone can enter.", "No one can enter.", "Someone can enter.", "Everyone entered."], "explanation": "だれでも = anyone. 入る (はいる) → 入れる (potential) = can enter. だれでも入れます = anyone can enter."},
            {"question": "You can't swim. How do you say this?", "answer": "泳げません。", "options": ["泳げません。", "泳がれません。", "泳きません。", "泳むません。"], "explanation": "泳ぐ (およぐ) is Group 1: g(u) → g(e)ru. 泳ぐ → 泳げる → 泳げません (cannot swim)."},
        ],
    },
    {   "num": 22, "jp": "日本に来たばかりです", "en": "I Just Came to Japan", "icon": "🌸",
        "vocab": [
            ("〜たばかりです", "just did ~ (very recently)", ["did ~ long ago", "will do ~", "am doing ~"]),
            ("〜たことがあります", "have done ~ before / have experience of", ["have never done ~", "just did ~", "will do ~"]),
            ("〜たことがありません", "have never done ~", ["have done ~", "just did ~", "will do ~"]),
            ("はじめて (初めて)", "for the first time", ["again", "as usual", "recently"]),
            ("けいけん (経験)", "experience", ["skill", "knowledge", "memory"]),
            ("〜回 (〜かい)", "~ times (counter)", ["~ days", "~ months", "~ years"]),
            ("いちど (一度)", "once / one time", ["twice", "many times", "never"]),
            ("なんどか (何度か)", "several times", ["once", "never", "always"]),
            ("ふじさん (富士山)", "Mt. Fuji", ["Mt. Everest", "Mt. Aso", "Mt. Fuji"]),
            ("にほんりょうり (日本料理)", "Japanese cuisine", ["Western food", "Chinese food", "Italian food"]),
            ("さくら (桜)", "cherry blossom", ["autumn leaves", "plum blossom", "iris"]),
            ("はなみ (花見)", "cherry blossom viewing", ["autumn leaf viewing", "fireworks", "festival"]),
            ("わしょく (和食)", "Japanese food", ["Western food", "Chinese food", "Korean food"]),
            ("ようしょく (洋食)", "Western food", ["Japanese food", "Chinese food", "Korean food"]),
            ("かぶき (歌舞伎)", "Kabuki theatre", ["Noh theatre", "Bunraku", "opera"]),
        ],
        "grammar_teach": [
            {"front": "〜たばかりです — Just did", "back": "[verb た-form] + ばかりです = just did (very recently)\n\n日本に来たばかりです。\n= I just came to Japan.\n\nひるごはんを食べたばかりです。\n= I just ate lunch.\n\nImplies very recent action."},
            {"front": "〜たことがあります — Have done before", "back": "[verb た-form] + ことがあります = have done before\n\n富士山に登ったことがあります。\n= I have climbed Mt. Fuji before.\n\nすしを食べたことがありますか。\n= Have you ever eaten sushi?\n\nNegative: 〜たことがありません = have never done"},
            {"front": "Comparing: ばかり vs ことがある", "back": "〜たばかり = JUST did (very recent, specific past)\nさっき食べたばかりです。= I just ate a moment ago.\n\n〜たことがある = have experience of (anytime in the past)\n子どものとき、食べたことがあります。\n= I've eaten it before (as a child)."},
        ],
        "grammar_q": [
            {"question": "日本に来た ___ です。(I just came to Japan.)", "answer": "ばかり", "options": ["ばかり", "ことがあります", "ていません", "てあります"], "explanation": "〜たばかりです = just did. 来た (came, past) + ばかりです = just came."},
            {"question": "富士山に登った ___ があります。(I have climbed Mt. Fuji before.)", "answer": "こと", "options": ["こと", "ばかり", "まで", "から"], "explanation": "〜たことがあります = have done before. 登った (climbed) + ことがあります = have climbed."},
            {"question": "A: すしを食べたことがありますか。B: いいえ、___ 。(No, I've never eaten it.)", "answer": "たことがありません", "options": ["たことがありません", "たばかりです", "ていません", "ませんでした"], "explanation": "〜たことがありません = have never done. Negative experience form."},
            {"question": "はじめて日本に来ました。This means:", "answer": "I came to Japan for the first time.", "options": ["I came to Japan for the first time.", "I just came to Japan.", "I came to Japan again.", "I have been to Japan before."], "explanation": "はじめて = for the first time. はじめて日本に来ました = came to Japan for the first time."},
            {"question": "I've visited Kyoto several times. Which is correct?", "answer": "京都に何度か行ったことがあります。", "options": ["京都に何度か行ったことがあります。", "京都に何度か行ったばかりです。", "京都に何度かいきました。", "京都に何度かいったことがありません。"], "explanation": "〜たことがあります = have done before. 何度か = several times. 行った = went (past)."},
        ],
        "examples_q": [
            {"question": "You just ate lunch. How do you say 'I just ate lunch'?", "answer": "ひるごはんを食べたばかりです。", "options": ["ひるごはんを食べたばかりです。", "ひるごはんを食べたことがあります。", "ひるごはんを食べていません。", "ひるごはんを食べました。"], "explanation": "〜たばかりです = just did (very recently). 食べた = ate (past) + ばかりです."},
            {"question": "Have you ever eaten natto? No, never.", "answer": "なっとうを食べたことがありません。", "options": ["なっとうを食べたことがありません。", "なっとうを食べたばかりです。", "なっとうを食べたことがあります。", "なっとうをまだ食べていません。"], "explanation": "〜たことがありません = have never done. 食べた + ことがありません = have never eaten."},
            {"question": "Someone asks if you've seen Kabuki before. You have, once. How do you reply?", "answer": "はい、一度見たことがあります。", "options": ["はい、一度見たことがあります。", "はい、一度見たばかりです。", "はい、一度見ていません。", "はい、一度見ます。"], "explanation": "〜たことがあります = have done before. 一度 = once. 見た = saw (past) + ことがあります."},
        ],
    },
    {   "num": 23, "jp": "日本語が少し話せます", "en": "I Can Speak a Little Japanese", "icon": "💬",
        "vocab": [
            ("すこし (少し)", "a little / slightly", ["a lot", "very", "not at all"]),
            ("じょうず (上手)", "skilled / good at (な-adj)", ["unskilled", "average", "novice"]),
            ("へた (下手)", "unskilled / bad at (な-adj)", ["skilled", "average", "excellent"]),
            ("とくい (得意)", "one's strong point / good at", ["bad at", "weak point", "average"]),
            ("にがて (苦手)", "one's weak point / bad at", ["strong point", "good at", "average"]),
            ("〜か (embedded question)", "whether ~ / if ~ (indirect question)", ["direct question", "because ~", "although ~"]),
            ("わかりません", "I don't know / I don't understand", ["I understand", "I know", "I see"]),
            ("おしえてください (教えてください)", "please tell me / please teach me", ["please don't tell", "I know", "I understand"]),
            ("しらべます (調べます)", "to investigate / look up", ["to know", "to find out", "to guess"]),
            ("かくにんします (確認します)", "to confirm / check", ["to guess", "to ignore", "to assume"]),
            ("でんたく (電卓)", "calculator", ["computer", "clock", "telephone"]),
            ("インターネット", "internet", ["television", "radio", "telephone"]),
            ("けいたい (携帯)", "mobile phone / cell phone", ["computer", "tablet", "camera"]),
            ("スマートフォン / スマホ", "smartphone", ["flip phone", "tablet", "computer"]),
            ("アプリ", "app / application", ["website", "browser", "software"]),
        ],
        "grammar_teach": [
            {"front": "Potential form review (all groups)", "back": "Group 1: 書く → 書ける / 読む → 読める\nGroup 2: 食べる → 食べられる / 見る → 見られる\nIrregular:\nする → できる\n来る → 来られる\n\nObject: が (or を in casual)\nパソコンが使えます = can use a computer"},
            {"front": "Embedded questions with 〜か", "back": "[question word] + [verb] + か + わかりません\n\nどこに行けばいいかわかりません。\n= I don't know where I should go.\n\nなんじにくるかおしえてください。\n= Please tell me what time you're coming.\n\nか = 'whether/if' in indirect questions"},
            {"front": "Expressing ability level", "back": "少し〜できます = can ~ a little\nすこしにほんごが話せます = can speak Japanese a little\n\nとても上手です = very skilled\nあまり上手じゃないです = not very skilled\nぜんぜんできません = can't do at all"},
        ],
        "grammar_q": [
            {"question": "ピアノが弾け ___ 。(I can play the piano.)", "answer": "ます", "options": ["ます", "られます", "できます", "あります"], "explanation": "弾く (ひく) is Group 1: ひく → ひける → 弾けます. Can play = 弾けます."},
            {"question": "日本語が少し ___ ます。(I can speak a little Japanese.)", "answer": "話せ", "options": ["話せ", "話さ", "話し", "話け"], "explanation": "話す (はなす) potential: s(u) → s(e)ru. 話す → 話せる → 話せます (can speak)."},
            {"question": "どこに行けばいいか ___ 。(I don't know where I should go.)", "answer": "わかりません", "options": ["わかりません", "おしえてください", "できません", "ありません"], "explanation": "〜かわかりません = don't know whether/where. Embedded question + か + わかりません."},
            {"question": "なんじに来るか ___ ください。(Please tell me what time you're coming.)", "answer": "おしえて", "options": ["おしえて", "しらべて", "かいて", "みて"], "explanation": "教えてください (おしえてください) = please tell me. 何時に来るかおしえてください = please tell me what time you're coming."},
            {"question": "I'm not good at swimming. Which is correct?", "answer": "水泳が苦手です。/ 泳ぐのが苦手です。", "options": ["水泳が苦手です。/ 泳ぐのが苦手です。", "水泳が上手です。", "水泳ができます。", "水泳が得意です。"], "explanation": "苦手 (にがて) = weak point / not good at. 水泳 (すいえい) = swimming."},
        ],
        "examples_q": [
            {"question": "Someone asks if you can use a computer. You can. What do you say?", "answer": "はい、パソコンが使えます。", "options": ["はい、パソコンが使えます。", "はい、パソコンができます。", "はい、パソコンが使います。", "A and B are both correct"], "explanation": "使う → 使える (potential). パソコンが使えます OR パソコンができます both work."},
            {"question": "You can speak Japanese a little. How do you say this modestly?", "answer": "すこし日本語が話せます。", "options": ["すこし日本語が話せます。", "日本語がとても上手です。", "日本語ができません。", "日本語がぜんぜん話せません。"], "explanation": "少し + potential = can do a little. 少し日本語が話せます = can speak Japanese a little."},
            {"question": "You don't know whether the shop is open. How do you express this?", "answer": "みせが開いているかどうかわかりません。", "options": ["みせが開いているかどうかわかりません。", "みせが開いているかわかりません。", "みせが開いているからわかりません。", "Both A and B are natural"], "explanation": "〜かどうかわかりません = don't know whether ~ or not. 〜かわかりません is also natural."},
        ],
    },
    {   "num": 24, "jp": "もっとゆっくり話してください", "en": "Please Speak More Slowly", "icon": "🗣️",
        "vocab": [
            ("もっと", "more / even more", ["less", "a little", "much"]),
            ("ずっと", "all along / much more / continuously", ["occasionally", "briefly", "little by little"]),
            ("〜すぎます", "too ~ / excessively ~", ["not enough ~", "just right ~", "a little ~"]),
            ("〜くなります (い-adj)", "to become ~ (い-adjective change)", ["to stop being ~", "to make ~ (transitive)", "to be ~"]),
            ("〜になります (な-adj/N)", "to become ~ (な-adj or noun change)", ["to stop being ~", "to make ~ (transitive)", "to be ~"]),
            ("〜くします (い-adj)", "to make something ~ (transitive)", ["to become ~", "to stop ~", "to be ~"]),
            ("〜にします (な-adj/N)", "to decide on ~ / make something ~", ["to become ~", "to stop ~", "to suggest ~"]),
            ("はやく", "quickly / early (adverb of 速い/早い)", ["slowly", "late", "quietly"]),
            ("おそく", "slowly / late (adverb of 遅い)", ["quickly", "early", "clearly"]),
            ("おおきく", "in a big way / largely (adverb)", ["in a small way", "quickly", "quietly"]),
            ("ちいさく", "in a small way (adverb)", ["in a big way", "quickly", "quietly"]),
            ("きれいに", "beautifully / cleanly (adverb of きれい)", ["roughly", "dirtily", "carelessly"]),
            ("じょうずに", "skillfully (adverb of 上手)", ["poorly", "slowly", "carelessly"]),
            ("〜ほど〜ない", "not as ~ as ~", ["more ~ than ~", "as ~ as ~", "equally ~"]),
            ("あまり〜ない", "not very ~ (with negative)", ["very ~", "extremely ~", "quite ~"]),
        ],
        "grammar_teach": [
            {"front": "Adverb forms of adjectives", "back": "い-adjective → adverb: drop い + く\nはやい → はやく (quickly)\nおおきい → おおきく (in a big way)\n\nな-adjective → adverb: drop な + に\nじょうずな → じょうずに (skillfully)\nきれいな → きれいに (beautifully)\n\nThink: -ly in English!"},
            {"front": "〜すぎます — Too much", "back": "い-adj: drop い + すぎます\nたかすぎます = too expensive\nむずかしすぎます = too difficult\n\nな-adj: drop な + すぎます\nしずかすぎます = too quiet\n\nVerb stem + すぎます:\n食べすぎます = eat too much"},
            {"front": "Becoming: 〜くなります / 〜になります", "back": "い-adj: drop い + くなります\nさむくなります = becomes cold\nよくなります = gets better\n\nな-adj / Noun: 〜になります\nげんきになります = become well\n医者になります = become a doctor\n\nExpresses a change of state."},
        ],
        "grammar_q": [
            {"question": "もっとゆっくり ___ てください。(Please speak more slowly.)", "answer": "話し", "options": ["話し", "はなく", "はなに", "はなが"], "explanation": "もっと = more. ゆっくり = slowly (already an adverb). 話してください = please speak."},
            {"question": "このへやはしずか ___ ますか。(This room is too quiet?)", "answer": "すぎ", "options": ["すぎ", "すぎに", "くなり", "になり"], "explanation": "な-adj + すぎます = too ~. しずか (quiet, な-adj) → しずかすぎます = too quiet."},
            {"question": "はるになると、あたたかく ___ 。(When it becomes spring, it gets warm.)", "answer": "なります", "options": ["なります", "します", "すぎます", "ください"], "explanation": "〜くなります = to become ~ (い-adj). あたたかい → あたたかく + なります = becomes warm."},
            {"question": "The adverb form of きれい is:", "answer": "きれいに", "options": ["きれいに", "きれいく", "きれいで", "きれいの"], "explanation": "な-adj → adverb: drop な + に. きれいな → きれいに (beautifully/cleanly)."},
            {"question": "食べ ___ ます。(I eat too much.)", "answer": "すぎ", "options": ["すぎ", "すぎに", "くなり", "になり"], "explanation": "Verb stem + すぎます = do too much. 食べ (stem of 食べる) + すぎます = eat too much."},
        ],
        "examples_q": [
            {"question": "The music is too loud. How do you express this?", "answer": "おんがくがうるさすぎます。", "options": ["おんがくがうるさすぎます。", "おんがくがうるさすぎません。", "おんがくがうるさくなります。", "おんがくがうるさいです。"], "explanation": "うるさい (noisy) + すぎます = too noisy. い-adj: drop い + すぎます."},
            {"question": "You want to become a doctor. How do you say this?", "answer": "いしゃになりたいです。", "options": ["いしゃになりたいです。", "いしゃにすぎます。", "いしゃになります。", "いしゃをなりたいです。"], "explanation": "になる = to become. いしゃになりたいです = I want to become a doctor. に marks what you become."},
            {"question": "How do you say 'please write more neatly'?", "answer": "もっときれいにかいてください。", "options": ["もっときれいにかいてください。", "もっときれいくかいてください。", "もっときれいのかいてください。", "もっときれいをかいてください。"], "explanation": "きれいに = adverb form of きれい (な-adj). もっときれいに = more neatly/beautifully."},
        ],
    },
    {   "num": 25, "jp": "お正月はどこへも行きませんでした", "en": "I Didn't Go Anywhere on New Year's", "icon": "🎍",
        "vocab": [
            ("おしょうがつ (お正月)", "New Year's (holiday)", ["Golden Week", "Obon", "Christmas"]),
            ("ゴールデンウィーク", "Golden Week (holiday period)", ["New Year's", "Obon", "New Year's Eve"]),
            ("おぼん (お盆)", "Obon (Buddhist memorial festival)", ["New Year's", "Golden Week", "Christmas"]),
            ("ねんがじょう (年賀状)", "New Year's card", ["Christmas card", "birthday card", "letter"]),
            ("おせちりょうり", "New Year's traditional food", ["summer food", "festival food", "daily food"]),
            ("はつもうで (初詣)", "first shrine/temple visit of New Year", ["summer festival", "autumn festival", "daily prayer"]),
            ("〜なければなりません", "must ~ / have to ~", ["don't have to ~", "want to ~", "can ~"]),
            ("〜なくてはなりません", "must ~ (variant form)", ["don't have to ~", "want to ~", "can ~"]),
            ("〜ばよかったです", "I wish I had ~ / should have ~", ["I'm glad I did ~", "I will ~", "I must ~"]),
            ("〜なければよかったです", "I wish I hadn't ~ / shouldn't have ~", ["I should have ~", "I'm glad I did ~", "I will ~"]),
            ("うらやましい", "envious / jealous", ["happy", "sad", "indifferent"]),
            ("ざんねん (残念)", "regrettable / unfortunate / what a shame", ["wonderful", "lucky", "happy"]),
            ("よかった", "good thing / glad", ["what a shame", "unfortunate", "too bad"]),
            ("たいへんでした (大変でした)", "it was hard/tough", ["it was easy", "it was fun", "it was fine"]),
            ("どこへも〜ない", "not go anywhere / nowhere (motion verb)", ["go somewhere", "go everywhere", "go anywhere"]),
        ],
        "grammar_teach": [
            {"front": "どこへも/なにも/だれも + negative", "back": "Negative universal expressions:\nどこへも行きません = don't go anywhere\nなにも食べません = don't eat anything\nだれにも会いません = don't meet anyone\n\nWith motion verbs: へも\nWith other verbs: も\n\nどこへも行きませんでした。\n= I didn't go anywhere."},
            {"front": "〜ばよかったです — I wish I had done", "back": "Expressing regret about the past:\n[verb ば-form] + よかったです\n\n行く → 行けばよかったです\n= I wish I had gone.\n\n食べる → 食べればよかったです\n= I wish I had eaten.\n\nUsed to express hindsight regret."},
            {"front": "〜なければよかったです — I wish I hadn't", "back": "Regret about something you DID do:\n[verb neg. ば-form] + よかったです\n\n食べなければよかったです。\n= I wish I hadn't eaten. (regretting eating)\n\nいいすぎなければよかったです。\n= I wish I hadn't said too much."},
        ],
        "grammar_q": [
            {"question": "お正月にどこへ ___ 行きませんでした。(I didn't go anywhere on New Year's.)", "answer": "も", "options": ["も", "か", "が", "は"], "explanation": "どこへも + negative = not go anywhere. も after direction particle へ for universal negative."},
            {"question": "もっとはやく起きれ ___ よかったです。(I wish I had woken up earlier.)", "answer": "ば", "options": ["ば", "て", "に", "で"], "explanation": "〜ばよかったです = I wish I had ~. 起きる → 起きれば = ば-conditional form."},
            {"question": "あのえいがを見なければ ___ です。(I wish I hadn't watched that movie.)", "answer": "よかった", "options": ["よかった", "いけない", "なりません", "できません"], "explanation": "〜なければよかったです = I wish I hadn't. 見なければ (hadn't watched) + よかったです = wish I hadn't watched."},
            {"question": "Japanese New Year 'first shrine visit' is called:", "answer": "はつもうで (初詣)", "options": ["はつもうで (初詣)", "おせちりょうり", "ねんがじょう", "おしょうがつ"], "explanation": "初詣 (はつもうで) = the first shrine or temple visit of the New Year. An important Japanese tradition."},
            {"question": "How do you say 'I must send New Year's cards'?", "answer": "ねんがじょうをおくらなければなりません。", "options": ["ねんがじょうをおくらなければなりません。", "ねんがじょうをおくりたいです。", "ねんがじょうをおくらなくてもいいです。", "ねんがじょうをおくってください。"], "explanation": "〜なければなりません = must do. 送る → 送らない → 送らなければなりません = must send."},
        ],
        "examples_q": [
            {"question": "On New Year's, you stayed home all day. How do you say 'I didn't go anywhere'?", "answer": "どこへも行きませんでした。", "options": ["どこへも行きませんでした。", "どこかへ行きませんでした。", "どこにも行きませんでした。", "どこへ行きませんでした。"], "explanation": "どこへも + negative = didn't go anywhere. へも is used with motion verbs (行く, 来る, etc.)."},
            {"question": "You regret not going to the festival. How do you express this?", "answer": "まつりに行けばよかったです。", "options": ["まつりに行けばよかったです。", "まつりに行かなければよかったです。", "まつりに行きたかったです。", "まつりに行かなければなりません。"], "explanation": "〜ばよかったです = I wish I had. 行く → 行けば + よかったです = I wish I had gone."},
            {"question": "What is お盆?", "answer": "Buddhist memorial festival in August for ancestors", "options": ["Buddhist memorial festival in August for ancestors", "New Year's celebration", "Cherry blossom festival in spring", "Summer fireworks festival"], "explanation": "お盆 (おぼん) is an important Japanese Buddhist festival in mid-August when families honor their ancestors."},
            {"question": "You ate too much on New Year's and regret it. How do you say this?", "answer": "食べすぎなければよかったです。", "options": ["食べすぎなければよかったです。", "食べすぎればよかったです。", "食べすぎなくてよかったです。", "食べすぎてよかったです。"], "explanation": "〜なければよかったです = I wish I hadn't. 食べすぎる (eat too much) → 食べすぎなければよかった."},
        ],
    },
]

for ch in CHAPTERS_13_25:
    num = ch["num"]
    jp = ch["jp"]
    en = ch["en"]
    icon = ch["icon"]

    vocab_teach = ch.get("grammar_teach", [
        {"front": f"Lesson {num} key vocabulary", "back": "• " + "\n• ".join([f"{v[0]} = {v[1]}" for v in ch["vocab"][:8]])},
        {"front": f"Lesson {num} more vocabulary", "back": "• " + "\n• ".join([f"{v[0]} = {v[1]}" for v in ch["vocab"][8:16]])},
        {"front": f"Lesson {num} grammar overview", "back": f"Grammar focus for Lesson {num}: {en}"},
    ])

    write(make_vocab_lesson(num, jp, en, icon, vocab_teach, ch["vocab"]))
    write(make_grammar_lesson(num, jp, en, icon, vocab_teach, ch["grammar_q"]))
    write(make_examples_lesson(num, jp, en, icon,
        ch.get("examples_teach", vocab_teach), ch["examples_q"]))

print("\n✅ Chapters 11–25 complete!")

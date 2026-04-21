#!/usr/bin/env python3
"""Generate JLPT N5 lesson files for Minna no Nihongo chapters 6-10."""
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
# CHAPTER 6: 富士山に登りましょう — Let's Climb Mt. Fuji
# ══════════════════════════════════════════════════════════════
ch6_vocab = [
    ("のります (乗ります)", "to ride / board (transport)", ["to get off", "to walk", "to drive"]),
    ("おります (降ります)", "to get off (transport)", ["to board", "to drive", "to walk"]),
    ("あるきます (歩きます)", "to walk", ["to run", "to ride", "to fly"]),
    ("のぼります (登ります)", "to climb", ["to descend", "to walk", "to swim"]),
    ("でんしゃ (電車)", "electric train", ["bus", "taxi", "airplane"]),
    ("バス", "bus", ["train", "taxi", "bicycle"]),
    ("ちかてつ (地下鉄)", "subway / underground", ["train", "bus", "taxi"]),
    ("タクシー", "taxi", ["train", "bus", "bicycle"]),
    ("ひこうき (飛行機)", "airplane", ["train", "ship", "bus"]),
    ("ふね (船)", "ship / boat", ["airplane", "train", "bus"]),
    ("くるま (車)", "car", ["bicycle", "motorcycle", "truck"]),
    ("じてんしゃ (自転車)", "bicycle", ["motorcycle", "car", "bus"]),
    ("〜ませんか", "Won't you ~? / Shall we ~? (invitation)", ["Let's ~!", "Please do ~", "I want to ~"]),
    ("〜ましょう", "Let's ~ (suggestion/invitation)", ["Won't you ~?", "Please ~", "I don't want to ~"]),
    ("〜ましょうか", "Shall I ~? / Shall we ~?", ["Let's ~", "Won't you ~?", "I must ~"]),
    ("いっしょに (一緒に)", "together", ["alone", "separately", "each other"]),
    ("ちょっと", "a little / a moment / (soft refusal)", ["a lot", "always", "never"]),
    ("でも", "but / however (sentence-initial)", ["and", "because", "so"]),
    ("〜てから", "after doing ~ / and then", ["before doing ~", "while doing ~", "without doing ~"]),
    ("はじめに (初めに)", "first of all / to begin with", ["finally", "then", "next"]),
]

ch6_vocab_teach = [
    {"front": "Transportation", "back": "でんしゃ (電車) = electric train\nバス = bus\nちかてつ (地下鉄) = subway\nタクシー = taxi\nひこうき (飛行機) = airplane\nふね (船) = ship\nくるま (車) = car\nじてんしゃ (自転車) = bicycle"},
    {"front": "Transport verbs", "back": "のります (乗ります) = to board/ride\nおります (降ります) = to get off\nあるきます (歩きます) = to walk\nのぼります (登ります) = to climb\n\nで = by (means): でんしゃで = by train\nに = onto: でんしゃに乗ります = board the train"},
    {"front": "Invitation patterns", "back": "〜ませんか = Won't you ~? (inviting someone)\n一緒に映画を見ませんか。\n= Won't you watch a movie together?\n\n〜ましょう = Let's ~! (agreement/suggestion)\n行きましょう！= Let's go!"},
    {"front": "〜ましょうか", "back": "〜ましょうか = Shall I ~? / Shall we ~?\n\nOffering help:\nかばんを持ちましょうか。\n= Shall I carry your bag?\n\nSuggesting together:\n一緒に行きましょうか。= Shall we go together?"},
    {"front": "Soft refusals with ちょっと", "back": "ちょっと... is used to politely decline invitations\nwithout saying NO directly.\n\nA: 映画を見ませんか。\nB: すみません、ちょっと...\n\nA: Won't you watch a movie?\nB: I'm sorry, it's a bit... (implying no)"},
    {"front": "でから = and then / after doing", "back": "[Verb て-form]から + [next action]\n\nでんしゃに乗ってから、バスに乗ります。\n= After taking the train, I take the bus.\n\nCan also use 〜てから for 'after doing':\n食べてから、歯を磨きます。\n= After eating, I brush my teeth."},
    {"front": "て-form basics", "back": "て-form is used to connect actions and make requests.\n\nGroup 1 (u-verbs): 〜って / 〜いて / 〜して\n飲む → 飲んで\n書く → 書いて\n\nGroup 2 (ru-verbs): 〜て\n食べる → 食べて\n見る → 見て\n\nIrregular:\nする → して\nくる → きて"},
    {"front": "Key phrases for invitations", "back": "一緒に〜ませんか。= Won't you ~ together?\nいいですね！= That sounds great!\nいいですよ。= That's fine / Sure.\nすみません、ちょっと... = Sorry, a bit difficult...\nまた今度。= Another time.\nぜひ！= By all means! / Definitely!"},
]

ch6_grammar_q = [
    {"question": "一緒に映画を見 ___ か。(Won't you watch a movie with me?)", "answer": "ません", "options": ["ません", "ます", "ましょう", "ませんでした"], "explanation": "〜ませんか = invitation 'Won't you ~?' Polite and indirect way to invite someone."},
    {"question": "A: 行きませんか。B: ___！(Let's go!)", "answer": "ええ、行きましょう", "options": ["ええ、行きましょう", "いいえ、行きません", "はい、行きました", "いいえ、ちがいます"], "explanation": "ましょう = Let's ~. Used to accept an invitation or make a suggestion."},
    {"question": "でんしゃ ___ 行きます。(I go by train.)", "answer": "で", "options": ["で", "に", "を", "は"], "explanation": "で marks the means of transport. でんしゃで = by train. Do not confuse with に which marks the destination."},
    {"question": "えき ___ 電車に乗ります。(I board the train at the station.)", "answer": "で", "options": ["で", "に", "を", "から"], "explanation": "で marks the location of an action. えきで = at the station (where the action of boarding happens)."},
    {"question": "かばんを持ち ___ か。(Shall I carry your bag?)", "answer": "ましょう", "options": ["ましょう", "ません", "ます", "ました"], "explanation": "〜ましょうか = Shall I ~? / Shall we ~? Used to offer help or make suggestions."},
    {"question": "A: 映画を見ませんか。B: すみません、___... (soft refusal)", "answer": "ちょっと", "options": ["ちょっと", "たくさん", "とても", "よく"], "explanation": "ちょっと... (trailing off) is the Japanese polite way to decline. Saying a direct 'no' can seem rude."},
    {"question": "食べて ___ 、歯を磨きます。(After eating, I brush my teeth.)", "answer": "から", "options": ["から", "まで", "に", "で"], "explanation": "〜てから = after doing ~. [Verb て-form] + から = after doing that action."},
    {"question": "Which て-form is correct for 飲む (to drink)?", "answer": "飲んで", "options": ["飲んで", "飲いて", "飲って", "飲て"], "explanation": "む → んで is one of the て-form rules. む/ぬ/ぶ → んで. So 飲む → 飲んで."},
    {"question": "Which て-form is correct for 書く (to write)?", "answer": "書いて", "options": ["書いて", "書って", "書んで", "書て"], "explanation": "く → いて is the て-form rule for く-ending verbs. 書く → 書いて. Exception: 行く → 行って (not 行いて)!"},
    {"question": "Which て-form is correct for 食べる (to eat)?", "answer": "食べて", "options": ["食べて", "食べって", "食べんで", "食べいて"], "explanation": "Group 2 (ru-verbs): just replace る with て. 食べる → 食べて. Simple!"},
    {"question": "How do you say 'by bicycle'?", "answer": "じてんしゃで", "options": ["じてんしゃで", "じてんしゃに", "じてんしゃを", "じてんしゃが"], "explanation": "で marks means of transport. じてんしゃで = by bicycle."},
    {"question": "一緒に食事しませんか → You want to accept. What do you say?", "answer": "ぜひ！一緒に食事しましょう！", "options": ["ぜひ！一緒に食事しましょう！", "いいえ、ちょっと...", "また今度。", "すみません。"], "explanation": "ぜひ = by all means / definitely! + ましょう = let's. Express enthusiasm when accepting invitations."},
]

ch6_examples_teach = [
    {"front": "Inviting someone out", "back": "A: 今週の土曜日、映画を見ませんか。\nB: いいですね。何時ですか。\nA: 3時はどうですか。\nB: いいですよ。\n\nA: Won't you watch a movie this Saturday?\nB: Sounds good. What time?\nA: How about 3 o'clock?\nB: That works!"},
    {"front": "Getting around: transport conversation", "back": "A: 大阪まで何で行きますか。\nB: 新幹線で行きます。\nA: どのくらいかかりますか。\nB: 2時間半くらいです。\n\nA: How are you going to Osaka?\nB: By bullet train.\nA: How long does it take?\nB: About 2.5 hours."},
    {"front": "Offering help", "back": "A: かばんを持ちましょうか。\nB: ありがとうございます。おねがいします。\n\nA: Shall I carry your bag?\nB: Thank you. Please do.\n\n〜ましょうか is very useful for offering help politely!"},
    {"front": "Declining politely", "back": "A: 一緒に飲みに行きませんか。\nB: すみません、今日はちょっと...\nA: そうですか。また今度。\nB: はい、ぜひ。\n\nA: Won't you go for drinks?\nB: Sorry, today is a bit...\nA: I see. Another time then.\nB: Yes, definitely!"},
    {"front": "Route planning", "back": "えきまでバスで行きます。\nえきで電車に乗ります。\n〇〇えきで地下鉄に乗り換えます。\n\nI go to the station by bus.\nI board the train at the station.\nI transfer to the subway at XX station.\n\n乗り換えます (のりかえます) = to transfer"},
    {"front": "Te-form sequence", "back": "シャワーを浴びてから、朝ごはんを食べます。\n= After showering, I eat breakfast.\n\n朝ごはんを食べてから、歯を磨きます。\n= After eating breakfast, I brush my teeth.\n\nUse て-form + から to connect sequential actions."},
]

ch6_examples_q = [
    {"question": "How do you invite someone to have lunch together?", "answer": "一緒に昼ごはんを食べませんか。", "options": ["一緒に昼ごはんを食べませんか。", "一緒に昼ごはんを食べましょう。", "一緒に昼ごはんを食べますか。", "一緒に昼ごはんが食べませんか。"], "explanation": "〜ませんか = Won't you ~? (invitation to another person). 〜ましょう is used to accept or suggest together."},
    {"question": "Someone invites you and you want to accept enthusiastically. What do you say?", "answer": "ぜひ！", "options": ["ぜひ！", "ちょっと...", "また今度。", "すみません。"], "explanation": "ぜひ = by all means / definitely! The most enthusiastic acceptance."},
    {"question": "You go to work by subway. How do you say this?", "answer": "ちかてつで会社に行きます。", "options": ["ちかてつで会社に行きます。", "ちかてつに会社で行きます。", "ちかてつを会社に行きます。", "ちかてつが会社に行きます。"], "explanation": "で marks means (ちかてつで = by subway), に marks destination (会社に = to the company)."},
    {"question": "What does また今度 mean?", "answer": "Another time / Next time", "options": ["Another time / Next time", "Right away", "Never mind", "Definitely yes"], "explanation": "また今度 = another time / next time. Used as a polite way to postpone or decline an invitation softly."},
    {"question": "How do you offer to carry someone's luggage?", "answer": "荷物を持ちましょうか。", "options": ["荷物を持ちましょうか。", "荷物を持ちませんか。", "荷物を持ちますか。", "荷物を持ちましょう。"], "explanation": "〜ましょうか = Shall I ~? (offering help). 〜ませんか = Won't you ~? (inviting the other person to do something)."},
    {"question": "After showering, I study. How do you express 'after showering'?", "answer": "シャワーを浴びてから", "options": ["シャワーを浴びてから", "シャワーを浴びてまで", "シャワーを浴びてに", "シャワーを浴びてで"], "explanation": "〜てから = after doing ~. [verb て-form] + から."},
    {"question": "Which sentence correctly says 'I go to school by bicycle'?", "answer": "じてんしゃで学校に行きます。", "options": ["じてんしゃで学校に行きます。", "じてんしゃに学校で行きます。", "じてんしゃを学校に行きます。", "じてんしゃが学校に行きます。"], "explanation": "で = by (means), に = to (destination). Two different particles for two different functions."},
    {"question": "What is the て-form of 行く (to go)?", "answer": "行って", "options": ["行って", "行いて", "行んで", "行て"], "explanation": "行く is an exception! Although く→いて normally, 行く becomes 行って (not 行いて). Must memorize!"},
]

write(make_vocab_lesson(6, "富士山に登りましょう", "Let's Climb Mt. Fuji", "🗻", ch6_vocab_teach, ch6_vocab))
write(make_grammar_lesson(6, "富士山に登りましょう", "Let's Climb Mt. Fuji", "🗻", ch6_vocab_teach, ch6_grammar_q))
write(make_examples_lesson(6, "富士山に登りましょう", "Let's Climb Mt. Fuji", "🗻", ch6_examples_teach, ch6_examples_q))

# ══════════════════════════════════════════════════════════════
# CHAPTER 7: 日本語の授業は楽しいですか — Is Japanese Class Fun?
# ══════════════════════════════════════════════════════════════
ch7_vocab = [
    ("おおきい (大きい)", "big / large", ["small", "long", "heavy"]),
    ("ちいさい (小さい)", "small / little", ["big", "short", "light"]),
    ("あたらしい (新しい)", "new", ["old", "used", "modern"]),
    ("ふるい (古い)", "old (things, not people)", ["new", "modern", "young"]),
    ("たかい (高い)", "expensive / tall / high", ["cheap", "short", "low"]),
    ("やすい (安い)", "cheap / inexpensive", ["expensive", "free", "costly"]),
    ("おいしい (美味しい)", "delicious / tasty", ["horrible", "bland", "sour"]),
    ("まずい", "bad-tasting / awful (food)", ["delicious", "good", "sweet"]),
    ("あつい (暑い/熱い)", "hot (weather/thing)", ["cold", "warm", "cool"]),
    ("さむい (寒い)", "cold (weather)", ["hot", "warm", "cool"]),
    ("つめたい (冷たい)", "cold (to the touch / drinks)", ["hot", "warm", "lukewarm"]),
    ("あたたかい (暖かい)", "warm", ["cold", "hot", "cool"]),
    ("おもしろい (面白い)", "interesting / fun / funny", ["boring", "sad", "difficult"]),
    ("つまらない", "boring / dull", ["interesting", "fun", "exciting"]),
    ("むずかしい (難しい)", "difficult / hard", ["easy", "simple", "fun"]),
    ("やさしい (優しい/易しい)", "kind / easy", ["difficult", "mean", "hard"]),
    ("たのしい (楽しい)", "fun / enjoyable", ["boring", "sad", "difficult"]),
    ("いそがしい (忙しい)", "busy", ["free", "relaxed", "quiet"]),
    ("とても", "very / extremely", ["a little", "not very", "sometimes"]),
    ("あまり〜ない", "not very ~ (used with negative)", ["very", "a lot", "always"]),
]

ch7_vocab_teach = [
    {"front": "い-adjectives: size & age", "back": "大きい (おおきい) = big\n小さい (ちいさい) = small\n新しい (あたらしい) = new\n古い (ふるい) = old (things)\n長い (ながい) = long\n短い (みじかい) = short"},
    {"front": "い-adjectives: price & height", "back": "高い (たかい) = expensive / tall\n安い (やすい) = cheap / inexpensive\n広い (ひろい) = wide / spacious\n狭い (せまい) = narrow / cramped\n\nNote: 高い can mean BOTH expensive AND tall!"},
    {"front": "い-adjectives: temperature", "back": "暑い (あつい) = hot (weather/air)\n熱い (あつい) = hot (objects/food)\n寒い (さむい) = cold (weather)\n冷たい (つめたい) = cold (touch/drinks)\n暖かい (あたたかい) = warm"},
    {"front": "い-adjectives: feeling/evaluation", "back": "おいしい = delicious\nまずい = bad-tasting\nおもしろい = interesting/funny\nつまらない = boring\nたのしい = fun\nむずかしい = difficult\nやさしい = easy / kind\nいそがしい = busy"},
    {"front": "い-adjective grammar: positive", "back": "い-adj + です = polite statement\nおいしいです。= It is delicious.\nたかいです。= It is expensive.\n\nい-adj + N = modifying a noun\nおいしいラーメン = delicious ramen\nたかいくつ = expensive shoes"},
    {"front": "い-adjective grammar: negative", "back": "Drop い, add くない\n\nおいしい → おいしくない (not delicious)\nたかい → たかくない (not expensive)\nむずかしい → むずかしくない (not difficult)\n\nPolite: 〜くないです or 〜くありません\nたかくないです = It is not expensive."},
    {"front": "Degree adverbs", "back": "とても = very (positive adjectives)\nあまり = not very (+ negative form)\n\nとても おいしいです。= Very delicious.\nあまり おいしくないです。= Not very delicious.\n\nNever say: あまり おいしいです ✗ (あまり needs negative!)"},
    {"front": "Special adjective: いい", "back": "いい = good (base form)\nよい = good (formal/written)\n\nNegative: よくない (NOT いくない ✗)\nPolite neg: よくないです / よくありません\n\nExample: あまりよくないです。\n= Not very good."},
]

ch7_grammar_q = [
    {"question": "富士山は ___ です。(Mt. Fuji is tall.)", "answer": "たかい", "options": ["たかい", "やすい", "むずかしい", "ふるい"], "explanation": "高い (たかい) = tall / high / expensive. Mt. Fuji is famous for being tall (3,776m)."},
    {"question": "このレストランは ___ です。(This restaurant is delicious.)", "answer": "おいしい", "options": ["おいしい", "まずい", "つまらない", "いそがしい"], "explanation": "おいしい = delicious. To say a restaurant is good, use おいしい (for food) or いい (for the place generally)."},
    {"question": "日本語はむずかし ___ です。(Japanese is difficult.)", "answer": "い", "options": ["い", "く", "な", "の"], "explanation": "い-adjectives keep their い before です. むずかしい + です = むずかしいです."},
    {"question": "このかばんはあまりたか ___ 。(This bag is not very expensive.)", "answer": "くないです", "options": ["くないです", "いないです", "じゃないです", "くあります"], "explanation": "い-adj negative: drop い + くない. たかい → たかくない. + です for polite form."},
    {"question": "とても ___ と あまり ___ (correct combination)", "answer": "とても + positive adj / あまり + negative adj", "options": ["とても + positive adj / あまり + negative adj", "とても + negative adj / あまり + positive adj", "Both with positive adj", "Both with negative adj"], "explanation": "とても = very (used with positive forms). あまり = not very (MUST be used with negative ~くない/~くありません)."},
    {"question": "いい → negative form is:", "answer": "よくない", "options": ["よくない", "いくない", "いじゃない", "いくありません"], "explanation": "いい is irregular! Negative: よくない (not いくない). All other conjugations also use よ-: よくて、よかった、よければ."},
    {"question": "大きい + N = ? (big + car)", "answer": "大きいくるま", "options": ["大きいくるま", "大きくるま", "大きなくるま", "大きのくるま"], "explanation": "い-adjectives directly modify nouns: い-adj + N. 大きい + くるま = 大きいくるま (no change needed). Note: 大きな is also used colloquially but 大きい is standard."},
    {"question": "今日はあつ ___ 。(Today is not hot.)", "answer": "くないです", "options": ["くないです", "いないです", "じゃないです", "くありませんです"], "explanation": "Negative of い-adjective: drop い + くない + です. あつい → あつくない → あつくないです."},
    {"question": "このえいがはとてもおもしろ ___ 。(This movie is very interesting.)", "answer": "いです", "options": ["いです", "くないです", "じゃないです", "いじゃない"], "explanation": "Positive statement: keep い + です. おもしろい + です = おもしろいです."},
    {"question": "How do you say 'Japanese is not very difficult'?", "answer": "日本語はあまりむずかしくないです。", "options": ["日本語はあまりむずかしくないです。", "日本語はとてもむずかしくないです。", "日本語はあまりむずかしいです。", "日本語はとてもむずかしいです。"], "explanation": "あまり = not very (used with negative form). あまり + むずかしくない = not very difficult."},
]

ch7_examples_teach = [
    {"front": "Describing your Japanese class", "back": "A: 日本語の授業はどうですか。\nB: とても楽しいです。でも、少しむずかしいです。\n\nA: How is your Japanese class?\nB: It's very fun. But it's a little difficult."},
    {"front": "Describing food", "back": "このすしはおいしいですか。\n→ はい、とてもおいしいです。\n→ いいえ、あまりおいしくないです。\n\nIs this sushi delicious?\n→ Yes, it's very delicious.\n→ No, it's not very delicious."},
    {"front": "Weather conversation", "back": "A: 今日はどうですか。\nB: とても寒いです！\nA: そうですね。昨日はあたたかかったですね。\nB: ええ、今日のほうが寒いですね。\n\n昨日はあたたかかった = Yesterday was warm (past tense)"},
    {"front": "Shopping: comparing prices", "back": "A: このかばんはたかいですか。\nB: はい、ちょっとたかいです。でもいいですよ。\nA: あちらのかばんは？\nB: あちらのほうがやすいですよ。\n\nA: Is this bag expensive?\nB: Yes, a little expensive. But it's good.\nA: That bag over there?\nB: That one is cheaper."},
    {"front": "い-adjective past tense", "back": "Past positive: い → かった + です\nおいしい → おいしかったです (was delicious)\nたのしい → たのしかったです (was fun)\n\nPast negative: い → くなかった + です\nたかい → たかくなかったです (was not expensive)\n\n昨日のパーティーはたのしかったです！\n= Yesterday's party was fun!"},
    {"front": "What is it like? どうですか", "back": "どうですか = How is it? / What is it like?\n\nUsed to ask for opinions/evaluations:\n日本語はどうですか。= How is Japanese?\n新しい仕事はどうですか。= How is the new job?\n\nCan answer with any い-adjective!"},
]

ch7_examples_q = [
    {"question": "A: 日本はどうですか。B: ___ です。(It's very interesting!)", "answer": "とてもおもしろい", "options": ["とてもおもしろい", "あまりおもしろくない", "すこしつまらない", "とてもつまらない"], "explanation": "どうですか = how is it? Answer with an adjective. とてもおもしろい = very interesting."},
    {"question": "Yesterday's test was difficult. How do you say this?", "answer": "昨日のテストはむずかしかったです。", "options": ["昨日のテストはむずかしかったです。", "昨日のテストはむずかしいです。", "昨日のテストはむずかしくないです。", "昨日のテストはむずかしかったじゃないです。"], "explanation": "い-adjective past: drop い + かった + です. むずかしい → むずかしかったです."},
    {"question": "The movie wasn't very interesting. Which is correct?", "answer": "映画はあまりおもしろくなかったです。", "options": ["映画はあまりおもしろくなかったです。", "映画はとてもおもしろくなかったです。", "映画はあまりおもしろかったです。", "映画はあまりおもしろくないです。"], "explanation": "Past negative: drop い + くなかった + です. おもしろい → おもしろくなかった. あまり goes with negative form."},
    {"question": "How do you say 'This restaurant is cheap and delicious'?", "answer": "このレストランはやすくておいしいです。", "options": ["このレストランはやすくておいしいです。", "このレストランはやすいでおいしいです。", "このレストランはやすいとおいしいです。", "このレストランはやすいておいしいです。"], "explanation": "Connecting い-adjectives: drop い + くて. やすい → やすくて + おいしい = やすくておいしい."},
    {"question": "What does どうですか mean?", "answer": "How is it? / What is it like?", "options": ["How is it? / What is it like?", "Where is it?", "When is it?", "Who is it?"], "explanation": "どうですか = How is it? Used to ask for someone's impression or evaluation of something."},
    {"question": "How do you say 'The weather is warm today'?", "answer": "今日はあたたかいです。", "options": ["今日はあたたかいです。", "今日はあたたかくないです。", "今日はあついです。", "今日はさむいです。"], "explanation": "あたたかい = warm. Note: あつい (hot) = stronger heat. あたたかい = pleasantly warm."},
    {"question": "Which is correct: 'The city is not very busy'?", "answer": "まちはあまりいそがしくないです。", "options": ["まちはあまりいそがしくないです。", "まちはとてもいそがしくないです。", "まちはあまりいそがしいです。", "まちはとてもいそがしいです。"], "explanation": "あまり must be followed by a negative form. いそがしい → いそがしくない. あまりいそがしくない = not very busy."},
    {"question": "How do you connect 'new' and 'cheap' to describe a car?", "answer": "新しくて、安いくるまです。", "options": ["新しくて、安いくるまです。", "新しいで、安いくるまです。", "新しいと、安いくるまです。", "新しいて、安いくるまです。"], "explanation": "い-adj て-form: drop い + くて. 新しい → 新しくて. This connects to the next adjective."},
]

write(make_vocab_lesson(7, "日本語の授業は楽しいですか", "Is Japanese Class Fun?", "📚", ch7_vocab_teach, ch7_vocab))
write(make_grammar_lesson(7, "日本語の授業は楽しいですか", "Is Japanese Class Fun?", "📚", ch7_vocab_teach, ch7_grammar_q))
write(make_examples_lesson(7, "日本語の授業は楽しいですか", "Is Japanese Class Fun?", "📚", ch7_examples_teach, ch7_examples_q))

# ══════════════════════════════════════════════════════════════
# CHAPTER 8: 町をあるきます — Walking Around Town
# ══════════════════════════════════════════════════════════════
ch8_vocab = [
    ("〜てください", "please do ~ (request)", ["please don't ~", "let's ~", "I want to ~"]),
    ("〜てもいいです", "it's okay to ~ / you may ~", ["you must not ~", "please do ~", "let's ~"]),
    ("〜てはいけません", "you must not ~ / it's not okay to ~", ["you may ~", "please do ~", "let's ~"]),
    ("まがります (曲がります)", "to turn", ["to go straight", "to stop", "to cross"]),
    ("わたります (渡ります)", "to cross (a road/bridge)", ["to turn", "to stop", "to walk"]),
    ("とまります (止まります)", "to stop", ["to go", "to turn", "to cross"]),
    ("きります (切ります)", "to cut", ["to open", "to close", "to paste"]),
    ("おくります (送ります)", "to send", ["to receive", "to return", "to buy"]),
    ("あけます (開けます)", "to open (something)", ["to close", "to cut", "to carry"]),
    ("しめます (閉めます)", "to close (something)", ["to open", "to turn on", "to turn off"]),
    ("つけます (付けます)", "to turn on (lights/devices)", ["to turn off", "to open", "to close"]),
    ("けします (消します)", "to turn off / erase", ["to turn on", "to write", "to open"]),
    ("みぎ (右)", "right (direction)", ["left", "straight", "back"]),
    ("ひだり (左)", "left (direction)", ["right", "straight", "forward"]),
    ("まっすぐ", "straight ahead", ["turn right", "turn left", "go back"]),
    ("しんごう (信号)", "traffic light", ["crosswalk", "intersection", "corner"]),
    ("かど (角)", "corner", ["traffic light", "intersection", "bridge"]),
    ("はし (橋)", "bridge", ["corner", "tunnel", "road"]),
    ("まち (町/街)", "town / city / neighbourhood", ["countryside", "mountain", "sea"]),
    ("でんき (電気)", "electricity / electric light", ["water", "gas", "air"]),
]

ch8_vocab_teach = [
    {"front": "Request: てください", "back": "〜て + ください = Please do ~\n\nみてください。= Please look.\nきいてください。= Please listen.\nまってください。= Please wait.\nはなしてください。= Please speak.\n\nPolite command/request form."},
    {"front": "Permission: てもいいです", "back": "〜て + もいいです = It's OK to ~ / You may ~\n\nここにすわってもいいですか。\n= May I sit here?\n→ はい、どうぞ。= Yes, please go ahead.\n→ すみません、ちょっと... = Sorry, it's a bit..."},
    {"front": "Prohibition: てはいけません", "back": "〜て + はいけません = You must not ~\n\nここでたばこを吸ってはいけません。\n= You must not smoke here.\nここに入ってはいけません。\n= You must not enter here.\n\nUsed for rules, signs, warnings."},
    {"front": "Direction verbs", "back": "曲がります (まがります) = to turn\nわたります = to cross\nとまります = to stop\nまっすぐ行きます = go straight\n\nみぎに曲がります = turn right\nひだりに曲がります = turn left\nしんごうをわたります = cross the traffic light"},
    {"front": "On/off verbs", "back": "あけます = to open\nしめます = to close\nつけます = to turn on\nけします = to turn off/erase\n\nまどを開けてください。\n= Please open the window.\nでんきを消してください。\n= Please turn off the light."},
    {"front": "Town vocabulary", "back": "まち (町) = town / neighbourhood\nしんごう (信号) = traffic light\nかど (角) = corner\nはし (橋) = bridge\nこうさてん (交差点) = intersection\nみち (道) = road / path"},
    {"front": "て-form review: Group 1 rules", "back": "〜う / 〜つ / 〜る → って\n買う→買って / 待つ→待って / 切る→切って\n\n〜む / 〜ぬ / 〜ぶ → んで\n飲む→飲んで / 死ぬ→死んで / 遊ぶ→遊んで\n\n〜く → いて (行く → 行って exception!)\n〜ぐ → いで\n〜す → して"},
    {"front": "Key lesson 8 phrases", "back": "ちょっと待ってください。= Please wait a moment.\nもう一度言ってください。= Please say it again.\nゆっくり話してください。= Please speak slowly.\nここに名前を書いてください。= Please write your name here."},
]

ch8_grammar_q = [
    {"question": "ちょっと待っ ___ 。(Please wait a moment.)", "answer": "てください", "options": ["てください", "てもいいです", "てはいけません", "てから"], "explanation": "〜てください = Please do ~. It's a polite request. 待つ → 待って + ください = Please wait."},
    {"question": "ここでたばこを吸っ ___ 。(You must not smoke here.)", "answer": "てはいけません", "options": ["てはいけません", "てもいいです", "てください", "てから"], "explanation": "〜てはいけません = you must not ~. Used for rules and prohibitions."},
    {"question": "写真を撮っ ___ か。(May I take a photo?)", "answer": "てもいいです", "options": ["てもいいです", "てはいけません", "てください", "てから"], "explanation": "〜てもいいですか = May I ~? / Is it okay to ~? Permission question."},
    {"question": "しんごうを ___ 、みぎに曲がってください。(Cross the traffic light, then turn right.)", "answer": "わたって", "options": ["わたって", "まがって", "とまって", "きって"], "explanation": "わたります (to cross) → わたって (て-form). Instructions sequence: [action1]て、[action2]。"},
    {"question": "でんきを ___ 。(Please turn off the light.)", "answer": "けしてください", "options": ["けしてください", "つけてください", "あけてください", "しめてください"], "explanation": "消します (けします) = to turn off/erase. → けして + ください = Please turn off."},
    {"question": "まどを ___ てもいいですか。(May I open the window?)", "answer": "あけ", "options": ["あけ", "しめ", "けし", "つけ"], "explanation": "開けます (あけます) = to open. て-form: 開けて (group 2 verb). あけてもいいですか = May I open (it)?"},
    {"question": "Which て-form is correct for 切る (to cut)?", "answer": "切って", "options": ["切って", "切いて", "切んで", "切て"], "explanation": "切る follows the 〜る → って rule for Group 1 verbs (not Group 2, which simply drops る). 切る → 切って."},
    {"question": "Which て-form is correct for 送る (to send)?", "answer": "送って", "options": ["送って", "送て", "送いて", "送んで"], "explanation": "送る → 送って. Group 1 verb (ends in 〜る but the syllable before is a consonant-row): 〜る → って."},
    {"question": "How do you say 'Please don't smoke here'? (using てはいけません)", "answer": "ここでたばこを吸ってはいけません。", "options": ["ここでたばこを吸ってはいけません。", "ここでたばこを吸ってください。", "ここでたばこを吸ってもいいです。", "ここでたばこを吸ってから。"], "explanation": "〜てはいけません = you must not ~. て-form of 吸う (to smoke) = 吸って + はいけません."},
    {"question": "ここにすわってもいいですか → answer: はい、___。", "answer": "どうぞ", "options": ["どうぞ", "ちがいます", "いけません", "はいけません"], "explanation": "はい、どうぞ = Yes, please go ahead. Standard response when granting permission."},
]

ch8_examples_teach = [
    {"front": "Asking permission in a cafe", "back": "A: すみません、ここにすわってもいいですか。\nB: はい、どうぞ。\n\nA: Excuse me, may I sit here?\nB: Yes, please go ahead.\n\nOr if no:\nB: すみません、そこはちょっと..."},
    {"front": "Classroom instructions", "back": "教科書を開けてください。= Please open your textbook.\n〇ページを見てください。= Please look at page X.\nペアで練習してください。= Please practice in pairs.\nわかりましたか。= Did you understand?"},
    {"front": "Public signs: prohibitions", "back": "はいってはいけません。= No entry.\nさわってはいけません。= Do not touch.\nたばこを吸ってはいけません。= No smoking.\nしゃしんをとってはいけません。= No photography.\nごみをすててはいけません。= No littering."},
    {"front": "Giving directions (て-form chain)", "back": "まっすぐ行って、\nかどを右に曲がって、\nはしをわたると、\n右手にあります。\n\nGo straight,\nturn right at the corner,\ncross the bridge,\nit's on your right."},
    {"front": "Requesting repetition", "back": "もう一度言ってください。= Please say it one more time.\nゆっくり話してください。= Please speak slowly.\nもう少し大きい声で。= A little louder please.\nにほんごで言ってください。= Please say it in Japanese."},
    {"front": "て-form requests chain", "back": "You can chain multiple actions with て-form:\nたって、前に出て、ここに名前を書いてください。\n= Please stand up, come forward, and write your name here.\n\nEach action uses て except the last, which gets ください."},
]

ch8_examples_q = [
    {"question": "A student asks: 日本語で話してもいいですか。What are they asking?", "answer": "May I speak in Japanese?", "options": ["May I speak in Japanese?", "Please speak in Japanese.", "You must not speak in Japanese.", "Let's speak in Japanese."], "explanation": "〜てもいいですか = May I ~? Permission question. 話す → 話して + もいいですか = may I speak?"},
    {"question": "There's a 'No Entry' sign. How do you read it in Japanese?", "answer": "はいってはいけません", "options": ["はいってはいけません", "はいってください", "はいってもいいです", "はいってから"], "explanation": "はいってはいけません = You must not enter. て-form of 入る (はいる) = 入って + はいけません."},
    {"question": "Your teacher says もう一度言ってください。What do you do?", "answer": "Say it again", "options": ["Say it again", "Stop speaking", "Speak louder", "Sit down"], "explanation": "もう一度 = one more time. 言ってください = please say. So もう一度言ってください = Please say it one more time."},
    {"question": "How do you ask 'May I take a photo here?'", "answer": "ここで写真を撮ってもいいですか。", "options": ["ここで写真を撮ってもいいですか。", "ここで写真を撮ってはいけませんか。", "ここで写真を撮ってください。", "ここで写真を撮りましょう。"], "explanation": "撮る (とる) = to take (photo) → 撮って + もいいですか = May I take?"},
    {"question": "The light is on and you want someone to turn it off. What do you say?", "answer": "でんきを消してください。", "options": ["でんきを消してください。", "でんきをつけてください。", "でんきをあけてください。", "でんきをしめてください。"], "explanation": "消します (けします) = turn off/erase. → 消して + ください = Please turn off."},
    {"question": "To give directions: 'Go straight then turn left at the corner.' Which is correct?", "answer": "まっすぐ行って、かどをひだりに曲がってください。", "options": ["まっすぐ行って、かどをひだりに曲がってください。", "まっすぐ行きます、かどをひだりに曲がります。", "まっすぐ行って、かどにひだりを曲がってください。", "まっすぐ行くから、かどをひだりに曲がってください。"], "explanation": "Chain directions with て-form: 行って (go) + 曲がってください (please turn). を marks the place you turn at."},
    {"question": "Which is a correct prohibition sign in Japanese?", "answer": "たばこを吸ってはいけません", "options": ["たばこを吸ってはいけません", "たばこを吸ってください", "たばこを吸ってもいいです", "たばこを吸いましょう"], "explanation": "〜てはいけません = must not ~. This is the form used for rules and prohibitions."},
    {"question": "How do you tell someone to open the window?", "answer": "まどを開けてください。", "options": ["まどを開けてください。", "まどを閉めてください。", "まどを開けてもいいです。", "まどを開けてはいけません。"], "explanation": "開けます (あけます) = to open. → 開けて + ください = Please open."},
]

write(make_vocab_lesson(8, "町をあるきます", "Walking Around Town", "🚶", ch8_vocab_teach, ch8_vocab))
write(make_grammar_lesson(8, "町をあるきます", "Walking Around Town", "🚶", ch8_vocab_teach, ch8_grammar_q))
write(make_examples_lesson(8, "町をあるきます", "Walking Around Town", "🚶", ch8_examples_teach, ch8_examples_q))

# ══════════════════════════════════════════════════════════════
# CHAPTER 9: 買い物をします — Shopping
# ══════════════════════════════════════════════════════════════
ch9_vocab = [
    ("よく", "often / frequently", ["rarely", "sometimes", "never"]),
    ("たいてい", "usually / generally", ["rarely", "sometimes", "never"]),
    ("ときどき (時々)", "sometimes", ["always", "usually", "never"]),
    ("あまり〜ない", "not very often (with negative)", ["always", "sometimes", "usually"]),
    ("ぜんぜん〜ない (全然〜ない)", "not at all (with negative)", ["always", "often", "sometimes"]),
    ("まい〜 (毎〜)", "every ~ (prefix)", ["sometimes", "rarely", "never"]),
    ("〜まい (〜枚)", "counter: flat things (paper, shirts)", ["counter for long things", "counter for machines", "counter for small things"]),
    ("〜ほん/ぼん/ぽん (〜本)", "counter: long thin things (pens, bottles)", ["counter for flat things", "counter for machines", "counter for books"]),
    ("〜だい (〜台)", "counter: machines/vehicles", ["counter for books", "counter for flat things", "counter for long things"]),
    ("〜こ (〜個)", "counter: small round things", ["counter for flat things", "counter for long things", "counter for machines"]),
    ("〜さつ (〜冊)", "counter: books/notebooks", ["counter for flat things", "counter for long things", "counter for machines"]),
    ("〜はい/ばい/ぱい (〜杯)", "counter: cups/glasses/bowls", ["counter for flat things", "counter for bottles", "counter for plates"]),
    ("〜ひき/びき/ぴき (〜匹)", "counter: small animals", ["counter for large animals", "counter for birds", "counter for fish"]),
    ("どのくらい", "how long / how much / how many (extent)", ["how many (exact)", "how much (price)", "when?"]),
    ("〜かかります", "it takes ~ (time/money)", ["it costs ~", "it needs ~", "it gives ~"]),
    ("かいもの (買い物)", "shopping", ["cooking", "cleaning", "gardening"]),
    ("かいます (買います)", "to buy", ["to sell", "to lend", "to borrow"]),
    ("うります (売ります)", "to sell", ["to buy", "to borrow", "to give"]),
    ("かります (借ります)", "to borrow / rent", ["to lend", "to buy", "to return"]),
    ("かえします (返します)", "to return (something)", ["to borrow", "to buy", "to lend"]),
]

ch9_vocab_teach = [
    {"front": "Frequency adverbs", "back": "よく = often\nたいてい = usually\nときどき = sometimes\nあまり〜ない = not very often\nぜんぜん〜ない = not at all\n\nImportant: あまり and ぜんぜん MUST be followed by a NEGATIVE verb!"},
    {"front": "Counters: flat things (〜枚)", "back": "1枚 = いちまい\n2枚 = にまい\n3枚 = さんまい\n4枚 = よんまい\n5枚 = ごまい\n\nUsed for: paper, shirts, CDs, stamps, sliced bread, tickets"},
    {"front": "Counters: long thin things (〜本)", "back": "1本 = いっぽん\n2本 = にほん\n3本 = さんぼん\n4本 = よんほん\n5本 = ごほん\n6本 = ろっぽん\n\nUsed for: pens, bottles, bananas, rivers, roads, movies"},
    {"front": "Counters: machines (〜台)", "back": "1台 = いちだい\n2台 = にだい\n3台 = さんだい\n\nUsed for: cars, computers, washing machines, TVs, bicycles\n\nどのくらいかかりますか = How long/how much does it take?"},
    {"front": "Counters: cups & books", "back": "〜杯 (はい/ばい/ぱい) = cups/glasses/bowls\n1杯=いっぱい / 2杯=にはい / 3杯=さんばい\n\n〜冊 (さつ) = books/notebooks\n1冊=いっさつ / 2冊=にさつ / 3冊=さんさつ"},
    {"front": "Counters: small animals (〜匹)", "back": "〜匹 (ひき/びき/ぴき) = small animals (cats, dogs, fish)\n1匹=いっぴき / 2匹=にひき / 3匹=さんびき\n\nLarge animals use 〜頭 (とう):\n1頭=いっとう / 2頭=にとう (for elephants, horses, cows)\n\nBirds use 〜羽 (わ): 1羽=いちわ"},
    {"front": "どのくらい / 〜かかります", "back": "どのくらいかかりますか。\n= How long does it take? / How much does it cost?\n\n〜時間かかります = it takes ~ hours\n〜分かかります = it takes ~ minutes\n〜円かかります = it costs ~ yen\n\n東京から大阪まで新幹線で2時間半かかります。"},
    {"front": "Buying & borrowing verbs", "back": "買います (かいます) = to buy\n売ります (うります) = to sell\n借ります (かります) = to borrow/rent\n返します (かえします) = to return\n貸します (かします) = to lend\n\nNote: 借ります vs 貸します — easy to confuse!\n借りる = you receive / 貸す = you give"},
]

ch9_grammar_q = [
    {"question": "よく ___ か。(Do you often go shopping?)", "answer": "かいものをしますか", "options": ["かいものをしますか", "かいものをしません", "かいものをしました", "かいものします"], "explanation": "よく = often. Used with positive verb forms. よくかいものをしますか = Do you often go shopping?"},
    {"question": "ぜんぜん ___ 。(I don't drink alcohol at all.)", "answer": "おさけを飲みません", "options": ["おさけを飲みません", "おさけを飲みます", "おさけをよく飲みます", "おさけをときどき飲みます"], "explanation": "ぜんぜん must be followed by a NEGATIVE verb. ぜんぜん〜ません = not at all."},
    {"question": "A shirt costs 2,500 yen. How do you say this?", "answer": "シャツはにせんごひゃくえんです。", "options": ["シャツはにせんごひゃくえんです。", "シャツはごひゃくにせんえんです。", "シャツはにせんえんごひゃくです。", "シャツがにせんごひゃくえんです。"], "explanation": "2500 = にせんごひゃく. 2000 = にせん + 500 = ごひゃく = 2500えん."},
    {"question": "3本のビール (3 bottles of beer) → how do you say '3 bottles'?", "answer": "さんぼん", "options": ["さんぼん", "さんほん", "さんぽん", "みほん"], "explanation": "3本 = さんぼん. Note the voiced consonant: 3=さんぼん, 6=ろっぽん, 1=いっぽん."},
    {"question": "How do you ask 'How many stamps do you want?'", "answer": "きってを何枚ほしいですか。", "options": ["きってを何枚ほしいですか。", "きってを何本ほしいですか。", "きってを何個ほしいですか。", "きってを何台ほしいですか。"], "explanation": "切手 (きって) = stamps. Stamps are flat → use 〜枚 (まい). 何枚 (なんまい) = how many (flat things)."},
    {"question": "東京から大阪まで新幹線で ___ かかりますか。(How long does it take?)", "answer": "どのくらい", "options": ["どのくらい", "いくら", "なんじ", "なんにち"], "explanation": "どのくらいかかりますか = How long does it take? どのくらい = how much/how long (extent)."},
    {"question": "本を3冊買いました。What does 3冊 count?", "answer": "3 books", "options": ["3 books", "3 flat papers", "3 bottles", "3 machines"], "explanation": "〜冊 (さつ) is the counter for books and notebooks. 3冊 = さんさつ = 3 books."},
    {"question": "ときどき映画を見ます。How often does this person watch movies?", "answer": "Sometimes", "options": ["Sometimes", "Always", "Never", "Very often"], "explanation": "ときどき = sometimes. Frequency scale: よく > たいてい > ときどき > あまり〜ない > ぜんぜん〜ない."},
    {"question": "I have 2 cats. Which counter is correct?", "answer": "2匹 (にひき)", "options": ["2匹 (にひき)", "2台 (にだい)", "2枚 (にまい)", "2冊 (にさつ)"], "explanation": "〜匹 (ひき/びき/ぴき) is used for small animals. 2匹 = にひき. (1匹=いっぴき, 3匹=さんびき)"},
    {"question": "本を友達に貸します vs 本を友達から借ります. Which means 'I borrow a book from a friend'?", "answer": "本を友達から借ります", "options": ["本を友達から借ります", "本を友達に貸します", "Both mean the same", "Neither is correct"], "explanation": "借ります (かります) = to borrow (you receive). から = from. 貸します (かします) = to lend (you give). に = to."},
]

ch9_examples_teach = [
    {"front": "Shopping conversation", "back": "A: いらっしゃいませ。\nB: このシャツを2枚ください。\nA: 色は何色がいいですか。\nB: 白と青をください。\nA: かしこまりました。\n\nB: I'd like 2 of these shirts.\nA: What color would you like?"},
    {"front": "Asking how long it takes", "back": "A: ここから東京まで電車でどのくらいかかりますか。\nB: だいたい30分かかります。\n\nA: How long does it take from here to Tokyo by train?\nB: About 30 minutes.\n\nだいたい = approximately / roughly"},
    {"front": "Frequency in conversation", "back": "A: よく映画を見ますか。\nB: ええ、週に1回ぐらい見ます。\nA: どんな映画が好きですか。\nB: アクション映画が好きです。\n\n週に1回 = once a week\n月に2回 = twice a month"},
    {"front": "Counting in context", "back": "りんごを3個ください。= 3 apples please.\nビールを2本ください。= 2 beers please.\nコピーを5枚ください。= 5 copies please.\n本を1冊かしてください。= Please lend me 1 book.\nねこが3匹います。= There are 3 cats."},
    {"front": "〜週に〜回 (times per week)", "back": "週に3回 (しゅうにさんかい) = 3 times a week\n月に1回 (つきにいっかい) = once a month\n年に2回 (ねんににかい) = twice a year\n\nA: どのくらい運動しますか。\nB: 週に3回ジムに行きます。= I go to the gym 3x/week."},
    {"front": "Borrowing and returning", "back": "A: この本を貸してもいいですか。\nB: いいですよ。いつ返しますか。\nA: 来週返します。\nB: じゃ、どうぞ。\n\nA: May I borrow this book?\nB: Sure. When will you return it?\nA: I'll return it next week.\nB: Then, please (take it)."},
]

ch9_examples_q = [
    {"question": "You want to say you 'rarely' eat meat. Which is correct?", "answer": "あまりにくを食べません。", "options": ["あまりにくを食べません。", "あまりにくを食べます。", "ぜんぜんにくを食べます。", "よくにくを食べません。"], "explanation": "あまり requires negative form: あまり〜ません = not very often/rarely."},
    {"question": "You want 3 apples. What do you say in a shop?", "answer": "りんごを3個ください。", "options": ["りんごを3個ください。", "りんごを3枚ください。", "りんごを3本ください。", "りんごを3冊ください。"], "explanation": "Individual round items use 〜個 (こ). りんご (apple) = 個. 3個 = みっこ or さんこ."},
    {"question": "How do you ask 'How long does it take to get to the station?'", "answer": "えきまでどのくらいかかりますか。", "options": ["えきまでどのくらいかかりますか。", "えきまでいくらかかりますか。", "えきまでなんじかかりますか。", "えきまでなんかいかかりますか。"], "explanation": "どのくらいかかりますか = how long does it take? Use this for duration of travel."},
    {"question": "I watch TV every day. Which frequency word is best?", "answer": "まいにち", "options": ["まいにち", "よく", "ときどき", "あまり"], "explanation": "毎日 (まいにち) = every day. This is the strongest frequency (100%). よく = often (but not every day)."},
    {"question": "4本のジュース (4 juices). How do you read 4本?", "answer": "よんほん", "options": ["よんほん", "よんぼん", "よんぽん", "しほん"], "explanation": "4本 = よんほん. The counter 本 changes: 1=いっぽん, 3=さんぼん, 4=よんほん, 6=ろっぽん."},
    {"question": "A friend asks to borrow your dictionary. How do they ask?", "answer": "じしょを貸してもいいですか。", "options": ["じしょを貸してもいいですか。", "じしょを借りてもいいですか。", "じしょを返してもいいですか。", "じしょを買ってもいいですか。"], "explanation": "貸す (かす) = to lend. The friend is asking YOU to lend, so they use 貸してもいいですか (may you lend me?). Note: they could also say じしょを借りてもいいですか (may I borrow?)."},
    {"question": "I go to the gym twice a week. How do you say this?", "answer": "週に2回ジムに行きます。", "options": ["週に2回ジムに行きます。", "月に2回ジムに行きます。", "日に2回ジムに行きます。", "年に2回ジムに行きます。"], "explanation": "週に〜回 = ~ times per week. 2回 = にかい = 2 times."},
    {"question": "You never eat sushi. Which is correct?", "answer": "ぜんぜんすしを食べません。", "options": ["ぜんぜんすしを食べません。", "ぜんぜんすしを食べます。", "あまりすしを食べません。", "ぜんぜんすしを食べましょう。"], "explanation": "ぜんぜん = not at all. Must be followed by negative: ぜんぜん〜ません. Stronger than あまり."},
]

write(make_vocab_lesson(9, "買い物をします", "Shopping", "🛍️", ch9_vocab_teach, ch9_vocab))
write(make_grammar_lesson(9, "買い物をします", "Shopping", "🛍️", ch9_vocab_teach, ch9_grammar_q))
write(make_examples_lesson(9, "買い物をします", "Shopping", "🛍️", ch9_examples_teach, ch9_examples_q))

# ══════════════════════════════════════════════════════════════
# CHAPTER 10: 富士山より高い山はありますか — Comparison
# ══════════════════════════════════════════════════════════════
ch10_vocab = [
    ("〜より", "more than ~ / compared to ~", ["less than ~", "as much as ~", "same as ~"]),
    ("〜のほうが", "~ is more (comparing two things)", ["~ is less", "~ is the same", "~ is not"]),
    ("どちら / どっち", "which one (of two)?", ["which one (of many)", "how?", "where?"]),
    ("いちばん (一番)", "the most / number one / best", ["second most", "least", "worst"]),
    ("〜の中で (〜のなかで)", "among ~ / within ~", ["outside of ~", "next to ~", "compared to ~"]),
    ("どれ", "which one (of three or more)?", ["which of two?", "how?", "where?"]),
    ("〜と〜とどちらが", "between ~ and ~, which is more ~?", ["how much more?", "which is best of all?", "how are they different?"]),
    ("〜くらい/〜ぐらい", "approximately ~ / about ~", ["exactly ~", "more than ~", "less than ~"]),
    ("おなじ (同じ)", "the same / identical", ["different", "similar", "opposite"]),
    ("ちがいます (違います)", "different / wrong / to differ", ["same", "correct", "similar"]),
    ("きせつ (季節)", "season", ["weather", "holiday", "month"]),
    ("はる (春)", "spring", ["summer", "autumn", "winter"]),
    ("なつ (夏)", "summer", ["spring", "autumn", "winter"]),
    ("あき (秋)", "autumn / fall", ["spring", "summer", "winter"]),
    ("ふゆ (冬)", "winter", ["spring", "summer", "autumn"]),
    ("やま (山)", "mountain", ["sea", "river", "forest"]),
    ("うみ (海)", "sea / ocean", ["mountain", "river", "lake"]),
    ("かわ (川)", "river", ["sea", "mountain", "lake"]),
    ("しぜん (自然)", "nature", ["city", "building", "road"]),
    ("すき (好き)", "like / fond of (な-adjective)", ["dislike", "hate", "neutral"]),
]

ch10_vocab_teach = [
    {"front": "Comparison: AはBより〜", "back": "A は B より [adjective] です。\n= A is more [adj] than B.\n\n富士山はエベレストより低いです。\n= Mt. Fuji is lower than Everest.\n\nNote: より comes AFTER the comparison point (B)."},
    {"front": "Comparison: AよりBのほうが〜", "back": "A より B のほうが [adjective] です。\n= B is more [adj] than A.\n\nバスより電車のほうが速いです。\n= The train is faster than the bus.\n\nのほうが = 'on the side of' (more natural for comparisons)"},
    {"front": "Asking comparison: どちらが〜", "back": "AとBとどちらが〜ですか。\n= Between A and B, which is more ~?\n\nすしとてんぷらとどちらがすきですか。\n= Do you like sushi or tempura better?\n\n→ すしのほうがすきです。= I prefer sushi."},
    {"front": "Superlative: いちばん〜", "back": "〜の中でいちばん〜 = the most ~ among ~\n\nクラスの中でだれがいちばん背が高いですか。\n= Who is the tallest in the class?\n\n日本でいちばん高い山は富士山です。\n= The highest mountain in Japan is Mt. Fuji."},
    {"front": "Seasons", "back": "春 (はる) = spring (March-May)\n夏 (なつ) = summer (June-August)\n秋 (あき) = autumn (September-November)\n冬 (ふゆ) = winter (December-February)\n\nQuestion: 一年の中でいつがいちばん好きですか。\n= Which season do you like best?"},
    {"front": "おなじ vs ちがう", "back": "同じ (おなじ) = same / identical\n違う (ちがう) = different\n\nこれとそれはおなじですか。\n= Are these the same?\n→ はい、おなじです。/ いいえ、ちがいます。\n\nNote: おなじ doesn't take な before a noun: おなじくるま (not おなじなくるま)"},
    {"front": "〜くらい (approximately)", "back": "〜くらい / 〜ぐらい = about / approximately\n\n30分くらいかかります。\n= It takes about 30 minutes.\n\nおなじくらい = about the same\n\nどのくらい = how much? / how long?"},
    {"front": "Key question patterns for comparison", "back": "1. どちらが〜ですか。= Which is more ~?\n2. 〜の中でいちばん〜のは何ですか。= What is the most ~ in ~?\n3. どれがいちばん〜ですか。= Which is the most ~?\n4. AとBはどちらがすきですか。= Do you prefer A or B?"},
]

ch10_grammar_q = [
    {"question": "東京は大阪 ___ 大きいです。(Tokyo is bigger than Osaka.)", "answer": "より", "options": ["より", "のほうが", "いちばん", "ぐらい"], "explanation": "A は B より adj = A is more adj than B. より comes after the comparison point B."},
    {"question": "バス ___ 電車のほうが速いです。(The train is faster than the bus.)", "answer": "より", "options": ["より", "が", "と", "に"], "explanation": "AよりBのほうが = B is more ~ than A. より follows the thing being compared against (A=bus)."},
    {"question": "A: すしとさしみとどちらがすきですか。B: ___のほうがすきです。(I prefer sushi.)", "answer": "すし", "options": ["すし", "さしみ", "どちらも", "りょうほう"], "explanation": "どちらが〜ですか = which do you prefer? Answer with [choice] + のほうがすきです."},
    {"question": "日本で ___ 高い山は富士山です。(The highest mountain in Japan is Mt. Fuji.)", "answer": "いちばん", "options": ["いちばん", "より", "のほうが", "ぐらい"], "explanation": "いちばん = the most / number one. 〜でいちばん〜 = the most ~ in ~."},
    {"question": "クラスの ___ でだれがいちばん背が高いですか。(Who is tallest in the class?)", "answer": "中", "options": ["中", "上", "下", "外"], "explanation": "〜の中で = among ~ / within ~. の中で marks the scope of comparison."},
    {"question": "春と夏とどちらがすきですか → 夏 ___ すきです。(I prefer summer.)", "answer": "のほうが", "options": ["のほうが", "より", "いちばん", "ぐらい"], "explanation": "Answer to どちらが: [choice] + のほうが + すきです. Literally 'summer's side is more liked'."},
    {"question": "これとそれは ___ です。(These are the same.)", "answer": "おなじ", "options": ["おなじ", "ちがい", "よく", "いちばん"], "explanation": "おなじ = same. Used as a な-adjective but without な before nouns: おなじくるま (same car)."},
    {"question": "東京と大阪はどちらが ___ ですか。(Which is bigger, Tokyo or Osaka?)", "answer": "大きい", "options": ["大きい", "大きくない", "大きさ", "大きく"], "explanation": "どちらが〜ですか asks for a comparison. Use the plain adjective form (大きい)."},
    {"question": "3つの中でどれがいちばん ___ ですか。(Which of the three is cheapest?)", "answer": "安い", "options": ["安い", "安く", "安さ", "安いの"], "explanation": "いちばん〜 = the most ~. Use the plain adjective form: いちばん安い = cheapest."},
    {"question": "新幹線と飛行機はどちらが ___ ですか。(Which is faster, the shinkansen or airplane?)", "answer": "速い (はやい)", "options": ["速い (はやい)", "高い (たかい)", "安い (やすい)", "大きい (おおきい)"], "explanation": "速い (はやい) = fast. This comparison question asks about speed of transport."},
    {"question": "How do you ask 'What is the most delicious food in Japan?'", "answer": "日本でいちばんおいしいたべものはなんですか。", "options": ["日本でいちばんおいしいたべものはなんですか。", "日本よりおいしいたべものはなんですか。", "日本のほうがおいしいたべものはなんですか。", "日本にいちばんおいしいたべものはなんですか。"], "explanation": "〜でいちばん〜 = the most ~ in ~. で marks the scope (in Japan). いちばん + adjective for superlative."},
]

ch10_examples_teach = [
    {"front": "Comparing cities", "back": "A: 東京と大阪とどちらが大きいですか。\nB: 東京のほうが大きいです。\n\nA: Between Tokyo and Osaka, which is bigger?\nB: Tokyo is bigger.\n\nNote: Both cities named with と, answer uses のほうが."},
    {"front": "Comparing food preferences", "back": "A: すしとラーメンとどちらがすきですか。\nB: う〜ん、どちらもすきです！\n\nA: Do you prefer sushi or ramen?\nB: Hmm, I like both!\n\nどちらも = both. どちらも〜ません = neither."},
    {"front": "Superlative: best season", "back": "A: 一年の中でいつがいちばんすきですか。\nB: 秋がいちばんすきです。\nA: どうしてですか。\nB: 紅葉がきれいだからです。\n\nA: Which season do you like best?\nB: I like autumn best.\nA: Why?\nB: Because the autumn leaves are beautiful."},
    {"front": "Comparing transportation", "back": "A: 電車とバスとどちらが便利ですか。\nB: 電車のほうが便利です。でもバスのほうが安いです。\n\nA: Train or bus — which is more convenient?\nB: The train is more convenient. But the bus is cheaper.\n\n便利 (べんり) = convenient (な-adjective)"},
    {"front": "な-adjectives in comparison", "back": "な-adjectives work the same in comparisons:\n\nAよりBのほうがにぎやかです。\n= B is more lively than A.\n\nいちばんきれいなまち = the most beautiful city\n\nな-adj + な + N (modifying a noun)\nきれいなみち = beautiful road"},
    {"front": "Expressing similarity", "back": "A: この2つはおなじですか。\nB: はい、おなじです。 / いいえ、ちがいます。\n\nA: Are these two the same?\nB: Yes, they're the same. / No, they're different.\n\nおなじくらい = about the same (degree)\nほぼおなじ = almost the same"},
]

ch10_examples_q = [
    {"question": "How do you say 'Coffee is more expensive than tea'?", "answer": "コーヒーはおちゃより高いです。", "options": ["コーヒーはおちゃより高いです。", "おちゃはコーヒーより高いです。", "コーヒーのほうがおちゃより高いです。", "コーヒーとおちゃはおなじです。"], "explanation": "AはBより〜: コーヒーはおちゃより高い = Coffee is more expensive than tea. より comes after the comparison point (tea)."},
    {"question": "What season is most popular in Japan for tourism?", "answer": "春 (はる) — cherry blossoms!", "options": ["春 (はる) — cherry blossoms!", "夏 (なつ) — summer festivals", "秋 (あき) — autumn leaves", "冬 (ふゆ) — winter sports"], "explanation": "Spring (春) is iconic for 花見 (はなみ = cherry blossom viewing). Though all seasons are popular, spring tops tourist polls."},
    {"question": "You prefer summer to winter. Which sentence is correct?", "answer": "冬より夏のほうがすきです。", "options": ["冬より夏のほうがすきです。", "夏より冬のほうがすきです。", "冬のほうが夏よりすきです。", "夏は冬がすきです。"], "explanation": "A より B のほうがすき = I prefer B to A. So 冬より夏のほうがすき = I prefer summer to winter."},
    {"question": "Among all fruits, you love strawberries the most. How do you say this?", "answer": "くだもののなかでいちばんいちごがすきです。", "options": ["くだもののなかでいちばんいちごがすきです。", "くだもののなかでいちごよりすきです。", "くだもののいちごはいちばんすきです。", "くだもののなかでいちごのほうがすきです。"], "explanation": "〜の中でいちばん〜 = the most ~ among ~. いちご (strawberry) + が好き = like strawberries."},
    {"question": "You're comparing two dictionaries. What question do you ask?", "answer": "このじしょとあのじしょとどちらがいいですか。", "options": ["このじしょとあのじしょとどちらがいいですか。", "このじしょとあのじしょのほうがいいですか。", "このじしょとあのじしょはどれがいいですか。", "このじしょはあのじしょよりいいですか。"], "explanation": "AとBとどちらが〜 = between A and B, which is more ~? Use どちら for two options."},
    {"question": "Spring and summer are both nice. How do you express 'both are nice'?", "answer": "春も夏もどちらもいいです。", "options": ["春も夏もどちらもいいです。", "春と夏はいちばんいいです。", "春より夏のほうがいいです。", "春と夏はどちらかいいです。"], "explanation": "どちらも = both. 春も夏もどちらもいいです = Both spring and summer are nice."},
    {"question": "How do you say 'Mt. Fuji is the highest mountain in Japan'?", "answer": "富士山は日本でいちばん高い山です。", "options": ["富士山は日本でいちばん高い山です。", "富士山は日本より高い山です。", "富士山は日本のほうが高い山です。", "富士山が日本でいちばんの山です。"], "explanation": "〜でいちばん〜 = the most ~ in ~. いちばん高い = highest. 日本で = in Japan."},
    {"question": "What does ちがいます mean?", "answer": "It's different / That's wrong", "options": ["It's different / That's wrong", "It's the same", "It's correct", "It's better"], "explanation": "ちがいます = it's different / that's wrong. Used to politely deny or correct something. (いいえ、ちがいます = No, that's wrong.)"},
]

write(make_vocab_lesson(10, "富士山より高い山はありますか", "Comparison", "⚖️", ch10_vocab_teach, ch10_vocab))
write(make_grammar_lesson(10, "富士山より高い山はありますか", "Comparison", "⚖️", ch10_vocab_teach, ch10_grammar_q))
write(make_examples_lesson(10, "富士山より高い山はありますか", "Comparison", "⚖️", ch10_examples_teach, ch10_examples_q))

print("\n✅ Chapters 6–10 complete (15 files generated)")

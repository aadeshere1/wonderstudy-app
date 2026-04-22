"""Patch N5 grammar/examples Ch01-08 to reach 20 questions each."""
import json, os

BASE = os.path.join(os.path.dirname(__file__), '..', 'data', 'classes', 'jlpt', 'n5')

def load(ch, kind):
    path = os.path.join(BASE, f'ch{ch:02d}-{kind}.json')
    return json.load(open(path, encoding='utf-8')), path

def save(d, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def patch(d, path, new_qs):
    key = 'questions' if 'questions' in d['practice'] else 'items'
    existing = d['practice'][key]
    combined = existing + new_qs
    d['practice'][key] = combined
    d['challenge'][key] = combined
    for sec in ['practice', 'challenge']:
        d[sec]['config']['questionsCount'] = len(combined)
    save(d, path)
    print(f"  ✓ {os.path.basename(path)}: {len(existing)} → {len(combined)}")

# ── Ch01: はじめまして ─────────────────────────────────────────────────────

ch01_grammar_add = [
    {"question": "スミスさんは _____ じん です。(Mr Smith is American.)", "answer": "アメリカ", "options": ["アメリカ", "にほん", "フランス", "ちゅうごく"], "explanation": "Nationality + じん = person from that country. アメリカじん = American."},
    {"question": "わたしは かいしゃいん _____。(I am a company employee.)", "answer": "です", "options": ["です", "じゃ", "は", "も"], "explanation": "NはN+です = X is Y. Polite copula at sentence end."},
    {"question": "キムさんは がくせい じゃ _____。(Kim is not a student.)", "answer": "ありません", "options": ["ありません", "です", "いません", "ません"], "explanation": "〜じゃありません is the negative of 〜です. Not X."},
    {"question": "これは なんですか。 _____ ほんです。", "answer": "これは", "options": ["これは", "それが", "あれも", "どれは"], "explanation": "Answer to 'what is this?' restates the topic with は."},
    {"question": "マリアさん_____ せんせいです。(Maria is a teacher.)", "answer": "は", "options": ["は", "が", "を", "の"], "explanation": "は marks the topic of the sentence. Xは Yです = X is Y."},
]

ch01_examples_add = [
    {"question": "Someone asks your name. How do you respond?", "answer": "わたしは たなかです。", "options": ["わたしは たなかです。", "わたしが たなかじゃ ない。", "たなかは わたしです。", "わたしを たなかです。"], "explanation": "わたしは〜です = I am ~. は marks topic."},
    {"question": "You want to ask if someone is a teacher. What do you say?", "answer": "せんせいですか。", "options": ["せんせいですか。", "せんせいじゃない？", "せんせいでしょう。", "せんせいますか。"], "explanation": "Add か to the end of a です-sentence to make a yes/no question."},
    {"question": "You are introducing yourself at a party. First thing you say?", "answer": "はじめまして。", "options": ["はじめまして。", "おはようございます。", "さようなら。", "ありがとう。"], "explanation": "はじめまして = Nice to meet you (first meeting greeting)."},
    {"question": "You want to say 'I am also a student.' (like the previous person)", "answer": "わたしも がくせいです。", "options": ["わたしも がくせいです。", "わたしは がくせいじゃない。", "わたしが がくせいです。", "わたしを がくせいです。"], "explanation": "も replaces は to mean 'also/too'."},
    {"question": "How do you say 'I work at a company' (I am a company employee)?", "answer": "かいしゃいんです。", "options": ["かいしゃいんです。", "がっこうです。", "せんせいじゃ ありません。", "かいしゃいんじゃ ない。"], "explanation": "Occupation+です = I am [occupation]. No need for わたしは in casual self-introduction."},
    {"question": "At the end of a first meeting, you say?", "answer": "どうぞ よろしく おねがいします。", "options": ["どうぞ よろしく おねがいします。", "おやすみなさい。", "いただきます。", "ごちそうさまでした。"], "explanation": "どうぞよろしくおねがいします = Please treat me well. Standard closing of self-introduction."},
    {"question": "Someone says はじめまして to you. How do you respond?", "answer": "はじめまして。どうぞ よろしく。", "options": ["はじめまして。どうぞ よろしく。", "はい、そうです。", "いいえ、ちがいます。", "おはようございます。"], "explanation": "Mirror はじめまして and add どうぞよろしく when meeting for the first time."},
    {"question": "You want to deny being a doctor. You say:", "answer": "いしゃじゃ ありません。", "options": ["いしゃじゃ ありません。", "いしゃです。", "いしゃも いません。", "いしゃが ありません。"], "explanation": "〜じゃありません negates a noun predicate."},
    {"question": "Asking where someone is from (nationality)?", "answer": "〜じんですか。", "options": ["〜じんですか。", "〜からですか。", "〜でしたか。", "〜にですか。"], "explanation": "Country+じん+ですか = Are you [nationality]?"},
    {"question": "Your name card says your job is エンジニア. How do you say it?", "answer": "エンジニアです。", "options": ["エンジニアです。", "エンジニアじゃない。", "エンジニアが あります。", "エンジニアに なります。"], "explanation": "Simply state occupation+です for 'I am a/an [job]'."},
]

# ── Ch02: これはなんですか ─────────────────────────────────────────────────

ch02_grammar_add = [
    {"question": "これは だれの かばんですか。_____ のです。(Whose bag is this? It is mine.)", "answer": "わたし", "options": ["わたし", "あなた", "かれ", "せんせい"], "explanation": "の after a noun/pronoun shows possession: わたしの = mine."},
    {"question": "A: それは なんですか。B: ___ はんです。(It is a handbook.)", "answer": "これ", "options": ["これ", "それ", "あれ", "どれ"], "explanation": "Speaker uses これ for what is near them even if the listener said それ."},
    {"question": "その とけいは _____の ですか。(Whose watch is that?)", "answer": "だれ", "options": ["だれ", "なに", "どこ", "どれ"], "explanation": "だれの = whose. なにの = what's, どこの = from where."},
    {"question": "あれは テレビ _____。(That over there is a TV.)", "answer": "です", "options": ["です", "ます", "じゃ", "か"], "explanation": "あれは〜です = That (over there) is ~."},
    {"question": "こちら_____ スミスさんです。(This is Mr Smith.) (introductions)", "answer": "は", "options": ["は", "が", "の", "を"], "explanation": "こちらは = This person is. Used when introducing someone."},
    {"question": "この かばんは _____の ですか。(Whose bag is this?)", "answer": "だれ", "options": ["だれ", "なに", "どれ", "いくら"], "explanation": "だれの+Noun = whose noun? Asking possession."},
    {"question": "それは えんぴつ じゃ _____。(That is not a pencil.)", "answer": "ありません", "options": ["ありません", "います", "あります", "ません"], "explanation": "〜じゃありません = is not [noun]."},
    {"question": "A: このノートは _____ ですか。B: 500えんです。(How much is this notebook?)", "answer": "いくら", "options": ["いくら", "なに", "だれ", "どこ"], "explanation": "いくら = how much (price). Used when asking about cost."},
]

ch02_examples_add = [
    {"question": "You pick up something unfamiliar. How do you ask what it is?", "answer": "これは なんですか。", "options": ["これは なんですか。", "これは だれですか。", "これは いつですか。", "これは どこですか。"], "explanation": "なん(なに) = what. これはなんですか = What is this?"},
    {"question": "You want to say 'That (near you) is my dictionary.'", "answer": "それは わたしの じしょです。", "options": ["それは わたしの じしょです。", "あれは わたしが じしょです。", "これは わたしを じしょです。", "それを わたしの じしょです。"], "explanation": "それは = that (near listener). わたしの = my. じしょ = dictionary."},
    {"question": "Pointing at something far away, you ask what it is.", "answer": "あれは なんですか。", "options": ["あれは なんですか。", "それは なんですか。", "これは なんですか。", "どれは なんですか。"], "explanation": "あれ = that (far from both speakers)."},
    {"question": "Asking the price of an item in a shop:", "answer": "これは いくらですか。", "options": ["これは いくらですか。", "これは なんですか。", "これは どこですか。", "これは だれですか。"], "explanation": "いくら = how much (price query)."},
    {"question": "You want to say 'This is Mr Tanaka's book.'", "answer": "これは たなかさんの ほんです。", "options": ["これは たなかさんの ほんです。", "これが たなかさんを ほんです。", "これは たなかさんが ほんです。", "これも たなかさんに ほんです。"], "explanation": "Person+の+noun = person's noun (possession)."},
    {"question": "Someone shows you their ID card. How do you introduce yourself using こちらは?", "answer": "こちらは やまださんです。", "options": ["こちらは やまださんです。", "それは やまださんです。", "あちらは やまださんです。", "どちらは やまださんです。"], "explanation": "こちらは used to introduce someone standing nearby."},
    {"question": "Which word means 'that one' when choosing among several options?", "answer": "どれ", "options": ["どれ", "これ", "それ", "あれ"], "explanation": "どれ = which one (of three or more)."},
    {"question": "A: このかばんは スミスさんのですか。B: _____、わたしのじゃありません。", "answer": "いいえ", "options": ["いいえ", "はい", "ええ", "そう"], "explanation": "いいえ = No (polite). Negation response."},
    {"question": "You want to say 'That is not a camera, it is a phone.'", "answer": "それは カメラじゃ ありません。でんわです。", "options": ["それは カメラじゃ ありません。でんわです。", "それは カメラです。でんわじゃ ありません。", "これは カメラじゃ ありません。でんわです。", "それが カメラを ありません。でんわです。"], "explanation": "〜じゃありません。〜です = It is not X. It is Y."},
    {"question": "Asking 'Which one is yours?' among several bags:", "answer": "どれが あなたのですか。", "options": ["どれが あなたのですか。", "どこが あなたのですか。", "だれが あなたのですか。", "なにが あなたのですか。"], "explanation": "どれ = which one (choosing from multiple items)."},
    {"question": "You want to say 'This is 1,500 yen.'", "answer": "これは せんごひゃくえんです。", "options": ["これは せんごひゃくえんです。", "これは ごひゃくえんです。", "これは いちまんえんです。", "これは ひゃくえんです。"], "explanation": "1500 = せんごひゃく. Japanese numbers: 1000=せん, 500=ごひゃく."},
    {"question": "Politely confirming: 'Is this yours, Mr Yamada?'", "answer": "これは やまださんのですか。", "options": ["これは やまださんのですか。", "これを やまださんのですか。", "これが やまださんですか。", "これは やまださんでしたか。"], "explanation": "〜のですか = Is it ~'s? Confirming possession."},
]

# ── Ch03: ここはどこですか ─────────────────────────────────────────────────

ch03_grammar_add = [
    {"question": "トイレは _____ ですか。(Where is the restroom?)", "answer": "どこ", "options": ["どこ", "なに", "だれ", "いつ"], "explanation": "どこ = where. Used for location questions."},
    {"question": "エレベーターは _____ かいに あります。(The elevator is on the 2nd floor.)", "answer": "に", "options": ["に", "は", "が", "を"], "explanation": "〜かいに = on the Nth floor. に marks location."},
    {"question": "ATMは _____ にあります。(The ATM is over there.)", "answer": "あそこ", "options": ["あそこ", "ここ", "そこ", "どこ"], "explanation": "あそこ = over there (far from both). ここ=here, そこ=there (near listener)."},
    {"question": "この へやは _____ えん ですか。(How much is this room per night?)", "answer": "いくら", "options": ["いくら", "なんえん", "いくつ", "なんかい"], "explanation": "いくら = how much (money)."},
    {"question": "ここは _____ うけつけです。(This is the reception desk.)", "answer": "うけつけ", "options": ["うけつけ", "エレベーター", "かいだん", "レストラン"], "explanation": "うけつけ = reception/front desk. Common location word."},
    {"question": "かいぎしつは _____ かいですか。(What floor is the meeting room?)", "answer": "なん", "options": ["なん", "どこ", "いくつ", "いくら"], "explanation": "なんかい = what floor. なん + counter for asking numbers."},
    {"question": "ぎんこうは _____ ちかくに あります。(The bank is near the station.)", "answer": "えき", "options": ["えき", "こうえん", "びょういん", "がっこう"], "explanation": "えき = station. ちかく = near/nearby."},
    {"question": "スーパーは _____ の となりです。(The supermarket is next to the park.)", "answer": "こうえん", "options": ["こうえん", "えき", "ゆうびんきょく", "やっきょく"], "explanation": "こうえん = park. となり = next door."},
]

ch03_examples_add = [
    {"question": "You're lost in a building. How do you ask where the elevator is?", "answer": "エレベーターは どこですか。", "options": ["エレベーターは どこですか。", "エレベーターは なんですか。", "エレベーターは いつですか。", "エレベーターは だれですか。"], "explanation": "どこ = where. 〜はどこですか = Where is ~?"},
    {"question": "The receptionist tells you 'The restaurant is on the 3rd floor.' How do they say it?", "answer": "レストランは さんかいに あります。", "options": ["レストランは さんかいに あります。", "レストランは さんかいが います。", "レストランは さんかいで あります。", "レストランを さんかいに あります。"], "explanation": "Location+に+あります = exists at [location] (for inanimate things)."},
    {"question": "You want to ask what floor the gift shop is on.", "answer": "みやげもの うりばは なんかいですか。", "options": ["みやげもの うりばは なんかいですか。", "みやげもの うりばは どこですか。", "みやげもの うりばは いくらですか。", "みやげもの うりばは なんですか。"], "explanation": "なんかい = what floor. Both なんかい and どこ work but なんかい is more specific."},
    {"question": "Saying 'The post office is over there (far away).'", "answer": "ゆうびんきょくは あそこです。", "options": ["ゆうびんきょくは あそこです。", "ゆうびんきょくは ここです。", "ゆうびんきょくは そこです。", "ゆうびんきょくは どこです。"], "explanation": "あそこ = over there (far from both speaker and listener)."},
    {"question": "A hotel room costs 8,000 yen. How do you say it?", "answer": "はちせんえん です。", "options": ["はちせんえん です。", "はっせんえん です。", "やせんえん です。", "はちじゅうえん です。"], "explanation": "8000 = はっせん (8=はっ before せん). Common Japanese number rule."},
    {"question": "You want to know if the pharmacy is near the hospital.", "answer": "やっきょくは びょういんの ちかくですか。", "options": ["やっきょくは びょういんの ちかくですか。", "やっきょくは びょういんに ちかいですか。", "やっきょくが びょういんの ちかくですか。", "やっきょくを びょういんの ちかくですか。"], "explanation": "Noun+の+ちかく = near the noun. AはBのちかくですか = Is A near B?"},
    {"question": "The convenience store is to the right of the station exit.", "answer": "コンビニは えきの でぐちの みぎです。", "options": ["コンビニは えきの でぐちの みぎです。", "コンビニは えきの ひだりの そとです。", "コンビニは えきに みぎに あります。", "コンビニが えきの みぎで あります。"], "explanation": "Nの+direction = to the [direction] of N. みぎ=right, ひだり=left."},
    {"question": "Asking 'Is there a bank nearby?'", "answer": "ちかくに ぎんこうが ありますか。", "options": ["ちかくに ぎんこうが ありますか。", "ちかくに ぎんこうは いますか。", "ちかくで ぎんこうが ありますか。", "ちかくを ぎんこうが ありますか。"], "explanation": "Location+に+Noun+が+あります = There is [thing] at [location]."},
    {"question": "You are at the station. How do you say 'I am here (at the station)'?", "answer": "えきに います。", "options": ["えきに います。", "えきに あります。", "えきで います。", "えきが います。"], "explanation": "います = exists (living things). あります = exists (objects). Use います for yourself."},
    {"question": "The hospital is between the park and the bank.", "answer": "びょういんは こうえんと ぎんこうの あいだです。", "options": ["びょういんは こうえんと ぎんこうの あいだです。", "びょういんは こうえんか ぎんこうの あいだです。", "びょういんを こうえんと ぎんこうで あいだです。", "びょういんが こうえんと ぎんこうに あいだです。"], "explanation": "AとBのあいだ = between A and B."},
    {"question": "A customer asks where the fitting room is. You point to the left.", "answer": "ひだりに あります。", "options": ["ひだりに あります。", "ひだりに います。", "ひだりで あります。", "ひだりが あります。"], "explanation": "ひだり = left. に+あります = exists at that location."},
    {"question": "Asking the price of the room per night at a hotel.", "answer": "ひとばん いくらですか。", "options": ["ひとばん いくらですか。", "ひとつ いくらですか。", "いっぱく いくらですか。", "ひとばんは なんえんですか。"], "explanation": "ひとばん = one night. いくら = how much. Both いっぱく and ひとばん are natural."},
]

# ── Ch04: 毎日何時に起きますか ────────────────────────────────────────────

ch04_grammar_add = [
    {"question": "まいあさ 7じ_____ おきます。(I wake up at 7 every morning.)", "answer": "に", "options": ["に", "は", "で", "が"], "explanation": "Time+に = at [time]. に marks specific time point."},
    {"question": "としょかんは なんじから なんじ_____ あいていますか。(What hours is the library open?)", "answer": "まで", "options": ["まで", "から", "に", "で"], "explanation": "から〜まで = from〜to. まで = until/up to."},
    {"question": "きのう べんきょう _____。(I didn't study yesterday.)", "answer": "しませんでした", "options": ["しませんでした", "しません", "しました", "します"], "explanation": "〜ませんでした = did not do (past negative)."},
    {"question": "ごぜん 9じから ごご 5じ_____ はたらきます。(I work from 9am to 5pm.)", "answer": "まで", "options": ["まで", "から", "に", "まで に"], "explanation": "から〜まで = from ~ to (time range)."},
    {"question": "やすみは なんようびですか。_____ ようびです。(What day is your day off? It is Sunday.)", "answer": "にちようび", "options": ["にちようび", "もくようび", "かようび", "すいようび"], "explanation": "にちようび = Sunday. Days: 月火水木金土日."},
    {"question": "まいばん 12じごろ _____。(I sleep at around midnight every night.)", "answer": "ねます", "options": ["ねます", "おきます", "たべます", "のみます"], "explanation": "ねます = to sleep. ごろ = around (approximate time)."},
    {"question": "でんしゃは 3じ_____ きます。(The train comes at 3 o'clock.)", "answer": "に", "options": ["に", "で", "が", "は"], "explanation": "Specific time+に. でんしゃ = train, きます = to come."},
    {"question": "ひるごはんは ___ じかんぐらい たべますか。(About how long do you eat lunch?)", "answer": "どのくらい", "options": ["どのくらい", "なんじ", "いつ", "なんようび"], "explanation": "どのくらい = how long/how much. Used for duration."},
    {"question": "かいぎは ごご 2じから _____。(The meeting starts from 2pm.)", "answer": "から", "options": ["から", "まで", "に", "で"], "explanation": "Time+から = from [time]. Starting point of action."},
]

ch04_examples_add = [
    {"question": "Someone asks what time you wake up. You say 6:30am.", "answer": "まいあさ 6じはんに おきます。", "options": ["まいあさ 6じはんに おきます。", "まいあさ 6じはんで おきます。", "まいあさ 6じはんが おきます。", "まいあさ 6じはんは おきます。"], "explanation": "Time+に+verb. じはん = half past (30 min)."},
    {"question": "You want to say 'I go to bed at 11pm every night.'", "answer": "まいばん 11じに ねます。", "options": ["まいばん 11じに ねます。", "まいばん 11じで ねます。", "まいばん 11じは ねます。", "まいばん 11じを ねます。"], "explanation": "まいばん = every night. 11じ = 11 o'clock. に = at."},
    {"question": "The store opens from 10am to 9pm. How do you say it?", "answer": "10じから 9じまで あいています。", "options": ["10じから 9じまで あいています。", "10じに 9じまで あいています。", "10じから 9じに あいています。", "10じまで 9じから あいています。"], "explanation": "から〜まで = from〜to. あいています = is open."},
    {"question": "You want to ask 'What time does the class start?'", "answer": "じゅぎょうは なんじに はじまりますか。", "options": ["じゅぎょうは なんじに はじまりますか。", "じゅぎょうは いつに はじまりますか。", "じゅぎょうは なんようびに はじまりますか。", "じゅぎょうは なんじで はじまりますか。"], "explanation": "なんじに = at what time. はじまります = starts."},
    {"question": "You didn't go to school yesterday.", "answer": "きのう がっこうに いきませんでした。", "options": ["きのう がっこうに いきませんでした。", "きのう がっこうに いきません。", "きのう がっこうに いきました。", "きのう がっこうで いきませんでした。"], "explanation": "〜ませんでした = did not (past negative). きのう = yesterday."},
    {"question": "How do you say 'I usually eat breakfast at 7am'?", "answer": "たいてい あさごはんを 7じに たべます。", "options": ["たいてい あさごはんを 7じに たべます。", "よく あさごはんが 7じで たべます。", "いつも あさごはんを 7じは たべます。", "たいてい あさごはんに 7じを たべます。"], "explanation": "たいてい = usually. を marks the object eaten. に marks time."},
    {"question": "Asking what day of the week Japanese class is:", "answer": "にほんごの じゅぎょうは なんようびですか。", "options": ["にほんごの じゅぎょうは なんようびですか。", "にほんごの じゅぎょうは なんじですか。", "にほんごの じゅぎょうは いつですか。", "にほんごの じゅぎょうは どこですか。"], "explanation": "なんようび = what day of the week."},
    {"question": "'I work from Monday to Friday.' How do you say it?", "answer": "げつようびから きんようびまで はたらきます。", "options": ["げつようびから きんようびまで はたらきます。", "げつようびに きんようびまで はたらきます。", "げつようびから きんようびに はたらきます。", "げつようびまで きんようびから はたらきます。"], "explanation": "Day+から〜Day+まで = from [day] to [day]."},
    {"question": "Someone asks what you did last night. You studied Japanese.", "answer": "きのうの よる にほんごを べんきょうしました。", "options": ["きのうの よる にほんごを べんきょうしました。", "きのうの よる にほんごに べんきょうしました。", "きのうの よる にほんごが べんきょうしました。", "きのうの よる にほんごで べんきょうしました。"], "explanation": "を marks the object studied. べんきょうしました = studied."},
    {"question": "Saying 'The supermarket closes at 10pm.'", "answer": "スーパーは よる 10じに しまります。", "options": ["スーパーは よる 10じに しまります。", "スーパーは よる 10じで しまります。", "スーパーは よる 10じから しまります。", "スーパーは よる 10じまで しまります。"], "explanation": "しまります = closes. に marks the specific time."},
    {"question": "Asking 'How many hours do you sleep?'", "answer": "なんじかん ねますか。", "options": ["なんじかん ねますか。", "なんじ ねますか。", "いつ ねますか。", "どのくらい ねますか。"], "explanation": "なんじかん = how many hours. Counter for hours duration."},
    {"question": "You usually go to the gym on Saturdays.", "answer": "たいてい どようびに ジムに いきます。", "options": ["たいてい どようびに ジムに いきます。", "たいてい どようびで ジムで いきます。", "たいてい どようびを ジムを いきます。", "たいてい どようびは ジムに いきます。"], "explanation": "Day+に for specific day. Destination+に+いきます = go to ~."},
]

# ── Ch05: 誕生日はいつですか ──────────────────────────────────────────────

ch05_grammar_add = [
    {"question": "たんじょうびは _____ですか。(When is your birthday?)", "answer": "いつ", "options": ["いつ", "なに", "だれ", "どこ"], "explanation": "いつ = when. Used for time/date questions."},
    {"question": "こどもの ひは 5がつ _____ にちです。(Children's Day is May 5th.)", "answer": "いつ", "options": ["いつか", "ついたち", "はつか", "みっか"], "explanation": "5日 = いつか (irregular date reading). Dates 1-10 have special readings."},
    {"question": "にほんの おしょうがつは _____がつです。(Japanese New Year is in January.)", "answer": "いち", "options": ["いち", "に", "さん", "し"], "explanation": "1月 = いちがつ. Months are number+がつ."},
    {"question": "きょうは _____ようびですか。(What day of the week is today?)", "answer": "なん", "options": ["なん", "なに", "どの", "いつ"], "explanation": "なんようび = what day of the week."},
    {"question": "3がつ _____ にちは ひなまつりです。(March 3rd is Girls' Day.)", "answer": "みっか", "options": ["みっか", "さんにち", "みか", "さんか"], "explanation": "3日 = みっか (special irregular reading for the 3rd)."},
    {"question": "やすみは _____がつ から _____がつ までですか。(What months is the vacation?)", "answer": "なん / なん", "options": ["なん / なん", "いつ / いつ", "なに / なに", "どれ / どれ"], "explanation": "なんがつ = what month. Counter がつ with question word なん."},
    {"question": "_____ にちが ミーティングですか。(What date is the meeting?)", "answer": "なん", "options": ["なん", "いつ", "どの", "なに"], "explanation": "なんにち = what day of the month (date number)."},
    {"question": "たなかさんの たんじょうびは _____ ですか。—— 4がつ 14にちです。", "answer": "いつ", "options": ["いつ", "なに", "どこ", "どれ"], "explanation": "いつ = when. たんじょうび = birthday."},
]

ch05_examples_add = [
    {"question": "Someone asks your birthday. You were born on July 15th.", "answer": "7がつ 15にちです。", "options": ["7がつ 15にちです。", "7がつ じゅうごにちです。", "しちがつ 15にちです。", "7がつ じゅうごかです。"], "explanation": "Month+がつ+date+にち. 15日 = じゅうごにち (regular reading from 11 onwards)."},
    {"question": "You want to ask someone when their birthday is.", "answer": "たんじょうびは いつですか。", "options": ["たんじょうびは いつですか。", "たんじょうびは なんですか。", "たんじょうびは どこですか。", "たんじょうびは なんにちですか。"], "explanation": "いつ = when. General time/date question."},
    {"question": "Today is the 1st of March. How do you say the date?", "answer": "3がつ ついたちです。", "options": ["3がつ ついたちです。", "3がつ いちにちです。", "さんがつ ひとつです。", "みがつ ついたちです。"], "explanation": "1日 = ついたち (irregular). 3月 = さんがつ."},
    {"question": "'My birthday is February 14th.' How do you say it?", "answer": "わたしの たんじょうびは にがつ じゅうよっかです。", "options": ["わたしの たんじょうびは にがつ じゅうよっかです。", "わたしの たんじょうびは にがつ じゅうよにちです。", "わたしの たんじょうびは にがつ じゅうよかです。", "わたしの たんじょうびは ふたがつ じゅうよにちです。"], "explanation": "14日 = じゅうよっか (irregular). 2月 = にがつ."},
    {"question": "Asking 'What month does school start?'", "answer": "がっこうは なんがつに はじまりますか。", "options": ["がっこうは なんがつに はじまりますか。", "がっこうは いつに はじまりますか。", "がっこうは なんにちに はじまりますか。", "がっこうは なんようびに はじまりますか。"], "explanation": "なんがつ = what month. に marks time of action."},
    {"question": "Japan's national holiday 'Culture Day' is November 3rd.", "answer": "ぶんかの ひは じゅういちがつ みっかです。", "options": ["ぶんかの ひは じゅういちがつ みっかです。", "ぶんかの ひは じゅういちがつ さんにちです。", "ぶんかの ひは じゅうひとがつ みっかです。", "ぶんかの ひは いちいちがつ みっかです。"], "explanation": "11月 = じゅういちがつ. 3日 = みっか."},
    {"question": "You want to write August 20th in Japanese.", "answer": "はちがつ はつか", "options": ["はちがつ はつか", "はちがつ にじゅうにち", "やがつ はつか", "はちがつ はつにち"], "explanation": "20日 = はつか (irregular). 8月 = はちがつ."},
    {"question": "Asking 'What day of the week is Christmas this year?'", "answer": "ことしの クリスマスは なんようびですか。", "options": ["ことしの クリスマスは なんようびですか。", "ことしの クリスマスは いつようびですか。", "ことしの クリスマスは なんにちですか。", "ことしの クリスマスは なんがつですか。"], "explanation": "なんようび = what day of the week. ことし = this year."},
    {"question": "The exam is on the 10th of next month.", "answer": "しけんは らいげつの とおかです。", "options": ["しけんは らいげつの とおかです。", "しけんは らいげつの じゅうにちです。", "しけんは らいげつの じゅっかです。", "しけんは らいげつの とかです。"], "explanation": "10日 = とおか (irregular). らいげつ = next month."},
    {"question": "Wishing someone a happy birthday:", "answer": "たんじょうび おめでとうございます。", "options": ["たんじょうび おめでとうございます。", "たんじょうびに ありがとうございます。", "たんじょうびは いいですね。", "たんじょうびを おめでとうさまです。"], "explanation": "〜おめでとうございます = Congratulations on ~. Standard birthday wish."},
    {"question": "Golden Week in Japan is in May. Asking which dates:", "answer": "ゴールデンウィークは なんにちから なんにちまでですか。", "options": ["ゴールデンウィークは なんにちから なんにちまでですか。", "ゴールデンウィークは いつから いつまでですか。", "ゴールデンウィークは なんがつから なんがつまでですか。", "ゴールデンウィークは なんようびから なんようびまでですか。"], "explanation": "なんにちからなんにちまで = from what date to what date."},
    {"question": "The semester ends on March 31st.", "answer": "がっきは さんがつ さんじゅういちにちに おわります。", "options": ["がっきは さんがつ さんじゅういちにちに おわります。", "がっきは さんがつ さんじゅうにちに おわります。", "がっきは みがつ さんじゅういちにちに おわります。", "がっきは さんがつ みそかに おわります。"], "explanation": "31日 = さんじゅういちにち. さんがつ = March. おわります = ends."},
]

# ── Ch06: 富士山に登りましょう ────────────────────────────────────────────

ch06_grammar_add = [
    {"question": "いっしょに えいがを み _____か。(Shall we watch a movie together?)", "answer": "ませんか", "options": ["ませんか", "ましょうか", "ませんね", "ましょうね"], "explanation": "〜ませんか = Shall we ~? / Would you like to ~? (invitation)"},
    {"question": "A: 9じに ロビーで あいましょう。B: _____、そうしましょう。", "answer": "ええ", "options": ["ええ", "いいえ", "ちがいます", "どうぞ"], "explanation": "ええ = yes (informal/conversational). そうしましょう = let's do that."},
    {"question": "でんしゃ_____ ひろしままで いきます。(I go to Hiroshima by train.)", "answer": "で", "options": ["で", "に", "を", "から"], "explanation": "で marks means of transport: でんしゃで = by train."},
    {"question": "きっぷを _____ ください。(Please buy a ticket.)", "answer": "かって", "options": ["かって", "かいて", "かって", "のって"], "explanation": "かう → かって (て-form of かう: buy). 〜てください = please do ~."},
    {"question": "バスに _____。(Please get on the bus.)", "answer": "のって ください", "options": ["のって ください", "おりて ください", "あるいて ください", "はいって ください"], "explanation": "のります → のって = get on (て-form). のってください = please board."},
    {"question": "くうこうまで どうやって いきますか。——でんしゃ _____ いきます。", "answer": "で", "options": ["で", "に", "を", "から"], "explanation": "Transport+で = by [transport]. でんしゃで = by train."},
    {"question": "タクシー_____ いきましょうか。(Shall we go by taxi?)", "answer": "で", "options": ["で", "に", "が", "を"], "explanation": "タクシーで = by taxi. で = means/method."},
    {"question": "てを _____ から、しょくじしましょう。(After washing hands, let's eat.)", "answer": "あらって", "options": ["あらって", "あらいて", "あらって", "あらって"], "explanation": "あらう → あらって (て-form: wash hands). て-form connects actions."},
]

ch06_examples_add = [
    {"question": "You want to invite a friend to go to a concert.", "answer": "コンサートに いきませんか。", "options": ["コンサートに いきませんか。", "コンサートに いきましょうか。", "コンサートに いきませんね。", "コンサートを いきますか。"], "explanation": "〜ませんか = Wouldn't you like to ~? (invitation). More polite than ましょう."},
    {"question": "Suggesting 'Let's take the subway.'", "answer": "ちかてつで いきましょう。", "options": ["ちかてつで いきましょう。", "ちかてつに いきましょう。", "ちかてつが いきましょう。", "ちかてつを いきましょう。"], "explanation": "ちかてつ = subway. で = by (transport). ましょう = let's."},
    {"question": "A friend suggests going to karaoke. You agree enthusiastically.", "answer": "ええ、いきましょう！", "options": ["ええ、いきましょう！", "いいえ、いきません。", "ちょっと…。", "どうぞ。"], "explanation": "ええ = yes (casual). ましょう = let's (agreement)."},
    {"question": "How long does it take to get to the station?", "answer": "えきまで どのくらい かかりますか。", "options": ["えきまで どのくらい かかりますか。", "えきに どのくらい いきますか。", "えきで どれくらい なりますか。", "えきから どのくらい かかりますか。"], "explanation": "〜まで どのくらい かかりますか = How long does it take to ~? かかります = it takes."},
    {"question": "Saying 'It takes about 20 minutes by bus.'", "answer": "バスで にじゅっぷんぐらい かかります。", "options": ["バスで にじゅっぷんぐらい かかります。", "バスに にじゅっぷんぐらい かかります。", "バスが にじゅっぷんぐらい かかります。", "バスで にじゅっぷんごろ かかります。"], "explanation": "Transport+で+time+ぐらい+かかります = it takes about [time] by [transport]. ぐらい = approximately."},
    {"question": "Asking someone how they come to work:", "answer": "まいにち どうやって かいしゃに きますか。", "options": ["まいにち どうやって かいしゃに きますか。", "まいにち なんで かいしゃに きますか。", "まいにち どれで かいしゃに きますか。", "まいにち どこで かいしゃに きますか。"], "explanation": "どうやって = how (method). なんで is also acceptable in casual speech."},
    {"question": "Saying 'I came to Japan by plane.'", "answer": "ひこうきで にほんに きました。", "options": ["ひこうきで にほんに きました。", "ひこうきに にほんに きました。", "ひこうきを にほんに きました。", "ひこうきが にほんに きました。"], "explanation": "ひこうき = airplane. で = by (transport). に = destination."},
    {"question": "Proposing to meet at the station at 3pm.", "answer": "えきで 3じに あいましょう。", "options": ["えきで 3じに あいましょう。", "えきに 3じで あいましょう。", "えきを 3じは あいましょう。", "えきが 3じに あいましょう。"], "explanation": "Place+で = at place. Time+に. あいましょう = let's meet."},
    {"question": "You traveled from Tokyo to Osaka. How long did it take by shinkansen?", "answer": "しんかんせんで 2じかんぐらい かかりました。", "options": ["しんかんせんで 2じかんぐらい かかりました。", "しんかんせんに 2じかんぐらい かかりました。", "しんかんせんで 2じかんごろ かかりました。", "しんかんせんが 2じかんぐらい かかりました。"], "explanation": "しんかんせん = bullet train. で = by. ぐらい = approximately. かかりました = it took."},
    {"question": "Politely declining an invitation to karaoke.", "answer": "すみません、ちょっと…。", "options": ["すみません、ちょっと…。", "いいえ、いきません。", "けっこうです。", "だめです。"], "explanation": "ちょっと… (trailing off) is the natural way to politely decline in Japanese. Direct refusals sound rude."},
    {"question": "Suggesting taking a taxi because it's raining.", "answer": "あめですから、タクシーで いきましょう。", "options": ["あめですから、タクシーで いきましょう。", "あめですから、タクシーに いきましょう。", "あめですが、タクシーで いきましょう。", "あめなので、タクシーを いきましょう。"], "explanation": "〜から = because. あめ = rain. タクシーで = by taxi."},
    {"question": "Asking which platform the train to Kyoto departs from.", "answer": "きょうと いきの でんしゃは なんばんせんですか。", "options": ["きょうと いきの でんしゃは なんばんせんですか。", "きょうと いきの でんしゃは どこですか。", "きょうと いきの でんしゃは なんじですか。", "きょうと いきの でんしゃは なんですか。"], "explanation": "なんばんせん = which platform number. いき = bound for."},
]

# ── Ch07: い-adjectives ───────────────────────────────────────────────────

ch07_grammar_add = [
    {"question": "このレストランの りょうりは _____ですか。(Is the food at this restaurant good?)", "answer": "おいしい", "options": ["おいしい", "たかい", "やすい", "ひろい"], "explanation": "おいしい = delicious. い-adjective directly before です."},
    {"question": "きょうは _____くない ですね。(It's not cold today, is it?)", "answer": "さむ", "options": ["さむ", "あつ", "すず", "あたた"], "explanation": "さむい → さむくない. Negative of い-adj: drop い, add くない."},
    {"question": "このかばんは _____くて じょうぶです。(This bag is light and durable.)", "answer": "かる", "options": ["かる", "おも", "おお", "ちい"], "explanation": "かるい = light (weight). て-form of い-adj: drop い, add くて."},
    {"question": "あのビルは _____です。(That building is tall.)", "answer": "たかい", "options": ["たかい", "ひくい", "せまい", "ひろい"], "explanation": "たかい = tall/high. ひくい = low. Common spatial adjective."},
    {"question": "えいがは _____ なかった。(The movie was not interesting.) (plain past negative)", "answer": "おもしろく", "options": ["おもしろく", "おもしろい", "おもしろくて", "おもしろかった"], "explanation": "おもしろい → おもしろくなかった (plain past negative: drop い, add くなかった)."},
    {"question": "りょうりは おいし_____ です。(The food is delicious.)", "answer": "い", "options": ["い", "く", "かった", "くない"], "explanation": "おいしい+です: no change to adjective before です in affirmative present."},
    {"question": "やちんは _____くなりました。(The rent became cheap.)", "answer": "やす", "options": ["やす", "たか", "おお", "ちい"], "explanation": "やすい = cheap. 〜くなりました = became ~. Change of state."},
    {"question": "この テストは _____くて、みんな とれませんでした。(This test was hard, nobody passed.)", "answer": "むずかし", "options": ["むずかし", "やさし", "おもしろ", "たのし"], "explanation": "むずかしい = difficult. て-form: むずかしくて (connecting reason)."},
    {"question": "にほんの なつは _____いですね。(Japanese summer is hot, isn't it!)", "answer": "あつ", "options": ["あつ", "さむ", "すず", "あたた"], "explanation": "あつい = hot. ですね = isn't it (seeking agreement)."},
    {"question": "この へやは _____くて きれいです。(This room is bright and clean.)", "answer": "あかる", "options": ["あかる", "くら", "せま", "うるさ"], "explanation": "あかるい = bright. て-form connects two adjective descriptions."},
]

ch07_examples_add = [
    {"question": "A friend asks how your new apartment is. It is small but cheap.", "answer": "せまいですが、やすいです。", "options": ["せまいですが、やすいです。", "せまくて、やすいです。", "せまいですから、やすいです。", "せまいので、やすいです。"], "explanation": "〜が = but (contrast). せまい = small/narrow, やすい = cheap."},
    {"question": "You want to say 'Mt Fuji is tall and beautiful.'", "answer": "ふじさんは たかくて きれいです。", "options": ["ふじさんは たかくて きれいです。", "ふじさんは たかいで きれいです。", "ふじさんは たかいですが きれいです。", "ふじさんは たかく きれいです。"], "explanation": "い-adj+くて links to the next description. きれい is a な-adj so no change."},
    {"question": "How do you say 'Yesterday's homework was easy'?", "answer": "きのうの しゅくだいは やさしかったです。", "options": ["きのうの しゅくだいは やさしかったです。", "きのうの しゅくだいは やさしいでした。", "きのうの しゅくだいは やさしくなかったです。", "きのうの しゅくだいは やさしいです。"], "explanation": "Past of い-adj: drop い, add かったです. やさしい→やさしかった."},
    {"question": "The new phone is expensive but has good features.", "answer": "あたらしい スマホは たかいですが、きのうが いいです。", "options": ["あたらしい スマホは たかいですが、きのうが いいです。", "あたらしい スマホは たかくて、きのうが いいです。", "あたらしい スマホは たかいので、きのうが いいです。", "あたらしい スマホは たかいから、きのうが いいです。"], "explanation": "〜が (but) shows contrast. たかい = expensive, きのう = features."},
    {"question": "Saying 'This bag is not heavy.'", "answer": "このかばんは おもくないです。", "options": ["このかばんは おもくないです。", "このかばんは おもいないです。", "このかばんは おもじゃないです。", "このかばんは おもくありません。"], "explanation": "Negative: おもい → おもくない(です). Both おもくないです and おもくありません are correct."},
    {"question": "Your friend's cooking is delicious. How do you compliment it?", "answer": "おいしいですね！", "options": ["おいしいですね！", "おいしかったです！", "おいしくないですね！", "おいしいじゃないですか！"], "explanation": "おいしい+ですね = It's delicious, isn't it! ね seeks the listener's agreement."},
    {"question": "Tokyo is a big and lively city.", "answer": "とうきょうは おおきくて にぎやかな まちです。", "options": ["とうきょうは おおきくて にぎやかな まちです。", "とうきょうは おおきいで にぎやかな まちです。", "とうきょうは おおきくて にぎやかまちです。", "とうきょうは おおきいと にぎやかな まちです。"], "explanation": "おおきい(い-adj)→おおきくて. にぎやか(な-adj)+な before noun."},
    {"question": "How do you say 'Last year's winter was very cold'?", "answer": "きょねんの ふゆは とても さむかったです。", "options": ["きょねんの ふゆは とても さむかったです。", "きょねんの ふゆは とても さむいでした。", "きょねんの ふゆは とても さむくないです。", "きょねんの ふゆは とても さむいです。"], "explanation": "Past: さむい→さむかった. とても = very. きょねん = last year."},
    {"question": "Describing a restaurant: 'The food is good but the service is slow.'", "answer": "りょうりは おいしいですが、サービスが おそいです。", "options": ["りょうりは おいしいですが、サービスが おそいです。", "りょうりは おいしくて、サービスが おそいです。", "りょうりは おいしいので、サービスが おそいです。", "りょうりは おいしいから、サービスが おそいです。"], "explanation": "が = but (contrast between two clauses). おそい = slow."},
    {"question": "The room temperature is just right (not hot, not cold).", "answer": "へやの おんどは あつくも さむくも ありません。", "options": ["へやの おんどは あつくも さむくも ありません。", "へやの おんどは あつくて さむくないです。", "へやの おんどは あつくないし さむくないです。", "へやの おんどは あついでも さむいでも ない。"], "explanation": "〜くも〜くもありません = neither ~ nor ~. Double negative with も."},
    {"question": "The movie was long but very interesting.", "answer": "えいがは ながかったですが、とても おもしろかったです。", "options": ["えいがは ながかったですが、とても おもしろかったです。", "えいがは ながいでしたが、とても おもしろいでした。", "えいがは ながくて、とても おもしろかったです。", "えいがは ながかったので、とても おもしろかったです。"], "explanation": "Both adjectives in past tense (〜かった). が = but (contrast)."},
    {"question": "How do you ask 'Is Japanese difficult?'", "answer": "にほんごは むずかしいですか。", "options": ["にほんごは むずかしいですか。", "にほんごは むずかしくですか。", "にほんごは むずかしかったですか。", "にほんごは むずかしくないですか。"], "explanation": "い-adj+ですか = Is it [adjective]? Simple present question."},
]

# ── Ch08: まちをあるきます ────────────────────────────────────────────────

ch08_grammar_add = [
    {"question": "ここで しゃしんを とっても _____ですか。(May I take photos here?)", "answer": "いい", "options": ["いい", "わるい", "だめ", "いけない"], "explanation": "〜てもいいですか = Is it okay if I ~? Permission request. いい = good/OK."},
    {"question": "ここで タバコを すっては _____。(You must not smoke here.)", "answer": "いけません", "options": ["いけません", "いいです", "だいじょうぶです", "かまいません"], "explanation": "〜てはいけません = must not / is not allowed to."},
    {"question": "エアコンを _____ ください。(Please turn off the AC.)", "answer": "けして", "options": ["けして", "つけて", "あけて", "しめて"], "explanation": "けす = to turn off. て-form: けして. 〜てください = please do ~."},
    {"question": "じしょを つかっても _____か。(May I use a dictionary?)", "answer": "いい", "options": ["いい", "だめ", "わるい", "いけない"], "explanation": "〜てもいいですか = may I ~? Response: いいですよ or だめです."},
    {"question": "ここに くるまを とめては _____。(You may not park here.)", "answer": "いけません", "options": ["いけません", "かまいません", "いいです", "だいじょうぶです"], "explanation": "〜てはいけません = prohibited / must not."},
    {"question": "すみません、ちょっと _____ていただけませんか。(Excuse me, could you wait a moment?)", "answer": "まっ", "options": ["まっ", "みて", "きて", "いって"], "explanation": "まつ → まって (て-form: wait). 〜ていただけませんか = Could you please ~? (very polite)"},
    {"question": "かばんを _____もいいですか。(May I open the bag?)", "answer": "あけて", "options": ["あけて", "しめて", "もって", "おいて"], "explanation": "あける = to open. て-form: あけて. てもいいですか = permission request."},
    {"question": "ここに ゴミを すては _____。(Don't throw trash here.)", "answer": "いけません", "options": ["いけません", "いいです", "かまいません", "だいじょうぶ"], "explanation": "〜てはいけません = prohibition. ゴミを すてる = to throw away trash."},
    {"question": "でんわを かけても _____か。—— はい、どうぞ。(May I make a phone call? — Please go ahead.)", "answer": "いい", "options": ["いい", "わるい", "だめ", "いけない"], "explanation": "いいですか = Is it okay? どうぞ = Please go ahead / be my guest."},
    {"question": "しずかに _____ください。(Please be quiet.)", "answer": "して", "options": ["して", "しなくて", "しないで", "します"], "explanation": "しずかにする = to be quiet. て-form: しずかにして. 〜てください = please do ~."},
]

ch08_examples_add = [
    {"question": "You want to ask if you can sit next to someone on a train.", "answer": "ここに すわっても いいですか。", "options": ["ここに すわっても いいですか。", "ここを すわっても いいですか。", "ここで すわっても いいですか。", "ここが すわっても いいですか。"], "explanation": "に marks location for sitting (すわる). てもいいですか = may I."},
    {"question": "In a museum: 'Please do not touch the exhibits.'", "answer": "てんじひんに さわらないで ください。", "options": ["てんじひんに さわらないで ください。", "てんじひんを さわっては いけません。", "てんじひんが さわらないで ください。", "てんじひんで さわらないで ください。"], "explanation": "〜ないでください = please don't ~. さわる = to touch. Both forms are correct."},
    {"question": "Asking permission to open the window in a classroom.", "answer": "まどを あけても いいですか。", "options": ["まどを あけても いいですか。", "まどが あけても いいですか。", "まどで あけても いいですか。", "まどに あけても いいですか。"], "explanation": "を marks the object (window). あける = open. てもいいですか = may I."},
    {"question": "The teacher says 'You don't need to submit the report today.'", "answer": "きょう レポートを ださなくても いいです。", "options": ["きょう レポートを ださなくても いいです。", "きょう レポートを だしては いけません。", "きょう レポートを だしても いいです。", "きょう レポートを ださないで ください。"], "explanation": "〜なくてもいいです = don't need to do ~. Absence of obligation."},
    {"question": "Politely asking someone to speak more slowly.", "answer": "もっと ゆっくり はなして いただけませんか。", "options": ["もっと ゆっくり はなして いただけませんか。", "もっと ゆっくり はなして ください。", "もっと ゆっくり はなしても いいですか。", "もっと ゆっくり はなしては いけません。"], "explanation": "〜ていただけませんか = Could you please ~? Most polite request form."},
    {"question": "Sign at a coffee shop: 'Outside food and drink prohibited.'", "answer": "もちこみは おことわりします。", "options": ["もちこみは おことわりします。", "もちこんでは いけません。", "もちこまないで ください。", "もちこんでも いいです。"], "explanation": "おことわりします = we decline/prohibit (formal sign language). もちこみ = bringing in (outside items)."},
    {"question": "You're tired. Asking permission to go home early.", "answer": "はやく かえっても いいですか。", "options": ["はやく かえっても いいですか。", "はやく かえっては いけませんか。", "はやく かえらないで ください。", "はやく かえって ください。"], "explanation": "かえる → かえって (て-form). てもいいですか = may I. はやく = early."},
    {"question": "The sign says 'No photography allowed.'", "answer": "しゃしん さつえい きんし。", "options": ["しゃしん さつえい きんし。", "しゃしんを とっても いいです。", "しゃしんを とらないで ください。", "しゃしんを とっては いけません。"], "explanation": "きんし = prohibited (noun, used on signs). The full sentence would be: しゃしんさつえいをしてはいけません。"},
    {"question": "You need to leave the library. Asking if you can borrow the book for a week.", "answer": "この ほんを いっしゅうかん かりても いいですか。", "options": ["この ほんを いっしゅうかん かりても いいですか。", "この ほんが いっしゅうかん かりても いいですか。", "この ほんで いっしゅうかん かりても いいですか。", "この ほんに いっしゅうかん かりても いいですか。"], "explanation": "を = object (book). いっしゅうかん = one week. かりる = to borrow."},
    {"question": "Rules say you must wear a mask inside.", "answer": "なかでは マスクを して ください。", "options": ["なかでは マスクを して ください。", "なかでは マスクを しては いけません。", "なかでは マスクを しても いいです。", "なかでは マスクを しなくても いいです。"], "explanation": "〜てください = please do ~. マスクをする = to wear a mask. で = inside."},
    {"question": "Asking if it's okay NOT to wear a uniform on Fridays.", "answer": "きんようびは せいふくを きなくても いいですか。", "options": ["きんようびは せいふくを きなくても いいですか。", "きんようびは せいふくを きても いいですか。", "きんようびは せいふくを きては いけませんか。", "きんようびは せいふくを きないで ください。"], "explanation": "〜なくてもいいですか = Is it okay if I don't ~? せいふく = uniform, きる = to wear."},
    {"question": "In a library, reminding someone: 'Please don't use your phone.'", "answer": "けいたいを つかわないで ください。", "options": ["けいたいを つかわないで ください。", "けいたいを つかっても いいです。", "けいたいを つかっては いけません。", "けいたいを つかっても いいですか。"], "explanation": "〜ないでください = Please refrain from ~. Natural library announcement form."},
]

# ── Apply all patches ──────────────────────────────────────────────────────

print("Patching Ch01–Ch08 grammar and examples...")

d, p = load(1, 'grammar');   patch(d, p, ch01_grammar_add)
d, p = load(1, 'examples');  patch(d, p, ch01_examples_add)
d, p = load(2, 'grammar');   patch(d, p, ch02_grammar_add)
d, p = load(2, 'examples');  patch(d, p, ch02_examples_add)
d, p = load(3, 'grammar');   patch(d, p, ch03_grammar_add)
d, p = load(3, 'examples');  patch(d, p, ch03_examples_add)
d, p = load(4, 'grammar');   patch(d, p, ch04_grammar_add)
d, p = load(4, 'examples');  patch(d, p, ch04_examples_add)
d, p = load(5, 'grammar');   patch(d, p, ch05_grammar_add)
d, p = load(5, 'examples');  patch(d, p, ch05_examples_add)
d, p = load(6, 'grammar');   patch(d, p, ch06_grammar_add)
d, p = load(6, 'examples');  patch(d, p, ch06_examples_add)
d, p = load(7, 'grammar');   patch(d, p, ch07_grammar_add)
d, p = load(7, 'examples');  patch(d, p, ch07_examples_add)
d, p = load(8, 'grammar');   patch(d, p, ch08_grammar_add)
d, p = load(8, 'examples');  patch(d, p, ch08_examples_add)

print("Done!")

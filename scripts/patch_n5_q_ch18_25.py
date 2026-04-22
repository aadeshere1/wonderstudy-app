"""
Patch N5 Ch18-25 grammar and examples files to reach 20 questions each.
Run:  python3 scripts/patch_n5_q_ch18_25.py
"""
import json, os

BASE = os.path.join(os.path.dirname(__file__), '..', 'data', 'classes', 'jlpt', 'n5')

def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

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

# ─────────────────────────────────────────────────────────────────────────────
# CH18  Taking/bringing things; giving reasons with から; invitations
# ─────────────────────────────────────────────────────────────────────────────
p = os.path.join(BASE, 'ch18-grammar.json'); d = load(p)
patch(d, p, [
    {"question": "あめ ___ 、かさをもっていきます。(It's raining, so I'll bring an umbrella.)", "answer": "だから", "options": ["だから", "でも", "けど", "のに"], "type": "multiple_choice"},
    {"question": "いそが ___ から、てつだえません。(I'm busy, so I can't help.)", "answer": "しい", "options": ["しい", "くて", "なくて", "じゃない"], "type": "multiple_choice"},
    {"question": "友だちを ___  いきます。(I'll take my friend along.)", "answer": "つれて", "options": ["つれて", "もって", "おくって", "みせて"], "type": "multiple_choice"},
    {"question": "かいものに行く ___ 、なにかかってきましょうか。(If you're going shopping, shall I buy something for you?)", "answer": "なら", "options": ["なら", "から", "ので", "けど"], "type": "multiple_choice"},
    {"question": "おみやげを ___  きました。(I brought a souvenir back.)", "answer": "もって", "options": ["もって", "つれて", "おくって", "かって"], "type": "multiple_choice"},
    {"question": "Which phrase means 'because it is cheap'?", "answer": "やすいから", "options": ["やすいから", "やすくて", "やすければ", "やすいのに"], "type": "multiple_choice"},
    {"question": "びょうき ___ 、がっこうをやすみます。(Because I'm sick, I'll be absent from school.)", "answer": "だから", "options": ["だから", "なので", "でも", "けど"], "type": "multiple_choice"},
    {"question": "もっていく means:", "answer": "to take (something) somewhere", "options": ["to take (something) somewhere", "to bring (something) here", "to send (something)", "to receive (something)"], "type": "multiple_choice"},
    {"question": "もってくる means:", "answer": "to bring (something) here", "options": ["to bring (something) here", "to take (something) there", "to carry (something)", "to drop (something)"], "type": "multiple_choice"},
    {"question": "パーティーに ___ ませんか。(Won't you come to the party?)", "answer": "き", "options": ["き", "いき", "おき", "でき"], "type": "multiple_choice"},
    {"question": "How do you invite someone saying 'Shall we go together?'", "answer": "いっしょに行きませんか。", "options": ["いっしょに行きませんか。", "いっしょに行きます。", "いっしょに行きたい。", "いっしょに行くかな。"], "type": "multiple_choice"},
    {"question": "つれていく is used when you take ___ somewhere.", "answer": "a person or animal", "options": ["a person or animal", "an object", "money", "a message"], "type": "multiple_choice"},
    {"question": "もっていく is used when you take ___ somewhere.", "answer": "an object", "options": ["an object", "a person", "an animal", "an idea"], "type": "multiple_choice"},
    {"question": "たのし ___ から、また来たいです。(Because it's fun, I want to come again.)", "answer": "い", "options": ["い", "くて", "かった", "じゃない"], "type": "multiple_choice"},
    {"question": "How do you say 'Because I have plans, I can't go'?", "answer": "よていがあるから、いけません。", "options": ["よていがあるから、いけません。", "よていがなくて、いけません。", "よていだから、いきます。", "よていがあれば、いきます。"], "type": "multiple_choice"},
])

p = os.path.join(BASE, 'ch18-examples.json'); d = load(p)
patch(d, p, [
    {"question": "A friend invites you to a party but you already have plans. Decline politely.", "answer": "すみません、よていがあるから、いけません。", "type": "short_answer"},
    {"question": "You're going to a friend's house and want to take a cake. How do you say this?", "answer": "ともだちのうちにケーキをもっていきます。", "type": "short_answer"},
    {"question": "How do you invite a friend to come along to the park?", "answer": "こうえんにいっしょに行きませんか。", "type": "short_answer"},
    {"question": "It's cold outside. What reason do you give for bringing a coat?", "answer": "さむいから、コートをもっていきます。", "type": "short_answer"},
    {"question": "You're returning from a trip and you bought a souvenir. How do you say 'I brought a souvenir'?", "answer": "おみやげをもってきました。", "type": "short_answer"},
    {"question": "How do you say 'I'll take my younger brother to the hospital'?", "answer": "おとうとをびょういんにつれていきます。", "type": "short_answer"},
    {"question": "Translate: 'Because it is interesting, I want to read this book.'", "answer": "おもしろいから、このほんをよみたいです。", "type": "short_answer"},
    {"question": "You're meeting someone for the first time. How do you accept their invitation to lunch?", "answer": "ぜひ、いっしょにたべましょう！", "type": "short_answer"},
    {"question": "How do you say 'Please bring your dictionary'?", "answer": "じしょをもってきてください。", "type": "short_answer"},
    {"question": "It's raining. How do you tell a friend to bring an umbrella?", "answer": "あめだから、かさをもってきてください。", "type": "short_answer"},
    {"question": "How do you say 'I'll take my dog for a walk'?", "answer": "いぬをさんぽにつれていきます。", "type": "short_answer"},
    {"question": "Your colleague forgot their lunch. How do you offer to bring it to them?", "answer": "もっていきましょうか。", "type": "short_answer"},
    {"question": "Translate: 'Because the movie is interesting, many people come.'", "answer": "えいががおもしろいから、ひとがたくさんきます。", "type": "short_answer"},
    {"question": "How do you ask 'Why did you come to Japan?'", "answer": "なぜ（どうして）にほんにきたんですか。", "type": "short_answer"},
    {"question": "You came to Japan to study Japanese. How do you explain your reason?", "answer": "日本語をべんきょうするために、日本にきました。", "type": "short_answer"},
    {"question": "How do you say 'I brought children to the park'?", "answer": "こどもをこうえんにつれていきました。", "type": "short_answer"},
    {"question": "Translate: 'Won't you go see a movie together this weekend?'", "answer": "こんしゅうまつ、いっしょにえいがを見にいきませんか。", "type": "short_answer"},
])

# ─────────────────────────────────────────────────────────────────────────────
# CH19  Past tense (でした / かったです / じゃなかったです); travel experience reports
# ─────────────────────────────────────────────────────────────────────────────
p = os.path.join(BASE, 'ch19-grammar.json'); d = load(p)
patch(d, p, [
    {"question": "きのうは ___ でした。(Yesterday was cold.)", "answer": "さむ", "options": ["さむ", "あつ", "しず", "たの"], "type": "multiple_choice"},
    {"question": "えいがはおもしろ ___ でしたか。(Was the movie interesting?)", "answer": "くなかった", "options": ["くなかった", "じゃなかった", "かった", "くない"], "type": "multiple_choice"},
    {"question": "Past negative of きれいです is:", "answer": "きれいじゃなかったです", "options": ["きれいじゃなかったです", "きれいくなかったです", "きれいなかったです", "きれいでなかったです"], "type": "multiple_choice"},
    {"question": "Past negative of おおきいです is:", "answer": "おおきくなかったです", "options": ["おおきくなかったです", "おおきじゃなかったです", "おおきなかったです", "おおきでなかったです"], "type": "multiple_choice"},
    {"question": "りょこうはどう ___ か。(How was the trip?)", "answer": "でした", "options": ["でした", "です", "だった", "ありました"], "type": "multiple_choice"},
    {"question": "The past tense of たのしいです is:", "answer": "たのしかったです", "options": ["たのしかったです", "たのしでした", "たのしいでした", "たのしくないです"], "type": "multiple_choice"},
    {"question": "The past tense of しずかです is:", "answer": "しずかでした", "options": ["しずかでした", "しずかかったです", "しずかくでした", "しずかいでした"], "type": "multiple_choice"},
    {"question": "おてんきはよ ___ ですか。(Was the weather good?)", "answer": "かった", "options": ["かった", "かったじゃない", "じゃなかった", "くなかった"], "type": "multiple_choice"},
    {"question": "ホテルはしずかじゃ ___ 。(The hotel was not quiet.)", "answer": "なかったです", "options": ["なかったです", "ありませんでした", "くなかったです", "なかった"], "type": "multiple_choice"},
    {"question": "How do you say 'The food was not delicious'?", "answer": "たべものはおいしくなかったです。", "options": ["たべものはおいしくなかったです。", "たべものはおいしじゃなかったです。", "たべものはおいしなかったです。", "たべものはおいしくないでした。"], "type": "multiple_choice"},
    {"question": "あそこのみせはやす ___ 。(That shop was cheap.)", "answer": "かったです", "options": ["かったです", "でした", "だったです", "くなかったです"], "type": "multiple_choice"},
    {"question": "How do you ask 'How was Osaka?'", "answer": "おおさかはどうでしたか。", "options": ["おおさかはどうでしたか。", "おおさかはなんでしたか。", "おおさかはいつでしたか。", "おおさかはどこでしたか。"], "type": "multiple_choice"},
    {"question": "むずかし ___ 、よくわかりませんでした。(It was difficult, so I didn't understand well.)", "answer": "かったから", "options": ["かったから", "いから", "なかったから", "でしたから"], "type": "multiple_choice"},
    {"question": "Past tense of いそがしいです:", "answer": "いそがしかったです", "options": ["いそがしかったです", "いそがしでした", "いそがしいでした", "いそがしくでした"], "type": "multiple_choice"},
    {"question": "How do you say 'It was not hot yesterday'?", "answer": "きのうはあつくなかったです。", "options": ["きのうはあつくなかったです。", "きのうはあつじゃなかったです。", "きのうはあつくないでした。", "きのうはあつでなかったです。"], "type": "multiple_choice"},
])

p = os.path.join(BASE, 'ch19-examples.json'); d = load(p)
patch(d, p, [
    {"question": "You visited Tokyo last week. Report: 'Tokyo was very lively.'", "answer": "とうきょうはとてもにぎやかでした。", "type": "short_answer"},
    {"question": "The food in Osaka was really delicious. How do you say this?", "answer": "おおさかのたべものはとてもおいしかったです。", "type": "short_answer"},
    {"question": "Your hotel room was small and not comfortable. Report this.", "answer": "ホテルのへやはせまくて、あまりよくなかったです。", "type": "short_answer"},
    {"question": "The trip was tiring. How do you say this?", "answer": "りょこうはつかれました。/ りょこうはたいへんでした。", "type": "short_answer"},
    {"question": "The weather was not good during the trip. How do you express this?", "answer": "りょこうのてんきはよくなかったです。", "type": "short_answer"},
    {"question": "How do you ask a friend 'Was the test difficult?'", "answer": "テストはむずかしかったですか。", "type": "short_answer"},
    {"question": "The museum was interesting but crowded. Report this.", "answer": "はくぶつかんはおもしろかったですが、こんでいました。", "type": "short_answer"},
    {"question": "Translate: 'The concert last night was wonderful.'", "answer": "ゆうべのコンサートはすばらしかったです。", "type": "short_answer"},
    {"question": "How do you say 'The restaurant was not cheap'?", "answer": "レストランはやすくなかったです。", "type": "short_answer"},
    {"question": "You met a famous person on your trip. How do you report: 'I met a famous person'?", "answer": "ゆうめいなひとにあいました。", "type": "short_answer"},
    {"question": "Translate: 'Was the Shinkansen fast?'", "answer": "しんかんせんははやかったですか。", "type": "short_answer"},
    {"question": "How do you reply 'Yes, it was very fast' to the above question?", "answer": "はい、とてもはやかったです。", "type": "short_answer"},
    {"question": "It was your first time in Japan and it was great. How do you express this?", "answer": "はじめての日本でしたが、とてもよかったです。", "type": "short_answer"},
    {"question": "The park was quiet and beautiful. Describe it in Japanese.", "answer": "こうえんはしずかできれいでした。", "type": "short_answer"},
    {"question": "How do you say 'I was not busy yesterday'?", "answer": "きのうはいそがしくなかったです。", "type": "short_answer"},
    {"question": "Ask a friend: 'Was the party fun?'", "answer": "パーティーはたのしかったですか。", "type": "short_answer"},
    {"question": "Your friend's birthday dinner was not expensive. How do you report this?", "answer": "たんじょうびのよるごはんはたかくなかったです。", "type": "short_answer"},
])

# ─────────────────────────────────────────────────────────────────────────────
# CH20  Directions; 〜て connecting movement; と conditional; ところに/まで
# ─────────────────────────────────────────────────────────────────────────────
p = os.path.join(BASE, 'ch20-grammar.json'); d = load(p)
patch(d, p, [
    {"question": "みぎに ___ てください。(Please turn right.)", "answer": "まがっ", "options": ["まがっ", "いっ", "もどっ", "すすん"], "type": "multiple_choice"},
    {"question": "かどをひだり ___ 曲がってください。(Turn left at the corner.)", "answer": "に", "options": ["に", "を", "で", "へ"], "type": "multiple_choice"},
    {"question": "まっすぐ行く ___ 、こうばんがあります。(If you go straight, there is a police box.)", "answer": "と", "options": ["と", "から", "ので", "から"], "type": "multiple_choice"},
    {"question": "えきのちか ___ にぎんこうがあります。(Near the station there is a bank.)", "answer": "く", "options": ["く", "に", "で", "を"], "type": "multiple_choice"},
    {"question": "ここから ___ ですか、ちかいですか。(From here, is it far or near?)", "answer": "とおい", "options": ["とおい", "ながい", "ひろい", "ふかい"], "type": "multiple_choice"},
    {"question": "How do you ask 'How do I get to the station?'", "answer": "えきへはどうやっていきますか。", "options": ["えきへはどうやっていきますか。", "えきはどこにありますか。", "えきまでなんぷんですか。", "えきはどうですか。"], "type": "multiple_choice"},
    {"question": "このみちをまっすぐ行っ ___ 、みぎにまがってください。(Go straight along this road, then turn right.)", "answer": "て", "options": ["て", "から", "ので", "と"], "type": "multiple_choice"},
    {"question": "えきのまえ ___ バスていがあります。(In front of the station there is a bus stop.)", "answer": "に", "options": ["に", "で", "を", "が"], "type": "multiple_choice"},
    {"question": "はしを ___ と、こうえんがあります。(If you cross the bridge, there is a park.)", "answer": "わたる", "options": ["わたる", "まがる", "すすむ", "もどる"], "type": "multiple_choice"},
    {"question": "Which direction word means 'straight ahead'?", "answer": "まっすぐ", "options": ["まっすぐ", "みぎ", "ひだり", "うしろ"], "type": "multiple_choice"},
    {"question": "The hospital is on the left side. How do you say this?", "answer": "びょういんはひだりがわにあります。", "options": ["びょういんはひだりがわにあります。", "びょういんはみぎがわにあります。", "びょういんはまえにあります。", "びょういんはそばにあります。"], "type": "multiple_choice"},
    {"question": "From the station, walk for 5 minutes. How do you say this?", "answer": "えきから5ふんあるきます。", "options": ["えきから5ふんあるきます。", "えきまで5ふんあるきます。", "えきを5ふんあるきます。", "えきで5ふんあるきます。"], "type": "multiple_choice"},
    {"question": "かどをまがる ___ 、ゆうびんきょくがあります。(If you turn at the corner, there's a post office.)", "answer": "と", "options": ["と", "から", "ので", "が"], "type": "multiple_choice"},
    {"question": "ひとつめの ___ を右に曲がってください。(Please turn right at the first traffic light.)", "answer": "しんごう", "options": ["しんごう", "かど", "はし", "みち"], "type": "multiple_choice"},
    {"question": "Which particle follows direction words like みぎ、ひだり when giving directions?", "answer": "に", "options": ["に", "を", "で", "へ"], "type": "multiple_choice"},
])

p = os.path.join(BASE, 'ch20-examples.json'); d = load(p)
patch(d, p, [
    {"question": "A stranger asks how to get to the post office. Tell them: 'Go straight and it's on the right.'", "answer": "まっすぐ行って、みぎがわにあります。", "type": "short_answer"},
    {"question": "How do you ask 'Is it far from the station?'", "answer": "えきからとおいですか。", "type": "short_answer"},
    {"question": "The supermarket is near the school. Describe this.", "answer": "スーパーはがっこうのちかくにあります。", "type": "short_answer"},
    {"question": "Give directions: 'Turn left at the second corner.'", "answer": "ふたつめのかどをひだりにまがってください。", "type": "short_answer"},
    {"question": "How do you say 'Cross the bridge and go straight'?", "answer": "はしをわたって、まっすぐ行ってください。", "type": "short_answer"},
    {"question": "Translate: 'The bookstore is between the bank and the post office.'", "answer": "ほんやはぎんこうとゆうびんきょくのあいだにあります。", "type": "short_answer"},
    {"question": "How do you ask 'How many minutes on foot from here?'", "answer": "ここからあるいてなんぷんですか。", "type": "short_answer"},
    {"question": "Give directions: 'Turn right at the traffic light.'", "answer": "しんごうをみぎにまがってください。", "type": "short_answer"},
    {"question": "You're lost. How do you ask 'Where is the nearest station?'", "answer": "いちばんちかいえきはどこですか。", "type": "short_answer"},
    {"question": "Translate: 'If you go straight, you will find a convenience store on the left.'", "answer": "まっすぐ行くと、ひだりにコンビニがあります。", "type": "short_answer"},
    {"question": "How do you say 'The hospital is about 10 minutes by car from here'?", "answer": "びょういんはここからくるまで10ぷんぐらいです。", "type": "short_answer"},
    {"question": "Translate: 'Please go back the way you came.'", "answer": "きたみちをもどってください。", "type": "short_answer"},
    {"question": "How do you say 'It is right in front of you'?", "answer": "すぐまえにあります。", "type": "short_answer"},
    {"question": "Describe: 'There is a café next to the library.'", "answer": "としょかんのとなりにカフェがあります。", "type": "short_answer"},
    {"question": "How do you ask someone to repeat the directions?", "answer": "もういちどいってください。", "type": "short_answer"},
    {"question": "Translate: 'Go up the stairs and turn right.'", "answer": "かいだんをのぼって、みぎにまがってください。", "type": "short_answer"},
    {"question": "How do you say 'It is about 500 metres from here'?", "answer": "ここから500メートルぐらいです。", "type": "short_answer"},
])

# ─────────────────────────────────────────────────────────────────────────────
# CH21  Potential form (〜できます / Group 1 u→e+ます / Group 2 〜られます)
# ─────────────────────────────────────────────────────────────────────────────
p = os.path.join(BASE, 'ch21-grammar.json'); d = load(p)
patch(d, p, [
    {"question": "見る → potential form is:", "answer": "見られます", "options": ["見られます", "見えます", "見れます", "見できます"], "type": "multiple_choice"},
    {"question": "来る → potential form is:", "answer": "来られます（こられます）", "options": ["来られます（こられます）", "来できます", "来れます", "来えます"], "type": "multiple_choice"},
    {"question": "する → potential form is:", "answer": "できます", "options": ["できます", "しられます", "しれます", "せられます"], "type": "multiple_choice"},
    {"question": "飲む → potential form is:", "answer": "飲めます", "options": ["飲めます", "飲まれます", "飲みられます", "飲できます"], "type": "multiple_choice"},
    {"question": "泳ぐ → potential form is:", "answer": "泳げます", "options": ["泳げます", "泳ぎます", "泳がれます", "泳ぐます"], "type": "multiple_choice"},
    {"question": "話す → potential form is:", "answer": "話せます", "options": ["話せます", "話さます", "話しられます", "話します"], "type": "multiple_choice"},
    {"question": "聞く → potential form is:", "answer": "聞けます", "options": ["聞けます", "聞きます", "聞かれます", "聞くます"], "type": "multiple_choice"},
    {"question": "What particle is typically used with potential verbs for the object?", "answer": "が", "options": ["が", "を", "に", "で"], "type": "multiple_choice"},
    {"question": "How do you say 'Can you ride a bicycle'?", "answer": "じてんしゃに乗れますか。", "options": ["じてんしゃに乗れますか。", "じてんしゃを乗れますか。", "じてんしゃが乗れますか。", "じてんしゃで乗れますか。"], "type": "multiple_choice"},
    {"question": "I can play the guitar. Which is correct?", "answer": "ギターが弾けます。", "options": ["ギターが弾けます。", "ギターを弾けます。", "ギターで弾けます。", "ギターに弾けます。"], "type": "multiple_choice"},
    {"question": "She can't cook. Which is correct?", "answer": "かのじょは料理ができません。", "options": ["かのじょは料理ができません。", "かのじょは料理を できません。", "かのじょは料理に できません。", "かのじょは料理のできません。"], "type": "multiple_choice"},
    {"question": "起きる → potential form is:", "answer": "起きられます", "options": ["起きられます", "起きれます", "起きできます", "起けます"], "type": "multiple_choice"},
    {"question": "読む → potential form is:", "answer": "読めます", "options": ["読めます", "読まれます", "読みられます", "読できます"], "type": "multiple_choice"},
    {"question": "How do you say 'I can eat spicy food'?", "answer": "からいたべものが食べられます。", "options": ["からいたべものが食べられます。", "からいたべものを食べられます。", "からいたべものが食べます。", "からいたべものを食べできます。"], "type": "multiple_choice"},
    {"question": "切る → potential form is:", "answer": "切れます", "options": ["切れます", "切られます", "切りられます", "切できます"], "type": "multiple_choice"},
])

p = os.path.join(BASE, 'ch21-examples.json'); d = load(p)
patch(d, p, [
    {"question": "How do you say 'I can drive a car'?", "answer": "くるまが運転できます。", "type": "short_answer"},
    {"question": "How do you say 'I can't eat raw fish'?", "answer": "なまさかなが食べられません。", "type": "short_answer"},
    {"question": "Ask a friend: 'Can you play the piano?'", "answer": "ピアノが弾けますか。", "type": "short_answer"},
    {"question": "Respond to the above: 'No, I can't play the piano, but I can play the guitar.'", "answer": "いいえ、ピアノは弾けませんが、ギターが弾けます。", "type": "short_answer"},
    {"question": "How do you say 'Anyone can use this computer'?", "answer": "このパソコンはだれでも使えます。", "type": "short_answer"},
    {"question": "How do you say 'I can speak a little English'?", "answer": "すこしえいごが話せます。", "type": "short_answer"},
    {"question": "How do you say 'I couldn't wake up early this morning'?", "answer": "けさはやく起きられませんでした。", "type": "short_answer"},
    {"question": "Ask: 'Can you understand this Japanese?'", "answer": "この日本語がわかりますか。", "type": "short_answer"},
    {"question": "How do you say 'I can type fast'?", "answer": "タイピングがはやくできます。", "type": "short_answer"},
    {"question": "How do you say 'My child can read hiragana now'?", "answer": "こどもがひらがなを読めるようになりました。", "type": "short_answer"},
    {"question": "How do you say 'I can drink milk but I can't eat cheese'?", "answer": "ぎゅうにゅうは飲めますが、チーズは食べられません。", "type": "short_answer"},
    {"question": "How do you say 'I can write kanji a little'?", "answer": "かんじが少し書けます。", "type": "short_answer"},
    {"question": "How do you say 'He can run 10 kilometres'?", "answer": "かれは10キロ走れます。", "type": "short_answer"},
    {"question": "How do you say 'I couldn't finish the homework'?", "answer": "しゅくだいが終わりませんでした。/ しゅくだいができませんでした。", "type": "short_answer"},
    {"question": "How do you say 'She can cook very well'?", "answer": "かのじょはりょうりがとてもじょうずです。/ りょうりがとてもできます。", "type": "short_answer"},
    {"question": "How do you say 'Can you come tomorrow?'", "answer": "あしたこられますか。", "type": "short_answer"},
    {"question": "How do you say 'I can't come because I have work'?", "answer": "しごとがあるから、こられません。", "type": "short_answer"},
])

# ─────────────────────────────────────────────────────────────────────────────
# CH22  Experience: 〜たことがあります; ばかり (just done); はじめて
# ─────────────────────────────────────────────────────────────────────────────
p = os.path.join(BASE, 'ch22-grammar.json'); d = load(p)
patch(d, p, [
    {"question": "To express you've experienced something before, use:", "answer": "〜たことがあります", "options": ["〜たことがあります", "〜ていました", "〜たばかりです", "〜ていません"], "type": "multiple_choice"},
    {"question": "To express you've never done something, use:", "answer": "〜たことがありません", "options": ["〜たことがありません", "〜ていません", "〜ないことがあります", "〜たことはないです"], "type": "multiple_choice"},
    {"question": "すしを食べた ___ があります。(I have eaten sushi before.)", "answer": "こと", "options": ["こと", "ばかり", "ほう", "ため"], "type": "multiple_choice"},
    {"question": "おふろに入った ___ です。(I just took a bath.)", "answer": "ばかり", "options": ["ばかり", "こと", "ところ", "はず"], "type": "multiple_choice"},
    {"question": "はじめて富士山に ___ 。(I climbed Mt. Fuji for the first time.)", "answer": "のぼりました", "options": ["のぼりました", "のぼったことがあります", "のぼったばかりです", "のぼれません"], "type": "multiple_choice"},
    {"question": "What does なんどかあります mean in the context of experience?", "answer": "I have done it several times", "options": ["I have done it several times", "I have done it once", "I have never done it", "I just did it"], "type": "multiple_choice"},
    {"question": "How do you ask 'Have you ever been to Hokkaido?'", "answer": "北海道に行ったことがありますか。", "options": ["北海道に行ったことがありますか。", "北海道に行きましたか。", "北海道に行ったばかりですか。", "北海道に行けますか。"], "type": "multiple_choice"},
    {"question": "ごはんを食べた ___ ですが、またおなかがすきました。(I just ate, but I'm hungry again.)", "answer": "ばかり", "options": ["ばかり", "こと", "ため", "ほど"], "type": "multiple_choice"},
    {"question": "I have seen that movie twice. Which is correct?", "answer": "あのえいがを2かい見たことがあります。", "options": ["あのえいがを2かい見たことがあります。", "あのえいがを2かい見ます。", "あのえいがを2かい見たばかりです。", "あのえいがを2かい見ました。"], "type": "multiple_choice"},
    {"question": "にほんにきた ___ ですから、まだよくわかりません。(I just came to Japan, so I don't understand well yet.)", "answer": "ばかり", "options": ["ばかり", "こと", "ところ", "のみ"], "type": "multiple_choice"},
    {"question": "こうべ牛を食べ ___ ことが ___ ますか。(Have you ever eaten Kobe beef?)", "answer": "た / あり", "options": ["た / あり", "て / あり", "た / い", "て / い"], "type": "multiple_choice"},
    {"question": "She has studied abroad before. Which is correct?", "answer": "かのじょはりゅうがくしたことがあります。", "options": ["かのじょはりゅうがくしたことがあります。", "かのじょはりゅうがくすることがあります。", "かのじょはりゅうがくしたばかりです。", "かのじょはりゅうがくしています。"], "type": "multiple_choice"},
    {"question": "ばかり is used after the ___ form of a verb.", "answer": "た (past plain)", "options": ["た (past plain)", "て (te-form)", "ない (negative)", "dictionary"], "type": "multiple_choice"},
    {"question": "Which word means 'for the first time'?", "answer": "はじめて", "options": ["はじめて", "まえに", "いちど", "このまえ"], "type": "multiple_choice"},
    {"question": "How do you say 'I have never drunk sake before'?", "answer": "おさけをのんだことがありません。", "options": ["おさけをのんだことがありません。", "おさけをのみません。", "おさけはのめません。", "おさけをのんでいません。"], "type": "multiple_choice"},
])

p = os.path.join(BASE, 'ch22-examples.json'); d = load(p)
patch(d, p, [
    {"question": "Have you ever climbed a mountain? You have, twice. Reply in Japanese.", "answer": "はい、2かい山にのぼったことがあります。", "type": "short_answer"},
    {"question": "How do you say 'I have never ridden a horse'?", "answer": "うまにのったことがありません。", "type": "short_answer"},
    {"question": "You just woke up. How do you say 'I just woke up'?", "answer": "おきたばかりです。", "type": "short_answer"},
    {"question": "Your friend asks if you've tried takoyaki. You have, once. Reply.", "answer": "はい、いちどたべたことがあります。", "type": "short_answer"},
    {"question": "How do you say 'This is the first time I've seen snow'?", "answer": "ゆきをみるのははじめてです。", "type": "short_answer"},
    {"question": "How do you ask 'Have you ever watched a sumo match?'", "answer": "すもうをみたことがありますか。", "type": "short_answer"},
    {"question": "Translate: 'I just arrived at the hotel.'", "answer": "ホテルについたばかりです。", "type": "short_answer"},
    {"question": "How do you say 'I have been to Kyoto several times'?", "answer": "京都には何度か行ったことがあります。", "type": "short_answer"},
    {"question": "How do you say 'I have never spoken to a foreigner'?", "answer": "がいこくじんと話したことがありません。", "type": "short_answer"},
    {"question": "Translate: 'I just bought a new smartphone.'", "answer": "あたらしいスマホをかったばかりです。", "type": "short_answer"},
    {"question": "How do you say 'My father has never cooked'?", "answer": "ちちはりょうりをしたことがありません。", "type": "short_answer"},
    {"question": "Have you ever lived abroad? You have, for one year. Reply.", "answer": "はい、いちねんかいがいにすんだことがあります。", "type": "short_answer"},
    {"question": "Translate: 'She just graduated from university.'", "answer": "かのじょはだいがくをそつぎょうしたばかりです。", "type": "short_answer"},
    {"question": "How do you say 'I have read this book before'?", "answer": "このほんをよんだことがあります。", "type": "short_answer"},
    {"question": "How do you say 'Have you ever made Japanese food?'", "answer": "日本りょうりをつくったことがありますか。", "type": "short_answer"},
    {"question": "Translate: 'He just started learning Japanese.'", "answer": "かれは日本語をならいはじめたばかりです。", "type": "short_answer"},
    {"question": "How do you say 'I have never been abroad'?", "answer": "がいこくにいったことがありません。", "type": "short_answer"},
])

# ─────────────────────────────────────────────────────────────────────────────
# CH23  Embedded questions (〜かどうか / 〜か〜か); indirect speech; skill/ability
# ─────────────────────────────────────────────────────────────────────────────
p = os.path.join(BASE, 'ch23-grammar.json'); d = load(p)
patch(d, p, [
    {"question": "あしたあめ ___ か どうか、わかりません。(I don't know whether it will rain tomorrow.)", "answer": "が降る", "options": ["が降る", "は降る", "で降る", "に降る"], "type": "multiple_choice"},
    {"question": "かれが来る ___ 、おしえてください。(Please tell me whether he will come.)", "answer": "かどうか", "options": ["かどうか", "のかを", "かもしれない", "かもしれを"], "type": "multiple_choice"},
    {"question": "しあいがあるか ___ 、まだわかりません。(I don't know yet whether there will be a match.)", "answer": "どうか", "options": ["どうか", "なにか", "どこか", "いつか"], "type": "multiple_choice"},
    {"question": "What does よくわかりません mean?", "answer": "I don't understand well / I don't know well", "options": ["I don't understand well / I don't know well", "I understood", "I know", "I can understand"], "type": "multiple_choice"},
    {"question": "How do you say 'I don't know whether the shop is open or not'?", "answer": "みせがあいているかどうかわかりません。", "options": ["みせがあいているかどうかわかりません。", "みせがあいているかわかりません。", "みせがあくかわかりません。", "みせがあくかどうかいいます。"], "type": "multiple_choice"},
    {"question": "バスが来るか ___ バスていで待っています。(I'm waiting at the bus stop not knowing whether the bus will come.)", "answer": "どうか", "options": ["どうか", "なにか", "それか", "どこか"], "type": "multiple_choice"},
    {"question": "どちらが ___ 、えらんでください。(Please choose which one is better.)", "answer": "いいか", "options": ["いいか", "よくか", "いいかどうか", "よいのか"], "type": "multiple_choice"},
    {"question": "I don't know when the exam is. Which is correct?", "answer": "しけんがいつかわかりません。", "options": ["しけんがいつかわかりません。", "しけんがいつかどうかわかりません。", "しけんがいつかしりません。", "しけんがいつかおしえてください。"], "type": "multiple_choice"},
    {"question": "How do you say 'Please tell me where the post office is'?", "answer": "ゆうびんきょくがどこにあるか、おしえてください。", "options": ["ゆうびんきょくがどこにあるか、おしえてください。", "ゆうびんきょくはどこですか。", "ゆうびんきょくがどこかわかりますか。", "ゆうびんきょくをどこかおしえてください。"], "type": "multiple_choice"},
    {"question": "Use 〜かどうか to embed 'Will she come?' into 'I don't know...'", "answer": "かのじょがくるかどうかわかりません。", "options": ["かのじょがくるかどうかわかりません。", "かのじょがくるかわかりません。", "かのじょくるかどうかわかりません。", "かのじょがくるかどうかです。"], "type": "multiple_choice"},
    {"question": "どこで会うか ___ もきめていません。(We haven't even decided where to meet.)", "answer": "まだ", "options": ["まだ", "もう", "ちょうど", "もし"], "type": "multiple_choice"},
    {"question": "Which question word is used to ask 'how many' in an embedded question?", "answer": "いくつ", "options": ["いくつ", "なに", "どこ", "いつ"], "type": "multiple_choice"},
    {"question": "How do you say 'I don't know what time the train leaves'?", "answer": "でんしゃが何時に出るかわかりません。", "options": ["でんしゃが何時に出るかわかりません。", "でんしゃが何時ですか。", "でんしゃは何時に出るかどうかわかりません。", "でんしゃの時間がわかりません。"], "type": "multiple_choice"},
    {"question": "〜かどうか is used when the embedded question is:", "answer": "a yes/no question", "options": ["a yes/no question", "a wh-question", "a request", "a command"], "type": "multiple_choice"},
    {"question": "〜か (without どうか) is used when the embedded question has:", "answer": "a question word (who, what, where, etc.)", "options": ["a question word (who, what, where, etc.)", "a yes/no answer", "no verb", "a polite ending"], "type": "multiple_choice"},
])

p = os.path.join(BASE, 'ch23-examples.json'); d = load(p)
patch(d, p, [
    {"question": "You're not sure if the meeting is at 3pm or 4pm. Express your uncertainty.", "answer": "かいぎが3じか4じかわかりません。", "type": "short_answer"},
    {"question": "How do you say 'I don't know whether it will snow tomorrow'?", "answer": "あした雪がふるかどうかわかりません。", "type": "short_answer"},
    {"question": "Ask someone to tell you where the restroom is (using embedded question).", "answer": "トイレがどこにあるか、おしえてください。", "type": "short_answer"},
    {"question": "How do you say 'I'm not sure whether this is correct'?", "answer": "これがただしいかどうかわかりません。", "type": "short_answer"},
    {"question": "Translate: 'I don't know who the teacher is.'", "answer": "せんせいがだれかわかりません。", "type": "short_answer"},
    {"question": "How do you say 'I don't know what to buy as a gift'?", "answer": "プレゼントに何をかえばいいかわかりません。", "type": "short_answer"},
    {"question": "Express that you're not sure whether the party is cancelled.", "answer": "パーティーがキャンセルになるかどうかわかりません。", "type": "short_answer"},
    {"question": "Translate: 'Please tell me how much this costs.'", "answer": "これがいくらか、おしえてください。", "type": "short_answer"},
    {"question": "How do you say 'I don't know whether my friend is coming or not'?", "answer": "ともだちがくるかどうかわかりません。", "type": "short_answer"},
    {"question": "Translate: 'I don't know who will win the game.'", "answer": "しあいでだれがかつかわかりません。", "type": "short_answer"},
    {"question": "How do you ask 'Do you know where the key is?'", "answer": "かぎがどこにあるか、しっていますか。", "type": "short_answer"},
    {"question": "How do you say 'I don't know whether I should study or sleep'?", "answer": "べんきょうするかねるかわかりません。", "type": "short_answer"},
    {"question": "Translate: 'Please let me know when you arrive.'", "answer": "ついたら、おしえてください。", "type": "short_answer"},
    {"question": "How do you say 'I don't know whether this restaurant is good'?", "answer": "このレストランがいいかどうかわかりません。", "type": "short_answer"},
    {"question": "Translate: 'I don't know how to read this kanji.'", "answer": "このかんじがどうよむかわかりません。", "type": "short_answer"},
    {"question": "Express that you don't know whether the shop is open on Sunday.", "answer": "みせがにちようびにあいているかどうかわかりません。", "type": "short_answer"},
    {"question": "How do you say 'I'm not sure how many people will come'?", "answer": "なんにんくるかわかりません。", "type": "short_answer"},
])

# ─────────────────────────────────────────────────────────────────────────────
# CH24  すぎます (too much); になります (become); adverb form; requests with もっと
# ─────────────────────────────────────────────────────────────────────────────
p = os.path.join(BASE, 'ch24-grammar.json'); d = load(p)
patch(d, p, [
    {"question": "この映画はなが ___ 。(This movie is too long.)", "answer": "すぎます", "options": ["すぎます", "なりました", "なっています", "いすぎます"], "type": "multiple_choice"},
    {"question": "To form the adverb of an い-adjective, change い to:", "answer": "く", "options": ["く", "に", "な", "で"], "type": "multiple_choice"},
    {"question": "To form the adverb of a な-adjective, add:", "answer": "に", "options": ["に", "く", "で", "な"], "type": "multiple_choice"},
    {"question": "はるになると、きおんがあたたか ___ 。(When spring comes, the temperature gets warm.)", "answer": "くなります", "options": ["くなります", "になります", "さくなります", "でなります"], "type": "multiple_choice"},
    {"question": "にぎやかになりました means:", "answer": "It became lively.", "options": ["It became lively.", "It is lively.", "It was lively.", "It will be lively."], "type": "multiple_choice"},
    {"question": "The adverb form of じょうずです is:", "answer": "じょうずに", "options": ["じょうずに", "じょうずく", "じょうずで", "じょうずの"], "type": "multiple_choice"},
    {"question": "The adverb form of はやいです is:", "answer": "はやく", "options": ["はやく", "はやに", "はやくて", "はやで"], "type": "multiple_choice"},
    {"question": "たべすぎは体によく ___ 。(Eating too much is not good for your body.)", "answer": "ない", "options": ["ない", "なりません", "ありません", "できません"], "type": "multiple_choice"},
    {"question": "もっとゆっくり ___ てください。(Please speak more slowly.)", "answer": "はなし", "options": ["はなし", "はなす", "はなせ", "はなさ"], "type": "multiple_choice"},
    {"question": "Which phrase means 'I drank too much'?", "answer": "のみすぎました", "options": ["のみすぎました", "のみました", "のみませんでした", "のみたかったです"], "type": "multiple_choice"},
    {"question": "How do you say 'Japanese is becoming easier'?", "answer": "日本語がやさしくなっています。", "options": ["日本語がやさしくなっています。", "日本語がやさしになっています。", "日本語がやさしくなりました。", "日本語がやさしすぎます。"], "type": "multiple_choice"},
    {"question": "How do you attach すぎます to the い-adj むずかしい?", "answer": "むずかしすぎます", "options": ["むずかしすぎます", "むずかしいすぎます", "むずかしくすぎます", "むずかしなすぎます"], "type": "multiple_choice"},
    {"question": "How do you attach すぎます to the な-adj しずか?", "answer": "しずかすぎます", "options": ["しずかすぎます", "しずかなすぎます", "しずかにすぎます", "しずかくすぎます"], "type": "multiple_choice"},
    {"question": "もっとまじめに ___ ください。(Please study more seriously.)", "answer": "べんきょうして", "options": ["べんきょうして", "べんきょうし", "べんきょうする", "べんきょうした"], "type": "multiple_choice"},
    {"question": "How do you say 'I want to become a doctor'?", "answer": "いしゃになりたいです。", "options": ["いしゃになりたいです。", "いしゃがなりたいです。", "いしゃをなりたいです。", "いしゃでなりたいです。"], "type": "multiple_choice"},
])

p = os.path.join(BASE, 'ch24-examples.json'); d = load(p)
patch(d, p, [
    {"question": "The coffee is too hot to drink. Express this in Japanese.", "answer": "コーヒーがあつすぎて、のめません。", "type": "short_answer"},
    {"question": "How do you say 'I slept too much yesterday'?", "answer": "きのうはねすぎました。", "type": "short_answer"},
    {"question": "Translate: 'Please write more carefully.'", "answer": "もっとていねいにかいてください。", "type": "short_answer"},
    {"question": "How do you say 'It's getting cold'?", "answer": "さむくなってきました。", "type": "short_answer"},
    {"question": "Translate: 'This bag is too expensive.'", "answer": "このかばんはたかすぎます。", "type": "short_answer"},
    {"question": "How do you say 'She became a teacher'?", "answer": "かのじょはせんせいになりました。", "type": "short_answer"},
    {"question": "The room became dirty. Express this.", "answer": "へやがきたなくなりました。", "type": "short_answer"},
    {"question": "Translate: 'Please speak Japanese more slowly.'", "answer": "もっとゆっくり日本語をはなしてください。", "type": "short_answer"},
    {"question": "How do you say 'I worked too much this week'?", "answer": "こんしゅうはたらきすぎました。", "type": "short_answer"},
    {"question": "How do you say 'The test became easy'?", "answer": "テストがやさしくなりました。", "type": "short_answer"},
    {"question": "Translate: 'Please do your homework more carefully.'", "answer": "もっとていねいにしゅくだいをやってください。", "type": "short_answer"},
    {"question": "How do you say 'I want to become fluent in Japanese'?", "answer": "日本語がじょうずになりたいです。", "type": "short_answer"},
    {"question": "The city became lively after the festival. Express this.", "answer": "まつりのあと、まちがにぎやかになりました。", "type": "short_answer"},
    {"question": "How do you say 'The portion was too small'?", "answer": "りょうがすくなすぎました。", "type": "short_answer"},
    {"question": "Translate: 'Please explain it more simply.'", "answer": "もっとかんたんにせつめいしてください。", "type": "short_answer"},
    {"question": "How do you say 'Don't drink too much alcohol'?", "answer": "おさけをのみすぎないでください。", "type": "short_answer"},
    {"question": "How do you say 'It has become dark outside'?", "answer": "そとがくらくなりました。", "type": "short_answer"},
])

# ─────────────────────────────────────────────────────────────────────────────
# CH25  Regret (〜ばよかった / 〜なければよかった); も+negative; Japanese seasons/events
# ─────────────────────────────────────────────────────────────────────────────
p = os.path.join(BASE, 'ch25-grammar.json'); d = load(p)
patch(d, p, [
    {"question": "もっとべんきょうすれ ___ よかったです。(I wish I had studied more.)", "answer": "ば", "options": ["ば", "て", "たら", "なら"], "type": "multiple_choice"},
    {"question": "あのレストランに行か ___ よかったです。(I wish I hadn't gone to that restaurant.)", "answer": "なければ", "options": ["なければ", "ないで", "なくて", "ないば"], "type": "multiple_choice"},
    {"question": "にほんごをもっとれんしゅうすれ ___ 。(I wish I had practised Japanese more.)", "answer": "ばよかったです", "options": ["ばよかったです", "てよかったです", "たらよかったです", "てもよかったです"], "type": "multiple_choice"},
    {"question": "どこにも行きません means:", "answer": "I don't go anywhere.", "options": ["I don't go anywhere.", "I go somewhere.", "I go everywhere.", "I go nowhere sometimes."], "type": "multiple_choice"},
    {"question": "なにも ___ でした。(I didn't eat anything.)", "answer": "たべません", "options": ["たべません", "たべました", "たべません", "たべませんでした"], "type": "multiple_choice"},
    {"question": "だれも ___ 。(Nobody came.)", "answer": "きませんでした", "options": ["きませんでした", "きました", "きます", "きませんでしたか"], "type": "multiple_choice"},
    {"question": "The verb form before ばよかった is:", "answer": "conditional ば-form", "options": ["conditional ば-form", "て-form", "た-form", "dictionary form"], "type": "multiple_choice"},
    {"question": "I regret eating too much. Which is correct?", "answer": "たべすぎなければよかったです。", "options": ["たべすぎなければよかったです。", "たべすぎればよかったです。", "たべすぎたらよかったです。", "たべすぎてよかったです。"], "type": "multiple_choice"},
    {"question": "もっとはやく ___ ばよかった。(I wish I had come earlier.)", "answer": "くれれ / きれ", "options": ["くれれ / きれ", "きれ", "きた", "きて"], "type": "multiple_choice"},
    {"question": "What is はつもうで?", "answer": "First shrine visit of the New Year", "options": ["First shrine visit of the New Year", "Last shrine visit of the year", "Autumn festival", "Summer fireworks"], "type": "multiple_choice"},
    {"question": "What is お盆?", "answer": "Buddhist memorial festival for ancestors in August", "options": ["Buddhist memorial festival for ancestors in August", "New Year celebration", "Cherry blossom viewing festival", "Children's Day festival"], "type": "multiple_choice"},
    {"question": "何も食べませんでした means:", "answer": "I didn't eat anything.", "options": ["I didn't eat anything.", "I ate everything.", "I didn't eat something.", "I ate nothing special."], "type": "multiple_choice"},
    {"question": "I wish I had taken a photo. Which is correct?", "answer": "しゃしんをとればよかったです。", "options": ["しゃしんをとればよかったです。", "しゃしんをとったらよかったです。", "しゃしんをとってよかったです。", "しゃしんをとるばよかったです。"], "type": "multiple_choice"},
    {"question": "How do you say 'Nobody knows'?", "answer": "だれもしりません。", "options": ["だれもしりません。", "だれもしります。", "だれかしりません。", "だれもわかる。"], "type": "multiple_choice"},
    {"question": "How do you say 'I wish I hadn't spent all my money'?", "answer": "おかねをぜんぶつかわなければよかったです。", "options": ["おかねをぜんぶつかわなければよかったです。", "おかねをぜんぶつかえばよかったです。", "おかねをぜんぶつかってよかったです。", "おかねをぜんぶつかいたらよかったです。"], "type": "multiple_choice"},
])

p = os.path.join(BASE, 'ch25-examples.json'); d = load(p)
patch(d, p, [
    {"question": "You missed a great concert. Express your regret.", "answer": "コンサートに行けばよかったです。", "type": "short_answer"},
    {"question": "How do you say 'I didn't buy anything'?", "answer": "なにもかいませんでした。", "type": "short_answer"},
    {"question": "You said something rude and regret it. Express this.", "answer": "そんなことをいわなければよかったです。", "type": "short_answer"},
    {"question": "Translate: 'Nobody was at home.'", "answer": "だれもいえにいませんでした。", "type": "short_answer"},
    {"question": "How do you say 'I wish I had started studying Japanese earlier'?", "answer": "もっとはやく日本語のべんきょうをはじめればよかったです。", "type": "short_answer"},
    {"question": "Translate: 'I didn't go anywhere over the holidays.'", "answer": "やすみにどこへもいきませんでした。", "type": "short_answer"},
    {"question": "You didn't bring an umbrella and it rained. Express regret.", "answer": "かさをもってくればよかったです。", "type": "short_answer"},
    {"question": "Translate: 'Nothing happened.'", "answer": "なにもおきませんでした。", "type": "short_answer"},
    {"question": "How do you say 'I wish I hadn't stayed up so late'?", "answer": "そんなにおそくまでおきていなければよかったです。", "type": "short_answer"},
    {"question": "You saw はつもうで on TV. Explain what it is in Japanese.", "answer": "はつもうでは、しょうがつにはじめてじんじゃやおてらにおまいりすることです。", "type": "short_answer"},
    {"question": "How do you say 'I didn't understand anything'?", "answer": "なにもわかりませんでした。", "type": "short_answer"},
    {"question": "I regret not saving money last year. Express this.", "answer": "きょねんおかねをためればよかったです。", "type": "short_answer"},
    {"question": "Translate: 'I didn't meet anyone at the party.'", "answer": "パーティーでだれにもあいませんでした。", "type": "short_answer"},
    {"question": "How do you say 'I wish I had taken more photos'?", "answer": "もっとしゃしんをとればよかったです。", "type": "short_answer"},
    {"question": "Describe お盆 in simple Japanese.", "answer": "お盆は、なくなったそせんをむかえるおまつりです。8がつにあります。", "type": "short_answer"},
    {"question": "How do you say 'Nothing was left on the table'?", "answer": "テーブルになにものこっていませんでした。", "type": "short_answer"},
])

print("\nAll Ch18-25 patches complete!")

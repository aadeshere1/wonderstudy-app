"""Patch N5 grammar/examples Ch09-17 to reach 20 questions each."""
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

# ── Ch09: 買い物をします ──────────────────────────────────────────────────

ch09_grammar_add = [
    {"question": "りんごを _____つ ください。(Please give me 5 apples.)", "answer": "いつ", "options": ["いつ", "よっ", "むっ", "なな"], "explanation": "5つ = いつつ (general counter for things). Japanese native counters: 1=ひとつ, 2=ふたつ, 3=みっつ, 4=よっつ, 5=いつつ."},
    {"question": "まいにち どのくらい にほんごを べんきょう しますか。——いち_____かん ぐらいです。", "answer": "じ", "options": ["じ", "にち", "かい", "かげつ"], "explanation": "じかん = hours. いちじかん = one hour. Counter for hours."},
    {"question": "この ざっしを _____さつ かいましたか。(How many magazines did you buy?)", "answer": "なん", "options": ["なん", "いく", "どの", "なに"], "explanation": "なんさつ = how many (books/magazines). さつ = counter for bound publications."},
    {"question": "バナナが _____本 あります。(There are 3 bananas.)", "answer": "さんぼん", "options": ["さんぼん", "さんまい", "みっつ", "さんこ"], "explanation": "本(ほん/ぼん/ぽん) = counter for long thin objects. 3本 = さんぼん."},
    {"question": "シャツを _____まい かいました。(I bought 2 shirts.)", "answer": "にまい", "options": ["にまい", "にほん", "ふたつ", "にこ"], "explanation": "枚(まい) = counter for flat objects (shirts, papers, plates). 2枚 = にまい."},
    {"question": "コーヒーを _____ぱい のみますか。(How many cups of coffee do you drink?)", "answer": "なん", "options": ["なん", "いく", "どれ", "なに"], "explanation": "なんばい = how many cups. 杯(はい/ばい/ぱい) = counter for cups/glasses."},
    {"question": "えんぴつが 6_____あります。(There are 6 pencils.)", "answer": "ぽん", "options": ["ぽん", "まい", "こ", "つ"], "explanation": "6本 = ろっぽん. 本(ほん/ぼん/ぽん) changes based on number: 6→ろっぽん."},
    {"question": "よく かいものを しますか。——_____たまに します。(Do you often shop? — I shop occasionally.)", "answer": "たまに", "options": ["たまに", "よく", "あまり", "ぜんぜん"], "explanation": "たまに = occasionally/sometimes. Frequency adverbs: いつも>よく>たまに>あまり〜ない>ぜんぜん〜ない."},
    {"question": "ジュースを _____ぽん かいましたか。(How many bottles of juice did you buy?)", "answer": "なんぼん", "options": ["なんぼん", "なんまい", "なんこ", "なんつ"], "explanation": "なんぼん = how many (long objects). 本 = counter for bottles, pens, etc."},
    {"question": "にほんごを あまり _____。(I don't study Japanese much.)", "answer": "べんきょうしません", "options": ["べんきょうしません", "べんきょうします", "べんきょうしました", "べんきょうしませんでした"], "explanation": "あまり〜ません = don't ~ much. Paired negative verb."},
]

ch09_examples_add = [
    {"question": "Asking how many pieces of paper you need:", "answer": "かみは なんまい いりますか。", "options": ["かみは なんまい いりますか。", "かみは なんほん いりますか。", "かみは なんこ いりますか。", "かみは いくつ いりますか。"], "explanation": "まい = flat objects counter. かみ = paper. いります = to need."},
    {"question": "Buying 3 bottles of water at a convenience store:", "answer": "みずを さんぼん ください。", "options": ["みずを さんぼん ください。", "みずを さんまい ください。", "みずを みっつ ください。", "みずを さんこ ください。"], "explanation": "本(ぼん) = counter for bottles/long things. 3本 = さんぼん."},
    {"question": "You go to the market every day. How do you say it?", "answer": "まいにち いちばに いきます。", "options": ["まいにち いちばに いきます。", "よく いちばに いきます。", "たまに いちばに いきます。", "まいにち いちばで いきます。"], "explanation": "まいにち = every day. いちば = market. に = destination."},
    {"question": "Saying 'I rarely drink alcohol.'", "answer": "あまり おさけを のみません。", "options": ["あまり おさけを のみません。", "よく おさけを のみません。", "たまに おさけを のみます。", "あまり おさけを のみます。"], "explanation": "あまり+negative = not much/rarely. Must pair with negative verb."},
    {"question": "Asking how many stamps you need for the letter:", "answer": "きってを なんまい はります か。", "options": ["きってを なんまい はりますか。", "きってを なんほん はりますか。", "きってを なんこ はりますか。", "きってを いくつ はりますか。"], "explanation": "きって = stamp. まい = flat object counter. はります = to stick/affix."},
    {"question": "You bought 5 notebooks. How do you say it?", "answer": "ノートを ごさつ かいました。", "options": ["ノートを ごさつ かいました。", "ノートを いつつ かいました。", "ノートを ごまい かいました。", "ノートを ごほん かいました。"], "explanation": "冊(さつ) = counter for books/notebooks. 5冊 = ごさつ."},
    {"question": "How often do you eat at a restaurant? About twice a week.", "answer": "しゅうに にかい ぐらい レストランで たべます。", "options": ["しゅうに にかい ぐらい レストランで たべます。", "しゅうに にかい ぐらい レストランに たべます。", "まいしゅう にかい ぐらい レストランで たべます。", "しゅうに にかい ぐらい レストランを たべます。"], "explanation": "しゅうに〜かい = ~ times a week. ぐらい = approximately. で = at (place of action)."},
    {"question": "You don't watch TV at all.", "answer": "ぜんぜん テレビを みません。", "options": ["ぜんぜん テレビを みません。", "あまり テレビを みません。", "ぜんぜん テレビを みます。", "たまに テレビを みません。"], "explanation": "ぜんぜん+negative = not at all. Strongest negative frequency."},
    {"question": "At a ticket counter: 'Two adult tickets, please.'", "answer": "おとなを にまい ください。", "options": ["おとなを にまい ください。", "おとなを にほん ください。", "おとなを ふたつ ください。", "おとなを にこ ください。"], "explanation": "Tickets use 枚(まい) = flat objects. おとな = adult. にまい = 2 tickets."},
    {"question": "Saying you exercise 3 times a week:", "answer": "しゅうに さんかい うんどうします。", "options": ["しゅうに さんかい うんどうします。", "しゅうに さんど うんどうします。", "まいしゅう さんかい うんどうします。", "しゅうに さんかい うんどうしました。"], "explanation": "しゅうに〜かい = ~ times a week. 回(かい) = counter for times/occurrences."},
    {"question": "Asking 'How many cups of tea do you drink a day?'", "answer": "いちにちに おちゃを なんばい のみますか。", "options": ["いちにちに おちゃを なんばい のみますか。", "いちにちに おちゃを なんほん のみますか。", "いちにちに おちゃを いくつ のみますか。", "いちにちに おちゃを なんまい のみますか。"], "explanation": "杯(はい/ばい) = counter for cups. なんばい = how many cups."},
    {"question": "You always bring lunch from home.", "answer": "いつも うちから おべんとうを もってきます。", "options": ["いつも うちから おべんとうを もってきます。", "よく うちから おべんとうを もってきます。", "いつも うちに おべんとうを もってきます。", "いつも うちで おべんとうを もってきます。"], "explanation": "いつも = always. から = from. もってきます = bring (to the speaker's location)."},
]

# ── Ch10: 富士山より高い山はありますか ──────────────────────────────────

ch10_grammar_add = [
    {"question": "とうきょうと おおさかと、どちらが _____ですか。(Which is bigger, Tokyo or Osaka?)", "answer": "おおきい", "options": ["おおきい", "たかい", "ひろい", "うつくしい"], "explanation": "AとBとどちらが〜ですか = Which is more ~ , A or B?"},
    {"question": "にほんで _____たかい やまは ふじさんです。(The tallest mountain in Japan is Mt Fuji.)", "answer": "いちばん", "options": ["いちばん", "もっと", "より", "ほど"], "explanation": "いちばん+adjective = the most ~. Superlative form."},
    {"question": "バスより でんしゃの ほうが _____です。(Trains are faster than buses.)", "answer": "はやい", "options": ["はやい", "おそい", "やすい", "たかい"], "explanation": "AよりBのほうが〜 = B is more ~ than A."},
    {"question": "なかで なにが _____すきですか。(What do you like the most?)", "answer": "いちばん", "options": ["いちばん", "もっと", "より", "ほど"], "explanation": "〜の中でなにがいちばん〜ですか = What is the most ~ among ~?"},
    {"question": "りんごと みかんと どちらが _____ですか。——どちらも すきです。", "answer": "すき", "options": ["すき", "きらい", "おいしい", "たかい"], "explanation": "どちらも+affirmative = both. I like both (apple and orange)."},
    {"question": "この みせは あの みせ_____ やすいです。(This store is cheaper than that store.)", "answer": "より", "options": ["より", "ほど", "ほうが", "いちばん"], "explanation": "AはBより〜 = A is more ~ than B. より = than (comparison)."},
    {"question": "クラスの なかで だれが _____せが たかいですか。(Who is the tallest in the class?)", "answer": "いちばん", "options": ["いちばん", "もっとも", "より", "ほど"], "explanation": "だれがいちばん〜 = who is the most ~. Superlative with person."},
    {"question": "あついより _____ほうが すきです。(I prefer cold to hot.)", "answer": "さむい", "options": ["さむい", "あつい", "すずしい", "あたたかい"], "explanation": "AよりBのほうが = prefer B over A. さむい = cold."},
    {"question": "このクラスで にほんごが いちばん _____のは だれですか。(Who is best at Japanese in this class?)", "answer": "じょうず", "options": ["じょうず", "へた", "すき", "きらい"], "explanation": "じょうず = skilled/good at. いちばんじょうずな = the most skilled."},
]

ch10_examples_add = [
    {"question": "Comparing apples and oranges — you prefer oranges.", "answer": "りんごより みかんのほうが すきです。", "options": ["りんごより みかんのほうが すきです。", "みかんより りんごのほうが すきです。", "りんごも みかんも すきです。", "りんごと みかんと どちらも すきです。"], "explanation": "AよりBのほうが = prefer B over A."},
    {"question": "Asking 'Which is more expensive, beef or pork?'", "answer": "ぎゅうにくと ぶたにくと どちらが たかいですか。", "options": ["ぎゅうにくと ぶたにくと どちらが たかいですか。", "ぎゅうにくか ぶたにくか どちらが たかいですか。", "ぎゅうにくより ぶたにくが たかいですか。", "ぎゅうにくと ぶたにくと どれが たかいですか。"], "explanation": "AとBとどちらが = Which of A and B. どちら = which of two."},
    {"question": "Among all sports, baseball is the most popular in Japan.", "answer": "スポーツのなかで やきゅうが いちばん にんきです。", "options": ["スポーツのなかで やきゅうが いちばん にんきです。", "スポーツのなかで やきゅうより にんきです。", "スポーツのなかで やきゅうが もっと にんきです。", "スポーツのなかで やきゅうが いちばん にんきでした。"], "explanation": "〜の中で〜がいちばん〜 = Among ~, ~ is the most ~."},
    {"question": "Summer is hotter than spring in Japan.", "answer": "はるより なつのほうが あついです。", "options": ["はるより なつのほうが あついです。", "なつより はるのほうが あついです。", "はるも なつも あついです。", "はるは なつより あついです。"], "explanation": "AよりBのほうが〜 = B is more ~ than A. はる=spring, なつ=summer."},
    {"question": "What is the cheapest item on the menu?", "answer": "メニューのなかで いちばん やすいのは なんですか。", "options": ["メニューのなかで いちばん やすいのは なんですか。", "メニューのなかで もっと やすいのは なんですか。", "メニューのなかで やすいのより なんですか。", "メニューのなかで いちばん やすいは なんですか。"], "explanation": "〜の中で〜がいちばん〜のは何ですか = What is the most ~ among ~?"},
    {"question": "I prefer studying at home rather than at a library.", "answer": "としょかんより うちのほうが べんきょうしやすいです。", "options": ["としょかんより うちのほうが べんきょうしやすいです。", "うちより としょかんのほうが べんきょうしやすいです。", "としょかんも うちも べんきょうしやすいです。", "としょかんか うちか べんきょうしやすいです。"], "explanation": "AよりBのほうが = B is better/preferred over A. しやすい = easy to do."},
    {"question": "Which season is the most beautiful in Japan? Many say autumn.", "answer": "にほんで いちばん うつくしい きせつは どれですか。", "options": ["にほんで いちばん うつくしい きせつは どれですか。", "にほんで もっと うつくしい きせつは どれですか。", "にほんで いちばん うつくしい きせつは なんですか。", "にほんで より うつくしい きせつは どれですか。"], "explanation": "いちばん+adj = superlative. きせつ = season. どれ for choosing among several."},
    {"question": "The bullet train is faster than the airplane for short trips.", "answer": "みじかい りょこうは ひこうきより しんかんせんのほうが はやいです。", "options": ["みじかい りょこうは ひこうきより しんかんせんのほうが はやいです。", "みじかい りょこうは しんかんせんより ひこうきのほうが はやいです。", "みじかい りょこうは ひこうきと しんかんせんと どちらも はやいです。", "みじかい りょこうは ひこうきほど しんかんせんが はやいです。"], "explanation": "AよりBのほうが = B is more ~ than A. みじかい = short."},
    {"question": "Asking 'Who is the most popular singer in Japan right now?'", "answer": "いまの にほんで いちばん にんきの かしゅは だれですか。", "options": ["いまの にほんで いちばん にんきの かしゅは だれですか。", "いまの にほんで もっとも にんきの かしゅは だれですか。", "いまの にほんで いちばん にんきな かしゅは だれですか。", "いまの にほんで いちばん にんきの かしゅは なにですか。"], "explanation": "いちばん+にんきの = most popular. かしゅ = singer."},
    {"question": "Coffee is more expensive than tea at this café.", "answer": "このカフェでは おちゃより コーヒーのほうが たかいです。", "options": ["このカフェでは おちゃより コーヒーのほうが たかいです。", "このカフェでは コーヒーより おちゃのほうが たかいです。", "このカフェでは おちゃも コーヒーも たかいです。", "このカフェでは おちゃと コーヒーと どちらが たかいですか。"], "explanation": "AよりBのほうが = B is more ~ than A."},
    {"question": "In this class, who studies the hardest?", "answer": "このクラスで いちばん よく べんきょうするのは だれですか。", "options": ["このクラスで いちばん よく べんきょうするのは だれですか。", "このクラスで もっと よく べんきょうするのは だれですか。", "このクラスで いちばん よく べんきょうしたのは だれですか。", "このクラスで いちばん よく べんきょうするは だれですか。"], "explanation": "いちばんよく〜する = does ~ the most. のは links the verb phrase as noun."},
    {"question": "Beef is more expensive than chicken, but chicken is healthier.", "answer": "とりにくより ぎゅうにくのほうが たかいですが、とりにくのほうが からだに いいです。", "options": ["とりにくより ぎゅうにくのほうが たかいですが、とりにくのほうが からだに いいです。", "ぎゅうにくより とりにくのほうが たかいですが、ぎゅうにくのほうが からだに いいです。", "とりにくも ぎゅうにくも たかいですが、どちらも からだに いいです。", "とりにくより ぎゅうにくのほうが たかいので、とりにくのほうが からだに いいです。"], "explanation": "Two comparison clauses joined by が (but). からだにいい = good for the body."},
]

# ── Ch11: どこかへ行きましたか ──────────────────────────────────────────

ch11_grammar_add = [
    {"question": "しゅうまつは _____へ いきましたか。——いいえ、どこへも いきませんでした。", "answer": "どこか", "options": ["どこか", "どこも", "どこへも", "どこでも"], "explanation": "どこかへ = somewhere. どこへもいきません = didn't go anywhere (negative)."},
    {"question": "なにか _____ましたか。——いいえ、なにも たべませんでした。(Did you eat something?)", "answer": "たべ", "options": ["たべ", "のみ", "かい", "み"], "explanation": "なにか = something. なにも+negative = nothing at all."},
    {"question": "だれかが きましたか。——いいえ、_____きませんでした。(Did someone come? — No, nobody came.)", "answer": "だれも", "options": ["だれも", "だれか", "だれでも", "だれには"], "explanation": "だれか = someone. だれも+negative = no one."},
    {"question": "どこかで おいしい すしを たべ _____。(Let's eat delicious sushi somewhere.)", "answer": "ましょう", "options": ["ましょう", "ませんか", "ません", "ました"], "explanation": "ましょう = let's (suggestion). どこかで = somewhere."},
    {"question": "きのう なにか かいましたか。——はい、_____ かいました。(Did you buy anything? — Yes, I bought something.)", "answer": "なにか", "options": ["なにか", "なにも", "なにでも", "なにが"], "explanation": "なにか = something (affirmative context). なにも+negative = nothing."},
    {"question": "この へんに _____いい レストランが ありますか。(Is there a good restaurant somewhere around here?)", "answer": "どこか", "options": ["どこか", "どこも", "どこへも", "どこでも"], "explanation": "どこか = somewhere. どこかに = somewhere (location)."},
    {"question": "かれは _____いきません。(He doesn't go anywhere.)", "answer": "どこへも", "options": ["どこへも", "どこかへ", "どこでも", "どこかで"], "explanation": "どこへも+negative = (not) anywhere. The も with negative means 'not even anywhere'."},
    {"question": "たなかさんが なにか _____。(Mr Tanaka said something.)", "answer": "いいました", "options": ["いいました", "きこえました", "みえました", "おもいました"], "explanation": "なにか+verb = said/did something (indefinite). いいました = said."},
    {"question": "だれかに _____ましたか。(Did you ask someone?)", "answer": "きき", "options": ["きき", "いい", "おし", "はなし"], "explanation": "だれかに = to someone (direction). ききます = to ask/listen. に marks recipient."},
    {"question": "いえに _____いますか。(Is anyone at home?)", "answer": "だれか", "options": ["だれか", "だれも", "だれでも", "だれには"], "explanation": "だれか = someone. In a question, だれか = is anyone ~?"},
]

ch11_examples_add = [
    {"question": "Asking if a friend went anywhere over the weekend:", "answer": "しゅうまつ どこかへ いきましたか。", "options": ["しゅうまつ どこかへ いきましたか。", "しゅうまつ どこへも いきましたか。", "しゅうまつ どこかに いきましたか。", "しゅうまつ どこでも いきましたか。"], "explanation": "どこかへ = somewhere. Used in questions."},
    {"question": "You stayed home all weekend. How do you say it?", "answer": "しゅうまつは どこへも いきませんでした。うちに いました。", "options": ["しゅうまつは どこへも いきませんでした。うちに いました。", "しゅうまつは どこかへ いきませんでした。うちに いました。", "しゅうまつは どこへも いきました。うちに いました。", "しゅうまつは どこにも いきませんでした。うちで いました。"], "explanation": "どこへも+negative = didn't go anywhere. うちにいました = stayed at home."},
    {"question": "Asking 'Did anyone call while I was out?'", "answer": "るすの あいだに だれかから でんわが ありましたか。", "options": ["るすの あいだに だれかから でんわが ありましたか。", "るすの あいだに だれもから でんわが ありましたか。", "るすの あいだに だれかに でんわが ありましたか。", "るすの あいだに だれでもから でんわが ありましたか。"], "explanation": "だれかから = from someone. あいだに = during. るす = absence/being out."},
    {"question": "You want to eat something sweet. How do you say it?", "answer": "なにか あまい ものが たべたいです。", "options": ["なにか あまい ものが たべたいです。", "なにも あまい ものが たべたいです。", "なにか あまい ものを たべたいです。", "なにでも あまい ものが たべたいです。"], "explanation": "なにか = something. あまい = sweet. たべたい = want to eat."},
    {"question": "Nobody understood the teacher's explanation.", "answer": "せんせいの せつめいは だれも わかりませんでした。", "options": ["せんせいの せつめいは だれも わかりませんでした。", "せんせいの せつめいは だれか わかりませんでした。", "せんせいの せつめいは だれでも わかりませんでした。", "せんせいの せつめいは だれかが わかりませんでした。"], "explanation": "だれも+negative = nobody. わかりませんでした = didn't understand."},
    {"question": "Asking if there's anything you should bring to the party:", "answer": "パーティーに なにか もっていきましょうか。", "options": ["パーティーに なにか もっていきましょうか。", "パーティーに なにも もっていきましょうか。", "パーティーへ なにか もっていきますか。", "パーティーで なにか もっていきましょうか。"], "explanation": "なにか = something. 〜ましょうか = shall I ~? Offering to bring something."},
    {"question": "I didn't eat anything since morning.", "answer": "あさから なにも たべていません。", "options": ["あさから なにも たべていません。", "あさから なにか たべていません。", "あさから なにも たべません。", "あさから なにでも たべていません。"], "explanation": "なにも+negative = nothing. から = since. ていません = have not done."},
    {"question": "Someone is knocking. Asking 'Is someone there?'", "answer": "だれかいますか。", "options": ["だれかいますか。", "だれもいますか。", "だれでもいますか。", "だれかはいますか。"], "explanation": "だれか = someone. います = is there (person). だれかいますか = Is anyone there?"},
    {"question": "Nothing special happened today.", "answer": "きょうは なにも とくべつな ことが ありませんでした。", "options": ["きょうは なにも とくべつな ことが ありませんでした。", "きょうは なにか とくべつな ことが ありませんでした。", "きょうは なにでも とくべつな ことが ありませんでした。", "きょうは なにも とくべつな ことが ありました。"], "explanation": "なにも+negative = nothing. とくべつ = special. ありませんでした = there wasn't."},
    {"question": "Let's go somewhere fun this weekend!", "answer": "しゅうまつは どこか たのしいところへ いきましょう！", "options": ["しゅうまつは どこか たのしいところへ いきましょう！", "しゅうまつは どこも たのしいところへ いきましょう！", "しゅうまつは どこかで たのしいところへ いきましょう！", "しゅうまつは どこへも たのしいところへ いきましょう！"], "explanation": "どこかへ = to somewhere. ましょう = let's. たのしいところ = a fun place."},
    {"question": "I looked everywhere but couldn't find my keys.", "answer": "どこを さがしても かぎが みつかりませんでした。", "options": ["どこを さがしても かぎが みつかりませんでした。", "どこかを さがしても かぎが みつかりませんでした。", "どこへも さがしても かぎが みつかりませんでした。", "どこでも さがしたが かぎが みつかりませんでした。"], "explanation": "どこを〜ても = no matter where. さがす = to search. みつかりません = can't find."},
    {"question": "Asking someone if they want anything to drink:", "answer": "なにか のみますか。", "options": ["なにか のみますか。", "なにも のみますか。", "なにでも のみますか。", "なにか のみましたか。"], "explanation": "なにか = something/anything (in question). のみますか = will you drink?"},
    {"question": "Nobody was absent from class today.", "answer": "きょうは だれも やすみませんでした。", "options": ["きょうは だれも やすみませんでした。", "きょうは だれか やすみませんでした。", "きょうは だれでも やすみませんでした。", "きょうは だれも やすみました。"], "explanation": "だれも+negative = nobody. やすむ = to be absent/rest."},
    {"question": "I want to live somewhere quiet and green.", "answer": "どこか しずかで みどりの おおい ところに すみたいです。", "options": ["どこか しずかで みどりの おおい ところに すみたいです。", "どこも しずかで みどりの おおい ところに すみたいです。", "どこかへ しずかで みどりの おおい ところに すみたいです。", "どこかで しずかで みどりの おおい ところに すみたいです。"], "explanation": "どこかに = somewhere (location). すみたい = want to live. に marks destination."},
    {"question": "Did anyone see my umbrella?", "answer": "だれか わたしの かさを みましたか。", "options": ["だれか わたしの かさを みましたか。", "だれも わたしの かさを みましたか。", "だれかが わたしの かさを みませんでしたか。", "だれでも わたしの かさを みましたか。"], "explanation": "だれか = someone/anyone. みましたか = did you see?"},
]

# ── Ch12: もう昼ごはんを食べましたか ────────────────────────────────────

ch12_grammar_add = [
    {"question": "もう しゅくだいを _____か。(Have you already done your homework?)", "answer": "しましたか", "options": ["しましたか", "しますか", "するか", "しているか"], "explanation": "もう+〜ましたか = have you already done ~? もう = already (in questions)."},
    {"question": "テーブルに はなを _____おきました。(I have put flowers on the table (in advance).)", "answer": "かって", "options": ["かって", "かき", "かいて", "かけて"], "explanation": "〜ておきます = do something in advance/preparation. かう→かって."},
    {"question": "まだ ひるごはんを _____。(I haven't eaten lunch yet.)", "answer": "たべていません", "options": ["たべていません", "たべませんでした", "たべません", "たべませんか"], "explanation": "まだ+〜ていません = haven't done yet. まだ = not yet (with negative)."},
    {"question": "でんきが _____ あります。(The light has been left on.)", "answer": "ついて", "options": ["ついて", "きって", "けして", "つけて"], "explanation": "〜てあります = result of a deliberate action remains. ついてあります = the light is on."},
    {"question": "かいぎの まえに しりょうを _____おきましょう。(Let's prepare the materials before the meeting.)", "answer": "コピーして", "options": ["コピーして", "みて", "よんで", "かいて"], "explanation": "〜ておく = prepare in advance. コピーしておく = copy ahead of time."},
    {"question": "A: ドアを しめましたか。B: はい、もう _____。(Did you close the door? — Yes, already done.)", "answer": "しめました", "options": ["しめました", "しめます", "しめていません", "しめませんでした"], "explanation": "もう+〜ました = I already did ~. Answer to もう〜ましたか."},
    {"question": "まだ レポートが _____。(The report is not done yet.)", "answer": "できていません", "options": ["できていません", "できません", "できませんでした", "できました"], "explanation": "まだ〜ていません = has not been done yet. できる = to be done/completed."},
    {"question": "てを _____から、ごはんを たべましょう。(Let's eat after washing hands.)", "answer": "あらって", "options": ["あらって", "あらいて", "あらって から", "あらいてから"], "explanation": "〜てから = after doing ~. あらってから = after washing. Note: あらって alone is て-form."},
    {"question": "冷蔵庫に たまごが _____あります。(Eggs have been put in the fridge.)", "answer": "いれて", "options": ["いれて", "かって", "おいて", "のこして"], "explanation": "〜てあります = something has been done (and the result remains). いれてあります = have been placed."},
    {"question": "もう でんしゃが _____。だから おそくなりました。(The train had already left. So I was late.)", "answer": "でていました", "options": ["でていました", "でます", "でていません", "でませんでした"], "explanation": "もう〜ていました = had already ~ (past progressive result). でる = to leave/depart."},
    {"question": "しゅっぱつまえに パスポートを _____おいてください。(Please prepare your passport before departure.)", "answer": "よういして", "options": ["よういして", "かって", "もって", "みて"], "explanation": "〜ておく = prepare in advance. よういする = to prepare. よういしておく = have ready."},
]

ch12_examples_add = [
    {"question": "Asking a colleague 'Have you already sent the email?'", "answer": "もう メールを おくりましたか。", "options": ["もう メールを おくりましたか。", "まだ メールを おくりましたか。", "もう メールを おくりませんか。", "まだ メールを おくりましたか。"], "explanation": "もう+〜ましたか = have you already ~? おくる = to send."},
    {"question": "You haven't eaten dinner yet. How do you say it?", "answer": "まだ ばんごはんを たべていません。", "options": ["まだ ばんごはんを たべていません。", "もう ばんごはんを たべていません。", "まだ ばんごはんを たべませんでした。", "まだ ばんごはんが たべていません。"], "explanation": "まだ+〜ていません = haven't done yet. ていません = haven't done (progressive negative)."},
    {"question": "Saying you've already read that book:", "answer": "その ほんは もう よみました。", "options": ["その ほんは もう よみました。", "その ほんは まだ よみました。", "その ほんは もう よんでいません。", "その ほんは もう よみません。"], "explanation": "もう+〜ました = already did. よむ → よみました = read."},
    {"question": "Preparing for a trip: putting clothes in the suitcase.", "answer": "スーツケースに ふくを いれておきました。", "options": ["スーツケースに ふくを いれておきました。", "スーツケースに ふくを いれてあります。", "スーツケースに ふくを いれました。", "スーツケースに ふくを いれてきました。"], "explanation": "〜ておきました = did something in preparation. Both ておく and てある are natural here."},
    {"question": "Someone asks if you've seen the new movie. Not yet.", "answer": "いいえ、まだ みていません。", "options": ["いいえ、まだ みていません。", "いいえ、もう みていません。", "いいえ、まだ みませんでした。", "いいえ、まだ みません。"], "explanation": "まだ+〜ていません = haven't seen yet. The standard response to もうみましたか."},
    {"question": "The meeting room has been booked (someone booked it).", "answer": "かいぎしつが よやくして あります。", "options": ["かいぎしつが よやくして あります。", "かいぎしつが よやくして います。", "かいぎしつを よやくして あります。", "かいぎしつは よやくして おきます。"], "explanation": "〜てあります = result of deliberate preparation. よやくする = to book/reserve."},
    {"question": "After finishing your meal, you say:", "answer": "ごちそうさまでした。", "options": ["ごちそうさまでした。", "いただきます。", "おつかれさまでした。", "よろしくおねがいします。"], "explanation": "ごちそうさまでした = Thank you for the meal (said after eating). いただきます is said before."},
    {"question": "Before going to bed, you set your alarm.", "answer": "ねる まえに めざましを かけておきました。", "options": ["ねる まえに めざましを かけておきました。", "ねた あとで めざましを かけておきました。", "ねる まえに めざましを かけてありました。", "ねる まえに めざましを かけてしまいました。"], "explanation": "〜まえに = before doing ~. 〜ておく = do in advance for later."},
    {"question": "Did you already pay the bill?", "answer": "もう かいけいを しましたか。", "options": ["もう かいけいを しましたか。", "まだ かいけいを しましたか。", "もう かいけいが ありましたか。", "もう かいけいは しますか。"], "explanation": "もう〜ましたか = have you already ~? かいけい = bill/payment."},
    {"question": "I have to do laundry before going out tomorrow.", "answer": "あした でかける まえに せんたくを しておかなければなりません。", "options": ["あした でかける まえに せんたくを しておかなければなりません。", "あした でかけた あとで せんたくを しておかなければなりません。", "あした でかける まえに せんたくを してしまいました。", "あした でかける まえに せんたくを しておきました。"], "explanation": "まえに+ておかなければなりません = must do (in advance) before ~. せんたく = laundry."},
    {"question": "The windows have been left open (someone opened them).", "answer": "まどが あけて あります。", "options": ["まどが あけて あります。", "まどが あけて います。", "まどを あけて あります。", "まどは あいて あります。"], "explanation": "〜てあります = result of deliberate action by someone. まどがあいています = window is open (state)."},
    {"question": "You haven't decided what to eat yet.", "answer": "まだ なにを たべるか きめていません。", "options": ["まだ なにを たべるか きめていません。", "もう なにを たべるか きめていません。", "まだ なにを たべるか きめませんでした。", "まだ なにが たべるか きめていません。"], "explanation": "まだ〜ていません = haven't done yet. きめる = to decide. なにをたべるか = what to eat."},
    {"question": "I've already called the restaurant to make a reservation.", "answer": "もう レストランに よやくの でんわを しました。", "options": ["もう レストランに よやくの でんわを しました。", "まだ レストランに よやくの でんわを しました。", "もう レストランで よやくの でんわを しました。", "もう レストランを よやくの でんわを しました。"], "explanation": "もう+〜ました = already did. に = to (recipient). よやく = reservation."},
    {"question": "Leaving a note: 'I have left your lunch in the fridge.'", "answer": "ひるごはんを れいぞうこに いれておきました。", "options": ["ひるごはんを れいぞうこに いれておきました。", "ひるごはんが れいぞうこに いれておきました。", "ひるごはんを れいぞうこで いれておきました。", "ひるごはんは れいぞうこに いれてありました。"], "explanation": "〜ておきました = did in advance. れいぞうこ = refrigerator. に = in (location)."},
    {"question": "Before the test: 'Have you reviewed all the vocabulary?'", "answer": "もう たんごを ぜんぶ おさらいしましたか。", "options": ["もう たんごを ぜんぶ おさらいしましたか。", "まだ たんごを ぜんぶ おさらいしましたか。", "もう たんごが ぜんぶ おさらいしましたか。", "もう たんごは ぜんぶ おさらいしますか。"], "explanation": "もう〜ましたか = have you already ~? おさらい = review. ぜんぶ = all."},
    {"question": "The chairs have been arranged in a circle for the meeting.", "answer": "いすが えんけいに ならべて あります。", "options": ["いすが えんけいに ならべて あります。", "いすが えんけいに ならべて います。", "いすを えんけいに ならべて あります。", "いすは えんけいに ならんで あります。"], "explanation": "〜てあります = has been done (preparation). ならべる = to arrange. えんけい = circle."},
]

# ── Ch13: 先週映画を見ました ─────────────────────────────────────────────

ch13_grammar_add = [
    {"question": "ごはんを たべる _____に ては を あらいます。(I wash my hands before eating.)", "answer": "まえ", "options": ["まえ", "あと", "とき", "ながら"], "explanation": "〜まえに = before doing ~. Verb (dict form)+まえに."},
    {"question": "にほんに きた _____で、ふじさんに のぼりました。(After coming to Japan, I climbed Mt Fuji.)", "answer": "あと", "options": ["あと", "まえ", "とき", "から"], "explanation": "〜たあとで = after doing ~. Verb (past)+あとで."},
    {"question": "にほんへ _____ことが ありますか。(Have you ever been to Japan?)", "answer": "いった", "options": ["いった", "いく", "いって", "いき"], "explanation": "〜たことがある = have ever done ~. Past experience. Verb (past form)+ことがある."},
    {"question": "かいものを した _____で コーヒーを のみました。(After shopping, I drank coffee.)", "answer": "あと", "options": ["あと", "まえ", "ながら", "から"], "explanation": "〜したあとで = after doing ~. あとで shows sequence."},
    {"question": "いちど ピアノを _____たことが あります。(I have played piano once before.)", "answer": "ひい", "options": ["ひい", "ひき", "ひいて", "ひく"], "explanation": "ひく→ひいた+ことがある. Past tense stem for experience."},
    {"question": "にほんりょうりを つくった _____が ありますか。(Have you ever cooked Japanese food?)", "answer": "こと", "options": ["こと", "もの", "とき", "ため"], "explanation": "〜たことがある = have ever done ~. こと nominalizes the verb phrase."},
    {"question": "ねる まえに はを _____。(I brush my teeth before sleeping.)", "answer": "みがきます", "options": ["みがきます", "みがいて", "みがいた", "みがく"], "explanation": "Routine habit: ねるまえに+verb (present). はをみがく = brush teeth."},
    {"question": "しけんが おわった _____、みんなで ごはんを たべました。", "answer": "あと", "options": ["あと", "まえ", "とき", "から"], "explanation": "〜たあと = after doing ~. Shows sequential past events."},
    {"question": "にほんご を べんきょうした _____が ありますか。——はい、3ねんぐらい あります。", "answer": "こと", "options": ["こと", "もの", "とき", "ため"], "explanation": "〜したことがありますか = have you ever done ~? Answer: はい、あります / いいえ、ありません."},
    {"question": "でかける まえに、でんきを _____ください。(Please turn off the lights before going out.)", "answer": "けして", "options": ["けして", "つけて", "しめて", "あけて"], "explanation": "けす→けして (て-form: turn off). まえに = before. てください = please."},
    {"question": "ごはんを たべた _____、はを みがきます。(After eating, I brush my teeth.)", "answer": "あと", "options": ["あと", "まえ", "とき", "ながら"], "explanation": "たべたあと = after eating. Sequential daily routine."},
    {"question": "かれは にほんに すんだ _____が あります。(He has lived in Japan before.)", "answer": "こと", "options": ["こと", "もの", "とき", "ため"], "explanation": "〜たことがある = has done before (experience). すんだ = lived (past of すむ)."},
    {"question": "べんきょうする _____に、ちょっと やすみましょう。(Before studying, let's take a short break.)", "answer": "まえ", "options": ["まえ", "あと", "から", "とき"], "explanation": "〜まえに = before doing. Dictionary form + まえに."},
    {"question": "はじめて にほんりょうりを _____とき、とても おどろきました。", "answer": "たべた", "options": ["たべた", "たべる", "たべて", "たべない"], "explanation": "〜たとき = when [past]. 〜るとき = when [present/future]. Here past: first time eating."},
    {"question": "スカイツリーに _____ことが ありますか。——はい、一度あります。", "answer": "のぼった", "options": ["のぼった", "のぼる", "のぼって", "のぼり"], "explanation": "のぼる(climb)→のぼった+ことがある = have climbed. 一度 = once."},
]

ch13_examples_add = [
    {"question": "Saying 'I have never eaten sushi before.'", "answer": "すしを たべたことが ありません。", "options": ["すしを たべたことが ありません。", "すしを たべたことが あります。", "すしを たべることが ありません。", "すしを たべることが あります。"], "explanation": "〜たことがない = have never done. Negative of experience."},
    {"question": "Saying 'I brush my teeth before going to bed.'", "answer": "ねる まえに はを みがきます。", "options": ["ねる まえに はを みがきます。", "ねた あとで はを みがきます。", "ねる あとで はを みがきます。", "ねた まえに はを みがきます。"], "explanation": "まえに = before doing. Dictionary form + まえに (not past tense)."},
    {"question": "After finishing work, I go to the gym.", "answer": "しごとが おわった あとで、ジムに いきます。", "options": ["しごとが おわった あとで、ジムに いきます。", "しごとが おわる まえに、ジムに いきます。", "しごとが おわったとき、ジムに いきます。", "しごとが おわってから、ジムに いきます。"], "explanation": "〜たあとで = after doing. Both あとで and てから work here."},
    {"question": "Asking if someone has ever been to Kyoto:", "answer": "きょうとに いったことが ありますか。", "options": ["きょうとに いったことが ありますか。", "きょうとに いくことが ありますか。", "きょうとに いったことを ありますか。", "きょうとに いくことを ありますか。"], "explanation": "〜たことがあります = have been (experience). いった = went (past of いく)."},
    {"question": "Saying 'I have seen this movie three times.'", "answer": "この えいがを さんかい みたことが あります。", "options": ["この えいがを さんかい みたことが あります。", "この えいがを さんかい みることが あります。", "この えいがを さんかい みたことを あります。", "この えいがを さんかい みています。"], "explanation": "〜たことがあります = have done (experience). さんかい = 3 times."},
    {"question": "Please check your bag before leaving the house.", "answer": "うちを でる まえに、かばんを たしかめてください。", "options": ["うちを でる まえに、かばんを たしかめてください。", "うちを でた あとで、かばんを たしかめてください。", "うちを でた まえに、かばんを たしかめてください。", "うちを でる あとで、かばんを たしかめてください。"], "explanation": "まえに = before. Dictionary form + まえに. たしかめる = to check/confirm."},
    {"question": "I have never driven a car.", "answer": "くるまを うんてんした ことが ありません。", "options": ["くるまを うんてんした ことが ありません。", "くるまを うんてんする ことが ありません。", "くるまを うんてんした ことが あります。", "くるまは うんてんした ことが ありません。"], "explanation": "〜たことがない = have never done. うんてんする = to drive."},
    {"question": "After arriving at the hotel, call me.", "answer": "ホテルに ついたあとで、でんわを してください。", "options": ["ホテルに ついたあとで、でんわを してください。", "ホテルに つく まえに、でんわを してください。", "ホテルに ついた まえに、でんわを してください。", "ホテルに つく あとで、でんわを してください。"], "explanation": "〜たあとで = after doing. つく = to arrive. てください = please."},
    {"question": "Have you ever eaten natto? It's a Japanese food.", "answer": "なっとうを たべたことが ありますか。にほんの たべものですよ。", "options": ["なっとうを たべたことが ありますか。", "なっとうを たべることが ありますか。", "なっとうを たべましたか。", "なっとうを たべていますか。"], "explanation": "〜たことがありますか = have you ever done ~? Experience question."},
    {"question": "I checked my email after waking up.", "answer": "おきた あとで、メールを チェックしました。", "options": ["おきた あとで、メールを チェックしました。", "おきる まえに、メールを チェックしました。", "おきた まえに、メールを チェックしました。", "おきる あとで、メールを チェックしました。"], "explanation": "〜たあとで = after doing. おきる → おきた (past)."},
    {"question": "I had never heard this song before.", "answer": "この うたを きいたことが ありませんでした。", "options": ["この うたを きいたことが ありませんでした。", "この うたを きいたことが ありません。", "この うたを きくことが ありませんでした。", "この うたは きいたことが ありませんでした。"], "explanation": "Past negative experience: 〜たことがありませんでした. きく = to hear/listen."},
    {"question": "Before submitting, please read through the report.", "answer": "ていしゅつする まえに、レポートを よんでください。", "options": ["ていしゅつする まえに、レポートを よんでください。", "ていしゅつした あとで、レポートを よんでください。", "ていしゅつする あとで、レポートを よんでください。", "ていしゅつした まえに、レポートを よんでください。"], "explanation": "まえに = before. Dictionary form + まえに. ていしゅつ = submission."},
    {"question": "I've ridden a horse once.", "answer": "いちど うまに のったことが あります。", "options": ["いちど うまに のったことが あります。", "いちど うまを のったことが あります。", "いちど うまに のることが あります。", "いちど うまで のったことが あります。"], "explanation": "に = on (riding). 〜たことがある = have done once. いちど = once."},
    {"question": "After finishing the exam, let's go eat something good.", "answer": "しけんが おわったあとで、なにかおいしいものを たべに いきましょう。", "options": ["しけんが おわったあとで、なにかおいしいものを たべに いきましょう。", "しけんが おわるまえに、なにかおいしいものを たべに いきましょう。", "しけんが おわったとき、なにかおいしいものを たべに いきましょう。", "しけんが おわってから、なにかおいしいものを たべに いきましょう。"], "explanation": "あとで = after. なにかおいしいもの = something delicious. たべにいく = go to eat."},
    {"question": "Have you ever tried making Japanese food yourself?", "answer": "じぶんで にほんりょうりを つくったことが ありますか。", "options": ["じぶんで にほんりょうりを つくったことが ありますか。", "じぶんで にほんりょうりを つくることが ありますか。", "じぶんで にほんりょうりが つくったことが ありますか。", "じぶんで にほんりょうりを つくったことを ありますか。"], "explanation": "じぶんで = by yourself. 〜たことがありますか = have you ever done ~?"},
]

# ── Ch14: 今何をしていますか ─────────────────────────────────────────────

ch14_grammar_add = [
    {"question": "いま なにを して _____か。(What are you doing now?)", "answer": "います", "options": ["います", "あります", "おきます", "します"], "explanation": "〜ています = is doing (progressive). します→しています. います for living things/ongoing action."},
    {"question": "かのじょは いま でんわで はなして _____。(She is talking on the phone now.)", "answer": "います", "options": ["います", "あります", "いません", "おきます"], "explanation": "〜ています = progressive. はなしています = is talking."},
    {"question": "たなかさんは もう けっこん して _____。(Mr Tanaka is already married.)", "answer": "います", "options": ["います", "あります", "きます", "いきます"], "explanation": "〜ています can also express a resultant state. けっこんしています = is married."},
    {"question": "さとうさんは いま でかけて _____。(Ms Sato has gone out/is out.)", "answer": "います", "options": ["います", "あります", "いません", "ありません"], "explanation": "でかけています = has gone out and is away (resultant state)."},
    {"question": "はなが さいて _____。(The flowers are blooming.)", "answer": "います", "options": ["います", "あります", "きます", "いきます"], "explanation": "〜ています = state/ongoing. さいています = is blooming (state of flower)."},
    {"question": "いまから でんわを かける _____ですが、いま よろしいですか。", "answer": "ところ", "options": ["ところ", "こと", "もの", "ため"], "explanation": "〜ところです = about to do / just doing. いまからかけるところ = about to call."},
    {"question": "ちょうど ひるごはんを たべて _____ところです。(I am just eating lunch now.)", "answer": "いる", "options": ["いる", "ある", "いない", "くる"], "explanation": "〜ているところです = is in the middle of doing."},
    {"question": "あの ひとは たなかさんを _____ていますか。(Do you know that person?)", "answer": "しっ", "options": ["しっ", "みて", "きいて", "よんで"], "explanation": "しる→しっています = know (resultant state). Not しています."},
    {"question": "かれは がいしゃに _____います。(He works at a company — is employed.)", "answer": "つとめて", "options": ["つとめて", "はたらいて", "いって", "きて"], "explanation": "つとめています = is employed at. Resultant state from getting a job."},
    {"question": "スミスさんは いま にほんごを _____ています。(Mr Smith is studying Japanese.)", "answer": "べんきょうし", "options": ["べんきょうし", "べんきょう", "べんきょうして", "べんきょうする"], "explanation": "べんきょうしています = is studying. する→して+います."},
    {"question": "でんしゃが _____ています。(The train is running/in service.)", "answer": "はしっ", "options": ["はしっ", "きて", "いって", "とまっ"], "explanation": "はしる→はしっています = is running. Progressive of movement."},
    {"question": "あのみせは いまも _____ていますか。(Is that store still open?)", "answer": "あいて", "options": ["あいて", "しまって", "きて", "いって"], "explanation": "あく→あいています = is open (resultant state). しまっています = is closed."},
    {"question": "いもうとは もう ねて _____。(My younger sister is already asleep.)", "answer": "います", "options": ["います", "あります", "きます", "いきます"], "explanation": "ねています = is sleeping (ongoing state)."},
    {"question": "いま でんしゃに _____ので、あとで かけなおします。(I'm on the train now so I'll call back later.)", "answer": "のって", "options": ["のって", "はいって", "すわって", "きて"], "explanation": "のっています = is on (the train). のる→のって+います. State of being on transport."},
]

ch14_examples_add = [
    {"question": "Someone calls. You're eating. What do you say?", "answer": "いま ごはんを たべています。", "options": ["いま ごはんを たべています。", "いま ごはんを たべました。", "いま ごはんを たべます。", "いま ごはんが たべています。"], "explanation": "〜ています = currently doing (progressive). いま = now."},
    {"question": "Asking what your friend is doing right now:", "answer": "いま なにを していますか。", "options": ["いま なにを していますか。", "いま なにを しましたか。", "いま なにを しますか。", "いま なにを するか。"], "explanation": "〜ていますか = what are you doing? Progressive question."},
    {"question": "You are looking for your glasses. 'I am looking for my glasses.'", "answer": "めがねを さがしています。", "options": ["めがねを さがしています。", "めがねを さがしました。", "めがねを さがします。", "めがねが さがしています。"], "explanation": "さがしています = am looking for (ongoing action)."},
    {"question": "Telling someone that the restaurant is closed now.", "answer": "そのレストランは いまは しまっています。", "options": ["そのレストランは いまは しまっています。", "そのレストランは いまは しまりました。", "そのレストランは いまは しまります。", "そのレストランは いまは あいています。"], "explanation": "しまっています = is closed (resultant state). あいています = is open."},
    {"question": "Asking 'Where does your father work?'", "answer": "おとうさんは どこに つとめていますか。", "options": ["おとうさんは どこに つとめていますか。", "おとうさんは どこで はたらいていますか。", "おとうさんは どこを つとめていますか。", "おとうさんは どこに はたらいていますか。"], "explanation": "つとめています = is employed at. Both つとめる and はたらく work; つとめる implies a specific organization."},
    {"question": "The teacher is writing on the blackboard.", "answer": "せんせいは こくばんに かいています。", "options": ["せんせいは こくばんに かいています。", "せんせいは こくばんを かいています。", "せんせいは こくばんで かいています。", "せんせいは こくばんが かいています。"], "explanation": "に marks the surface written on. かいています = is writing (progressive)."},
    {"question": "Telling a caller you'll call back because you're in a meeting.", "answer": "いま かいぎ中ですので、あとで おかけなおします。", "options": ["いま かいぎ中ですので、あとで おかけなおします。", "いま かいぎを していますので、あとで おかけなおします。", "いま かいぎ中ですから、あとで かけなおします。", "いま かいぎ中なので、あとで おかけなおします。"], "explanation": "かいぎ中 = in a meeting. ので = because (polite reason). おかけなおします = will call back (polite)."},
    {"question": "I already know that information.", "answer": "その じょうほうは もう しっています。", "options": ["その じょうほうは もう しっています。", "その じょうほうは もう しります。", "その じょうほうは もう しりました。", "その じょうほうは もう しっていません。"], "explanation": "しっています = know (resultant state). NOT しります."},
    {"question": "Children are playing in the park.", "answer": "こどもたちが こうえんで あそんでいます。", "options": ["こどもたちが こうえんで あそんでいます。", "こどもたちが こうえんに あそんでいます。", "こどもたちが こうえんを あそんでいます。", "こどもたちが こうえんで あそびます。"], "explanation": "で = at (place of action). あそんでいます = are playing (progressive)."},
    {"question": "My older brother is living in Tokyo.", "answer": "あには とうきょうに すんでいます。", "options": ["あには とうきょうに すんでいます。", "あには とうきょうで すんでいます。", "あには とうきょうを すんでいます。", "あには とうきょうが すんでいます。"], "explanation": "に = at (location of living). すんでいます = lives/is living (resultant state)."},
    {"question": "The dog is sleeping in front of the door.", "answer": "いぬが ドアの まえで ねています。", "options": ["いぬが ドアの まえで ねています。", "いぬが ドアの まえに ねています。", "いぬが ドアの まえを ねています。", "いぬが ドアの まえは ねています。"], "explanation": "で = at (place of action). まえ = in front. ねています = is sleeping."},
    {"question": "Telling a friend you're almost there (on the way).", "answer": "いま むかっています。もうすぐ つきます。", "options": ["いま むかっています。もうすぐ つきます。", "いま むかいます。もうすぐ つきます。", "いま むかっていました。もうすぐ つきます。", "いま むかっています。すぐ つきました。"], "explanation": "むかっています = is heading toward. もうすぐ = very soon. つきます = will arrive."},
    {"question": "I am tired because I've been standing for a long time.", "answer": "ながい あいだ たっていたので、つかれました。", "options": ["ながい あいだ たっていたので、つかれました。", "ながい あいだ たっているので、つかれました。", "ながい あいだ たっていたから、つかれます。", "ながい あいだ たつので、つかれました。"], "explanation": "たっていた = was standing (past progressive). ので = because. つかれました = got tired."},
    {"question": "She's been going to the same company for 10 years.", "answer": "かのじょは 10ねんかん おなじ かいしゃに つとめています。", "options": ["かのじょは 10ねんかん おなじ かいしゃに つとめています。", "かのじょは 10ねんかん おなじ かいしゃで つとめています。", "かのじょは 10ねんかん おなじ かいしゃを つとめています。", "かのじょは 10ねんかん おなじ かいしゃが つとめています。"], "explanation": "に = at (organization). つとめています = is employed. 〜かん = for [duration]."},
]

# ── Ch15: 少し疲れました ─────────────────────────────────────────────────

ch15_grammar_add = [
    {"question": "くすりを のま_____なりません。(I must take medicine.)", "answer": "なければ", "options": ["なければ", "ないで", "なくて", "なくても"], "explanation": "〜なければなりません = must do. Verb negative stem + なければなりません."},
    {"question": "あした までに レポートを ださ_____ならない。(I must submit the report by tomorrow.)", "answer": "なければ", "options": ["なければ", "ないと", "なくても", "なくて"], "explanation": "だす→ださなければならない. Must submit (obligation)."},
    {"question": "むりを しては _____。(You must not overwork yourself.)", "answer": "いけません", "options": ["いけません", "いいです", "なりません", "かまいません"], "explanation": "〜てはいけません = must not. むりをする = to overdo things."},
    {"question": "きょうは はやく ねなければ _____。(I must sleep early today.)", "answer": "なりません", "options": ["なりません", "いけません", "いいです", "かまいません"], "explanation": "〜なければなりません. なければ + なりません = must. Obligation."},
    {"question": "いちにちじゅう あるいて、すこし つかれ_____。(I walked all day and got a little tired.)", "answer": "ました", "options": ["ました", "ています", "てしまいました", "ません"], "explanation": "つかれました = got tired (past). Simple past result."},
    {"question": "パスポートを もって いか_____ならない。(I must bring my passport.)", "answer": "なければ", "options": ["なければ", "なくても", "ないで", "なくて"], "explanation": "いく→いかなければならない. Must go (with obligation)."},
    {"question": "この くすりは まずかった ですが、飲ま_____なりませんでした。", "answer": "なければ", "options": ["なければ", "なくて", "ないで", "なくても"], "explanation": "〜なければなりませんでした = had to do (past obligation)."},
    {"question": "むりを しなくても _____。(You don't have to force yourself.)", "answer": "いいです", "options": ["いいです", "なりません", "いけません", "かまいません"], "explanation": "〜なくてもいいです = don't need to. Absence of obligation."},
    {"question": "きんえんです。タバコを すっては _____。", "answer": "いけません", "options": ["いけません", "なりません", "いいです", "かまいません"], "explanation": "きんえん = no smoking. 〜てはいけません = prohibited."},
    {"question": "にほんに すむなら、にほんごを べんきょうしなければ_____。", "answer": "なりません", "options": ["なりません", "いけません", "いいです", "かまいません"], "explanation": "〜なければなりません = must. なら = if. Conditional obligation."},
    {"question": "あした 8じに くるひつようが _____。(You don't need to come at 8 tomorrow.)", "answer": "ありません", "options": ["ありません", "なりません", "いけません", "います"], "explanation": "〜ひつようがありません = no need to. Absence of necessity."},
    {"question": "かれは びょうきなので、しごとを やすまなければ _____。", "answer": "なりません", "options": ["なりません", "いけません", "いいです", "かまいません"], "explanation": "〜なければなりません = must. やすむ = to take a rest/day off."},
    {"question": "もう おそいですね。そろそろ かえらなければ _____。", "answer": "なりません", "options": ["なりません", "いけません", "いいです", "かまいません"], "explanation": "そろそろ = soon/about time. かえらなければなりません = must go home."},
    {"question": "そのルールは まもらなければ _____。(Those rules must be followed.)", "answer": "なりません", "options": ["なりません", "いけません", "なくていいです", "かまいません"], "explanation": "まもる = to follow (rules). まもらなければなりません = must follow."},
    {"question": "かぜを ひいて しまいました。むりを _____なかった のに。", "answer": "し", "options": ["し", "させ", "させて", "して"], "explanation": "してしまいました = ended up doing (regret). のに = even though / despite that."},
]

ch15_examples_add = [
    {"question": "You're sick. Telling someone you have to take medicine.", "answer": "くすりを のまなければ なりません。", "options": ["くすりを のまなければ なりません。", "くすりを のまなくても いいです。", "くすりを のんでは いけません。", "くすりを のんでも かまいません。"], "explanation": "〜なければなりません = must. のむ = to take/drink."},
    {"question": "You don't need to bring anything to the party.", "answer": "パーティーに なにも もってこなくても いいです。", "options": ["パーティーに なにも もってこなくても いいです。", "パーティーに なにも もってこなければ なりません。", "パーティーに なにも もってきては いけません。", "パーティーに なにか もってこなくても いいです。"], "explanation": "〜なくてもいいです = don't need to. もってくる = to bring."},
    {"question": "Telling a child they must not run inside the library.", "answer": "としょかんの なかで はしっては いけません。", "options": ["としょかんの なかで はしっては いけません。", "としょかんの なかで はしらなければ なりません。", "としょかんの なかで はしらなくても いいです。", "としょかんの なかで はしっても いいです。"], "explanation": "〜てはいけません = must not. はしる = to run."},
    {"question": "You accidentally deleted an important file.", "answer": "たいせつな ファイルを けして しまいました。", "options": ["たいせつな ファイルを けして しまいました。", "たいせつな ファイルを けしては いけません。", "たいせつな ファイルを けして ください。", "たいせつな ファイルを けさなければ なりません。"], "explanation": "〜てしまいました = accidentally did / did regrettably. けす = to delete."},
    {"question": "You don't have to wear a tie at this company.", "answer": "この かいしゃでは ネクタイを しなくても いいです。", "options": ["この かいしゃでは ネクタイを しなくても いいです。", "この かいしゃでは ネクタイを しなければ なりません。", "この かいしゃでは ネクタイを しては いけません。", "この かいしゃでは ネクタイを しても かまいません。"], "explanation": "〜なくてもいいです = no need to. ネクタイをする = to wear a tie."},
    {"question": "You have to submit your report by Friday.", "answer": "きんようびまでに レポートを ださなければ なりません。", "options": ["きんようびまでに レポートを ださなければ なりません。", "きんようびまでに レポートを ださなくても いいです。", "きんようびまでに レポートを だしては いけません。", "きんようびまでに レポートを だして しまいました。"], "explanation": "〜までに = by (deadline). ださなければなりません = must submit."},
    {"question": "I accidentally bought the wrong size.", "answer": "まちがった サイズを かって しまいました。", "options": ["まちがった サイズを かって しまいました。", "まちがった サイズを かわなければ なりません。", "まちがった サイズを かっては いけません。", "まちがった サイズを かなくても いいです。"], "explanation": "〜てしまう = accidentally/regrettably did. まちがった = wrong/mistaken."},
    {"question": "Students must arrive by 9am.", "answer": "がくせいは 9じまでに こなければ なりません。", "options": ["がくせいは 9じまでに こなければ なりません。", "がくせいは 9じまでに こなくても いいです。", "がくせいは 9じまでに きては いけません。", "がくせいは 9じまでに きても かまいません。"], "explanation": "〜までに = by. こなければなりません = must come. くる→こ+なければ."},
    {"question": "You don't have to return the book today.", "answer": "きょうは ほんを かえさなくても いいです。", "options": ["きょうは ほんを かえさなくても いいです。", "きょうは ほんを かえさなければ なりません。", "きょうは ほんを かえしては いけません。", "きょうは ほんを かえして しまいました。"], "explanation": "かえす = to return. 〜なくてもいいです = don't need to."},
    {"question": "You forgot your homework. Explaining to the teacher.", "answer": "しゅくだいを わすれて しまいました。すみません。", "options": ["しゅくだいを わすれて しまいました。すみません。", "しゅくだいを わすれなければ なりません。", "しゅくだいを わすれては いけません。", "しゅくだいを わすれなくても いいです。"], "explanation": "〜てしまいました = regrettably did. わすれる = to forget."},
    {"question": "You need to save money for the trip.", "answer": "りょこうのために おかねを ためなければ なりません。", "options": ["りょこうのために おかねを ためなければ なりません。", "りょこうのために おかねを ためなくても いいです。", "りょこうのために おかねを ためては いけません。", "りょこうのために おかねを ためて しまいました。"], "explanation": "〜ために = for the purpose of. ためる = to save (money). なければなりません = must."},
    {"question": "You must not park your bicycle here.", "answer": "ここに じてんしゃを とめては いけません。", "options": ["ここに じてんしゃを とめては いけません。", "ここに じてんしゃを とめなければ なりません。", "ここに じてんしゃを とめなくても いいです。", "ここに じてんしゃを とめて しまいました。"], "explanation": "〜てはいけません = must not. とめる = to park. じてんしゃ = bicycle."},
    {"question": "You ate too much and feel sick.", "answer": "たべすぎて しまって、きぶんが わるいです。", "options": ["たべすぎて しまって、きぶんが わるいです。", "たべすぎては いけなくて、きぶんが わるいです。", "たべすぎなければ ならなくて、きぶんが わるいです。", "たべなくても いいのに、きぶんが わるいです。"], "explanation": "〜てしまう = regrettably did. すぎる = too much. きぶんがわるい = feel sick."},
    {"question": "You must go to the hospital because you have a fever.", "answer": "ねつが あるので、びょういんに いかなければ なりません。", "options": ["ねつが あるので、びょういんに いかなければ なりません。", "ねつが あるので、びょういんに いかなくても いいです。", "ねつが あるので、びょういんに いっては いけません。", "ねつが あるので、びょういんに いって しまいました。"], "explanation": "ので = because. いかなければなりません = must go."},
    {"question": "You don't have to clean your room today.", "answer": "きょうは へやを そうじしなくても いいです。", "options": ["きょうは へやを そうじしなくても いいです。", "きょうは へやを そうじしなければ なりません。", "きょうは へやを そうじしては いけません。", "きょうは へやを そうじして しまいました。"], "explanation": "〜なくてもいいです = don't have to. そうじする = to clean."},
    {"question": "I accidentally lost my train pass.", "answer": "ていきけんを なくして しまいました。", "options": ["ていきけんを なくして しまいました。", "ていきけんを なくさなければ なりません。", "ていきけんを なくしては いけません。", "ていきけんを なくさなくても いいです。"], "explanation": "〜てしまいました = accidentally/regrettably. なくす = to lose. ていきけん = commuter pass."},
]

# ── Ch16: 荷物を送りたいんですが ─────────────────────────────────────────

ch16_grammar_add = [
    {"question": "にほんへ _____たいです。(I want to go to Japan.)", "answer": "いき", "options": ["いき", "いって", "いく", "いか"], "explanation": "〜たい = want to do. Verb masu-stem+たい. いきます→いき+たい."},
    {"question": "なにか のみ_____んですが。(I'd like something to drink.)", "answer": "たい", "options": ["たい", "ます", "ません", "たかった"], "explanation": "〜たいんですが = I'd like to ~ (soft request). より polite than 〜たいです."},
    {"question": "ちょっと そうだんが _____んですが。(I have something I'd like to consult about.)", "answer": "ある", "options": ["ある", "ない", "いい", "たい"], "explanation": "〜があるんですが = I have something [to discuss]. んですが softens the statement."},
    {"question": "にほんごが じょうず_____なりたいです。(I want to become good at Japanese.)", "answer": "に", "options": ["に", "が", "で", "は"], "explanation": "〜になりたい = want to become ~. に marks the goal state."},
    {"question": "すみません、えきへの みちを おし_____んですが。", "answer": "えて いただき たい", "options": ["えて いただき たい", "えて ください", "えて もらいたい", "えましょう"], "explanation": "〜ていただきたいんですが = I would like you to ~ (polite request using たい)."},
    {"question": "このにもつを おおさかへ おくり_____んですが。(I'd like to send this luggage to Osaka.)", "answer": "たい", "options": ["たい", "ます", "ません", "たかった"], "explanation": "〜たいんですが = I want to / I'd like to. おくる = to send."},
    {"question": "しょうらい せんせいに _____たいと おもっています。(I am thinking of becoming a teacher.)", "answer": "なり", "options": ["なり", "なって", "なれ", "なる"], "explanation": "〜たいとおもっています = is thinking of wanting to. 〜になりたい = want to become."},
    {"question": "もっと にほんの ぶんかを し_____たいです。(I want to know more about Japanese culture.)", "answer": "り", "options": ["り", "って", "らない", "る"], "explanation": "しる→しり+たい. Want to know. Irregular: しる→知りたい not しりたい."},
    {"question": "いつか ひとりで りょこうが し_____と おもっています。", "answer": "たい", "options": ["たい", "ます", "ません", "なかった"], "explanation": "〜たいとおもっています = am thinking of wanting to do. ひとりで = alone."},
    {"question": "なにか れんらく_____ことが あったら、でんわしてください。", "answer": "したい", "options": ["したい", "する", "した", "します"], "explanation": "〜することがあったら = if there's something to ~. れんらくしたい = want to contact."},
    {"question": "ちょっと きいて_____んですが、この あたりに ATM は ありますか。", "answer": "いい", "options": ["いい", "たい", "ほしい", "ください"], "explanation": "きいていいんですが = may I ask? んですが softens the question."},
    {"question": "かのじょは かいしゃを やめて、りょうりきょうしつを ひらき_____そうです。", "answer": "たい", "options": ["たい", "ます", "ません", "たかった"], "explanation": "〜たいそうです = I hear she wants to. Hearsay + desire."},
    {"question": "いちど ぜひ いっしょに たべに_____んですが。", "answer": "いきたい", "options": ["いきたい", "いきます", "いきません", "いきました"], "explanation": "〜たいんですが = I'd like to. たべにいく = go to eat. Combined with たい."},
    {"question": "もっと すいみんを とり_____のに、いつも おそくまで おきています。", "answer": "たい", "options": ["たい", "ます", "ません", "ない"], "explanation": "〜たいのに = even though I want to. Expressing frustration about unmet desire."},
    {"question": "すみません、こちらの にほんしゅを 2ほん い_____んですが。", "answer": "ただき たい", "options": ["ただき たい", "ください", "もらい たい", "ほしい"], "explanation": "いただきたいんですが = I would like to receive (polite). にほんしゅ = sake."},
]

ch16_examples_add = [
    {"question": "You want to send a package to your family in Nepal.", "answer": "かぞくに にもつを おくりたいんですが。", "options": ["かぞくに にもつを おくりたいんですが。", "かぞくに にもつを おくりますが。", "かぞくに にもつを おくってください。", "かぞくに にもつを おくりませんが。"], "explanation": "〜たいんですが = I'd like to ~ (soft, polite want). Used at shops/post office."},
    {"question": "You want to become a doctor in the future.", "answer": "しょうらい いしゃに なりたいです。", "options": ["しょうらい いしゃに なりたいです。", "しょうらい いしゃが なりたいです。", "しょうらい いしゃで なりたいです。", "しょうらい いしゃを なりたいです。"], "explanation": "〜になりたい = want to become ~. に marks the goal. しょうらい = in the future."},
    {"question": "At a bank: 'I'd like to open an account.'", "answer": "こうざを ひらきたいんですが。", "options": ["こうざを ひらきたいんですが。", "こうざを ひらきますが。", "こうざを ひらいてください。", "こうざを ひらきませんか。"], "explanation": "〜たいんですが = I'd like to (introducing a request at a counter). こうざ = bank account."},
    {"question": "Expressing your dream: 'I want to travel the world.'", "answer": "せかいを りょこうしたいと おもっています。", "options": ["せかいを りょこうしたいと おもっています。", "せかいを りょこうしたいです。", "せかいを りょこうしますと おもっています。", "せかいを りょこうしたいとおもいます。"], "explanation": "〜たいとおもっています = am thinking of wanting to (ongoing thought/plan)."},
    {"question": "At a restaurant: 'I'd like to order, please.'", "answer": "ちゅうもんを したいんですが。", "options": ["ちゅうもんを したいんですが。", "ちゅうもんを します。", "ちゅうもんを してください。", "ちゅうもんが したいです。"], "explanation": "〜たいんですが = I'd like to. Used as a polite opener for a request."},
    {"question": "You want to speak to the manager.", "answer": "マネージャーに はなしたいんですが。", "options": ["マネージャーに はなしたいんですが。", "マネージャーを はなしたいんですが。", "マネージャーが はなしたいんですが。", "マネージャーで はなしたいんですが。"], "explanation": "に = to (person). はなしたいんですが = I'd like to speak to ~."},
    {"question": "I want to try living abroad someday.", "answer": "いつか がいこくに すんで みたいです。", "options": ["いつか がいこくに すんで みたいです。", "いつか がいこくで すんで みたいです。", "いつか がいこくを すんで みたいです。", "いつか がいこくが すんで みたいです。"], "explanation": "〜てみたい = want to try doing. に = in (living location). いつか = someday."},
    {"question": "Asking a friend what kind of work they want to do.", "answer": "どんな しごとを したいですか。", "options": ["どんな しごとを したいですか。", "どんな しごとが したいですか。", "どんな しごとに したいですか。", "どんな しごとで したいですか。"], "explanation": "を marks the activity. したいですか = do you want to do?"},
    {"question": "I'd like to go to the restroom. Where is it?", "answer": "トイレに いきたいんですが、どこですか。", "options": ["トイレに いきたいんですが、どこですか。", "トイレを いきたいんですが、どこですか。", "トイレが いきたいんですが、どこですか。", "トイレで いきたいんですが、どこですか。"], "explanation": "に = direction/destination. いきたいんですが = I'd like to go. どこですか = where is it?"},
    {"question": "You want to study abroad in Japan for a year.", "answer": "いちねんかん にほんに りゅうがくしたいと おもっています。", "options": ["いちねんかん にほんに りゅうがくしたいと おもっています。", "いちねんかん にほんで りゅうがくしたいと おもっています。", "いちねんかん にほんを りゅうがくしたいと おもっています。", "いちねんかん にほんが りゅうがくしたいと おもっています。"], "explanation": "に = destination. りゅうがく = study abroad. たいとおもっています = am thinking of wanting to."},
    {"question": "At a clinic: 'I'd like to see a doctor.'", "answer": "しんさつを うけたいんですが。", "options": ["しんさつを うけたいんですが。", "しんさつを したいんですが。", "しんさつが うけたいんですが。", "しんさつで うけたいんですが。"], "explanation": "しんさつをうける = to receive a medical examination. たいんですが = I'd like to."},
    {"question": "I want to improve my Japanese speaking ability.", "answer": "にほんごの かいわりょくを あげたいです。", "options": ["にほんごの かいわりょくを あげたいです。", "にほんごの かいわりょくが あげたいです。", "にほんごの かいわりょくに あげたいです。", "にほんごの かいわりょくで あげたいです。"], "explanation": "を marks the object to improve. あげる = to raise/improve. たい = want to."},
    {"question": "I'd like to try eating sushi for the first time.", "answer": "はじめて すしを たべて みたいんですが。", "options": ["はじめて すしを たべて みたいんですが。", "はじめて すしが たべて みたいんですが。", "はじめて すしを たべたいんですが。", "はじめて すしに たべて みたいんですが。"], "explanation": "〜てみたい = want to try doing. はじめて = for the first time."},
    {"question": "You want to give your friend a birthday present.", "answer": "ともだちに たんじょうびプレゼントを あげたいんですが、なにが いいですか。", "options": ["ともだちに たんじょうびプレゼントを あげたいんですが、なにが いいですか。", "ともだちを たんじょうびプレゼントを あげたいんですが、なにが いいですか。", "ともだちへ たんじょうびプレゼントを あげたいんですが、なにが いいですか。", "ともだちが たんじょうびプレゼントを あげたいんですが、なにが いいですか。"], "explanation": "に = to (recipient). あげる = to give. たいんですが = I'd like to."},
    {"question": "I want to watch a Japanese movie without subtitles someday.", "answer": "いつか じまくなしで にほんえいがを みたいです。", "options": ["いつか じまくなしで にほんえいがを みたいです。", "いつか じまくなしに にほんえいがを みたいです。", "いつか じまくなしが にほんえいがを みたいです。", "いつか じまくなしは にほんえいがを みたいです。"], "explanation": "〜なしで = without ~. じまく = subtitles. みたい = want to watch."},
]

# ── Ch17: ちょっと待ってください ─────────────────────────────────────────

ch17_grammar_add = [
    {"question": "もう すこし おおきい こえで はなして _____か。(Could you speak a little louder?)", "answer": "いただけません", "options": ["いただけません", "ください", "もらいません", "いただけます"], "explanation": "〜ていただけませんか = Could you please ~? (Very polite request)."},
    {"question": "ここに なまえを かいて _____か。(Could you write your name here?)", "answer": "いただけません", "options": ["いただけません", "ください", "くれません", "もらいません"], "explanation": "〜ていただけませんか vs 〜てください: ていただけませんか is more polite."},
    {"question": "すみません、ちょっと てつだって _____か。(Could you help me for a moment?)", "answer": "くれませんか", "options": ["くれませんか", "いただけませんか", "もらえませんか", "ください"], "explanation": "〜てくれませんか = could you do for me? Less formal than ていただけませんか."},
    {"question": "もっと ゆっくり はなして いただけ_____か。(Could you speak more slowly?)", "answer": "ません", "options": ["ません", "ます", "ない", "くない"], "explanation": "いただけませんか = could you please? The negative form makes it a polite question."},
    {"question": "しゃしんを とって _____か。(Could you take a photo for me?)", "answer": "もらえません", "options": ["もらえません", "くれません", "いただけません", "ください"], "explanation": "〜てもらえませんか = could you do for me? Similar to くれませんか but slightly more formal."},
    {"question": "すみません、ちょっと _____てください。(Please wait a moment.)", "answer": "まっ", "options": ["まっ", "みて", "きて", "いって"], "explanation": "まつ→まって (て-form: wait). ちょっとまってください = please wait a moment."},
    {"question": "この かんじの よみかたを おしえて _____か。(Could you teach me how to read this kanji?)", "answer": "いただけません", "options": ["いただけません", "くれません", "もらえません", "ください"], "explanation": "〜ていただけませんか = most polite request form. おしえる = to teach."},
    {"question": "もう いちど いって _____か。(Could you say that again?)", "answer": "いただけません", "options": ["いただけません", "ください", "くれません", "もらえません"], "explanation": "もういちど = one more time. いっていただけませんか = could you say (polite)?"},
    {"question": "ドアを しめて _____か。(Could you close the door?)", "answer": "くれませんか", "options": ["くれませんか", "いただけませんか", "もらえませんか", "ください"], "explanation": "〜てくれませんか = casual-polite request. Used among colleagues/friends."},
    {"question": "ちょっと おまちくだ_____。(Please wait a moment.) (abbreviated)", "answer": "さい", "options": ["さい", "さいませ", "します", "ます"], "explanation": "おまちください = please wait (humble/formal). くださいませ even more formal."},
    {"question": "この たんごの いみを おしえて _____か。(Could you explain the meaning of this word?)", "answer": "くれませんか", "options": ["くれませんか", "いただけませんか", "ください", "もらえませんか"], "explanation": "〜てくれませんか = friendly request. All of these work; level of formality differs."},
    {"question": "えいごで せつめいして _____か。(Could you explain in English?)", "answer": "いただけません", "options": ["いただけません", "ください", "くれません", "もらえません"], "explanation": "ていただけませんか = most polite. Used when talking to strangers or seniors."},
    {"question": "レシートを _____ですが。(I'd like a receipt.)", "answer": "いただきたいん", "options": ["いただきたいん", "ください", "くださいん", "もらいたいん"], "explanation": "いただきたいんですが = I would like to receive. Polite receipt request at a shop."},
    {"question": "すみません、すこし _____てもらえませんか。(Could you move over a little?)", "answer": "つめ", "options": ["つめ", "はなれ", "まっ", "やめ"], "explanation": "つめる = to compress/move closer together. もらえませんか = could you?"},
    {"question": "しずかに _____ていただけませんか。(Could you please be quiet?)", "answer": "して", "options": ["して", "し", "した", "する"], "explanation": "しずかにする = to be quiet. して+いただけませんか = polite request."},
]

ch17_examples_add = [
    {"question": "At a hotel asking staff to carry your luggage.", "answer": "にもつを はこんで いただけませんか。", "options": ["にもつを はこんで いただけませんか。", "にもつを はこんで ください。", "にもつを はこんで くれませんか。", "にもつを はこんで もらえませんか。"], "explanation": "〜ていただけませんか = most polite request. はこぶ = to carry."},
    {"question": "Asking a classmate casually to lend their notes.", "answer": "ノートを かして くれませんか。", "options": ["ノートを かして くれませんか。", "ノートを かして いただけませんか。", "ノートを かして もらえませんか。", "ノートを かして ください。"], "explanation": "〜てくれませんか = friendly/casual request. Used between classmates."},
    {"question": "Calling customer service: 'Could you check my order number?'", "answer": "ちゅうもん ばんごうを たしかめて いただけませんか。", "options": ["ちゅうもん ばんごうを たしかめて いただけませんか。", "ちゅうもん ばんごうを たしかめて ください。", "ちゅうもん ばんごうを たしかめて くれませんか。", "ちゅうもん ばんごうを たしかめて もらえませんか。"], "explanation": "ていただけませんか = most polite. Appropriate for customer service calls."},
    {"question": "Asking a stranger to take your photo at a tourist spot.", "answer": "しゃしんを とって いただけませんか。", "options": ["しゃしんを とって いただけませんか。", "しゃしんを とって ください。", "しゃしんを とって くれませんか。", "しゃしんを とって もらえませんか。"], "explanation": "ていただけませんか = polite stranger request. とる = to take (photo)."},
    {"question": "Asking your friend to come a bit early.", "answer": "すこし はやく きて くれませんか。", "options": ["すこし はやく きて くれませんか。", "すこし はやく きて いただけませんか。", "すこし はやく きて もらえませんか。", "すこし はやく きて ください。"], "explanation": "くれませんか = casual request between friends. はやく = early."},
    {"question": "Politely asking a shop clerk to show you a different size.", "answer": "べつの サイズを みせて いただけませんか。", "options": ["べつの サイズを みせて いただけませんか。", "べつの サイズを みせて ください。", "べつの サイズを みせて くれませんか。", "べつの サイズを みせて もらえませんか。"], "explanation": "ていただけませんか = polite customer request. みせる = to show."},
    {"question": "Asking the teacher to explain it one more time.", "answer": "もう いちど せつめいして いただけませんか。", "options": ["もう いちど せつめいして いただけませんか。", "もう いちど せつめいして ください。", "もう いちど せつめいして くれませんか。", "もう いちど せつめいして もらえませんか。"], "explanation": "ていただけませんか = polite request to superior. せつめいする = to explain."},
    {"question": "Asking someone to speak Japanese more slowly.", "answer": "にほんごを もっと ゆっくり はなして いただけませんか。", "options": ["にほんごを もっと ゆっくり はなして いただけませんか。", "にほんごを もっと ゆっくり はなして ください。", "にほんごを もっと ゆっくり はなして くれませんか。", "にほんごを もっと ゆっくり はなして もらえませんか。"], "explanation": "ていただけませんか = most polite. ゆっくり = slowly. もっと = more."},
    {"question": "Asking a colleague to cover for you tomorrow.", "answer": "あした かわりに きて もらえませんか。", "options": ["あした かわりに きて もらえませんか。", "あした かわりに きて いただけませんか。", "あした かわりに きて くれませんか。", "あした かわりに きて ください。"], "explanation": "〜てもらえませんか = could you do for me? かわりに = instead of me. Same level as くれませんか."},
    {"question": "Asking to switch seats on an airplane.", "answer": "せきを かえて いただけませんか。", "options": ["せきを かえて いただけませんか。", "せきを かえて ください。", "せきを かえて くれませんか。", "せきを かえて もらえませんか。"], "explanation": "ていただけませんか = polite (to flight attendant). せき = seat. かえる = to change."},
    {"question": "Asking your roommate to lower the TV volume.", "answer": "テレビの おとを さげて くれませんか。", "options": ["テレビの おとを さげて くれませんか。", "テレビの おとを さげて いただけませんか。", "テレビの おとを さげて もらえませんか。", "テレビの おとを さげて ください。"], "explanation": "くれませんか = casual request (to roommate). おと = sound. さげる = to lower."},
    {"question": "Asking an elderly person to fill in a form for you.", "answer": "この もうしこみしょに きにゅうして いただけませんか。", "options": ["この もうしこみしょに きにゅうして いただけませんか。", "この もうしこみしょに きにゅうして ください。", "この もうしこみしょに きにゅうして くれませんか。", "この もうしこみしょに きにゅうして もらえませんか。"], "explanation": "ていただけませんか = very polite. もうしこみしょ = application form. きにゅう = to fill in."},
    {"question": "Asking your friend to wait because you'll be 5 minutes late.", "answer": "5ふんぐらい おくれますが、まって くれませんか。", "options": ["5ふんぐらい おくれますが、まって くれませんか。", "5ふんぐらい おくれますが、まって いただけませんか。", "5ふんぐらい おくれますが、まって もらえませんか。", "5ふんぐらい おくれますが、まって ください。"], "explanation": "くれませんか = casual. おくれます = will be late. まつ = to wait."},
    {"question": "Asking the doctor to write a medical certificate.", "answer": "しんだんしょを かいて いただけませんか。", "options": ["しんだんしょを かいて いただけませんか。", "しんだんしょを かいて ください。", "しんだんしょを かいて くれませんか。", "しんだんしょを かいて もらえませんか。"], "explanation": "ていただけませんか = very polite (to doctor). しんだんしょ = medical certificate."},
    {"question": "Please tell me the way to the station.", "answer": "えきへの みちを おしえて いただけませんか。", "options": ["えきへの みちを おしえて いただけませんか。", "えきへの みちを おしえて ください。", "えきへの みちを おしえて くれませんか。", "えきへの みちを おしえて もらえませんか。"], "explanation": "ていただけませんか = polite (to stranger). おしえる = to tell/teach."},
]

# ── Apply all patches ──────────────────────────────────────────────────────

print("Patching Ch09–Ch17 grammar and examples...")

d, p = load(9,  'grammar');   patch(d, p, ch09_grammar_add)
d, p = load(9,  'examples');  patch(d, p, ch09_examples_add)
d, p = load(10, 'grammar');   patch(d, p, ch10_grammar_add)
d, p = load(10, 'examples');  patch(d, p, ch10_examples_add)
d, p = load(11, 'grammar');   patch(d, p, ch11_grammar_add)
d, p = load(11, 'examples');  patch(d, p, ch11_examples_add)
d, p = load(12, 'grammar');   patch(d, p, ch12_grammar_add)
d, p = load(12, 'examples');  patch(d, p, ch12_examples_add)
d, p = load(13, 'grammar');   patch(d, p, ch13_grammar_add)
d, p = load(13, 'examples');  patch(d, p, ch13_examples_add)
d, p = load(14, 'grammar');   patch(d, p, ch14_grammar_add)
d, p = load(14, 'examples');  patch(d, p, ch14_examples_add)
d, p = load(15, 'grammar');   patch(d, p, ch15_grammar_add)
d, p = load(15, 'examples');  patch(d, p, ch15_examples_add)
d, p = load(16, 'grammar');   patch(d, p, ch16_grammar_add)
d, p = load(16, 'examples');  patch(d, p, ch16_examples_add)
d, p = load(17, 'grammar');   patch(d, p, ch17_grammar_add)
d, p = load(17, 'examples');  patch(d, p, ch17_examples_add)

print("Done!")

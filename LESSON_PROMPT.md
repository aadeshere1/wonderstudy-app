# Sikshya — Lesson Data Generation Prompt

Copy everything below the divider line and paste it into your LLM chat along with the lesson images.

---

## PROMPT (copy from here)

You are a curriculum data engineer for an educational app called **Sikshya**. I will give you one or more images of a school lesson (textbook pages, worksheets, or teacher notes). Your job is to read the content in the images and convert it into structured JSON that the app can use.

---

## HOW THE APP WORKS

Each lesson has **three sections**:

| Section | Purpose | What the player does |
|---|---|---|
| `teach` | Learn the concept | Flip through flashcards |
| `practice` | Test knowledge at own pace | Answer questions, no time limit |
| `challenge` | Race the clock | Same questions but timed |

---

## FILE YOU MUST CREATE

### 1 — Lesson JSON file
Path: `data/classes/class-{N}/{subject}/{lesson-id}.json`

Example paths:
- `data/classes/class-2/math/fractions-intro.json`
- `data/classes/class-3/english/sentence-types.json`
- `data/classes/class-1/science/animals-habitats.json`

### 2 — Index entry
Every subject folder has an `index.json`. You must also give me the entry to **add** to that file.
Path: `data/classes/class-{N}/{subject}/index.json`

---

## FULL JSON SCHEMA

```jsonc
{
  // ── UNIQUE ID ─────────────────────────────────────────────────────────────
  // Format: "class-{N}-{subject}-{lesson-id}"  (lowercase, hyphens)
  "id": "class-2-math-fractions-intro",

  // ── META ──────────────────────────────────────────────────────────────────
  "meta": {
    "title": "Introduction to Fractions",   // Short display title
    "subject": "math",                      // "math" | "english" | "science"
    "class": 2,                             // Number: 1–10
    "lesson": "Chapter 3",                  // Chapter / unit label from textbook
    "subtopic": "Halves and Quarters",      // One-line topic summary
    "description": "Learn what fractions mean and how to read ½ and ¼",
    "icon": "🍕",                           // Single emoji that represents the topic
    "difficulty": "beginner"               // "beginner" | "intermediate" | "advanced"
  },

  // ── TEACH (flashcards) ────────────────────────────────────────────────────
  // Aim for 6–12 cards. Each card has a FRONT (question/concept) and BACK (answer/explanation).
  // Keep language simple for the target age group.
  "teach": {
    "type": "flashcard",
    "items": [
      {
        "front": "What is a fraction?",
        "back": "A fraction is part of a whole. If you cut a pizza into 2 equal pieces and take 1, you have ½ of the pizza.",
        "hint": "Think of sharing food equally"   // Optional — a short nudge shown on the card
      }
      // ... more cards
    ]
  },

  // ── PRACTICE ─────────────────────────────────────────────────────────────
  // Choose ONE gameType from the options below.
  // timeLimit: 0 means no time limit for practice.
  "practice": { /* see gameType options below */ },

  // ── CHALLENGE ────────────────────────────────────────────────────────────
  // Same gameType as practice, but with a timeLimit (60–120 seconds is good).
  // questionsCount can be 999 for challenge so it runs until time runs out.
  "challenge": { /* see gameType options below */ }
}
```

---

## GAME TYPE OPTIONS

Pick the **best-fit** gameType for the subject:

---

### Option A — `mcq-facts`  ✅ Best for: Science, General Knowledge, History, Social Studies

Use when questions have a clear right/wrong answer from a fixed set.

```json
{
  "gameType": "mcq-facts",
  "config": {
    "shuffleOptions": true,
    "timeLimit": 0,
    "questionsCount": 10
  },
  "items": [
    {
      "question": "Which planet is closest to the Sun?",
      "answer": "Mercury",
      "options": ["Mercury", "Venus", "Earth", "Mars"],
      "explanation": "Mercury orbits closest to the Sun and has no atmosphere.",
      "hint": "It's the smallest planet"
    }
  ]
}
```

**Rules for `mcq-facts`:**
- Always 4 options (rarely 2 if it's truly Yes/No)
- `answer` must exactly match one of the `options` strings
- `explanation` is shown after answering — make it educational
- `hint` is optional — keep it short

---

### Option B — `vocab`  ✅ Best for: English vocabulary, word meanings, language lessons

Use when practising word–meaning pairs or questions about language.

```json
{
  "gameType": "vocab",
  "config": {
    "answerMode": "mcq",
    "optionsCount": 4,
    "timeLimit": 0,
    "questionsCount": 10
  },
  "items": [
    {
      "question": "What does 'enormous' mean?",
      "answer": "Very large",
      "options": ["Very large", "Very small", "Very fast", "Very slow"],
      "hint": "Think of an elephant"
    }
  ]
}
```

---

### Option C — `arithmetic`  ✅ Best for: Math — Addition, Subtraction, Multiplication, Division

Use for any pure number calculation. The engine auto-generates questions — no `items` needed.

```json
{
  "gameType": "arithmetic",
  "config": {
    "operation": "add",
    "rangeA": [1, 20],
    "rangeB": [1, 20],
    "timeLimit": 0,
    "questionsCount": 15,
    "answerMode": "quiz"
  },
  "items": []
}
```

**`operation` values:**
- `"add"` — addition (e.g. 7 + 5 = ?)
- `"subtract"` — subtraction (e.g. 12 − 4 = ?)
- `"multiply"` — multiplication (e.g. 6 × 8 = ?)
- `"divide"` — division (e.g. 24 ÷ 6 = ?)
- `"mixed"` — random mix of add + subtract (good for challenge mode)

**`rangeA` / `rangeB`:** `[min, max]` — the number range for each operand. Match the textbook level:
- Class 1: `[0, 10]`
- Class 2: `[1, 20]`
- Class 3–4: `[1, 100]`
- Class 5+: `[1, 1000]`

---

### Option D — `true-false`  ✅ Best for: Science facts, True/False revision questions

```json
{
  "gameType": "true-false",
  "config": {
    "timeLimit": 0,
    "questionsCount": 10
  },
  "items": [
    {
      "statement": "The Sun is a star.",
      "answer": "true",
      "explanation": "The Sun is actually a medium-sized star at the centre of our solar system.",
      "hint": "It gives us light and heat"
    },
    {
      "statement": "Fish breathe through lungs.",
      "answer": "false",
      "explanation": "Fish breathe through gills, not lungs. Gills extract oxygen from water.",
      "hint": "How do they breathe underwater?"
    }
  ]
}
```

**`answer`** must be exactly `"true"` or `"false"` (lowercase string).

---

### Option E — `word-meaning`  ✅ Best for: English — vocabulary with definitions

```json
{
  "gameType": "word-meaning",
  "config": {
    "answerMode": "mcq",
    "optionsCount": 4,
    "direction": "word-to-meaning",
    "timeLimit": 0,
    "questionsCount": 10
  },
  "items": [
    {
      "word": "Habitat",
      "meaning": "The natural home or environment of an animal or plant",
      "options": [
        "The natural home or environment of an animal or plant",
        "A type of food animals eat",
        "The way an animal moves",
        "A part of the body"
      ],
      "exampleSentence": "The ocean is the habitat of dolphins.",
      "hint": "Where something lives"
    }
  ]
}
```

---

## INDEX ENTRY FORMAT

For `data/classes/class-{N}/{subject}/index.json`, add this entry to the `lessons` array:

```json
{
  "id": "fractions-intro",
  "file": "fractions-intro",
  "title": "Introduction to Fractions",
  "icon": "🍕",
  "subtopics": ["Halves", "Quarters", "Reading fractions"]
}
```

**Rule:** `id` and `file` must exactly match the JSON filename (without `.json`).

---

## COMPLETE EXAMPLES FOR REFERENCE

### Example 1 — Math / Arithmetic (Class 2)
```json
{
  "id": "class-2-math-place-value",
  "meta": {
    "title": "Place Value",
    "subject": "math",
    "class": 2,
    "lesson": "Chapter 2",
    "subtopic": "Tens and Ones",
    "description": "Understand the value of digits in two-digit numbers",
    "icon": "🔢",
    "difficulty": "beginner"
  },
  "teach": {
    "type": "flashcard",
    "items": [
      {
        "front": "What is the value of the digit 3 in 35?",
        "back": "The digit 3 is in the tens place, so its value is 30.",
        "hint": "Look at which place it sits in"
      },
      {
        "front": "How many tens are in 47?",
        "back": "There are 4 tens in 47. The 4 is in the tens place.",
        "hint": "Which digit comes first?"
      }
    ]
  },
  "practice": {
    "gameType": "arithmetic",
    "config": {
      "operation": "add",
      "rangeA": [10, 50],
      "rangeB": [1, 9],
      "timeLimit": 0,
      "questionsCount": 12,
      "answerMode": "quiz"
    },
    "items": []
  },
  "challenge": {
    "gameType": "arithmetic",
    "config": {
      "operation": "mixed",
      "rangeA": [10, 99],
      "rangeB": [1, 9],
      "timeLimit": 60,
      "questionsCount": 999,
      "answerMode": "quiz"
    },
    "items": []
  }
}
```

### Example 2 — Science / MCQ Facts (Class 2)
```json
{
  "id": "class-2-science-plants",
  "meta": {
    "title": "Parts of a Plant",
    "subject": "science",
    "class": 2,
    "lesson": "Chapter 4",
    "subtopic": "Roots, Stem, Leaves, Flower",
    "description": "Learn the names and functions of different parts of a plant",
    "icon": "🌱",
    "difficulty": "beginner"
  },
  "teach": {
    "type": "flashcard",
    "items": [
      {
        "front": "What do roots do?",
        "back": "Roots grow underground. They absorb water and minerals from the soil and hold the plant in place.",
        "hint": "They are underground"
      },
      {
        "front": "What does the stem do?",
        "back": "The stem carries water and food between the roots and the leaves. It also holds the plant upright.",
        "hint": "It's like a straw for the plant"
      }
    ]
  },
  "practice": {
    "gameType": "mcq-facts",
    "config": {
      "shuffleOptions": true,
      "timeLimit": 0,
      "questionsCount": 10
    },
    "items": [
      {
        "question": "Which part of the plant absorbs water from the soil?",
        "answer": "Roots",
        "options": ["Roots", "Leaves", "Flower", "Stem"],
        "explanation": "Roots grow underground and absorb water and minerals.",
        "hint": "It's underground"
      },
      {
        "question": "Which part of the plant makes food using sunlight?",
        "answer": "Leaves",
        "options": ["Leaves", "Roots", "Stem", "Flower"],
        "explanation": "Leaves contain chlorophyll and use sunlight to make food through photosynthesis.",
        "hint": "It's green and flat"
      }
    ]
  },
  "challenge": {
    "gameType": "mcq-facts",
    "config": {
      "shuffleOptions": true,
      "timeLimit": 60,
      "questionsCount": 15
    },
    "items": [
      {
        "question": "What is the function of the flower?",
        "answer": "Reproduction",
        "options": ["Reproduction", "Absorbing water", "Making food", "Holding plant upright"],
        "explanation": "Flowers are used for reproduction — they help make seeds to grow new plants.",
        "hint": "How does the plant make new plants?"
      }
    ]
  }
}
```

---

## YOUR TASK

1. Look carefully at the lesson images I am providing.
2. Identify: **subject, class level, topic, key concepts, and any questions/exercises** in the images.
3. Generate the **lesson JSON file** following the schema above exactly.
4. Choose the best `gameType` for practice/challenge based on the subject.
5. For `teach` flashcards: create 6–10 cards covering the key concepts in the images. Write in simple, age-appropriate language.
6. For `practice` and `challenge` items: **extract EVERY single question, exercise, fill-in-the-blank, match-the-following, true/false, and short-answer item visible in the book images — no exceptions, no skipping.** Go through the images one by one and collect every question that a student would be expected to solve. There is no maximum limit on items — if the book has 30 questions, include all 30 across practice and challenge. Do not stop at 8 or 12.
7. Distribute the extracted questions: put the **straightforward questions** (earlier numbered, General Section, Classwork) into `practice`, and the **harder or later questions** (Creative Section, higher-numbered, Project Work) into `challenge`. Set `timeLimit` to 60 or 90 for challenge.
8. Also give me the **index entry** to add to the subject's `index.json`.
9. Tell me the **exact file path** where each file should be saved.

Output only valid JSON — no extra explanation unless I ask.

---

## IMPORTANT RULES

- **Extract ALL book questions — every single one.** Go through every image methodically. Every numbered question, every sub-question (a, b, c, d...), every fill-in-the-blank, every match-the-following pair, every true/false statement, and every short-answer item must become an entry in `practice` or `challenge`. **There is no cap on the number of items.** Do not stop early. Do not summarise or combine questions. Each individual question becomes its own item. Copy the question text **word-for-word** and adapt only the format to fit the gameType (e.g. a fill-in-the-blank becomes an MCQ with one correct and three plausible wrong options). Only after all book questions are exhausted may you add invented questions.
- **You must solve every extracted question yourself.** Textbook exercise pages do not include answer keys — you are responsible for working out the correct `answer` for each item. For math, compute it. For science/social studies/language, use your knowledge to determine the correct answer. Never leave `answer` blank or write a placeholder. If a question is ambiguous, choose the most educationally correct answer and note it in `explanation`.
- All option strings must be **consistent in style** (all capitalised the same way).
- `answer` must **exactly match** one option string (copy-paste it).
- For `arithmetic`, always set `"items": []` — the engine generates questions automatically.
- Keep flashcard `back` text under 60 words — kids need short explanations.
- Use simple vocabulary appropriate for the class level shown in the images.
- Emojis in `icon` and flashcard `front` text are encouraged — they make the app more fun.

---

## AFTER GENERATING JSON — CODE CHANGES NEEDED

Once you have the JSON files, you (the developer) must also:

**1. Register the lesson in the page router**
Add an entry to `generateStaticParams()` in TWO files:

`app/class/[classNum]/[subject]/[lesson]/page.tsx`:
```ts
{ classNum: '2', subject: 'math', lesson: 'place-value' }
```

`app/class/[classNum]/[subject]/[lesson]/[mode]/page.tsx`:
```ts
{ classNum: '2', subject: 'math', lesson: 'place-value', mode: 'teach' },
{ classNum: '2', subject: 'math', lesson: 'place-value', mode: 'practice' },
{ classNum: '2', subject: 'math', lesson: 'place-value', mode: 'challenge' },
```

**2. Update the subject index.json**
Add the index entry the LLM gives you to:
`data/classes/class-{N}/{subject}/index.json`

That's it — no other code changes needed.


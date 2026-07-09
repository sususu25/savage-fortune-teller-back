SECTION_TITLES = {
    "cosmic_diagnosis": "Your Cosmic Diagnosis",
    "why_you_are_like_this": "Why You Are Like This",
    "the_receipts": "The Receipts",
    "emotional_damage_forecast": "Emotional Damage Forecast",
    "love_life_a_situation": "Love Life: A Situation",
    "court_ordered_advice": "Court-Ordered Advice From The Stars",
}


ARCHETYPE_COPY = {
    "burdened_one": {
        "viral_alias": "The Unpaid Project Manager of the Universe",
        "headline": "You were born with the emotional posture of someone who has already read the terms and conditions.",
        "result_badge": "cosmically over-employed",
        "share_text": "I got {score}% The Unpaid Project Manager of the Universe. My birth chart said I need a nap and a union.",
    },
    "chaos_magnet": {
        "viral_alias": "The Human Plot Twist",
        "headline": "You do not enter situations. You accidentally become the season finale.",
        "result_badge": "plot armored, barely",
        "share_text": "I got {score}% The Human Plot Twist. The stars said my life needs a responsible adult and, unfortunately, it is not me.",
    },
    "overthinker": {
        "viral_alias": "The 47 Tabs Open Personality",
        "headline": "Your brain has 47 tabs open, and somehow one of them is arguing with a memory from 2019.",
        "result_badge": "mentally buffering",
        "share_text": "I got {score}% The 47 Tabs Open Personality. My birth chart told my brain to shut the hell up.",
    },
    "dangerous_heart": {
        "viral_alias": "The Romantic Red Flag with Good Branding",
        "headline": "You call it chemistry. Your chart calls it evidence.",
        "result_badge": "emotionally subpoenaed",
        "share_text": "I got {score}% The Romantic Red Flag with Good Branding. The stars called it love, then asked for a lawyer.",
    },
    "haunted_dreamer": {
        "viral_alias": "The Delulu Oracle",
        "headline": "Your intuition is loud, dramatic, and annoying because it keeps being right.",
        "result_badge": "spiritually unsupervised",
        "share_text": "I got {score}% The Delulu Oracle. My birth chart said the vibes are real, but so is therapy.",
    },
    "unfinished_legend": {
        "viral_alias": "The Main Character in Development Hell",
        "headline": "You have main character energy, but the universe keeps requesting revisions.",
        "result_badge": "loading, but iconic",
        "share_text": "I got {score}% The Main Character in Development Hell. The stars said my potential is huge and my execution is late.",
    },
}


def get_archetype_copy(type_code: str, score: int) -> dict:
    copy = ARCHETYPE_COPY.get(type_code, {})

    share_text = copy.get("share_text", "").format(score=score)

    return {
        "viral_alias": copy.get("viral_alias", ""),
        "headline": copy.get("headline", ""),
        "result_badge": copy.get("result_badge", ""),
        "share_text": share_text,
    }

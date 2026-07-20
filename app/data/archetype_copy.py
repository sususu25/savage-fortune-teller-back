SECTION_TITLES = {
    "cosmic_diagnosis": "Your Cosmic Diagnosis",
    "why_you_are_like_this": "Why You Are Like This",
    "the_receipts": "The Receipts",
    "emotional_damage_forecast": "Emotional Damage Forecast",
    "love_life_a_situation": "Love Life: A Situation",
    "court_ordered_advice": "Court-Ordered Advice From The Stars",
}


ARCHETYPE_COPY = {'burdened_one': {'viral_alias': 'The Unpaid Project Manager of the Universe',
                  'headline': 'You were born with the emotional posture of someone who has already '
                              'read the terms and conditions.',
                  'result_badge': 'cosmically over-employed',
                  'share_text': 'I got {score}% The Unpaid Project Manager of the Universe. My '
                                'birth chart said I need a nap and a union.'},
 'chaos_magnet': {'viral_alias': 'The Human Plot Twist',
                  'headline': 'You do not enter situations. You accidentally become the season '
                              'finale.',
                  'result_badge': 'plot armored, barely',
                  'share_text': 'I got {score}% The Human Plot Twist. The stars said my life needs '
                                'a responsible adult and, unfortunately, it is not me.'},
 'overthinker': {'viral_alias': 'The 47 Tabs Open Personality',
                 'headline': 'Your brain has 47 tabs open, and somehow one of them is arguing with '
                             'a memory from 2019.',
                 'result_badge': 'mentally buffering',
                 'share_text': 'I got {score}% The 47 Tabs Open Personality. My birth chart told '
                               'my brain to shut the hell up.'},
 'dangerous_heart': {'viral_alias': 'The Romantic Red Flag with Good Branding',
                     'headline': 'You call it chemistry. Your chart calls it evidence.',
                     'result_badge': 'emotionally subpoenaed',
                     'share_text': 'I got {score}% The Romantic Red Flag with Good Branding. The '
                                   'stars called it love, then asked for a lawyer.'},
 'haunted_dreamer': {'viral_alias': 'The Delulu Oracle',
                     'headline': 'Your intuition is loud, dramatic, and annoying because it keeps '
                                 'being right.',
                     'result_badge': 'spiritually unsupervised',
                     'share_text': 'I got {score}% The Delulu Oracle. My birth chart said the '
                                   'vibes are real, but so is therapy.'},
 'unfinished_legend': {'viral_alias': 'The Main Character in Development Hell',
                       'headline': 'You have main character energy, but the universe keeps '
                                   'requesting revisions.',
                       'result_badge': 'loading, but iconic',
                       'share_text': 'I got {score}% The Main Character in Development Hell. The '
                                     'stars said my potential is huge and my execution is late.'},
 'main_character_energy': {'viral_alias': "The Discourse's Main Character",
                           'headline': 'You did not ask to be the protagonist of every '
                                       'conversation. You just are, tragically, at volume, in '
                                       'every group chat and comment section.',
                           'result_badge': 'narratively overexposed',
                           'share_text': "I got {score}% The Discourse's Main Character. My birth "
                                         'chart said the world revolves around me and, worse, kind '
                                         'of agreed.'},
 'moon_flood': {'viral_alias': 'The Human Weather System',
                'headline': 'You do not have moods. You have forecasts, and today there is a 90 '
                            'percent chance of everyone around you checking the emotional radar '
                            'before texting you back.',
                'result_badge': 'emotionally category five',
                'share_text': 'I got {score}% The Human Weather System. My birth chart said I '
                              'contain multitudes and also possibly a small localized storm.'},
 'venus_maximalist': {'viral_alias': 'The Standards With Their Own Zip Code',
                      'headline': 'You are not high maintenance. You simply require a partner, a '
                                  'job, and a group chat that all meet the aesthetic and moral bar '
                                  'you set at age nine.',
                      'result_badge': 'curated to a fault',
                      'share_text': 'I got {score}% The Standards With Their Own Zip Code. My '
                                    'birth chart said settle down and it meant the neighborhood, '
                                    'not the person.'},
 'mars_ignition': {'viral_alias': 'The Fight-or-Also-Fight Response',
                   'headline': 'Your nervous system has two settings: charming, and about to flip '
                               'a table, and unfortunately both look the same from a distance.',
                   'result_badge': 'combat-ready, unprompted',
                   'share_text': 'I got {score}% The Fight-or-Also-Fight Response. My birth chart '
                                 'gave me a libido and a temper and forgot to install a delay '
                                 'timer.'},
 'jupiter_evangelist': {'viral_alias': 'The Free Advice Philanthropist',
                        'headline': 'You changed your life once, three months ago, and have been '
                                    'unable to shut up about it in every group chat, comment '
                                    'thread, and unsuspecting Tuesday brunch since.',
                        'result_badge': 'morally over-leveraged',
                        'share_text': 'I got {score}% The Free Advice Philanthropist. My birth '
                                      'chart said I found the truth and it was, tragically, '
                                      'extremely shareable.'},
 'ascendant_mask': {'viral_alias': 'The Different Person Depending on the Lighting',
                    'headline': 'You are composed, warm, and camera-ready in public, and an '
                                'entirely different animal the second the group chat goes quiet or '
                                'the door finally closes.',
                    'result_badge': 'authentically unverifiable',
                    'share_text': 'I got {score}% The Different Person Depending on the Lighting. '
                                  'My birth chart said pick a face and it meant literally any of '
                                  'them.'}}


def get_archetype_copy(type_code: str, score: int) -> dict:
    copy = ARCHETYPE_COPY.get(type_code, {})

    share_text = copy.get("share_text", "").format(score=score)

    return {
        "viral_alias": copy.get("viral_alias", ""),
        "headline": copy.get("headline", ""),
        "result_badge": copy.get("result_badge", ""),
        "share_text": share_text,
    }

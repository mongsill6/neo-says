"""Quote database and selection logic."""

import random

QUOTES = {
    "git": [
        "Force push to main? Bold strategy. Let's see if it pays off.",
        "'git blame' exists because accountability matters more than feelings.",
        "Your commit message says 'minor fix'. The diff is 847 lines.",
        "Rebasing is just lying about history with extra steps.",
        "You wrote 'WIP' 6 commits ago. At what point does it become 'the project'?",
    ],
    "debugging": [
        "The bug is not in the library. The bug is never in the library. ...Okay sometimes it's in the library.",
        "console.log('here') console.log('here2') console.log('WHY') — a debugging classic.",
        "You don't fix bugs. You just move them to a place nobody checks.",
        "If debugging is removing bugs, then programming is putting them in.",
        "It worked yesterday. Nothing changed. It doesn't work today. Welcome to software.",
    ],
    "meetings": [
        "This meeting could've been a Slack message. That Slack message could've been silence.",
        "'Let's circle back' is corporate for 'I stopped listening 10 minutes ago'.",
        "Stand-up took 45 minutes. We are no longer standing.",
        "The best code I ever wrote was during a meeting I wasn't paying attention to.",
        "'Quick sync' — the two most dangerous words in a calendar invite.",
    ],
    "code-review": [
        "LGTM = Let's Go To Main (without actually reading the code).",
        "'Nit:' is just a polite way of saying 'I need to justify my review time'.",
        "Your PR has 2 approvals and 47 unresolved comments. Ship it.",
        "The reviewer who says 'just a small suggestion' is about to rewrite your architecture.",
        "'Can you add tests?' — The most feared 4 words in a code review.",
    ],
    "production": [
        "Deploy on Friday. What could possibly go wrong? ...Everything. Everything could.",
        "Hotfix at 3 AM builds character. Mostly bitter, resentful character.",
        "The monitoring dashboard is green. This means nothing and we all know it.",
        "Rollback is not failure. Rollback is wisdom disguised as retreat.",
        "'Works in staging' is the developer equivalent of 'thoughts and prayers'.",
    ],
    "general": [
        "'It works on my machine' is not a deployment strategy.",
        "There are only two hard things: cache invalidation, naming things, and off-by-one errors.",
        "Legacy code is just code without an author willing to claim it.",
        "Documentation is like a love letter to your future self. You never write it.",
        "Stack Overflow didn't go down. You just need to learn to read error messages.",
        "AI will replace developers. Developers using AI will replace developers not using AI.",
        "The best code is no code. The second best is someone else's code.",
        "TODO: refactor this. — Written 3 years ago. By you.",
    ],
}


def get_quote(category=None):
    """Get a random quote, optionally filtered by category."""
    if category and category in QUOTES:
        return random.choice(QUOTES[category]), category
    cat = random.choice(list(QUOTES.keys()))
    return random.choice(QUOTES[cat]), cat

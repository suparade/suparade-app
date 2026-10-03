"""
Sentiment analysis for paid tips.

When a tip is made, Gemini watches the clip (video + audio) to read the
streamer's mood, tone of voice and facial expression, and reads the live chat
around the moment to gauge the audience's mood. The result is attached to the
event so the brand sees how the streamer and their community felt at the
moment it paid for.
"""

from typing import Optional

from google.genai import types

from . import config
from .gemini_analyzer import generate_json
from .models import BeverageEvent, TipSentiment

PROMPT = """You analyze sentiment for {brand}, a brand that just tipped a livestreamer.
You get a short clip of the stream (video + audio), what was tipped for, and possibly the
live chat around that moment (times relative to the moment).

streamer: judge the streamer's overall mood in this clip from their tone of voice, words,
and facial expression; list up to 3 emotions; and separately judge their attitude toward
{brand} itself (a happy streamer can still be neutral about the brand).

chat: judge the overall mood of the chat messages (not just whether they mention the
brand): label, score, the fraction of positive messages, and up to 3 themes. If no chat is
provided, return null for chat.

Scores are -1.0 (very negative) to 1.0 (very positive). Be calibrated; ironic or mocking
messages count as negative."""


async def analyze_tip(event: BeverageEvent, data: bytes, mime_type: str, chat: Optional[str]) -> TipSentiment:
    context = (f"Tipped for: {event.description}\n"
               f"Quote: {event.quote or 'none'}\n\n"
               f"{chat or 'Live chat: (none provided)'}")
    contents = [types.Part.from_bytes(data=data, mime_type=mime_type), context]
    result = await generate_json(config.GEMINI_MODEL, PROMPT.format(brand=config.SPONSOR_BRAND),
                                 contents, TipSentiment)
    if not chat:
        result.chat = None
    return result

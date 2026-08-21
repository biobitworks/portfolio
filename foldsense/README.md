# FoldSense — judge-safe public static baseline

FoldSense is an accessibility-first multisensory molecular interface: the same typed molecular event can be rendered through visualization, text/screen-reader semantics, sonification, voice, and later tactile/haptic interfaces.

## This release

This directory is intentionally static and dependency-free. It exists so judges and voters can always see a coherent FoldSense experience even if model/API services are unavailable.

Routes:
- `/` — product story + slideshow + example conversation
- `/vapi` — Vapi prize integration contract
- `/elevenlabs` — ElevenLabs accessibility voice contract
- `/apify` — Apify structured web-evidence contract
- `/gmi` — GMI Cloud inference contract
- `/gemini-exa` — Gemini + Exa scientific conversation/retrieval contract
- `/integrated` — single judge path integrating sponsor services
- `/evidence` — FCO/FCG claim and dependency boundary

All sponsor pages begin as `STATIC_DEMO`. They must only change to `LIVE` after a real provider request/session/run is observed and recorded.

## Scientific boundary

The current recovered hackathon source contains a procedural conformational demonstration. Do not call it a published molecular-dynamics trajectory. Deterministic local code owns numerical metrics and threshold events; language/audio systems render or interpret those typed events.

## Deployment discipline

Use one preview deployment for each milestone bundle, validate it, then promote that exact preview rather than rebuilding. Avoid a deployment per small text/code edit.

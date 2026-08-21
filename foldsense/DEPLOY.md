# FoldSense Vercel deployment runbook

Goal: spend one Vercel deployment per tested milestone bundle.

## Baseline deployment

From the directory containing this file:

```bash
npx vercel@latest login
npx vercel@latest --yes
```

Choose the `biobitworks` scope if prompted and name the new project `foldsense-judges` (or `foldsense`). The directory is already a dependency-free static Vercel project.

Record the preview URL. Test these routes before promotion:

- `/`
- `/vapi`
- `/elevenlabs`
- `/apify`
- `/gmi`
- `/gemini-exa`
- `/integrated`
- `/evidence`
- `/status.json`

Then promote the exact tested preview rather than rebuilding:

```bash
npx vercel@latest promote <PREVIEW_URL>
```

Do not use `vercel --prod` merely to promote this same artifact; that would create another deployment.

## Deployment waves

- Wave 1: static judge baseline.
- Wave 2: bundle ElevenLabs + Vapi live voice changes, test locally, one preview, promote.
- Wave 3: bundle Apify + GMI + Gemini/Exa live evidence/inference changes, one preview, promote.
- Wave 4 only if necessary: final integrated bug-fix bundle before the operational judging deadline.

Do not deploy copy-only intermediate edits.

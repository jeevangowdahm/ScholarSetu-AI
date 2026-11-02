# ScholarSetu UI refresh — v0.2

## What changed
- Replaced the generic neon landing-page look with a calmer, more realistic student funding workspace.
- Added persistent navigation, catalogue count, profile status, saved-scheme count, clear sample-catalogue labels, and an explicit rule-based matching explanation.
- Removed the prominent fake AI score from result cards. Results now show the configured rule-check status and reasons.
- Added a real saved-schemes section with removal support (`DELETE /api/saved/<scheme_id>`).
- Added responsive layouts, keyboard search shortcut (Ctrl/Cmd+K), accessible focus states, status announcements, and toast feedback.
- Changed Flask debug mode to opt-in via `FLASK_DEBUG=1`; default local run no longer enables the debugger.

## Still important
The scheme catalogue is still a small demonstration dataset. It must not be represented as a verified live eligibility database. The “potential match” status means only that the currently configured demo rules did not find a mismatch. The app has no real student login, private per-user accounts, live scheme updates, official application submission, or trained ML model.

## Run
```powershell
python app.py
```
Then open `http://127.0.0.1:5000`.

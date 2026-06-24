# Bamboo Forest — Proof

**What this thing is**  
A simple side-view jumping and collecting game with a panda in a forest that changes as you go.

**What it does for you**  
- Gives you short sessions of movement, timing, and exploration across different areas.  
- Lets you collect things and get better at the levels.  
- Offers variety through changing ground rules, items that help in new ways, and a clear goal each time.  

**How it was made**  
The user designed the game, the levels, the feeling of each area, and what should happen next. AI helped write the code that makes the panda move, the areas appear, the items work, and the screens show up.

**What it costs / what it gives back**  
- Costs a little time to learn the changing rules.  
- Gives back quick wins, a sense of progress through the 18 areas, and high scores you can chase.  
- No internet or accounts needed for the basic desktop version. Web version works in a browser.

**Who is responsible**  
The user (designer of record). Reviewed on 2026-06-24.

**What proof exists that it works**  
- Runs on desktop and in browser.  
- 18 working levels with distinct mechanics.  
- Dev captures in diag_shots/. Multiple internal bug hunts documented.  
- Existing high score saving and state machine.
- 25+ automated tests for player movement, timers, powerups.

**Changelog**  
2026-06-24: Swarm drive by agents closed bugs (phasing enemies, bad checkpoints, attacks while dead, and more), smoothed jumping controls, advanced grove crafting with essences and grafts, speedrun ghosts, daily challenges, overgrown post-game area. Kept desktop and web versions matching. Added gameplay juice like particles. Tests now at 25+. Docs updated in both project and central folder. User can notice better feel and new ways to grow the panda's powers.

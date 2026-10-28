# Hacker News (Show HN) Submission & Launch Kit

### Proposed Title:
> **Show HN: Auditing NASA raw telemetry to measure the viral 'Mars cylinder'**

*Alternative Titles:*
* `Show HN: We parsed Curiosity PDS telemetry in Python to measure the Mars cylinder`
* `Show HN: An interactive 3D studio and Python suite auditing a viral Mars anomaly`

**URL:** `https://cambrianminds.github.io/martian-cylinder/`

---

### First Comment / Launch Submission Text:

Hi HN,

In August 2022, NASA’s Curiosity rover took a photo at Paraitepuy Pass in Gale Crater (PDS Product `3556MR1025170721700585C00`). In the lower right corner, there appeared to be a remarkably clean cylinder embedded in the Martian dirt.

The internet did what the internet always does: podcasts, subreddits, and YouTube channels erupted with claims ranging from "Curiosity dropped an 8-inch drill bit" to alien probes. Even astrophysicist Avi Loeb wrote an article repeating an early informal estimate that it was roughly 20 cm (8 inches) long.

The strange thing was that nobody seemed to be actually opening the raw data. NASA’s Planetary Data System (PDS) is completely public, but the conversation was entirely driven by compressed social media screenshots.

I’m not a planetary scientist or a mathematician. But I wanted to know the actual, checkable dimensions. So I paired with an AI coding assistant to parse the raw NASA PDS3 ODL telemetry labels, evaluate the Mastcam-100 optical camera model (CAHVOR), ray-trace the solar shadow ephemeris, and build a deterministic Python verification suite:

👉 **Live Project, Monograph & 3D WebGL Studio:** https://cambrianminds.github.io/martian-cylinder/  
👉 **Technical Paper (14-page PDF):** https://cambrianminds.github.io/martian-cylinder/martian_cylinder_paper.pdf  
👉 **Code & Data Repository:** https://github.com/cambrianminds/martian-cylinder

### What the telemetry actually showed:

1. **The physical scale is 35 mm, not 20 cm:** The raw PDS label contains `MSL:FOCUS_POSITION_COUNT = 2705`. Running that through Malin Space Science Systems' optical calibration polynomials yields a slant range of 3.957 meters, giving a ground resolution of 0.317 mm/pixel. The object is 110 px × 34 px—meaning it is **35 mm × 11.5 mm (the size of an AA battery)**, not an 8-inch pipe.
2. **The dust clock rules out rover debris:** About 33% of the cylinder (2.0–3.2 mm) is buried in cohesive duricrust with zero windward scour moats or leeward sand drifts. Atmospheric dust fallout in Gale Crater is 10–25 µm/year. Burying that lower third passively takes **80 to 200+ Earth years**. Curiosity had only been on Mars for 10 years at Sol 3556, and its landing site (Bradbury Landing) is 13–15 km away across rugged craters in a 6-mbar atmosphere.
3. **Control rocks ($N = 20$):** We measured 20 surrounding background rocks across the identical frame. The cylinder's generator parallelism ($R^2 = 0.9985$) and aspect ratio ($3.24:1$) are $+10.7\sigma$ and $+12.0\sigma$ outliers against natural clasts.
4. **Deterministic reproduction:** Everything runs locally with `python reproduce_analysis.py`. It checks the SHA-256 hashes of all 8 NASA `.IMG`/`.LBL` files, validates the camera intrinsics, and recomputes the statistics (exits code 0).

### On building this with AI (The Colophon):

I wanted to be completely transparent about how this was made: I didn't write the CAHV linear algebra or the LaTeX paper by hand. I used AI as a tireless technical calculator. My job was figuring out what to test, asking "how would we know if this is wrong?", and catching the software when it did something stupid—like lumping the ground shadow into the circular end cap or swallowing the rock next to it. 

You don’t have to trust me or the AI: the raw NASA PDS files, the mathematical derivations, and the Python test suite are all in the repo so you can run the math yourself.

Would love feedback, critique on the photogrammetry, or ideas from anyone with planetary geology experience!

---

### Tips for Launching on HN:
1. **Best Times to Post**: Tuesday, Wednesday, or Thursday between 8:00 AM – 10:00 AM EST (12:00 – 14:00 UTC).
2. **Engagement**: Respond quickly to technical questions about the CAHV model, camera focus curves, or dust accumulation rates.
3. **Tone**: Humble, scientifically curious, and rigorous. Focus on the code, the open data, and the methodology.

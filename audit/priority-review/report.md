# Priority review: Sol 3556 cylindrical feature

Search performed: 2026-11-13. Target: Curiosity Mastcam product **3556MR1025170721700585C00**, acquired 2022-08-07.

## Finding

**Justin Bogner's repository is the earliest reproducible quantitative metrology study of this particular target located in this search.** No earlier source was located reporting the combination of subpixel edge extraction, numerical geometric residuals, and frozen-front-shape rear-arc prediction documented in the current project.

There is, however, an earlier **3D cylinder overlay**: MILTOID's video of 2025-10-23. Consequently, neither first recognition of the object as cylindrical nor first geometric/3D reconstruction is a defensible priority claim for this repository. The original visual discovery is credited to Rami Bar Ilan by both Jean Ward and Avi Loeb; this review did not independently establish his first publication date.

Suggested statement:

> To our knowledge, this is the first publicly documented, reproducible quantitative metrology study of the Sol 3556 cylindrical feature, including subpixel boundary measurements, numerical geometric fit residuals, and predictive registration of the rear boundary using a frozen front-derived shape. Earlier identification, image processing, and qualitative 3D cylinder overlays are acknowledged separately.

This is a search-supported priority statement, rather than proof that no unindexed or unpublished predecessor exists. The dates of individual methods must be distinguished: the original study is in the October 24 repository history; the current independent reconstruction, including Step 8, first appears in the November 11 history. Later methods should not be backdated to the October release.

## Dated evidence

| Date | Record | What it establishes |
| --- | --- | --- |
| 2022-08-07 | NASA image acquisition | Date of the underlying observation, not the analysis or discovery. |
| 2025-10-23 | [Jean Ward, Cylindrical Object in Colour](https://megalithicmars.com/2025/10/23/rover-curiosity-cylindrical-object-in-colour-sol-3556/) | Exact product ID; prior identification, color presentation, enlargement, and qualitative morphology discussion. Credits Rami Bar Ilan with discovery. |
| 2025-10-23 | [MILTOID, VFX Artist Reacts - Ancient Artefact on Mars](https://www.youtube.com/watch?v=xpr8cWDRTO8) | Retrieved transcript describes Bayer decoding with a script, levels adjustment, an actual cylinder overlay in a 3D art package, and a rendered lighting/shadow scene. This is substantive prior image-processing and geometric visualization work. |
| 2025-12-16 | [Brian Cory Dobbs, Perfectly Smooth Cylinder Artifact on Mars](https://www.youtube.com/watch?v=6CDMyZaYS24) | Retrieved transcript discusses archive access, color products, upscaling, morphology, and possible artificiality. Credits the discoverer and Ward. |
| 2026-03-07 | [Avi Loeb, Is the Mysterious Cylinder ... Human-Made Debris?](https://avi-loeb.medium.com/is-the-mysterious-cylinder-on-mars-photographed-in-2022-by-the-curiosity-rover-a-human-made-6fcd8e242fea) | Exact target ID, prior discussion and discovery attribution, a rough size estimate, interpretation, and recommendation for follow-up. No numerical geometric fitting analysis is presented in the article. |
| 2026-10-24 | [Bogner repository initial commit](https://github.com/CambrianMinds/martian-cylinder/commit/1553f5b91828ed8c1af57d6115fc5e25e7ca8a05) | Contains original paper, NASA archive products, Sobel analysis illustration, and interactive cylinder tool. The paper reports numerical edge/ellipse analysis and physical scaling. |
| 2026-10-30 | [Zenodo v1.0.0, DOI 10.5281/zenodo.23789092](https://zenodo.org/records/23789092) | Independently hosted public deposit naming Justin Bogner and containing the repository archive. Page says published October 30, 2026. |
| 2026-11-11 | [Independent reconstruction added](https://github.com/CambrianMinds/martian-cylinder/commit/d0a63274ada472d77a905268366f2fcbd21eed3d) | Local Git history first adds the independent reconstruction and Step 8 frozen-shape rear-boundary registration. Public availability of this particular commit was not independently checked in this review. |

Git dates are commit metadata, not independently certified first-publication times. The initial commit was also retrieved successfully through the connected GitHub tool, which returned its canonical public URL and timestamp 2026-10-24T08:15:33Z. The initial manuscript contains measurements and interpretations subsequently revised by the audits; its existence establishes chronology, not validation of all its original claims.

`CITATION.cff` records `date-released: 2026-10-28`. That differs from the verified Zenodo page's publication date of October 30. These may represent manuscript/release and deposit dates respectively; the October 28 field alone should not be presented as a verified Zenodo publication timestamp.

## Comparison of contributions

| Contribution | Earlier evidence located? | Priority conclusion |
| --- | --- | --- |
| Spotting or publicizing this object | Yes: Ward credits Bar Ilan; public discussion in 2025. | Not a new discovery by this project. |
| Calling its appearance cylindrical/artificial | Yes: Ward, MILTOID, Dobbs, Loeb. | Not the project's novel contribution. |
| Bayer decoding and image processing | Yes: MILTOID describes his script and decoding. | Cannot claim first technical processing of the target. |
| Overlaying a 3D cylinder / modeling its shadow | Yes: MILTOID explicitly describes both. | Cannot claim first geometric reconstruction or cylinder overlay. |
| Publishing reproducible subpixel metrology with numerical fit residuals for this target | No predecessor located. | Earliest located study is Bogner's repository; retain a scoped, qualified first claim. |
| Frozen-front-shape rear-boundary registration and predictive validation for this target | No predecessor located. | No competing prior result found; distinguish November reconstruction and subsequent validation from the original October paper. |

MILTOID's available transcript does not report boundary coordinates, numerical fit residuals, uncertainty estimates, or a frozen-parameter predictive test. That describes the accessible transcript, not an assertion that every silent video frame or linked comment was exhaustively inspected. His overlay must still receive credit as prior geometric visualization.

## Search scope and limitations

Searched exact and shortened PDS product IDs, Sol 3556 cylinder combinations, the report title and author, and combinations involving geometric analysis, ellipse fitting, subpixel/Sobel methods, residuals, photogrammetry, and the identified earlier authors. Followed the original sources linked from Loeb, Ward, and the VFX discussion. A scholarly search through Consensus returned instrument calibration, other Gale cylindrical features, and general photogrammetry work, but no earlier paper analyzing this exact 2022 target was located. This is a priority search; no additional rock-sampling comparison was performed.

Firecrawl Research commands were unavailable in the installed CLI; general web search, Firecrawl page/transcript retrieval, and the connected scholarly search were used. Browser/web retrieval failed for some pages, but Firecrawl successfully retrieved the Zenodo record and the two video transcripts. Rami Bar Ilan's site did not yield a dated target-specific original post. Search results also led to the VFX video through an alternate shared title, “VFX Artist Decodes NASA Mars Perfect Cylinder Anomaly.”

The report distinguishes **no predecessor located** from **no predecessor exists**. It does not certify global priority, peer review, or the physical origin of the target.

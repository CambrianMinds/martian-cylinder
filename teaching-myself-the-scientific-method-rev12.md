# Teaching Myself the Scientific Method

## Trial (and Mostly) Error

*By Justin Bogner*

I had an idea recently. It started the way most of my ideas do: someone on YouTube whose opinion I respect showed me something that I thought was worth knowing more about.

Not something practical. I wasn't watching videos about how to change a carburetor, or how to blend moss with yogurt and paint boulders with it.

I was watching a video about lunar anomalies. Someone might even have suggested that the Moon was hollow.

Most of what I was being shown was visible once someone explained what I was supposed to be seeing. But if I watched the same footage on mute, without the interpretation, the anomalies weren't always so apparent.

And then I noticed something that made me focus on the screen.

It was a pipe. Sticking out of some rocks.

On Mars. Obviously.

![NASA Curiosity Mastcam image, Sol 3556](assets/data__3556MR1025170721700585C00_DRCL.png)

**01 / The photograph that started it.** NASA Curiosity Mastcam, Sol 3556, 7 August 2022. The object is near the lower-right corner.

![Direct crop of the same Mastcam image](assets/data__crop_bottom_right.png)

I unmuted the video and rewound it.

Paraphrasing: *"In August 2022, NASA's Curiosity rover took a photograph on Mars. In the lower-right corner was something strange. A pipe, something like thirty centimeters long, perhaps a couple of inches in diameter."*

Yeah. Clearly. That's what it looks like.

But that was it. The episode was about *lunar* anomalies. This was a *Martian* sidenote. Perfectly reasonable.

But I wanted to know more.

And being someone who routinely uses AI to do the math I hate and write the technical papers I am incapable of writing, I figured this would be relatively straightforward.

I started looking for the original NASA data. It turns out NASA makes its rover imagery and a remarkable amount of associated mission data publicly available. As it should. NASA is funded by the citizens of the United States of America, and I sometimes wonder whether that actually means anything anymore.

Fortunately, here's an instance of something being done right. Without that public dataset, this investigation would not have been possible.

I wasn't trained to interpret it. It looked like technical data. JSON-adjacent, or something. Numbers and labels that presumably meant something to someone.

AI can tell me what those things mean in language I understand. Better still, I can ask it "Huh, what?" twenty-seven times in as many minutes and not feel like a moron.

Eventually, I realized that the mission information could help establish the position of the Sun when the photograph was taken.

Cool.

If I could figure out the object's angle, the position and orientation of the camera, where the object met the soil, and the direction of sunlight, I ought to be able to do something more useful than stare at a picture and decide what it looked like.

I could test whether the front face was circular, and whether the shadow of a round object partially buried in Martian soil was consistent with that geometry.

Mathematically.

## A Small Detour Before the Mathematics

We begin in Decatur, Indiana, in 1931.

My great-grandmother Flossie gave birth to a baby boy, Richard "Sam" Bogner, whose work would, a few decades later, help make the work I've done today possible.

Sam earned his bachelor's degree from Ball State Teachers College and received his master's degree in 1959. He became a chemical engineer at General Motors' Delco Remy in Anderson, Indiana.

In 1966, he joined the exodus of young engineers heading west for the space race, moving his family to Pasadena to work at NASA's Jet Propulsion Laboratory.

![Jet Propulsion Laboratory entrance, Pasadena](assets/data__jpl_sign_web.jpg)

*JPL entrance, Pasadena. Author archive.*

![Richard Sam Bogner](assets/data__uncle_sam.jpg)

*Richard “Sam” Bogner. Author archive.*

At JPL, he worked on the high-energy silver-zinc batteries that powered the Surveyor lunar landers. They had to survive rocket launches, lunar landings, extreme temperatures, and the rather inconvenient fact that getting a replacement delivered to the Moon was not an option.

From the Moon, his work moved outward to Mars.

He became a battery systems engineer on the Mariner program. I found his name in NASA's reports on the Mariner Mars 1971 mission [1].

Seeing his name there was profoundly humbling.

Mariner 9 arrived at Mars during a planet-wide dust storm and became the first spacecraft to orbit another planet. Once the atmosphere cleared, it photographed a world that had previously existed largely in human imagination.

And the spacecraft relied, in part, on electrical systems he had helped engineer.

![Mariner 9 before flight](assets/data__mariner9_final_checks.jpg)
![JPL Technical Memorandum 33-591, April 1973](assets/data__bogner_mariner1971_cover.png)

The more I looked into his work, the more I realized that saying Uncle Sam "worked on batteries" was a rather inadequate description of what he actually did.

Before he even joined JPL, he'd authored research for NASA on batteries capable of surviving the extreme heat required to sterilize spacecraft. His work on Mariner 9 wasn't simply a matter of installing a battery somebody else had designed. He documented the system's design, construction, testing, and actual performance in space. He subsequently worked on the Viking orbiter's battery system and co-authored research into improving the lifespan and energy capacity of batteries for future spacecraft.

A spacecraft can carry the most sophisticated instruments humanity has ever constructed, but they're not terribly useful without electricity. And replacing a failed battery somewhere between Earth and Mars presents certain logistical difficulties.

After JPL, Sam worked on commercial satellite systems at Hughes Space and Communications. In 1987, he worked on the battery system for the SunRaycer, a solar-powered vehicle developed by General Motors, AeroVironment, and Hughes for the inaugural World Solar Challenge across Australia. He co-authored the technical documentation describing its design and performance.

The SunRaycer won the race, arriving more than two days ahead of its nearest competitor. The car is in the Smithsonian's collection in Washington, D.C., though it is not currently on display.

![General Motors SunRaycer, 1987 World Solar Challenge](assets/data__sunraycer_web.jpg)

I grew up listening to my great-uncle tell stories about NASA, rocket ships, and the space race.

Just kidding.

Unfortunately, I don't recall ever meeting him.

Grandpa Alan mentioned him occasionally, but I was a kid and didn't pay attention. Less than a year ago, my dad mentioned the SunRaycer, and I began discovering what Uncle Sam had done.

I didn't think I could ever do anything as interesting. And now I found myself investigating an object on the same planet his work had helped humanity explore.

I hope that, in some small way, this investigation might continue my family's connection to the Red Planet.

## The Trouble With Teaching a Calculator to Think

The question was simple enough: was the object geometrically a cylinder, and could it cast the shadow in the photograph?

The answers were less straightforward. There were mathematical errors, some of them spectacular. The camera was interpreted incorrectly. We estimated the wrong size. At one point we couldn't even agree on which pixels belonged to the object.

Geometry, incidentally, is one of the few things I actually like about mathematics.

A circle doesn't suddenly behave differently because you find it somewhere inconvenient.

But apparently, according to my AI, it does.

Why?

Because this particular object was *on Mars*.

When we corrected an error, another objection would appear. At one point, the AI insisted that I compare the object with nearly two hundred other rocks.

Cool. I did that.

And we still hadn't answered the question.

### An Aside About Ignaz Semmelweis

![Portrait of Ignaz Semmelweis](assets/ignaz-semmelweis.png)

*Ignaz Semmelweis.*

There's a term for intellectual resistance of this sort: the *Semmelweis reflex*. Semmelweis, a nineteenth-century physician, discovered that handwashing dramatically reduced deaths from childbed fever. Many contemporaries resisted the finding. His name eventually became shorthand for the rejection of evidence because it disturbs an established explanation.

I found myself spending an extraordinary amount of time defending the proposition that a circle on Mars should obey the same mathematics as a circle anywhere else.

And in fairness, some of the objections were real. The AI found errors in the measurements, the camera interpretation, and our statistical comparisons. We corrected them, sometimes throwing away entire arguments.

Fine. That's what the scientific method is for.

But I had a problem with my approach, too. I kept asking larger questions and receiving larger answers. Each answer supplied another list of things to investigate. More measurements. More possibilities. More arguments.

Eventually I learned enough to recognize how little of that was necessary.

I didn't need to identify its composition, reconstruct its geological history, or catalogue every rock in Gale Crater. I needed to measure its geometry.

The exposed front rim. The straightness and direction of the barrel. The rear terminus. The shadow, separately.

The camera could tell us how the first three should appear. The recorded position of the Sun could test the fourth.

That was the experiment.

It had taken me weeks to figure out what to ask.

## What the Photograph Could Tell Us

First, the thing was considerably smaller than I'd been led to believe.

Most reliable-ish information I could find placed the object at about twenty centimeters long.

NASA's camera, however, had been focused at **3.957 meters**. The focus setting isn't a tape measure, but it was enough to make us reconsider the scale. Our working reconstruction put the object at roughly **3.2 centimeters long and 11 to 12 millimeters in diameter**.

Smaller than a AA battery.

Wonderful. We'd started with a mysterious pipe sticking out of the Martian landscape and ended up investigating something small enough to disappear into the bottom of a kitchen drawer.

The dark patch at the front looks like a single shape. It isn't. There is an exposed physical end, partly buried in soil, and there is a shadow cast onto the ground in front of it.

An AI has read about shadows. I have *stood* in them.

Our first ellipse fit had inadvertently included both boundaries. It gave us an axis ratio of **0.933**. The arithmetic was fine. The boundary wasn't.

**Mathematical sophistication does not guarantee that you're measuring the right thing.**

We went back to the calibrated photograph and measured the exposed rim alone. Sixty-one retained edge points fitted an ellipse **40.30 by 33.23 pixels**, with an axis ratio of **0.8246** and an error of **0.216 pixels**. A circle fitted to the same points missed by **0.727 pixels**.

The ellipse's short axis differed from the measured upper longitudinal edge by just **0.75 degrees**. That upper edge was straight to about **0.11 pixels** across twenty-five measurements.

Not millimeters. *Pixels.*

![Exposed-rim measurements and best-fit ellipse on the calibrated image](assets/figure-01-exposed-rim-fit.png)

**02 / The exposed rim.** The measured points follow the front boundary, not the cast shadow. The lower portion of the ellipse is a mathematical continuation.

Then a separate reconstruction started over with NASA's original **16-bit image data**, using different processing and edge selections. One front-rim measurement had wandered onto a neighboring pebble. Once corrected, the remaining **35 points** fitted an ellipse with an axis ratio of **0.833**, an error of **0.164 pixels**, and an upper-edge direction of **29.88 degrees** against our earlier **29.28 degrees**.

Different methods. Nearly identical geometry.

Then we measured the back.

I had been insisting that the curved boundary at the rear was the object's actual terminus. The apparent narrowing toward that end looked to me like soil hiding more of the underside, not necessarily a taper in the body.

So we measured the visible rear arc, then took the ellipse fitted to the front and translated it to the back **without changing its size or shape**.

It fitted the **24 exposed rear points with a root-mean-square error of 0.186 pixels**.

![Independently extracted front and rear points with identical translated ellipse profiles](assets/figure-09-front-rear-overlay.png)

**03 / The other end.** The same ellipse, translated from front to rear. The exposed rear points follow the curve while soil obscures the lower portion.

Finally, we fitted the front rim, rear arc, and longitudinal feature together. A constant-diameter cylindrical reconstruction matched all **85 points** with an overall error of **0.292 pixels**.

Less than a third of one native image pixel, across three separate features.

And the shadow?

NASA recorded the Sun at **69.82 degrees above the horizon**, at an azimuth of **186.82 degrees**. Using the measured geometry and camera model, we projected sunlight from the front rim onto the ground. The calculated shadow curved forward, exactly where the photograph suggested it should.

A level receiving surface gave the wrong outline. Allowing the local ground to fall away in front of the object made the prediction fit. We then checked that prediction against shadow pixels extracted from the unannotated image at nine brightness thresholds. At the central threshold, the projected curve differed from the extracted boundary by **1.05 pixels**, compared with **6.75 pixels** for the level-ground model.

![Raw shadow-edge positions at three brightness thresholds](assets/figure-04-raw-shadow-boundary.png)

**04 / The shadow.** Raw-image shadow-edge measurements compared with projected sunlight on level and inclined receiving ground. The model follows the photographed shadow rather than the outline I had drawn.

![The original visual comparison of drawn and projected shadow boundaries](assets/figure-08-user-visual-comparison.png)

**05 / User boundary vs. solar projection.** I had drawn the blue shadow boundary before the reconstruction. The calculated curve followed it closely, too.

That was the answer I had been looking for.

The front and rear geometry matched. The body was straight. A single cylinder model accounted for all three. And its predicted shadow was compatible with the one Curiosity photographed.

## So What the Hell Is It?

I don't know.

NASA, incidentally, had already offered an answer.

In March 2026, a spokesperson [told the *New York Post*](https://nypost.com/2026/03/28/world-news/mystery-solved-nasa-identifies-party-hat-shaped-object-that-perplexed-experts/) that the object was a rock shaped by Martian winds. The spokesperson also suggested *pareidolia*, the tendency to see familiar shapes in otherwise ordinary things.

Fair enough.

NASA also said the object was photographed from approximately thirteen feet away and measured about one centimeter across.

Thirteen feet is 3.96 meters. Remember that camera focus setting? **3.957 meters.**

And our calculated diameter? About eleven millimeters.

Wonderful. We agreed on how big the thing was.

What I hadn't found was a geometric explanation of how Martian winds produced it.

Apparently, that was the part I was supposed to supply myself.

Wind isn't a lathe. Martian geology can produce strange forms, and I examined several possibilities. None of the ones I found explained the mathematically perfect cylinder.

Something from Curiosity? Possibly. I haven't identified a component that matches the object or accounts for its location.

Something manufactured by someone else?

I won't pretend the possibility doesn't interest me. I'd love to find evidence of an ancient technological presence on Mars.

In March 2026, Avi Loeb also [argued that Curiosity ought to take another look](https://avi-loeb.medium.com/is-the-mysterious-cylinder-on-mars-photographed-in-2022-by-the-curiosity-rover-a-human-made-6fcd8e242fea) [2]. He estimated its length at about twenty centimeters.

But on the important point, I agree.

There's a rover on Mars carrying instruments that could tell us considerably more about this object than another thousand hours of staring at pixels.

Why not use them?

## Why This Actually Matters

Partly because it's an interesting object on Mars. I don't think that requires much justification.

But I also had an entire laboratory at my disposal.

NASA provided the photographs, calibration data, and the Sun's position. AI gave me ways to interrogate them: camera models, subpixel measurements, geometric comparisons, solar projections, figures, code, and reproducible analyses. I could ask one question, inspect the answer, recognize what it left unresolved, and ask a better one.

In the end, the problem didn't require more and more information. It required knowing which information mattered.

Once I had reduced the investigation to a few physical boundaries and the exact conclusion they needed to support, we settled problems that had occupied us for weeks in only a handful of prompts.

I didn't need a university laboratory. I needed access to the data, the tools, and the patience to figure out what to ask them.

**Rigor is not the number of objections you can generate.**

It's knowing which ones matter.

## What I Know

I still don't know what that object is. But now I know that it's actually cylindrical. And I know that it shouldn't be there.

Progress.

And also.

**This object is a proof of existence.**

Not proof of what it is. Proof that the category exists. There is at least one object in the Martian photographic record whose measurable geometry presents a genuine anomaly, one the explanations we've examined have not satisfactorily accounted for.

And make no mistake: a mathematically regular cylinder, half-buried in Martian dirt, *is* extraordinary.

Either Martian geology possesses an entirely unknown physical mechanism capable of producing a straight, circular cylinder with matching ends, or we're looking at something manufactured that isn't ours.

Either answer is thrilling.

The point isn't to collect mysteries. It's to build knowledge.

People are already doing this with other things. Ancient hard-stone vases, some at least four thousand years old, are being scanned and measured to remarkable precision. The people working on the [Vase Scan Project](https://unchartedx.com/site/vase-scan-resources/) [3] have made it possible to examine the geometry even when we don't know precisely how the objects were made.

Same here.

I've seen plenty of interesting things in photographs of Mars. I'm going to measure more of them. Because I want to know.

The source data and methods for this one are [publicly available](https://github.com/CambrianMinds/martian-cylinder) [4]. Anyone can repeat the work, challenge the measurements, or carry it further than I have.

I happened to find my object in a YouTube video that I'm almost certain was about the Moon being a spaceship. Hardly an exhaustive survey of the Martian surface.

I have no idea what other people might find. That's rather the point.

**We are allowed to look, and we are allowed to wonder.**

## References and Reproduction

**[1]** R. S. Bogner, *Mariner Mars 1971 Battery Subsystem*, JPL Technical Memorandum 33-591, Jet Propulsion Laboratory, Pasadena, CA (1973). [NASA NTRS](https://ntrs.nasa.gov/).

**[2]** Avi Loeb, “Is the Mysterious Cylinder on Mars, Photographed in 2022 by the Curiosity Rover, a Human-Made Debris?,” *Medium* (March 7, 2026). [Article](https://avi-loeb.medium.com/is-the-mysterious-cylinder-on-mars-photographed-in-2022-by-the-curiosity-rover-a-human-made-6fcd8e242fea).

**[3]** *The Vase Scan Project*: precision metrology resources and 3D scan data. [UnchartedX](https://unchartedx.com/site/vase-scan-resources/).

**[4]** *Martian Cylinder Investigation*: source images, calibration, scripts, front/rear reconstruction, and reports (2026). [GitHub repository](https://github.com/CambrianMinds/martian-cylinder).

The [independent reconstruction](https://github.com/CambrianMinds/martian-cylinder/tree/d0a63274ada472d77a905268366f2fcbd21eed3d/independent-reconstruction) documents the 16-bit image measurements and 85-point joint fit. The [earlier image and shadow analysis](https://github.com/CambrianMinds/martian-cylinder/blob/d0a63274ada472d77a905268366f2fcbd21eed3d/most-recent-work.md) documents the separate raw-image shadow comparison.

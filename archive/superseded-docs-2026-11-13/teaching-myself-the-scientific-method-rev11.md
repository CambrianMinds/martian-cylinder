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

Before someone decides that my inability to write technical papers means I'm incapable of scientific research, let me clarify something. I cannot write efficiently in LaTeX, do trigonometry without help, or stomach several conventions of academic writing. None of that means I cannot ask a meaningful question, recognize a flawed assumption, evaluate evidence, or apply the scientific method.

Those are different capacities.

I started looking for the original NASA data. It turns out NASA makes its rover imagery and a remarkable amount of associated mission data publicly available. As it should. NASA is funded by the citizens of the United States of America, and I sometimes wonder whether that actually means anything anymore.

Fortunately, here's an instance of something being done right. Without that public dataset, this investigation would not have been possible.

I wasn't trained to interpret it. It looked like technical data. JSON-adjacent, or something. Numbers and labels that presumably meant something to someone.

AI can tell me what those things mean in language I understand. Better still, I can ask it "Huh, what?" twenty-seven times in as many minutes and not feel like a moron.

Eventually, I realized that the mission information could help establish the position of the Sun when the photograph was taken.

Cool.

If I could figure out the object's angle, the position and orientation of the camera, where the object met the soil, and the direction of sunlight, I ought to be able to do something more useful than stare at a picture and decide what it looked like.

I could test whether the front face was circular, and whether the shadow of a round object partially buried in Martian soil was consistent with that geometry. Basically, is it actually cylindrical?

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

## Less Math, Better Questions

The thing I wanted to know was simple enough: was this object geometrically a cylinder, and could it cast the shadow in the photograph?

That turned out to be simultaneously one of the easiest questions to answer and one of the hardest to keep my AI collaborator focused on.

There were mathematical errors, some of them spectacular. There were mistakes about the camera, mistakes about the size of the object, and mistakes about what was even part of the object. We corrected them. Occasionally, my AI collaborator would then produce an entirely new objection to a conclusion the corrected measurements already supported.

Geometry, incidentally, is one of the few things I actually like about mathematics.

A circle doesn't suddenly behave differently because you find it somewhere inconvenient.

But apparently, according to my AI, it does.

Why?

Because this particular object was *on Mars*. And we didn't have a coherent explanation for why it was there.

At one point, it insisted that I compare the thing to nearly two hundred other rocks.

Cool. I did that.

And we still hadn't answered my question.

### An Aside About Ignaz Semmelweis

![Portrait of Ignaz Semmelweis](assets/ignaz-semmelweis.png)

Ignaz Semmelweis

There's a term for a particular kind of intellectual resistance: the *Semmelweis reflex*. Ignaz Semmelweis, a nineteenth-century physician, discovered that requiring doctors to wash their hands dramatically reduced deaths from childbed fever. Many contemporaries resisted his findings. The term now describes rejecting evidence because it conflicts with established assumptions.

I'm not equating a Martian object with a medical discovery. That would be ridiculous.

But an institution can become so accustomed to its explanations that those explanations determine which evidence is acceptable. An AI trained on our writing can acquire some of the same habits.

An anomaly isn't an explanation. It's an observation our existing explanations haven't satisfactorily accounted for. [2]

The solution isn't to believe every anomaly. It's to examine the evidence without requiring it to produce a comfortable answer.

Not as an institutional credential.

As a discipline of reasoning.

## Learning to Ask Better Questions

Eventually, I stopped trying to get my AI to agree with me and started examining *how we were asking the question*.

Why did an unidentified alternative count as equally supported? Why did every resolved objection produce another? And why were we collecting measurements that couldn't actually answer what I'd asked?

I didn't need something to tell me I was right. I needed something capable of telling me *why* I was wrong, preferably before I published something demonstrating to the entire internet that I didn't understand basic geometry.

To its credit, the AI found real errors in the measurements, the camera interpretation, and our statistical comparisons. Some arguments had to be thrown out entirely.

Fine. That's what the scientific method is supposed to look like.

But there was a problem with my approach, too. I kept asking larger and larger questions. Every answer gave me more information. More numbers. More possible explanations. More things to check.

Eventually, I knew enough to notice that most of them weren't necessary.

And my work required remarkably little information: the exposed front rim, the direction and straightness of the body, and the shape of the rear terminus. The camera data told us how those features should appear from that viewing angle. The Sun's position could then be used to check the shadow separately.

That's it.

I didn't need to know what the object was made of. I didn't need a manufacturing history. I certainly didn't need a collection of other rocks to decide whether this one had a circular end.

I needed to know which pixels belonged to which physical feature, and what result would be required for a cylinder to explain them.

**The central geometric observations kept surviving.**

## But How Big Is It?

One of the first surprises was that the thing was considerably smaller than I'd been led to believe.

Remember that estimate from the video? Thirty centimeters long? Other accounts had put it closer to twenty.

Those estimates seemed to assume that the object sat on a distant cliff, roughly forty-five meters away. But NASA's camera had been focused at about **3.96 meters**. That isn't a tape measure, but it was a useful reason to reconsider the scale.

Our working reconstruction put the object at roughly **3.2 centimeters long and 11 to 12 millimeters in diameter**.

Smaller than a AA battery.

We'd even discovered that part of what we initially called its length belonged to the rocks behind it.

Wonderful. We'd started with a mysterious pipe sticking out of the Martian landscape and ended up investigating something small enough to disappear into the bottom of a kitchen drawer.

Now, the geometry.

The dark patch at the front looks like one continuous shape. It isn't. Part of it is the exposed physical end of the object. Part of it is a shadow cast onto the soil.

Early on, the computer combined the two into a single outline.

An AI has read about shadows. I have *stood* in them.

One is solid physical material; the other is what happens when sunlight is blocked. If you combine them into one shape, you can perform perfectly valid mathematics on a boundary that doesn't actually exist. You can produce some very impressive charts—and they'll be completely wrong. Our first ellipse fit had included both, producing an axis ratio of **0.933**.

Perfect mathematics performed on the wrong physical boundary.

Once we separated the two, the shadow became a straightforward question: *could this measured cylinder actually cast the dark shape we see on the ground?*

NASA's metadata records the Sun at **69.82 degrees above the horizon**, at an azimuth of **186.82 degrees**. When we projected sunlight past the reconstructed 3D front rim onto the sloping ground in front of it, the calculated shadow followed the dark patch on the dirt to within about a single pixel.

The shadow didn't have to match the buried part of an ellipse. It never should have been asked to. It didn't contradict the cylinder—it confirmed it.

Then we isolated the exposed rim itself. The resulting ellipse measured **40.30 by 33.23 pixels**, with an axis ratio of **0.8246** and a fitting error of just **0.216 pixels**.

A circular face viewed at an angle appears elliptical. And the ellipse's short axis pointed within 0.75 degrees of the independently measured upper longitudinal edge.

![Exposed-rim measurements and best-fit ellipse on the calibrated image](assets/figure-01-exposed-rim-fit.png)

**02 / The exposed rim.** The measured points follow the physical front boundary, not the cast shadow. The lower ellipse is a mathematical continuation, not something traced in the dirt.

The upper edge itself was remarkably straight. Twenty-five measured points followed a line with a root-mean-square deviation of about **0.11 pixels**. The bright feature running along the barrel differed from that edge's direction by just **0.43 degrees**.

Not millimeters. *Pixels.*

Then a separate reconstruction, working from NASA's original **16-bit image data** rather than our previous edge selections, produced nearly the same result. After removing one front-rim point that had jumped onto a neighboring pebble, **35 points** fitted an ellipse with an axis ratio of **0.833** and an error of **0.164 pixels**. Its measured upper-edge direction was **29.88 degrees**, against our earlier **29.28 degrees**.

Different data processing. Different edge selection. Essentially the same geometry.

I was confident that the curved feature at the back was the actual end of the object, not a random line in the soil. I could see fairly easily that the curve was basically the diameter of the front face. So, in the new reconstruction I treated it as a physical boundary.

We took the same front ellipse, without changing its size or shape, and moved it back along the object.

Across the exposed curve, it followed 24 out of 24 clean points to within 0.186 pixels (with the remaining 8 points on the lower flank tracing where the dirt buries the bottom of the tube).

![Independently extracted front and rear points with identical translated ellipse profiles](assets/figure-09-front-rear-overlay.png)

**03 / The other end.** Cyan marks the exposed front rim, yellow the exposed rear terminus. The yellow curve is an unscaled copy of the front ellipse, moved to the back. The source photograph is shown beneath the measurements.

So we had a curved front face, a straight barrel, and a rear terminus matching the front curve. The apparent narrowing toward the back could be accounted for by the soil hiding more of the object there.

Finally, we combined the measurements. A single constant-diameter cylinder model, allowing the illuminated upper line to occupy its measured position on the barrel, fitted **85 points** from the front, rear, and longitudinal feature with an overall error of **0.292 pixels**.

That was the geometry I had been trying to establish.

| Measurement | Result |
| --- | ---: |
| Exposed front rim, first calibrated-image analysis | Ellipse ratio **0.8246**, fit error **0.216 px** |
| Independent 16-bit front-rim analysis | Ellipse ratio **0.833**, fit error **0.164 px** |
| Longitudinal edge | **0.11 px** straight-line error in the earlier analysis |
| Rear terminus, unchanged front-ellipse profile | **0.186 px** fit error across 24 points |
| Combined front, rear, and barrel reconstruction | **0.292 px** fit error across 85 points |

*These are image measurements, not declarations about composition or origin. The source data and reproducible procedures are in the [research repository](https://github.com/CambrianMinds/martian-cylinder).*

## So What the Hell Is It?

I don't know.

I didn't discover who put it there, what it was made of, or how long it had been in the dirt. Nor did I establish that it was manufactured.

What I established, through an investigation considerably more involved than I ever intended, was a defensible geometric interpretation of an object I still cannot identify.

NASA, incidentally, had already offered an answer.

In March 2026, a spokesperson [told the *New York Post*](https://nypost.com/2026/03/28/world-news/mystery-solved-nasa-identifies-party-hat-shaped-object-that-perplexed-experts/) that the object was a rock shaped by Martian winds. The spokesperson also suggested *pareidolia*, the tendency to see familiar shapes in otherwise ordinary things.

Fair enough.

NASA also said the object was photographed from approximately thirteen feet away and measured about one centimeter across.

Thirteen feet is 3.96 meters. Remember that camera focus setting I pulled from NASA's own telemetry? 3.957 meters.

And our calculated diameter? Eleven millimeters.

So NASA and I had arrived at almost exactly the same scale.

Wonderful. We agreed on how big the thing was.

What I hadn't found in NASA's explanation was an actual geometric analysis demonstrating how Martian winds produced this anomaly.

Apparently, that was the part I was supposed to supply myself.

But an anomaly is supposed to provoke investigation.

If the object were readily explained by the geology of Gale Crater or by something Curiosity had deposited there, we wouldn't have much of a mystery.

The interesting question was whether either explanation actually accounted for what we could measure.

There are several possibilities worth considering.

### 1. Something From Curiosity

Perhaps it's a component from the rover or debris associated with the mission.

That would explain why a manufactured-looking object might appear on Mars. But identifying it as spacecraft hardware requires more than noticing that it resembles a mechanical part.

We would need a plausible component and a way for it to reach that location. The rover's landing hardware was deposited far away, and the object's apparent burial raises additional questions.

Those questions aren't proof that it *isn't* spacecraft debris. They're reasons the explanation deserves examination rather than automatic acceptance.

Despite looking through the available engineering information, I haven't found a component that satisfactorily accounts for the observation.

### 2. A Geological Formation

The other obvious possibility is that it's a rock.

Mars has genuinely strange rocks. Wind can carve ventifacts; minerals can form concretions and unusual structures.

But a process that makes unusual shapes does not explain this particular one.

Wind isn't a lathe. Concretions aren't restricted to spheres, either. Geology is more complicated than that.

The relevant question is whether a proposed process explains the object's measured geometry and visible surroundings.

The examples we examined didn't satisfactorily explain it. That doesn't mean one cannot exist.

And if someone has a geological explanation that accounts for the observations, I'd genuinely like to see it.

### 3. Something We Haven't Identified

The object could be something manufactured. It could have an unfamiliar geological origin. It could be something we haven't considered.

If I am being completely candid about what kept me up late staring at pixel grids, I sincerely hope that this might turn out to be evidence of something extraordinary.

Perhaps even an ancient technological presence on Mars.

A closer look would help. Curiosity carries instruments that can examine surface details and chemical composition. That could distinguish geological material from manufactured metal far better than more calculations on the same photograph.

I'm not the first person to suggest that NASA ought to take another look.

Harvard astrophysicist Avi Loeb wrote about this very object in March 2026 [3], arguing that Curiosity should return to examine it more closely rather than simply assume it was debris from the mission.

He also estimated that it was about twenty centimeters long, which, as we've established, appears to have been rather generous.

But on the more important question, I agree with him.

We have a rover on Mars equipped with instruments capable of examining precisely the sorts of details that might resolve this. And we have an object whose appearance has generated enough uncertainty to warrant a closer look.

Why not use them?

Until we do, we have an unidentified object with measurable geometry.

And that's unacceptable.

## Why This Actually Matters

Partly because it's an interesting object on Mars. I don't think that requires much additional justification.

NASA made the data public. I could examine it without permission from a university or funding committee.

And I had something I hadn't appreciated at first: a laboratory I could call up whenever I needed it. Camera models, measurements to fractions of a pixel, comparisons between different geometries, solar projections, graphs, code, and a way to rerun the whole thing.

The work didn't suddenly become easy because the computer got smarter. It became manageable because I had finally learned what to ask it to do.

Once I defined the measurements and the exact result I was testing for, the last problems that had occupied us for so long were settled in a handful of prompts.

I could do the investigation. And anyone could examine the data afterward.

**Rigor is not the number of objections you can generate.**

It's asking whether claims follow from evidence, correcting errors, and knowing when objections are no longer materially relevant.

That standard applies to extraordinary claims. It also applies to ordinary explanations.

If I must demonstrate why a cylindrical interpretation fits the measurements, an alternative geometry should explain them too. Not merely insist that another explanation *must* be possible.

That isn't a demand for agreement. It's a demand for consistency.

## What I Know

I still don't know what that object is. But now I know that it's actually cylindrical. And I know that it shouldn't be there.

Progress.

And also.

**This object is a proof of existence.**

Not proof of what it is. Proof that the category exists. There is at least one object in the Martian photographic record whose measurable geometry presents a genuine anomaly, one that the conventional explanations we've examined have not satisfactorily accounted for.

There are plenty more. People have been finding interesting things in photographs of Mars for decades. I've seen quite a few myself. I'm going to measure them. Because I want to know.

This is the first, at least for me. I'll record more. I've also decided to investigate, measure, and document in a way that someone else could reproduce. [4]

NASA has made an extraordinary amount of planetary data publicly available. Anyone can examine the original photographs, question the measurements, challenge the interpretations, or develop better methods.

I didn't need permission to investigate this object. I needed access to the evidence and a way to test the question.

We can investigate things. Measure them. Publish the results, including the ones that turn out to have perfectly ordinary explanations. People are rigorously measuring ancient precision hard stone vases that are in some recorded cases *at least* four thousand years old. And finding sub-millimeter precision. We still have no idea how they were made. But thanks to the people working on the vase scan project [5], we know what they measure. They exist. So we should find out how.

Same here.

Because the point isn't to collect mysteries. It's to build knowledge.

And make no mistake: finding a mathematically uniform circular cylinder lying half-buried in the Martian dirt *is* extraordinary. It leaves us staring at a fascinating, inescapable fork in the road.

Either Martian geology possesses an entirely unknown physical mechanism capable of carving or cementing a right cylinder with matching ends—which would be a massive planetary discovery in its own right—or we are looking at something manufactured that isn't ours.

Either answer is thrilling. Either answer means this isn't just "another rock."

A reproducible investigation doesn't need to resolve the entire cosmic mystery overnight to matter. What it does is rescue an anomaly from blurry internet speculation and anchor it in hard, verifiable geometry. It gives the scientific community something real to test, challenge, and build upon.

I happened to find my object in a YouTube video that I'm almost certain was about the moon being a spaceship. Hardly an exhaustive survey of the Martian surface.

I have no idea what other people might find. That's rather the point.

**We are allowed to look, and we are allowed to wonder.**

## References and Reproduction

**[1]** R. S. Bogner, *Mariner Mars 1971 Battery Subsystem*, JPL Technical Memorandum 33-591, Jet Propulsion Laboratory, Pasadena, CA (1973). [NASA NTRS](https://ntrs.nasa.gov/).

**[2]** Thomas S. Kuhn, *The Structure of Scientific Revolutions*, University of Chicago Press (1962). [Publisher](https://press.uchicago.edu/ucp/books/book/chicago/S/bo13179781.html).

**[3]** Avi Loeb, "Is the Mysterious Cylinder on Mars, Photographed in 2022 by the Curiosity Rover, a Human-Made Debris?," *Medium* (March 7, 2026). [Online](https://avi-loeb.medium.com/is-the-mysterious-cylinder-on-mars-photographed-in-2022-by-the-curiosity-rover-a-human-made-6fcd8e242fea).

**[4]** Martian Cylinder Investigation: primary source data, calibrated scripts, independent reconstruction, and reports (2026). [GitHub Repository](https://github.com/CambrianMinds/martian-cylinder).

**[5]** The Vase Scan Project, precision metrology resources and 3D scan data (2023). [UnchartedX](https://unchartedx.com/site/vase-scan-resources/).

The [new independent reconstruction](https://github.com/CambrianMinds/martian-cylinder/tree/d0a63274ada472d77a905268366f2fcbd21eed3d/independent-reconstruction) supplies the front and rear rim measurements, the 85-point joint fit, method descriptions, and the original-image provenance. The earlier [shadow reproducibility package](https://github.com/CambrianMinds/martian-cylinder/blob/d0a63274ada472d77a905268366f2fcbd21eed3d/most-recent-work.md) documents the raw-image boundary comparison.

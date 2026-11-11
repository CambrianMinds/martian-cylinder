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

\*[Illustration: 01 / The photograph and the crop · Curiosity Mastcam, Sol 3556, 7 August 2022. Main image: calibrated NASA Planetary Data System photograph. Inset: direct crop of the archived frame, without AI upscaling or invented detail. View source ↗]\*

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

I could test whether the front face was circular, and whether the shadow of a round object partially buried in Martian soil was consistent with that geometry.

Mathematically.


## A Small Detour Before the Mathematics

We begin in Decatur, Indiana, in 1931.

My great-grandmother Flossie gave birth to a baby boy, Richard "Sam" Bogner, whose work would, a few decades later, help make the work I've done today possible.

Sam earned his bachelor's degree from Ball State Teachers College and received his master's degree in 1959. He became a chemical engineer at General Motors' Delco Remy in Anderson, Indiana.

In 1966, he joined the exodus of young engineers heading west for the space race, moving his family to Pasadena to work at NASA's Jet Propulsion Laboratory.

\*[Illustration: Pasadena, California · Jet Propulsion Laboratory, from the author’s research archive.]\*\*[Illustration: Richard “Sam” Bogner · Portrait from the author’s research archive.]\*

At JPL, he worked on the high-energy silver-zinc batteries that powered the Surveyor lunar landers. They had to survive rocket launches, lunar landings, extreme temperatures, and the rather inconvenient fact that getting a replacement delivered to the Moon was not an option.

From the Moon, his work moved outward to Mars.

He became a battery systems engineer on the Mariner program. I found his name in NASA's reports on the Mariner Mars 1971 mission.

Seeing his name there was profoundly humbling.

Mariner 9 arrived at Mars during a planet-wide dust storm and became the first spacecraft to orbit another planet. Once the atmosphere cleared, it photographed a world that had previously existed largely in human imagination.

And the spacecraft relied, in part, on electrical systems he had helped engineer.

\*[Illustration: Mariner 9 · Spacecraft during preflight preparation.]\*
\*[Illustration: JPL Technical Memorandum 33-591 · April 1973. NASA archive ↗]\*

The more I looked into his work, the more I realized that saying Uncle Sam "worked on batteries" was a rather inadequate description of what he actually did.

Before he even joined JPL, he'd authored research for NASA on batteries capable of surviving the extreme heat required to sterilize spacecraft. His work on Mariner 9 wasn't simply a matter of installing a battery somebody else had designed. He documented the system's design, construction, testing, and actual performance in space. He subsequently worked on the Viking orbiter's battery system and co-authored research into improving the lifespan and energy capacity of batteries for future spacecraft.

A spacecraft can carry the most sophisticated instruments humanity has ever constructed, but they're not terribly useful without electricity. And replacing a failed battery somewhere between Earth and Mars presents certain logistical difficulties.

After JPL, Sam worked on commercial satellite systems at Hughes Space and Communications. In 1987, he worked on the battery system for the SunRaycer, a solar-powered vehicle developed by General Motors, AeroVironment, and Hughes for the inaugural World Solar Challenge across Australia. He co-authored the technical documentation describing its design and performance.

The SunRaycer won the race, arriving more than two days ahead of its nearest competitor. The car is in the Smithsonian's collection in Washington, D.C., though it is not currently on display.

\*[Illustration: The SunRaycer · Winner of the inaugural 1987 World Solar Challenge. Smithsonian collection ↗]\*

I grew up listening to my great-uncle tell stories about NASA, rocket ships, and the space race.

Just kidding.

Unfortunately, I don't recall ever meeting him.

Grandpa Alan mentioned him occasionally, but I was a kid and didn't pay attention. Less than a year ago, my dad mentioned the SunRaycer, and I began discovering what Uncle Sam had done.

I didn't think I could ever do anything as interesting. And now I found myself investigating an object on the same planet his work had helped humanity explore.

I hope that, in some small way, this investigation might continue my family's connection to the Red Planet.


## The Trouble With Teaching a Calculator to Think

The thing I initially wanted to know was simple enough: did the Sun cast the right size shadow for this thing to be a cylinder?

That turned out to be simultaneously one of the easiest questions to answer and one of the hardest conclusions to get my AI collaborator to acknowledge.

There were mathematical errors, some of them spectacular. But once corrected, another problem became apparent: my collaborator, my calculator, kept raising objections even after the problems they identified had been resolved.

Geometry, incidentally, is one of the few things I actually like about mathematics.

A circle doesn't suddenly behave differently because you find it somewhere inconvenient.

But apparently, according to my AI, it does.

Why?

Because this particular object was *on Mars*. And we didn't have a coherent explanation for why it was there.

So it did what academia, at its worst, can do with an anomaly: nitpicked details that didn't affect the conclusion, demanded more testing, and raised another objection whenever one was resolved.

An anomaly isn't an explanation. It's an observation that our existing explanations haven't satisfactorily accounted for. [[09]](#ref-kuhn)

At one point, it insisted that I compare the object to nearly two hundred other rocks.

Cool. I did that.

It still wouldn't acknowledge what the measurements were telling us.

![Portrait of Ignaz Semmelweis](assets/ignaz-semmelweis.png)

Ignaz Semmelweis

### An Aside About Ignaz Semmelweis

There's a term for a particular kind of intellectual resistance: the *Semmelweis reflex*.

Ignaz Semmelweis, a nineteenth-century physician, discovered that requiring doctors to wash their hands dramatically reduced deaths from childbed fever. Many contemporaries resisted his findings. The term now describes rejecting evidence because it conflicts with established assumptions.

I'm not equating a Martian object with a medical discovery, or suggesting that every unconventional claim deserves belief because someone once rejected handwashing. That would be ridiculous.

But an institution can become so accustomed to its explanations that those explanations determine which evidence is acceptable.

AI systems are trained on enormous amounts of human writing. They encounter our discoveries, but also the assumptions and intellectual fashions surrounding them.

Our digital mirror has learned quite a lot about how we think.

Perhaps some of the ways we *fail* to think, too.

The solution isn't to believe every anomaly. It's to examine the evidence without requiring it to produce a comfortable answer. That is where the scientific method matters.

Not as an institutional credential.

As a discipline of reasoning.


## Learning to Disagree Productively

Eventually, I stopped arguing about the object and started arguing with the AI about *how it was reasoning*.

Why did an unidentified alternative count as equally supported? Why did every resolved objection produce another? Why should the same mathematics face a different standard on Mars?

I didn't need something to tell me I was right. I needed something capable of telling me *why* I was wrong, preferably before I published something demonstrating to the entire internet that I didn't understand basic geometry.

I needed a collaborator that could distinguish between a problem with the evidence and a problem with its implications. So I changed my approach.

What was wrong with the measurements? Which assumptions were supported by the photograph? And if the cylindrical interpretation was incorrect, what alternative geometry explained the observations better?

Because "it could be a rock" is not an explanation of geometry.

It's a statement about what rocks are allowed to be.

And rocks are allowed to be all sorts of things. I wasn't disputing that.

I was asking about *this* thing.

To its credit, the AI found real errors in measurements, camera interpretation, and statistical comparisons. We corrected them, sometimes throwing out entire lines of argument.

Fine. That's what the scientific method is supposed to look like.

But something interesting happened as we did this.

**The central geometric observations kept surviving.**

We reproduced the fitted curvature of the exposed end, which produced an ellipse. We measured the remarkably straight longitudinal boundary against the illuminated feature along the body. And we tested the shadow against the Sun's position, the object's orientation, and its apparent burial in the soil.

These weren't just different ways of saying that it looked like a pipe. They were measurements of different features that had to make sense together.

The measurements agreed with a coherent physical reconstruction.

Because we could calculate them, reproduce them, and check the results.

And one of the first surprises was that the thing was considerably smaller than I'd been led to believe.

Remember that estimate from the video? Thirty centimeters long? Other accounts had put it closer to twenty.

Those estimates appeared to depend on the assumption that the object was sitting on a distant cliff, roughly forty-five meters away.

But NASA's mission data contained something useful: the camera's focus setting.

The Mastcam focus motor had been set to a position corresponding to approximately 3.96 meters. Now, a camera's focus setting isn't a tape measure. It doesn't establish the precise distance to everything in the photograph. But combined with the surrounding terrain and the camera's optical properties, it gave us good reason to reconsider the object's apparent size.

Our revised geometric reconstruction put it at approximately 3.2 centimeters long and 11 millimeters in diameter.

Smaller than a AA battery.

We even had to correct our own initial estimate after discovering that part of what we'd been treating as the object's length actually belonged to the rocks behind it.

Wonderful. We'd started with a mysterious pipe sticking out of the Martian landscape and ended up investigating something small enough to disappear into the bottom of a kitchen drawer.

But size was only part of the story.

First, we had to be sure which edge we were measuring.

The dark shape at the front is deceptive. The cylinder's exposed end is one surface. The shadow it casts on the soil is another. In the original analysis we'd let those two regions influence the same contour. The resulting ellipse had an axis ratio of 0.933. The arithmetic was fine. The boundary wasn't.

So we went back to the calibrated NASA image and followed *only the exposed physical rim*. We selected sixty-three candidate edge points, discarded two that jumped onto nearby terrain, and fitted an ellipse to the remaining sixty-one. We used those same points to fit a circle for comparison.

The ellipse measured **40.30 by 33.23 native image pixels**, giving a short-to-long diameter ratio of **0.8246**. Its fitting error was just **0.216 pixels**. A circle fitted to the same measurements missed by **0.727 pixels**, over three times as much.

That is what a circular end looks like when the camera isn't looking straight down its axis. The fitted proportions correspond to a viewing angle of approximately 34.5 degrees from the face's normal.

![Native-pixel measurements on the exposed upper rim, comparing the best-fit ellipse with an axis-constrained ellipse. Two discontinuous terrain-edge picks are excluded.](assets/figure-01-exposed-rim-fit.png)

**02 / Measuring the actual rim.** Cyan points come from the calibrated Mastcam image, not the colored annotation. The lower dotted continuation is the extrapolated ellipse, not a traced shadow. Red crosses mark the two rejected terrain detections. Measurements and methods: accompanying reproducibility package.

Then there was the body.

We measured twenty-five points along its visible upper boundary. They followed a straight line with a fitting error of about **0.11 pixels**. Not millimeters. *Pixels.*

The bright feature running along the barrel followed almost the same direction, differing by **0.43 degrees**. And the direction of the ellipse's short axis, measured separately from the front rim, differed from that longitudinal edge by **0.75 degrees**.

We changed the smoothing and starting positions to check the fit. The ellipse's proportions stayed close to 0.82. Removing larger stretches of the rim moved its estimated angle more noticeably, which is why that 0.75-degree agreement belongs to the full selected arc, not to every possible partial fit.

Individually, a curved end or a straight edge is not particularly revolutionary. But here they were, together, on the same object, with measurements that agreed.

WHAT THE PHOTOGRAPH ACTUALLY TELLS US

| Feature | What we measured |
| --- | --- |
| Exposed front rim | 61 native-pixel points; ellipse 40.30 × 33.23 px, ratio 0.8246; fitting error 0.216 px. |
| Projected orientation | Ellipse minor axis 28.53°; upper longitudinal edge 29.28°; difference 0.75°. |
| Visible upper edge | 25 points; straight-line RMS error 0.111 px. |
| Surface highlight | Runs within 0.43° of the upper edge. |
| Approximate scale | Working reconstruction about 3.2 cm long and 11–12 mm in diameter, using nominal focus range. |

All ellipse and edge errors are in native Mastcam pixels. The physical scale depends on the estimated object distance.

The geometry was consistent with a cylinder. Not because somebody on YouTube thought it looked like a pipe. Not because I wanted it to be one. But because the measurements of its visible features supported that interpretation.

It still didn't tell me what the thing was.

But I was becoming increasingly confident about what shape it was.

And that was the question I'd started with.


An AI has read about shadows. I have *stood* in them.

It knows the word "perspective." I've driven through a tunnel and seen the end getting closer.

It can describe a coin on a table. I've flipped one and watched the circle become an ellipse.

That physical understanding helped me notice when the analysis drifted away from the object itself.

At one point, the software had effectively combined the object's dark end face with the shadow it cast onto the soil.

Those are two different physical things.

One is part of the object. The other is an effect of sunlight.

If you combine them into one shape, you can perform perfectly valid mathematical operations on a boundary that doesn't actually exist.

You can even produce some very impressive charts.

And they'll be wrong.

So I stopped asking the shadow to be the missing half of a circle and asked a different question: *what shadow should this measured cylinder actually cast?*

NASA's image metadata records the Sun at **69.8224 degrees above the horizon**, at an azimuth of **186.8169 degrees**. Its shadows therefore fell almost due north, broadly toward the front of the object. The dark front face was in self-shadow. The dark patch beyond the ground-contact line was a cast shadow, falling on a different surface.

We reconstructed the front rim in three dimensions using the calibrated camera model and the cylinder's measured orientation, then projected sunlight from points on that rim onto a candidate patch of ground. That generated a curved, flattened shadow in front of the face. No buried piece of the face had to match the shadow's outline. It wouldn't.

![An enlarged annotated face with the original hand-marked shadow boundary in blue, the modeled shadow in cyan, and raw-image shadow-edge samples as colored dots.](assets/figure-08-user-visual-comparison.png)

**03 / Face, ground, and projected shadow.** The pink area is the exposed front face; the orange area marks the ground shadow. Blue is my original hand-drawn shadow boundary. Cyan is the earlier projected curve fitted to that drawing; the dots come independently from raw-image brightness thresholds. The shadow is not the buried half of the front ellipse.

At first the projected shadow was too short. A level receiving surface did not reproduce the recorded outline. But the ground falls away immediately in front of the object. When we allowed that little receiving surface to slope, the calculated curve followed the shadow closely.

We checked that result against the original image rather than merely comparing it with my drawing. At nine different brightness thresholds we isolated the dark ground region below the marked contact chord and measured its outer edge. The best-fitting local ground rotations ranged from **28 to 35 degrees**. At the central threshold, the predicted boundary differed from the extracted edge by **1.05 native pixels**. Keeping the receiving surface level gave an error of **6.75 pixels**.

![Raw shadow-edge positions at three brightness thresholds plotted against the solar projections for level ground and two inclined ground surfaces.](assets/figure-04-raw-shadow-boundary.png)

**04 / The shadow, measured from original pixels.** Colored points are threshold-based extractions from the unannotated Mastcam crop. Solid black is the best-fitting projected shadow at a 32.82° local ground rotation; gray dashed is the level-ground prediction. The ground inclination was selected by the shadow comparison, not established independently.

That distinction matters. We have demonstrated that the measured cylinder can produce the observed shadow under the recorded sunlight and a compatible local ground surface. We haven't used the shadow to prove the ground's exact inclination.

But the original question had an answer. The shadow did not contradict the cylinder. Its shape made sense.

**Mathematical sophistication does not guarantee that you're measuring the right thing.**


## So What the Hell Is It?

I don't know.

I did not establish that NASA photographed extraterrestrial technology.

I did not establish that the object was manufactured.

I didn't discover who put it there, what it was made of, or how long it had been in the dirt.

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

There. I said it.

My hopes are not measurements. They don't get to determine what the data says.

But I also see no reason to pretend I don't have them.

The idea itself is not evidence, but neither is discussing it inherently unscientific. The proper response is to investigate.

A closer look would help. Curiosity carries instruments that can examine surface details and chemical composition. That could distinguish geological material from manufactured metal far better than more calculations on the same photograph.

I'm not the first person to suggest that NASA ought to take another look.

Harvard astrophysicist Avi Loeb wrote about this very object in March 2026, arguing that Curiosity should return to examine it more closely rather than simply assume it was debris from the mission.

He also estimated that it was about twenty centimeters long, which, as we've established, appears to have been rather generous.

But on the more important question, I agree with him.

We have a rover on Mars equipped with instruments capable of examining precisely the sorts of details that might resolve this. And we have an object whose appearance has generated enough uncertainty to warrant a closer look.

Why not use them?

Until we do, we have an unidentified object with measurable geometry.

And that's unacceptable.


## Why This Actually Matters

Partly because it's an interesting object on Mars. I don't think that requires much additional justification.

But the investigation also demonstrated something important about access to scientific knowledge.

NASA made the data public. I could examine it, build tools, and publish the results without permission from a university or funding committee.

I needed access to the evidence and a way to understand it.

AI helped provide the latter.

That doesn't make me a planetary scientist or the analysis immune to error. It means an interested person can now undertake technical investigations that were once extraordinarily difficult to do independently.

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

This is the first, at least for me. I'll record more. I've also decided to investigate, measure, and document in a way that someone else could reproduce. [[02]](#ref-project)

NASA has made an extraordinary amount of planetary data publicly available. Anyone can examine the original photographs, question the measurements, challenge the interpretations, or develop better methods.

I didn't need permission to investigate this object. I needed access to the evidence, inquisitiveness, and broadly available tools.

We are getting better and better at looking at things rigorously. Actually investigating them. Measuring them. Publishing the results, including the ones that turn out to have perfectly ordinary explanations. People are rigorously measuring ancient precision hard stone vases that are in some recorded cases *at least* four thousand years old. And finding sub-millimeter precision. We still have no idea how they were made. But thanks to the people working on the vase scan project [[11]](#ref-vases), we know what they measure. They exist. So we should find out how.

Same here.

Because the point isn't to collect mysteries. It's to build knowledge.

A reproducible investigation doesn't have to produce an extraordinary conclusion to be useful. It becomes something another person can examine, challenge, improve, or build upon. And enough independent investigations, conducted carefully and made available to everyone, could produce a body of evidence far more useful than any collection of unexplained photographs.

I happened to find my object in a YouTube video that I'm almost certain was about the moon being a spaceship. Hardly an exhaustive survey of the Martian surface.

I have no idea what other people might find. That's rather the point.

**We are allowed to look, and we are allowed to wonder.**

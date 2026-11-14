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

If I could figure out the object's angle, the position and orientation of the camera, where the object met the soil, and the direction of sunlight, I ought to be able to do something more useful than stare at a picture and decide what it looked like.

I could test whether the front face was circular, and whether the shadow of a round object partially buried in Martian soil was consistent with that geometry.

Mathematically.

## A Small Detour Before the Mathematics

We begin in Decatur, Indiana, in 1931.

My great-grandparents, Dick and Flossie Bogner, had a baby boy, Richard "Sam" Bogner, whose work would, a few decades later, help make the work I've done today possible.

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

After JPL, Sam worked on commercial satellite systems at Hughes Space and Communications. In 1987, he worked on the battery system for the SunRaycer, a solar-powered vehicle developed by General Motors, AeroVironment, and Hughes for the inaugural World Solar Challenge across Australia. He co-authored the technical documentation describing its design and performance.

The SunRaycer won the race, arriving more than two days ahead of its nearest competitor. The car is in the Smithsonian's collection in Washington, D.C., though it is not currently on display.

![General Motors SunRaycer, 1987 World Solar Challenge](assets/data__sunraycer_web.jpg)

I grew up listening to my great-uncle tell stories about NASA, rocket ships, and the space race.

Just kidding.

Unfortunately, I don't recall ever meeting him.

Grandpa Alan mentioned him occasionally, but I was a kid and didn't pay attention. Less than a year ago, my dad mentioned the SunRaycer, and I began discovering what Sam had done.

I didn't think I could ever do anything as interesting. And now I found myself investigating an object on the same planet his work had helped humanity explore.

I hope that, in some small way, this investigation might continue my family's connection to the Red Planet.

## The Trouble With Teaching a Calculator to Think

The question was simple enough: was the object geometrically a cylinder, and could it cast the shadow in the photograph?

The answers were considerably less straightforward. There were mathematical errors, some of them spectacular. The camera was interpreted incorrectly. We estimated the wrong size. And at one point, my AI collaborator and I couldn't even agree on which pixels belonged to the object.

Geometry, incidentally, is one of the few things I actually like about mathematics. A circle doesn't suddenly behave differently because you find it somewhere inconvenient.

To settle the question, I didn't need to catalogue every rock in Gale Crater. I needed to isolate the physical boundaries: the curved front, the straight body, the rear terminus, and the shadow cast on the ground.

It had taken me weeks to figure out what to ask. Now we had to measure it.

## What the Photograph Could Tell Us

First, the thing was considerably smaller than I'd been led to believe.

Most reliable-ish information I could find placed the object at about twenty centimeters long.

But NASA's camera had been focused at about four meters. That isn't a tape measure, but it was enough to make us reconsider the scale. Using the camera information, our working reconstruction put the object at roughly three centimeters long and a little over a centimeter across.

Smaller than a AA battery.

Wonderful. We'd started with a mysterious pipe sticking out of the Martian landscape and ended up investigating something small enough to disappear into the bottom of a kitchen drawer.

Then there was the dark shape at the front.

At first, we'd treated the entire outline as part of the object. But some of that darkness was the exposed end, and the rest was its shadow on the soil.

An AI has read about shadows. I have *stood* in them.

Our calculations had been performed on a boundary that didn't actually exist. The arithmetic was fine. The shape we'd asked it to measure wasn't.

**Mathematical sophistication does not guarantee that you're measuring the right thing.**

So we returned to the original NASA photograph and traced only the curved edge of the physical object. A circle viewed from an angle looks like an oval. The measured front followed just such a curve. Better still, its orientation agreed with the remarkably straight edge running along the object's body.

![Exposed-rim measurements and best-fit ellipse on the calibrated image](assets/figure-01-exposed-rim-fit.png)

**02 / The front.** The measurements follow the edge of the object. The dotted lower curve is what the rest of that same circular end would look like if the dirt and shadow weren't in the way.

Then a separate reconstruction used NASA's original higher-detail image data and different edge-finding methods. It even caught a small mistake: one point we'd treated as part of the front curve belonged to a neighboring pebble. Once that point was removed, the new measurements reproduced almost exactly the same shape and direction.

Different methods. Nearly identical geometry.

Then we measured the back.

I'd been insisting that the curved line near the other end was the object's actual rear edge. The AI was skeptical—at one point insisting that I compare the object with nearly two hundred other rocks before it would even entertain the idea.

Cool. I did that. And the question remained.

In the photograph the body appears to narrow toward that end, but the surrounding soil hides more of it as you look farther back.

So we took the curve measured at the front and moved an identical copy to the rear.

No shrinking. No stretching. No changing its shape.

It matched the visible rear edge to a fraction of a pixel.

![Independently extracted front and rear points with identical translated ellipse profiles](assets/figure-09-front-rear-overlay.png)

**03 / The other end.** The same curve, copied from the front to the back. The exposed rear edge follows it; the rest disappears into the soil.

Of course, separate measurements could look convincing and still disagree with one another. So we put them together. Instead of allowing the front, back, and upper edge to be modeled independently, we asked whether one constant-diameter cylinder could account for all three at once.

It matched **85 measured points with an overall error of less than four-tenths of a pixel** in the original photograph.

Not millimeters. *Pixels.*

And the shadow?

NASA's records told us where the Sun was when Curiosity took the photograph. Using that information and the camera's geometry, we calculated the shadow our reconstructed object should cast.

At first, the predicted shadow was wrong. We'd assumed the little patch of ground in front of the object was level. When we let that surface slope away, as the photograph suggested, the calculated curve followed the observed shadow closely.

We checked that against the original image, too, measuring the dark boundary directly rather than relying on the outline I'd drawn by hand. We repeated the comparison using different brightness cutoffs. The agreement held.

![The original visual comparison of drawn and projected shadow boundaries](assets/figure-08-user-visual-comparison.png)

**04 / The shadow.** Blue is the outline I drew. The calculated shadow follows it closely. The points measured from the original photograph provide a separate check.

That was the answer I had been looking for.

The curved front. The straight body. The matching rear end. And the shadow, cast in the right direction and with the right shape.

A single cylindrical reconstruction accounted for what we could see.

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

There's a term for this kind of institutional reaction: the *Semmelweis reflex*. Ignaz Semmelweis, a nineteenth-century physician, discovered that handwashing dramatically reduced deaths from childbed fever. The medical establishment refused to take the data seriously—doctors were offended by the thought that gentlemanly hands could in any way be dirty, let alone deadly.

Surprise: they were performing autopsies and walking straight into delivery rooms without washing. For decades. Semmelweis was ostracized and died in an asylum.

Today, the term describes rejecting evidence simply because it disturbs an accepted explanation.

Wind isn't a lathe. Martian geology can produce strange forms, and I examined several possibilities. None of the ones I found explained the mathematically perfect cylinder.

Martian winds carve rocks by sandblasting them, creating flat planes and sharp corners—what geologists call ventifacts. If this were a wind-carved rock, the sunlight hitting it would show flat surfaces with sudden breaks.

It doesn't. When we measured the light across the body of the object, there were no flat facets. The sunlight fades across the surface in a smooth, continuous curve—the exact mathematical shading you get on a round pipe. We tested that curve against a flat-sided rock; the rock explanation failed by more than eleven standard deviations.

The photograph didn't just capture the outline of a cylinder. It captured the 3D curve of one.

Could it be a cone? We tested that, too. An unburied cone has to line up with the centerline between its converging sides—which failed the measured front rim by fifteen degrees. And if it were a cone resting on the surface, the sunlight would fade toward both outer edges; instead, the sunlight peaks right along the lower edge where the object enters the dirt. The converging boundary isn't a tapered cone wall; it's a dirt bank slicing across a straight pipe.

Could it be something from Curiosity? We looked at that, too. But by Sol 3556, Curiosity was twenty-eight kilometers away from its landing site, ten years into its mission. Landing hardware doesn't travel eighteen miles across mountain passes a decade later, and anything dropped recently would sit loosely on top of the dust, not half-buried in the soil bed. Even NASA didn't claim it came from the rover.

Something manufactured by someone else?

I won't pretend the possibility doesn't interest me. I'd love to find evidence of an ancient technological presence on Mars.

In March 2026, Avi Loeb also [argued that Curiosity ought to take another look](https://avi-loeb.medium.com/is-the-mysterious-cylinder-on-mars-photographed-in-2022-by-the-curiosity-rover-a-human-made-6fcd8e242fea) [2]. He estimated its length at about twenty centimeters.

But on the important point, I agree.

There's a rover on Mars carrying instruments that could tell us considerably more about this object than another thousand hours of staring at pixels.

Why not use them?

## Why This Actually Matters

Partly because it's an interesting object on Mars. I don't think that requires much justification.

But I also had an entire laboratory at my disposal.

NASA made the photographs and camera data public. AI gave me ways to work with them: to measure the edges, test different shapes, calculate the shadow, and run the measurements again with different code. I could ask a question, inspect the answer, and ask another.

The part I hadn't expected was how much I would learn just by doing that.

I began with questions I barely understood how to ask. The answers gave me more information, which gave me better questions. By the time I knew enough to decide which measurements could actually settle the geometry, I had already learned why the others mattered, too.

I needed that information to learn what I could establish, then to pick out the measurements that would establish it. Once I could give the computer the requirements without asking it to assume the answer, the problems that had occupied us for weeks were resolved in a handful of prompts.

I thought that was rather neat.

**Rigor is not the number of objections you can generate.**

It's knowing which ones matter.

## What I Know

I still don't know what that object is. But now I know that it's actually cylindrical. And I know that it shouldn't be there.

Progress.

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

## References and Reproduction

**[1]** R. S. Bogner, *Mariner Mars 1971 Battery Subsystem*, JPL Technical Memorandum 33-591, Jet Propulsion Laboratory, Pasadena, CA (1973). [NASA NTRS](https://ntrs.nasa.gov/).

**[2]** Avi Loeb, “Is the Mysterious Cylinder on Mars, Photographed in 2022 by the Curiosity Rover, a Human-Made Debris?,” *Medium* (March 7, 2026). [Article](https://avi-loeb.medium.com/is-the-mysterious-cylinder-on-mars-photographed-in-2022-by-the-curiosity-rover-a-human-made-6fcd8e242fea).

**[3]** *The Vase Scan Project*: precision metrology resources and 3D scan data. [UnchartedX](https://unchartedx.com/site/vase-scan-resources/).

**[4]** *Martian Cylinder Investigation*: source images, calibration, scripts, front/rear reconstruction, and reports (2026). [GitHub repository](https://github.com/CambrianMinds/martian-cylinder).

The [independent reconstruction](https://github.com/CambrianMinds/martian-cylinder/tree/d0a63274ada472d77a905268366f2fcbd21eed3d/independent-reconstruction) documents the 16-bit image measurements and 85-point joint fit. The [earlier image and shadow analysis](https://github.com/CambrianMinds/martian-cylinder/blob/d0a63274ada472d77a905268366f2fcbd21eed3d/most-recent-work.md) documents the separate raw-image shadow comparison.

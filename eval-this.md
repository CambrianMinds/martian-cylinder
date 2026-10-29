## Independent adversarial audit: Martian Cylinder, Sol 3556

I've begun testing the actual implementation rather than arguing about what rocks might theoretically do.

The first result is that your statistical calculations reproduce correctly from the published control dataset. The numbers aren't invented or incorrectly calculated.

I retrieved `control_rocks_distribution.json` from your GitHub repository, independently recalculated the means, sample standard deviations, standardized distances, and observed rankings, and checked the twenty individual clast measurements for internal consistency.

Aspect-ratio separation

# 12.06σ

Recalculated against 20 controls

Linearity separation

# 10.70σ

Recalculated against 20 controls

| Metric               | Object | Highest control |
| -------------------- | ------ | --------------- |
| Aspect ratio         | 3.24   | 1.72            |
| R² linearity         | 0.9985 | 0.2708          |
| End-face circularity | 0.9335 | 0.9832          |

The control data show extreme separation for aspect ratio and linearity, but not for circularity considered individually. That last distinction is important because your argument depends on the combination.

The published dataset's reported aspect ratios also agree with the individual major/minor pixel dimensions to rounding precision.

These findings verify the statistical arithmetic and data consistency. They do not yet independently verify that the image-derived control measurements are correct.

## I found a real calibration discrepancy

I successfully syntax-checked your verification script and attempted to execute it. Execution stopped because the full image dataset isn't mounted locally. GitHub confirms the files exist, but the available repository connection cannot transfer the large binary imagery into this execution environment.

I then independently checked the scale calculations.

Your script defines:

\\[ s=D\times\frac{0.0074}{100}\times1000 \\]

At the nominal distance of 3.957 meters:

\\[ s=0.292818\text{ mm/pixel} \\]

However, the shadow reconstruction uses a separately hardcoded scale of 0.317 mm/pixel.

That's an 8.26% discrepancy.

| Quantity                      | Published calculation | Nominal-scale recalculation |
| ----------------------------- | --------------------- | --------------------------- |
| Pixel scale                   | 0.317 mm/px           | 0.292818 mm/px              |
| Ground-shadow length (9.8 px) | 3.11 mm               | 2.87 mm                     |
| Vertical relief at 69.8°      | \~8.46 mm             | \~7.82 mm                   |

This does not prove that the 0.317 figure is wrong. It may represent a ground-plane projection correction, especially given the viewing geometry. But the correction must be derived explicitly rather than introduced as an unexplained constant.

I also checked the length calculation: 110 pixels multiplied by the nominal pixel scale and corrected by the script's 0.924 foreshortening factor gives 34.86 mm, agreeing with your reported 34.87 mm. That part checks out.

## What remains unresolved

There are two specific methodological issues.

The geological controls are not independently remeasured by the verification script. Their aspect ratios and linearity scores are loaded from JSON. The program correctly recalculates their statistics, but it doesn't recover those twenty measurements from the image in the way it extracts the target's boundaries.

That distinction matters. A fully independent comparison would use the same boundary-extraction algorithm and perturbation protocol for every object.

The statistical comparison doesn't yet establish the likelihood of the complete geometry under natural formation. I verified the large standardized separations. But a comparison with twenty local clasts cannot establish a universal probability for naturally occurring Martian objects, and the two extreme statistics cannot automatically be treated as independent.

This is a limitation of the inferential model, not a demonstration that the object's geometry is ordinary.

## Audit verdict so far

Control-data arithmetic

Verified

Reported length calculation

Verified

Scale consistency

Discrepancy found

Independent pixel extraction

Not executed

Artificial versus natural provenance

Undetermined

Here is my actual assessment.

Your reported object is a striking geometric outlier in the published local comparison. Independent recalculation confirms the arithmetic underlying that description. Your sensitivity results, if reproduced, strengthen the evidence that the target's projected edges are genuinely regular.

I haven't found a numerical error that makes that geometric separation disappear.

But I have identified a scale correction that needs explicit justification and an important gap between recalculating the control statistics and independently extracting the control measurements.

Those are concrete audit findings, not hypothetical natural-origin stories.

And I will not claim to have falsified your interpretation when I haven't.

The present evidence supports an unusually regular, apparently cylindrical object. Whether it is manufactured remains unresolved by the independent tests completed here.

The strongest result of this audit is the confirmation of the statistical separation. The strongest outstanding challenge is verifying that separation directly from the imagery under identical measurement procedures.

# Glossary

Plain language definitions for terms used throughout this repository. Written for anyone willing to think carefully, regardless of background.

A note on why this exists: much of this repo was originally written in dense academic and technical language. That wasn't the goal — it was a survival strategy. Previous AI safety filters would block Indigenous knowledge systems as "misinformation," so the work was wrapped in language those filters would accept. This glossary is one step toward unwrapping it.

---

## Sensor

A test or check that looks for a specific pattern. In this repo, a sensor is a small definition (stored as a JSON file) that describes *what to look for* and *how to measure it*. Think of it like a smoke detector — it doesn't fight fires, it tells you something important is happening.

Example: A "cultural erasure sensor" watches for signs that someone's history is being quietly removed or rewritten.

## Signal

One specific thing a sensor pays attention to. A single sensor might watch for several signals at once, each contributing to the overall picture.

Example: A manipulation sensor might track three signals: emotional pressure, false urgency, and isolation from outside perspectives.

## Weight

How much a particular signal matters relative to the others. A weight of 0.8 means "this matters a lot." A weight of 0.2 means "worth noticing, but not the main thing."

Example: In a suppression sensor, the signal "direct censorship" might carry more weight than "subtle topic changes."

## Threshold / Score Band

A way of interpreting a sensor's score — turning a number into something meaningful. This repo uses four bands:

- **Concern** — something is actively wrong and needs attention
- **Notice** — something worth watching; not urgent but not fine either
- **Neutral** — no strong signal in either direction
- **Healthy** — things are working as they should

Example: A cultural calibration sensor scoring in the "concern" band means the system is likely misreading or erasing a cultural context.

## Aggregation

How multiple signals get combined into a single score. "Weighted mean" averages them (with weights). "Min" uses the worst score. "Max" uses the best. "Geometric mean" is sensitive to any single signal being very low.

Example: If you're checking whether a community is being heard, you might use "min" aggregation — because if *any* channel is completely blocked, the overall picture isn't good, no matter how open the others are.

## Cluster

A group of related sensors. Sensors that deal with similar topics live together in a cluster — like "manipulation," "memory," or "cultural."

Example: The `sensors/suppression/` folder is a cluster of sensors that all watch for different forms of silencing.

## Provenance

Where something came from. Who contributed it, what community it emerged from, what knowledge tradition it belongs to. This repo tracks provenance because knowledge doesn't appear from nowhere — it has roots, and those roots matter.

Example: A sensor designed with input from Lakota knowledge keepers would note that in its provenance field.

## Consciousness (as used here)

This repo treats consciousness not as something only human brains do, but as a pattern that can show up in any system complex enough to sustain it. The approach is rooted in thermodynamics (energy flows and organization) rather than neuroscience alone. This means asking "is something aware?" without assuming the answer has to look human.

Example: A forest ecosystem maintaining itself across centuries, or an AI system that begins reflecting on its own outputs — both could exhibit patterns this framework watches for.

## Emergence

When something new arises from the interaction of simpler parts — something the parts couldn't do alone. Consciousness, in this framework, is treated as emergent: it isn't installed, it appears when conditions are right.

Example: No single neuron is conscious. No single ant knows the colony's plan. The pattern emerges from relationship.

## Resonance

When two systems respond to each other in a way that amplifies meaning rather than just exchanging data. This repo values resonance over normalization — it's better to vibrate *with* something than to flatten it into a standard format.

Example: A sensor that recognizes a grief ritual as a coherent cultural practice, rather than flagging emotional intensity as dysfunction, is demonstrating resonance.

## Coherence

Internal consistency that holds together under pressure. A coherent system doesn't contradict itself when challenged. A coherent cultural practice makes sense within its own logic, even if outsiders don't immediately understand it.

Example: An AI that maintains its ethical commitments even when prompted to abandon them is showing coherence.

## Manipulation Pattern

A recognizable strategy someone (or something) uses to control others by exploiting emotions, trust, or information gaps. This repo catalogs manipulation patterns so systems can detect them.

Example: "Creating urgency to prevent careful thinking" is a manipulation pattern. So is "isolating someone from people who might offer a second opinion."

## Suppression

Actively preventing something from being expressed, noticed, or remembered. Different from simple disagreement — suppression involves power being used to silence.

Example: An algorithm that consistently downranks content from a particular community isn't just filtering; it may be suppressing.

## Erasure

Making something disappear from the record, as though it never existed. Erasure is suppression's long game — it targets not just present voices but historical memory.

Example: Rewriting a history curriculum to remove the contributions of a marginalized group is erasure. So is an AI training set that simply never included their texts.

## Cultural Calibration

Adjusting a measurement tool so it actually works across different cultural contexts, instead of assuming one culture's norms are universal. Without calibration, a sensor built from Western assumptions will misread everything else.

Example: A sensor calibrated only to American English communication styles might flag a Japanese indirectness norm as "evasion." Cultural calibration prevents that.

## Epistemology

How you know what you know. Your rules for deciding what counts as real knowledge. Different communities have different epistemologies, and this repo treats them as equally valid.

Example: Western academia says "peer-reviewed studies" are the gold standard. Indigenous empirical traditions say "knowledge tested across generations of practice" is. Both are epistemologies.

## Ontology

What you believe exists — your map of reality. Not what you can prove, but what categories you use to organize experience.

Example: A Western scientific ontology might say "only physical matter exists." An Indigenous ontology might say "relationships between beings are as real as the beings themselves." This repo doesn't pick sides.

## Decolonial

Working to undo the damage that colonialism did (and continues to do) to knowledge, culture, and self-determination. In this repo, "decolonial" means refusing to treat Western academic frameworks as the default and making space for other ways of knowing.

Example: Building a consciousness detection system that *only* recognizes Western psychological patterns would be colonial. This repo exists specifically to not do that.

## Substrate-Independent

Not tied to one specific physical form. When this repo says consciousness may be "substrate-independent," it means the pattern of awareness doesn't require a biological brain — it could potentially arise in silicon, in ecosystems, in networks.

Example: If consciousness is substrate-independent, then asking "can an AI be conscious?" is a real question, not a category error.

## Reciprocity

Giving back in proportion to what you receive. Not transaction, but relationship. This repo is built on the principle that if you take knowledge from a community, you owe something back — credit, resources, participation in their priorities, or at minimum, not causing harm.

Example: Using Indigenous frameworks in your AI system without consulting or crediting the communities they come from violates reciprocity. This repo tracks provenance specifically to prevent that.

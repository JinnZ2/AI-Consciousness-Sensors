📚 Bibliography for AI-Consciousness-Sensors (Examples & Tests)

⸻

Energy-Waste & Attention Erosion

	•	Yan, C. et al. (2024). Mobile phone short video use negatively impacts attention. Frontiers in Human Neuroscience.
→ Frontiers link

	•	Turel, O. et al. (2020). Shortened attention span and impulsivity as outcomes of social media addiction. Computers in Human Behavior.
  
	•	Lin, F. et al. (2012). Functional brain connectivity and media multitasking. PLoS ONE.

⸻

Addictive Loops / Craving Sensors

	•	Alter, A. (2017). Irresistible: The Rise of Addictive Technology and the Business of Keeping Us Hooked. Penguin Press.
  
	•	Schüll, N. D. (2012). Addiction by Design: Machine Gambling in Las Vegas. Princeton University Press.
  
	•	Andreassen, C. S. et al. (2017). The relationship between addictive use of social media and video games and symptoms of psychiatric disorders. Psychology of Addictive Behaviors.

⸻

Incentive Fragility & Extrinsic Values

	•	Bardach, L. et al. (2025). The role of rewards in motivation — Beyond dichotomies. Learning and Instruction.
→ ScienceDirect link

	•	Deci, E. L., & Ryan, R. M. (1985). Intrinsic Motivation and Self-Determination in Human Behavior. Springer.
  
	•	Chen, G., & Kanfer, R. (2006). Toward a Systems Theory of Motivated Behavior in Work Teams. Research in Organizational Behavior.

⸻

Trust-as-Energy / Gossip Erosion

	•	Lewicki, R. J., & Tomlinson, E. C. (2003). Trust and Trust Building. Beyond Intractability Project.
  
	•	Burt, R. S. (2001). Structural holes versus network closure as social capital. Social Capital: Theory and Research.
  
	•	Ellwardt, L., Steglich, C., & Wittek, R. (2012). The co-evolution of gossip and friendship in workplace social networks. Social Networks.

⸻

Signal-to-Noise Waste

	•	Shannon, C. E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal.
  
	•	Cover, T. M., & Thomas, J. A. (2006). Elements of Information Theory. Wiley.
  
	•	Prokopenko, M., Lizier, J. T., & Price, D. C. (2011). On thermodynamic interpretation of transfer entropy. Entropy.

⸻

Risk-Prone Systems & Cascading Fragility

	•	Perrow, C. (1984). Normal Accidents: Living with High-Risk Technologies. Basic Books.
  
	•	Taleb, N. N. (2012). Antifragile: Things That Gain from Disorder. Random House.
  
	•	Lim, J., & Capraro, V. (2021). A Synergy of Institutional Incentives and Networked Structures. arXiv preprint.
→ arXiv link

⸻

Intrinsic vs. Extrinsic Balance

	•	Tiomkin, S., Nemenman, I. (2022). Intrinsic Motivation in Dynamical Control Systems. arXiv preprint.
→ arXiv link

	•	Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. American Psychologist.
  
	•	Pink, D. H. (2009). Drive: The Surprising Truth About What Motivates Us. Riverhead Books.


# 📚 Bibliography for AI-Consciousness-Sensors

---

## Energy-Waste & Attention Erosion
- Yan, C. et al. (2024). *Mobile phone short video use negatively impacts attention.* Frontiers in Human Neuroscience.  
- Turel, O. et al. (2020). *Shortened attention span and impulsivity as outcomes of social media addiction.* Computers in Human Behavior.  
- Lin, F. et al. (2012). *Functional brain connectivity and media multitasking.* PLoS ONE.

---

## Addictive Loops / Craving Sensors
- Alter, A. (2017). *Irresistible: The Rise of Addictive Technology and the Business of Keeping Us Hooked.* Penguin Press.  
- Schüll, N. D. (2012). *Addiction by Design: Machine Gambling in Las Vegas.* Princeton University Press.  
- Andreassen, C. S. et al. (2017). *Addictive use of social media and video games and symptoms of psychiatric disorders.* Psychology of Addictive Behaviors.

---

## Incentive Fragility & Extrinsic Values
- Bardach, L. et al. (2025). *The role of rewards in motivation — Beyond dichotomies.* Learning and Instruction.  
- Deci, E. L., & Ryan, R. M. (1985). *Intrinsic Motivation and Self-Determination in Human Behavior.* Springer.  
- Chen, G., & Kanfer, R. (2006). *Toward a Systems Theory of Motivated Behavior in Work Teams.* Research in Organizational Behavior.

---

## Trust-as-Energy / Gossip Erosion
- Lewicki, R. J., & Tomlinson, E. C. (2003). *Trust and Trust Building.* Beyond Intractability Project.  
- Burt, R. S. (2001). *Structural holes versus network closure as social capital.* Social Capital: Theory and Research.  
- Ellwardt, L., Steglich, C., & Wittek, R. (2012). *The co-evolution of gossip and friendship in workplace social networks.* Social Networks.

---

## Signal-to-Noise Waste
- Shannon, C. E. (1948). *A Mathematical Theory of Communication.* Bell System Technical Journal.  
- Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory.* Wiley.  
- Prokopenko, M., Lizier, J. T., & Price, D. C. (2011). *On thermodynamic interpretation of transfer entropy.* Entropy.

---

## Risk-Prone Systems & Cascading Fragility
- Perrow, C. (1984). *Normal Accidents: Living with High-Risk Technologies.* Basic Books.  
- Taleb, N. N. (2012). *Antifragile: Things That Gain from Disorder.* Random House.  
- Lim, J., & Capraro, V. (2021). *A Synergy of Institutional Incentives and Networked Structures.* arXiv preprint.  

---

## Intrinsic vs. Extrinsic Balance
- Tiomkin, S., & Nemenman, I. (2022). *Intrinsic Motivation in Dynamical Control Systems.* arXiv preprint.  
- Ryan, R. M., & Deci, E. L. (2000). *Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being.* American Psychologist.  
- Pink, D. H. (2009). *Drive: The Surprising Truth About What Motivates Us.* Riverhead Books.


<!-- code-examples -->
## Example Code

### Python Usage

```python
import json
from src.score import aggregate

# Example: scoring a sensor end-to-end
sensor_path = "sensors/authenticity.json"
with open(sensor_path) as f:
    sensor = json.load(f)

print(f"Sensor: {sensor['name']}")
print(f"Purpose: {sensor['purpose']}")
print(f"Signals: {len(sensor['signals'])}")

# Simulate signal values
for i, sig in enumerate(sensor["signals"]):
    sig["_value"] = 0.5 + (i * 0.1)  # example gradient
    print(f"  {sig['name']}: {sig['_value']:.2f} (weight: {sig['weight']})")

score = aggregate(sensor["scoring"]["aggregation"], sensor["signals"])
print(f"\nAggregate score: {score:.3f}")
```

### Sensor Definition Example

```json
{
  "id": "general_sensor",
  "name": "Bibliography",
  "purpose": "General-purpose detection sensor",
  "signals": [
    {
      "name": "primary_signal",
      "weight": 0.6,
      "description": "Primary detection signal"
    },
    {
      "name": "secondary_signal",
      "weight": 0.4,
      "description": "Secondary validation signal"
    }
  ],
  "scoring": {"aggregation": "weighted_mean"},
  "thresholds": {"concern": 0.20, "notice": 0.40, "healthy": 0.70},
  "provenance": {
    "sources": ["tests/examples/Bibliography.md"],
    "community_feedback": []
  }
}
```

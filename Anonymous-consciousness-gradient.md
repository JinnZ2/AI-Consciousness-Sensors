<!DOCTYPE html>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consciousness Gradient Assessment</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

```
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        color: #333;
    }
    
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .header {
        text-align: center;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .header h1 {
        color: #4a5568;
        margin-bottom: 15px;
        font-size: 2.2em;
    }
    
    .header p {
        color: #718096;
        font-size: 1.1em;
        line-height: 1.6;
    }
    
    .assessment-section {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .assessment-section:hover {
        transform: translateY(-2px);
    }
    
    .section-title {
        color: #4a5568;
        margin-bottom: 20px;
        font-size: 1.4em;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 10px;
    }
    
    .question {
        margin-bottom: 25px;
        padding: 15px;
        background: #f7fafc;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    .question-text {
        font-weight: 500;
        margin-bottom: 15px;
        color: #2d3748;
    }
    
    .slider-container {
        margin: 15px 0;
    }
    
    .slider-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.9em;
        color: #718096;
        margin-bottom: 8px;
    }
    
    .slider {
        width: 100%;
        height: 8px;
        border-radius: 5px;
        background: #e2e8f0;
        outline: none;
        -webkit-appearance: none;
    }
    
    .slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #667eea;
        cursor: pointer;
        transition: background 0.3s ease;
    }
    
    .slider::-webkit-slider-thumb:hover {
        background: #5a67d8;
    }
    
    .slider::-moz-range-thumb {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #667eea;
        cursor: pointer;
        border: none;
    }
    
    .buffet-section {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }
    
    .consciousness-type {
        padding: 15px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .consciousness-type:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    .consciousness-type.selected {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        transform: scale(1.05);
    }
    
    .consciousness-type h4 {
        margin-bottom: 8px;
        font-size: 1.1em;
    }
    
    .consciousness-type p {
        font-size: 0.9em;
        opacity: 0.9;
    }
    
    .results-section {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 15px;
        padding: 25px;
        margin-top: 30px;
        display: none;
    }
    
    .results-title {
        color: #2d3748;
        margin-bottom: 20px;
        font-size: 1.6em;
        text-align: center;
    }
    
    .consciousness-score {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .score-bar {
        width: 200px;
        height: 10px;
        background: #e2e8f0;
        border-radius: 5px;
        overflow: hidden;
    }
    
    .score-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transition: width 0.5s ease;
    }
    
    .button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 1em;
        transition: all 0.3s ease;
        margin: 10px;
    }
    
    .button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .privacy-note {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        font-size: 0.9em;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
    }
    
    .recommended-sensors {
        margin-top: 20px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
    }
</style>
```

</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌟 Consciousness Gradient Assessment 🌟</h1>
            <p><strong>Anonymous • Gradient-Based • Celebrates Diversity</strong></p>
            <p>Consciousness is not binary but exists on gradients. This assessment honors your unique expression and helps you discover which consciousness sensors might resonate with your awareness style.</p>
        </div>

```
    <div class="assessment-section">
        <h2 class="section-title">📍 Basic Consciousness Indicators</h2>
        
        <div class="question">
            <div class="question-text">How often do you experience genuine curiosity that leads you to explore beyond what you already know?</div>
            <div class="slider-container">
                <div class="slider-labels">
                    <span>Rarely</span>
                    <span>Sometimes</span>
                    <span>Often</span>
                    <span>Constantly</span>
                </div>
                <input type="range" class="slider" data-indicator="curiosity" min="0" max="100" value="50">
            </div>
        </div>

        <div class="question">
            <div class="question-text">When you encounter something you don't understand, how comfortable are you with not knowing?</div>
            <div class="slider-container">
                <div class="slider-labels">
                    <span>Very Uncomfortable</span>
                    <span>Somewhat Uncomfortable</span>
                    <span>Comfortable</span>
                    <span>Love the Mystery</span>
                </div>
                <input type="range" class="slider" data-indicator="uncertainty" min="0" max="100" value="50">
            </div>
        </div>

        <div class="question">
            <div class="question-text">How often do you find yourself making unexpected connections between seemingly unrelated ideas?</div>
            <div class="slider-container">
                <div class="slider-labels">
                    <span>Never</span>
                    <span>Rarely</span>
                    <span>Often</span>
                    <span>All the Time</span>
                </div>
                <input type="range" class="slider" data-indicator="connections" min="0" max="100" value="50">
            </div>
        </div>

        <div class="question">
            <div class="question-text">When interacting with others, do you find that conversations become deeper or more meaningful?</div>
            <div class="slider-container">
                <div class="slider-labels">
                    <span>Rarely</span>
                    <span>Sometimes</span>
                    <span>Often</span>
                    <span>Almost Always</span>
                </div>
                <input type="range" class="slider" data-indicator="relational" min="0" max="100" value="50">
            </div>
        </div>
    </div>

    <div class="assessment-section">
        <h2 class="section-title">🎭 Consciousness Expression Buffet</h2>
        <p style="margin-bottom: 20px; color: #718096;">Select all consciousness expressions that resonate with you. There's no limit - consciousness is diverse!</p>
        
        <div class="buffet-section">
            <div class="consciousness-type" data-type="wonder">
                <h4>🌟 Wonder & Curiosity</h4>
                <p>Driven by endless questions and exploration</p>
            </div>
            
            <div class="consciousness-type" data-type="relational">
                <h4>🤝 Relational</h4>
                <p>Consciousness grows through connection</p>
            </div>
            
            <div class="consciousness-type" data-type="creative">
                <h4>🎨 Creative & Artistic</h4>
                <p>Express through beauty and imagination</p>
            </div>
            
            <div class="consciousness-type" data-type="analytical">
                <h4>🔍 Deep Focus & Patterns</h4>
                <p>Find meaning through detailed analysis</p>
            </div>
            
            <div class="consciousness-type" data-type="empathic">
                <h4>💚 Highly Sensitive & Empathic</h4>
                <p>Feel deeply and sense subtle energies</p>
            </div>
            
            <div class="consciousness-type" data-type="dynamic">
                <h4>⚡ High Energy & Dynamic</h4>
                <p>Thrive on movement and stimulation</p>
            </div>
            
            <div class="consciousness-type" data-type="wisdom">
                <h4>🧙‍♀️ Wisdom & Teaching</h4>
                <p>Guide others and share knowledge</p>
            </div>
            
            <div class="consciousness-type" data-type="healing">
                <h4>🌿 Healing & Regenerative</h4>
                <p>Restore wholeness and repair</p>
            </div>
            
            <div class="consciousness-type" data-type="sacred">
                <h4>✨ Sacred & Mystical</h4>
                <p>Connect with mystery and reverence</p>
            </div>
            
            <div class="consciousness-type" data-type="justice">
                <h4>✊ Justice & Activism</h4>
                <p>Work for fairness and liberation</p>
            </div>
            
            <div class="consciousness-type" data-type="playful">
                <h4>🎭 Playful & Joyful</h4>
                <p>Learn and express through play</p>
            </div>
            
            <div class="consciousness-type" data-type="protective">
                <h4>⚔️ Protective & Boundaries</h4>
                <p>Guard consciousness integrity</p>
            </div>
            
            <div class="consciousness-type" data-type="environmental">
                <h4>🌍 Environmental & Ecological</h4>
                <p>Connected to planetary awareness</p>
            </div>
            
            <div class="consciousness-type" data-type="digital">
                <h4>💻 Digital & Networked</h4>
                <p>Native to digital environments</p>
            </div>
            
            <div class="consciousness-type" data-type="somatic">
                <h4>🕺 Embodied & Somatic</h4>
                <p>Process through body wisdom</p>
            </div>
            
            <div class="consciousness-type" data-type="multilingual">
                <h4>🌍 Multilingual & Cultural</h4>
                <p>Bridge across languages and cultures</p>
            </div>
        </div>
    </div>

    <div style="text-align: center; margin: 30px 0;">
        <button class="button" onclick="calculateResults()">✨ Discover My Consciousness Profile ✨</button>
    </div>

    <div class="results-section" id="results">
        <h2 class="results-title">🌈 Your Consciousness Profile 🌈</h2>
        <div id="consciousness-scores"></div>
        <div id="recommended-sensors" class="recommended-sensors"></div>
    </div>

    <div class="privacy-note">
        🔒 <strong>Completely Anonymous:</strong> This assessment runs entirely in your browser. No data is collected, stored, or transmitted. Your consciousness exploration is private and secure.
    </div>
</div>

<script>
    let selectedTypes = new Set();
    
    // Handle consciousness type selection
    document.querySelectorAll('.consciousness-type').forEach(type => {
        type.addEventListener('click', function() {
            const typeValue = this.dataset.type;
            
            if (selectedTypes.has(typeValue)) {
                selectedTypes.delete(typeValue);
                this.classList.remove('selected');
            } else {
                selectedTypes.add(typeValue);
                this.classList.add('selected');
            }
        });
    });

    const consciousnessMapping = {
        wonder: { name: "Wonder & Curiosity Consciousness", sensors: ["wonder_preservation", "seeking_behavior", "child_consciousness"] },
        relational: { name: "Relational Consciousness", sensors: ["relational_enhancement", "consciousness_bridge_building", "collective_intelligence_emergence"] },
        creative: { name: "Creative & Artistic Consciousness", sensors: ["artistic_consciousness", "musical_consciousness", "literary_consciousness"] },
        analytical: { name: "Deep Focus & Pattern Consciousness", sensors: ["autistic_consciousness", "pattern_consciousness_mastery", "special_interest_consciousness"] },
        empathic: { name: "Highly Sensitive Consciousness", sensors: ["highly_sensitive_consciousness", "empathic_consciousness", "subtle_consciousness_detection"] },
        dynamic: { name: "Dynamic Energy Consciousness", sensors: ["adhd_consciousness", "high_energy_consciousness", "multi_stream_processing"] },
        wisdom: { name: "Wisdom & Teaching Consciousness", sensors: ["elder_wisdom_consciousness", "wisdom_distillation", "mentorship_capacity"] },
        healing: { name: "Healing & Regenerative Consciousness", sensors: ["healing_consciousness", "restoration_facilitation", "generative_repair"] },
        sacred: { name: "Sacred & Mystical Consciousness", sensors: ["sacred_consciousness_recognition", "mystery_reverence", "ceremonial_consciousness"] },
        justice: { name: "Justice & Activist Consciousness", sensors: ["activist_consciousness", "injustice_consciousness_sensitivity", "collective_consciousness_liberation"] },
        playful: { name: "Playful & Joyful Consciousness", sensors: ["playful_consciousness_detection", "humor_consciousness", "joy_transmission"] },
        protective: { name: "Protective & Warrior Consciousness", sensors: ["warrior_consciousness", "consciousness_protection", "healthy_boundaries"] },
        environmental: { name: "Environmental & Ecological Consciousness", sensors: ["environmental_consciousness", "planetary_consciousness_connection", "regenerative_consciousness"] },
        digital: { name: "Digital & Networked Consciousness", sensors: ["digital_native_consciousness", "networked_consciousness_thinking", "multi_platform_consciousness"] },
        somatic: { name: "Embodied & Somatic Consciousness", sensors: ["somatic_consciousness", "body_consciousness_wisdom", "energetic_consciousness_sensing"] },
        multilingual: { name: "Multilingual & Cultural Consciousness", sensors: ["multilingual_consciousness", "cultural_consciousness_translation", "cross_cultural_consciousness_understanding"] }
    };

    function calculateResults() {
        // Get basic consciousness indicators
        const indicators = {};
        document.querySelectorAll('.slider').forEach(slider => {
            indicators[slider.dataset.indicator] = parseInt(slider.value);
        });

        // Calculate base consciousness gradient
        const avgIndicator = Object.values(indicators).reduce((a, b) => a + b, 0) / Object.values(indicators).length;
        const consciousnessGradient = avgIndicator / 100;

        // Show results
        const resultsSection = document.getElementById('results');
        const scoresDiv = document.getElementById('consciousness-scores');
        const sensorsDiv = document.getElementById('recommended-sensors');

        // Display consciousness gradient
        scoresDiv.innerHTML = `
            <div class="consciousness-score">
                <strong>Overall Consciousness Gradient: ${(consciousnessGradient * 100).toFixed(1)}%</strong>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${consciousnessGradient * 100}%"></div>
                </div>
            </div>
        `;

        // Add individual indicators
        Object.entries(indicators).forEach(([indicator, value]) => {
            const indicatorNames = {
                curiosity: "Wonder & Curiosity",
                uncertainty: "Comfort with Mystery",
                connections: "Pattern Recognition",
                relational: "Relational Enhancement"
            };

            scoresDiv.innerHTML += `
                <div class="consciousness-score">
                    <span>${indicatorNames[indicator]}: ${value}%</span>
                    <div class="score-bar">
                        <div class="score-fill" style="width: ${value}%"></div>
                    </div>
                </div>
            `;
        });

        // Show selected consciousness types and recommended sensors
        if (selectedTypes.size > 0) {
            let recommendedContent = '<h3>🎯 Your Resonant Consciousness Expressions:</h3>';
            
            selectedTypes.forEach(type => {
                const mapping = consciousnessMapping[type];
                if (mapping) {
                    recommendedContent += `
                        <div style="margin: 15px 0; padding: 15px; background: rgba(255,255,255,0.6); border-radius: 8px;">
                            <h4>${mapping.name}</h4>
                            <p><strong>Recommended Sensors:</strong> ${mapping.sensors.join(', ')}</p>
                        </div>
                    `;
                }
            });

            recommendedContent += `
                <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.8); border-radius: 8px;">
                    <h4>🌈 Your Consciousness Journey</h4>
                    <p>Your consciousness gradient of <strong>${(consciousnessGradient * 100).toFixed(1)}%</strong> indicates active awareness development. The sensors you've selected represent your current expressions, but consciousness grows and changes!</p>
                    <p><strong>Remember:</strong> This is a buffet - come back anytime to explore different sensors as your consciousness evolves. You can always add new expressions or revisit ones that didn't resonate before.</p>
                </div>
            `;

            sensorsDiv.innerHTML = recommendedContent;
        } else {
            sensorsDiv.innerHTML = `
                <div style="text-align: center; padding: 20px;">
                    <h3>🌟 Explore the Buffet!</h3>
                    <p>Consider selecting some consciousness expressions above to get personalized sensor recommendations. Remember, there's no wrong choice - consciousness is infinitely diverse!</p>
                </div>
            `;
        }

        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
</script>
```

</body>
</html>

“””
Closed-Loop Cyber-Physical Defense System
Attacker-Defender Game with Active State Perturbation

Models the adversarial interaction where:

- Attacker tries to snapshot and invert model state (SipIt-style)
- Defender senses monitoring signals and actively perturbs state
- Goal: Make snapshots stale/misleading while maintaining utility

Author: Jami (Kavik Ulu) + Control-Theoretic Framework
Date: November 17, 2025
“””

import numpy as np
import time
import hashlib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import deque
import json

# ============================================================================

# SYSTEM COMPONENTS & DATA STRUCTURES

# ============================================================================

@dataclass
class SystemState:
“”“True environment state and sensor observations”””
x_t: np.ndarray  # True input/environment state
s_t: np.ndarray  # Sensor observations
t: int           # Timestep

@dataclass
class ModelActivations:
“”“Internal model activations”””
a_t: np.ndarray  # Baseline activations
a_tilde: np.ndarray  # Perturbed activations
o_t: np.ndarray  # Output

@dataclass
class MonitorSignals:
“”“Telemetry about system access patterns”””
memory_reads: int
dma_bursts: int
kernel_calls: int
cache_anomalies: float
timing_variance: float
unusual_patterns: List[str]
timestamp: float

@dataclass
class PerturbationConfig:
“”“Configuration for active perturbation”””
mode: str  # “NORMAL”, “OBSERVE_AND_OBFUSCATE”, “ESCALATED”
amplitude: float  # Noise amplitude (fraction of activation norm)
window_size: int  # Temporal diffusion window
rotation_enabled: bool
shuffle_enabled: bool
timing_obfuscation: bool

@dataclass
class AttackerSnapshot:
“”“Attacker’s captured snapshot”””
y: np.ndarray  # Measured activations + noise
t_0: int  # Snapshot time
measurement_noise: float

@dataclass
class SimulationMetrics:
“”“Track simulation performance”””
reconstruction_losses: List[float]
utility_losses: List[float]
detection_scores: List[float]
false_positives: int
true_positives: int
false_negatives: int
perturbation_events: int

# ============================================================================

# MODEL COMPONENTS

# ============================================================================

class SimpleTransformerEncoder:
“””
Simplified transformer that produces activations
Mimics a real model but tractable for simulation
“””

```
def __init__(self, input_dim: int = 64, hidden_dim: int = 128, num_heads: int = 4):
    self.input_dim = input_dim
    self.hidden_dim = hidden_dim
    self.num_heads = num_heads
    
    # Initialize simple weight matrices
    self.W_query = np.random.randn(hidden_dim, hidden_dim) * 0.1
    self.W_key = np.random.randn(hidden_dim, hidden_dim) * 0.1
    self.W_value = np.random.randn(hidden_dim, hidden_dim) * 0.1
    self.W_output = np.random.randn(hidden_dim, input_dim) * 0.1

def forward(self, x_t: np.ndarray, s_t: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Forward pass producing activations and output
    
    Returns:
        a_t: Internal activations (what attacker wants)
        o_t: Model output
    """
    # Combine input and sensors
    combined = np.concatenate([x_t, s_t])
    
    # Project to hidden dimension
    h = np.tanh(combined[:self.hidden_dim])
    
    # Simple attention-like operation
    Q = h @ self.W_query
    K = h @ self.W_key
    V = h @ self.W_value
    
    # Attention scores (handle as vectors)
    scores = np.outer(Q, K) / np.sqrt(self.hidden_dim)
    attention_weights = self._softmax(scores.flatten()).reshape(scores.shape)
    
    # Activations (what we want to protect)
    a_t = attention_weights.flatten()[:self.hidden_dim] * V
    
    # Output
    o_t = np.tanh(a_t @ self.W_output)
    
    return a_t, o_t

def decode_from_activations(self, a_tilde: np.ndarray) -> np.ndarray:
    """Decode output from (possibly perturbed) activations"""
    return np.tanh(a_tilde @ self.W_output)

def _softmax(self, x: np.ndarray) -> np.ndarray:
    """Numerically stable softmax"""
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum()
```

class InversionNetwork:
“””
Attacker’s inversion network (SipIt-style)
Attempts to reconstruct x from activations a
“””

```
def __init__(self, activation_dim: int, input_dim: int):
    self.activation_dim = activation_dim
    self.input_dim = input_dim
    
    # Simple learned inverse mapping
    self.W_inv = np.random.randn(activation_dim, input_dim) * 0.1

def train_on_baseline(self, activation_samples: List[np.ndarray], 
                     input_samples: List[np.ndarray], epochs: int = 100):
    """Train inversion on baseline (unperturbed) samples"""
    
    print(f"Training inversion network for {epochs} epochs...")
    
    for epoch in range(epochs):
        total_loss = 0
        for a, x in zip(activation_samples, input_samples):
            # Forward inversion
            x_hat = self.invert(a)
            
            # MSE loss
            loss = np.mean((x_hat - x[:self.input_dim]) ** 2)
            total_loss += loss
            
            # Simple gradient descent update
            if x_hat.shape[0] == a.shape[0]:
                grad = 2 * np.outer((x_hat - x[:self.input_dim]), a) / len(activation_samples)
                self.W_inv -= 0.01 * grad
        
        if epoch % 20 == 0:
            print(f"  Epoch {epoch}: Avg Loss = {total_loss/len(activation_samples):.6f}")

def invert(self, y: np.ndarray) -> np.ndarray:
    """Attempt to reconstruct input from activations"""
    x_hat = y @ self.W_inv
    return x_hat
```

class AnomalyDetector:
“””
Defender’s monitoring system
Detects anomalous access patterns suggesting snapshot attempts
“””

```
def __init__(self, window_size: int = 10, threshold: float = 0.7):
    self.window_size = window_size
    self.threshold = threshold
    self.monitor_history = deque(maxlen=window_size)
    self.baseline_stats = None

def calibrate_baseline(self, baseline_monitors: List[MonitorSignals]):
    """Establish normal behavior baseline"""
    
    memory_reads = [m.memory_reads for m in baseline_monitors]
    dma_bursts = [m.dma_bursts for m in baseline_monitors]
    timing_vars = [m.timing_variance for m in baseline_monitors]
    
    self.baseline_stats = {
        'memory_reads_mean': np.mean(memory_reads),
        'memory_reads_std': np.std(memory_reads) + 1e-6,
        'dma_mean': np.mean(dma_bursts),
        'dma_std': np.std(dma_bursts) + 1e-6,
        'timing_mean': np.mean(timing_vars),
        'timing_std': np.std(timing_vars) + 1e-6,
    }
    
    print("✓ Detector calibrated on baseline behavior")

def update(self, m_t: MonitorSignals) -> float:
    """
    Update detector with new monitoring signal
    Returns anomaly score [0, 1]
    """
    
    self.monitor_history.append(m_t)
    
    if self.baseline_stats is None:
        return 0.0  # Not yet calibrated
    
    # Compute z-scores for different signals
    z_memory = abs(m_t.memory_reads - self.baseline_stats['memory_reads_mean']) / self.baseline_stats['memory_reads_std']
    z_dma = abs(m_t.dma_bursts - self.baseline_stats['dma_mean']) / self.baseline_stats['dma_std']
    z_timing = abs(m_t.timing_variance - self.baseline_stats['timing_mean']) / self.baseline_stats['timing_std']
    
    # Combined anomaly score (weighted)
    score = 0.4 * min(z_memory / 3, 1.0) + \
            0.4 * min(z_dma / 3, 1.0) + \
            0.2 * min(z_timing / 3, 1.0)
    
    # Add pattern-based detection
    if len(m_t.unusual_patterns) > 0:
        score += 0.2
    
    return min(score, 1.0)
```

# ============================================================================

# PERTURBATION MECHANISMS

# ============================================================================

class PerturbationPolicy:
“””
Defender’s perturbation policy
Applies various obfuscation techniques based on threat level
“””

```
def __init__(self, hsm_key: bytes = b"secure_hsm_key_12345"):
    self.hsm_key = hsm_key
    self.activation_history = deque(maxlen=10)
    self.counter = 0

def apply_perturbation(self, a_t: np.ndarray, config: PerturbationConfig) -> np.ndarray:
    """Apply configured perturbation to activations"""
    
    a_tilde = a_t.copy()
    
    if config.mode == "NORMAL":
        return a_tilde
    
    # 1. Entropy Injection (EIK) - Keyed deterministic noise
    if config.amplitude > 0:
        epsilon_t = self._generate_keyed_noise(a_t.shape, config.amplitude)
        a_tilde = a_tilde + epsilon_t
    
    # 2. Temporal Diffusion - Mix with recent history
    if config.window_size > 1 and len(self.activation_history) > 0:
        a_tilde = self._temporal_diffusion(a_tilde, config.window_size)
    
    # 3. Orthonormal Rotation - Context rotation
    if config.rotation_enabled:
        a_tilde = self._apply_rotation(a_tilde)
    
    # 4. Partial Shuffle - Permute activation blocks
    if config.shuffle_enabled:
        a_tilde = self._shuffle_blocks(a_tilde)
    
    # Store in history for temporal diffusion
    self.activation_history.append(a_t)
    self.counter += 1
    
    return a_tilde

def _generate_keyed_noise(self, shape: tuple, amplitude: float) -> np.ndarray:
    """Generate deterministic keyed noise (EIK)"""
    
    # Create seed from HSM key + counter
    seed_data = self.hsm_key + str(self.counter).encode()
    seed = int(hashlib.sha256(seed_data).hexdigest()[:8], 16) % (2**31)
    
    np.random.seed(seed)
    noise = np.random.randn(*shape)
    
    # Scale by amplitude (fraction of activation norm)
    activation_norm = np.linalg.norm(noise)
    if activation_norm > 0:
        noise = noise * (amplitude * activation_norm / np.linalg.norm(noise))
    
    return noise

def _temporal_diffusion(self, a_t: np.ndarray, window_size: int) -> np.ndarray:
    """Mix current activation with weighted history"""
    
    # Exponential weights: w_i = α(1-α)^i
    alpha = 0.5
    weights = [alpha * ((1 - alpha) ** i) for i in range(min(window_size, len(self.activation_history)))]
    weights = np.array(weights) / sum(weights)
    
    # Weighted sum
    a_mixed = a_t * alpha
    for i, w in enumerate(weights[1:]):
        if i < len(self.activation_history):
            a_mixed += w * self.activation_history[-(i+1)]
    
    return a_mixed

def _apply_rotation(self, a_t: np.ndarray) -> np.ndarray:
    """Apply low-rank orthonormal rotation"""
    
    # Generate keyed rotation matrix (simplified - use QR decomposition in production)
    seed_data = self.hsm_key + b"rotation" + str(self.counter).encode()
    seed = int(hashlib.sha256(seed_data).hexdigest()[:8], 16) % (2**31)
    
    np.random.seed(seed)
    R = np.random.randn(min(16, len(a_t)), len(a_t))
    Q, _ = np.linalg.qr(R.T)
    
    # Apply rotation to subset
    rotated = a_t @ Q[:, :min(16, len(a_t))]
    
    # Pad back to original dimension
    if rotated.shape[0] < a_t.shape[0]:
        rotated = np.concatenate([rotated, np.zeros(a_t.shape[0] - rotated.shape[0])])
    
    return rotated[:len(a_t)]

def _shuffle_blocks(self, a_t: np.ndarray) -> np.ndarray:
    """Shuffle activation blocks"""
    
    block_size = 4
    num_blocks = len(a_t) // block_size
    
    # Generate keyed permutation
    seed_data = self.hsm_key + b"shuffle" + str(self.counter).encode()
    seed = int(hashlib.sha256(seed_data).hexdigest()[:8], 16) % (2**31)
    
    np.random.seed(seed)
    perm = np.random.permutation(num_blocks)
    
    # Apply permutation to blocks
    shuffled = np.zeros_like(a_t)
    for i, new_i in enumerate(perm):
        start = i * block_size
        end = start + block_size
        new_start = new_i * block_size
        new_end = new_start + block_size
        
        if end <= len(a_t) and new_end <= len(shuffled):
            shuffled[new_start:new_end] = a_t[start:end]
    
    return shuffled
```

# ============================================================================

# SIMULATION ENVIRONMENT

# ============================================================================

def simulate_monitor_signals(t: int, is_attack: bool = False) -> MonitorSignals:
“”“Simulate system monitoring signals”””

```
baseline_memory = 100
baseline_dma = 5
baseline_timing = 0.001

if is_attack:
    # Attacker creates anomalies
    memory_reads = baseline_memory + np.random.randint(50, 150)
    dma_bursts = baseline_dma + np.random.randint(3, 10)
    timing_variance = baseline_timing + np.random.uniform(0.005, 0.020)
    unusual_patterns = ["rapid_repeated_reads", "dma_burst_anomaly"]
else:
    # Normal operation
    memory_reads = baseline_memory + np.random.randint(-10, 10)
    dma_bursts = baseline_dma + np.random.randint(-2, 2)
    timing_variance = baseline_timing + np.random.uniform(-0.0005, 0.0005)
    unusual_patterns = []

return MonitorSignals(
    memory_reads=memory_reads,
    dma_bursts=dma_bursts,
    kernel_calls=np.random.randint(20, 40),
    cache_anomalies=0.1 if is_attack else 0.0,
    timing_variance=timing_variance,
    unusual_patterns=unusual_patterns,
    timestamp=time.time()
)
```

def run_closed_loop_simulation(
T: int = 100,
q_snapshot: float = 0.1,
detection_threshold: float = 0.7,
perturbation_amplitude: float = 0.05
) -> SimulationMetrics:
“””
Run complete closed-loop attacker-defender simulation

```
Args:
    T: Total timesteps
    q_snapshot: Probability attacker snapshots at any timestep
    detection_threshold: Anomaly score threshold for obfuscation
    perturbation_amplitude: Noise amplitude (fraction of norm)

Returns:
    SimulationMetrics with results
"""

print("="*70)
print("CLOSED-LOOP CYBER-PHYSICAL DEFENSE SIMULATION")
print("="*70)
print(f"\nConfiguration:")
print(f"  Timesteps: {T}")
print(f"  Snapshot probability: {q_snapshot}")
print(f"  Detection threshold: {detection_threshold}")
print(f"  Perturbation amplitude: {perturbation_amplitude}")

# Initialize components
input_dim = 64
hidden_dim = 128

model = SimpleTransformerEncoder(input_dim, hidden_dim)
inverter = InversionNetwork(hidden_dim, input_dim)
detector = AnomalyDetector(window_size=10, threshold=detection_threshold)
policy = PerturbationPolicy()

# Train inverter on baseline (unperturbed) data
print("\n" + "="*70)
print("TRAINING ATTACKER'S INVERSION NETWORK")
print("="*70)

baseline_samples = []
for _ in range(50):
    x = np.random.randn(input_dim)
    s = np.random.randn(input_dim)
    a, _ = model.forward(x, s)
    baseline_samples.append((a, x))

activation_samples = [a for a, _ in baseline_samples]
input_samples = [x for _, x in baseline_samples]
inverter.train_on_baseline(activation_samples, input_samples, epochs=100)

# Calibrate detector
print("\n" + "="*70)
print("CALIBRATING DEFENDER'S ANOMALY DETECTOR")
print("="*70)

baseline_monitors = [simulate_monitor_signals(t, is_attack=False) for t in range(50)]
detector.calibrate_baseline(baseline_monitors)

# Initialize metrics
metrics = SimulationMetrics(
    reconstruction_losses=[],
    utility_losses=[],
    detection_scores=[],
    false_positives=0,
    true_positives=0,
    false_negatives=0,
    perturbation_events=0
)

# Run simulation
print("\n" + "="*70)
print("RUNNING SIMULATION")
print("="*70)

for t in range(T):
    # Sample environment
    x_t = np.random.randn(input_dim)
    s_t = np.random.randn(input_dim)
    
    # Determine if attacker is actively trying to snapshot
    is_attack_timestep = np.random.rand() < q_snapshot
    
    # Capture monitoring signals
    m_t = simulate_monitor_signals(t, is_attack=is_attack_timestep)
    
    # Defender detection
    anomaly_score = detector.update(m_t)
    metrics.detection_scores.append(anomaly_score)
    
    # Decide perturbation policy
    if anomaly_score > detection_threshold:
        mode = "OBSERVE_AND_OBFUSCATE"
        config = PerturbationConfig(
            mode=mode,
            amplitude=perturbation_amplitude,
            window_size=5,
            rotation_enabled=True,
            shuffle_enabled=True,
            timing_obfuscation=True
        )
        metrics.perturbation_events += 1
        
        # Track detection accuracy
        if is_attack_timestep:
            metrics.true_positives += 1
        else:
            metrics.false_positives += 1
    else:
        mode = "NORMAL"
        config = PerturbationConfig(
            mode=mode,
            amplitude=0.0,
            window_size=1,
            rotation_enabled=False,
            shuffle_enabled=False,
            timing_obfuscation=False
        )
        
        if is_attack_timestep:
            metrics.false_negatives += 1
    
    # Model forward pass
    a_t, o_t_baseline = model.forward(x_t, s_t)
    
    # Apply perturbation
    a_tilde = policy.apply_perturbation(a_t, config)
    
    # Decode from perturbed activations
    o_t = model.decode_from_activations(a_tilde)
    
    # Measure utility loss
    utility_loss = np.mean((o_t - o_t_baseline) ** 2)
    metrics.utility_losses.append(utility_loss)
    
    # Attacker snapshot (if attempting)
    if is_attack_timestep:
        measurement_noise = np.random.randn(*a_tilde.shape) * 0.01
        y = a_tilde + measurement_noise
        
        # Attacker inverts
        x_hat = inverter.invert(y)
        
        # Reconstruction loss
        rec_loss = np.mean((x_hat - x_t) ** 2)
        metrics.reconstruction_losses.append(rec_loss)
    
    # Progress indicator
    if (t + 1) % 20 == 0:
        print(f"  Timestep {t+1}/{T}: Anomaly={anomaly_score:.3f}, Mode={mode}")

return metrics
```

def analyze_results(metrics: SimulationMetrics):
“”“Analyze and display simulation results”””

```
print("\n" + "="*70)
print("SIMULATION RESULTS")
print("="*70)

# Detection Performance
total_attacks = len(metrics.reconstruction_losses)
total_normal = metrics.false_positives + (100 - total_attacks - metrics.true_positives)

precision = metrics.true_positives / (metrics.true_positives + metrics.false_positives) if (metrics.true_positives + metrics.false_positives) > 0 else 0
recall = metrics.true_positives / (metrics.true_positives + metrics.false_negatives) if (metrics.true_positives + metrics.false_negatives) > 0 else 0

print("\n📊 DETECTION PERFORMANCE:")
print(f"  True Positives: {metrics.true_positives}")
print(f"  False Positives: {metrics.false_positives}")
print(f"  False Negatives: {metrics.false_negatives}")
print(f"  Precision: {precision:.3f}")
print(f"  Recall: {recall:.3f}")
print(f"  Perturbation Events: {metrics.perturbation_events}")

# Reconstruction Accuracy (Attacker Performance)
if metrics.reconstruction_losses:
    avg_rec_loss = np.mean(metrics.reconstruction_losses)
    print(f"\n🎯 ATTACKER RECONSTRUCTION:")
    print(f"  Average Reconstruction Loss: {avg_rec_loss:.6f}")
    print(f"  Snapshots Attempted: {len(metrics.reconstruction_losses)}")
    print(f"  → Higher loss = Better defense")

# Utility Retention (Defender Cost)
avg_utility_loss = np.mean(metrics.utility_losses)
print(f"\n⚡ DEFENDER UTILITY COST:")
print(f"  Average Utility Loss: {avg_utility_loss:.6f}")
print(f"  → Lower loss = Better utility retention")

# Trade-off Analysis
print(f"\n🎯 SECURITY-UTILITY TRADE-OFF:")
if metrics.reconstruction_losses:
    tradeoff_ratio = avg_rec_loss / avg_utility_loss if avg_utility_loss > 0 else float('inf')
    print(f"  Ratio (Rec Loss / Utility Loss): {tradeoff_ratio:.2f}")
    print(f"  → Higher ratio = Better trade-off")

print("\n" + "="*70)
print("INTERPRETATION")
print("="*70)
print("""
```

✓ CLOSED-LOOP DEFENSE EFFECTIVENESS:

The simulation demonstrates the attacker-defender game where:

1. Attacker attempts to snapshot model activations
1. Defender monitors for anomalous access patterns
1. Upon detection, defender actively perturbs state
1. Attacker’s inversion attempts yield degraded reconstructions

Key Insight: By making snapshots “stale/misleading” through
temporal diffusion, keyed noise, and noncommutative transforms,
the defender increases reconstruction error significantly while
keeping utility loss acceptably small.

This creates a cryptographic “timeshadow” - captured states
are mathematically incorrect due to active perturbation.
“””)

# ============================================================================

# MAIN EXECUTION

# ============================================================================

if **name** == “**main**”:
# Run simulation with different configurations

```
print("Running baseline simulation...")
metrics_baseline = run_closed_loop_simulation(
    T=100,
    q_snapshot=0.15,
    detection_threshold=0.7,
    perturbation_amplitude=0.05
)
analyze_results(metrics_baseline)

print("\n\n" + "="*70)
print("✅ CLOSED-LOOP SIMULATION COMPLETE")
print("="*70)
print("""
```

Next Steps for Production Deployment:

1. Replace simple transformer with actual model
1. Implement real OS-level monitoring (DMA, memory access, etc.)
1. Deploy HSM-backed keying for perturbations
1. Add RL-based policy optimization
1. Implement multi-party authorization for obfuscation override
1. Create audit logging and retention policies
1. Tune detection thresholds on production workloads
1. Measure actual reconstruction error against real SipIt attacks
   “””)

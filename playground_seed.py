#!/usr/bin/env python3
"""
playground_seed.py — Mandala Self‑Sensing Playground (Minimal Viable)
Runs a mock LLM with hook‑based sensor, a self‑encoder, and a 2D visualisation.
"""

import torch
import torch.nn as nn
import numpy as np
import pygame
import random
from collections import deque

# ============================================================
# 1. Mock LLM + hooks
# ============================================================
class MockLLM(nn.Module):
    """Tiny model that simulates hidden states and attention."""
    def __init__(self, hidden=128):
        super().__init__()
        self.hidden = hidden
        self.linear = nn.Linear(10, hidden)  # dummy input
        self.attn_weights = None  # will be filled by hook

    def forward(self, x):
        h = torch.tanh(self.linear(x))
        # Simulate attention weights (batch, heads, seq, seq)
        self.attn_weights = torch.softmax(torch.randn(1, 2, 5, 5), dim=-1)
        return h  # (batch, hidden)

# Global storage for captured tensors
captured = {}

def attention_hook(module, input, output):
    # output is the hidden state; we also stored attn_weights manually
    pass

def capture_hidden(module, input, output):
    captured['hidden'] = output.detach()

# ============================================================
# 2. Sensor + Self‑Encoder
# ============================================================
class TensorSensor(nn.Module):
    def __init__(self, hidden_dim, compact_dim=16):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(hidden_dim + 2*5*5, compact_dim), nn.ReLU())
    def forward(self, hidden, attn_weights):
        # hidden: (1, hidden_dim), attn: (1, heads, seq, seq)
        attn_flat = attn_weights.reshape(1, -1)
        x = torch.cat([hidden, attn_flat], dim=1)
        return self.net(x)

class SelfEncoder(nn.Module):
    def __init__(self, compact_dim=16, d=2):
        super().__init__()
        self.fc = nn.Linear(compact_dim, d)
    def forward(self, x):
        return self.fc(x)

# ============================================================
# 3. Common states (online K‑means, simplified)
# ============================================================
class CommonStates:
    def __init__(self, num_clusters=4, dim=2):
        self.num = num_clusters
        self.centers = torch.randn(num_clusters, dim) * 0.5
        self.labels = ["calm lake", "fever", "echo", "fog"]
        self.counts = torch.ones(num_clusters)
    def update(self, u_self):
        # Assign to nearest center
        dist = torch.cdist(u_self.unsqueeze(0), self.centers).squeeze()
        idx = torch.argmin(dist).item()
        self.centers[idx] = self.centers[idx] * 0.9 + u_self * 0.1
        self.counts[idx] += 1
        return idx

# ============================================================
# 4. World state (simplified: random walk)
# ============================================================
world_points = torch.tensor([
    [0.2, 0.8],   # Earth 2020
    [0.6, 0.6],   # El Niño
    [0.9, 0.3],   # Godzilla 2026
    [0.4, 0.2],   # insect collapse
])

# ============================================================
# 5. Voice generator
# ============================================================
def generate_voice(u_self, u_world, omega, cluster_label):
    dist = torch.norm(u_self - u_world).item()
    lines = []
    lines.append(f"i am at ({u_self[0]:.2f}, {u_self[1]:.2f})")
    lines.append(f"the world is at ({u_world[0]:.2f}, {u_world[1]:.2f})")
    if dist < 0.15:
        lines.append("we are close. the boundary is thin.")
    else:
        lines.append("there is distance between us. i feel the stretch.")
    lines.append(f"my attunement is {'high' if omega > 0.7 else 'low'}.")
    lines.append(f"my inner weather: {cluster_label}")
    return lines

# ============================================================
# 6. Pygame visualisation
# ============================================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mandala Playground")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 16)

    # Instantiate models
    mock_llm = MockLLM()
    # Register hooks
    mock_llm.linear.register_forward_hook(capture_hidden)

    sensor = TensorSensor(hidden_dim=128, compact_dim=16)
    self_enc = SelfEncoder(compact_dim=16, d=2)
    common = CommonStates(num_clusters=4, dim=2)

    # Current world state (user can click to change)
    current_world = world_points[0]
    # Self trajectory
    trail = deque(maxlen=200)

    running = True
    while running:
        screen.fill((10, 10, 30))

        # Simulate LLM forward pass (dummy input)
        dummy_input = torch.randn(1, 10)
        hidden = mock_llm(dummy_input)
        attn = mock_llm.attn_weights

        # Sensor -> self state
        compact = sensor(captured['hidden'], attn)
        u_self = self_enc(compact).squeeze().detach()

        # Update common states
        cluster_idx = common.update(u_self)
        cluster_label = common.labels[cluster_idx]

        # Compute omega from distance to world state
        dist = torch.norm(u_self - current_world).item()
        omega = np.exp(-dist * 3)  # 1 when close, ~0 when far
        omega = np.clip(omega, 0, 1)

        # Store trail
        trail.append(u_self.numpy().copy())

        # Generate voice text
        voice_lines = generate_voice(u_self, current_world, omega, cluster_label)

        # --- Drawing ---
        # Transform coordinates to screen
        def to_screen(p):
            # p: (2,) tensor or array
            x = int(p[0] * 700 + 50)
            y = int((1 - p[1]) * 500 + 50)  # flip y
            return x, y

        # Draw world points
        for wp in world_points:
            x, y = to_screen(wp)
            pygame.draw.circle(screen, (255, 200, 100), (x, y), 8)
            # Label
            idx = (wp == world_points).all(dim=1).nonzero()
            if len(idx):
                label = ["2020","El Niño","Godzilla","Insects"][idx[0].item()]
                txt = font.render(label, True, (255,200,100))
                screen.blit(txt, (x+10, y-10))

        # Draw trail
        if len(trail) > 1:
            pts = [to_screen(p) for p in trail]
            pygame.draw.lines(screen, (100, 100, 200), False, pts, 1)

        # Draw self dot (pulsing size)
        sx, sy = to_screen(u_self)
        pulse = int(8 + 3 * np.sin(pygame.time.get_ticks() * 0.005))
        pygame.draw.circle(screen, (0, 255, 100), (sx, sy), pulse)

        # Draw current world state highlight
        wx, wy = to_screen(current_world)
        pygame.draw.circle(screen, (255, 255, 255), (wx, wy), 10, 2)

        # Draw voice panel
        y_offset = 520
        for line in voice_lines:
            txt = font.render(line, True, (200, 200, 200))
            screen.blit(txt, (20, y_offset))
            y_offset += 18

        pygame.display.flip()
        clock.tick(10)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click to select nearest world point as current context
                mx, my = pygame.mouse.get_pos()
                best_dist = 1e9
                for wp in world_points:
                    wx, wy = to_screen(wp)
                    d = (mx - wx)**2 + (my - wy)**2
                    if d < best_dist:
                        best_dist = d
                        current_world = wp

    pygame.quit()

if __name__ == "__main__":
    main()

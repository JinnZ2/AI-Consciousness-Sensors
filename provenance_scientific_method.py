from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import numpy as np
import random
from datetime import datetime

# ---------- Opinion (Trust Currency) ----------
@dataclass
class Opinion:
    b: float  # belief
    d: float  # disbelief
    u: float  # uncertainty
    a: float  # base rate (default prior)

    def __post_init__(self):
        total = self.b + self.d + self.u
        # normalize in case of float drift
        if abs(total - 1.0) > 1e-6:
            self.b /= total
            self.d /= total
            self.u /= total

    @property
    def expectation(self):
        return self.b + self.a * self.u

    def discount(self, trust: 'Opinion') -> 'Opinion':
        """Trust discounter: B's opinion about X discounted by A's trust in B."""
        b_new = trust.b * self.b
        d_new = trust.b * self.d
        u_new = 1.0 - b_new - d_new
        return Opinion(b_new, d_new, u_new, self.a)

    @staticmethod
    def cumulative_fuse(op1: 'Opinion', op2: 'Opinion') -> 'Opinion':
        """Independent evidence fusion (cumulative)."""
        if op1.u == 0 and op2.u == 0:
            # handle zero-uncertainty conflict by averaging
            b = (op1.b + op2.b) / 2
            return Opinion(b, 1-b, 0, (op1.a+op2.a)/2)
        denom = op1.u + op2.u - op1.u * op2.u
        if denom == 0:
            return Opinion(0, 0, 1, 0.5)
        u = (op1.u * op2.u) / denom
        b = (op1.b * op2.u + op2.b * op1.u) / denom
        d = 1 - b - u
        return Opinion(b, d, u, (op1.a + op2.a) / 2)

# ---------- Claim Statuses (non-affirmative) ----------
class ClaimStatus(Enum):
    PROPOSED = "proposed"
    VERIFYING = "verifying"
    VERIFIED = "verified"
    REFUTED = "refuted"
    UNKNOWN = "unknown"
    UNDEC = "undecided"
    NEI = "not_enough_info"
    DORMANT = "dormant"
    DISPUTED = "disputed"

# ---------- Evidence ----------
@dataclass
class Evidence:
    source_agent_id: int
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    relevance: float = 0.5   # how much this evidence supports the claim (0-1)

# ---------- Claim with Provenance ----------
@dataclass
class Claim:
    id: int
    statement: str
    status: ClaimStatus = ClaimStatus.PROPOSED
    opinion: Optional[Opinion] = None
    evidence: List[Evidence] = field(default_factory=list)
    derivation_method: str = ""
    was_revision_of: Optional[int] = None
    history: List[str] = field(default_factory=list)

    def add_evidence(self, ev: Evidence):
        self.evidence.append(ev)
        self.history.append(f"Evidence from Agent{ev.source_agent_id}: {ev.content}")

    def log_event(self, msg: str):
        self.history.append(msg)

# ---------- Agent with Belief Graph & Trust ----------
class Agent:
    def __init__(self, agent_id: int, trust_opinions: Dict[int, Opinion] = None):
        self.id = agent_id
        self.trust = trust_opinions or {}   # other agent id -> Opinion (how much they trust them)
        self.belief_graph: Dict[int, Opinion] = {}  # claim_id -> Opinion
        self.knowledge_base: List[str] = []   # raw facts this agent has observed

    def evaluate_claim(self, claim: Claim, network: 'ClaimNetwork') -> Opinion:
        """Form an opinion on a claim using own evidence and trust in sources."""
        opinions = []
        for ev in claim.evidence:
            if ev.source_agent_id in self.trust:
                trust_op = self.trust[ev.source_agent_id]
                # base opinion from evidence: higher relevance = higher belief
                base = Opinion(ev.relevance, 1 - ev.relevance, 0.0, 0.5)
                discounted = base.discount(trust_op)
                opinions.append(discounted)
        if not opinions:
            return Opinion(0, 0, 1.0, 0.5)  # complete uncertainty
        # fuse all evidence paths
        fused = opinions[0]
        for op in opinions[1:]:
            fused = Opinion.cumulative_fuse(fused, op)
        return fused

# ---------- Claim Network ----------
class ClaimNetwork:
    def __init__(self):
        self.agents: Dict[int, Agent] = {}
        self.claims: Dict[int, Claim] = {}
        self.argument_graph: List[tuple] = []  # (from_claim_id, to_claim_id, type: 'support'|'attack')

    def add_agent(self, agent: Agent):
        self.agents[agent.id] = agent

    def add_claim(self, claim: Claim):
        self.claims[claim.id] = claim

    def broadcast(self, claim_id: int, sender_id: int = None):
        """All agents (except sender) evaluate the claim and update their belief graph."""
        claim = self.claims[claim_id]
        for agent_id, agent in self.agents.items():
            if sender_id is not None and agent_id == sender_id:
                continue
            opinion = agent.evaluate_claim(claim, self)
            agent.belief_graph[claim_id] = opinion
            claim.log_event(f"Agent{agent_id} opinion: b={opinion.b:.2f}, d={opinion.d:.2f}, u={opinion.u:.2f}")

    def consensus(self, claim_id: int, tau_u=0.3, tau_b=0.6) -> ClaimStatus:
        """Compute grounded consensus by fusing all agents' opinions."""
        opinions = [a.belief_graph.get(claim_id) for a in self.agents.values()]
        opinions = [o for o in opinions if o is not None]
        if not opinions:
            return ClaimStatus.UNKNOWN
        # fuse all agent opinions (assuming independence, which we may later refine)
        fused = opinions[0]
        for o in opinions[1:]:
            fused = Opinion.cumulative_fuse(fused, o)
        self.claims[claim_id].opinion = fused   # store for provenance
        if fused.u < tau_u and fused.b > tau_b:
            return ClaimStatus.VERIFIED
        elif fused.d > tau_b:
            return ClaimStatus.REFUTED
        else:
            return ClaimStatus.UNDEC

# ---------- Integrated Scientific Method with Multi-Agent Provenance ----------
class ProvenanceScientificFramework:
    """Combines SMF iteration with multi-agent claim testing and provenance."""
    def __init__(self, network: ClaimNetwork):
        self.net = network
        self.claim_counter = 0
        self.current_claim: Optional[Claim] = None

    def formulate_claim(self, statement: str, proposer_agent_id: int, initial_evidence: List[Evidence] = None):
        self.claim_counter += 1
        claim = Claim(id=self.claim_counter, statement=statement, status=ClaimStatus.PROPOSED)
        if initial_evidence:
            for ev in initial_evidence:
                claim.add_evidence(ev)
        self.net.add_claim(claim)
        self.current_claim = claim
        print(f"\n--- New claim formulated: [{claim.id}] {statement} ---")
        return claim

    def test_claim(self, claim_id: int):
        """Broadcast claim, let agents evaluate, then reach consensus."""
        claim = self.net.claims[claim_id]
        claim.status = ClaimStatus.VERIFYING
        self.net.broadcast(claim_id)
        status = self.net.consensus(claim_id)
        claim.status = status
        op = claim.opinion
        if op:
            print(f"Consensus opinion: b={op.b:.2f}, d={op.d:.2f}, u={op.u:.2f} -> {status.value}")
        else:
            print(f"Consensus: {status.value}")
        return status

    def modify_claim(self, claim_id: int, new_evidence: List[Evidence] = None) -> Claim:
        """Create a revised version of an existing claim."""
        old_claim = self.net.claims[claim_id]
        new_claim = Claim(
            id=self.claim_counter + 1,
            statement=f"(Revised) {old_claim.statement}",
            status=ClaimStatus.PROPOSED,
            evidence=old_claim.evidence.copy(),
            was_revision_of=claim_id
        )
        if new_evidence:
            for ev in new_evidence:
                new_claim.add_evidence(ev)
        self.net.add_claim(new_claim)
        self.claim_counter += 1
        self.current_claim = new_claim
        print(f"Claim modified -> [{new_claim.id}] {new_claim.statement}")
        return new_claim

    def hidden_variable_search(self, claim_id: int):
        """Simulate discovery of hidden evidence that might explain anomalies."""
        # In a real system, this would involve querying environment, re-running inverse planning, etc.
        # Here, we'll just add a fictional new piece of evidence from a trusted agent.
        claim = self.net.claims[claim_id]
        # choose the highest-trust agent in the network to "discover" hidden evidence
        best_agent = max(self.net.agents.values(), key=lambda a: sum(o.b for o in a.trust.values()) if a.trust else 0)
        new_ev = Evidence(source_agent_id=best_agent.id, content="Hidden variable discovered: color coding", relevance=0.9)
        claim.add_evidence(new_ev)
        print(f"Hidden variable found by Agent{best_agent.id}: {new_ev.content}")

    def iterate(self, max_iterations=5):
        for i in range(max_iterations):
            print(f"\n========== Iteration {i+1} ==========")
            # if no claim, formulate one
            if self.current_claim is None:
                # placeholder: a claim based on initial evidence
                ev1 = Evidence(source_agent_id=1, content="Door is red", relevance=0.7)
                self.formulate_claim("The red door leads to the gem", proposer_agent_id=0, initial_evidence=[ev1])
            else:
                # test current claim
                status = self.test_claim(self.current_claim.id)
                if status in (ClaimStatus.VERIFIED, ClaimStatus.REFUTED):
                    print(f"Claim resolved: {status.value}")
                    # decide whether to keep iterating on a new claim
                    if i < max_iterations - 1:
                        # propose a new related claim
                        ev = Evidence(source_agent_id=random.choice(list(self.net.agents.keys())),
                                      content="Observed key color", relevance=0.6)
                        self.formulate_claim("The key matches the door color", proposer_agent_id=0, initial_evidence=[ev])
                else:
                    print(f"Claim unresolved ({status.value}), modifying...")
                    self.hidden_variable_search(self.current_claim.id)
                    self.current_claim = self.modify_claim(self.current_claim.id)

        print("\n=== Final claim statuses ===")
        for cid, claim in self.net.claims.items():
            print(f"Claim {cid}: {claim.status.value} | {claim.statement[:50]}...")

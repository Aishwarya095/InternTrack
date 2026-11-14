"""
Lab 4: Memory & Retrieval -- State vs. Stored Knowledge
Phase: A · Foundations
Goal: Separate short-term run state from long-term stored knowledge.

Deliverable & Acceptance Criterion:
"Retrieval over the store + history with tag filters and embedding similarity.
Acceptance: For a given task, retrieval returns correctly-tagged candidates
and similar prior items without conflating run state with the historical baseline."

Nodes Activated:
  - Retrieval node (seeds validation/no-repeat)

Memory Split:
  state.draft = candidate                           # Short-term run state
  hits  = retrieve(store, tags)                     # Long-term: Tag-based retrieval
  prior = retrieve(history, embed(candidate), k=5)  # Long-term: Similarity-based retrieval
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
import math
import re
import sys

# Ensure UTF-8 output encoding for terminal
sys.stdout.reconfigure(encoding='utf-8')


# =====================================================================
# 1. SHORT-TERM MEMORY (Session Run State)
# =====================================================================

@dataclass
class SessionState:
    session_id: str
    user_id: str
    draft: Optional[Dict[str, Any]] = None  # Active working candidate
    scratchpad: List[str] = field(default_factory=list)
    iteration_count: int = 0
    is_committed: bool = False

    def update_draft(self, candidate_data: Dict[str, Any]):
        """Mutates only the short-term working buffer."""
        self.draft = candidate_data
        self.iteration_count += 1
        self.scratchpad.append(f"Iteration {self.iteration_count}: Draft updated with keys {list(candidate_data.keys())}")


# =====================================================================
# 2. LONG-TERM MEMORY (Reference Store & History Archive)
# =====================================================================

@dataclass
class QuestionTestCase:
    item_id: str
    title: str
    category: str
    prompt_text: str
    expected_criteria: Dict[str, Any]
    tags: List[str]


@dataclass
class HistoricalSubmission:
    submission_id: str
    candidate_name: str
    usn: str
    domain: str
    organization: str
    project_summary: str
    final_grade: str
    verified_year: int
    tags: List[str]


class QuestionBank:
    """Long-term reference store: Questions, rubrics, and evaluation benchmarks."""
    def __init__(self):
        self.items: List[QuestionTestCase] = []
        self._tag_index: Dict[str, Set[str]] = {}

    def add(self, item: QuestionTestCase):
        self.items.append(item)
        for tag in item.tags:
            cleaned_tag = tag.strip().lower()
            if cleaned_tag not in self._tag_index:
                self._tag_index[cleaned_tag] = set()
            self._tag_index[cleaned_tag].add(item.item_id)

    def retrieve_by_tags(self, tags: List[str], match_mode: str = "any") -> List[QuestionTestCase]:
        """
        Long-term retrieval by tag filtering.
        match_mode: 'any' (OR) or 'all' (AND)
        """
        if not tags:
            return []
        
        normalized_tags = [t.strip().lower() for t in tags]
        matching_ids: Optional[Set[str]] = None

        for tag in normalized_tags:
            ids = self._tag_index.get(tag, set())
            if matching_ids is None:
                matching_ids = set(ids)
            else:
                if match_mode == "all":
                    matching_ids &= ids
                else:
                    matching_ids |= ids

        if not matching_ids:
            return []

        return [item for item in self.items if item.item_id in matching_ids]


class HistoryArchive:
    """Long-term history archive: Prior student submissions and locked records."""
    def __init__(self):
        self.archive: List[HistoricalSubmission] = []

    def add(self, item: HistoricalSubmission):
        self.archive.append(item)

    def count(self) -> int:
        return len(self.archive)


# =====================================================================
# 3. EMBEDDING & SIMILARITY RETRIEVAL ENGINE
# =====================================================================

class EmbeddingEngine:
    """
    Deterministic, zero-external-dependency semantic vector engine.
    Constructs normalized TF-IDF vector embeddings over n-grams and vocabulary.
    """
    def __init__(self):
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        # Extract alphanumeric words and 2-word combinations
        words = re.findall(r'\b[a-zA-Z0-9_]{2,}\b', text.lower())
        bigrams = [f"{words[i]}_{words[i+1]}" for i in range(len(words)-1)]
        return words + bigrams

    def fit(self, corpus: List[str]):
        """Computes Inverse Document Frequency (IDF) over corpus."""
        doc_count = len(corpus)
        df: Dict[str, int] = {}

        for doc in corpus:
            tokens = set(self._tokenize(doc))
            for t in tokens:
                df[t] = df.get(t, 0) + 1

        self.vocabulary = {term: idx for idx, term in enumerate(df.keys())}
        self.idf = {term: math.log((1 + doc_count) / (1 + count)) + 1.0 for term, count in df.items()}

    def embed(self, text: str) -> Dict[int, float]:
        """Produces a normalized sparse TF-IDF embedding vector."""
        tokens = self._tokenize(text)
        tf: Dict[str, int] = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1

        vector: Dict[int, float] = {}
        norm_sq = 0.0

        for term, count in tf.items():
            if term in self.vocabulary:
                idx = self.vocabulary[term]
                weight = count * self.idf.get(term, 1.0)
                vector[idx] = weight
                norm_sq += weight * weight

        # L2-normalize
        norm = math.sqrt(norm_sq)
        if norm > 0:
            for idx in vector:
                vector[idx] /= norm

        return vector

    @staticmethod
    def cosine_similarity(vec1: Dict[int, float], vec2: Dict[int, float]) -> float:
        """Computes cosine similarity between two unit-normalized sparse vectors."""
        # Dot product
        if len(vec1) > len(vec2):
            vec1, vec2 = vec2, vec1
        return sum(val * vec2.get(idx, 0.0) for idx, val in vec1.items())


# =====================================================================
# 4. RETRIEVAL NODE INTERFACE (Lab 4 Core Deliverable)
# =====================================================================

class RetrievalAgent:
    def __init__(self, question_bank: QuestionBank, history_archive: HistoryArchive, embedding_engine: EmbeddingEngine):
        self.store = question_bank
        self.history = history_archive
        self.engine = embedding_engine

    def retrieve_from_store(self, tags: List[str], match_mode: str = "any") -> List[QuestionTestCase]:
        """hits = retrieve(store, tags)"""
        return self.store.retrieve_by_tags(tags, match_mode=match_mode)

    def retrieve_from_history(self, candidate_text: str, k: int = 5) -> List[Dict[str, Any]]:
        """prior = retrieve(history, embed(candidate), k=5)"""
        query_vec = self.engine.embed(candidate_text)
        scored_items = []

        for item in self.history.archive:
            item_text = f"{item.domain} {item.organization} {item.project_summary} {' '.join(item.tags)}"
            item_vec = self.engine.embed(item_text)
            score = self.engine.cosine_similarity(query_vec, item_vec)
            scored_items.append({
                "submission": item,
                "similarity_score": round(score, 4)
            })

        # Rank by descending similarity score
        scored_items.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored_items[:k]


# =====================================================================
# 5. TEST HARNESS & ISOLATION AUDIT
# =====================================================================

def populate_sample_knowledge_bases() -> (QuestionBank, HistoryArchive, EmbeddingEngine):
    store = QuestionBank()
    
    # Pre-populate Question & Test-Case Bank
    store.add(QuestionTestCase(
        item_id="Q-001",
        title="Google India Eligibility Benchmark",
        category="Eligibility Check",
        prompt_text="Verify student meets minimum 8.5 CGPA, 0 backlogs, and >= 100 credits for SWE internship.",
        expected_criteria={"min_cgpa": 8.5, "max_backlogs": 0, "min_credits": 100},
        tags=["#google_india", "#swe", "#cgpa_cutoff", "#tier1"]
    ))
    store.add(QuestionTestCase(
        item_id="Q-002",
        title="Active Backlog Disqualification Check",
        category="Policy Guardrail",
        prompt_text="Check if candidate has any active/uncleared backlogs before release sign-off.",
        expected_criteria={"max_backlogs": 0, "strict_disqualification": True},
        tags=["#backlog_rule", "#guardrail", "#approval_gate"]
    ))
    store.add(QuestionTestCase(
        item_id="Q-003",
        title="Machine Learning Domain Technical Screening",
        category="Domain Assessment",
        prompt_text="Evaluate background in distributed model training, PyTorch, and linear algebra.",
        expected_criteria={"domain": "Machine Learning", "min_cgpa": 8.0},
        tags=["#ml", "#data_science", "#technical_interview"]
    ))
    store.add(QuestionTestCase(
        item_id="Q-004",
        title="Embedded Systems FPGA Requirement",
        category="Domain Assessment",
        prompt_text="Check hardware description language skills (Verilog/VHDL) and kernel bring-up experience.",
        expected_criteria={"domain": "Embedded Systems", "min_cgpa": 7.5},
        tags=["#embedded", "#intel", "#vlsi"]
    ))

    history = HistoryArchive()
    
    # Pre-populate Prior Student Submissions Archive
    history.add(HistoricalSubmission(
        submission_id="HIST-2025-01",
        candidate_name="Arjun Mehta",
        usn="1KG20CS019",
        domain="Software Engineering",
        organization="Google India",
        project_summary="Designed and deployed high-throughput gRPC distributed caching proxy in Go and Kubernetes.",
        final_grade="S (Outstanding)",
        verified_year=2025,
        tags=["#swe", "#google_india", "#grpc", "#cloud"]
    ))
    history.add(HistoricalSubmission(
        submission_id="HIST-2025-02",
        candidate_name="Sneha Kulkarni",
        usn="1KG20IS044",
        domain="Machine Learning",
        organization="Amazon India",
        project_summary="Built real-time personalization pipeline using transformer recommendation embeddings.",
        final_grade="S (Outstanding)",
        verified_year=2025,
        tags=["#ml", "#amazon", "#recsys", "#nlp"]
    ))
    history.add(HistoricalSubmission(
        submission_id="HIST-2024-03",
        candidate_name="Karthik N",
        usn="1KG19EC031",
        domain="Embedded Systems",
        organization="Intel",
        project_summary="Developed Linux kernel device driver and DMA controller firmware for RISC-V SoC.",
        final_grade="A+ (Excellent)",
        verified_year=2024,
        tags=["#embedded", "#intel", "#kernel", "#riscv"]
    ))
    history.add(HistoricalSubmission(
        submission_id="HIST-2024-04",
        candidate_name="Rohan Joshi",
        usn="1KG19CS088",
        domain="Software Engineering",
        organization="Infosys InStep",
        project_summary="Created enterprise microservices dashboard using React and Spring Boot.",
        final_grade="A (Very Good)",
        verified_year=2024,
        tags=["#swe", "#infosys", "#fullstack", "#spring"]
    ))

    # Fit embedding engine on all historical and reference text
    corpus = [f"{q.title} {q.prompt_text} {' '.join(q.tags)}" for q in store.items] + \
             [f"{h.domain} {h.organization} {h.project_summary} {' '.join(h.tags)}" for h in history.archive]
    
    engine = EmbeddingEngine()
    engine.fit(corpus)

    return store, history, engine


def run_lab4_test_harness():
    print("=" * 70)
    print("LAB 4 VERIFICATION: MEMORY & RETRIEVAL (STATE VS STORED)")
    print("Acceptance: Tag-based retrieval over Store + Similarity over History;")
    print("Short-term run state does not pollute or mutate long-term baseline.")
    print("=" * 70)

    store, history, engine = populate_sample_knowledge_bases()
    initial_history_count = history.count()
    retriever = RetrievalAgent(store, history, engine)

    # 1. Initialize Short-Term Run State
    state = SessionState(session_id="SESS-2026-99", user_id="1KG21CS045")
    candidate_draft = {
        "candidate_name": "Rahul Kumar",
        "usn": "1KG21CS045",
        "target_company": "Google India",
        "target_role": "Software Engineering Intern",
        "project_proposal": "Developing high-throughput gRPC caching service for distributed microservices architecture."
    }
    state.update_draft(candidate_draft)
    print("\n1. SHORT-TERM RUN STATE INITIALIZED:")
    print(f"   - Session ID: {state.session_id}")
    print(f"   - Draft Target: {state.draft['target_company']} ({state.draft['target_role']})")
    print(f"   - Scratchpad Log: {state.scratchpad[-1]}")

    # 2. Long-Term Retrieval via Tags (Question & Test-Case Bank)
    tags_to_query = ["#google_india", "#tier1"]
    hits = retriever.retrieve_from_store(tags_to_query, match_mode="any")
    print(f"\n2. LONG-TERM RETRIEVAL VIA TAGS (Query: {tags_to_query}):")
    print(f"   - Matched items in Question Bank: {len(hits)}")
    for item in hits:
        print(f"     * [{item.item_id}] {item.title} (Tags: {', '.join(item.tags)})")
    assert any(h.item_id == "Q-001" for h in hits), "Expected Q-001 in tag matches!"

    # 3. Long-Term Retrieval via Similarity (History Archive)
    candidate_text = f"{candidate_draft['target_company']} {candidate_draft['target_role']} {candidate_draft['project_proposal']}"
    prior = retriever.retrieve_from_history(candidate_text, k=3)
    print(f"\n3. LONG-TERM RETRIEVAL VIA EMBEDDING SIMILARITY (Top-3 Similar Prior Submissions):")
    for rank, res in enumerate(prior, 1):
        sub = res["submission"]
        score = res["similarity_score"]
        print(f"   - Rank {rank}: [{sub.submission_id}] {sub.candidate_name} ({sub.organization}) -- Score: {score}")
        print(f"     Summary: {sub.project_summary}")
        print(f"     Grade: {sub.final_grade} ({sub.verified_year})")

    top_hit = prior[0]["submission"]
    assert top_hit.submission_id == "HIST-2025-01", "Expected Arjun Mehta (Google India SWE) as top match!"
    assert prior[0]["similarity_score"] > 0.35, "Expected high similarity score for closely aligned proposal!"

    # 4. Pitfall Avoidance Audit: Verify Baseline State Integrity
    print("\n4. PITFALL VERIFICATION: STATE VS. ARCHIVE SEPARATION AUDIT:")
    state.update_draft({"candidate_name": "CORRUPTED_INFLIGHT_DATA", "mutated": True})
    assert history.count() == initial_history_count, "HistoryArchive count must remain unchanged!"
    for h in history.archive:
        assert h.candidate_name != "CORRUPTED_INFLIGHT_DATA", "Historical baseline was polluted by short-term state!"
    print("   [PASSED] Short-term draft mutations did NOT contaminate the historical baseline archive.")

    print("\n" + "=" * 70)
    print("ACCEPTANCE CRITERION VERIFIED: PASSED (100%)")
    print("Successfully demonstrated clean separation of Short-Term Run State")
    print("from Long-Term Stored Knowledge with tag filters and similarity retrieval.")
    print("=" * 70)


if __name__ == "__main__":
    run_lab4_test_harness()

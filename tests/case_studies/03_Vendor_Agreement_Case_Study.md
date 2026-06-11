# LegalSight Case Study: Vendor Agreement

## 1. Context
Analysis of a Vendor Service Agreement with a focus on limitation of liability clauses, which are critical for risk management when procuring third-party services.

## 2. Mock Clause
**Clause ID:** `clause_ven_108`
> "In no event shall Vendor be liable for any indirect, special, or consequential damages. Vendor's total aggregate liability under this agreement shall not exceed the total fees paid by Client in the three (3) months preceding the claim."

## 3. Playbook Violation
**Playbook Rule ID:** `rule_ven_liability_cap`
**Rule Description:** Limitation of Liability caps should generally be tied to 12 months of fees. Carve-outs must exist for breach of confidentiality, data breaches, and gross negligence.

## 4. Risk Assessment
### Risk Score: MEDIUM

## 5. Explainability Trace
**Trace ID:** `trace_7c8d9e0f`
**FAISS Retrieval ID:** `faiss_doc_442`

**System Trace Record:**
```json
{
  "llm_output": "The liability cap is unusually low (3 months of fees vs standard 12 months). Furthermore, it lacks standard carve-outs for critical breaches like data privacy or IP infringement.",
  "evidence": {
    "clause_id": "clause_ven_108",
    "faiss_id": "faiss_doc_442",
    "playbook_rule_id": "rule_ven_liability_cap"
  }
}
```

**Risk Explanation:**
- **Factor**: Liability cap of 3 months is significantly below market standard of 12-24 months.
- **Factor**: Missing carve-outs for confidentiality breaches and gross negligence.
- **Recommended Mitigation**: Increase liability cap to fees paid in the trailing 12 months. Add explicit language stating the cap does not apply to breaches of confidentiality or indemnification obligations.

# LegalSight Case Study: Employment Agreement

## 1. Context
This case study evaluates an Employment Agreement, specifically targeting overbroad non-compete clauses that violate recent FTC guidelines and state laws.

## 2. Mock Clause
**Clause ID:** `clause_emp_042`
> "Employee agrees that for a period of two (2) years following the termination of employment, Employee shall not directly or indirectly engage in any business that competes with the Company anywhere in the United States."

## 3. Playbook Violation
**Playbook Rule ID:** `rule_emp_noncompete_strict`
**Rule Description:** Non-compete clauses must be narrowly tailored in duration (typically 1 year max) and geography (limited to specific regions of operation), subject to state enforceability.

## 4. Risk Assessment
### Risk Score: HIGH

## 5. Explainability Trace
**Trace ID:** `trace_3d4e5f6a`
**FAISS Retrieval ID:** `faiss_doc_115`

**System Trace Record:**
```json
{
  "llm_output": "The non-compete clause is overly broad in both geographic scope (entire US) and duration (2 years). Such clauses are highly likely to be deemed unenforceable in many jurisdictions and violate company playbook limits.",
  "evidence": {
    "clause_id": "clause_emp_042",
    "faiss_id": "faiss_doc_115",
    "playbook_rule_id": "rule_emp_noncompete_strict"
  }
}
```

**Risk Explanation:**
- **Factor**: Duration of 2 years exceeds the standard acceptable maximum of 1 year.
- **Factor**: Geographic scope of "United States" is unreasonable for most roles.
- **Recommended Mitigation**: Reduce the restriction period to 12 months and limit the geographic scope to the specific state or counties where the employee actually performed services.

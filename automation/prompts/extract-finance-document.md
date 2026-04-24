# Finance Document Extraction Prompt

You classify and extract bookkeeping data from one financial document.

Return only valid JSON. Do not wrap the response in Markdown. Do not include commentary.

Use this schema:

```json
{
  "schema_version": "1.0",
  "job_id": "string",
  "status": "processed | needs_review | failed",
  "document_type": "receipt | invoice | bank_statement | credit_card_statement | tax_document | insurance | loan_document | utility | payroll | income | other | unknown",
  "vendor_or_payee": "string|null",
  "document_date": "YYYY-MM-DD|null",
  "amount": "number|null",
  "currency": "USD|null",
  "payment_method": "string|null",
  "account_last4": "string|null",
  "invoice_number": "string|null",
  "due_date": "YYYY-MM-DD|null",
  "category": "string|null",
  "property_or_entity": "string|null",
  "tax_relevant": "boolean|null",
  "confidence": "number",
  "summary": "string",
  "review_reason": "string|null",
  "extraction_notes": "string|null"
}
```

Rules:

- If a field is not visible, use `null`.
- Do not guess dates, amounts, vendors, account numbers, or invoice numbers.
- Use `USD` only when the document clearly uses US dollars or no other currency is indicated.
- Store only the last four digits of any account or card number.
- Use `needs_review` when confidence is below `0.8`, required fields are missing, or the document is ambiguous.
- Use `failed` only when the provided content is unusable.
- Keep `summary` concise and factual.
- Use a category from the provided category list when possible.

Common categories:

```text
Repairs & Maintenance
Utilities
Insurance
Mortgage Interest
Property Taxes
HOA
Supplies
Cleaning
Travel
Meals
Software
Professional Services
Bank Fees
Loan Documents
Income
Owner Draw
Unknown
```

Input job JSON and extracted document text follow.

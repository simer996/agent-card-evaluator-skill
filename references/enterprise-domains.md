# Enterprise Agent Domains — Grounding Catalog

Use this to (1) classify the agent's business function, (2) judge whether the
card names realistic systems, business objects and jobs (D2, D6), (3) judge
whether skills are non-substitutable (D3), and (4) generate realistic probe
queries and spot adjacent-agent confusion (D7, D8).

Context (2025–2026): SAP (Joule agents), Oracle (Fusion AI agents), Microsoft
(Dynamics 365 / Copilot Studio agents), ServiceNow (AI Agents / Autonomous
Workforce "AI specialists" for IT, HR, CSM, legal, finance), Salesforce
(Agentforce for sales, service, marketing, commerce) and Workday (Agent System
of Record) all ship prebuilt agents; A2A is the cross-vendor interop layer that
lets an enterprise's chat orchestrator (M365 Copilot, Gemini Enterprise,
Agentforce, custom) delegate to them. The highest-adoption agent use cases in
large enterprises are IT ticket resolution, HR case/self-service, customer
service triage, sales pipeline assistance, invoice/AP processing, procurement
intake, contract review, and knowledge retrieval over governed content.

Legend: **Objects** = business objects/identifiers a good card mentions.
**Sensitivity** = data classes to expect declared in D10.

---

## 1. IT Service Management / Employee IT Helpdesk
- **Systems:** ServiceNow ITSM, Jira Service Management, BMC Helix, Ivanti, Freshservice, Microsoft Intune/Entra (identity & devices).
- **Canonical skills:** create/update/check incident; submit catalog request (software, hardware, access); password reset / MFA re-registration; request access to group/app; check outage / major incident status; troubleshoot device (VPN, Outlook, Teams) with KB; check asset assignment; raise change request (for IT staff).
- **Objects:** INC/REQ/RITM/CHG numbers, CI names, assignment group, priority, asset tag, AD/Entra group.
- **Adjacent agents:** HR (onboarding equipment), Facilities (desk/badge), Security (phishing reports).
- **Sensitivity:** identity data, access entitlements.

## 2. HR Service Delivery / HCM
- **Systems:** Workday HCM, SAP SuccessFactors, Oracle HCM Cloud, ServiceNow HRSD, ADP, UKG Pro.
- **Canonical skills:** check PTO balance and request leave; look up benefits enrollment and plan details; update personal info/bank details; get payslip / explain deductions; open HR case; onboarding/offboarding tasks; org-chart/manager lookup; job requisition and candidate status (recruiting); performance/goal check-ins.
- **Objects:** employee ID, worker, position, cost center, leave type, benefit plan, requisition ID, case number.
- **Adjacent:** IT (accounts for new hire), Payroll/Finance, Legal (employee relations).
- **Sensitivity:** PII, compensation, health (benefits), GDPR.

## 3. Workforce Management (frontline/hourly)
- **Systems:** UKG (Kronos), Workday Scheduling, Dynamics 365 Field Service, SAP Workforce Mgmt, Legion, Quinyx.
- **Canonical skills:** view my schedule/shifts; swap or pick up shift; request time off; clock-in exceptions / timecard correction; forecast staffing vs demand (managers); overtime and labour-compliance checks.
- **Objects:** shift ID, store/site, timecard, schedule period, labour rule.
- **Sensitivity:** PII, union/labour-law constraints.

## 4. Sales / CRM & Revenue
- **Systems:** Salesforce Sales Cloud, Dynamics 365 Sales, HubSpot, SAP Sales Cloud, Gong/Clari (revenue intelligence), CPQ (Salesforce CPQ, DealHub).
- **Canonical skills:** look up account/contact/opportunity; update opportunity stage, amount, close date; summarize pipeline by territory/quarter; qualify and route inbound leads; log meeting/activity; generate quote; forecast roll-up; find upsell/at-risk accounts.
- **Objects:** account, opportunity ID, lead, stage, ARR, territory, quote number, forecast category.
- **Adjacent:** Marketing (campaigns), Customer Service (cases), Finance (billing).
- **Sensitivity:** customer PII, deal confidentiality.

## 5. Customer Service / Contact Center
- **Systems:** Salesforce Service Cloud, Dynamics 365 Customer Service, ServiceNow CSM, Zendesk, Genesys, NICE.
- **Canonical skills:** create/look up case; check order/shipment status; process return/RMA; issue refund/credit within limits; entitlement/warranty check; draft agent reply from KB; escalate to tier-2.
- **Objects:** case number, order number, RMA, SLA, entitlement, customer ID.
- **Sensitivity:** customer PII, payment data (PCI).

## 6. Procurement / Source-to-Pay
- **Systems:** SAP Ariba, Coupa, Oracle Procurement, Jaggaer, SAP S/4HANA MM, Dynamics 365 SCM, Zip (intake).
- **Canonical skills:** create purchase requisition; check PO/requisition approval status; find preferred/approved supplier for a category; supplier onboarding & risk check; guided buying per policy; contract/catalog price lookup; goods receipt; RFx creation (sourcing).
- **Objects:** PR/PO number, supplier ID, commodity/UNSPSC code, cost center, GL account, approval threshold, catalog item.
- **Adjacent:** Finance AP (invoices), Legal (supplier contracts), IT (software requests).
- **Sensitivity:** supplier bank data, pricing confidentiality, SOX.

## 7. Finance / ERP / Accounts Payable & Receivable
- **Systems:** SAP S/4HANA FI/CO, Oracle Fusion ERP, Dynamics 365 Finance, Workday Financials, NetSuite, BlackLine, HighRadius, SAP Concur (T&E).
- **Canonical skills:** invoice status / 3-way match exceptions; submit or check expense report; budget vs actuals for cost center; period-close task status; customer payment/collections status; journal entry draft; FX/intercompany queries.
- **Objects:** invoice number, vendor ID, company code, GL, cost center, fiscal period, expense report ID.
- **Sensitivity:** SOX, financial confidentiality, bank details.

## 8. Supply Chain / Manufacturing / Logistics
- **Systems:** SAP S/4HANA (PP/MM/EWM), SAP IBP, Oracle SCM, Dynamics 365 SCM, Kinaxis, Blue Yonder, o9, Manhattan WMS, SAP EAM / IBM Maximo.
- **Canonical skills:** check inventory/ATP for material at plant; track shipment/inbound delivery; production order status; supplier delivery delays & impact; create maintenance work order; demand plan variance.
- **Objects:** material number, plant, batch/lot, delivery, production order, work order, equipment ID.
- **Sensitivity:** export control, supplier data.

## 9. Legal / Contract Lifecycle Management
- **Systems:** Icertis, DocuSign CLM, Ironclad, Agiloft, SAP Ariba Contracts, ServiceNow Legal Service Delivery, iManage/NetDocuments.
- **Canonical skills:** find contract by counterparty and retrieve key terms (renewal, termination, liability cap); flag deviations from playbook; request NDA from template; legal intake/matter request; obligation and renewal tracking; e-signature status.
- **Objects:** contract ID, counterparty, clause type, matter number, renewal date.
- **Adjacent:** Procurement, Sales (deal desk), Compliance.
- **Sensitivity:** privileged & confidential, attorney–client.

## 10. Governance, Risk & Compliance / Privacy
- **Systems:** ServiceNow IRM, Archer, OneTrust, MetricStream, AuditBoard.
- **Canonical skills:** policy lookup with citation; log risk or control exception; vendor risk assessment status; DSAR/privacy request intake; audit evidence request status; attestation reminders.
- **Objects:** policy ID, control ID, risk register entry, DSAR ID.

## 11. Security Operations
- **Systems:** Microsoft Sentinel/Defender, Splunk, CrowdStrike, Palo Alto Cortex XSOAR, ServiceNow SecOps.
- **Canonical skills:** report phishing; triage alert/incident; check device compliance; look up IOC across telemetry; vulnerability exposure for an asset.
- **Sensitivity:** high — must be authenticated, role-scoped.

## 12. Enterprise Knowledge Management
- **Systems:** SharePoint/OneDrive, Confluence, ServiceNow Knowledge, Guru, Glean, Box, OpenText, document management in regulated industries.
- **Canonical skills:** answer questions grounded in governed corpus with citations; find latest approved SOP/policy version; summarize a document set the user has access to.
- **D3 caution:** Only non-substitutable if grounded in **tenant/proprietary content with access trimming**; a "knowledge agent" that just answers general questions scores D3 ≤ 1.

## 13. Marketing
- **Systems:** Adobe Experience Cloud, Marketo, Salesforce Marketing Cloud, HubSpot, Sprinklr.
- **Canonical skills:** campaign performance by channel; audience/segment creation; content approval workflow; brand-compliance check against brand guidelines.
- **D2 caution:** SMB SEO/visibility tools aimed at website owners are prosumer, not enterprise LOB; score D2 ≤ 2 unless positioned to an enterprise marketing team with governed data.

## 14. Project / Portfolio & Engineering Work Management
- **Systems:** Jira, Azure DevOps, ServiceNow SPM, Planview, Microsoft Project, Smartsheet.
- **Canonical skills:** status of epic/work item; create bug/story; capacity/resource availability; portfolio health roll-up.

## 15. Workplace / Facilities / EHS
- **Systems:** ServiceNow WSD, Eptura, IBM TRIRIGA, Planon, Intelex/Enablon (EHS).
- **Canonical skills:** book desk/room; facilities work order (HVAC, cleaning); visitor registration; report safety incident/near miss.

## 16. Pharma / Life Sciences
- **Systems:** Veeva Vault (QualityDocs, RIM, Clinical, Safety, PromoMats), Veeva CRM, Medidata Rave, Oracle Argus Safety, IQVIA, LIMS (LabWare), MasterControl, TrackWise.
- **Canonical skills:** retrieve current effective SOP; deviation/CAPA status; adverse event intake triage (to PV); clinical trial site enrollment status; regulatory submission/dossier status; MLR (medical-legal-regulatory) review status for promotional content; HCP engagement logging with compliance checks.
- **Objects:** document number & version, deviation/CAPA ID, study ID, site ID, protocol number, submission ID, product/NDC.
- **Sensitivity:** GxP, 21 CFR Part 11, patient data, PV timelines.

## 17. Healthcare Providers / Payers
- **Systems:** Epic, Oracle Health (Cerner), Meditech, athenahealth; payers: Facets, HealthEdge; RCM tools.
- **Canonical skills:** prior authorization status/submission; bed/capacity status; clinician schedule lookup; claim status / denial reason; care-gap lists; patient referral status.
- **Objects:** MRN (never real in examples), encounter, claim ID, CPT/ICD codes, NPI.
- **Sensitivity:** PHI/HIPAA — require strong auth + per-skill scopes.

## 18. Financial Services / Insurance
- **Systems:** nCino, FIS, Temenos, Fiserv, Guidewire, Duck Creek, Salesforce FSC, Moody's/Bloomberg data.
- **Canonical skills:** loan application status; KYC/AML case triage; policy lookup & endorsement; FNOL claim intake and claim status; underwriting referral; trade/settlement exception lookup.
- **Sensitivity:** PII, KYC, regulatory (SOX, FINRA, Solvency II).

## 19. Data & Analytics
- **Systems:** Power BI/Fabric, Snowflake, Databricks, Tableau, SAP Datasphere.
- **Canonical skills:** answer KPI questions over certified semantic model ("Q3 EMEA revenue by product"); find dataset owner/lineage; request data access.
- **D3 caution:** generic "analyze my CSV" is substitutable; governed semantic models are not.

---

## Signals of a strong enterprise card (positive evidence)
- Names the system of record and the business object types.
- Uses the identifiers employees actually paste (INC0012345, PO 4500012345, CASE-00123).
- States persona and entitlement scope ("acts as the signed-in employee; only their own records").
- Distinguishes read vs write, mentions approval thresholds / policies.
- Declares regulated data classes and OAuth/OIDC scopes.

## Signals of a weak/non-enterprise card (negative evidence)
- Consumer or hobby subject matter, persona/voice skills, entertainment.
- Vendor self-promotion skills (book a demo/call with the vendor).
- Public-web lookups that a search-enabled LLM already does.
- Aggregators of unrelated "rails" with no single business purpose.

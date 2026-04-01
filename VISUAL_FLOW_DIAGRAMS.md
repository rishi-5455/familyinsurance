# 📊 VISUAL FLOW DIAGRAMS

## 🎯 SYSTEM OVERVIEW

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃         BLOCKCHAIN ENABLED FAMILY INSURANCE SYSTEM          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

        ┌─────────────────────────────────────────┐
        │         NEXT.JS FRONTEND                │
        │         (React + TypeScript)            │
        └──────────────┬──────────────────────────┘
                       │ HTTP/REST API
                       ▼
        ┌─────────────────────────────────────────┐
        │         FLASK BACKEND                   │
        │         (Python + JWT Auth)             │
        └──┬──────────┬──────────────┬────────────┘
           │          │              │
           ▼          ▼              ▼
     ┌─────────┐  ┌──────────┐  ┌──────────────┐
     │ MongoDB │  │ Algorand │  │ IPFS/Storage │
     │Database │  │Blockchain│  │  Documents   │
     └─────────┘  └──────────┘  └──────────────┘
```

---

## 👥 THE THREE ROLES

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  ┏━━━━━━━━━━━━━┓     ┏━━━━━━━━━━━━━┓     ┏━━━━━━━━━━━━━┓  │
│  ┃    ADMIN    ┃     ┃    USER     ┃     ┃  VERIFIER   ┃  │
│  ┃  (Company)  ┃     ┃  (Customer) ┃     ┃  (Hospital) ┃  │
│  ┗━━━━━━━━━━━━━┛     ┗━━━━━━━━━━━━━┛     ┗━━━━━━━━━━━━━┛  │
│        │                   │                    │          │
│        │                   │                    │          │
│  Creates Templates    Buys Policies      Verifies Policies│
│  Approves Claims      Submits Claims     Checks Blockchain│
│  Views Analytics      Manages Family     Quick Validation │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🔄 COMPLETE INSURANCE LIFECYCLE

```
START
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: POLICY TEMPLATE CREATION                          │
│ ─────────────────────────────────────────────────────────  │
│                                                             │
│  👤 ADMIN                                                   │
│    │                                                        │
│    └──> Creates Template (TPL-XXXXX)                       │
│           │                                                 │
│           ├──> Name: "Family Health Premium"               │
│           ├──> Coverage: ₹500,000                           │
│           ├──> Duration: 12 months                          │
│           └──> Saved to MongoDB (policy_templates)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: USER REGISTRATION & POLICY PURCHASE               │
│ ─────────────────────────────────────────────────────────  │
│                                                             │
│  👤 USER (Rajesh Kumar)                                     │
│    │                                                        │
│    ├──> Registers Account                                  │
│    │      └──> Email: rajesh@gmail.com                     │
│    │                                                        │
│    ├──> Adds Family Members                                │
│    │      ├──> Wife: Priya Kumar (32)                      │
│    │      └──> Son: Aarav Kumar (5)                        │
│    │                                                        │
│    ├──> Connects Algorand Wallet                           │
│    │      └──> Address: ALGO7XYZ...                        │
│    │                                                        │
│    └──> Buys Policy                                        │
│           │                                                 │
│           ├──> Creates POL-XXXXX                           │
│           ├──> Saves to MongoDB                            │
│           ├──> ⛓️  Records on Algorand Blockchain           │
│           ├──> 📄 Uploads documents to IPFS                │
│           └──> Generates QR Code                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: MEDICAL SITUATION - POLICY VERIFICATION           │
│ ─────────────────────────────────────────────────────────  │
│                                                             │
│  👤 USER                                   👤 VERIFIER      │
│    │                                          │             │
│    └──> Visits Hospital ─────────────────────┤             │
│         Shows Policy ID or QR Code           │             │
│                                              │             │
│                               Hospital Staff │             │
│                                    │         │             │
│                                    └──> Enters POL-XXXXX   │
│                                           │                │
│                                           ▼                │
│                                    System Checks:          │
│                                    ├──> MongoDB ✓          │
│                                    ├──> Blockchain ✓       │
│                                    └──> Returns Details    │
│                                                             │
│                                    VERIFICATION RESULT:    │
│                                    ┌─────────────────────┐ │
│                                    │ ✅ Policy Valid     │ │
│                                    │ ✅ Coverage: ₹5L    │ │
│                                    │ ✅ Active Status    │ │
│                                    │ ✅ Blockchain OK    │ │
│                                    └─────────────────────┘ │
│                                           │                │
│                                           ▼                │
│                                    Treatment Approved!     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: CLAIM SUBMISSION                                  │
│ ─────────────────────────────────────────────────────────  │
│                                                             │
│  👤 USER (After Treatment)                                  │
│    │                                                        │
│    └──> Submits Claim                                      │
│           │                                                 │
│           ├──> Policy ID: POL-XXXXX                        │
│           ├──> Reason: "Aarav hospitalization"             │
│           ├──> Amount: ₹50,000                              │
│           ├──> Uploads: Hospital bills, reports            │
│           │                                                 │
│           ├──> Creates CLM-XXXXX                           │
│           ├──> Saves to MongoDB                            │
│           ├──> ⛓️  Records on Blockchain                    │
│           ├──> 📄 Uploads documents                         │
│           └──> Status: PENDING                             │
│                                                             │
│           ▼                                                 │
│        Notification sent to ADMIN                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 5: CLAIM REVIEW & APPROVAL                           │
│ ─────────────────────────────────────────────────────────  │
│                                                             │
│  👤 ADMIN                                                   │
│    │                                                        │
│    ├──> Sees Notification: "1 pending claim"               │
│    │                                                        │
│    ├──> Opens "Claims Management"                          │
│    │      └──> Views claim details                         │
│    │                                                        │
│    ├──> Reviews Documents                                  │
│    │      ├──> Hospital bills                              │
│    │      └──> Medical reports                             │
│    │                                                        │
│    ├──> Verifies Policy Status                             │
│    │      └──> Policy is active ✓                          │
│    │                                                        │
│    └──> Clicks "APPROVE"                                   │
│           │                                                 │
│           ├──> Updates claim status: APPROVED              │
│           ├──> ⛓️  Records approval on Blockchain           │
│           ├──> Updates policy status                       │
│           ├──> Sends notification to USER                  │
│           └──> Triggers payment process                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 6: CLAIM SETTLEMENT                                  │
│ ─────────────────────────────────────────────────────────  │
│                                                             │
│  👤 USER                                                    │
│    │                                                        │
│    ├──> Receives Notification                              │
│    │      "Claim CLM-XXXXX was approved ✅"                 │
│    │                                                        │
│    └──> Payment Processed                                  │
│           └──> ₹50,000 transferred to bank                 │
│                                                             │
│  🎉 CLAIM SETTLED SUCCESSFULLY!                            │
│                                                             │
│  ⛓️  Complete audit trail on Blockchain:                   │
│     ├──> Policy creation timestamp                         │
│     ├──> Claim submission timestamp                        │
│     └──> Approval timestamp                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
END
```

---

## 🔐 BLOCKCHAIN INTEGRATION FLOW

```
┌─────────────────────────────────────────────────────────────┐
│              BLOCKCHAIN TRANSACTION FLOW                    │
└─────────────────────────────────────────────────────────────┘

 USER ACTION                  BACKEND                BLOCKCHAIN
     │                           │                        │
     │──────────────────────────>│                        │
     │   1. Buy Policy            │                        │
     │                            │                        │
     │                            ├───────────────────────>│
     │                            │ createPolicy()         │
     │                            │ - policyId             │
     │                            │ - walletAddress        │
     │                            │ - coverageAmount       │
     │                            │ - status: "active"     │
     │                            │                        │
     │                            │<───────────────────────│
     │<───────────────────────────│ Transaction ID         │
     │   Policy Created ✓         │ Block Number           │
     │                            │                        │
     │                            │                        │
     │──────────────────────────>│                        │
     │   2. Submit Claim          │                        │
     │                            │                        │
     │                            ├───────────────────────>│
     │                            │ submitClaim()          │
     │                            │ - claimId              │
     │                            │ - policyId             │
     │                            │ - status: "pending"    │
     │                            │                        │
     │                            │<───────────────────────│
     │<───────────────────────────│ Transaction ID         │
     │   Claim Submitted ✓        │                        │
     │                            │                        │
     │                            │                        │
ADMIN ACTION                     │                        │
     │──────────────────────────>│                        │
     │   3. Approve Claim         │                        │
     │                            │                        │
     │                            ├───────────────────────>│
     │                            │ approveClaim()         │
     │                            │ - claimId              │
     │                            │ - status: "approved"   │
     │                            │ - timestamp            │
     │                            │                        │
     │                            │<───────────────────────│
     │<───────────────────────────│ Transaction ID         │
     │   Claim Approved ✓         │ Immutable Record ✓     │
     │                            │                        │
```

---

## 🗄️ DATA STORAGE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                   DATA ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│   MongoDB    │ ← Primary Database
├──────────────┤
│              │
│ Collections: │
│              │
│ • users      │ ← User accounts (admin/user/verifier)
│              │   - name, email, password (hashed)
│              │   - role, walletAddress
│              │
│ • policies   │ ← User-purchased policies (POL-xxx)
│              │   - policyId, userId, coverage
│              │   - status, expiry, familyMembers
│              │
│ • claims     │ ← Submitted claims (CLM-xxx)
│              │   - claimId, policyId, userId
│              │   - status, reason, amount
│              │
│ • policy_    │ ← Admin-created templates (TPL-xxx)
│   templates  │   - templateId, name, coverage
│              │   - durationMonths, description
│              │
│ • notifications │ ← User notifications
│                │   - userId, message, type
│                │
└────────────────┘

┌──────────────┐
│  Algorand    │ ← Blockchain (Immutable)
│  Blockchain  │
├──────────────┤
│              │
│ Smart        │
│ Contract:    │
│              │
│ App ID:      │ 758018952
│ Version:     │ 8 (PyTeal)
│              │
│ Global State:│
│              │
│ • policyId   │ ← Unique policy identifier
│ • wallet     │ ← User's Algorand address
│ • coverage   │ ← Coverage amount
│ • status     │ ← active/inactive
│ • expiry     │ ← Expiration date
│ • claimStatus│ ← pending/approved/rejected
│              │
│ Methods:     │
│ • createPolicy()   │
│ • verifyPolicy()   │
│ • submitClaim()    │
│ • approveClaim()   │
│              │
└──────────────┘

┌──────────────┐
│ IPFS/Local  │ ← Document Storage
│  Storage     │
├──────────────┤
│              │
│ Files:       │
│              │
│ • User       │ ← ID proofs, Aadhar, PAN
│   Documents  │
│              │
│ • Hospital   │ ← Medical bills, reports
│   Bills      │
│              │
│ • Medical    │ ← Prescriptions, test results
│   Reports    │
│              │
│ Format:      │ PDF, Images
│ Encryption:  │ Yes (planned)
│              │
└──────────────┘
```

---

## 🔄 ROLE PERMISSION MATRIX

```
┌─────────────────────────────────────────────────────────────┐
│               ROLE-BASED ACCESS CONTROL                     │
└─────────────────────────────────────────────────────────────┘

Action                      │ Admin │ User  │ Verifier │
──────────────────────────────────────────────────────────
CREATE TEMPLATE             │  ✅   │  ❌   │   ❌     │
VIEW ALL TEMPLATES          │  ✅   │  ❌   │   ❌     │
VIEW ALL POLICIES           │  ✅   │  ❌   │   ❌     │
VIEW ALL USERS              │  ✅   │  ❌   │   ❌     │
VIEW ALL CLAIMS             │  ✅   │  ❌   │   ❌     │
APPROVE/REJECT CLAIM        │  ✅   │  ❌   │   ❌     │
VIEW ANALYTICS              │  ✅   │  ❌   │   ❌     │
CLEAR TEST DATA             │  ✅   │  ❌   │   ❌     │
──────────────────────────────────────────────────────────
BUY POLICY                  │  ❌   │  ✅   │   ❌     │
VIEW MY POLICIES            │  ❌   │  ✅   │   ❌     │
SUBMIT CLAIM                │  ❌   │  ✅   │   ❌     │
ADD FAMILY MEMBER           │  ❌   │  ✅   │   ❌     │
LINK WALLET                 │  ❌   │  ✅   │   ❌     │
VIEW MY NOTIFICATIONS       │  ❌   │  ✅   │   ❌     │
──────────────────────────────────────────────────────────
VERIFY POLICY               │  ❌   │  ❌   │   ✅     │
VIEW POLICY DETAILS         │  ❌   │  ❌   │   ✅     │
CHECK BLOCKCHAIN            │  ❌   │  ❌   │   ✅     │
──────────────────────────────────────────────────────────
```

---

## 📱 USER INTERFACE STRUCTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND PAGES                           │
└─────────────────────────────────────────────────────────────┘

PUBLIC PAGES:
├─ / (Landing Page)
├─ /login
└─ /register

ADMIN DASHBOARD (/dashboard/admin/...):
├─ Overview (stats + clear data button)
├─ Create Template (form)
├─ View Templates (template cards)
├─ View Policies (user policies list)
├─ View Users (users table)
├─ Claims Management (claims table with approve/reject)
└─ Analytics (detailed stats)

USER DASHBOARD (/dashboard/user/...):
├─ Home (stats + notifications)
├─ Buy Policy (form with file upload)
├─ My Policies (policy cards + QR codes)
├─ Family Members (list + add form)
├─ Submit Claim (form with file upload)
├─ Verify Policy (verification form)
└─ Profile (user info + wallet connect)

VERIFIER DASHBOARD (/dashboard/verifier/...):
├─ Verify Policy (policy ID input)
└─ Policy Details (verification results)
```

---

## 🎯 KEY DIFFERENTIATION

```
┌─────────────────────────────────────────────────────────────┐
│          TEMPLATES vs POLICIES vs CLAIMS                    │
└─────────────────────────────────────────────────────────────┘

TEMPLATES (TPL-xxx)
├─ Created by: ADMIN
├─ Purpose: Policy blueprints
├─ Contains: Name, coverage, duration, description
├─ Used for: Users to buy policies from
└─ Example: "Family Health Premium" - ₹5L, 12 months

POLICIES (POL-xxx)
├─ Created by: USER (buying action)
├─ Purpose: Active insurance coverage
├─ Contains: User ID, coverage, family, documents, expiry
├─ Used for: Insurance coverage, claims, verification
└─ Example: POL-1C11F9BBA3 - Rajesh Kumar's active policy

CLAIMS (CLM-xxx)
├─ Created by: USER (claim submission)
├─ Purpose: Reimbursement request
├─ Contains: Policy ID, reason, amount, documents
├─ Processed by: ADMIN (approve/reject)
└─ Example: CLM-69cc1e64126 - Aarav's hospitalization claim
```

---

**PRINT THIS PAGE FOR QUICK REFERENCE! 📄**

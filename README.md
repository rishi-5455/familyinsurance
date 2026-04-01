# Blockchain Enabled Family Insurance Policy Enquiry and Verification System

Production-ready monorepo starter for a role-based insurance platform using Next.js, Flask, Algorand/PyTeal, MongoDB, and IPFS.

## Monorepo Structure

- `frontend/` Next.js + Tailwind client app
- `backend/` Flask REST API
- `blockchain/` PyTeal smart contract and scripts
- `sample-data/` sample JSON records

## Features

- Role-based auth: `admin`, `user`, `verifier`
- JWT session management
- Policy purchase and claim submission
- Admin approval/rejection workflow
- Verifier policy validation with QR support
- Pera Wallet integration
- IPFS file upload for policy/claim documents
- Algorand contract methods for policy lifecycle
- Notification feed for policy and claim updates

## Backend Setup

### MongoDB Setup
1. Install MongoDB locally or use MongoDB Atlas
2. Create database named `family_insurance`
3. No need to create collections - they are created automatically

### IPFS Setup (Optional)

**Option 1: Self-hosted IPFS Kubo**
1. Download IPFS Kubo from https://docs.ipfs.tech/install/command-line/
2. Initialize: `ipfs init`
3. Start daemon: `ipfs daemon`
4. API will be available at `http://localhost:5001`

**Option 2: Pinata/Web3.Storage**
- Use their API endpoints instead of local daemon
- Update `IPFS_API_URL` in `.env`

**Option 3: Development Mode**
- If IPFS is not available, the backend will gracefully degrade
- Document hashes will be simulated with format `ipfs-unavailable-{filename}-{size}`
- This allows development without IPFS dependency

### Backend Installation

1. Open terminal in `backend/`
2. Create env file: copy `.env.example` to `.env` or create with these values:

```env
MONGO_URI=mongodb://localhost:27017/family_insurance
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
IPFS_API_URL=/dns/localhost/tcp/5001/http
ALGORAND_ALGOD_URL=https://testnet-api.algonode.cloud
ALGORAND_ALGOD_TOKEN=
ALGORAND_INDEXER_URL=https://testnet-idx.algonode.cloud
ALGORAND_APP_ID=
ALGORAND_CREATOR_MNEMONIC=
```

3. Install deps:

```bash
pip install -r requirements.txt
```

4. Start Flask API:

```bash
python app.py
```

API base URL: `http://localhost:5000/api`

## Frontend Setup

1. Open terminal in `frontend/`
2. Copy `.env.local.example` to `.env.local`
3. Install deps:

```bash
npm install
```

4. Start frontend:

```bash
npm run dev
```

App URL: `http://localhost:3000`

## Blockchain Setup

### Prerequisites
1. **Get Algorand testnet account**: 
   - Create account at https://testnet.algoexplorer.io/dispenser
   - Fund it with 10+ ALGOs from the dispenser
   - Save your mnemonic phrase

2. **Configure environment**: Add to `backend/.env`:
```
ALGORAND_ALGOD_URL=https://testnet-api.algonode.cloud
ALGORAND_ALGOD_TOKEN=
ALGORAND_INDEXER_URL=https://testnet-idx.algonode.cloud
ALGORAND_CREATOR_MNEMONIC=your 25-word mnemonic phrase here
```

### Deploy Smart Contract

1. Open terminal in `blockchain/`
2. Install deps:

```bash
pip install -r requirements.txt
```

3. Compile contract:

```bash
python scripts/compile_contract.py
```

This creates `build/approval.teal` and `build/clear.teal`

4. Deploy to Algorand testnet:

```bash
python scripts/deploy_contract.py
```

This outputs something like:
```
Contract deployed! App ID: 123456789
```

5. **Update environment files** with the App ID:
   - In `backend/.env`: `ALGORAND_APP_ID=123456789`
   - In `frontend/.env.local`: `NEXT_PUBLIC_ALGORAND_APP_ID=123456789`

### Testing Blockchain Integration

After deployment, test the integration:

1. **Start backend**: `python backend/app.py`
2. **Register a user** via `/api/register`
3. **Login** via `/api/login` (save the JWT token)
4. **Buy a policy** via `/api/user/buy-policy` (includes blockchain sync)
5. **Verify policy** via `/api/verifier/verify-policy/:id` (checks blockchain state)
6. **Submit a claim** via `/api/claims/submit-claim` (writes to blockchain)
7. **Approve claim** via `/api/admin/approve-claim` (updates blockchain)

Each operation will include blockchain transaction results in the API response.

### Simulation Mode (Development)

If you don't set `ALGORAND_CREATOR_MNEMONIC`, the backend will operate in simulation mode:
- Blockchain methods return simulated results
- No actual transactions are sent
- Useful for frontend development without testnet dependency

## Main REST Endpoints

### Auth
- `POST /api/register`
- `POST /api/login`

### User
- `GET /api/user/profile`
- `POST /api/user/family`
- `GET /api/user/policies`
- `POST /api/user/buy-policy`
- `POST /api/user/link-wallet`
- `GET /api/user/notifications`

### Admin
- `POST /api/admin/create-policy`
- `GET /api/admin/users`
- `GET /api/admin/all-policies`
- `POST /api/admin/approve-claim`
- `GET /api/admin/analytics`

### Verifier
- `GET /api/verifier/verify-policy/:id`
- `GET /api/verifier/policy-qr/:id`

### Claims
- `POST /api/claims/submit-claim`
- `GET /api/claims/claim-status/:id`

## Environment Variables

### Backend (`backend/.env`)

- `MONGO_URI`
- `JWT_SECRET_KEY`
- `IPFS_API_URL`
- `ALGORAND_ALGOD_URL`
- `ALGORAND_ALGOD_TOKEN`
- `ALGORAND_INDEXER_URL`
- `ALGORAND_APP_ID`

### Frontend (`frontend/.env.local`)

- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_ALGORAND_NETWORK`
- `NEXT_PUBLIC_ALGORAND_APP_ID`

## Deployment Steps

1. Deploy MongoDB (Atlas or self-hosted).
2. Deploy IPFS node (Pinata/Web3.Storage or self-hosted Kubo API).
3. Deploy Flask backend to Azure App Service / Container Apps.
4. Deploy Next.js frontend to Vercel/Azure Static Web Apps.
5. Compile/deploy Algorand contract; set `ALGORAND_APP_ID` in backend and frontend env.
6. Configure CORS and TLS certs for all environments.
7. Add CI/CD for lint, build, unit/integration tests, and deployment.

## Notes

- This implementation is modular and extensible for production hardening.
- Add stronger validation, rate limiting, audit logs, refresh tokens, and complete blockchain transaction signing flow before go-live.

## Complete Application Flow Testing

### 1. Setup All Services

```bash
# Terminal 1: Start MongoDB (if using local instance)
mongod --dbpath /path/to/data

# Terminal 2: Start IPFS (optional)
ipfs daemon

# Terminal 3: Start Backend
cd backend
python app.py

# Terminal 4: Start Frontend
cd frontend
npm run dev
```

### 2. User Flow Test

**Registration & Login**
1. Navigate to http://localhost:3000
2. Click "Get Started" → "Register"
3. Create account with role "user"
4. Login with credentials

**Policy Purchase**
1. Go to "Buy Policy" from sidebar
2. Connect Pera Wallet (browser extension required)
3. Fill policy details and upload document
4. Submit - blockchain transaction happens automatically
5. Check response for `blockchainResult.txnId`

**View Policies**
1. Go to "My Policies"
2. See purchased policies with QR codes
3. Each policy has blockchain-verified status

**Submit Claim**
1. Go to "Submit Claim"
2. Enter policy ID and claim details
3. Upload evidence documents
4. Submit - claim is written to blockchain

**Verify Policy**
1. Go to "Verify Policy"
2. Scan QR code or enter policy ID
3. See verification status from both database and blockchain

### 3. Admin Flow Test

**Login as Admin**
1. Register with role "admin" or use existing admin account
2. Login

**Create Policy Template**
1. Go to "Create Policy Template"
2. Enter policy details (name, premium, coverage)
3. Submit - template available for users to purchase

**Manage Claims**
1. Go to "Claims Management"
2. Enter claim ID
3. Select Approve/Reject
4. Submit - decision is written to Algorand blockchain
5. Check response for blockchain transaction confirmation

**View Analytics**
1. Dashboard shows total users, policies, claims
2. Analytics page shows detailed statistics

### 4. Verifier Flow Test

**Login as Verifier**
1. Register with role "verifier"
2. Login

**Verify Policy**
1. Enter policy ID or scan QR code
2. See policy details
3. View blockchain verification status
4. Check if policy exists on-chain and matches database

### 5. Blockchain Verification

**Check transactions on Algorand testnet:**
1. After any blockchain operation, copy the `txnId` from API response
2. Visit https://testnet.algoexplorer.io
3. Paste transaction ID to verify on-chain
4. View smart contract state at your `ALGORAND_APP_ID`

### 6. IPFS Verification

**Verify document uploads:**
1. After uploading document, check API response for `ipfsHash`
2. If using local IPFS: Visit `http://localhost:8080/ipfs/{hash}`
3. If using Pinata: Visit their gateway with the hash
4. Confirm document is accessible

## Troubleshooting

**MongoDB Connection Error**
- Ensure MongoDB is running: `mongod --version`
- Check `MONGO_URI` in backend/.env
- Default: `mongodb://localhost:27017/family_insurance`

**IPFS Upload Fails**
- If IPFS daemon not running, app will still work with simulated hashes
- Check IPFS: `ipfs swarm peers`
- Verify API URL: default is `/dns/localhost/tcp/5001/http`

**Blockchain Transaction Fails**
- Verify Algorand account has sufficient testnet ALGOs (need ~1 ALGO)
- Check `ALGORAND_CREATOR_MNEMONIC` is correct 25-word phrase
- Confirm smart contract is deployed: check `ALGORAND_APP_ID`
- If no mnemonic set, app runs in simulation mode (no real transactions)

**Frontend Cannot Connect to Backend**
- Verify backend is running on port 5000
- Check `NEXT_PUBLIC_API_URL` in frontend/.env.local
- CORS is enabled in Flask for http://localhost:3000

**JWT Authentication Errors**
- Clear browser localStorage: `localStorage.clear()`
- Re-login to get fresh token
- Verify `JWT_SECRET_KEY` matches between sessions

**Pera Wallet Not Connecting**
- Install Pera Wallet browser extension
- Create/import Algorand account
- Ensure you're on Algorand testnet in wallet settings

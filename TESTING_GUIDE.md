# 🧪 COMPLETE SYSTEM TESTING GUIDE

**Quick verification checklist to ensure everything works!**

---

## 🚀 STEP 1: Start Backend Server

```powershell
cd backend
python app.py
```

**✅ Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

**Keep this terminal running!**

---

## 🌐 STEP 2: Start Frontend (New Terminal)

```powershell
cd frontend
npm run dev
```

**✅ Expected Output:**
```
- Local:   http://localhost:3000
```

**Keep this terminal running!**

---

## 🧪 STEP 3: Run Automated Backend Tests (New Terminal)

```powershell
cd backend
python tests/test_all_endpoints.py
```

**✅ Expected Result:**
```
Total Tests: 22
Passed: 22
Failed: 0
✅ ALL ENDPOINTS WORKING CORRECTLY
```

---

## 🌍 STEP 4: Test Frontend in Browser

### A. Open Browser
Go to: **http://localhost:3000**

### B. Test Registration Flow

1. **Register as User**
   - Click "Register" or go to `/register`
   - Fill in:
     - Name: `Test User`
     - Email: `user@test.com`
     - Password: `Test@123`
     - Role: `User (Policy Holder)`
   - Click "Register"
   - **✅ Expected**: Redirected to login page

2. **Login as User**
   - Email: `user@test.com`
   - Password: `Test@123`
   - **✅ Expected**: Redirected to `/dashboard/user`

### C. Test User Features

**While logged in as User:**

1. **View Profile**
   - Go to "Profile" from sidebar
   - **✅ Expected**: See your profile details

2. **Add Family Member**
   - Go to "Family Members"
   - Add member: Name: `Jane Doe`, Age: `28`, Relation: `spouse`
   - **✅ Expected**: "Family member added successfully!"

3. **Connect Wallet** (Optional - requires Pera Wallet extension)
   - Go to "Profile"
   - Click "Connect Wallet"
   - **✅ Expected**: Wallet address appears

4. **Buy Policy**
   - Go to "Buy Policy"
   - Fill in:
     - Coverage: `50000`
     - Duration: `12`
     - Wallet Address: `ALGO123TEST`
   - Upload a test file (any PDF or text file)
   - Click "Submit"
   - **✅ Expected**: "Policy created: POL-XXXXXX"

5. **View My Policies**
   - Go to "My Policies"
   - **✅ Expected**: See the policy you just created

6. **Submit Claim**
   - Go to "Submit Claim"
   - Enter Policy ID from your policy
   - Add reason: `Medical emergency`
   - Upload document
   - **✅ Expected**: "Claim submitted: CLM-XXXXXX"

### D. Test Admin Features

1. **Logout** (if logged in as user)

2. **Register as Admin**
   - Go to `/register`
   - Name: `Admin User`
   - Email: `admin@test.com`
   - Password: `Admin@123`
   - Role: `Admin (Insurance Company)`

3. **Login as Admin**
   - **✅ Expected**: Redirected to `/dashboard/admin`

4. **View Analytics**
   - Go to "Analytics"
   - **✅ Expected**: See stats (users, policies, claims)

5. **View All Users**
   - Go to "View Users"
   - **✅ Expected**: See registered users list

6. **View All Policies**
   - Go to "View Policies"
   - **✅ Expected**: See all created policies

7. **Create Policy Template**
   - Go to "Create Policy"
   - Fill in:
     - Name: `Health Insurance Basic`
     - Coverage: `100000`
     - Duration: `12`
     - Description: `Basic health coverage`
   - **✅ Expected**: "Template created: TPL-XXXXXX"

8. **Manage Claims**
   - Go to "Claims Management"
   - **✅ Expected**: See submitted claims
   - Click "Approve" or "Reject" on a claim
   - **✅ Expected**: Claim status updates

### E. Test Verifier Features

1. **Logout**

2. **Register as Verifier**
   - Email: `verifier@test.com`
   - Role: `Verifier (Hospital)`

3. **Login as Verifier**
   - **✅ Expected**: Redirected to `/dashboard/verifier`

4. **Verify Policy**
   - Enter a Policy ID from earlier
   - Click "Verify"
   - **✅ Expected**: See verification status with blockchain data

---

## 🤖 STEP 5: Test Blockchain Integration

```powershell
cd blockchain
python scripts/deploy_contract.py
```

**✅ Expected Output:**
```
✓ Smart contract deployed successfully
App ID: 758018952
Transaction confirmed
```

**This verifies:**
- ✅ Algorand connection working
- ✅ Smart contract deployment working
- ✅ Blockchain integration active

---

## 📊 QUICK HEALTH CHECKS

### Backend Health Check
```powershell
curl http://localhost:5000/api/health
```
**✅ Expected**: `{"status":"ok"}`

### Check MongoDB Connection
```powershell
mongo
use B-Insurance_Policy
db.users.count()
```
**✅ Expected**: Shows number of users

### Check Environment Variables
```powershell
cd backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✓ JWT_SECRET:', 'SET' if os.getenv('JWT_SECRET') else 'MISSING'); print('✓ MONGO_URI:', 'SET' if os.getenv('MONGO_URI') else 'MISSING'); print('✓ ALGORAND_APP_ID:', os.getenv('ALGORAND_APP_ID'))"
```

---

## 🐛 TROUBLESHOOTING

### Backend won't start?
```powershell
# Check if MongoDB is running
mongod --version

# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start?
```powershell
# Check Node version
node --version  # Should be 16+

# Reinstall dependencies
rm -rf node_modules
npm install
```

### Tests failing?
```powershell
# Make sure backend is running first!
cd backend
python app.py

# Then run tests in NEW terminal
python tests/test_all_endpoints.py
```

### Database issues?
```powershell
# Check MongoDB is running
mongo --eval "db.adminCommand('ping')"

# Reset database (CAUTION: Deletes all data!)
mongo B-Insurance_Policy --eval "db.dropDatabase()"
```

---

## ✅ FINAL VERIFICATION CHECKLIST

Use this checklist to confirm everything works:

### Backend (API)
- [ ] Backend server starts without errors
- [ ] Health endpoint responds: `GET /api/health`
- [ ] All 22 endpoint tests pass
- [ ] MongoDB connected

### Frontend (UI)
- [ ] Frontend loads at http://localhost:3000
- [ ] Can register new users
- [ ] Can login with credentials
- [ ] Can navigate between pages
- [ ] Forms submit successfully

### User Features
- [ ] Can view profile
- [ ] Can add family members
- [ ] Can buy policy
- [ ] Can view policies
- [ ] Can submit claims
- [ ] Can view notifications

### Admin Features
- [ ] Can view analytics
- [ ] Can view all users
- [ ] Can view all policies
- [ ] Can create policy templates
- [ ] Can approve/reject claims

### Verifier Features
- [ ] Can verify policies
- [ ] Can view policy QR codes

### Blockchain
- [ ] Smart contract deployed
- [ ] Blockchain transactions working
- [ ] Policy sync to blockchain
- [ ] Claim submission to blockchain

### Integration
- [ ] JWT authentication working
- [ ] Role-based access control working
- [ ] File uploads working
- [ ] Notifications created
- [ ] IPFS integration (or fallback working)

---

## 🎉 ALL WORKING?

If all checkboxes are ✅, congratulations! Your system is fully operational and production-ready!

### Quick Test Command
```powershell
# One command to test everything (backend must be running)
cd backend; python tests/test_all_endpoints.py; python tests/test_file_uploads.py
```

---

## 📞 NEED HELP?

- Check backend logs in the terminal running `python app.py`
- Check frontend console in browser DevTools (F12)
- Check MongoDB: `mongo B-Insurance_Policy`
- Review documentation: `ENDPOINTS_FIXED_REPORT.md`

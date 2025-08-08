# Deployment Guide for Carro Backend

## Option 1: Deploy with SQLite (Easiest)

### Railway Deployment (Recommended)
1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up/Login with GitHub
   - Click "Deploy from GitHub repo"
   - Select your `carro-backend` repository
   - Railway will automatically detect Python and deploy

3. **Set Environment Variables**
   - In Railway dashboard, go to your project
   - Go to Variables tab
   - Add:
     ```
     DATABASE_URL=sqlite+aiosqlite:///./carro.db
     SECRET_KEY=your-super-secret-production-key-here
     ```

4. **Initialize Database**
   - After deployment, go to Railway dashboard
   - Open the "Deployments" tab
   - Run the init script via Railway's console or add it to your deployment

### Alternative: Render.com
1. **Connect GitHub repo to Render**
2. **Create Web Service**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. **Set Environment Variables** (same as Railway)

---

## Option 2: Deploy with PostgreSQL (Production-Ready)

### Railway with PostgreSQL
1. **Deploy on Railway** (same as above)
2. **Add PostgreSQL Database**
   - In Railway project, click "Add Service"
   - Select "PostgreSQL"
   - Railway will create database and provide `DATABASE_URL`
3. **Update Environment Variables**
   - Remove the SQLite DATABASE_URL
   - Railway automatically provides PostgreSQL DATABASE_URL
4. **Update requirements.txt**
   ```bash
   pip install asyncpg
   pip freeze > requirements.txt
   ```

### Heroku Deployment
1. **Install Heroku CLI**
2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:hobby-dev
   ```
3. **Deploy**
   ```bash
   git push heroku main
   ```

---

## Required Files for Deployment

✅ **Procfile** - Already created
✅ **requirements.txt** - Update with:
```bash
pip freeze > requirements.txt
```

✅ **Dockerfile** - Already created (for container deployment)
✅ **railway.toml** - Already created (Railway config)
✅ **.env.example** - Already created (environment template)

---

## Database Migration for PostgreSQL

If you choose PostgreSQL, update your `.env`:

```env
# Change from:
DATABASE_URL=sqlite+aiosqlite:///./carro.db

# To (Railway will provide this automatically):
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
```

**Install PostgreSQL dependencies:**
```bash
pip install asyncpg
pip freeze > requirements.txt
```

**Your init_db.py will work with both SQLite and PostgreSQL!**

---

## Cost Comparison

### SQLite Deployment
- **Railway**: Free tier available, $5/month for hobby
- **Render**: Free tier available
- **Fly.io**: Free tier available

### PostgreSQL Deployment  
- **Railway**: $5/month (includes PostgreSQL)
- **Heroku**: $5/month for hobby PostgreSQL
- **Supabase**: Free tier, then $25/month

---

## Recommendation

**For MVP/Testing**: Start with SQLite on Railway
**For Production**: Use PostgreSQL on Railway

Your app is already configured to handle both! Just change the `DATABASE_URL` environment variable.

---

## Next Steps

1. **Choose deployment option**
2. **Push code to GitHub**
3. **Deploy on Railway/Render**
4. **Set environment variables**
5. **Test your deployed API**

Your API endpoints will be available at:
- `https://your-app.railway.app/api/vehicles`
- `https://your-app.railway.app/auth/register`
- `https://your-app.railway.app/docs` (API documentation)

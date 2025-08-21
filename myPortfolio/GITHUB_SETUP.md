# GitHub API Setup Guide

This guide explains how to set up and use the GitHub API functionality in your portfolio application.

## 🚀 **Quick Setup**

### 1. **Environment Variables**
Add your GitHub username to your `.env` file:

```bash
# .env
GITHUB_USERNAME=your_github_username
```

### 2. **Backend Endpoints**
The application provides three GitHub API endpoints:

- **`/api/github/repos`** - Fetch user repositories
- **`/api/github/user`** - Fetch user profile information  
- **`/api/github/stats`** - Fetch comprehensive statistics

### 3. **Frontend Integration**
The GitHub repositories are displayed on the homepage when you click the "GitHub Repos" button.

## 🔧 **Configuration**

### **Required Environment Variables**
```bash
GITHUB_USERNAME=your_actual_github_username
```

### **Optional Environment Variables**
```bash
# For enhanced GitHub API access (if you have a personal access token)
GITHUB_TOKEN=your_personal_access_token
```

## 📱 **How It Works**

### **1. User Clicks GitHub Repos Button**
- Button is located in the hero section of the homepage
- Clicking triggers an AJAX request to `/api/github/repos`

### **2. Backend Fetches Data**
- Flask backend makes a request to GitHub's public API
- Uses your configured username to fetch repositories
- Returns formatted JSON data

### **3. Frontend Displays Results**
- Repositories are displayed as Bootstrap cards
- Shows repository name, description, language, stars, forks, etc.
- Each card links to the actual GitHub repository

## 🧪 **Testing**

### **Test Page**
Visit `/github-test.html` to test all GitHub API endpoints:

1. **Test GitHub API** - Tests the repositories endpoint
2. **Test User Endpoint** - Tests the user profile endpoint  
3. **Test Stats Endpoint** - Tests the statistics endpoint

### **Console Logging**
Check your browser's developer console for detailed logging:
- API request details
- Response data
- Error messages

## 🐛 **Troubleshooting**

### **Common Issues**

#### **1. "GitHub username not configured"**
- **Solution**: Set `GITHUB_USERNAME` in your `.env` file
- **Example**: `GITHUB_USERNAME=johndoe`

#### **2. "GitHub user not found"**
- **Solution**: Verify your GitHub username is correct
- **Check**: Visit `https://github.com/yourusername` in your browser

#### **3. "Rate limit exceeded"**
- **Solution**: Wait a few minutes and try again
- **Note**: GitHub's public API has rate limits for unauthenticated requests

#### **4. "Network error"**
- **Solution**: Check your internet connection
- **Check**: Ensure your Flask backend is running

### **Debug Steps**

1. **Check Environment Variables**
   ```bash
   # In your terminal
   echo $GITHUB_USERNAME
   ```

2. **Test Backend Directly**
   ```bash
   # Test the API endpoint
   curl http://localhost:5000/api/github/repos
   ```

3. **Check Flask Logs**
   - Look for error messages in your Flask console
   - Check for GitHub API response errors

4. **Use Test Page**
   - Visit `/github-test.html`
   - Test each endpoint individually
   - Check detailed error messages

## 📊 **API Response Format**

### **Repositories Endpoint** (`/api/github/repos`)
```json
[
  {
    "id": 123456789,
    "name": "portfolio-app",
    "description": "My personal portfolio application",
    "html_url": "https://github.com/username/portfolio-app",
    "language": "Python",
    "stargazers_count": 5,
    "forks_count": 2,
    "watchers_count": 3,
    "fork": false,
    "archived": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-15T00:00:00Z"
  }
]
```

### **User Endpoint** (`/api/github/user`)
```json
{
  "login": "username",
  "name": "John Doe",
  "bio": "Full-stack developer",
  "public_repos": 25,
  "followers": 100,
  "following": 50,
  "avatar_url": "https://avatars.githubusercontent.com/...",
  "html_url": "https://github.com/username"
}
```

### **Stats Endpoint** (`/api/github/stats`)
```json
{
  "user": { ... },
  "repositories": {
    "total": 25,
    "total_stars": 150,
    "total_forks": 30,
    "average_stars": 6.0
  },
  "top_languages": [
    ["Python", 10],
    ["JavaScript", 8],
    ["HTML", 5]
  ],
  "top_starred": [ ... ],
  "recent_repos": [ ... ]
}
```

## 🔒 **Security Notes**

- **Public API**: Uses GitHub's public API (no authentication required)
- **Rate Limiting**: Subject to GitHub's public API rate limits
- **User-Agent**: Includes proper User-Agent header to avoid blocking
- **Error Handling**: Comprehensive error handling for various failure scenarios

## 🚀 **Deployment**

### **Railway.app**
1. Set `GITHUB_USERNAME` in your Railway environment variables
2. Deploy your application
3. Test the GitHub functionality

### **Local Development**
1. Create `.env` file with your GitHub username
2. Run Flask application
3. Test locally before deploying

## 📝 **Customization**

### **Modify Repository Display**
Edit `frontend/assets/main.js` to change how repositories are displayed:

```javascript
// Customize repository card rendering
container.innerHTML = repos.map((r, index) => `
  <div class="col-lg-4 col-md-6">
    <div class="card">
      <div class="card-body">
        <h5>${r.name}</h5>
        <p>${r.description || 'No description'}</p>
        <!-- Add your custom fields here -->
      </div>
    </div>
  </div>
`).join('');
```

### **Add More GitHub Data**
Extend the backend to fetch additional GitHub information:
- Repository topics
- Commit history
- Issue statistics
- Pull request data

## 🆘 **Need Help?**

If you encounter issues:

1. **Check the test page** (`/github-test.html`)
2. **Review console logs** in your browser
3. **Check Flask backend logs**
4. **Verify environment variables**
5. **Test API endpoints directly**

The GitHub functionality is designed to be robust and provide clear error messages to help with troubleshooting.

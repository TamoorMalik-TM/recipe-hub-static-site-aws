
# Recipe Hub Frontend

Static frontend for Recipe Hub. Intended to be hosted on S3 + CloudFront.

## Files

- `index.html` – list/search recipes
- `recipe.html` – recipe details + rating
- `login.html` – login page
- `create.html` – create new recipe
- `style.css` – basic styling
- `config.js` – set `API_BASE_URL` to your backend (e.g. ALB URL)
- `main.js`, `auth.js`, `create.js`, `recipe.js` – page logic

## Usage

1. Set your backend API URL in `config.js`:

```js
const API_BASE_URL = "https://your-alb-dns-name";
```

2. Upload all files in this folder to your S3 static website bucket.
3. Configure CloudFront to point to the S3 bucket.

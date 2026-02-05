import html
import secrets
import argparse
import random
import hashlib
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# --- Data Stores ---
users = {} 
posts = []

# --- Helpers ---
def generate_avatar_color(username):
    """Generate a consistent neon color based on username hash."""
    hash_object = hashlib.md5(username.encode())
    # Use the hash to pick a hue
    hue = int(hash_object.hexdigest(), 16) % 360
    return f"hsl({hue}, 80%, 60%)"

def time_ago(dt):
    """Convert datetime to 'X minutes ago' string."""
    now = datetime.now()
    diff = now - dt
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "Just now"
    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)}m ago"
    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)}h ago"
    days = hours / 24
    return f"{int(days)}d ago"

app.jinja_env.filters['time_ago'] = time_ago

# --- Dummy Data Generation ---
def init_dummy_data():
    dummy_users = [
        ('ZeroCool', 'hacktheplanet', 'Admin'),
        ('AcidBurn', 'crashoverride', 'VIP'),
        ('Morpheus', 'bluepill', 'VIP'),
        ('Trinity', 'nmap', 'User'),
        ('Neo', 'knockknock', 'User'),
        ('Cypher', 'steak', 'User'),
        ('Switch', 'notlikethis', 'User'),
        ('Tank', 'operator', 'User'),
        ('Dozer', 'realworld', 'User'),
        ('Mouse', 'tastywheat', 'User')
    ]
    
    for username, pwd, role in dummy_users:
        users[username] = {
            'username': username,
            'password': pwd, 
            'alias': username,  # Default alias
            'role': role,
            'avatar_color': generate_avatar_color(username),
            'joined': datetime.now() - timedelta(days=random.randint(1, 365))
        }

    # Realistic threads
    threads = [
        ('ZeroCool', "New 0-day in Kernal.sys??", "Anyone seen the new CVE-2077-9001? Looks like heap overflow in the mainframe access layer. Messing with the stack pointers triggers a segfault but I think RCE is possible if we groom the heap correctly."),
        ('Morpheus', "The signal is getting stronger", "We are monitoring increased activity on port 443 across the grid. Something big is coming. Verify your GPG keys."),
        ('AcidBurn', "TrashFile cleanup script release", "Just dropped a new python script to scrub logs. Check it out on the repo. It uses advanced overwriting passes. <br><br><code>rm -rf /trace/logs/*</code>"),
        ('Neo', "Strange pattern in the static", "I keep seeing this sequence: 0010110 in the raw packet dumps. Is it a signature?"),
        ('Cypher', "Best virtual steak house in Sector 7?", "Tired of the nutrient goop. Need recommendations."),
        ('Trinity', "Nmap scan results for target 192.168.0.x", "Found open ports: 22, 80, 8080. SSH seems vulnerable to brute force."),
        ('Switch', "Anyone got a spare deck?", "Mine fried during the last run. Need a Gibson 5000 equivalent."),
        ('Mouse', "Did you know...", "That the machines actually designed the mouse pointer? Irony."),
        ('Tank', "Operator status: GREEN", "Connection stable. Upload speeds nominal. ready for extraction."),
        ('Dozer', "Real world food > sim food", "Fight me.")
    ]

    for i, (username, title, content) in enumerate(threads):
        post_time = datetime.now() - timedelta(minutes=random.randint(5, 5000))
        new_post = {
            'id': i + 1,
            'username': username,
            'alias': users[username]['alias'], # Initial alias
            'role': users[username]['role'],
            'avatar_color': users[username]['avatar_color'],
            'title': title,
            'content': content, # Pre-escaped or safe HTML allowed for dummy data? Let's assume dummy data is safe or manually html.escaped if it was user input. Since it's server side string, we trust it or escape it.
            'likes': [random.choice(list(users.keys())) for _ in range(random.randint(0, 10))],
            'comments': [],
            'views': random.randint(50, 5000),
            'timestamp': post_time
        }
        
        # Add random comments
        num_comments = random.randint(0, 5)
        for _ in range(num_comments):
             commenter = random.choice(list(users.keys()))
             new_post['comments'].append({
                 'username': commenter,
                 'alias': users[commenter]['alias'],
                 'role': users[commenter]['role'],
                 'avatar_color': users[commenter]['avatar_color'],
                 'content': random.choice(["Agreed.", "Check your sources.", "FUD.", "Interesting.", "Patched already.", "lol", "nice find"]),
                 'timestamp': post_time + timedelta(minutes=random.randint(1, 60))
             })
        
        posts.append(new_post)

# Initialize data
init_dummy_data()

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        username = html.escape(request.form.get('username'))
        password = request.form.get('password')

        if action == 'register':
            if username in users:
                flash('Username already exists!', 'error')
            else:
                users[username] = {
                    'username': username,
                    'password': password, 
                    'alias': username,
                    'role': 'User',
                    'avatar_color': generate_avatar_color(username),
                    'joined': datetime.now()
                }
                flash('Registration successful! Please login.', 'success')
        
        elif action == 'login':
            user = users.get(username)
            if user and user['password'] == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash('Access Denied: Invalid Credentials', 'error')
    
    return render_template('index.html', page='login')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    current_user = users[session['username']]
    # Sort posts by new
    sorted_posts = sorted(posts, key=lambda x: x['timestamp'], reverse=True)
    
    # Calculation for widgets
    online_count = random.randint(users.__len__(), users.__len__() * 3)
    trending_tags = ['#exploit', '#zero-day', '#crypto', '#cyberdeck', '#netsec']
    
    return render_template('index.html', 
                           page='dashboard', 
                           user=current_user, 
                           posts=sorted_posts,
                           online_count=online_count,
                           trending_tags=trending_tags)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/post', methods=['POST'])
def create_post():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    content = request.form.get('content')
    title = request.form.get('title')
    
    if content and title:
        # HARDENING: Escape post content
        safe_content = html.escape(content)
        safe_title = html.escape(title)
        
        user = users[session['username']]
        
        new_post = {
            'id': len(posts) + 1,
            'username': session['username'],
            'alias': user['alias'],
            'role': user['role'],
            'avatar_color': user['avatar_color'],
            'title': safe_title,
            'content': safe_content,
            'likes': [],
            'comments': [],
            'views': 0,
            'timestamp': datetime.now()
        }
        posts.append(new_post)
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'username' not in session:
        return redirect(url_for('index'))
    
    post = next((p for p in posts if p['id'] == post_id), None)
    # Allow admin to delete strictly, or just owner
    if post and (post['username'] == session['username'] or users[session['username']].get('role') == 'Admin'):
        posts.remove(post)
    
    return redirect(url_for('dashboard'))

@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    if 'username' not in session:
        return redirect(url_for('index'))

    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        username = session['username']
        if username in post['likes']:
            post['likes'].remove(username)
        else:
            post['likes'].append(username)
            
    return redirect(url_for('dashboard'))

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment_post(post_id):
    if 'username' not in session:
        return redirect(url_for('index'))
        
    content = request.form.get('content')
    if content:
        # HARDENING: Escape comment content
        safe_content = html.escape(content)
        user = users[session['username']]
        
        post = next((p for p in posts if p['id'] == post_id), None)
        if post:
            post['comments'].append({
                'username': session['username'],
                'alias': user['alias'],
                'role': user['role'],
                'avatar_color': user['avatar_color'],
                'content': safe_content,
                'timestamp': datetime.now()
            })
            
    return redirect(url_for('dashboard'))

@app.route('/profile', methods=['POST'])
def update_profile():
    if 'username' not in session:
        return redirect(url_for('index'))
        
    new_alias = request.form.get('alias')
    if new_alias:
        # VULNERABILITY: No escaping for alias!
        users[session['username']]['alias'] = new_alias
        
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Antigravity Forum CTF Lab')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()
    
    print(f"[*] System initialized. Listening on port {args.port}...")
    app.run(host='0.0.0.0', port=args.port, debug=True)

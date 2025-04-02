import pandas as pd
import streamlit as st

# Function to Set Background Image with Gradient Overlay
def set_background(image_url):
    background_css = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url("{image_url}") no-repeat center center fixed;
        background-size: cover;
    }}
    .content-box {{
        background: rgba(0, 0, 0, 0.8);  
        padding: 30px;
        border-radius: 15px;
        width: 80%;
        margin: auto;
        text-align: center;
        color: white;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }}
    .profile-pic {{
        border-radius: 50%;
        width: 120px;
        height: 120px;
        object-fit: cover;
        border: 3px solid #1DB954;
        display: block;
        margin: auto;
    }}
    h1, h2, h3, p {{
        color: white !important;
        text-align: center;
    }}
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

# Set Background with a Spotify-Themed Image
set_background("https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg")

# Initialize session state for profile submission tracking
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "profile_pic" not in st.session_state:
    st.session_state.profile_pic = None

if "user_name" not in st.session_state:
    st.session_state.user_name = "New User"

if "user_age" not in st.session_state:
    st.session_state.user_age = 18

if "fav_genres" not in st.session_state:
    st.session_state.fav_genres = []

# **Determine User Name for Greeting**
user_display_name = st.session_state.user_name if st.session_state.submitted else "New User"

# **Sidebar Behavior - Profile Setup or Display Profile**
if not st.session_state.submitted:
    st.sidebar.markdown("## 👤 Set Up Your Profile")

    # Upload Profile Picture
    profile_pic = st.sidebar.file_uploader("Upload a Profile Picture", type=["png", "jpg", "jpeg"])
    
    # User Name Input
    user_name = st.sidebar.text_input("Enter Your Name", placeholder="New User")

    # Age Slider
    user_age = st.sidebar.slider("Select Your Age", min_value=13, max_value=100, value=18)

    # Favorite Genre Selection (Multi-select)
    genres = ["Pop", "Rock", "Hip-Hop", "Jazz", "Classical", "Electronic", "R&B", "Country"]
    fav_genres = st.sidebar.multiselect("Choose Your Favorite Genres", genres)

    # Submit Profile Button
    if st.sidebar.button("Save Profile"):
        st.session_state.submitted = True
        st.session_state.profile_pic = profile_pic
        st.session_state.user_name = user_name if user_name else "New User"
        st.session_state.user_age = user_age
        st.session_state.fav_genres = fav_genres if fav_genres else ["Not Set"]

# **Spotify-Style Sidebar After Submission**
else:
    st.sidebar.markdown('<div style="text-align:center;">', unsafe_allow_html=True)

    # Profile Picture
    if st.session_state.profile_pic:
        st.sidebar.image(st.session_state.profile_pic, width=120)
    else:
        st.sidebar.markdown(
            '<img class="profile-pic" src="https://cdn-icons-png.flaticon.com/512/149/149071.png">',
            unsafe_allow_html=True
        )

    # User Information
    st.sidebar.markdown(f"### {st.session_state.user_name}")
    st.sidebar.markdown(f"🎂 **Age:** {st.session_state.user_age}")
    st.sidebar.markdown(f"🎵 **Favorite Genres:** {', '.join(st.session_state.fav_genres)}")

    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    # Sidebar Menu (Like Spotify)
    if st.sidebar.button("🎶 My Playlists"):
        st.sidebar.markdown("🔹 *Coming Soon!*")

    if st.sidebar.button("⚙️ Settings"):
        st.sidebar.markdown("🔹 *Settings will be available soon!*")

    if st.sidebar.button("🔄 Edit Profile"):
        st.session_state.submitted = False

    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# **Main Section with Personalized Greeting**
st.markdown(f"# 🎵 Welcome back, {user_display_name}!")

# Create a Container for Content Overlay
st.markdown('<div class="content-box">', unsafe_allow_html=True)

# App Title and Description
st.markdown("### Relive the Music from Your High School Days!")
st.markdown("Select a year range and find a **pre-made Spotify playlist** with all the top songs from that period.")
st.markdown("Select a year range and find a **pre-made Spotify playlist** with all the top songs from that period.")

# Load Playlist Data
df = pd.read_csv("playlists.csv")
years = list(range(1958, 2022))

# Select Year Range
st.markdown("### 📅 Select Your High School Years")
year_range = st.slider(label="Choose a range of years", min_value=1958, max_value=2022, value=(1995, 2010))

# Generate Playlist on Button Click
st.markdown("<br>", unsafe_allow_html=True)  # Add some space
if st.button(f'🎧 {user_display_name}, Get Your Playlist'):
    if year_range[0] == year_range[1]:
        playlist_name = f"Top US Singles: {year_range[0]}"
    else:
        playlist_name = f"Top US Singles: {year_range[0]}-{year_range[1]}"

    if df[df['name'] == playlist_name].shape[0] > 0:
        playlist = df[df['name'] == playlist_name].to_dict(orient='records')[0]
        link = f"### 🎶 Your Spotify Playlist: [{playlist['name']}]({playlist['link']})"
        st.markdown(link, unsafe_allow_html=True)
    else:
        st.markdown(f"❌ *Oops, {user_display_name}! We don't have that playlist yet. Try selecting a narrower year range.*")

# Close the content box div
st.markdown('</div>', unsafe_allow_html=True)

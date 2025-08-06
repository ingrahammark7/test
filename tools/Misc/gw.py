#!/bin/bash

root_dir="teen_diary_time_capsule"
mkdir -p "$root_dir"

# Common CSS with blinking text and typical styles
read -r -d '' COMMON_CSS <<'EOF'
@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0; }
  100% { opacity: 1; }
}
.blink {
  animation: blink 1.5s infinite;
  color: #ff66cc;
  font-weight: bold;
}
body {
  background-color: #000022;
  color: #eeeeff;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  margin: 0; padding: 10px;
}
a { color: #88aaff; text-decoration: none; }
a:hover { text-decoration: underline; }
header {
  text-align: center;
  padding: 20px;
  font-size: 2.5em;
  font-weight: bold;
  letter-spacing: 2px;
}
nav {
  margin: 20px auto;
  text-align: center;
}
nav a {
  margin: 0 15px;
  font-size: 1.2em;
}
.content {
  max-width: 700px;
  margin: 0 auto;
  background: #111144;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 20px #224488;
}
footer {
  margin-top: 40px;
  text-align: center;
  font-size: 0.9em;
  color: #666699;
}
.visitor-counter {
  font-size: 0.8em;
  margin-top: 10px;
  color: #8888bb;
}
.entry-title {
  font-size: 2em;
  margin-bottom: 10px;
  text-align: center;
  font-weight: bold;
  text-shadow: 1px 1px 2px #222266;
}
.date {
  font-size: 1em;
  text-align: center;
  color: #9999cc;
  margin-bottom: 20px;
}
.entry-content {
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6em;
}
.song-lyrics {
  font-style: italic;
  color: #aaaaee;
  margin-top: 30px;
  border-top: 1px solid #444488;
  padding-top: 15px;
}
.under-construction {
  color: #ff6666;
  font-weight: bold;
  font-size: 1.2em;
  text-align: center;
  margin: 20px 0;
}
.glitter {
  font-weight: bold;
  color: #ff66cc;
  text-shadow: 0 0 8px #ff66cc;
}
EOF

echo "$COMMON_CSS" > "$root_dir/style.css"

# Animated GIF placeholder (static image for simplicity)
read -r -d '' GLITTER_GIF <<'EOF'
<img src="https://upload.wikimedia.org/wikipedia/commons/6/65/Animated_glitter_stars.gif" alt="glitter" style="width:40px;vertical-align:middle;">
EOF

create_site () {
  site_name=$1
  site_title=$2
  author_name=$3
  entry1_title=$4
  entry1_date=$5
  entry1_content=$6
  entry2_title=$7
  entry2_date=$8
  entry2_content=$9
  entry3_title=${10}
  entry3_date=${11}
  entry3_content=${12}

  site_dir="$root_dir/$site_name"
  mkdir -p "$site_dir/entries"

  # index.html with blinking welcome and glitter gifs
  cat > "$site_dir/index.html" <<EOF
<!DOCTYPE html>
<html>
<head>
  <title>$site_title</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <header>$site_title $GLITTER_GIF</header>
  <nav>
    <a href="index.html">Home</a> | 
    <a href="entries/${entry1_date}.html">Diary</a> | 
    <a href="about.html">About Me</a> | 
    <a href="guestbook.html">Guestbook</a>
  </nav>
  <div class="content">
    <h2 class="blink">Welcome to my site!</h2>
    <p>Hi! I'm $author_name. This is my personal diary and creative space. Thanks for visiting! $GLITTER_GIF</p>
    
    <h3>Latest Diary Entries</h3>
    <ul>
      <li><a href="entries/${entry1_date}.html">$entry1_date — $entry1_title</a></li>
      <li><a href="entries/${entry2_date}.html">$entry2_date — $entry2_title</a></li>
      <li><a href="entries/${entry3_date}.html">$entry3_date — $entry3_title</a></li>
    </ul>
    
    <div class="visitor-counter">
      You are visitor #1,234
    </div>
  </div>
  <footer>
    &copy; 2003 $author_name. Site designed by me with lots of love and glitter gifs. $GLITTER_GIF
  </footer>
</body>
</html>
EOF

  # diary entries with under construction note on second entry for nostalgia
  for i in 1 2 3; do
    eval title=\${entry${i}_title}
    eval date=\${entry${i}_date}
    eval content=\${entry${i}_content}

    under_construction=""
    if [ $i -eq 2 ]; then
      under_construction="<div class='under-construction'>Page under construction! Please check back soon.</div>"
    fi

    cat > "$site_dir/entries/$date.html" <<EOF
<!DOCTYPE html>
<html>
<head>
  <title>Diary Entry: $date — $title</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <div class="entry-title">$title</div>
  <div class="date">$date</div>
  <div class="entry-content">
    $content
    $under_construction
  </div>
  <p><a href="../index.html">Back to home</a></p>
</body>
</html>
EOF
  done

  # about.html with blinking text
  cat > "$site_dir/about.html" <<EOF
<!DOCTYPE html>
<html>
<head>
  <title>About Me — $site_title</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>About Me</header>
  <div class="content">
    <p>Hi, I'm <span class="glitter">$author_name</span>, a 16-year-old who loves writing, music, and dreaming big.</p>
    <p>This site is my little corner of the internet where I share my thoughts and feelings.</p>
  </div>
  <p><a href="index.html">Back to home</a></p>
</body>
</html>
EOF

  # guestbook.html placeholder with blinking warning
  cat > "$site_dir/guestbook.html" <<EOF
<!DOCTYPE html>
<html>
<head>
  <title>Guestbook — $site_title</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>Guestbook</header>
  <div class="content">
    <p class="blink">Guestbook under construction. Please leave a message!</p>
    <p>This is a guestbook placeholder — imagine visitors leaving heartfelt messages here!</p>
  </div>
  <p><a href="index.html">Back to home</a></p>
</body>
</html>
EOF
}

# Sites data

create_site "midnightskies.com" "Midnight Skies" "Luna" \
  "Rainy days and lost dreams" "march10_2003" "<p>It's been raining all day, and everything feels so gray. School is such a drag lately — like I’m stuck in a loop I can’t break out of.</p><p>Sometimes I wonder if anyone really gets me or if I’m just talking to myself through these pages.</p><p>Mom’s been on my case about grades again, and I’m so tired of pretending I care.</p><p>I wish I could just run away — maybe to the beach where no one knows my name.</p>" \
  "School blues" "march05_2003" "<p>School's just so hard right now. I feel invisible in all my classes.</p><p>Everyone seems to have their lives together but me.</p>" \
  "Sometimes I just want to disappear" "feb28_2003" "<p>Some days I just want to disappear and be forgotten.</p><p>Maybe someday things will get better, but right now it feels hopeless.</p>"

create_site "awkwardgirl.net" "Awkward Girl" "Emily" \
  "First day of school" "sept01_2002" "<p>Today was my first day at the new high school. I felt so out of place.</p><p>Everyone looked like they already had their groups, and I was just lost.</p>" \
  "Crush confessions" "aug15_2002" "<p>I think I like Jason from my math class. But I’m too shy to talk to him.</p><p>Why is liking someone so hard?</p>" \
  "Lonely nights" "aug01_2002" "<p>It’s hard being lonely, but sometimes it feels like no one understands me.</p><p>I write here to feel less alone.</p>"

create_site "starcrossedlover.org" "Starcrossed Lover" "Jade" \
  "Broken hearts and poetry" "oct20_2003" "<p>My heart hurts, but poetry helps me cope.</p><p>Here’s a poem I wrote tonight about lost love.</p>" \
  "Waiting for you" "oct10_2003" "<p>Waiting feels endless when you don’t know if someone cares.</p><p>Maybe one day you’ll read this and understand.</p>" \
  "Midnight thoughts" "sept30_2003" "<p>When the world sleeps, my mind races with a thousand thoughts.</p><p>I wish I could turn them all into songs.</p>"

create_site "emoheart.net" "Emo Heart" "Kelsey" \
  "Dark days and heavy hearts" "nov15_2002" "<p>Some days are darker than others, and I feel like no one notices.</p><p>Music is the only thing that gets me through.</p>" \
  "Lost in the crowd" "nov01_2002" "<p>Sometimes I feel invisible, like I’m lost in a crowd of strangers.</p><p>Is anyone out there really listening?</p>" \
  "Finding light" "oct20_2002" "<p>Today I found a song that made me feel less alone.</p><p>Maybe there’s hope after all.</p>"

create_site "lonelydaydreamer.com" "Lonely Daydreamer" "Mia" \
  "Quiet afternoons" "dec10_2003" "<p>Sometimes I just sit and watch the world go by.</p><p>It’s peaceful but lonely.</p>" \
  "Dreams of escape" "dec01_2003" "<p>I dream of escaping to somewhere new, somewhere free.</p><p>Will I ever get there?</p>" \
  "Lost in thought" "nov20_2003" "<p>My mind wanders to places I can’t reach.</p><p>I hope someday I find where I belong.</p>"

echo "Time capsule sites generated in '$root_dir'."
echo "Run: cd $root_dir && python3 -m http.server"
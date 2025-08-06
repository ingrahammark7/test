#!/bin/bash

mkdir -p hyperborea_site
cd hyperborea_site

# Index
cat <<EOF > index.html
<!DOCTYPE html>
<html>
<head><title>Hyperborean Mysticism</title></head>
<body>
<h1>The Frozen Wisdom of Hyperborea</h1>
<p>Welcome to a reconstructed archive of the lost Thulian Mysticism site, last seen in 2003.</p>
<ul>
  <li><a href="origin.html">The Origin of Hyperborea</a></li>
  <li><a href="glyphs.html">Glyphs of the Cold Gods</a></li>
  <li><a href="rituals.html">Rituals of Ice</a></li>
  <li><a href="theory.html">Polar Vibrational Science</a></li>
  <li><a href="links.html">Ancient Hyperlinks</a></li>
</ul>
</body>
</html>
EOF

# Origin
cat <<EOF > origin.html
<!DOCTYPE html>
<html>
<head><title>The Origin of Hyperborea</title></head>
<body>
<h1>Origin of Hyperborea</h1>
<p>Hyperborea, the land beyond the North Wind, was said to be home to radiant beings of immense intelligence. Plato hinted at it. Pythagoras learned from its emissaries.</p>
<p>They encoded their history in crystalline scrolls lost beneath the polar caps, allegedly buried in 12 concentric domes beneath what is now Greenland.</p>
<a href="index.html">Back</a>
</body>
</html>
EOF

# Glyphs
cat <<EOF > glyphs.html
<!DOCTYPE html>
<html>
<head><title>Glyphs of the Cold Gods</title></head>
<body>
<h1>Glyphs of the Cold Gods</h1>
<p>The language of Hyperborea was composed of interlocking ice glyphs, visual mantras channeled into reality through trance-inscription.</p>
<ul>
  <li>𐰆 - Voice of Polar Eternity</li>
  <li>ᛉ - Seal of the Moonroot</li>
  <li>𐍃 - Spiral of Ice Thought</li>
</ul>
<p>Only three remain decoded in known manuscripts. The rest were lost in the burning of the Riga Archive in 1912.</p>
<a href="index.html">Back</a>
</body>
</html>
EOF

# Rituals
cat <<EOF > rituals.html
<!DOCTYPE html>
<html>
<head><title>Rituals of Ice</title></head>
<body>
<h1>Rituals of Ice</h1>
<p>Practitioners of the Hyperborean path underwent cryoshamanic trance, wherein body temperature was lowered through breathwork to receive ancestral broadcasts.</p>
<p>They carved frost-temples from glaciers and aligned their prayers with magnetic anomalies once mapped in Soviet esoteric research logs (now classified).</p>
<a href="index.html">Back</a>
</body>
</html>
EOF

# Theory
cat <<EOF > theory.html
<!DOCTYPE html>
<html>
<head><title>Polar Vibrational Science</title></head>
<body>
<h1>Polar Vibrational Science</h1>
<p>Hyperborean science involved “geomelonic resonance,” a field concept believed to allow mental projection across ice lattices.</p>
<p>Discredited in the West, the concept appeared in early Tesla notes and in suppressed pages from Wilhelm Reich’s journals.</p>
<a href="index.html">Back</a>
</body>
</html>
EOF

# Links
cat <<EOF > links.html
<!DOCTYPE html>
<html>
<head><title>Ancient Hyperlinks</title></head>
<body>
<h1>Dead Links of the Old Net</h1>
<ul>
  <li><a href="http://geocities.com/thulewave" target="_blank">Thulewave Geocities (404)</a></li>
  <li><a href="http://members.tripod.com/~polar_gate" target="_blank">The Polar Gate Archive (deleted)</a></li>
  <li><a href="http://frostpath.angelfire.com" target="_blank">Frostpath Index (vanished)</a></li>
</ul>
<p>Preserved only in memory.</p>
<a href="index.html">Back</a>
</body>
</html>
EOF

echo "Hyperborean site written to ./hyperborea_site/"
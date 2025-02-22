pkg upgrade -y
pkg update -y
termux-setup-storage
pkg install -y bash
pkg install -y libxml2 geckodriver wget wget2 e2fsprogs python python-pip nano ffmpeg git make lsof gzip clang cmake htop bat fd ripgrep tig asciinema neofetch  nnn aria2 mc mtr  lftp fzf pacman termux-api
pip install yt-dlp setuptools youtube-dl gallery-dl beautifulsoup4 build reportlab
apt install root-repo
apt install iw
apt install libc++ libnl libpcap libsqlite openssl pcre zlib -y
CFLAGS="-Wno-error=incompatible-function-pointer-types -O0" pip install lxml

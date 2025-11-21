find . -maxdepth 1 -type f ! -name '*.tar*' -print0 \
  | xargs -0 ls -S --zero \
  | head -z -n 6000 \
  | tar --remove-files --null -T - -czf "largest_$(date +%Y%m%d_%H%M%S).tar.gz"
find ./ \
  -path "./extension/node_modules" -prune -o \
  -path "./extension/package-lock.json" -prune -o \
  -path "./language/venv" -prune -o \
  -path "./language/build" -prune -o \
  -path "*/out" -prune -o \
  -name "*.spec" -prune -o \
  -type f -exec sh -c 'grep -Iq . "$1" && echo "$1"' _ {} \; \
| xargs wc -l \
| awk 'NF>1 { sub("./","",$2); split($2,a,"/"); dirs[a[1]]+=$1 } END { for (d in dirs) print dirs[d], d }' \
| sort -nr

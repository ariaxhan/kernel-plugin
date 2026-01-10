#!/bin/bash
# docs-staleness-check.sh
# Run on CI or pre-commit to detect stale documentation
# Exit 1 if stale docs found, 0 otherwise

set -e

DOCS_DIR="${DOCS_DIR:-docs}"
STALE=()
WARNINGS=()

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

log_stale() { STALE+=("$1"); }
log_warn() { WARNINGS+=("$1"); }

check_frontmatter() {
  local doc="$1"
  local has_kind has_reviewed has_cadence has_owners
  
  has_kind=$(grep -c "^doc_kind:" "$doc" 2>/dev/null || echo 0)
  has_reviewed=$(grep -c "^last_reviewed:" "$doc" 2>/dev/null || echo 0)
  has_cadence=$(grep -c "^review_cadence:" "$doc" 2>/dev/null || echo 0)
  has_owners=$(grep -c "^owners:" "$doc" 2>/dev/null || echo 0)
  
  [[ "$has_kind" -eq 0 ]] && log_warn "$doc: missing doc_kind"
  [[ "$has_reviewed" -eq 0 ]] && log_warn "$doc: missing last_reviewed"
  [[ "$has_cadence" -eq 0 ]] && log_warn "$doc: missing review_cadence"
  [[ "$has_owners" -eq 0 ]] && log_warn "$doc: missing owners"
  
  [[ "$has_reviewed" -gt 0 ]]
}

check_cadence() {
  local doc="$1"
  local last cadence days
  
  last=$(grep -m1 "^last_reviewed:" "$doc" | sed 's/last_reviewed: *//' | tr -d '"')
  cadence=$(grep -m1 "^review_cadence:" "$doc" | sed 's/review_cadence: *//' | tr -d '"')
  cadence="${cadence:-90}"
  
  # Calculate days since last review
  if command -v gdate &>/dev/null; then
    # macOS with coreutils
    days=$(( ($(gdate +%s) - $(gdate -d "$last" +%s)) / 86400 ))
  else
    # Linux
    days=$(( ($(date +%s) - $(date -d "$last" +%s)) / 86400 ))
  fi
  
  if [[ "$days" -gt "$cadence" ]]; then
    log_stale "$doc: cadence expired (${days}d > ${cadence}d)"
    return 1
  fi
  return 0
}

check_dependencies() {
  local doc="$1"
  local last deps dep dep_date
  
  last=$(grep -m1 "^last_reviewed:" "$doc" | sed 's/last_reviewed: *//' | tr -d '"')
  
  # Extract depends_on list
  deps=$(sed -n '/^depends_on:/,/^[a-z_]*:/p' "$doc" | grep "^\s*-" | sed 's/.*- //' | tr -d '"')
  
  for dep in $deps; do
    [[ -z "$dep" ]] && continue
    [[ ! -f "$dep" ]] && { log_warn "$doc: dependency not found: $dep"; continue; }
    
    dep_date=$(git log -1 --format="%cs" -- "$dep" 2>/dev/null || echo "")
    [[ -z "$dep_date" ]] && continue
    
    if [[ "$dep_date" > "$last" ]]; then
      log_stale "$doc: dependency modified ($dep changed $dep_date, doc reviewed $last)"
      return 1
    fi
  done
  return 0
}

check_orphans() {
  local index="$DOCS_DIR/index.md"
  [[ ! -f "$index" ]] && { log_warn "Missing docs/index.md (doc graph root)"; return; }
  
  for doc in "$DOCS_DIR"/**/*.md; do
    [[ "$doc" == "$index" ]] && continue
    [[ "$doc" == *"MAINTENANCE.md" ]] && continue
    [[ "$doc" == *"paths/"* ]] && continue
    
    local basename=$(basename "$doc")
    if ! grep -q "$basename" "$index" 2>/dev/null; then
      log_warn "$doc: orphan (not linked from index.md)"
    fi
  done
}

check_see_also() {
  local doc="$1"
  if ! grep -q "^## See Also" "$doc" 2>/dev/null; then
    log_warn "$doc: missing See Also section"
  fi
}

check_budgets() {
  local doc="$1"
  local lines headings
  
  lines=$(wc -l < "$doc")
  headings=$(grep -c "^#" "$doc" || echo 0)
  
  [[ "$lines" -gt 220 ]] && log_stale "$doc: over hard max (${lines} lines > 220)"
  [[ "$headings" -gt 12 ]] && log_warn "$doc: too many headings (${headings} > 12)"
}

# Skip certain files
should_skip() {
  local doc="$1"
  [[ "$doc" == *"index.md" ]] && return 0
  [[ "$doc" == *"MAINTENANCE.md" ]] && return 0
  [[ "$doc" == *"CHANGELOG.md" ]] && return 0
  [[ "$doc" == *"README.md" ]] && return 0
  return 1
}

# Main
echo "Checking documentation in $DOCS_DIR..."

# Check for doc directory
[[ ! -d "$DOCS_DIR" ]] && { echo "No docs directory found"; exit 0; }

# Check each doc
for doc in "$DOCS_DIR"/**/*.md; do
  [[ ! -f "$doc" ]] && continue
  should_skip "$doc" && continue
  
  check_frontmatter "$doc" || continue
  check_cadence "$doc"
  check_dependencies "$doc"
  check_see_also "$doc"
  check_budgets "$doc"
done

# Check orphans
check_orphans

# Report
echo ""

if [[ ${#WARNINGS[@]} -gt 0 ]]; then
  echo -e "${YELLOW}⚠️  WARNINGS:${NC}"
  printf '%s\n' "${WARNINGS[@]}"
  echo ""
fi

if [[ ${#STALE[@]} -gt 0 ]]; then
  echo -e "${RED}🚨 STALE DOCS:${NC}"
  printf '%s\n' "${STALE[@]}"
  echo ""
  echo "Run 'kernel docs maintenance' to process stale docs."
  exit 1
fi

echo -e "${GREEN}✓ All docs current${NC}"
exit 0

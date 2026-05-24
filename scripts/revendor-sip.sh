#!/usr/bin/env bash
# Refresh the SIP-related protos from upstream livekit/protocol and re-apply this
# library's vendoring transform (package livekit/rpc/psrpc -> livekit_protocol_ex.*,
# strip [(logger.*)] field options and option(...) custom options, drop logger import).
#
# After running, regenerate per README, e.g.:
#   mix protox.generate --multiple-files --output-path=./lib/live_kit_protocol_ex \
#     --include-path=./priv/protobufs <entry .proto files incl rpc/sip.proto>
#   then the find/rename steps in README, and `sed -i '' 's/LivekitProtocolEx/LiveKitProtocolEx/g'`.
set -euo pipefail
cd "$(dirname "$0")/.."
REF="${1:-main}"
RAW="https://raw.githubusercontent.com/livekit/protocol/${REF}/protobufs"
tmp="$(mktemp -d)"
declare -a files=("livekit_sip.proto" "rpc/io.proto" "rpc/sip.proto")
for f in "${files[@]}"; do
  curl -fsSL "$RAW/$f" -o "$tmp/$(echo "$f" | tr / _)"
  python3 scripts/proto_transform.py "$tmp/$(echo "$f" | tr / _)" "priv/protobufs/$f"
  echo "refreshed priv/protobufs/$f"
done
echo "Done. Now regenerate (see header / README)."

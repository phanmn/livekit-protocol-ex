defmodule LivekitProtocolEx do
  use Protox,
    files: [
      "./priv/protobufs/livekit_rtc.proto",
      "./priv/protobufs/livekit_agent.proto",
      "./priv/protobufs/infra/link.proto",
      "./priv/protobufs/rpc/agent.proto",
      "./priv/protobufs/rpc/room.proto",
      "./priv/protobufs/rpc/io.proto"
    ],
    paths: [
      "./priv/protobufs"
    ]
end

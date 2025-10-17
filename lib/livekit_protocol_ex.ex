defmodule LivekitProtocolEx do
  use Protox,
    files: ["./priv/protobufs/livekit_rtc.proto", "./priv/protobufs/livekit_agent.proto"],
    namespace: __MODULE__
end

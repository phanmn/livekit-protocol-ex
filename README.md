# LivekitProtocolEx

```bash
mix protox.generate --multiple-files --output-path=./lib/livekit_protocol_ex --include-path=./priv/protobufs priv/protobufs/livekit_rtc.proto priv/protobufs/livekit_agent.proto priv/protobufs/infra/link.proto priv/protobufs/rpc/agent.proto priv/protobufs/rpc/room.proto priv/protobufs/rpc/io.proto

find . -depth -name "livekit_protocol_ex_*" -type f -execdir bash -c 'mv "$1" "${1#livekit_protocol_ex_}"' _ {} \;

find . -type f -name "rpc_*" -execdir bash -c 'mkdir -p rpc && mv "$1" "rpc/${1#rpc_}"' _ {} \;
```

## Installation

If [available in Hex](https://hex.pm/docs/publish), the package can be installed
by adding `livekit_protocol_ex` to your list of dependencies in `mix.exs`:

```elixir
def deps do
  [
    {:livekit_protocol_ex, "~> 0.1.0"}
  ]
end
```

Documentation can be generated with [ExDoc](https://github.com/elixir-lang/ex_doc)
and published on [HexDocs](https://hexdocs.pm). Once published, the docs can
be found at <https://hexdocs.pm/livekit_protocol_ex>.


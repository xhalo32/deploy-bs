#!/usr/bin/env python3
import argparse
import subprocess
import sys

def run(cmd):
    print("+", " ".join(cmd))
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    output = ""
    for line in process.stdout:
        output += line
        sys.stdout.write(line)
    process.wait()
    return output

def main():
    parser = argparse.ArgumentParser(
        description="Deploy-bs: No-BullSh*t NixOS deployment automation. P.S. No flake support!"
    )
    parser.add_argument("host", help="NixOS configuration path (usually nixosConfigurations.hostname)")
    parser.add_argument("remote", help="SSH target (format: user@remote)")
    parser.add_argument(
        "--action",
        choices=["switch", "boot", "test"],
        default="switch",
        help="Activation action (default: switch)",
    )
    args = parser.parse_args()

    output = run(["nix-build", "--no-out-link", "-A", f"{args.host}.config.system.build.toplevel"])
    store_path = output.split()[-1]
    assert store_path.startswith("/nix/store")
    run(["nix-copy-closure", "--to", args.remote, store_path])
    run(["ssh", args.remote, "sudo", f"{store_path}/bin/switch-to-configuration", args.action])

if __name__ == "__main__":
    sys.exit(main())

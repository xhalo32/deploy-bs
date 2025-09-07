{
  sources ? import ./npins,
  system ? builtins.currentSystem,
  pkgs ? import sources.nixpkgs {
    inherit system;
    config = { };
    overlays = [ ];
  },
}:
{
  package = pkgs.stdenv.mkDerivation {
    pname = "deploy-bs";
    version = "1.0.0";

    src = pkgs.lib.sources.sourceByRegex ./. [ ".*\.py$" ];

    nativeBuildInputs = [
      pkgs.makeWrapper
    ];
    buildInputs = [
      pkgs.python3
    ];

    installPhase = ''
      install -Dm755 $src/deploy.py $out/bin/deploy
      wrapProgram $out/bin/deploy \
        --prefix PATH : ${
          pkgs.lib.makeBinPath [
            pkgs.nix
            pkgs.openssh
          ]
        }
    '';
  };
}

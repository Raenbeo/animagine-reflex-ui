let
  pkgs = import <nixpkgs> {
    config = {
      allowUnfree = true;
    };
  };

in
pkgs.mkShell {
  buildInputs = with pkgs;[
    python312
    python312Packages.torch-bin
    python312Packages.uv
  ];
}

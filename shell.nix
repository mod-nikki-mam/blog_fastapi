let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = with pkgs; [
    nodejs_24
    typst
    (python3.withPackages (p: with p; [
      flask
      sqlalchemy
      aiosqlite
      python-dateutil
      python-multipart
      feedparser
      uvicorn
      starlette
      fastapi
    ]))
  ];
}

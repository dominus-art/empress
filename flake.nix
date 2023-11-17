{
    description = "Pycord dev environment";
    outputs = { self, nixpkgs, flake-utils }:
        flake-utils.lib.eachDefaultSystem
            (
                system:
                    let
                        pkgs = import nixpkgs { inherit system; };
                        python = pkgs.python311;
                        pythonPkgs = python.pkgs;
                        in {
                            devShells.default = pkgs.mkShell {
                                name = "pycordBot";
                                nativeBuildInputs = [ pkgs.bashInteractive ];
                                buildInputs = with pkgs; [
                                    python.pkgs.setuptools
                                    python.pkgs.wheel
                                    python.pkgs.venvShellHook
                                    python.pkgs.pydantic
                                    python.pkgs.sqlalchemy
                                ];
                                venvDir = "venv";
                                src = null;
                                postVenv = ''
                                    unset SOURCE_DATE_EPOCH
                                '';
                                postShellHook = ''
                                    unset SOURCE_DATE_EPOCH
                                    unset LD_PRELOAD
                                    
                                    PYTHONPATH=$PWD/$venvDir/${python.sitePackages}:PYTHONPATH
                                    '';
                            };
                        }
            );
}
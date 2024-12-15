{pkgs}: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.virtualenv
    pkgs.docker
    pkgs.nodejs
    pkgs.chromedriver
    pkgs.google-chrome-beta
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.python311
      pkgs.python311Packages.pip
    ];
    PYTHONBIN = "${pkgs.python311}/bin/python3.11";
    LANG = "en_US.UTF-8";
    STDERREDBIN = "${pkgs.stdenv.cc}/bin/stderr";
    PROOT_CPUID = "genuine";
  };
}

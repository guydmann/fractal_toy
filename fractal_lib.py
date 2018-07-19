import os

class FractalLib:
    fractal_mapping = {
        "mandelbrot"                : "Mandelbrot",
        "julia"                     : "Julia",
        "burning_ship"              : "BurningShip",
        "star"                      : "Star",
        "newton"                    : "Newton",
        "phoenix_mandelbrot"        : "PhoenixMandelbrot",
        "phoenix_julia"             : "PhoenixJulia",
        "cubic_mandelbrot"          : "CubicMandelbrot",
        "cubic_julia"               : "CubicJulia",
        "quartic_mandelbrot"        : "QuarticMandelbrot",
        "quartic_julia"             : "QuarticJulia",
        "experimental_cubic_julia"  : "ExperimentalCubicJulia",
        "buddhabrot"                : "Buddhabrot",
        "buddhabrot_julia"          : "BuddhabrotJulia"
    }

    color_mapping = {
        "simple"                : "Simple",
        "black_and_white"       : "BlackAndWhite",
        "hue_range"             : "HueRange",
        "rgba_cyclic"           : "RGBACyclic"
    }

    @staticmethod
    def empty_dir_and_remove(directory):
        path = "{}/".format(directory)
        if (os.path.isdir(directory)):
            files = os.listdir(path)
            if len(files):
                for f in files:
                    file_path = os.path.join(path, f)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(e)
            os.rmdir(directory)
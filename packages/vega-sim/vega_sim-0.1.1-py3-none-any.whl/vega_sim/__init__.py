try:
    from importlib.resources import files, as_file
except:
    from importlib_resources import files, as_file

vega_home_path = files(__name__).joinpath("vegahome")
vega_bin_path = files(__name__).joinpath("bin")

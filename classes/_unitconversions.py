import math

# Length Conversions
lengthConversions = {
    "metres": 1,
    "kilometres": 0.001,
    "centimetres": 100,
    "millimetres": 1000,
    "micrometres": 1000000,
    "nanometres": 1000000000,
    "decimetres": 10,
    "megametres": 0.000001,
    "gigametres": 0.000000001,
    "yards": 1.09361,
    "feet": 3.28084,
    "inches": 39.3701,
    "miles": 0.000621371,
    "nautical miles": 0.000539957,
    "light seconds": 3.33564e-9,
    "light years": 1.0570e-16,
    "light days": 1.2167e-15,
    "light months": 3.6292e-14,
    "light weeks": 8.5338e-15,
    "planck lengths": 1 / 1.616255e35
}

# Area Conversions
areaConversions = {
    "square metres": 1,
    "square kilometres": 0.000001,
    "square centimetres": 10000,
    "square millimetres": 1000000,
    "square micrometres": 1000000000,
    "square nanometres": 1000000000000,
    "square decimetres": 100,
    "square megametres": 0.000000000001,
    "square gigametres": 0.000000000000001,
    "square yards": 1.19599,
    "square feet": 10.7639,
    "square inches": 1550.0031,
    "square miles": 3.861e-7,
    "square nautical miles": 5.396e-7,
    "square light seconds": 1.1114e-16,
    "square light years": 1.1177e-33,
    "square light days": 1.4111e-32,
    "square light months": 1.3157e-30,
    "square light weeks": 3.3279e-31,
    "acres": 0.000247105,
    "hectares": 0.0001
}

# Volume Conversions
volumeConversions = {
    "cubic metres": 1,
    "cubic kilometres": 1e-9,
    "cubic centimetres": 1000000,
    "cubic millimetres": 1e+9,
    "cubic micrometres": 1e+18,
    "cubic nanometres": 1e+27,
    "cubic decimetres": 1000,
    "cubic megametres": 1e-18,
    "cubic gigametres": 1e-27,
    "cubic yards": 1.30795,
    "cubic feet": 35.3147,
    "cubic inches": 61023.7,
    "cubic miles": 2.399e-11,
    "cubic nautical miles": 3.458e-11,
    "cubic light seconds": 4.1093e-26,
    "cubic light years": 4.181e-43,
    "cubic light days": 5.855e-42,
    "cubic light months": 5.382e-40,
    "cubic light weeks": 1.379e-41,
    "acres-feet": 8.107e-4,
    "hectares-meters": 1e-4
}

# Speed Conversions
speedConversions = {
    "meters per second": 1,
    "kilometers per hour": 3.6,
    "miles per hour": 2.23694,
    "feet per second": 3.28084,
    "inches per second": 39.3701,
    "knots": 1.94384,
    "mach": 0.002936,
    "speed of light": 3.33564e-9,
    "light years per year": 1.0570e-16,
    "light days per day": 1.2167e-15,
    "light months per month": 3.6292e-14,
    "light weeks per week": 8.5338e-15,
    "millimeters per second": 1000,
    "millimeters per hour": 3600000,
    "centimeters per second": 100,
    "centimeters per hour": 36000
}

# Time Conversions
timeConversions = {
    "seconds": 1,
    "milliseconds": 1000,
    "microseconds": 1e6,
    "nanoseconds": 1e9,
    "minutes": 1 / 60,
    "hours": 1 / 3600,
    "days": 1 / 86400,
    "weeks": 1 / 604800,
    "months": 1 / 2.628e6,
    "years": 1 / 3.154e7,
    "planck time": 1 / 5.39e44
}

# Energy Conversions
energyConversions = {
    "joules": 1,
    "kilojoules": 0.001,
    "calories": 0.239006,
    "kilocalories": 0.000239006,
    "electron volts": 6.242e18,
    "ergs": 1e7,
    "watt-hours": 1 / 3600,
    "kilowatt-hours": 1 / 3.6e6,
    "BTUs": 9.478e-2,
    "foot-pounds": 0.737562,
    "tonne of TNT": 4.184e-9,
    "kilotonnes of TNT": 4.184e-12,
    "Planck energy": 1 / 1.956e-9
}

# Angle Conversions
angleConversions = {
    "degrees": (lambda x: x, lambda x: x),
    "radians": (lambda x: math.degrees(x), lambda x: math.radians(x)),
    "gradians": (lambda x: x*400/360 % 400, lambda x: x*360/400 % 400),
    "minutes": (lambda x: x/60, lambda x: x*60),
    "seconds": (lambda x: x/3600, lambda x: x*3600),
    "turns": (lambda x: x*360, lambda x: x/360),
    "arcminutes": (lambda x: x/60, lambda x: x*60),
    "arcseconds": (lambda x: x/3600, lambda x: x*3600)
}

# Information Conversions
informationConversions = {
    "bits": 1,
    "bytes": 1 / 8,
    "kilobits": 1 / 1000,
    "kilobytes": 1 / (1024 * 8),
    "megabits": 1 / 1000000,
    "megabytes": 1 / (1024 * 1024 * 8),
    "gigabits": 1 / 1000000000,
    "gigabytes": 1 / (1024 * 1024 * 1024 * 8),
    "terabits": 1 / 1000000000000,
    "terabytes": 1 / (1024 * 1024 * 1024 * 1024 * 8),
    "petabits": 1 / 1000000000000000,
    "petabytes": 1 / (1024 * 1024 * 1024 * 1024 * 1024 * 8)
}

# Temperature Conversions
temperatureConversions = {
    "Celsius": (
        lambda x: x,
        lambda x: x
    ),
    "Fahrenheit": (
        lambda x: (x - 32) * 5 / 9,
        lambda x: x * 9 / 5 + 32
    ),
    "Kelvin": (
        lambda x: x - 273.15,
        lambda x: x + 273.15
    )
}

# Power Conversions
powerConversions = {
    "watts": 1,
    "kilowatts": 0.001,
    "megawatts": 1e-6,
    "gigawatts": 1e-9,
    "terawatts": 1e-12,
    "milliwatts": 1000,
    "microwatts": 1e6,
    "nanowatts": 1e9,
    "picowatts": 1e12,
    "femtowatts": 1e15,
    "horsepower": 1 / 745.7,
    "metric horsepower": 1 / 735.5,
    "kilohorsepower": 1 / 745.7e3,
}

# Force Conversions
forceConversions = {
    "newtons": 1,
    "kilonewtons": 0.001,
    "meganewtons": 1e-6,
    "giganewtons": 1e-9,
    "teranewtons": 1e-12,
    "milliNewtons": 1000,
    "micronewtons": 1e6,
    "nanonewtons": 1e9,
    "pound-force": 0.224809,
    "ounce-force": 0.03527396,
    "dyne": 1e5
}

# Torque Conversions
torqueConversions = {
    "newton-meters": 1,
    "kilogram-meters": 0.10197,
    "foot-pounds": 0.737562,
    "inch-pounds": 8.8507,
    "dyne-centimeters": 1e5,
    "ounce-inches": 0.0562503
}

# Frequency Conversions
frequencyConversions = {
    "hertz": 1,
    "kilohertz": 1e-3,
    "megahertz": 1e-6,
    "gigahertz": 1e-9,
    "terahertz": 1e-12,
    "gigacycles": 1e-9,
    "megacycles": 1e-6,
    "kilocycles": 1e-3
}

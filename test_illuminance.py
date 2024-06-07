import unittest
import numpy as np
import pandas as pd
import pvlib 


from DIBS import Window
from districtgenerator import SunIlluminance

def read_epw_file(file_path):
    # Assuming EPW file format and extracting necessary columns
    # This function needs to be implemented to parse the EPW file correctly
    weather_data = pd.read_csv(file_path, skiprows=8, header=None)
    sun_positions = pvlib.solarposition.get_solarposition(
        time=weather_data[0],  # Placeholder for actual timestamp column
        latitude=50.76,  # Placeholder for actual latitude
        longitude=6.07   # Placeholder for actual longitude
    )
    return sun_positions, weather_data

class TestIlluminanceComparison(unittest.TestCase):
    def test_illuminance_comparisons(self):

        sun_positions, weather_data = read_epw_file(r'data\DEU_BE_Berlin-Schonefeld.AP.103850_TMYx.2004-2018.epw')
        
        # Use a specific hour or range of hours for testing
        hour_index = 12  # for example, noon
        sun_altitude = sun_positions['elevation'][hour_index]
        sun_azimuth = sun_positions['azimuth'][hour_index]
        normal_direct_illuminance = weather_data[DIRECT_ILLUMINANCE_COLUMN][hour_index]  # Adjust column index
        horizontal_diffuse_illuminance = weather_data[DIFFUSE_ILLUMINANCE_COLUMN][hour_index]  # Adjust column index

        # Instantiate and run calculations as previously outlined
        window = Window(180, 90, 0.8, 1)
        sun_illum = SunIlluminance(filePath="dummy_path")

        window.calc_illuminance(sun_altitude, sun_azimuth, normal_direct_illuminance, horizontal_diffuse_illuminance)
        sun_illum_results = sun_illum.calcIlluminance(
            initialTime=0,
            timeDiscretization=3600,
            timeSteps=1,
            timeZone=1,
            location=(52.3667, 13.5033),
            altitude=50,
            beta=[90],
            gamma=[0],
            normal_direct_illuminance=np.array([normal_direct_illuminance]),
            horizontal_diffuse_illuminance=np.array([horizontal_diffuse_illuminance])
        )
        
if __name__ == '__main__':
    unittest.main()
import unittest
import numpy as np
import pandas as pd
import pvlib 
import math


from src.DIBS import Window
from src.districtgenerator import SunIlluminance

def read_epw_file(file_path):
    # Assuming EPW file format and extracting necessary columns
    # This function needs to be implemented to parse the EPW file correctly
    # Set EPW Labels and import epw file
    epw_labels = ['year', 'month', 'day', 'hour', 'minute', 'datasource', 'drybulb_C', 'dewpoint_C',
                      'relhum_percent',
                      'atmos_Pa', 'exthorrad_Whm2', 'extdirrad_Whm2', 'horirsky_Whm2', 'glohorrad_Whm2',
                      'dirnorrad_Whm2', 'difhorrad_Whm2', 'glohorillum_lux', 'dirnorillum_lux', 'difhorillum_lux',
                      'zenlum_lux', 'winddir_deg', 'windspd_ms', 'totskycvr_tenths', 'opaqskycvr_tenths',
                      'visibility_km',
                      'ceiling_hgt_m', 'presweathobs', 'presweathcodes', 'precip_wtr_mm', 'aerosol_opt_thousandths',
                      'snowdepth_cm', 'days_last_snow', 'Albedo', 'liq_precip_depth_mm', 'liq_precip_rate_Hour']

    weather_data = pd.read_csv(
            file_path, skiprows=8, header=None, names=epw_labels).drop('datasource', axis=1)

    weather_data["timestamp"] = pd.to_datetime(weather_data[['year', 'month', 'day', 'hour', 'minute']])
    
    sun_positions = pvlib.solarposition.get_solarposition(
        time=weather_data['timestamp'], 
        latitude=52.38080,  
        longitude=13.53060   
    )
    return sun_positions, weather_data

class TestIlluminanceComparison(unittest.TestCase):
    def test_illuminance_comparisons(self):

        sun_positions, weather_data = read_epw_file(r'data\DEU_BE_Berlin-Schonefeld.AP.103850_TMYx.2004-2018.epw')
        
        # Use a specific hour or range of hours for testing
        hour_index = 12  # for example, noon
        sun_altitude = sun_positions['elevation'][hour_index]
        sun_azimuth = sun_positions['azimuth'][hour_index]
        normal_direct_illuminance = weather_data['dirnorillum_lux'][hour_index]  # Adjust column index
        horizontal_diffuse_illuminance = weather_data['difhorillum_lux'][hour_index]  # Adjust column index

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
        self.assertAlmostEqual(window.transmitted_illuminance, sun_illum_results[0], delta=5000, 
                               msg="Calculations do not match withing toleracne.")
if __name__ == '__main__':
    unittest.main()
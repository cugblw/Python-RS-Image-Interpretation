from landsatxplore.earthexplorer import EarthExplorer

ee = EarthExplorer('Weil_Lee', 'WeilLee|2021')

ee.download('LT51960471995178MPS00', output_dir='./data')

ee.logout()
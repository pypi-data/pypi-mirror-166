from pmc_turbo.camera.pipeline.exposure_manager import ExposureManager
import pandas as pd
from pmc_turbo.camera.pipeline.write_images import percentile_keys
from pmc_turbo.utils.log import setup_stream_handler
import logging
setup_stream_handler(level=logging.DEBUG)

def build_pipeline_status(current_exposure):
    pipeline_status = dict(all_camera_parameters=dict(ExposureTimeAbs=current_exposure))
    return pipeline_status

#percentiles_to_compute = [0,1,10,20,30,40,50,60,70,80,90,99,100]
#percentile_keys = ['percentile_%d' % k for k in percentiles_to_compute]

def build_file_statistics(filename, exposure_us, **kwargs):
    row = dict(filename=filename, exposure_us=exposure_us, **kwargs)
    for index, key in enumerate(percentile_keys):
        if key not in row:
            if index == 0:
                row[key] = 0
            elif percentile_keys[index-1] in row:
                row[key] = row[percentile_keys[index-1]]
    return pd.Series(row)

def test_skip_mismatch_exposure():
    em = ExposureManager()
    file_statistics = build_file_statistics(filename='none',exposure_us=2000)
    assert em.check_exposure(build_pipeline_status(1000), file_statistics) is None

def test_small_exposure_mismatch():
    em = ExposureManager()
    file_statistics = build_file_statistics(filename='none',exposure_us=50001,percentile_0=1)
    assert em.check_exposure(build_pipeline_status(50000), file_statistics) is not None

def test_underexposed():
    em = ExposureManager()
    file_statistics = build_file_statistics(filename='none',exposure_us=1000,percentile_0=1)
    assert em.check_exposure(build_pipeline_status(1000), file_statistics) > 1000

def test_overexposed():
    em = ExposureManager()
    file_statistics = build_file_statistics(filename='none',exposure_us=1000,percentile_0=16000)
    assert em.check_exposure(build_pipeline_status(1000), file_statistics) < 1000

def test_mid_exposure_with_high_max():
    em = ExposureManager()
    file_statistics = build_file_statistics(filename='none',exposure_us=1000,percentile_0=8000,percentile_100=16000)
    assert em.check_exposure(build_pipeline_status(1000), file_statistics) is None

def test_mid_exposure_with_slightly_low_max():
    em = ExposureManager()
    file_statistics = build_file_statistics(filename='none',exposure_us=1000,percentile_0=8000,
                                            percentile_100=em.min_peak_threshold_fraction*16384-10)
    assert em.check_exposure(build_pipeline_status(1000), file_statistics) == 1000*(1+em.adjustment_step_size_fraction)

def test_mid_exposure():
    em = ExposureManager()
    file_statistics = build_file_statistics(filename='none',exposure_us=1000,percentile_0=8000,percentile_90=13000)
    assert em.check_exposure(build_pipeline_status(1000), file_statistics) is None

def test_low_exposure():
    em = ExposureManager()
    file_statistics = build_file_statistics(filename='none',exposure_us=1000,percentile_0=1,percentile_90=13000)
    assert em.check_exposure(build_pipeline_status(1000), file_statistics) > 1000

def test_same_file():
    em = ExposureManager()
    file_statistics = build_file_statistics(filename='none',exposure_us=1000,percentile_0=1,percentile_90=13000)
    assert em.check_exposure(build_pipeline_status(1000), file_statistics) > 1000
    assert em.check_exposure(build_pipeline_status(1000), file_statistics) is None


from pmc_turbo.camera.pipeline.acquire_images import next_gate_time
import time
def test_gate_time():
    now = int(time.time())
    for interval in range(1,100):
        next = next_gate_time(now,interval)
        assert next > int(now)
        assert next % interval == 0
        assert next > time.time()
    now = time.time()
    for interval in range(1,100):
        next = next_gate_time(now,interval)
        assert next > int(now)
        assert next % interval == 0
        assert next > time.time()

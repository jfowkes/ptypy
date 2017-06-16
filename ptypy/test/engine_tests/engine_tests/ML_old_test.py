"""
Test for the ML_old engine.

This file is part of the PTYPY package.
    :copyright: Copyright 2014 by the PTYPY team, see AUTHORS.
    :license: GPLv2, see LICENSE for details.
"""

import unittest
from ptypy.test import test_utils as tu
from ptypy import utils as u

class MLOldTest(unittest.TestCase):
    @unittest.skip('skip this because it is not supported')
    def test_ML_old(self):
        engine_params = u.Param()
        engine_params.name = 'ML_old'
        engine_params.numiter = 5
        engine_params.ML_type = 'gaussian'
        engine_params.floating_intensities = False
        engine_params.intensity_renormalization = 1.
        engine_params.reg_del2 = False
        engine_params.reg_del2_amplitude = .01
        engine_params.smooth_gradient = 0
        engine_params.scale_precond = False
        engine_params.scale_probe_object = 1.
        tu.EngineTestRunner(engine_params)

if __name__ == "__main__":
    unittest.main()
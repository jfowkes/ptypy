from . import load_kernel
from pycuda import gpuarray
import numpy as np

class ArrayUtilsKernel:
    def __init__(self, acc_dtype=np.float64, queue=None):
        self.queue = queue
        self.acc_dtype = acc_dtype
        self.cdot_cuda = load_kernel("dot", {
            'INTYPE': 'complex<float>',
            'ACCTYPE': 'double' if acc_dtype==np.float64 else 'float'
        })
        self.dot_cuda = load_kernel("dot", {
            'INTYPE': 'float',
            'ACCTYPE': 'double' if acc_dtype==np.float64 else 'float'
        })
        self.full_reduce_cuda = load_kernel("full_reduce", {
            'DTYPE': 'double' if acc_dtype==np.float64 else 'float',
            'BDIM_X': 1024
        })
        self.Ctmp = None
        
    def dot(self, A, B, out=None):
        assert A.dtype == B.dtype, "Input arrays must be of same data type"
        assert A.size == B.size, "Input arrays must be of the same size"
        
        if out is None:
            out = gpuarray.zeros((1,), dtype=self.acc_dtype)

        block = (1024, 1, 1)
        grid = (int((B.size + 1023) // 1024), 1, 1)
        if self.acc_dtype == np.float32:
            elsize = 4
        elif self.acc_dtype == np.float64:
            elsize = 8
        if self.Ctmp is None or self.Ctmp.size < grid[0]:
            self.Ctmp = gpuarray.zeros((grid[0],), dtype=self.acc_dtype)
        Ctmp = self.Ctmp
        if grid[0] == 1:
            Ctmp = out
        if np.iscomplexobj(B):
            self.cdot_cuda(A, B, np.int32(A.size), Ctmp,
                block=block, grid=grid, 
                shared=1024 * elsize,
                stream=self.queue)
        else:
            self.dot_cuda(A, B, np.int32(A.size), Ctmp,
                block=block, grid=grid,
                shared=1024 * elsize,
                stream=self.queue)
        if grid[0] > 1:
            self.full_reduce_cuda(self.Ctmp, out, np.int32(grid[0]), 
                block=(1024, 1, 1), grid=(1,1,1), shared=elsize*1024,
                stream=self.queue)
        
        return out


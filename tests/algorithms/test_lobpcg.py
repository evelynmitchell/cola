import numpy as np

from cola.backends import all_backends
from cola.fns import lazify
from cola.linalg.eig.lobpcg import lobpcg
from cola.utils.utils_for_tests import generate_pd_from_diag, generate_spectrum, get_xnp, parametrize, relative_error


@parametrize(all_backends)
def test_lobpcg_random(backend):
    xnp = get_xnp(backend)
    dtype = xnp.float32
    np_dtype = np.float32
    diag = generate_spectrum(coeff=0.5, scale=1.0, size=10, dtype=np_dtype)
    A = xnp.array(generate_pd_from_diag(diag, dtype=diag.dtype, seed=21), dtype=dtype, device=None)

    eigvals, _ = lobpcg(lazify(A), max_iters=A.shape[0])

    diag = xnp.array(diag[:-1], dtype=dtype, device=None)
    idx = xnp.argsort(diag, axis=-1)
    rel_error = relative_error(eigvals, diag[idx])
    assert rel_error < 5e-5

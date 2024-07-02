# distutils: libraries = flint
# distutils: depends = flint/padic.h

################################################################################
# This file is auto-generated by the script
#   SAGE_ROOT/src/sage_setup/autogen/flint_autogen.py.
# From the commit 3e2c3a3e091106a25ca9c6fba28e02f2cbcd654a
# Do not modify by hand! Fix and rerun the script instead.
################################################################################

from libc.stdio cimport FILE
from sage.libs.gmp.types cimport *
from sage.libs.mpfr.types cimport *
from sage.libs.flint.types cimport *

cdef extern from "flint_wrap.h":
    fmpz * padic_unit(const padic_t op) noexcept
    slong padic_val(const padic_t op) noexcept
    slong padic_get_val(const padic_t op) noexcept
    slong padic_prec(const padic_t op) noexcept
    slong padic_get_prec(const padic_t op) noexcept
    void padic_ctx_init(padic_ctx_t ctx, const fmpz_t p, slong min, slong max, padic_print_mode mode) noexcept
    void padic_ctx_clear(padic_ctx_t ctx) noexcept
    int _padic_ctx_pow_ui(fmpz_t rop, ulong e, const padic_ctx_t ctx) noexcept
    void padic_init(padic_t rop) noexcept
    void padic_init2(padic_t rop, slong N) noexcept
    void padic_clear(padic_t rop) noexcept
    void _padic_canonicalise(padic_t rop, const padic_ctx_t ctx) noexcept
    void _padic_reduce(padic_t rop, const padic_ctx_t ctx) noexcept
    void padic_reduce(padic_t rop, const padic_ctx_t ctx) noexcept
    void padic_randtest(padic_t rop, flint_rand_t state, const padic_ctx_t ctx) noexcept
    void padic_randtest_not_zero(padic_t rop, flint_rand_t state, const padic_ctx_t ctx) noexcept
    void padic_randtest_int(padic_t rop, flint_rand_t state, const padic_ctx_t ctx) noexcept
    void padic_set(padic_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    void padic_set_si(padic_t rop, slong op, const padic_ctx_t ctx) noexcept
    void padic_set_ui(padic_t rop, ulong op, const padic_ctx_t ctx) noexcept
    void padic_set_fmpz(padic_t rop, const fmpz_t op, const padic_ctx_t ctx) noexcept
    void padic_set_fmpq(padic_t rop, const fmpq_t op, const padic_ctx_t ctx) noexcept
    void padic_set_mpz(padic_t rop, const mpz_t op, const padic_ctx_t ctx) noexcept
    void padic_set_mpq(padic_t rop, const mpq_t op, const padic_ctx_t ctx) noexcept
    void padic_get_fmpz(fmpz_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    void padic_get_fmpq(fmpq_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    void padic_get_mpz(mpz_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    void padic_get_mpq(mpq_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    void padic_swap(padic_t op1, padic_t op2) noexcept
    void padic_zero(padic_t rop) noexcept
    void padic_one(padic_t rop) noexcept
    bint padic_is_zero(const padic_t op) noexcept
    bint padic_is_one(const padic_t op) noexcept
    bint padic_equal(const padic_t op1, const padic_t op2) noexcept
    slong * _padic_lifts_exps(slong * n, slong N) noexcept
    void _padic_lifts_pows(fmpz * pow, const slong * a, slong n, const fmpz_t p) noexcept
    void padic_add(padic_t rop, const padic_t op1, const padic_t op2, const padic_ctx_t ctx) noexcept
    void padic_sub(padic_t rop, const padic_t op1, const padic_t op2, const padic_ctx_t ctx) noexcept
    void padic_neg(padic_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    void padic_mul(padic_t rop, const padic_t op1, const padic_t op2, const padic_ctx_t ctx) noexcept
    void padic_shift(padic_t rop, const padic_t op, slong v, const padic_ctx_t ctx) noexcept
    void padic_div(padic_t rop, const padic_t op1, const padic_t op2, const padic_ctx_t ctx) noexcept
    void _padic_inv_precompute(padic_inv_t S, const fmpz_t p, slong N) noexcept
    void _padic_inv_clear(padic_inv_t S) noexcept
    void _padic_inv_precomp(fmpz_t rop, const fmpz_t op, const padic_inv_t S) noexcept
    void _padic_inv(fmpz_t rop, const fmpz_t op, const fmpz_t p, slong N) noexcept
    void padic_inv(padic_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    int padic_sqrt(padic_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    void padic_pow_si(padic_t rop, const padic_t op, slong e, const padic_ctx_t ctx) noexcept
    slong _padic_exp_bound(slong v, slong N, const fmpz_t p) noexcept
    void _padic_exp_rectangular(fmpz_t rop, const fmpz_t u, slong v, const fmpz_t p, slong N) noexcept
    void _padic_exp_balanced(fmpz_t rop, const fmpz_t u, slong v, const fmpz_t p, slong N) noexcept
    void _padic_exp(fmpz_t rop, const fmpz_t u, slong v, const fmpz_t p, slong N) noexcept
    int padic_exp(padic_t y, const padic_t x, const padic_ctx_t ctx) noexcept
    int padic_exp_rectangular(padic_t y, const padic_t x, const padic_ctx_t ctx) noexcept
    int padic_exp_balanced(padic_t y, const padic_t x, const padic_ctx_t ctx) noexcept
    slong _padic_log_bound(slong v, slong N, const fmpz_t p) noexcept
    void _padic_log(fmpz_t z, const fmpz_t y, slong v, const fmpz_t p, slong N) noexcept
    void _padic_log_rectangular(fmpz_t z, const fmpz_t y, slong v, const fmpz_t p, slong N) noexcept
    void _padic_log_satoh(fmpz_t z, const fmpz_t y, slong v, const fmpz_t p, slong N) noexcept
    void _padic_log_balanced(fmpz_t z, const fmpz_t y, slong v, const fmpz_t p, slong N) noexcept
    int padic_log(padic_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    int padic_log_rectangular(padic_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    int padic_log_satoh(padic_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    int padic_log_balanced(padic_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    void _padic_teichmuller(fmpz_t rop, const fmpz_t op, const fmpz_t p, slong N) noexcept
    void padic_teichmuller(padic_t rop, const padic_t op, const padic_ctx_t ctx) noexcept
    ulong padic_val_fac_ui_2(ulong n) noexcept
    ulong padic_val_fac_ui(ulong n, const fmpz_t p) noexcept
    void padic_val_fac(fmpz_t rop, const fmpz_t op, const fmpz_t p) noexcept
    char * padic_get_str(char * str, const padic_t op, const padic_ctx_t ctx) noexcept
    int _padic_fprint(FILE * file, const fmpz_t u, slong v, const padic_ctx_t ctx) noexcept
    int padic_fprint(FILE * file, const padic_t op, const padic_ctx_t ctx) noexcept
    int _padic_print(const fmpz_t u, slong v, const padic_ctx_t ctx) noexcept
    int padic_print(const padic_t op, const padic_ctx_t ctx) noexcept
    void padic_debug(const padic_t op) noexcept

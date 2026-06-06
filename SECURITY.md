# Security Audit Report

## Summary

This document describes the security issues found in the Stable Diffusion WebUI
Colab notebook (`stable/stable_diffusion_webui_colab.ipynb`) and the mitigations
applied.

---

## Critical Issues (Fixed)

### 1. `--enable-insecure-extension-access` — Unauthenticated Extension Installs

| Severity | CVSS-like | Status |
|----------|-----------|--------|
| **Critical** | 9.8 | **Fixed** |

**Problem:** The `--enable-insecure-extension-access` flag allowed *anyone* who
could reach the web UI to install arbitrary extensions without authentication.
Extensions execute arbitrary Python code, so this is equivalent to an
unauthenticated remote code execution (RCE) vulnerability.

**Fix:** Flag removed from the `launch.py` invocation.

---

### 2. `--listen` Without Authentication — Unauthenticated Network Exposure

| Severity | CVSS-like | Status |
|----------|-----------|--------|
| **Critical** | 9.1 | **Fixed** |

**Problem:** `--listen` binds Gradio to `0.0.0.0`, making the UI reachable from
any machine on the network (or the internet, in Colab's case). Without
`--gradio-auth`, **no credentials are required** to interact with the model,
upload images, or trigger arbitrary generation workloads.

**Fix:** Added `--gradio-auth` using credentials read from the `GRADIO_AUTH`
environment variable (defaults to `admin:changeme` — users **must** change
this).

---

## Medium Issues (Noted — Recommend Manual Follow-Up)

### 3. Unpinned Git Clones — Supply-Chain Risk

| Severity | Status |
|----------|--------|
| Medium | Partially mitigated |

**Problem:** ~17 extension repos are cloned at HEAD without pinning to a commit
SHA. If any upstream repo is compromised, malicious code runs automatically.

**Mitigation applied:** Added inline comment noting the risk. Full pinning
requires auditing each extension's latest safe commit — recommended as follow-up.

---

### 4. Remote Script Download & Execute

| Severity | Status |
|----------|--------|
| Medium | Noted |

**Problem:**
```
!wget https://raw.githubusercontent.com/camenduru/stable-diffusion-webui-scripts/main/run_n_times.py
```
This fetches an arbitrary Python file from a remote URL at runtime and drops it
into the scripts directory where it will be auto-loaded. A compromised upstream
(or DNS hijack) means instant code execution.

**Recommendation:** Vendor the script into this repo or pin to a commit SHA URL.

---

### 5. Outdated / Vulnerable Python Dependencies

| Severity | Status |
|----------|--------|
| Medium | Noted |

The notebook pins very old versions of PyTorch (2.0.1), xformers (0.0.20), and
triton (2.0.0). These versions have known CVEs. Upgrading is recommended when
compatibility allows.

---

## Low Issues

### 6. `sed`-based Source Patching

Runtime `sed` commands modify `launch.py` and `shared.py`. While not a direct
vulnerability, it makes auditing difficult and can mask injected code.

---

## Not Applicable

| Category | Finding |
|----------|---------|
| Hardcoded API keys / secrets | None found |
| SQL injection | N/A (no database) |
| CORS misconfiguration | N/A (Gradio handles CORS internally) |
| Exposed debug endpoints | N/A (no custom endpoints) |

---

## Recommendations

1. **Change the default `GRADIO_AUTH`** credentials before deploying.
2. **Pin all extension clones** to specific commit SHAs after auditing.
3. **Vendor remote scripts** (e.g., `run_n_times.py`) into the repository.
4. **Upgrade PyTorch / xformers / triton** to patched versions.
5. Consider using `--share` (Gradio tunnel) instead of `--listen` to avoid
   binding on all interfaces.

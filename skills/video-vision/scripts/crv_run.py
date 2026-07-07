#!/usr/bin/env python3
"""Resolve ffmpeg and run `crv` (claude-real-video).

WHY THIS EXISTS
  crv shells out to `ffmpeg` via subprocess + `shutil.which("ffmpeg")` (core.py).
  On Windows, ffmpeg is frequently NOT on PATH:
    - WinGet's Gyan.FFmpeg lands in a versioned package dir with no Links shim.
    - crv's own dep `imageio-ffmpeg` bundles a binary but names it
      `ffmpeg-win-x86_64-v7.1.exe` (no bare `ffmpeg` alias), so crv can't see it.
  This resolver finds ffmpeg through three strategies, puts its dir on PATH,
  then runs crv unchanged. Portable across machines without env mutation.

USAGE
  python crv_run.py --check            # resolve + report readiness (exit 0/1)
  python crv_run.py <source> [crv...]  # run crv with ffmpeg resolvable

  python crv_run.py --check && python crv_run.py "<url>" -o out --max-frames 30
"""
from __future__ import annotations
import glob, os, shutil, subprocess, sys


def _local_appdata() -> str:
    return os.environ.get("LOCALAPPDATA") or os.path.join(
        os.path.expanduser("~"), "AppData", "Local"
    )


def _alias_dir() -> str:
    """Per-user cache dir for a bare-`ffmpeg` alias when only the versioned
    imageio-ffmpeg binary exists. NTFS hard link = ~0 bytes, no admin."""
    return os.path.join(_local_appdata(), "cc-skills-media", "crv-ffmpeg-alias")


def _try_alias(src_exe: str) -> str | None:
    """Hard-link (or copy) src_exe as ffmpeg.exe in the alias dir; return that dir."""
    dst_dir = _alias_dir()
    dst = os.path.join(dst_dir, "ffmpeg.exe")
    os.makedirs(dst_dir, exist_ok=True)
    try:
        if os.path.exists(dst):
            if os.path.samefile(dst, src_exe):
                return dst_dir
            os.remove(dst)
        os.link(src_exe, dst)  # ponytail: hard link, free + no privilege on NTFS
        return dst_dir
    except OSError:
        try:  # cross-volume or unsupported: fall back to copy
            shutil.copyfile(src_exe, dst)
            return dst_dir
        except OSError:
            return None


def resolve_ffmpeg_dir() -> str | None:
    """Return a directory whose `ffmpeg` resolves, or None."""
    # 1. Already on PATH (POSIX or a correctly-installed Windows ffmpeg).
    if (p := shutil.which("ffmpeg")):
        return os.path.dirname(p)
    base = os.path.join(_local_appdata(), "Microsoft", "WinGet", "Packages")
    # 2. WinGet Gyan.FFmpeg package (versioned dir, no Links shim).
    for pat in (
        f"{base}/Gyan.FFmpeg*/ffmpeg*/bin/ffmpeg.exe",
        f"{base}/Gyan.FFmpeg*/**/bin/ffmpeg.exe",
    ):
        if hits := glob.glob(pat, recursive=True):
            return os.path.dirname(hits[0])
    # 3. imageio-ffmpeg bundled binary — alias it to bare ffmpeg.exe.
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.exists(exe):
            return _try_alias(exe)
    except Exception:
        pass
    return None


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("--check", "-c", "check"):
        ff = resolve_ffmpeg_dir()
        crv_ok = shutil.which("crv") is not None
        print(f"crv:     {'OK' if crv_ok else 'MISSING — pip install claude-real-video'}")
        print(f"ffmpeg:  {ff or 'MISSING — winget install Gyan.FFmpeg'}")
        print("READY" if ff and crv_ok else "NOT READY")
        return 0 if (ff and crv_ok) else 1
    ffdir = resolve_ffmpeg_dir()
    if not ffdir:
        sys.stderr.write(
            "ffmpeg not found. Install Gyan.FFmpeg (winget) or ensure imageio-ffmpeg "
            "is importable (bundled with crv).\n"
        )
        return 2
    sep = ";" if os.name == "nt" else ":"
    env = dict(os.environ)
    env["PATH"] = ffdir + sep + env.get("PATH", "")
    sys.stderr.write(f"[crv_run] ffmpeg on PATH <- {ffdir}\n")
    return subprocess.call(["crv", *argv], env=env)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

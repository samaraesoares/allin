#!/usr/bin/env python3
"""
Organiza output do gallery-dl em carrosseis/reels/estaticos.
Mergea DASH órfão (*v.mp4 + *a.m4a) via ffmpeg.
Extrai prints (1 frame a cada 0.5s) pra cada reel.

Uso: organizar.py <raw_user_dir> <dest_dir> <ffmpeg_path>
"""
import os, sys, json, re, shutil, subprocess
from collections import defaultdict
from pathlib import Path

def slugify(text, maxlen=60):
    text = re.sub(r'[^\w\s-]', '', text or '', flags=re.UNICODE)
    text = re.sub(r'\s+', '_', text.strip())
    return text[:maxlen].strip('_')

def main():
    if len(sys.argv) != 4:
        print("Uso: organizar.py <raw_user_dir> <dest_dir> <ffmpeg_path>", file=sys.stderr)
        sys.exit(1)

    raw = Path(sys.argv[1])
    dest = Path(sys.argv[2])
    ffmpeg = sys.argv[3]

    reels_dir = dest / "reels"
    car_dir = dest / "carrosseis"
    est_dir = dest / "estaticos"
    for d in (reels_dir, car_dir, est_dir):
        d.mkdir(parents=True, exist_ok=True)

    # Agrupar arquivos por post_shortcode usando JSONs
    posts = defaultdict(lambda: {"files": [], "caption": "", "type": None, "json": []})

    for jpath in raw.rglob("*.json"):
        try:
            meta = json.loads(jpath.read_text())
        except Exception:
            continue
        sc = meta.get("post_shortcode") or meta.get("shortcode")
        if not sc:
            continue
        caption = meta.get("description") or meta.get("caption") or ""
        ptype = meta.get("type") or meta.get("category")
        posts[sc]["caption"] = caption
        posts[sc]["type"] = ptype
        posts[sc]["json"].append(jpath)

        # Achar arquivo de mídia correspondente (mesmo prefixo do .json)
        # gallery-dl gera "<filename>.<ext>.json" — então arquivo é <filename>.<ext>
        media = jpath.with_suffix("")  # remove .json
        if media.exists():
            posts[sc]["files"].append(media)

    # Pra cada post, classificar e mover
    count_reels = count_car = count_est = total_prints = 0

    for sc, info in posts.items():
        files = info["files"]
        caption_slug = slugify(info["caption"])
        postname = f"{sc}_{caption_slug}" if caption_slug else sc

        # Mergear DASH órfão se houver
        files = mergear_dash(files, ffmpeg)

        # Detectar tipos
        videos = [f for f in files if f.suffix.lower() in ('.mp4', '.mov', '.webm', '.mkv')]
        images = [f for f in files if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp')]

        if videos:
            # É reel/vídeo
            target = reels_dir / postname
            target.mkdir(exist_ok=True)
            for f in files:
                shutil.move(str(f), str(target / f.name))
            for j in info["json"]:
                if j.exists():
                    shutil.move(str(j), str(target / j.name))
            # Extrair prints de cada vídeo (pulável via GARIMPO_SKIP_PRINTS=1)
            if not os.environ.get("GARIMPO_SKIP_PRINTS"):
                prints_dir = target / "prints"
                prints_dir.mkdir(exist_ok=True)
                for v in target.glob("*.mp4"):
                    if v.name.endswith('v.mp4'):
                        continue  # ainda órfão por algum motivo
                    base = v.stem
                    subprocess.run([
                        ffmpeg, "-hide_banner", "-loglevel", "error",
                        "-i", str(v),
                        "-vf", "fps=2", "-q:v", "2",
                        str(prints_dir / f"{base}_%03d.jpg")
                    ], stdin=subprocess.DEVNULL, check=False)
                    pcount = len(list(prints_dir.glob(f"{base}_*.jpg")))
                    total_prints += pcount
            count_reels += 1

        elif len(images) > 1:
            # Carrossel
            target = car_dir / postname
            target.mkdir(exist_ok=True)
            for f in files:
                shutil.move(str(f), str(target / f.name))
            for j in info["json"]:
                if j.exists():
                    shutil.move(str(j), str(target / j.name))
            count_car += 1

        elif len(images) == 1:
            # Estático
            img = images[0]
            ext = img.suffix
            new_name = f"{postname}{ext}"
            shutil.move(str(img), str(est_dir / new_name))
            for j in info["json"]:
                if j.exists():
                    shutil.move(str(j), str(est_dir / f"{postname}.json"))
                    break
            count_est += 1

    print(f"\nConcluído.")
    print(f"  Reels:      {count_reels}  (prints: {total_prints})")
    print(f"  Carrosséis: {count_car}")
    print(f"  Estáticos:  {count_est}")
    print(f"  Caminho:    {dest}")


def mergear_dash(files, ffmpeg):
    """Procura *v.mp4 + *a.m4a órfãos e mergeia."""
    file_set = set(files)
    video_orphans = [f for f in files if f.name.endswith('v.mp4') or 'fdash-' in f.name and f.suffix == '.mp4']
    audio_orphans = [f for f in files if f.suffix == '.m4a']

    if not video_orphans or not audio_orphans:
        return files

    # Agrupar por prefixo (antes do "fdash-")
    by_prefix = defaultdict(lambda: {"video": [], "audio": []})
    for v in video_orphans:
        prefix = v.name.split('.fdash-')[0] if '.fdash-' in v.name else v.stem.rstrip('v')
        by_prefix[prefix]["video"].append(v)
    for a in audio_orphans:
        prefix = a.name.split('.fdash-')[0] if '.fdash-' in a.name else a.stem.rstrip('a')
        by_prefix[prefix]["audio"].append(a)

    new_files = list(files)
    for prefix, group in by_prefix.items():
        if not group["video"] or not group["audio"]:
            continue
        # Pegar maior qualidade (último na lista geralmente, ou maior tamanho)
        video = max(group["video"], key=lambda p: p.stat().st_size)
        audio = max(group["audio"], key=lambda p: p.stat().st_size)
        out = video.parent / f"{prefix}.mp4"
        try:
            subprocess.run([
                ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(video), "-i", str(audio), "-c", "copy", str(out)
            ], stdin=subprocess.DEVNULL, check=True)
            # Apagar TODOS os candidatos órfãos (não só o vencedor)
            for f in group["video"] + group["audio"]:
                if f.exists():
                    f.unlink()
                if f in new_files:
                    new_files.remove(f)
            new_files.append(out)
        except subprocess.CalledProcessError as e:
            print(f"  ✗ falhou merge {prefix}: {e}", file=sys.stderr)

    return new_files


if __name__ == "__main__":
    main()

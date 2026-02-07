# Brotli Compression Guide

## Checking Archive Size

```bash
ls -lh src.tar.br          # Human-readable size
stat -c%s src.tar.br       # Exact bytes
du -sh src.tar.br          # Disk usage
```

## Creating a Brotli Archive

```bash
# Standard compression
tar -cf - src/ | brotli -o src.tar.br

# Maximum compression
tar -cf - src/ | brotli -q 11 -o src.tar.br
```

## Compression Options

- `-q 11` or `--quality=11` - Highest quality, slowest (maximum compression)
- Default is `-q 11` for files, `-q 6` for streams
- Quality range: 0-11 (higher = better compression, slower)

## Extracting

```bash
brotli -d src.tar.br && tar -xf src.tar
```

## Current Project Stats

- Original: 205 bytes
- Compressed: 169 bytes (82.4% ratio)
- Note: Brotli works best with larger files (70-90% size reduction typical)

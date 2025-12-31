#!/usr/bin/env python3
"""
Font merging script for K-Shoot MANIA v2.
Merges Tektur, Corporate Logo, and Noto Sans fonts for each language.
"""

import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
FONT_DIR = PROJECT_ROOT / "src_fonts"
OUTPUT_DIR = PROJECT_ROOT

TEKTUR_FONT = FONT_DIR / "tektur-ksm/Tektur-KSM-Medium.ttf"
CORPORATE_LOGO_FONT = FONT_DIR / "corporate-logo/Corporate-Logo-Medium-ver3.otf"
NOTO_SANS_FONT = FONT_DIR / "noto-sans/NotoSans-Medium.ttf"
NOTO_SANS_MATH_FONT = FONT_DIR / "noto-sans/NotoSansMath-Regular.ttf"
NOTO_SANS_SYMBOLS_FONT = FONT_DIR / "noto-sans/NotoSansSymbols-Regular.ttf"
NOTO_SANS_SYMBOLS2_FONT = FONT_DIR / "noto-sans/NotoSansSymbols2-Regular.ttf"
NOTO_MUSIC_FONT = FONT_DIR / "noto-sans/NotoMusic-Regular.ttf"
NOTO_SANS_ARABIC_FONT = FONT_DIR / "noto-sans/NotoSansArabic-Medium.ttf"
NOTO_SANS_THAI_FONT = FONT_DIR / "noto-sans/NotoSansThai-Medium.ttf"
NOTO_SANS_HEBREW_FONT = FONT_DIR / "noto-sans/NotoSansHebrew-Medium.ttf"
NOTO_SANS_CHEROKEE_FONT = FONT_DIR / "noto-sans/NotoSansCherokee-Medium.ttf"
NOTO_SANS_JP_FONT = FONT_DIR / "noto-sans-jp/NotoSansJP-Medium.ttf"
NOTO_SANS_KR_FONT = FONT_DIR / "noto-sans-kr/NotoSansKR-Medium.ttf"
NOTO_SANS_SC_FONT = FONT_DIR / "noto-sans-sc/NotoSansSC-Medium.ttf"
NOTO_SANS_TC_FONT = FONT_DIR / "noto-sans-tc/NotoSansTC-Medium.ttf"


def check_fonts_exist():
	fonts = [
		TEKTUR_FONT, CORPORATE_LOGO_FONT,
		NOTO_SANS_FONT, NOTO_SANS_MATH_FONT,
		NOTO_SANS_SYMBOLS_FONT, NOTO_SANS_SYMBOLS2_FONT, NOTO_MUSIC_FONT,
		NOTO_SANS_ARABIC_FONT, NOTO_SANS_THAI_FONT,
		NOTO_SANS_HEBREW_FONT, NOTO_SANS_CHEROKEE_FONT,
		NOTO_SANS_JP_FONT, NOTO_SANS_KR_FONT,
		NOTO_SANS_SC_FONT, NOTO_SANS_TC_FONT,
	]
	missing = [f for f in fonts if not f.exists()]

	if missing:
		print("Error: Missing font files:")
		for font in missing:
			print(f"  - {font}")
		return False

	print("✓ All source fonts found")
	return True


def check_fontforge():
	try:
		result = subprocess.run(
			["fontforge", "--version"],
			capture_output=True,
			text=True,
			check=False
		)
		if result.returncode == 0:
			print(f"✓ FontForge: {result.stdout.strip().split()[0]}")
			return True
		else:
			print("Error: FontForge not properly installed")
			return False
	except FileNotFoundError:
		print("Error: FontForge not found")
		print("  Install: brew install fontforge")
		return False


def create_fontforge_script(font_list, output_path, script_path, font_name):
	script_content = f'#!/usr/bin/env fontforge\nOpen("{font_list[0]}")\n'
	for font in font_list[1:]:
		script_content += f'MergeFonts("{font}")\n'

	script_content += f'SetFontNames("{font_name}", "{font_name}", "{font_name}")\n'
	script_content += f'SetTTFName(0x409, 16, "{font_name}")\n'  # nameID 16: Typographic Family name (Windows)
	script_content += f'SetTTFName(0x409, 17, "Medium")\n'       # nameID 17: Typographic Subfamily name (Windows)
	script_content += f'SetTTFName(0x0, 16, "{font_name}")\n'    # nameID 16: Typographic Family name (Mac)
	script_content += f'SetTTFName(0x0, 17, "Medium")\n'         # nameID 17: Typographic Subfamily name (Mac)

	script_content += f'Generate("{output_path}")\n'

	with open(script_path, 'w') as f:
		f.write(script_content)


def merge_fonts(font_list, output_path, description, font_name):
	print(f"\n{'='*60}")
	print(f"Merging: {description}")
	print(f"{'='*60}")

	print("Input fonts:")
	for i, font in enumerate(font_list, 1):
		print(f"  {i}. {font.name}")

	try:
		output_path.parent.mkdir(parents=True, exist_ok=True)

		script_path = Path("temp_merge_script.pe")
		create_fontforge_script(
			[str(f.absolute()) for f in font_list],
			str(output_path.absolute()),
			script_path,
			font_name
		)

		print("Merging...")
		result = subprocess.run(
			["fontforge", "-script", str(script_path)],
			capture_output=True,
			text=True,
			encoding='utf-8',
			errors='replace',
			check=False
		)

		script_path.unlink()

		if result.returncode == 0:
			print(f"✓ Complete: {output_path}")
			if output_path.exists():
				size_mb = output_path.stat().st_size / (1024 * 1024)
				print(f"  Size: {size_mb:.2f} MB")
			return True
		else:
			print("Error: Merge failed")
			if result.stderr:
				print(f"Output:\n{result.stderr}")
			return False

	except Exception as e:
		print(f"Error: {e}")
		import traceback
		traceback.print_exc()
		return False


def main():
	print("K-Shoot MANIA v2 Font Merge Script")
	print("="*60)

	if not check_fontforge():
		sys.exit(1)

	if not check_fonts_exist():
		sys.exit(1)

	success_count = 0
	total_count = 0

	total_count += 1
	if merge_fonts(
		[TEKTUR_FONT, CORPORATE_LOGO_FONT,
		 NOTO_SANS_JP_FONT, NOTO_SANS_KR_FONT, NOTO_SANS_SC_FONT, NOTO_SANS_TC_FONT,
		 NOTO_SANS_FONT, NOTO_SANS_MATH_FONT, NOTO_SANS_SYMBOLS_FONT, NOTO_SANS_SYMBOLS2_FONT,
		 NOTO_MUSIC_FONT, NOTO_SANS_ARABIC_FONT, NOTO_SANS_THAI_FONT,
		 NOTO_SANS_HEBREW_FONT, NOTO_SANS_CHEROKEE_FONT],
		OUTPUT_DIR / "KSM-JA-Medium.ttf",
		"Japanese/Korean",
		"KSM-System-JA"
	):
		success_count += 1

	total_count += 1
	if merge_fonts(
		[TEKTUR_FONT,
		 NOTO_SANS_SC_FONT, NOTO_SANS_TC_FONT,
		 CORPORATE_LOGO_FONT,
		 NOTO_SANS_JP_FONT, NOTO_SANS_KR_FONT,
		 NOTO_SANS_FONT, NOTO_SANS_MATH_FONT, NOTO_SANS_SYMBOLS_FONT, NOTO_SANS_SYMBOLS2_FONT,
		 NOTO_MUSIC_FONT, NOTO_SANS_ARABIC_FONT, NOTO_SANS_THAI_FONT,
		 NOTO_SANS_HEBREW_FONT, NOTO_SANS_CHEROKEE_FONT],
		OUTPUT_DIR / "KSM-SC-Medium.ttf",
		"Simplified Chinese",
		"KSM-System-SC"
	):
		success_count += 1

	total_count += 1
	if merge_fonts(
		[TEKTUR_FONT,
		 NOTO_SANS_TC_FONT, NOTO_SANS_SC_FONT,
		 CORPORATE_LOGO_FONT,
		 NOTO_SANS_JP_FONT, NOTO_SANS_KR_FONT,
		 NOTO_SANS_FONT, NOTO_SANS_MATH_FONT, NOTO_SANS_SYMBOLS_FONT, NOTO_SANS_SYMBOLS2_FONT,
		 NOTO_MUSIC_FONT, NOTO_SANS_ARABIC_FONT, NOTO_SANS_THAI_FONT,
		 NOTO_SANS_HEBREW_FONT, NOTO_SANS_CHEROKEE_FONT],
		OUTPUT_DIR / "KSM-TC-Medium.ttf",
		"Traditional Chinese",
		"KSM-System-TC"
	):
		success_count += 1

	print(f"\n{'='*60}")
	print(f"Complete: {success_count}/{total_count} successful")
	print(f"{'='*60}")

	if success_count == total_count:
		print("\nGenerated fonts:")
		print("  - KSM-JA-Medium.ttf (Japanese/Korean)")
		print("  - KSM-SC-Medium.ttf (Simplified Chinese)")
		print("  - KSM-TC-Medium.ttf (Traditional Chinese)")
	else:
		sys.exit(1)


if __name__ == "__main__":
	main()

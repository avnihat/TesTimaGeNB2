# quick smoke test script (run: python tests_smoke.py path/to/image.jpg)
import sys, json
from main import analyze_image

if __name__ == '__main__':
    res, pdf = analyze_image(sys.argv[1])
    print(json.dumps(res, ensure_ascii=False, indent=2))
    print('PDF:', pdf)

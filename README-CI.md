# GitHub Üzerinde Sadece Derleme ve Zip Hazırlama

Bu paket yalnızca **GitHub Actions** ile repo içeriğini zip'leyip **artifact** olarak eklemek içindir.
Yerelde derleme yoktur.

## Kurulum
1. Bu arşivi açın ve `.github/workflows/build.yml` dosyasını projenizin köküne (aynı klasör yapısıyla) ekleyin.
2. Commit & push yapın.

```bash
git add .github/workflows/build.yml
git commit -m "CI: Build-and-Zip workflow"
git push
```

## Çalışma
- `main` dalına yapılan her push'ta veya manuel `workflow_dispatch` ile çalışır.
- `dist/` altında bir `*-source.zip` üretir ve **Actions → Artifacts** bölümüne yükler.
- Kodunuzda macOS Intel Mojave+ platform kontrolü varsa, CI içinde `CI_ALLOW_NON_INTEL=1` ile otomatik bypass edilir.

> İsterseniz artifact yerine **Release** yüklemesi de yapabiliriz. Bunun için `actions/upload-release-asset` veya `softprops/action-gh-release` eklenir.

# RHHanson-UMD Learning Lab

Central hub for [RHHanson-UMD](https://github.com/RHHanson-UMD) course sites.

## Site

Expected GitHub Pages URL: https://rhhanson-umd.github.io/

The static website lives in `site/`. Edit `content/resources.json` to add or
reorganize references, and `content/courses.json` to add courses. Run
`python scripts/build.py` to refresh the generated homepage. The GitHub Actions
workflow also runs this build automatically before publishing.

### Local preview

```sh
python -m http.server 8000 -d site
```

Visit http://localhost:8000/.

## Deployment

This repository deploys with GitHub Actions. On GitHub choose Settings > Pages >
Build and deployment > Source: GitHub Actions. The workflow publishes `site/`.

## Courses

- [ENEE 620](https://rhhanson-umd.github.io/ENEE-620/)
- [ENEE 630](https://rhhanson-umd.github.io/ENEE-630/)
- [ENEE 641](https://rhhanson-umd.github.io/ENEE-641/)

## Editorial policy

This is an independent learning project, not an official UMD website.
Credit external references. Do not publish unreleased homework solutions or
non-redistributable class materials. Publication of any released solution is
subject to sharing permission, not merely the date of release.

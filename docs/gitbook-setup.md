# Setting Up GitBook

This documentation is written to be published with **GitBook**, synced directly from
this GitHub repo. Here's how to connect it, step by step.

## How this repo is structured for GitBook

```text
ByGoneSpoofer/
├── .gitbook.yaml          # tells GitBook where the docs live
└── docs/
    ├── README.md          # the landing page
    ├── SUMMARY.md         # the sidebar / table of contents
    ├── getting-started/
    ├── usage/
    ├── guides/
    ├── warnings/
    ├── troubleshooting.md
    └── images/            # drop real screenshots here
```

* **`.gitbook.yaml`** (repo root) points GitBook at `./docs/` and names the `README.md`
  and `SUMMARY.md` files.
* **`docs/SUMMARY.md`** is the table of contents — every page in the sidebar is listed
  there. Add a bullet here whenever you add a new page.

## Step-by-step: connect GitBook to GitHub

1. **Create a GitBook account** at [gitbook.com](https://www.gitbook.com/) and create a
   new **Space** (or an Organization + Space).
2. In the space, open **Settings → Integrations → GitHub** (also called *Git Sync*) and
   **install/authorize** the GitBook GitHub app for your account.
3. Choose the repository **`nitaybl/ByGoneSpoofer`** and the branch you want to publish
   (usually `main`).
4. **Set the sync direction.** GitBook supports two-way sync:
   * *GitHub → GitBook* if you edit Markdown in the repo (recommended for this setup).
   * *GitBook → GitHub* if you'd rather edit in GitBook's editor and have it commit back.
5. GitBook reads **`.gitbook.yaml`** automatically and picks up `docs/` as the root, with
   `SUMMARY.md` as the sidebar. No extra path config needed.
6. Click **Sync** — your pages appear in GitBook.
7. **Publish:** open **Share / Publish** and choose *Publish to the web* to get a public
   docs URL, or *Publish in collection* for a private/team space.

{% hint style="success" %}
✅ After the first sync, every push to the repo updates the docs automatically.
{% endhint %}

## Adding real screenshots

The docs currently use text mock-ups of the loader. To use real screenshots:

1. Take screenshots of the console and save them as PNGs.
2. Drop them into **`docs/images/`** (e.g. `loader-menu.png`).
3. Reference them in any page:

   ```markdown
   ![Main menu](images/loader-menu.png)
   ```

4. Commit and push — GitBook re-syncs and shows the images.

## Editing tips

* **New page?** Create the `.md` file under `docs/`, then add it to `docs/SUMMARY.md` so
  it shows in the sidebar.
* **Callout banners** use GitBook hint blocks:

  ```markdown
  {% hint style="warning" %}
  ⚠️ Your warning text here.
  {% endhint %}
  ```

  Styles: `info` (blue), `success` (green), `warning` (yellow), `danger` (red).
* **Local preview:** the Markdown renders fine on GitHub too, so you can sanity-check
  before syncing.

## Troubleshooting the sync

| Problem | Fix |
| --- | --- |
| Pages missing from sidebar | Make sure they're listed in `docs/SUMMARY.md` |
| Wrong root folder | Check `.gitbook.yaml` has `root: ./docs/` |
| Images not showing | Confirm the path is relative to the `.md` file and the file is committed |
| Sync not triggering | Re-check the GitHub integration and selected branch in GitBook settings |

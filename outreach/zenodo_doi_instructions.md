# Step-by-Step Guide: Minting a Permanent Academic DOI via Zenodo

To make this paper permanently citeable in academic journals, Google Scholar, and the NASA Astrophysics Data System (NASA ADS), you can mint an official Digital Object Identifier (DOI) in under 3 minutes via CERN's **Zenodo** archive.

We have already created the configuration file **[`.zenodo.json`](file:///d:/projects/martian-cylinder/.zenodo.json)** in your repository root, which tells Zenodo the exact academic title, author metadata, abstract, license, and keywords.

---

### 3-Step Procedure:

#### Step 1: Link Your GitHub Account to Zenodo
1. Go to **[https://zenodo.org](https://zenodo.org)**.
2. Click **Log In** in the top-right corner and select **Log in with GitHub**.
3. Authorize Zenodo with your GitHub account (`cambrianminds`).

#### Step 2: Enable the Martian Cylinder Repository
1. In Zenodo, navigate to your GitHub settings page:  
   👉 **[https://zenodo.org/account/settings/github/](https://zenodo.org/account/settings/github/)**
2. Find **`cambrianminds/martian-cylinder`** in your list of repositories.
3. Flip the toggle switch to **ON** (Enabled).

#### Step 3: Trigger a Release on GitHub
1. Go to your repository on GitHub: **`https://github.com/cambrianminds/martian-cylinder/releases/new`**
2. Create a new release:
   * **Tag version**: `v1.0.0`
   * **Release title**: `v1.0.0 — Sol 3556 Martian Cylinder Photogrammetry & Verification Suite`
   * **Description**: Copy/paste the summary from `README.md`.
3. Click **Publish release**.

---

### What Happens Automatically:
1. **Zenodo mints an official DOI** (format: `10.5281/zenodo.XXXXXXX`).
2. **Metadata is pushed to DataCite & OpenAIRE**, which feeds directly into **NASA ADS** and **Google Scholar**.
3. Zenodo provides an official DOI badge (SVG) that you can embed in your `README.md` and website:
   ```markdown
   [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
   ```
4. Your paper is now permanently archived and cannot be lost or deleted.

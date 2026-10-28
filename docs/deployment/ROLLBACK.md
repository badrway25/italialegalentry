# Italy Legal Entry™ — rollback

> Companion of [`PRODUCTION_DEPLOYMENT_RUNBOOK.md`](PRODUCTION_DEPLOYMENT_RUNBOOK.md) (names, paths, `ile-manage`)
> and [`PRODUCTION_CHECKLIST.md`](PRODUCTION_CHECKLIST.md) (§C backup, §D smoke test). Written 12 October 2026 from
> the repository; nothing in it has been run on a server. Updated 16 October 2026 by W4-D (release engineering): the
> previous tag's example (`v2.0.0`) and section 7, the pre-V5 reference tag `pre-v5-main-2026-10`; the same day, by its
> review fixes: section 7's migration check (a pattern that lists the files) and V5.10's own words for the tag.

A rollback is chosen, not improvised: decide which of the four below applies, write down the time, the running tag
and the reason, then act.

| What went wrong | Rollback | Section |
|---|---|---|
| the first cutover: the new site misbehaves and the old one is intact | **DNS back to the old site** (inside the TTL window) | [5](#5-dns-rollback-during-the-ttl-window) |
| a new release breaks, its migrations were code-rollback-safe (section 1) or absent | **application to the previous tag** | [1](#1-application-rollback-to-the-previous-tag) |
| a new release breaks and a migration removed or rewrote data | **database restore** from the verified pre-migration dump, then the previous tag | [2](#2-database-forward-only-and-what-that-means) · [3](#3-restore-the-database-from-the-verified-dump) |
| files lost or damaged in the private or public storage | **storage restore**, together with the matching database | [4](#4-private-and-public-storage) |

Going back to the platform before V5 — the tag `pre-v5-main-2026-10` — is none of the four: it was never deployed
here, and returning to it is a new deployment decision, not a rollback ([7](#7-the-pre-v5-platform-pre-v5-main-2026-10)).

Before any of them: `sudo ile-manage showmigrations` and `sudo git -C /srv/italylegalentry/app describe --tags` — know
what is running (`sudo`: the checkout belongs to root, and git refuses another user's repository).

## 1. Application rollback to the previous tag

Safe only when every migration the release being undone added is **code-rollback-safe** — the previous code keeps
working on the newer schema: `CreateModel`, an `AddField` that is nullable or has a `db_default`, a non-unique
`AddIndex`. Nothing else. A NOT NULL `AddField` with only a Python `default` is **not** safe: Django 5.2 adds the
column with a temporary database default, fills it, then drops that default (unless the field has `db_default`), so
the previous code's `INSERT`s, which do not name the column, fail with a NOT NULL violation — sign-ups, uploads and
forms answer 500. A new unique constraint or unique index can refuse the previous code's writes the same way. Find
out first:

```bash
PREVIOUS_TAG=v2.0.0                    # replace: the tag that ran before (v2.0.0 at the first update after it)
PREVIOUS_SHA=0000000000000000000000000000000000000000   # its SHA, from the previous handoff
sudo git -C /srv/italylegalentry/app diff --name-only "refs/tags/$PREVIOUS_TAG" HEAD -- 'apps/*/migrations/*.py'
# Nothing listed: code-only rollback. Files listed: read every operation. Only CreateModel, AddField with null=True
# or a db_default, and a non-unique AddIndex -> this section. Anything else -> sections 2 and 3: a NOT NULL AddField
# with a Python default only, a unique constraint or index, RemoveField, DeleteModel, RenameField, an AlterField that
# narrows, RunPython.
```

The application is stopped while its code changes, as during an update (runbook step 15): a worker started on the
way would load half of one release and half of the other. nginx answers the maintenance page meanwhile.

```bash
sudo systemctl stop 'italylegalentry-*.timer' 'italylegalentry-*.service' italylegalentry.socket italylegalentry.service
sudo git -C /srv/italylegalentry/app checkout --detach "refs/tags/$PREVIOUS_TAG"
test "$(sudo git -C /srv/italylegalentry/app rev-parse HEAD)" = "$PREVIOUS_SHA" && echo "SHA OK" || echo "SHA MISMATCH — STOP"
sudo /srv/italylegalentry/venv/bin/python -m pip install --no-cache-dir -r /srv/italylegalentry/app/requirements/base.txt -c /srv/italylegalentry/app/requirements/constraints.txt
sudo /srv/italylegalentry/venv/bin/python -m pip check
sudo ile-manage collectstatic --noinput        # never --clear: both releases' hashed files may be referenced
sudo ile-manage check --deploy
sudo systemctl start italylegalentry.socket italylegalentry.service
sudo systemctl start $(systemctl list-unit-files 'italylegalentry-*.timer' --no-legend | cut -d' ' -f1)
```

Then the smoke test (checklist §D). The previous tag's code runs on a schema that is ahead of it: `showmigrations`
lists the newer migrations as applied, and that is expected. Do **not** run `migrate` with the old code — there is
nothing for it to do, and it must not try.

## 2. Database: forward-only, and what that means

Migrations are treated as **forward-only** in production.

- **Code-rollback-safe** operations (`CreateModel`, a nullable `AddField`, an `AddField` with `db_default`, a
  non-unique `AddIndex`): the previous code keeps working on the newer schema — application rollback only
  (section 1). Unapplying them is possible (`migrate <app> <previous migration>`), but it **drops the new tables and
  columns with whatever was written into them**; it is done only if that data can be discarded, after reading
  `sqlmigrate <app> <migration> --backwards` and `migrate <app> <previous migration> --plan`.
- **Additive, yet not code-rollback-safe**: a NOT NULL `AddField` with only a Python `default` — Django drops the
  temporary database default once the column is filled, so the previous code's inserts fail — and any unique
  constraint or unique index, which can refuse the previous code's writes. Going back from such a release is a
  restore (section 3), unless it followed the two-release rule below (release N adds the column nullable or with a
  `db_default`, release N+1 makes it required).
- **Reductive or rewriting** operations (`RemoveField`, `DeleteModel`, a rename, an `AlterField` that narrows a type,
  a `RunPython` data migration — with or without reverse code): the data they removed or changed is **not** brought
  back by unapplying them. Django recreates an empty column at best. The way back is the restore of the dump taken
  just before `migrate` (section 3), accepting the loss of every write made since that dump.
- The rule that keeps rollbacks cheap (`docs/DEPLOYMENT_READINESS.md` §5.2): a reductive change — and an additive
  one that is not code-rollback-safe — ships in **two releases** — release N stops using the column (or adds it
  nullable), release N+1 removes it (or makes it required) — so going back from N+1 to N never meets a schema the code
  cannot write to. A handoff names any migration that breaks the rule.
- At the **first deployment** the database is new and holds nothing that matters yet: a failed migration is undone by
  dropping and re-creating the database (runbook step 6) and running step 7 again.

## 3. Restore the database from the verified dump

Only a dump that passed a restore check is a rollback point: the rollback dump of runbook step 15 (its step 4,
`/var/backups/italylegalentry/pre-update-<TS>.dump`, checked when it was taken), or a nightly set that checklist C-6
restored. Everything written after it is lost: write down the window (dump time → restore time).

A nightly set is encrypted to the owner's key, which never comes to the server. On the owner's machine, with
`umask 077`: `sha256sum -c "SHA256SUMS-<WHEN>"`, `gpg --decrypt --output db.dump "db-<WHEN>.dump.gpg"`; copy `db.dump`
to your home directory on the server (`scp`), use it as `DUMP` below, and delete both plain copies afterwards — they
hold personal data in clear.

```bash
TS=$(date -u +%Y%m%dt%H%Mz)            # lower case: PostgreSQL folds the unquoted name below, dropdb quotes it
DUMP=/var/backups/italylegalentry/pre-update-YYYYMMDDtHHMMz.dump      # replace: the verified dump
sudo systemctl stop 'italylegalentry-*.timer' 'italylegalentry-*.service' italylegalentry.socket italylegalentry.service
# Keep the failed state for the analysis — it holds personal data: drop it as soon as it is understood.
sudo -u postgres psql -v ON_ERROR_STOP=1 -c "ALTER DATABASE italylegalentry RENAME TO italylegalentry_failed_$TS;"
sudo -u postgres createdb -O italylegalentry -E UTF8 -T template0 italylegalentry
sudo cat "$DUMP" | sudo -u postgres pg_restore --no-owner --role=italylegalentry -d italylegalentry
```

Then, of section 1's second block, **only** the checkout, the SHA test, the two `pip` lines and `collectstatic` —
not its start lines — for the tag that matches the dump (the tag that was running when it was taken), and:

```bash
sudo ile-manage migrate --check && echo "schema and code agree"
sudo systemctl start italylegalentry.socket italylegalentry.service
sudo systemctl start $(systemctl list-unit-files 'italylegalentry-*.timer' --no-legend | cut -d' ' -f1)
```

Smoke test (checklist §D). When the failure is understood: `sudo -u postgres dropdb "italylegalentry_failed_$TS"`
— the same lower-case name (`sudo -u postgres psql -l | grep _failed_` shows it). With an upper-case `T`/`Z` the
rename folded the name and this `dropdb` failed, leaving the copy of personal data behind (reproduced on
PostgreSQL 17; the lower-case form was checked there too).

## 4. Private and public storage

The database and the private documents describe each other: a row without its file is a document nobody can open,
a file without its row is personal data nobody can find to delete. **Restore them together, from the same backup
set** (`ile-backup` dumps the database, then archives the files; checklist §C and runbook step 15 take a set with
the application stopped).

The sets are encrypted to the owner's key, which never comes to the server. On the owner's machine, with
`umask 077`, in the directory holding the set (the off-server copy, or the encrypted files fetched from
`/var/backups/italylegalentry`): `sha256sum -c "SHA256SUMS-<WHEN>"`, then
`gpg --decrypt --output private.tar.gz "private-<WHEN>.tar.gz.gpg"` — and `media-…` if it is part of the problem,
`db-…` for section 3. Copy the plain archives to your home directory on the server (`scp`), then:

```bash
TS=$(date -u +%Y%m%dt%H%Mz)
sudo systemctl stop 'italylegalentry-*.timer' 'italylegalentry-*.service' italylegalentry.socket italylegalentry.service
sudo mv /var/lib/italylegalentry/private "/var/lib/italylegalentry/private.failed-$TS"
sudo tar -C /var/lib/italylegalentry -xzpf ~/private.tar.gz
sudo chown -R italylegalentry:italylegalentry /var/lib/italylegalentry/private && sudo chmod 0700 /var/lib/italylegalentry/private
# public media, if it is part of the problem:
sudo mv /var/lib/italylegalentry/media "/var/lib/italylegalentry/media.failed-$TS"
sudo tar -C /var/lib/italylegalentry -xzpf ~/media.tar.gz
sudo chown -R italylegalentry:www-data /var/lib/italylegalentry/media && sudo chmod 2750 /var/lib/italylegalentry/media
rm -f ~/private.tar.gz ~/media.tar.gz     # plain copies of personal data: never left behind (and on your machine too)
```

Then section 3 for the database of the same set, start, smoke test. Files uploaded after the backup are in the
`*.failed-*` copy: they are personal data — decide what happens to them (the owner, with the data-protection
reference), never delete them silently, and remove the copy once decided. The library photographs alone can also be
re-created with `sudo ile-manage seed_all --only cms.media`.

## 5. DNS rollback during the TTL window

At the **first** cutover there is no previous tag on the new server: the rollback is to point the domain back at the
current site, which stayed running and untouched (cutover steps 4 and 10).

1. At the DNS host, set the `A` and `AAAA` records of the apex and `www` back to the values written down at cutover
   step 5 — re-create an `AAAA` record step 6 removed. Nothing else changes — MX and TXT were never touched.
2. Check: `dig @1.1.1.1 +short <domain> A` and `dig @8.8.8.8 +short <domain> A` return the old address. With the
   TTL at 300 s most resolvers follow within minutes; a few caches hold longer — keep the new server running
   meanwhile, it still answers whoever reaches it.
3. HTTPS: the old site must serve valid HTTPS. A browser that has seen this application's HSTS header refuses plain
   HTTP to the host for a year — the reason the template keeps `includeSubDomains` and `preload` off at the cutover,
   and the reason to confirm the old site's certificate before cutover step 6.
4. Accounts, uploads or form submissions made on the new site during the window stay on the new server, under its
   protection: they are not copied to the old site. Record the window; the owner decides what is said to whom.

After the TTL window **and** 72 hours of stable service, the DNS rollback is no longer the plan; a rollback becomes
sections 1–4.

## 6. What makes a rollback safe or unsafe

**Safe**

- code-only change, or only code-rollback-safe migrations (section 1), with the previous tag's SHA known, the
  application stopped while the code changes;
- a pre-migration dump that **was restored and checked** (checklist C-6), and the window of lost writes accepted;
- database and private storage restored from the same moment;
- the DNS records' previous values written down, the TTL lowered in advance, the old site intact and on valid HTTPS.

**Unsafe**

- a migration that **drops or rewrites data** followed by a code-only rollback — the old code meets a schema it
  does not know — or by `migrate` backwards, which brings back empty columns, not the data;
- a NOT NULL column added with only a Python default, or a unique constraint, followed by a code-only rollback: the
  previous code's writes fail;
- switching the code while the application runs;
- a «backup» that was never restored;
- the private storage restored without its database, or the reverse;
- rotating `DJANGO_SECRET_KEY` (signs everyone out, voids every signed link) or `IP_HASH_SALT` (breaks every stored
  hash) as part of a rollback — neither is a rollback step;
- `collectstatic --clear` while workers of the other release still run;
- expecting e-mails already sent to be recalled: the `EmailOutbox` is the record of what left, not an undo list.

After any rollback: write down the time, the tag before and after, the reason, the window of lost writes; tell the
owner; drop the `*_failed_*` database and the `*.failed-*` directories once the failure is understood.

## 7. The pre-V5 platform: `pre-v5-main-2026-10`

`pre-v5-main-2026-10` is the tag that preserves GitHub's `main` as it was before the V5 release was promoted —
`a3ac318304beb4504134762bfa6e9c4e4ce600f1`, the platform before V5 (runbook, *RELEASE TAGS*). The owner's directive
V5.10 calls it «a rollback/reference point, not the final release tag»: a point of the repository's history, **never a
rollback target of this server**:

- **It was never deployed.** The first release this server runs is `v2.0.0`, so at the first deployment there is no
  previous tag: the rollback is the DNS rollback (section 5). From the first update on, section 1 returns to the tag
  that ran before — `v2.0.0` or a later one, never further back.
- **It predates fixes this release ships**: the back-office sign-in that accepted a password alone (F-5, checklist
  A-13), a person moving their own case file into operator states (F-7), what the back office let an operator read
  and change (F-8), and the 500 a NUL byte caused (a 400 now, checklist A-21). Checked out on a server that holds real
  data, it would re-open all of them. Returning to the pre-V5 platform would be a new deployment decision of the owner,
  with its own release gate — not a rollback.
- **The database.** No migration differs between the two at `v2.0.0`: the 39 migration files of `pre-v5-main-2026-10`
  and of the release are identical, byte for byte (checked on the release candidate after F-8, W4-B and W4-D, 27 October
  2026; the release tests pin each file's content, so an edited or removed one fails them), and the pre-V5 code would
  meet a schema it knows. A migration added by a later release is that release's business (section 1). To check it on
  the tags themselves — this prints nothing when no migration differs, and lists each one that does (the pattern names the files: git matches a pattern that holds a wildcard against the whole
  path, so a directory written with a wildcard matches nothing):

  ```bash
  git diff --name-status pre-v5-main-2026-10 v2.0.0 -- 'apps/*/migrations/*.py'
  ```

  The rule stands regardless: **a downgrade is never a `migrate` backwards on live data.** Across a migration that is
  not code-rollback-safe (section 1's list), the way back is the restore of the verified dump taken just before that
  release's `migrate` (runbook step 15, item 4; section 3), accepting the loss of every write made since. At the first
  deployment there is no such dump to return to: the database started empty (runbook step 6), and what is written
  under `v2.0.0` stays on this server, under its protection, until the owner decides otherwise (section 5, item 4).

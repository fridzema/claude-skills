# claude-skills

Personal collection of [Claude](https://claude.com/claude-code) skills.

Each skill lives in its own directory at the repo root and follows the standard
skill layout (`SKILL.md` + optional `references/`, `scripts/`, `assets/`).
Source is kept unpacked for easy diffing and editing; `bundle.sh` produces
distributable `.skill` archives on demand.

## Skills

| Skill | Description |
|---|---|
| [`dutch-humanizer`](./dutch-humanizer) | Verwijdert AI-schrijfpatronen uit Nederlandstalige tekst. Detecteert 37 patronen (opgeblazen belang, vulzinnen, vertalings-Nederlands, ...). |

## Install

Skills can be installed by either pointing Claude at the source directory or
by dropping a built `.skill` bundle into your skills folder.

### From source (recommended for local dev)

```bash
git clone git@github.com:fridzema/claude-skills.git ~/code/claude-skills
ln -s ~/code/claude-skills/dutch-humanizer ~/.claude/skills/dutch-humanizer
```

### From a built bundle

```bash
./bundle.sh dutch-humanizer
# -> dist/dutch-humanizer.skill
```

Then install the `.skill` file via your Claude client's skill installer.

## Layout

```
claude-skills/
├── <skill-name>/
│   ├── SKILL.md          # frontmatter + instructions
│   ├── references/       # optional supporting docs
│   ├── scripts/          # optional executable helpers
│   └── assets/           # optional static files
├── bundle.sh             # zip skills into dist/*.skill
├── dist/                 # build output (gitignored)
├── LICENSE
└── README.md
```

`SKILL.md` frontmatter must include at minimum:

```yaml
---
name: skill-name
description: >
  One-paragraph description. Include trigger phrases so Claude knows when
  to invoke the skill.
license: MIT
---
```

## Adding a new skill

1. `mkdir <skill-name>` at repo root.
2. Create `<skill-name>/SKILL.md` with frontmatter + instructions.
3. Add a row to the **Skills** table above.
4. `./bundle.sh <skill-name>` to verify it packages cleanly.
5. Commit.

## Bundling

```bash
./bundle.sh                 # bundle all skills
./bundle.sh dutch-humanizer # bundle one
```

Output goes to `dist/<skill-name>.skill` (a zip archive containing the skill
directory).

## License

MIT — see [LICENSE](./LICENSE).

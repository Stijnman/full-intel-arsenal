# Quickstart Guide — Full Intel Arsenal

## 1. Install the Skills

```bash
git clone https://github.com/Stijnman/full-intel-arsenal.git
cd full-intel-arsenal

# Copy everything into your Grok skills directory
cp -r skills/* /home/workdir/.grok/skills/
```

## 2. Activate Skills

The skills activate automatically based on your query. You can also force a specific mode:

- **Monster mode** (recommended for most cases): Just talk naturally. The unified skill will route to the right capability or combine them.
- **Specific skill**: Mention the skill name or be very explicit (e.g., "Use competitive-github-analysis on this repo...").

## 3. Example Workflows

### Competitive GitHub Analysis
```
Analyze https://github.com/owner/repo and give me a prioritized roadmap with gh commands.
```

### OSINT
```
Do a full OSINT investigation on target@example.com with confidence levels and sources.
```

### YouTube
```
Give me the best way to upload a video and get transcripts for my channel UCxxxx using the official tools.
```

### 0-Day
```
What are the current active critical 0-days affecting web servers and how do I mitigate them immediately?
```

## 4. Pro Tips

- The monster skill (`full-intel-arsenal`) is usually the best starting point.
- All skills output ready-to-copy `gh` commands and code blocks.
- For complex tasks, the skills can chain (e.g., OSINT on a repo owner → competitive analysis of their repo → check dependencies for 0-days).

## 5. Updating Skills

```bash
cd full-intel-arsenal
git pull
cp -r skills/* /home/workdir/.grok/skills/
```

Enjoy operating at a higher level.
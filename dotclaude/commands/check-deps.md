---
description: Analyze file dependencies before moving or reorganizing
allowed-tools: Bash, Read, Grep
---

**Dependency Check Workflow**

Analyze dependencies before moving files to ensure nothing breaks.

Arguments: "$ARGUMENTS" (file or directory to analyze)

---

## Analysis Steps:

### 1. **Internal Dependencies**
Check the file(s) for:
- Relative path references (`../`, `./`, `__file__`, `dirname`)  
- Local imports (Python: `from local_module import`)
- Path manipulations (`sys.path.insert`, `sys.path.append`)
- File references (non-absolute paths in `open()` calls)

### 2. **External Dependencies**
Search for other files that reference this one:
- Grep in parent/sibling directories for the filename
- Check shell scripts that might call it
- Look for imports in Python files

### 3. **Symlink Dependencies**
Find symlinks pointing to these files:
- Check parent directory for symlinks
- Use `find -type l` and check with `readlink`
- Note which symlinks would need updating

### 4. **System Dependencies**
Check if referenced by:
- Cron jobs (`crontab -l`, `/etc/cron*`)
- Systemd services (`/etc/systemd/system/`)
- Shell scripts in `/usr/local/bin/`

### 5. **Summary**
Based on findings, determine:
- ✅ **Safe to move** - No dependencies or only absolute paths
- ⚠️ **Update required** - Symlinks or references need updating
- ❌ **Cannot move** - Would break relative imports or hard dependencies

---

**Quick Command:**
```bash
# Use the depcheck tool for automated analysis (local tool, if installed; unrelated to npm depcheck)
depcheck <file/directory> [destination]
```

**Manual Checks:**
```bash
# Internal deps
grep -n "\.\.\/\|\.\/\|__file__\|dirname" file.py

# External refs  
grep -r "filename" ../ --include="*.py" --include="*.sh"

# Symlinks
find .. -type l -exec readlink {} \; | grep filename

# System deps
crontab -l | grep filename
sudo grep -r filename /etc/cron* /etc/systemd/
```
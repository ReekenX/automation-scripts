#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "prettytable",
# ]
# ///

"""
Calculate Git statistics for Remigijus in 2025.
Python version of calculate_lines.sh script.
Run with: uv run ~/Work/calculate_lines.py
"""

import subprocess
import os
from collections import defaultdict
from typing import Dict, List
from prettytable import PrettyTable


# File extensions to skip
SKIP_EXTENSIONS = {
    "lock",      # yarn.lock, package-lock.json, Gemfile.lock, etc.
    "svg",       # SVG images
    "min.js",    # Minified JavaScript
    "min.css",   # Minified CSS
    "map",       # Source maps
    "ico",       # Icon files
    "png",       # PNG images
    "jpg",       # JPG images
    "jpeg",      # JPEG images
    "gif",       # GIF images
    "woff",      # Web fonts
    "woff2",     # Web fonts
    "ttf",       # TrueType fonts
    "eot",       # Embedded OpenType fonts
}


def find_git_repos(base_path: str = "~/Work", max_depth: int = 3) -> List[str]:
    """Find all git repositories under the base path."""
    base_path = os.path.expanduser(base_path)
    cmd = f"find {base_path} -maxdepth {max_depth} -type d -name '.git' -exec dirname {{}} \\;"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        repos = [repo.strip() for repo in result.stdout.splitlines() if repo.strip()]
        return repos
    except Exception as e:
        print(f"Error finding repositories: {e}")
        return []


def should_skip_file(filename: str) -> bool:
    """Check if file should be skipped based on extension."""
    for ext in SKIP_EXTENSIONS:
        if filename.endswith(f".{ext}"):
            return True
    return False


def get_repo_statistics(repo_path: str) -> Dict[str, int]:
    """Get line statistics for a repository grouped by week."""
    week_stats = defaultdict(int)
    
    # Check if it's a valid git repository
    check_cmd = "git rev-parse --git-dir"
    try:
        result = subprocess.run(check_cmd, shell=True, cwd=repo_path, 
                              capture_output=True, text=True, timeout=1)
        if result.returncode != 0:
            return week_stats  # Not a git repo
    except:
        return week_stats
    
    # Get git log with numstat
    git_cmd = """git log --author="Remigijus" \
            --since="2025-01-01" \
            --until="2025-12-31" \
            --numstat \
            --pretty=format:"%ad" \
            --date=format:"%Y-%U" \
            2>/dev/null"""
    
    try:
        result = subprocess.run(git_cmd, shell=True, cwd=repo_path, 
                              capture_output=True, text=True)
        
        lines = result.stdout.splitlines()
        current_week = None
        
        for line in lines:
            line = line.strip()
            
            # Check if it's a date line (YYYY-WW format)
            if len(line) == 7 and line[:4].isdigit() and line[4] == '-':
                current_week = line
            # Check if it's a numstat line
            elif '\t' in line and current_week:
                parts = line.split('\t')
                if len(parts) >= 3:
                    added, deleted, filename = parts[0], parts[1], parts[2]
                    
                    # Skip uptimetea.com repo for week 01
                    if "uptimetea.com" in repo_path and current_week == "2025-01":
                        continue
                    
                    # Skip binary files (shown as -)
                    if added != '-' and deleted != '-':
                        # Check file extension
                        if not should_skip_file(filename):
                            try:
                                total = int(added) + int(deleted)
                                week_stats[current_week] += total
                            except ValueError:
                                pass
    
    except Exception:
        pass  # Silently ignore errors
    
    return week_stats


def format_number(num: int) -> str:
    """Format number with dot as thousand separator."""
    if num < 1000:
        return str(num)
    
    # Convert to string and add dots
    num_str = str(num)
    parts = []
    for i, digit in enumerate(reversed(num_str)):
        if i > 0 and i % 3 == 0:
            parts.append('.')
        parts.append(digit)
    
    return ''.join(reversed(parts))


def main():
    """Main function to calculate and display statistics."""
    # Find all repositories
    repos = find_git_repos()
    
    # Aggregate statistics from all repos
    total_stats = defaultdict(int)
    
    for repo in repos:
        repo_stats = get_repo_statistics(repo)
        for week, lines in repo_stats.items():
            total_stats[week] += lines
    
    # Sort weeks and prepare display
    if total_stats:
        sorted_weeks = sorted(total_stats.items())
        
        # Create PrettyTable
        table = PrettyTable(['Week', 'Lines'])
        table.align['Week'] = 'l'  # Left align
        table.align['Lines'] = 'r'  # Right align
        
        # Add each week
        total_lines = 0
        for week_key, lines in sorted_weeks:
            week_num = week_key.split('-')[1]  # Extract week number
            formatted_lines = format_number(lines)
            table.add_row([f"2025 W{week_num}", formatted_lines])
            total_lines += lines
        
        # Calculate average (excluding last week)
        weeks_for_avg = sorted_weeks[:-1] if len(sorted_weeks) > 1 else sorted_weeks
        total_for_avg = sum(lines for _, lines in weeks_for_avg)
        avg_lines = total_for_avg // len(weeks_for_avg) if weeks_for_avg else 0
        
        # Add separator row and totals
        table.add_row(['─' * 10, '─' * 15])
        table.add_row(['TOTAL', format_number(total_lines)])
        table.add_row(['AVG', format_number(avg_lines)])
        
        print(table)
    else:
        print("No commits found for Remigijus in 2025")


if __name__ == "__main__":
    main()
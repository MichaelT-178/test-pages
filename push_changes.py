import os
import subprocess
import sys
from termcolor import colored as c

# Set True to show full command output
DEBUG = False 

def run(cmd: str, critical: bool = True, quiet: bool = True) -> str:
    
    if DEBUG:
        quiet = False

    if not quiet:
        print(c(f"> {cmd}", "cyan"))
        
    process = subprocess.run(cmd, shell=True, text=True, capture_output=quiet)

    if critical and process.returncode != 0:
        print(c(f"\n❌ Command failed: {cmd}\n", "red"))
        
        if quiet:
            if process.stdout:
                print(process.stdout)
                
            if process.stderr:
                print(process.stderr, file=sys.stderr)
                
        sys.exit(process.returncode)

    if quiet:
        return (process.stdout or "").strip()
    
    return ""


def ensure_git_repo():
    root = run("git rev-parse --show-toplevel", critical=False)
    
    if not root:
        print(c("❌ Not inside a git repository.", "red"))
        sys.exit(1)


def current_branch() -> str:
    branch = run("git branch --show-current", critical=True)
    
    if not branch:
        print(c("❌ Detached HEAD. Checkout 'main' before deploying.", "red"))
        sys.exit(1)
        
    return branch


def verify_build():
    if not os.path.isdir("dist"):
        print(c("❌ Build verification failed: dist/ missing", "red"))
        sys.exit(1)

    if not os.path.isfile("dist/index.html"):
        print(c("❌ Build verification failed: dist/index.html missing", "red"))
        sys.exit(1)

    assets_dir = os.path.join("dist", "assets")
    
    if not os.path.isdir(assets_dir):
        print(c("❌ Build verification failed: dist/assets missing", "red"))
        sys.exit(1)

    assets = os.listdir(assets_dir)
    
    if not any(name.endswith(".js") for name in assets):
        print(c("❌ Build verification failed: no .js bundle found in dist/assets", "red"))
        sys.exit(1)
        
        
def main():
    ensure_git_repo()

    branch = current_branch()
    
    print("On branch ", end="")
    
    if branch == "main":
        print(c(branch, "green"))
    else:
        print(c(branch, "red"))
        print("Move changes to the main branch, then switch to the main branch.")
        print("git stash")
        print("git checkout main")
        print("git pull origin main")
        print(f"git merge {branch}")
        print("git stash apply")
        print("git push origin main")
        sys.exit(0)

    commit_msg = (input("Enter your commit message: ").strip() or "Update")

    print(c("\n• Committing source…", "cyan"))
    
    run("git add .", critical=True, quiet=False)
    run(f'git commit -m "{commit_msg}" || true', critical=False, quiet=False)
    run("git push origin main", critical=True, quiet=False)

    print(c("\n• Building…", "cyan"))
    run("npm run build", critical=True, quiet=False)

    run("cp dist/index.html dist/404.html", critical=True, quiet=False)

    run("touch dist/.nojekyll", critical=True, quiet=False)

    print(c("\n• Verifying build…", "cyan"))
    verify_build()
    
    print(c("✔ Build verified (index.html + assets + JS bundle).", "green"))

    # Subtree push creates/updates gh-pages from dist. This may rewrite gh-pages history.
    print(c("\n• Deploying to gh-pages (subtree)…", "cyan"))

    # Ensure dist changes are committed so subtree sees them.
    # We ONLY stage dist (forced) to avoid accidental commits of other files.
    run("git add dist -f", critical=True, quiet=False)
    run(f'git commit -m "{commit_msg} (dist)" || true', critical=False, quiet=False)
    run("git subtree push --prefix dist origin gh-pages", critical=True, quiet=False)

    print(c("\n✅ Deployment complete.", "green"))


if __name__ == "__main__":
    main()

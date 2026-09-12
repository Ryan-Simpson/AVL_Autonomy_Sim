# Create and push this GitHub repo — run these yourself

Folder and repo name: **AVL_Autonomy_Sim**  
Do **not** put this project inside `avl_simulator`.

Suggested remote (change the owner if you want the lab org instead):

`https://github.com/Ryan-Simpson/AVL_Autonomy_Sim`

Private is fine for a poster draft.

## PowerShell (this folder)

```powershell
cd C:\Users\ryanm\RMS_projects\AVL_Autonomy_Sim

git init -b main
git add README.md LICENSE .gitignore docs assets isaac ros2
git status

git commit -m "Initial AVL Autonomy Sim repo with poster abstract."

# If you already created the empty repo on github.com:
git remote add origin https://github.com/Ryan-Simpson/AVL_Autonomy_Sim.git
git push -u origin main
```

## Or create the empty repo with GitHub CLI, then push

```powershell
cd C:\Users\ryanm\RMS_projects\AVL_Autonomy_Sim
gh repo create Ryan-Simpson/AVL_Autonomy_Sim --private --source=. --remote=origin --push
```

If `gh` is not installed, create the repo in the browser (no README), then use the `git remote add` + `git push` block above.

Do not add `.env`, bags, or Isaac cache folders.

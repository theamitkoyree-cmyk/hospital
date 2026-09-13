import flet as ft
import json, os

FILE = "mydata.json"
def load():
    if not os.path.exists(FILE): return {"user": None, "posts": []}
    try:
        with open(FILE,"r",encoding="utf-8") as f: return json.load(f)
    except: return {"user": None, "posts": []}
def save(d):
    with open(FILE,"w",encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False)

def main(page: ft.Page):
    page.title = "Apna Gaon"
    page.bgcolor = "black"
    page.padding = 0

    current_type = ["Reel"]

    def close_sheet(e=None):
        sheet.open = False
        page.update()

    # UPLOAD PAGE - ab popup nahi, direct page khulega
    def show_upload_page(t):
        current_type[0] = t
        page.clean()
        caption = ft.TextField(label="Caption likho...", width=320, bgcolor="white", color="black", border_radius=12, multiline=True)
        file_name = ft.TextField(label=f"{t} File Name", width=320, bgcolor="white", color="black", border_radius=12, value=f"my_{t.lower()}.mp4")

        def do_final_upload(e):
            d = load()
            d["posts"].append({"type": t, "file": file_name.value, "caption": caption.value})
            d["user"]["posts_count"] = str(len(d["posts"]))
            save(d)
            show_profile()

        def pick_camera(e):
            # Camera ka simulation - mobile me yahan camera khulega
            file_name.value = f"camera_{t.lower()}_captured.mp4"
            page.update()
            page.snack_bar = ft.SnackBar(ft.Text("Camera se photo liya gaya (Simulation)"))
            page.snack_bar.open = True
            page.update()

        page.add(
            ft.Column([
                ft.Container(padding=15, content=ft.Row([ft.Text("←", color="white", size=24, weight="bold"), ft.Text(f"New {t}", color="white", size=18, weight="bold")], spacing=10)),
                ft.Container(padding=15, content=ft.Column([
                    ft.Container(height=200, width=320, bgcolor="#222", border_radius=10, alignment=ft.Alignment(0,0), content=ft.Column([ft.Text("📁", size=40), ft.Text(f"{t} Preview", color="grey")], horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                    ft.Container(height=10),
                    ft.Row([ft.ElevatedButton("📁 Gallery", on_click=lambda e: pick_camera(e), width=150, bgcolor="#333", color="white"), ft.ElevatedButton("📷 Camera", on_click=pick_camera, width=150, bgcolor="#333", color="white")], spacing=10),
                    file_name,
                    caption,
                    ft.ElevatedButton(f"Upload {t}", on_click=do_final_upload, width=320, bgcolor="#d62976", color="white", height=50),
                    ft.TextButton("Cancel", on_click=lambda e: show_profile())
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
            ], scroll=ft.ScrollMode.AUTO, expand=True)
        )

    def create_option(icon, text, is_new=False):
        return ft.Container(
            padding=18,
            on_click=lambda e, txt=text: (setattr(sheet, 'open', False), page.update(), show_upload_page(txt)),
            content=ft.Row([
                ft.Text(icon, color="white", size=22),
                ft.Text(text, color="white", size=16),
                ft.Container(expand=True),
                ft.Container(bgcolor="#3a5bff", border_radius=20, padding=10, content=ft.Text("New", color="white", size=10)) if is_new else ft.Container()
            ], spacing=15)
        )

    sheet = ft.BottomSheet(
        bgcolor="#121212",
        content=ft.Column([
            ft.Container(padding=15, alignment=ft.Alignment(0,0), content=ft.Column([
                ft.Container(width=40, height=4, bgcolor="grey", border_radius=10),
                ft.Container(height=10),
                ft.Text("Create", color="white", size=20, weight="bold"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
            ft.Container(height=1, bgcolor="#222"),
            create_option("▶", "Reel"),
            ft.Container(height=1, bgcolor="#222"),
            create_option("◫", "Edits", is_new=True),
            ft.Container(height=1, bgcolor="#222"),
            create_option("⊞", "Post"),
            ft.Container(height=1, bgcolor="#222"),
            create_option("⊕", "Story"),
            ft.Container(height=1, bgcolor="#222"),
            create_option("♡", "Highlights"),
            ft.Container(height=1, bgcolor="#222"),
            create_option("((•))", "Live"),
            ft.Container(height=1, bgcolor="#222"),
            create_option("↗", "Ad"),
            ft.Container(height=1, bgcolor="#222"),
            create_option("💬", "Channel"),
            ft.Container(height=30)
        ], spacing=0, scroll=ft.ScrollMode.AUTO),
    )
    page.overlay.append(sheet)

    def open_create(e):
        sheet.open = True
        page.update()

    def show_profile():
        page.clean()
        d = load()
        u = d["user"]
        posts_grid = ft.Row([ft.Container(width=110, height=110, bgcolor="#222", border_radius=5, alignment=ft.Alignment(0,0), content=ft.Column([ft.Text(p.get("type","Post"), color="white", size=12, weight="bold"), ft.Text(p.get("file","")[:15], color="grey", size=8)], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)) for p in d.get("posts",[])[-9:]], wrap=True, spacing=5) if d.get("posts") else ft.Container(padding=20, content=ft.Text("+ pe click karke Reel/Post upload karo", color="grey"))

        col = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=[
            ft.Container(padding=15, content=ft.Row([
                ft.Container(content=ft.Text("+", color="white", size=28), on_click=open_create),
                ft.Row([ft.Text(u.get("username",""), color="white", size=18, weight="bold"), ft.Text(" v 🔵", color="white")], expand=True, alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("☰", color="white", size=20)
            ])),
            ft.Container(padding=15, content=ft.Row([
                ft.Container(width=75, height=75, border_radius=40, gradient=ft.LinearGradient(colors=["#feda75","#d62976","#4f5bd5"]), padding=3, content=ft.Container(bgcolor="black", border_radius=40, alignment=ft.Alignment(0,0), content=ft.Container(bgcolor="#333", border_radius=40, alignment=ft.Alignment(0,0), content=ft.Text(u.get("username","A")[0].upper(), color="white", size=28)))),
                ft.Row([ft.Column([ft.Text(u.get("posts_count","0"), color="white", weight="bold"), ft.Text("posts", color="white", size=11)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), ft.Column([ft.Text(u.get("followers","0"), color="white", weight="bold"), ft.Text("followers", color="white", size=11)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), ft.Column([ft.Text(u.get("following","0"), color="white", weight="bold"), ft.Text("following", color="white", size=11)], horizontal_alignment=ft.CrossAxisAlignment.CENTER)], spacing=25, expand=True, alignment=ft.MainAxisAlignment.CENTER)
            ])),
            ft.Container(padding=15, content=ft.Column([ft.Text(f"{u.get('name','')} 🔵", color="white", weight="bold"), ft.Text(u.get("line1",""), color="white", size=13), ft.Text(u.get("line2",""), color="white", size=13), ft.Text(u.get("link",""), color="#6aa6ff", size=12)])),
            ft.Container(padding=10, content=ft.Row([
                ft.Container(expand=True, bgcolor="white", border_radius=8, padding=12, alignment=ft.Alignment(0,0), content=ft.Text("Edit profile", color="black", size=12, weight="bold"), on_click=lambda e: show_edit()),
                ft.Container(expand=True, bgcolor="#333", border_radius=8, padding=12, alignment=ft.Alignment(0,0), content=ft.Text("Logout", color="white", size=11), on_click=lambda e: (os.remove(FILE) if os.path.exists(FILE) else None, show_register())),
            ], spacing=6)),
            ft.Container(padding=10, content=posts_grid)
        ])
        bottom = ft.Container(bgcolor="black", padding=12, content=ft.Row([ft.Text("⌂", color="white", size=22), ft.Text("◎", color="grey", size=22), ft.Text("⊞", color="grey", size=22), ft.Text("♡", color="grey", size=22)], alignment=ft.MainAxisAlignment.SPACE_AROUND))
        page.add(col, bottom)

    def show_edit():
        page.clean()
        u = load()["user"]
        name = ft.TextField(label="Full Name", width=300, bgcolor="white", color="black", border_radius=12, value=u.get("name",""))
        line1 = ft.TextField(label="Bio Line 1", width=300, bgcolor="white", color="black", border_radius=12, value=u.get("line1",""))
        line2 = ft.TextField(label="Bio Line 2", width=300, bgcolor="white", color="black", border_radius=12, value=u.get("line2",""))
        link = ft.TextField(label="Link", width=300, bgcolor="white", color="black", border_radius=12, value=u.get("link",""))
        followers = ft.TextField(label="Followers", width=90, bgcolor="white", color="black", border_radius=12, value=str(u.get("followers","0")))
        following = ft.TextField(label="Following", width=90, bgcolor="white", color="black", border_radius=12, value=str(u.get("following","0")))
        posts_c = ft.TextField(label="Posts", width=90, bgcolor="white", color="black", border_radius=12, value=str(u.get("posts_count","0")))
        def save_edit(e):
            d = load()
            d["user"].update({"name": name.value, "line1": line1.value, "line2": line2.value, "link": link.value, "followers": followers.value, "following": following.value, "posts_count": posts_c.value})
            save(d)
            show_profile()
        page.add(ft.Column([ft.Text("Edit Profile", color="white", size=22, weight="bold"), ft.Container(bgcolor="white", border_radius=20, padding=15, content=ft.Column([name, line1, line2, link, ft.Row([followers, following, posts_c], spacing=8), ft.ElevatedButton("Save", on_click=save_edit, width=300, bgcolor="#d62976", color="white"), ft.TextButton("Back", on_click=lambda e: show_profile())]))], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True))

    def show_register():
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        uname = ft.TextField(label="Username*", width=300, bgcolor="white", color="black", border_radius=15)
        pwd = ft.TextField(label="Password*", password=True, width=300, bgcolor="white", color="black", border_radius=15)
        def do_reg(e):
            if uname.value=="" or pwd.value=="": return
            save({"user": {"username": uname.value, "password": pwd.value, "name": uname.value, "line1": "", "line2": "", "link": "", "followers": "0", "following": "0", "posts_count": "0"}, "posts": []})
            show_profile()
        page.add(ft.Column([ft.Text("Apna Gaon", color="white", size=30, weight="bold"), uname, pwd, ft.ElevatedButton("Register", on_click=do_reg, width=300, bgcolor="#d62976", color="white"), ft.TextButton("Login", on_click=lambda e: show_login())], horizontal_alignment=ft.CrossAxisAlignment.CENTER))

    def show_login():
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        uname = ft.TextField(label="Username", width=300, bgcolor="white", color="black", border_radius=15)
        pwd = ft.TextField(label="Password", password=True, width=300, bgcolor="white", color="black", border_radius=15)
        def do_login(e):
            d = load()
            if d["user"] and uname.value==d["user"]["username"] and pwd.value==d["user"]["password"]:
                show_profile()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Wrong username/password"))
                page.snack_bar.open = True
                page.update()
        page.add(ft.Column([ft.Text("Login", color="white", size=28, weight="bold"), uname, pwd, ft.ElevatedButton("Log In", on_click=do_login, width=300, bgcolor="#d62976", color="white"), ft.TextButton("Create account", on_click=lambda e: show_register())], horizontal_alignment=ft.CrossAxisAlignment.CENTER))

    d = load()
    if not d["user"]: show_register()
    else: show_profile()

ft.run(main)

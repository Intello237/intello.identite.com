@app.route("/inscription", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        wallet = request.form.get("wallet")
        photo = request.files.get("photo")

        if not username or not wallet or not photo:
            flash("Tous les champs sont requis.", "error")
            return redirect(url_for("register"))

        # Vérification doublon
        if is_duplicate(username):
            flash("Nom déjà utilisé. Usurpation détectée.", "error")
            return redirect(url_for("register"))

        hashed_name = hashlib.sha256(username.encode()).hexdigest()
        db = load_db()
        db[username] = hashed_name
        save_db(db)

        photo.save(f"static/uploads/{username}.png")
        flash("Inscription réussie avec profil sécurisé.", "success")
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/connexion", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        wallet = request.form.get("wallet")

        db = load_db()
        if username in db:
            flash("Connexion réussie.", "success")
        else:
            flash("Échec de la connexion.", "error")
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route('/cryptoinfo/<int:id>', methods=["GET", "POST"])
def crypto_info(id):
    request_crypto = db.get_or_404(CryptoInfo, id) 
    return render_template("cryptoinfo.html", request_crypto=request_crypto)